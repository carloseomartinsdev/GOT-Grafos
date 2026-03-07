const isMobile = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth <= 600;

        let scene, camera, renderer, controls;
        let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false, sprint = false;
        const velocity = new THREE.Vector3();
        const direction = new THREE.Vector3();
        let prevTime = performance.now();
        // Rotação manual para mobile (sem PointerLock)
        let mobileYaw = 0, mobilePitch = 0;
        
        let allNodes = [];
        let allEdges = [];
        let graphData = null;
        let selectedCharacter = null;
        let hiddenCommunities = new Set();
        let raycaster = new THREE.Raycaster();
        let mouse = new THREE.Vector2();
        let imageCache = {};
        let pathCharacters = new Set();
        let pathLines = [];
        
        const communityNames = [
            'Stark/Norte',
            'Lannister',
            'Targaryen',
            'Night\'s Watch',
            'Baratheon',
            'Outros',
            'Secundários',
            'Terciários'
        ];

        function init() {
            // Scene
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x000000);

            // Camera
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 20000);
            camera.position.set(0, 0, 15000);

            // Renderer
            renderer = new THREE.WebGLRenderer({ antialias: !isMobile });
            renderer.setPixelRatio(isMobile ? 1 : window.devicePixelRatio);
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.body.appendChild(renderer.domElement);

            // PointerLock Controls
            controls = new THREE.PointerLockControls(camera, document.body);
            scene.add(controls.getObject());

            // Teclado
            document.addEventListener('keydown', onKeyDown);
            document.addEventListener('keyup', onKeyUp);
            
            // Click para selecionar personagem
            document.addEventListener('click', onMouseClick);

            // Estrelas
            createStars();

            // Carregar dados
            loadData();

            // Resize
            window.addEventListener('resize', onWindowResize);

            animate();
        }

        function onKeyDown(event) {
            switch (event.code) {
                case 'KeyW': moveForward = true; break;
                case 'KeyS': moveBackward = true; break;
                case 'KeyA': moveLeft = true; break;
                case 'KeyD': moveRight = true; break;
                case 'ShiftLeft': sprint = true; break;
                case 'Tab': 
                    event.preventDefault();
                    if (!isMobile) {
                        if (controls.isLocked) controls.unlock();
                        else controls.lock();
                    }
                    break;
            }
        }

        function onKeyUp(event) {
            switch (event.code) {
                case 'KeyW': moveForward = false; break;
                case 'KeyS': moveBackward = false; break;
                case 'KeyA': moveLeft = false; break;
                case 'KeyD': moveRight = false; break;
                case 'ShiftLeft': sprint = false; break;
            }
        }
        
        function onMouseClick(event) {
            if (controls.isLocked || isMobile) return;
            doRaycast(event.clientX, event.clientY);
        }

        function doRaycast(clientX, clientY) {
            mouse.x = (clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(clientY / window.innerHeight) * 2 + 1;
            raycaster.setFromCamera(mouse, camera);
            const sprites = allNodes.map(n => n.sphere);
            const intersects = raycaster.intersectObjects(sprites);
            if (intersects.length > 0) {
                const charName = intersects[0].object.userData.name;
                document.getElementById('charList').value = charName;
                selectCharacter();
            }
        }

        function createStars() {
            const starsGeometry = new THREE.BufferGeometry();
            const starsMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 2 });
            
            const starsVertices = [];
            for (let i = 0; i < 5000; i++) {
                const x = (Math.random() - 0.5) * 50000;
                const y = (Math.random() - 0.5) * 50000;
                const z = (Math.random() - 0.5) * 50000;
                starsVertices.push(x, y, z);
            }
            
            starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
            const stars = new THREE.Points(starsGeometry, starsMaterial);
            scene.add(stars);
        }

        function createCubeGrid() {
            // Grid removido
        }

        async function loadData() {
            try {
                graphData = await loadJSON('graph_data');
                
                document.getElementById('loading').style.display = 'none';
                document.getElementById('nodeCount').textContent = graphData.nodes.length;
                document.getElementById('edgeCount').textContent = graphData.edges.length;
                
                createGraph(graphData);
                setupControls(graphData);
            } catch (error) {
                console.error('Erro ao carregar dados:', error);
                document.getElementById('loading').textContent = 'Erro ao carregar dados. Execute gerar_dados_grafo.py primeiro.';
            }
        }
        
        function setupControls(data) {
            // Lista de personagens
            const charList = document.getElementById('charList');
            const searchInput = document.getElementById('searchChar');
            const searchFrom = document.getElementById('searchFrom');
            const searchTo = document.getElementById('searchTo');
            
            const sortedChars = data.nodes.map(n => n.id).sort();
            sortedChars.forEach(char => {
                const option = document.createElement('option');
                option.value = char;
                option.textContent = char;
                charList.appendChild(option);
                
                const optionFrom = document.createElement('option');
                optionFrom.value = char;
                optionFrom.textContent = char;
                searchFrom.appendChild(optionFrom);
                
                const optionTo = document.createElement('option');
                optionTo.value = char;
                optionTo.textContent = char;
                searchTo.appendChild(optionTo);
            });
            
            searchInput.addEventListener('input', (e) => {
                const search = e.target.value.toLowerCase();
                Array.from(charList.options).forEach(opt => {
                    opt.style.display = opt.value.toLowerCase().includes(search) ? '' : 'none';
                });
            });
            
            // Filtros de comunidade
            const communities = [...new Set(data.nodes.map(n => n.community))].sort();
            const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffa500', '#800080'];
            const filtersDiv = document.getElementById('communityFilters');
            
            communities.forEach(comm => {
                const div = document.createElement('div');
                div.className = 'community-filter';
                const commName = communityNames[comm] || `Comunidade ${comm}`;
                div.innerHTML = `
                    <input type="checkbox" id="comm${comm}" checked onchange="toggleCommunity(${comm})" />
                    <label for="comm${comm}" style="color: ${colors[comm % colors.length]}">${commName}</label>
                `;
                filtersDiv.appendChild(div);
            });
        }
        
        function selectCharacter() {
            const charList = document.getElementById('charList');
            const selected = charList.value;
            if (!selected) return;
            
            selectedCharacter = selected;
            
            // Mostrar informações
            const nodeData = graphData.nodes.find(n => n.id === selected);
            if (nodeData) {
                // Calcular ranks
                const influenceRank = graphData.nodes.sort((a,b) => b.influence_score - a.influence_score).findIndex(n => n.id === selected) + 1;
                const pagerankRank = graphData.nodes.sort((a,b) => b.pagerank - a.pagerank).findIndex(n => n.id === selected) + 1;
                const betweennessRank = graphData.nodes.sort((a,b) => b.betweenness - a.betweenness).findIndex(n => n.id === selected) + 1;
                const weightedRank = graphData.nodes.sort((a,b) => b.weighted_degree - a.weighted_degree).findIndex(n => n.id === selected) + 1;
                
                const commName = communityNames[nodeData.community] || `Comunidade ${nodeData.community}`;
                const imgPath = getCharacterImage(selected);
                
                document.getElementById('charPhoto').src = imgPath;
                document.getElementById('charName').textContent = selected;
                document.getElementById('charCommunity').textContent = commName;
                document.getElementById('charFamilia').textContent = nodeData.familia || 'N/A';
                document.getElementById('charInfluence').textContent = `${nodeData.influence_score.toFixed(4)} (#${influenceRank})`;
                document.getElementById('charPageRank').textContent = `${nodeData.pagerank.toFixed(4)} (#${pagerankRank})`;
                document.getElementById('charBetweenness').textContent = `${nodeData.betweenness.toFixed(4)} (#${betweennessRank})`;
                document.getElementById('charConnections').textContent = `${nodeData.connections} (peso: ${Math.round(nodeData.weighted_degree)} #${weightedRank})`;
                document.getElementById('charInfo').style.display = 'block';
                if (isMobile) document.getElementById('pathVisual').style.display = 'none';
            }
            
            updateVisibility();
        }
        
        function centerOnCharacter() {
            if (!selectedCharacter) return;
            
            const nodeData = graphData.nodes.find(n => n.id === selectedCharacter);
            if (nodeData) {
                const distance = 500;
                camera.position.set(
                    nodeData.x,
                    nodeData.y,
                    nodeData.z + distance
                );
            }
        }
        
        function clearSelection() {
            selectedCharacter = null;
            document.getElementById('charInfo').style.display = 'none';
            clearPath();
            updateVisibility();
        }
        
        function findPath() {
            const from = document.getElementById('searchFrom').value;
            const to = document.getElementById('searchTo').value;
            
            if (!from || !to) {
                alert('Selecione ambos os personagens');
                return;
            }
            
            // Construir grafo para busca
            const G = {};
            graphData.edges.forEach(edge => {
                if (!G[edge.source]) G[edge.source] = [];
                if (!G[edge.target]) G[edge.target] = [];
                G[edge.source].push(edge.target);
                G[edge.target].push(edge.source);
            });
            
            // BFS para encontrar caminho mais curto
            const path = bfs(G, from, to);
            
            if (!path) {
                document.getElementById('pathResult').innerHTML = '<p style="color: #ff5555;">Sem caminho entre esses personagens</p>';
                document.getElementById('pathResult').style.display = 'block';
                return;
            }
            
            // Mostrar resultado
            const pathText = path.join(' → ');
            document.getElementById('pathResult').innerHTML = `
                <p style="color: #4CAF50;"><strong>Caminho encontrado (${path.length - 1} conexões):</strong></p>
                <p>${pathText}</p>
            `;
            document.getElementById('pathResult').style.display = 'block';
            
            // Destacar caminho no visualizador
            highlightPath(path);
        }
        
        function bfs(graph, start, end) {
            const queue = [[start]];
            const visited = new Set([start]);
            
            while (queue.length > 0) {
                const path = queue.shift();
                const node = path[path.length - 1];
                
                if (node === end) return path;
                
                const neighbors = graph[node] || [];
                for (const neighbor of neighbors) {
                    if (!visited.has(neighbor)) {
                        visited.add(neighbor);
                        queue.push([...path, neighbor]);
                    }
                }
            }
            return null;
        }
        
        function highlightPath(path) {
            clearPath();
            if (isMobile) document.getElementById('charInfo').style.display = 'none';
            
            // Armazenar personagens do caminho
            pathCharacters = new Set(path);
            
            // Criar linhas amarelas para o caminho
            for (let i = 0; i < path.length - 1; i++) {
                const fromNode = graphData.nodes.find(n => n.id === path[i]);
                const toNode = graphData.nodes.find(n => n.id === path[i + 1]);
                
                if (fromNode && toNode) {
                    const start = new THREE.Vector3(fromNode.x, fromNode.y, fromNode.z);
                    const end = new THREE.Vector3(toNode.x, toNode.y, toNode.z);
                    
                    const geometry = new THREE.BufferGeometry().setFromPoints([start, end]);
                    const material = new THREE.LineBasicMaterial({ 
                        color: 0xffff00, 
                        transparent: true, 
                        opacity: 0.9,
                        linewidth: 3
                    });
                    const line = new THREE.Line(geometry, material);
                    scene.add(line);
                    pathLines.push(line);
                }
            }
            
            // Criar visualização do caminho
            const pathVisual = document.getElementById('pathVisual');
            const container = pathVisual.querySelector('.path-container');
            container.innerHTML = '';
            
            path.forEach((char, idx) => {
                const charItem = document.createElement('div');
                charItem.className = 'char-item';
                
                const img = document.createElement('img');
                img.src = `../resources/imagens/personagens/${char.replace(/ /g, '_').replace(/\//g, '_')}.jpg`;
                img.title = char;
                
                const name = document.createElement('div');
                name.className = 'char-name';
                name.textContent = char;
                
                charItem.appendChild(img);
                charItem.appendChild(name);
                container.appendChild(charItem);
                
                if (idx < path.length - 1) {
                    const arrow = document.createElement('span');
                    arrow.className = 'arrow';
                    arrow.textContent = '→';
                    container.appendChild(arrow);
                }
            });
            
            pathVisual.style.display = 'block';
            updateVisibility();
        }
        
        function clearPath() {
            pathLines.forEach(line => scene.remove(line));
            pathLines = [];
            pathCharacters.clear();
            document.getElementById('pathResult').style.display = 'none';
            document.getElementById('pathVisual').style.display = 'none';
        }
        
        function toggleControls() {
            document.getElementById('controls').classList.toggle('minimized');
        }
        
        function showTab(tab) {
            document.getElementById('contentPersonagem').style.display = tab === 'personagem' ? 'block' : 'none';
            document.getElementById('contentCaminho').style.display = tab === 'caminho' ? 'block' : 'none';
            document.getElementById('contentComunidades').style.display = tab === 'comunidades' ? 'block' : 'none';
            
            document.getElementById('tabPersonagem').style.background = tab === 'personagem' ? '#d4b76a' : '#c9a961';
            document.getElementById('tabCaminho').style.background = tab === 'caminho' ? '#d4b76a' : '#c9a961';
            document.getElementById('tabComunidades').style.background = tab === 'comunidades' ? '#d4b76a' : '#c9a961';
        }
        
        function toggleCommunity(commId) {
            const checkbox = document.getElementById(`comm${commId}`);
            if (checkbox.checked) {
                hiddenCommunities.delete(commId);
            } else {
                hiddenCommunities.add(commId);
            }
            updateVisibility();
        }
        
        function updateVisibility() {
            if (!graphData) return;
            
            // Encontrar conexões do personagem selecionado
            let connectedChars = new Set();
            if (selectedCharacter) {
                connectedChars.add(selectedCharacter);
                graphData.edges.forEach(edge => {
                    if (edge.source === selectedCharacter) connectedChars.add(edge.target);
                    if (edge.target === selectedCharacter) connectedChars.add(edge.source);
                });
            }
            
            // Atualizar visibilidade dos nós
            allNodes.forEach(node => {
                const nodeData = graphData.nodes.find(n => n.id === node.id);
                if (!nodeData) return;
                
                let visible = !hiddenCommunities.has(nodeData.community);
                
                if (pathCharacters.size > 0) {
                    visible = pathCharacters.has(nodeData.id);
                } else if (selectedCharacter) {
                    visible = connectedChars.has(nodeData.id) && !hiddenCommunities.has(nodeData.community);
                }
                
                node.sphere.visible = visible;
                node.label.visible = visible;
                node.ring.visible = visible;
            });
            
            // Atualizar visibilidade das arestas
            const colors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff, 0x00ffff, 0xffa500, 0x800080];
            
            allEdges.forEach(edge => {
                let visible = false;
                let edgeColor = 0xcccccc;
                let edgeOpacity = 0.5;
                
                if (pathCharacters.size > 0) {
                    visible = false;
                } else if (selectedCharacter) {
                    if (edge.source === selectedCharacter || edge.target === selectedCharacter) {
                        visible = true;
                        const selectedNode = graphData.nodes.find(n => n.id === selectedCharacter);
                        if (selectedNode) {
                            edgeColor = colors[selectedNode.community % colors.length];
                            edgeOpacity = 0.8;
                        }
                    }
                } else {
                    const sourceNode = graphData.nodes.find(n => n.id === edge.source);
                    const targetNode = graphData.nodes.find(n => n.id === edge.target);
                    
                    if (sourceNode && targetNode) {
                        visible = !hiddenCommunities.has(sourceNode.community) && !hiddenCommunities.has(targetNode.community);
                    }
                }
                
                edge.line.visible = visible;
                edge.line.material.color.setHex(edgeColor);
                edge.line.material.opacity = edgeOpacity;
            });
        }

        const TEX_SIZE = isMobile ? 128 : 512;
        const FONT_SIZE = isMobile ? 20 : 80;
        const FONT_OFFSET = isMobile ? 70 : 280;
        const HALF = TEX_SIZE / 2;

        function drawCircularImage(ctx, img, color, name) {
            ctx.clearRect(0, 0, TEX_SIZE, TEX_SIZE);
            if (img) {
                ctx.beginPath();
                ctx.arc(HALF, HALF, HALF, 0, Math.PI * 2);
                ctx.clip();
                ctx.drawImage(img, 0, 0, TEX_SIZE, TEX_SIZE);
            } else {
                ctx.fillStyle = `#${color.toString(16).padStart(6, '0')}`;
                ctx.beginPath();
                ctx.arc(HALF, HALF, HALF, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = 'white';
                ctx.font = `bold ${FONT_SIZE}px Arial`;
                ctx.textAlign = 'center';
                ctx.fillText(name.substring(0, 2), HALF, FONT_OFFSET);
            }
        }
        
        function createGraph(data) {
            const colors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff, 0x00ffff, 0xffa500, 0x800080];
            
            allNodes = [];
            allEdges = [];
            
            // Criar nós (personagens)
            const nodePositions = {};
            data.nodes.forEach((node, idx) => {
                // Criar sprite com foto (sempre voltado para câmera)
                const imgPath = getCharacterImage(node.id);
                
                const spriteMaterial = new THREE.SpriteMaterial({ 
                    transparent: true
                });
                const sprite = new THREE.Sprite(spriteMaterial);
                
                // Canvas com foto circular
                const photoCanvas = document.createElement('canvas');
                photoCanvas.width = TEX_SIZE;
                photoCanvas.height = TEX_SIZE;
                const photoCtx = photoCanvas.getContext('2d');
                
                // Verificar cache
                if (imageCache[imgPath]) {
                    drawCircularImage(photoCtx, imageCache[imgPath], colors[node.community % colors.length], node.id);
                    const texture = new THREE.CanvasTexture(photoCanvas);
                    sprite.material.map = texture;
                    sprite.material.needsUpdate = true;
                } else {
                    const img = new Image();
                    img.crossOrigin = 'anonymous';
                    img.onload = () => {
                        imageCache[imgPath] = img;
                        drawCircularImage(photoCtx, img, colors[node.community % colors.length], node.id);
                        sprite.material.map = new THREE.CanvasTexture(photoCanvas);
                        sprite.material.needsUpdate = true;
                    };
                    img.onerror = () => {
                        drawCircularImage(photoCtx, null, colors[node.community % colors.length], node.id);
                        sprite.material.map = new THREE.CanvasTexture(photoCanvas);
                        sprite.material.needsUpdate = true;
                    };
                    img.src = imgPath;
                }
                sprite.scale.set(node.size * 2, node.size * 2, 1);
                sprite.position.set(node.x, node.y, node.z);
                sprite.userData = { name: node.id, pagerank: node.pagerank };
                
                // Borda colorida (círculo)
                const canvas = document.createElement('canvas');
                canvas.width = TEX_SIZE;
                canvas.height = TEX_SIZE;
                const ctx = canvas.getContext('2d');
                ctx.strokeStyle = `#${colors[node.community % colors.length].toString(16).padStart(6, '0')}`;
                ctx.lineWidth = isMobile ? 5 : 20;
                ctx.beginPath();
                ctx.arc(HALF, HALF, HALF - (isMobile ? 3 : 16), 0, Math.PI * 2);
                ctx.stroke();
                
                const ringTexture = new THREE.CanvasTexture(canvas);
                const ringMaterial = new THREE.SpriteMaterial({ 
                    map: ringTexture,
                    transparent: true
                });
                const ring = new THREE.Sprite(ringMaterial);
                ring.scale.set(node.size * 2.2, node.size * 2.2, 1);
                ring.position.set(node.x, node.y, node.z);
                
                nodePositions[node.id] = sprite.position;
                scene.add(sprite);
                scene.add(ring);

                let labelSprite;
                if (!isMobile) {
                    const labelCanvas = document.createElement('canvas');
                    const context = labelCanvas.getContext('2d');
                    labelCanvas.width = 256;
                    labelCanvas.height = 64;
                    context.fillStyle = 'white';
                    context.font = '20px Arial';
                    context.fillText(node.id, 10, 30);
                    const labelTexture = new THREE.CanvasTexture(labelCanvas);
                    const labelMaterial = new THREE.SpriteMaterial({ map: labelTexture });
                    labelSprite = new THREE.Sprite(labelMaterial);
                    labelSprite.position.set(node.x, node.y + node.size + 50, node.z);
                    labelSprite.scale.set(300, 75, 1);
                    scene.add(labelSprite);
                } else {
                    // Sprite vazio para não quebrar referências
                    labelSprite = new THREE.Sprite(new THREE.SpriteMaterial());
                    labelSprite.visible = false;
                }
                
                allNodes.push({ sphere: sprite, label: labelSprite, ring, id: node.id });
            });

            // Criar arestas (conexões) — no mobile limita para reduzir uso de memória
            const MAX_EDGES = isMobile ? 300 : Infinity;
            let edgeCount = 0;
            // Ordenar por peso para manter as mais relevantes
            const sortedEdges = isMobile
                ? [...data.edges].sort((a, b) => (b.weight || 0) - (a.weight || 0)).slice(0, MAX_EDGES)
                : data.edges;

            sortedEdges.forEach(edge => {
                const sourceNode = data.nodes.find(n => n.id === edge.source);
                const targetNode = data.nodes.find(n => n.id === edge.target);
                
                if (sourceNode && targetNode) {
                    const start = new THREE.Vector3(sourceNode.x, sourceNode.y, sourceNode.z);
                    const end = new THREE.Vector3(targetNode.x, targetNode.y, targetNode.z);
                    
                    const geometry = new THREE.BufferGeometry().setFromPoints([start, end]);
                    const material = new THREE.LineBasicMaterial({ 
                        color: 0xcccccc, 
                        transparent: true, 
                        opacity: 0.5,
                        linewidth: 1
                    });
                    const line = new THREE.Line(geometry, material);
                    scene.add(line);
                    
                    allEdges.push({ line, source: edge.source, target: edge.target, weight: edge.weight });
                }
            });
        }

        function animate() {
            requestAnimationFrame(animate);

            const time = performance.now();
            const delta = (time - prevTime) / 1000;

            if (isMobile) {
                // Aplicar rotação manual no mobile
                camera.rotation.order = 'YXZ';
                camera.rotation.y = mobileYaw;
                camera.rotation.x = mobilePitch;

                if (moveForward || moveBackward || moveLeft || moveRight) {
                    velocity.x -= velocity.x * 10.0 * delta;
                    velocity.z -= velocity.z * 10.0 * delta;
                    velocity.y -= velocity.y * 10.0 * delta;
                    const speed = 4000.0 * delta;
                    if (moveForward || moveBackward) {
                        camera.getWorldDirection(direction);
                        const s = moveForward ? 1 : -1;
                        velocity.x += direction.x * speed * s;
                        velocity.y += direction.y * speed * s;
                        velocity.z += direction.z * speed * s;
                    }
                    if (moveLeft || moveRight) {
                        camera.getWorldDirection(direction);
                        const right = new THREE.Vector3();
                        right.crossVectors(camera.up, direction).normalize();
                        const s = moveRight ? 1 : -1;
                        velocity.x -= right.x * speed * s;
                        velocity.z -= right.z * speed * s;
                    }
                    camera.position.x += velocity.x * delta;
                    camera.position.y += velocity.y * delta;
                    camera.position.z += velocity.z * delta;
                }
            } else if (controls.isLocked) {
                velocity.x -= velocity.x * 10.0 * delta;
                velocity.z -= velocity.z * 10.0 * delta;
                velocity.y -= velocity.y * 10.0 * delta;

                direction.z = Number(moveForward) - Number(moveBackward);
                direction.x = Number(moveRight) - Number(moveLeft);
                direction.normalize();

                const speed = (sprint ? 15000.0 : 4000.0) * delta;

                // Movimento livre em 3D baseado na direção da câmera
                if (moveForward || moveBackward) {
                    camera.getWorldDirection(direction);
                    velocity.x += direction.x * speed * (moveForward ? 1 : -1);
                    velocity.y += direction.y * speed * (moveForward ? 1 : -1);
                    velocity.z += direction.z * speed * (moveForward ? 1 : -1);
                }
                if (moveLeft || moveRight) {
                    camera.getWorldDirection(direction);
                    const right = new THREE.Vector3();
                    right.crossVectors(camera.up, direction).normalize();
                    velocity.x -= right.x * speed * (moveRight ? 1 : -1);
                    velocity.z -= right.z * speed * (moveRight ? 1 : -1);
                }

                controls.getObject().position.x += velocity.x * delta;
                controls.getObject().position.y += velocity.y * delta;
                controls.getObject().position.z += velocity.z * delta;
            }

            prevTime = time;
            renderer.render(scene, camera);
        }

        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }

        init();
        setupMobileControls();
        
        window.addEventListener('load', () => {
            showTab('personagem');
        });

        function resetView() {
            camera.position.set(0, 0, 15000);
            mobileYaw = 0;
            mobilePitch = 0;
            velocity.set(0, 0, 0);
            clearSelection();
        }

        function setupMobileControls() {
            const joystick = document.getElementById('joystick');
            const knob = document.getElementById('joystickKnob');
            if (!joystick) return;

            let joyActive = false;
            let joyOrigin = { x: 0, y: 0 };
            const maxDist = 30;

            joystick.addEventListener('touchstart', e => {
                e.preventDefault();
                joyActive = true;
                const t = e.touches[0];
                const rect = joystick.getBoundingClientRect();
                joyOrigin = { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 };
            }, { passive: false });

            joystick.addEventListener('touchmove', e => {
                e.preventDefault();
                if (!joyActive) return;
                const t = e.touches[0];
                let dx = t.clientX - joyOrigin.x;
                let dy = t.clientY - joyOrigin.y;
                const dist = Math.min(Math.sqrt(dx*dx + dy*dy), maxDist);
                const angle = Math.atan2(dy, dx);
                dx = Math.cos(angle) * dist;
                dy = Math.sin(angle) * dist;
                knob.style.transform = `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`;
                const nx = dx / maxDist;
                const ny = dy / maxDist;
                moveForward = ny < -0.3;
                moveBackward = ny > 0.3;
                moveLeft = nx < -0.3;
                moveRight = nx > 0.3;
            }, { passive: false });

            const endJoy = () => {
                joyActive = false;
                knob.style.transform = 'translate(-50%, -50%)';
                moveForward = moveBackward = moveLeft = moveRight = false;
            };
            joystick.addEventListener('touchend', endJoy);
            joystick.addEventListener('touchcancel', endJoy);

            // Pan com 1 dedo no canvas = rotacionar câmera
            let panLast = null;
            let lastPinchDist = 0;
            renderer.domElement.addEventListener('touchstart', e => {
                e.preventDefault();
                if (e.touches.length === 1) panLast = { x: e.touches[0].clientX, y: e.touches[0].clientY };
                if (e.touches.length === 2) {
                    const dx = e.touches[0].clientX - e.touches[1].clientX;
                    const dy = e.touches[0].clientY - e.touches[1].clientY;
                    lastPinchDist = Math.sqrt(dx*dx + dy*dy);
                    panLast = null;
                }
            }, { passive: false });
            renderer.domElement.addEventListener('touchmove', e => {
                e.preventDefault();
                if (e.touches.length === 1 && panLast) {
                    const dx = e.touches[0].clientX - panLast.x;
                    const dy = e.touches[0].clientY - panLast.y;
                    mobileYaw   += dx * 0.003;
                    mobilePitch += dy * 0.003;
                    mobilePitch = Math.max(-Math.PI/2, Math.min(Math.PI/2, mobilePitch));
                    panLast = { x: e.touches[0].clientX, y: e.touches[0].clientY };
                } else if (e.touches.length === 2) {
                    const dx = e.touches[0].clientX - e.touches[1].clientX;
                    const dy = e.touches[0].clientY - e.touches[1].clientY;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    const delta = lastPinchDist - dist;
                    camera.getWorldDirection(direction);
                    camera.position.addScaledVector(direction, delta * 20);
                    lastPinchDist = dist;
                    panLast = null;
                }
            }, { passive: false });
            renderer.domElement.addEventListener('touchend', e => {
                e.preventDefault();
                // Tap curto no canvas = selecionar personagem
                if (e.changedTouches.length === 1 && panLast) {
                    const t = e.changedTouches[0];
                    const dx = t.clientX - panLast.x;
                    const dy = t.clientY - panLast.y;
                    // Só considera tap se não houve movimento significativo
                    if (Math.sqrt(dx*dx + dy*dy) < 10) {
                        doRaycast(t.clientX, t.clientY);
                    }
                }
                panLast = null;
            }, { passive: false });
        }
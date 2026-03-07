let scene, camera, renderer;
let allNodes = [];
let allEdges = [];
let graphData = null;
let timelapseData = null;
let currentEpisodeIndex = 0;
let isPlaying = false;
let playInterval = null;
let imageCache = {};
let rotationEnabled = false;
let legendFilter = 'all';

let fadeTargets = [];
let seenCharacters = new Set();
let absentEpisodes = {};
let edgeFirstSeen = {};

const communityNames = ['Stark/Norte', 'Lannister', 'Targaryen', 'Nights Watch', 'Baratheon', 'Outros', 'Secundarios', 'Terciarios'];

async function init() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 20000);
    camera.position.set(0, 0, 15000);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    createStars();
    
    await loadData();
    
    window.addEventListener('resize', onWindowResize);
    animate();
}

function createStars() {
    const starsGeometry = new THREE.BufferGeometry();
    const starsMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 1, opacity: 0.3, transparent: true });
    const starsVertices = [];
    for (let i = 0; i < 5000; i++) {
        starsVertices.push((Math.random() - 0.5) * 50000, (Math.random() - 0.5) * 50000, (Math.random() - 0.5) * 50000);
    }
    starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
    scene.add(new THREE.Points(starsGeometry, starsMaterial));
}

async function loadData() {
    
    graphData = await loadJSON('graph_data');
    timelapseData = await loadJSON('timelapse_data');
    
    document.getElementById('slider').max = timelapseData.episodios.length - 1;
    document.getElementById('totalCount').textContent = graphData.nodes.length;
    
    createGraph(graphData);
}

function createGraph(data) {
    const colors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff, 0x00ffff, 0xffa500, 0x800080];
    
    data.nodes.forEach((node) => {
        const imgPath = getCharacterImage(node.id);
        
        const photoCanvas = document.createElement('canvas');
        photoCanvas.width = 512;
        photoCanvas.height = 512;
        const photoCtx = photoCanvas.getContext('2d');
        
        const spriteMaterial = new THREE.SpriteMaterial({ transparent: true, opacity: 1 });
        const sprite = new THREE.Sprite(spriteMaterial);
        sprite.scale.set(node.size * 2, node.size * 2, 1);
        sprite.position.set(node.x, node.y, node.z);
        sprite.userData = { name: node.id };
        sprite.visible = false;
        scene.add(sprite);
        
        const img = new Image();
        img.crossOrigin = 'anonymous';
        img.onload = () => {
            photoCtx.clearRect(0, 0, 512, 512);
            photoCtx.beginPath();
            photoCtx.arc(256, 256, 256, 0, Math.PI * 2);
            photoCtx.clip();
            photoCtx.drawImage(img, 0, 0, 512, 512);
            sprite.material.map = new THREE.CanvasTexture(photoCanvas);
            sprite.material.needsUpdate = true;
        };
        img.onerror = () => {
            const defaultImg = new Image();
            defaultImg.crossOrigin = 'anonymous';
            defaultImg.onload = () => {
                photoCtx.clearRect(0, 0, 512, 512);
                photoCtx.beginPath();
                photoCtx.arc(256, 256, 256, 0, Math.PI * 2);
                photoCtx.clip();
                photoCtx.drawImage(defaultImg, 0, 0, 512, 512);
                sprite.material.map = new THREE.CanvasTexture(photoCanvas);
                sprite.material.needsUpdate = true;
            };
            defaultImg.src = getResourcePath('imagens/got-logo.png');
        };
        img.src = imgPath;
        
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');
        ctx.strokeStyle = `#${colors[node.community % colors.length].toString(16).padStart(6, '0')}`;
        ctx.lineWidth = 20;
        ctx.beginPath();
        ctx.arc(256, 256, 236, 0, Math.PI * 2);
        ctx.stroke();
        
        const ringTexture = new THREE.CanvasTexture(canvas);
        const ring = new THREE.Sprite(new THREE.SpriteMaterial({ map: ringTexture, transparent: true }));
        ring.scale.set(node.size * 2.2, node.size * 2.2, 1);
        ring.position.set(node.x, node.y, node.z);
        ring.visible = false;
        scene.add(ring);
        
        const labelCanvas = document.createElement('canvas');
        labelCanvas.width = 256;
        labelCanvas.height = 64;
        const labelCtx = labelCanvas.getContext('2d');
        labelCtx.fillStyle = 'white';
        labelCtx.font = '20px Arial';
        labelCtx.fillText(node.id, 10, 30);
        
        const labelTexture = new THREE.CanvasTexture(labelCanvas);
        const labelSprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: labelTexture }));
        labelSprite.position.set(node.x, node.y + node.size + 50, node.z);
        labelSprite.scale.set(300, 75, 1);
        labelSprite.visible = false;
        scene.add(labelSprite);
        
        allNodes.push({ sphere: sprite, label: labelSprite, ring, name: node.id });
    });

    data.edges.forEach(edge => {
        const fromNode = data.nodes.find(n => n.id === edge.source);
        const toNode = data.nodes.find(n => n.id === edge.target);
        
        if (fromNode && toNode) {
            const geometry = new THREE.BufferGeometry().setFromPoints([
                new THREE.Vector3(fromNode.x, fromNode.y, fromNode.z),
                new THREE.Vector3(toNode.x, toNode.y, toNode.z)
            ]);
            const material = new THREE.LineBasicMaterial({ 
                color: 0xffffff, 
                transparent: true, 
                opacity: Math.min(edge.weight / 100, 0.6),
                linewidth: 2
            });
            const line = new THREE.Line(geometry, material);
            line.userData = { weight: edge.weight };
            line.visible = false;
            scene.add(line);
            allEdges.push({ line, source: edge.source, target: edge.target });
        }
    });
}

function updateVisibility() {
    const episodio = timelapseData.episodios[currentEpisodeIndex];
    const personagensAtivos = new Set(episodio.personagens_ativos);
    const personagensVisiveis = new Set(episodio.personagens_visiveis);
    const todosPersonagens = new Set(episodio.todos_personagens);
    
    let visibleCount = 0;
    allNodes.forEach(node => {
        const visible = personagensVisiveis.has(node.name);
        const mats = [node.sphere.material, node.label.material, node.ring.material];
        
        if (visible) {
            absentEpisodes[node.name] = 0; // resetar contador
            if (!node.sphere.visible) {
                node.sphere.visible = true;
                node.label.visible = true;
                node.ring.visible = true;
                mats.forEach(m => { m.opacity = 0; m.transparent = true; m.needsUpdate = true; });
                fadeTargets.push({ materials: mats, target: 1, speed: 1/60 });
            }
            visibleCount++;
        } else if (node.sphere.visible) {
            absentEpisodes[node.name] = (absentEpisodes[node.name] || 0) + 1;
            if (absentEpisodes[node.name] >= 3) {
                fadeTargets.push({
                    materials: mats,
                    target: 0,
                    speed: 1/60,
                    onDone: () => {
                        node.sphere.visible = false;
                        node.label.visible = false;
                        node.ring.visible = false;
                    }
                });
            }
        } else {
            if (seenCharacters.has(node.name)) {
                absentEpisodes[node.name] = (absentEpisodes[node.name] || 0) + 1;
            }
        }
        if (visible) seenCharacters.add(node.name);
    });
    
    // Atualizar cor das linhas baseado em ausencia
    allEdges.forEach(edge => {
        const sourceVisible = personagensVisiveis.has(edge.source);
        const targetVisible = personagensVisiveis.has(edge.target);
        const visible = sourceVisible && targetVisible;
        const baseOpacity = Math.min(edge.line.userData.weight / 100, 0.6);
        const sourceAbsent = absentEpisodes[edge.source] || 0;
        const targetAbsent = absentEpisodes[edge.target] || 0;
        const anyAbsent = sourceAbsent > 0 || targetAbsent > 0;
        const maxAbsent = Math.max(sourceAbsent, targetAbsent);
        const edgeKey = `${edge.source}-${edge.target}`;
        
        if (visible) {
            if (!edge.line.visible) {
                edgeFirstSeen[edgeKey] = currentEpisodeIndex;
                edge.line.material.color.setHex(0x00ff00);
                edge.line.material.opacity = 0;
                edge.line.visible = true;
                fadeTargets.push({ materials: [edge.line.material], target: baseOpacity, speed: baseOpacity/60 });
            } else {
                const episodesSinceFirst = currentEpisodeIndex - (edgeFirstSeen[edgeKey] || 0);
                if (episodesSinceFirst < 2) {
                    edge.line.material.color.setHex(0x00ff00);
                } else {
                    edge.line.material.color.setHex(0xffffff);
                }
            }
        } else if (edge.line.visible) {
            if (anyAbsent) {
                edge.line.material.color.setHex(0xff6666);
            }
            if (maxAbsent >= 3) {
                fadeTargets.push({
                    materials: [edge.line.material],
                    target: 0,
                    speed: baseOpacity/60,
                    onDone: () => { edge.line.visible = false; }
                });
            }
        }
    });
    
    document.getElementById('episodeLabel').textContent = `S${episodio.temporada}E${episodio.episodio}`;
    document.getElementById('slider').value = currentEpisodeIndex;
    document.getElementById('visibleCount').textContent = personagensVisiveis.size;
    
    // Calcular comunidade mais relevante
    const communityCount = {};
    graphData.nodes.forEach(node => {
        if (personagensVisiveis.has(node.id)) {
            communityCount[node.community] = (communityCount[node.community] || 0) + node.influence_score;
        }
    });
    const topComm = Object.entries(communityCount).sort((a, b) => b[1] - a[1])[0];
    document.getElementById('topCommunity').textContent = topComm ? communityNames[topComm[0]] : '-';
    
    // Atualizar legenda com cores
    const sortedNodes = graphData.nodes.sort((a, b) => b.influence_score - a.influence_score);
    const legendHtml = sortedNodes.map(node => {
        let className = 'char-item';
        let type = '';
        if (personagensAtivos.has(node.id)) {
            className += ' char-active';
            type = 'active';
        } else if (personagensVisiveis.has(node.id)) {
            className += ' char-left';
            type = 'left';
        } else if (todosPersonagens.has(node.id)) {
            className += ' char-left';
            type = 'left';
        } else {
            className += ' char-notyet';
            type = 'notyet';
        }
        
        // Aplicar filtro
        if (legendFilter !== 'all' && legendFilter !== type) {
            return '';
        }
        
        return `<div class="${className}">${node.id}</div>`;
    }).join('');
    document.getElementById('legendContent').innerHTML = legendHtml;
}

const isMobile = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) || window.innerWidth <= 600;
if (isMobile) document.getElementById('legend').classList.add('collapsed');
function toggleLegend() {
    const leg = document.getElementById('legend');
    const btn = document.getElementById('legendToggle');
    leg.classList.toggle('collapsed');
    btn.textContent = leg.classList.contains('collapsed') ? '▶' : '▼';
}
function toggleFilter(filter) {
    legendFilter = filter;
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    updateVisibility();
}

function nextEpisode() {
    if (currentEpisodeIndex < timelapseData.episodios.length - 1) {
        currentEpisodeIndex++;
        updateVisibility();
    }
}

function prevEpisode() {
    if (currentEpisodeIndex > 0) {
        currentEpisodeIndex--;
        updateVisibility();
    }
}

function togglePlay() {
    isPlaying = !isPlaying;
    rotationEnabled = !rotationEnabled;
    const btn = document.getElementById('playBtn');
    
    if (isPlaying) {
        btn.textContent = '⏸ Pause';
        if (currentEpisodeIndex === 0) {
            updateVisibility();
        }
        playInterval = setInterval(() => {
            if (currentEpisodeIndex < timelapseData.episodios.length - 1) {
                nextEpisode();
            } else {
                togglePlay();
            }
        }, 3000);
    } else {
        btn.textContent = '▶ Play';
        clearInterval(playInterval);
    }
}

document.getElementById('slider').addEventListener('input', (e) => {
    currentEpisodeIndex = parseInt(e.target.value);
    updateVisibility();
});

function animate() {
    requestAnimationFrame(animate);
    
    // Processar fades
    fadeTargets = fadeTargets.filter(ft => {
        ft.materials.forEach(m => {
            if (ft.target > m.opacity) m.opacity = Math.min(m.opacity + ft.speed, ft.target);
            else m.opacity = Math.max(m.opacity - ft.speed, ft.target);
        });
        const done = Math.abs(ft.materials[0].opacity - ft.target) < 0.01;
        if (done && ft.onDone) ft.onDone();
        return !done;
    });
    
    // Rotacionar câmera ao redor do centro apenas se estiver em play
    if (rotationEnabled) {
        const radius = 15000;
        const speed = 0.00005;
        camera.position.x = Math.sin(Date.now() * speed) * radius;
        camera.position.z = Math.cos(Date.now() * speed) * radius;
        camera.lookAt(0, 0, 0);
    }
    
    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

init();
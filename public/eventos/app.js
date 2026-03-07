let eventosData = null;

        async function loadData() {
            try {
                eventosData = await loadJSON('eventos_importantes');
                renderCenas();
                renderEpisodios();
                renderTurning();
            } catch (error) {
                console.error('Erro ao carregar dados:', error);
                document.getElementById('cenasContent').innerHTML = 
                    '<p style="color: #ff5555;">Erro ao carregar dados. Execute gerar_eventos.py primeiro.</p>';
            }
        }

        function showTab(tab) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(tab).classList.add('active');
        }

        function renderCenas() {
            const html = eventosData.top_cenas.map((cena, index) => `
                <div class="card">
                    <h3>#${index + 1} - S${cena.temporada}E${cena.episodio}</h3>
                    <p><span class="score">Score: ${cena.score.toFixed(2)}</span> | ${cena.num_personagens} personagens</p>
                    ${cena.descricao ? `<p style="margin-top: 10px; color: #aaa;">${cena.descricao}</p>` : ''}
                    <div class="personagens">
                        ${cena.personagens.map(p => `<span class="badge">${p}</span>`).join('')}
                    </div>
                </div>
            `).join('');
            document.getElementById('cenasContent').innerHTML = html;
        }

        function renderEpisodios() {
            const html = eventosData.top_episodios.map((ep, index) => `
                <div class="card">
                    <h3>#${index + 1} - S${ep.temporada}E${ep.episodio}</h3>
                    <p>
                        <span class="score">Densidade: ${ep.densidade.toFixed(2)}</span> | 
                        ${ep.num_interacoes} interações | 
                        ${ep.num_personagens} personagens
                    </p>
                </div>
            `).join('');
            document.getElementById('episodiosContent').innerHTML = html;
        }

        function renderTurning() {
            const html = eventosData.turning_points.map((tp, index) => `
                <div class="card turning">
                    <h3>S${tp.temporada}E${tp.episodio}</h3>
                    ${tp.num_novos > 0 ? `
                        <p style="margin-top: 10px;"><strong>Novos personagens (${tp.num_novos}):</strong></p>
                        <div>${tp.novos.map(p => `<span class="badge novo">${p}</span>`).join('')}</div>
                    ` : ''}
                    ${tp.num_saidos > 0 ? `
                        <p style="margin-top: 10px;"><strong>Personagens que saíram (${tp.num_saidos}):</strong></p>
                        <div>${tp.saidos.map(p => `<span class="badge saiu">${p}</span>`).join('')}</div>
                    ` : ''}
                </div>
            `).join('');
            document.getElementById('turningContent').innerHTML = html;
        }

        // Criar estrelas de fundo
        const canvas = document.getElementById('stars');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        for (let i = 0; i < 200; i++) {
            const x = Math.random() * canvas.width;
            const y = Math.random() * canvas.height;
            const radius = Math.random() * 1.5;
            ctx.fillStyle = 'white';
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fill();
        }
        
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });

        loadData();
// Carregar estatísticas dinâmicas
async function loadStats() {
    try {
        const [graphData, interactionsData] = await Promise.all([
            loadJSON('graph_data'),
            loadJSON('interactions_index')
        ]);

        // Personagens únicos
        document.querySelector('.stat-card:nth-child(3) .stat-number').textContent = graphData.nodes.length;

        // Calcular temporadas e episódios únicos
        const temporadas = new Set();
        const episodios = new Set();
        let totalInteracoes = 0;

        Object.values(interactionsData).forEach(interactions => {
            interactions.forEach(int => {
                temporadas.add(int.s);
                episodios.add(`${int.s}-${int.e}`);
            });
            totalInteracoes += interactions.length;
        });

        document.querySelector('.stat-card:nth-child(1) .stat-number').textContent = temporadas.size;
        document.querySelector('.stat-card:nth-child(2) .stat-number').textContent = episodios.size;
        
        // Formatar interações
        if (totalInteracoes >= 1000) {
            document.querySelector('.stat-card:nth-child(4) .stat-number').textContent = 
                Math.floor(totalInteracoes / 1000) + 'k+';
        } else {
            document.querySelector('.stat-card:nth-child(4) .stat-number').textContent = totalInteracoes;
        }
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
    }
}

loadStats();

let currentSlide = 1;
const totalSlides = 7;
let graphData = null;

// Navegação de slides
function changeSlide(direction) {
    const slides = document.querySelectorAll('.slide');
    slides[currentSlide - 1].classList.remove('active');
    
    currentSlide += direction;
    if (currentSlide < 1) currentSlide = 1;
    if (currentSlide > totalSlides) currentSlide = totalSlides;
    
    slides[currentSlide - 1].classList.add('active');
    
    document.getElementById('slideCounter').textContent = `${currentSlide} / ${totalSlides}`;
    document.getElementById('progressFill').style.width = `${(currentSlide / totalSlides) * 100}%`;
    
    document.getElementById('btnPrev').disabled = currentSlide === 1;
    document.getElementById('btnNext').disabled = currentSlide === totalSlides;
}

// Carregar dados
async function loadData() {
    try {
        const response = await fetch('../resources/jsons/graph_data.json');
        graphData = await response.json();
        updateMetrics();
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
    }
}

function updateMetrics() {
    if (!graphData) return;
    
    const nodes = graphData.nodes;
    
    // Top por métrica
    const topConsolidated = [...nodes].sort((a, b) => b.consolidated_score - a.consolidated_score)[0];
    const topPagerank = [...nodes].sort((a, b) => b.pagerank - a.pagerank)[0];
    const topBetweenness = [...nodes].sort((a, b) => b.betweenness - a.betweenness)[0];
    const topDegree = [...nodes].sort((a, b) => b.degree_centrality - a.degree_centrality)[0];
    const topCloseness = [...nodes].sort((a, b) => b.closeness_centrality - a.closeness_centrality)[0];
    const topWeighted = [...nodes].sort((a, b) => b.weighted_degree - a.weighted_degree)[0];
    
    document.getElementById('m-consolidated').textContent = topConsolidated.id;
    document.getElementById('m-pagerank').textContent = topPagerank.id;
    document.getElementById('m-betweenness').textContent = topBetweenness.id;
    document.getElementById('m-degree').textContent = topDegree.id;
    document.getElementById('m-closeness').textContent = topCloseness.id;
    document.getElementById('m-weighted').textContent = topWeighted.id;
    
    // Atualizar conclusão
    document.getElementById('conclusion-char').textContent = topConsolidated.id;
    document.getElementById('conclusion-points').innerHTML = `
        <li>Score Consolidado: ${topConsolidated.consolidated_score.toFixed(4)} (maior de todos)</li>
        <li>PageRank: ${topConsolidated.pagerank.toFixed(4)} - Importância global na rede</li>
        <li>Betweenness: ${topConsolidated.betweenness.toFixed(4)} - Ponte entre comunidades</li>
        <li>Degree: ${topConsolidated.degree_centrality.toFixed(4)} - Diversidade de conexões</li>
        <li>Weighted Degree: ${topConsolidated.weighted_degree} interações totais</li>
    `;
}

// Estrelas de fundo
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

// Inicializar
loadData();

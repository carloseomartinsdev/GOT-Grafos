let graphData = null;
let currentMetric = 'influence_score';

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

const metricLabels = {
    'influence_score': 'Influence Score',
    'pagerank': 'PageRank',
    'betweenness': 'Betweenness',
    'weighted_degree': 'Weighted Degree',
    'connections': 'Conexões'
};

async function loadData() {
    try {
        graphData = await loadJSON('graph_data');
        sortBy('influence_score');
    } catch (error) {
        console.error('Erro ao carregar dados:', error);
        document.getElementById('rankingTable').innerHTML = 
            '<tr><td colspan="4" style="text-align: center;">Erro ao carregar dados</td></tr>';
    }
}

function sortBy(metric) {
    currentMetric = metric;
    
    // Atualizar botões
    document.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
    const btnMap = {
        'influence_score': 'btn-influence',
        'pagerank': 'btn-pagerank',
        'betweenness': 'btn-betweenness',
        'weighted_degree': 'btn-weighted',
        'connections': 'btn-connections'
    };
    const btn = document.getElementById(btnMap[metric]);
    if (btn) btn.classList.add('active');
    
    // Ordenar dados
    const sorted = [...graphData.nodes].sort((a, b) => b[metric] - a[metric]);
    
    // Renderizar tabela
    const tbody = document.getElementById('rankingTable');
    tbody.innerHTML = sorted.map((node, index) => {
        const imgPath = getCharacterImage(node.id);
        const commName = communityNames[node.community] || `Comunidade ${node.community}`;
        const value = metric === 'connections' ? node[metric] : node[metric].toFixed(4);
        const rowClass = index < 3 ? 'top3' : '';
        
        return `
            <tr class="${rowClass}">
                <td class="rank">${index + 1}</td>
                <td class="name">
                    <img src="${imgPath}" onerror="this.src='${getResourcePath('imagens/got-logo.png')}'" />
                    ${node.id}
                </td>
                <td class="value">${value}</td>
                <td>${commName}</td>
            </tr>
        `;
    }).join('');
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
// Detecta o nível de profundidade da página atual
function getDepth() {
    return '../';
}

// Retorna o caminho correto para recursos baseado na profundidade
function getResourcePath(resource) {
    const depth = getDepth();
    return `${depth}resources/${resource}`;
}

// Retorna o caminho para imagem de personagem
function getCharacterImage(characterName) {
    const imageName = characterName.replace(/ /g, '_').replace(/\//g, '_').toUpperCase();
    return getResourcePath(`imagens/personagens/${imageName}.JPG`);
}

// Carrega arquivo JSON
async function loadJSON(filename) {
    const path = getResourcePath(`jsons/${filename}.json`);
    const response = await fetch(path);
    return await response.json();
}

// Cria o menu de navegação
function createNavigationMenu() {
    const currentPage = window.location.pathname.split('/').filter(p => p).pop() || 'index';
    
    const menuHTML = `
        <div class="nav-buttons">
            <button onclick="window.location.href='../'" ${currentPage === 'index' ? 'disabled' : ''}>🏠 Início</button>
            <button onclick="window.location.href='../visualizador/'" ${currentPage === 'visualizador' ? 'disabled' : ''}>🌐 Visualizador</button>
            <button onclick="window.location.href='../rankings/'" ${currentPage === 'rankings' ? 'disabled' : ''}>📊 Rankings</button>
            <button onclick="window.location.href='../eventos/'" ${currentPage === 'eventos' ? 'disabled' : ''}>🎬 Eventos</button>
            <button onclick="window.location.href='../timelapse/'" ${currentPage === 'timelapse' ? 'disabled' : ''}>⏱️ Timelapse</button>
            <button onclick="window.location.href='../caminhos/'" ${currentPage === 'caminhos' ? 'disabled' : ''}>🔍 Caminhos</button>
            <button onclick="window.location.href='../metricas/'" ${currentPage === 'metricas' ? 'disabled' : ''}>📈 Métricas</button>
            <button onclick="window.location.href='../apresentacao/'" ${currentPage === 'apresentacao' ? 'disabled' : ''}>📖 Apresentação</button>
        </div>
    `;
    
    return menuHTML;
}

// Insere o menu de navegação no elemento com id 'nav-menu'
function insertNavigationMenu() {
    const navElement = document.getElementById('nav-menu');
    if (navElement) {
        navElement.innerHTML = createNavigationMenu();
    }
}

// Executa quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', insertNavigationMenu);
} else {
    insertNavigationMenu();
}

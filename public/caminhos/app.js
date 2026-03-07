let graphData = null;
let adjacency = {};
let interactionsIndex = null;

async function loadInteractions() {
    try {
        interactionsIndex = await loadJSON('interactions_index');
    } catch(e) { interactionsIndex = {}; }
}

function getInteractions(a, b) {
    if (!interactionsIndex) return [];
    const key1 = `${a}|||${b}`;
    const key2 = `${b}|||${a}`;
    return interactionsIndex[key1] || interactionsIndex[key2] || [];
}

function openModal(path) {
    const body = document.getElementById('modalBody');
    const title = document.getElementById('modalTitle');
    body.innerHTML = '';

    // Para cada par consecutivo no caminho
    const pairs = [];
    for (let i = 0; i < path.length - 1; i++) pairs.push([path[i], path[i+1]]);

    title.textContent = `Interações: ${path[0].split(' ')[0]} → ${path[path.length-1].split(' ')[0]}`;

    pairs.forEach(([a, b]) => {
        const items = getInteractions(a, b);

        // Cabeçalho do par
        const pairDiv = document.createElement('div');
        pairDiv.className = 'modal-pair';
        pairDiv.innerHTML = `
            ${pairThumbHTML(a)}
            <div class="modal-pair-info"><strong>${a}</strong><br><span>↔</span></div>
            ${pairThumbHTML(b)}
            <div class="modal-pair-info"><strong>${b}</strong></div>
            <div class="interaction-count">${items.length} interações</div>
        `;
        body.appendChild(pairDiv);

        if (items.length === 0) {
            const p = document.createElement('p');
            p.className = 'no-interactions';
            p.textContent = 'Nenhuma interação direta encontrada no dataset.';
            body.appendChild(p);
            return;
        }

        // Agrupar por temporada
        const bySeason = {};
        items.forEach(it => {
            if (!bySeason[it.s]) bySeason[it.s] = [];
            bySeason[it.s].push(it);
        });

        Object.keys(bySeason).sort((a,b) => a-b).forEach(season => {
            const st = document.createElement('div');
            st.className = 'section-title';
            st.textContent = `Temporada ${season}`;
            body.appendChild(st);

            const table = document.createElement('table');
            table.className = 'interactions-table';
            table.innerHTML = `<thead><tr><th>Ep.</th><th>Cena</th><th>Tipo</th><th>Fala</th></tr></thead>`;
            const tbody = document.createElement('tbody');

            bySeason[season].forEach(it => {
                const tr = document.createElement('tr');
                const tipoClass = it.tipo === 'direct' ? 'tipo-direct' : it.tipo === 'group' ? 'tipo-group' : 'tipo-scene';
                tr.innerHTML = `
                    <td>${it.e}</td>
                    <td>${it.c}</td>
                    <td><span class="tipo-badge ${tipoClass}">${it.tipo}</span></td>
                    <td>${it.fala || '—'}</td>
                `;
                tbody.appendChild(tr);
            });

            table.appendChild(tbody);
            body.appendChild(table);
        });
    });

    document.getElementById('modalOverlay').classList.add('open');
}

function pairThumbHTML(name) {
    const src = getCharacterImage(name);
    const defaultSrc = getResourcePath('imagens/got-logo.png');
    const ini = name.split(' ').slice(0,2).map(w=>w[0]).join('').toUpperCase();
    return `<img src="${src}" alt="${name}" onerror="this.src='${defaultSrc}'" style="width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid #c9a961;flex-shrink:0">`;
}

function closeModal() {
    document.getElementById('modalOverlay').classList.remove('open');
}
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('modalOverlay').addEventListener('click', e => {
        if (e.target === e.currentTarget) closeModal();
    });
});

async function loadData() {
    await loadInteractions();
    graphData = await loadJSON('graph_data');

    // Montar adjacência
    graphData.edges.forEach(e => {
        if (!adjacency[e.source]) adjacency[e.source] = [];
        if (!adjacency[e.target]) adjacency[e.target] = [];
        adjacency[e.source].push({ id: e.target, weight: e.weight });
        adjacency[e.target].push({ id: e.source, weight: e.weight });
    });

    // Popular select
    const select = document.getElementById('charSelect');
    const sorted = [...graphData.nodes].sort((a, b) => a.id.localeCompare(b.id));
    sorted.forEach(n => {
        const opt = document.createElement('option');
        opt.value = n.id;
        opt.textContent = n.id;
        select.appendChild(opt);
    });

    document.getElementById('btnAnalyze').disabled = false;
}

// Filtro de busca no select
document.getElementById('searchInput').addEventListener('input', function() {
    const q = this.value.toLowerCase();
    Array.from(document.getElementById('charSelect').options).forEach(opt => {
        opt.style.display = opt.value.toLowerCase().includes(q) ? '' : 'none';
    });
});

document.getElementById('btnAnalyze').addEventListener('click', () => {
    const sel = document.getElementById('charSelect').value;
    if (sel) analyze(sel);
});

document.getElementById('charSelect').addEventListener('dblclick', () => {
    const sel = document.getElementById('charSelect').value;
    if (sel) analyze(sel);
});

function bfsAll(start) {
    const dist = { [start]: 0 };
    const prev = { [start]: null };
    const queue = [start];
    while (queue.length) {
        const node = queue.shift();
        for (const nb of (adjacency[node] || [])) {
            if (!(nb.id in dist)) {
                dist[nb.id] = dist[node] + 1;
                prev[nb.id] = node;
                queue.push(nb.id);
            }
        }
    }
    return { dist, prev };
}

function reconstructPath(prev, target) {
    const path = [];
    let cur = target;
    while (cur !== null) {
        path.unshift(cur);
        cur = prev[cur];
    }
    return path;
}

function imgSrc(name) {
    return getCharacterImage(name);
}

function initials(name) {
    return name.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase();
}

function charThumb(name, size = 32) {
    const img = document.createElement('img');
    img.src = imgSrc(name);
    img.alt = name;
    img.title = name;
    img.style.width = size + 'px';
    img.style.height = size + 'px';
    img.style.borderRadius = '50%';
    img.style.objectFit = 'cover';
    img.style.border = '2px solid #c9a961';
    img.onerror = function() {
        this.src = getResourcePath('imagens/got-logo.png');
    };
    return img;
}

let currentFilter = 'all';
let currentSearch = '';
let currentResults = [];
let currentChar = '';

function analyze(charName) {
    currentChar = charName;
    const content = document.getElementById('content');
    content.innerHTML = '<div class="loading">⚔️ Calculando caminhos...</div>';

    setTimeout(() => {
        const { dist, prev } = bfsAll(charName);
        const nodeMap = {};
        graphData.nodes.forEach(n => nodeMap[n.id] = n);

        currentResults = graphData.nodes
            .filter(n => n.id !== charName)
            .map(n => {
                const d = dist[n.id];
                const path = d !== undefined ? reconstructPath(prev, n.id) : null;
                return { node: n, dist: d ?? Infinity, path };
            })
            .sort((a, b) => a.dist - b.dist || a.node.id.localeCompare(b.node.id));

        renderResults(charName, nodeMap);
    }, 10);
}

function renderResults(charName, nodeMap) {
    if (!nodeMap) {
        nodeMap = {};
        graphData.nodes.forEach(n => nodeMap[n.id] = n);
    }
    const charNode = nodeMap[charName];
    const content = document.getElementById('content');
    content.innerHTML = '';

    // Header do personagem selecionado
    const header = document.createElement('div');
    header.className = 'selected-char';
    const img = charThumb(charName, 70);
    img.style.width = '70px';
    img.style.height = '70px';
    img.style.border = '3px solid #c9a961';
    header.appendChild(img);
    const info = document.createElement('div');
    info.innerHTML = `<h2>${charName}</h2><p>${charNode?.familia || ''} &nbsp;|&nbsp; ${charNode?.connections || 0} conexões diretas</p>`;
    header.appendChild(info);
    content.appendChild(header);

    // Legenda
    const legend = document.createElement('div');
    legend.className = 'legend';
    legend.innerHTML = `
        <div class="legend-item"><div class="legend-dot" style="background:#4CAF50"></div> Conexão direta (1 passo)</div>
        <div class="legend-item"><div class="legend-dot" style="background:#c9a961"></div> 2 passos</div>
        <div class="legend-item"><div class="legend-dot" style="background:#ff9800"></div> 3 passos</div>
        <div class="legend-item"><div class="legend-dot" style="background:#f44336"></div> 4+ passos</div>
        <div class="legend-item"><div class="legend-dot" style="background:#555"></div> Sem caminho</div>
    `;
    content.appendChild(legend);

    // Filtros
    const filters = document.createElement('div');
    filters.className = 'filters';
    const filterDefs = [
        { key: 'all', label: 'Todos' },
        { key: '1', label: '1 passo' },
        { key: '2', label: '2 passos' },
        { key: '3', label: '3 passos' },
        { key: '4+', label: '4+ passos' },
        { key: 'unreachable', label: 'Sem caminho' },
    ];
    filterDefs.forEach(f => {
        const btn = document.createElement('button');
        btn.className = 'filter-btn' + (currentFilter === f.key ? ' active' : '');
        btn.textContent = f.label;
        btn.dataset.filter = f.key;
        btn.addEventListener('click', () => {
            currentFilter = f.key;
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderGrid();
        });
        filters.appendChild(btn);
    });

    const searchBox = document.createElement('input');
    searchBox.type = 'text';
    searchBox.className = 'filter-search';
    searchBox.placeholder = 'Filtrar por nome...';
    searchBox.value = currentSearch;
    searchBox.addEventListener('input', function() {
        currentSearch = this.value;
        renderGrid();
    });
    filters.appendChild(searchBox);

    const countEl = document.createElement('span');
    countEl.className = 'results-count';
    countEl.id = 'resultsCount';
    filters.appendChild(countEl);

    content.appendChild(filters);

    // Grid container
    const grid = document.createElement('div');
    grid.className = 'paths-grid';
    grid.id = 'pathsGrid';
    content.appendChild(grid);

    renderGrid();
}

function renderGrid() {
    const grid = document.getElementById('pathsGrid');
    const countEl = document.getElementById('resultsCount');
    if (!grid) return;
    grid.innerHTML = '';

    const filtered = currentResults.filter(r => {
        const nameMatch = !currentSearch || r.node.id.toLowerCase().includes(currentSearch.toLowerCase());
        let distMatch = true;
        if (currentFilter === '1') distMatch = r.dist === 1;
        else if (currentFilter === '2') distMatch = r.dist === 2;
        else if (currentFilter === '3') distMatch = r.dist === 3;
        else if (currentFilter === '4+') distMatch = r.dist >= 4 && r.dist !== Infinity;
        else if (currentFilter === 'unreachable') distMatch = r.dist === Infinity;
        return nameMatch && distMatch;
    });

    countEl.textContent = `${filtered.length} personagens`;

    filtered.forEach(({ node, dist, path }) => {
        const card = document.createElement('div');
        let cardClass = 'path-card';
        let badgeClass = 'dn';
        let badgeText = '∞';
        if (dist === 1) { cardClass += ' direct'; badgeClass = 'd1'; badgeText = '1 passo'; }
        else if (dist === 2) { cardClass += ' two-hops'; badgeClass = 'd2'; badgeText = '2 passos'; }
        else if (dist === 3) { cardClass += ' three-hops'; badgeClass = 'd3'; badgeText = '3 passos'; }
        else if (dist !== Infinity) { cardClass += ' far'; badgeClass = 'd4'; badgeText = dist + ' passos'; }
        else { cardClass += ' unreachable'; }
        card.className = cardClass;

        // Header do card
        const cardHeader = document.createElement('div');
        cardHeader.className = 'path-card-header';
        const thumb = charThumb(node.id, 40);
        cardHeader.appendChild(thumb);
        const nameDiv = document.createElement('div');
        nameDiv.style.flex = '1';
        nameDiv.innerHTML = `<div class="target-name">${node.id}</div><div class="target-familia">${node.familia || ''}</div>`;
        cardHeader.appendChild(nameDiv);
        const badge = document.createElement('span');
        badge.className = `hop-badge ${badgeClass}`;
        badge.textContent = badgeText;
        cardHeader.appendChild(badge);
        card.appendChild(cardHeader);

        // Visualização do caminho
        if (path && path.length > 1) {
            const pathVisual = document.createElement('div');
            pathVisual.className = 'path-visual';

            path.forEach((charId, idx) => {
                const nodeEl = document.createElement('div');
                nodeEl.className = 'path-node';
                const nodeImg = charThumb(charId, 32);
                nodeEl.appendChild(nodeImg);
                const nameEl = document.createElement('div');
                nameEl.className = 'node-name';
                nameEl.textContent = charId.split(' ')[0]; // só primeiro nome
                nodeEl.appendChild(nameEl);
                pathVisual.appendChild(nodeEl);

                if (idx < path.length - 1) {
                    const arrow = document.createElement('span');
                    arrow.className = 'path-arrow';
                    arrow.textContent = '→';
                    pathVisual.appendChild(arrow);
                }
            });

            card.appendChild(pathVisual);
        } else if (dist === Infinity) {
            const noPath = document.createElement('div');
            noPath.style.cssText = 'color:#666;font-size:0.85em;margin-top:6px;';
            noPath.textContent = 'Sem caminho encontrado na rede';
            card.appendChild(noPath);
        }

        if (path && path.length > 1) {
            card.addEventListener('click', () => openModal(path));
            card.title = 'Clique para ver as interações';
        }

        grid.appendChild(card);
    });

    if (filtered.length === 0) {
        grid.innerHTML = '<div style="color:#b8a88a;padding:20px;grid-column:1/-1;">Nenhum resultado encontrado.</div>';
    }
}

loadData();

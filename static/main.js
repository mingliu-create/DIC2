let n = parseInt(document.getElementById('nval').textContent, 10);
let start = defaultStart.slice();
let goal = defaultGoal.slice();
let blocks = defaultBlocks.map(b => b.slice());
let mode = 'block';

const arrows = {U: '↑', D: '↓', L: '←', R: '→', T: '★'};

function createGrid() {
  const wrap = document.getElementById('gridwrap');
  wrap.innerHTML = '';
  const table = document.createElement('table');
  table.className = 'grid';
  for (let r = 0; r < n; r++) {
    const tr = document.createElement('tr');
    for (let c = 0; c < n; c++) {
      const td = document.createElement('td');
      td.dataset.r = r; td.dataset.c = c;
      td.addEventListener('click', onCellClick);
      td.innerHTML = '<div class="val"></div><div class="arrow"></div>';
      tr.appendChild(td);
    }
    table.appendChild(tr);
  }
  wrap.appendChild(table);
  renderMarks();
}

function onCellClick(ev) {
  const r = parseInt(this.dataset.r, 10);
  const c = parseInt(this.dataset.c, 10);
  if (mode === 'start') {
    start = [r, c];
  } else if (mode === 'goal') {
    goal = [r, c];
  } else {
    const idx = blocks.findIndex(b => b[0]===r && b[1]===c);
    if (idx >= 0) blocks.splice(idx,1);
    else if (blocks.length < n-2) blocks.push([r,c]);
  }
  renderMarks();
}

function renderMarks(values, policy, path) {
  const cells = document.querySelectorAll('td');
  cells.forEach(td => {
    td.className = '';
    const r = parseInt(td.dataset.r,10), c = parseInt(td.dataset.c,10);
    if (r===start[0] && c===start[1]) td.classList.add('start');
    if (r===goal[0] && c===goal[1]) td.classList.add('goal');
    if (blocks.find(b=>b[0]===r&&b[1]===c)) td.classList.add('block');
    const valDiv = td.querySelector('.val');
    const arrowDiv = td.querySelector('.arrow');
    valDiv.textContent = values ? values[r][c].toFixed(2) : '';
    arrowDiv.textContent = policy ? (arrows[policy[r][c]]||'') : '';
  });
  if (path) {
    path.forEach(([pr,pc]) => {
      const td = document.querySelector(`td[data-r='${pr}'][data-c='${pc}']`);
      if (td) td.classList.add('path');
    });
  }
}

document.getElementById('modeStart').addEventListener('click', ()=>{mode='start'});
document.getElementById('modeGoal').addEventListener('click', ()=>{mode='goal'});
document.getElementById('modeBlock').addEventListener('click', ()=>{mode='block'});
document.getElementById('resize').addEventListener('click', ()=>{
  const v = parseInt(document.getElementById('ninput').value,10);
  if (v>=5 && v<=9) { n=v; document.getElementById('nval').textContent = n; blocks = []; start=[0,0]; goal=[n-1,n-1]; createGrid(); }
});

document.getElementById('compute').addEventListener('click', async ()=>{
  const resp = await fetch('/compute', {
    method: 'POST', headers: {'Content-Type':'application/json'},
    body: JSON.stringify({n, start, goal, blocks})
  });
  const data = await resp.json();
  renderMarks(data.V, data.policy, data.path);
});

createGrid();

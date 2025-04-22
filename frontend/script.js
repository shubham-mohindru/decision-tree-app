document.getElementById('submit').addEventListener('click', parseAndRender);

async function parseAndRender() {
  const text = document.getElementById('input').value;

  // 1️⃣ Call the backend
  let resp;
  try {
    resp = await fetch('https://decision-tree-app-gw1t.onrender.com', { … }), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
  } catch (e) {
    return alert('🛑 Cannot reach backend. Is Flask running?');
  }

  const data = await resp.json();
  if (data.status !== 'success') {
    return alert('Parsing error: ' + (data.message || 'unknown'));
  }

  const tree = data.tree;

  // 2️⃣ Show Expected Values
  document.getElementById('ev').innerHTML =
    '<h2>Expected Values</h2><ul>' +
    tree.options.map(o => `<li>${o.name}: ${o.ev.toFixed(2)}</li>`).join('') +
    '</ul>';

  // 3️⃣ Build Mermaid source
  let md = 'graph TB;\n';
  md += `Root["${tree.decision}"];\n`;
  tree.options.forEach((opt, i) => {
    const id = `opt${i}`;
    md += `Root --> ${id}["${opt.name}\\n(EV=${opt.ev.toFixed(2)})"];\n`;
    opt.outcomes.forEach((o, j) => {
      md += `${id} --> outcome${i}_${j}["${(o[0] * 100).toFixed(0)}%: ${o[1]}"];\n`;
    });
  });

  // 4️⃣ Render with mermaid.render
  const container = document.getElementById('diagram');
  // Clear any old content
  container.innerHTML = '';

  try {
    // mermaid.render returns a Promise in recent versions
    const { svg } = await mermaid.render('graphDiv', md);
    container.innerHTML = svg;
  } catch (err) {
    console.error('Mermaid render error:', err);
    alert('⚠️ Failed to render the diagram. See console for details.');
  }
}

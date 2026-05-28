async function loadStats() {
  const container = document.getElementById('stats');
  try {
    const res = await fetch('/stats');
    const data = await res.json();
    container.innerHTML = `
      <div class="stat-card"><span>Crear</span><strong>${data.create}</strong></div>
      <div class="stat-card"><span>Actualizar</span><strong>${data.update}</strong></div>
      <div class="stat-card"><span>Eliminar</span><strong>${data.delete}</strong></div>
      <div class="stat-card"><span>Consultar</span><strong>${data.query}</strong></div>
      <div class="stat-card"><span>Total</span><strong>${data.total}</strong></div>
    `;
  } catch {
    container.innerHTML = '<p>No se pudieron cargar las estadísticas.</p>';
  }
}

async function loadEvents() {
  const list = document.getElementById('events-list');
  try {
    const res = await fetch('/events');
    const events = await res.json();
    if (!events.length) {
      list.innerHTML = '<li>Sin eventos registrados.</li>';
      return;
    }
    list.innerHTML = events
      .slice(0, 20)
      .map(
        (e) =>
          `<li><strong>${e.action}</strong> — ${e.title} (${e.source}/${e.entity}) <small>${e.created_at}</small></li>`,
      )
      .join('');
  } catch {
    list.innerHTML = '<li>Error al cargar eventos.</li>';
  }
}

loadStats();
loadEvents();

const fallback = {
  state: { mode: "offline", runtime: {}, metrics: {} },
  missions: [],
  signals: [],
  connections: { nodes: [], edges: [] },
  sources: [],
  activity: [],
  heartbeat: { run_status: "not_started", world_data_updated: false },
};

const files = ["state", "missions", "signals", "connections", "sources", "activity", "heartbeat"];

async function load(name) {
  try {
    const response = await fetch(`data/${name}.json`, { cache: "no-store" });
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    return await response.json();
  } catch (error) {
    console.warn(`PAM Continuum could not load ${name}.json`, error);
    return fallback[name];
  }
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatDate(value, withTime = false) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return escapeHtml(value);
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
    ...(withTime ? { hour: "numeric", minute: "2-digit" } : {}),
  }).format(date);
}

function statusClass(value) {
  return String(value || "unknown").toLowerCase().replaceAll("_", "-").replaceAll(" ", "-");
}

function renderMetrics(state, missions, signals, connections) {
  const activeMissions = missions.filter((item) => ["active", "blocked", "collecting"].includes(item.status)).length;
  const openSignals = signals.filter((item) => !["confirmed", "invalidated", "archived"].includes(item.status)).length;
  const edges = connections.edges?.length || 0;
  const runtime = state.runtime || {};
  const worldStatus = runtime.world_refresh_status || "not-configured";
  const freshness = document.querySelector("#metric-freshness");
  const note = document.querySelector("#metric-freshness-note");
  freshness.textContent = worldStatus.replaceAll("-", " ").toUpperCase();
  freshness.className = `metric-value text-value ${statusClass(worldStatus)}`;
  note.textContent = runtime.last_world_refresh
    ? `Last capture ${formatDate(runtime.last_world_refresh, true)}`
    : "Heartbeat is not a world refresh.";
  document.querySelector("#metric-missions").textContent = activeMissions;
  document.querySelector("#metric-signals").textContent = openSignals;
  document.querySelector("#metric-connections").textContent = edges;
  const heartbeat = runtime.last_heartbeat ? `Heartbeat ${formatDate(runtime.last_heartbeat, true)}` : "No pulse recorded";
  document.querySelector("#footer-freshness").textContent = `Data status: ${heartbeat}`;
  document.querySelector("#hero-date").textContent = runtime.last_heartbeat ? formatDate(runtime.last_heartbeat, true) : "BOOTSTRAP";
  const topStatus = document.querySelector("#top-status");
  topStatus.textContent = `${String(state.mode || "standby").replaceAll("-", " ").toUpperCase()} · ${String(runtime.status || "standby").toUpperCase()}`;
  document.querySelector("#directive").textContent = worldStatus === "not-configured"
    ? "Connect a source before calling the world current."
    : "Map the change. Preserve the uncertainty. Move the mission.";
}

function renderMissions(missions) {
  const host = document.querySelector("#missions");
  if (!missions.length) {
    host.innerHTML = '<div class="empty-state">No missions in the queue.</div>';
    return;
  }
  host.innerHTML = missions.slice(0, 5).map((mission) => `
    <div class="mission-item">
      <div class="item-topline"><span class="status-dot ${statusClass(mission.status)}"></span><span>${escapeHtml(mission.id)}</span><span class="priority ${statusClass(mission.priority)}">${escapeHtml(mission.priority)}</span></div>
      <h3>${escapeHtml(mission.title)}</h3>
      <p>${escapeHtml(mission.next_action)}</p>
      <div class="item-meta"><span>${escapeHtml(mission.domain || "general")}</span><span>${escapeHtml(mission.status)}</span></div>
    </div>
  `).join("");
}

function renderSignals(signals) {
  const host = document.querySelector("#signals");
  if (!signals.length) {
    host.innerHTML = '<div class="empty-state">No signals are being tracked.</div>';
    return;
  }
  host.innerHTML = signals.slice(0, 5).map((signal) => `
    <div class="signal-item">
      <div class="signal-title"><span class="signal-badge ${statusClass(signal.confidence)}">${escapeHtml(signal.confidence)}</span><h3>${escapeHtml(signal.title)}</h3></div>
      <p>${escapeHtml(signal.claim)}</p>
      <div class="signal-foot"><span>${escapeHtml(signal.id)}</span><span>falsifier present</span></div>
    </div>
  `).join("");
}

function renderActivity(activity) {
  const host = document.querySelector("#activity");
  if (!activity.length) {
    host.innerHTML = '<div class="empty-state">No activity recorded.</div>';
    return;
  }
  host.innerHTML = activity.slice(0, 6).map((item) => `
    <div class="activity-item">
      <div class="activity-marker ${statusClass(item.type)}"></div>
      <div><div class="activity-title">${escapeHtml(item.title)}</div><p>${escapeHtml(item.detail)}</p><time>${formatDate(item.timestamp, true)}</time></div>
    </div>
  `).join("");
}

function renderSources(sources) {
  const host = document.querySelector("#sources");
  const ready = sources.filter((source) => ["connected", "available", "ready"].includes(source.status)).length;
  document.querySelector("#source-count").textContent = `${ready} / ${sources.length} READY`;
  host.innerHTML = sources.map((source) => `
    <div class="source-item">
      <span class="source-status ${statusClass(source.status)}"></span>
      <div class="source-main"><strong>${escapeHtml(source.label)}</strong><span>${escapeHtml(source.note || source.kind)}</span></div>
      <span class="source-state">${escapeHtml(source.status)}</span>
    </div>
  `).join("");
}

function renderMap(graph) {
  const svg = document.querySelector("#system-map");
  const nodes = graph.nodes || [];
  const lookup = Object.fromEntries(nodes.map((node) => [node.id, node]));
  const edges = (graph.edges || []).map((edge) => {
    const from = lookup[edge.from];
    const to = lookup[edge.to];
    if (!from || !to) return "";
    const midX = (from.x + to.x) / 2;
    const midY = (from.y + to.y) / 2;
    return `<g class="edge"><line x1="${from.x}" y1="${from.y}" x2="${to.x}" y2="${to.y}" /><text x="${midX}" y="${midY - 8}">${escapeHtml(edge.label)}</text></g>`;
  }).join("");
  const nodeMarkup = nodes.map((node) => `
    <g class="map-node ${statusClass(node.health)}" transform="translate(${node.x}, ${node.y})">
      <circle class="node-ring" r="40"></circle><circle class="node-core" r="29"></circle>
      <text class="node-label" y="62">${escapeHtml(node.label)}</text>
      <text class="node-health" y="78">${escapeHtml(node.health)}</text>
    </g>
  `).join("");
  svg.innerHTML = `<defs><filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>${edges}${nodeMarkup}`;
  const categories = [...new Set(nodes.map((node) => node.category))];
  document.querySelector("#map-legend").innerHTML = categories.map((category) => `<span><i class="legend-dot ${statusClass(category)}"></i>${escapeHtml(category)}</span>`).join("");
}

async function init() {
  const [state, missions, signals, connections, sources, activity, heartbeat] = await Promise.all(files.map(load));
  const mergedState = { ...state, runtime: { ...(state.runtime || {}), ...(heartbeat || {}) } };
  renderMetrics(mergedState, missions || [], signals || [], connections || { edges: [] });
  renderMissions(missions || []);
  renderSignals(signals || []);
  renderActivity(activity || []);
  renderSources(sources || []);
  renderMap(connections || { nodes: [], edges: [] });
}

init();


const stateLabel = {
  quieto: "quieto",
  pendiente: "pendiente",
  pensando: "pensando",
  ejecutando: "ejecutando",
  bloqueado: "bloqueado",
  done: "listo",
};

const stateClass = {
  quieto: "idle",
  pendiente: "pending",
  pensando: "thinking",
  ejecutando: "running",
  bloqueado: "blocked",
  done: "done",
};

function text(value, fallback = "-") {
  return value === undefined || value === null || value === "" ? fallback : String(value);
}

function makeLink(path, label) {
  if (!path) return document.createTextNode("-");
  const link = document.createElement("a");
  link.href = path;
  link.textContent = label || path.split("/").pop();
  return link;
}

function setText(id, value) {
  document.getElementById(id).textContent = text(value);
}

function renderFronts(fronts) {
  const root = document.getElementById("frontRows");
  root.replaceChildren();
  fronts.forEach((front) => {
    const row = document.createElement("div");
    row.className = `flow-row ${stateClass[front.state] || "idle"}`;

    const name = document.createElement("strong");
    name.textContent = front.front;

    const status = document.createElement("span");
    status.className = `status ${stateClass[front.state] || "idle"}`;
    status.textContent = stateLabel[front.state] || front.state;

    const current = document.createElement("span");
    current.appendChild(makeLink(front.current_job_path, front.current_job));

    const result = document.createElement("span");
    result.appendChild(makeLink(front.last_result, front.last_result_id));

    const action = document.createElement("span");
    action.textContent = text(front.next_action);

    row.append(name, status, current, result, action);
    root.appendChild(row);
  });
}

function renderWorkers(workers) {
  const root = document.getElementById("workers");
  root.replaceChildren();
  if (!workers.length) {
    root.textContent = "sin workers registrados";
    return;
  }
  workers.forEach((worker) => {
    const item = document.createElement("p");
    item.textContent = `${text(worker.role)} | ${text(worker.status)} | ${text(worker.host)} | ${text(worker.updated_at)}`;
    root.appendChild(item);
  });
}

function renderGit(git) {
  const root = document.getElementById("gitState");
  root.replaceChildren();
  const lines = [
    `branch: ${text(git.branch)}`,
    `commit: ${text(git.last_commit)}`,
    `dirty: ${git.dirty ? "si" : "no"}`,
  ];
  lines.forEach((line) => {
    const item = document.createElement("p");
    item.textContent = line;
    root.appendChild(item);
  });
}

function render(data) {
  setText("updatedAt", data.updated_at);
  setText("pendingCount", data.global?.pending ?? 0);
  setText("activeCount", data.global?.active ?? 0);
  setText("blockedCount", data.global?.blocked ?? 0);
  setText("resultCount", data.global?.results ?? 0);

  const globalState = document.getElementById("globalState");
  const blocked = data.global?.blocked ?? 0;
  const active = data.global?.active ?? 0;
  globalState.textContent = blocked ? "requiere atencion" : active ? "en marcha" : "estable";
  globalState.className = `pill ${blocked ? "blocked" : active ? "running" : "idle"}`;

  renderFronts(data.fronts || []);
  renderWorkers(data.workers || []);
  renderGit(data.git || {});
}

async function loadState() {
  try {
    const response = await fetch("state.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    render(await response.json());
  } catch (error) {
    document.getElementById("globalState").textContent = "sin datos";
    document.getElementById("frontRows").textContent = `No pude leer dashboard/state.json: ${error.message}`;
  }
}

loadState();
setInterval(loadState, 15000);

function getComponentIcon(componentType) {
  const iconMap = {
    SYSSTAT: "monitoring",
    CHAT: "chat",
    VIEW_CHAT: "chat_bubble",
    DBQUERY: "database",
    VIEW_DBQUERY: "table_view",
    FILEWATCH: "folder",
    MESSAGE_ROTATE: "rotate_right",
    URLGET: "link",
    TIMER: "timer",
    VIEW_TIMER: "schedule",
  };
  return iconMap[componentType] || "widgets";
}

let dashboards = {};

document.addEventListener("DOMContentLoaded", () => {
  loadDashboards();
  handleRoute();

  // Handle browser back/forward buttons
  window.addEventListener("popstate", handleRoute);
});

function handleRoute() {
  const path = window.location.pathname;
  const dashboardName = path.split("/").pop();

  if (dashboardName && dashboardName !== "") {
    showDashboard(dashboardName);
  } else {
    showDashboardList();
  }
  updateNavigation();
}

function createDashboard() {
  const name = prompt("Enter dashboard name:");
  if (!name) return;

  const safeName = name.toLowerCase().replace(/\s+/g, "-");

  if (dashboards[safeName]) {
    alert("Dashboard with this name already exists!");
    return;
  }

  dashboards[safeName] = {
    name: name,
    tabs: [],
  };

  saveDashboards();
  updateNavigation();
  navigateTo(safeName);
}

function initializeDragAndDrop(dashboardName, tabIndex) {
  const componentsContainer = document.querySelector(".components");
  let components = componentsContainer.querySelectorAll(".component");

  components.forEach((component) => {
    component.draggable = true;
    component.addEventListener("dragstart", handleDragStart);
    component.addEventListener("dragend", handleDragEnd);
    component.addEventListener("dragover", handleDragOver);
    component.addEventListener("drop", handleDrop);
  });

  function handleDragStart(e) {
    e.target.classList.add("dragging");
    e.dataTransfer.setData("text/plain", e.target.dataset.index);
  }

  function handleDragEnd(e) {
    e.target.classList.remove("dragging");
  }

  function handleDragOver(e) {
    e.preventDefault();
    const draggingElement = document.querySelector(".dragging");
    if (draggingElement && e.currentTarget !== draggingElement) {
      const draggingRect = draggingElement.getBoundingClientRect();
      const targetRect = e.currentTarget.getBoundingClientRect();

      if (targetRect.top > draggingRect.top) {
        e.currentTarget.parentNode.insertBefore(
          draggingElement,
          e.currentTarget.nextSibling
        );
      } else {
        e.currentTarget.parentNode.insertBefore(
          draggingElement,
          e.currentTarget
        );
      }
    }
  }

  function handleDrop(e) {
    e.preventDefault();
    const newOrder = Array.from(componentsContainer.children).map(
      (comp) => comp.innerHTML
    );
    dashboards[dashboardName].tabs[tabIndex].components = newOrder;
    saveDashboards();
  }
}

function showDashboardList() {
  const mainContent = document.getElementById("main-content");
  mainContent.innerHTML = `
            <div class="header">
                <h2><span class="material-icons">space_dashboard</span>Available Dashboards</h2>
                <button onclick="createDashboard()">
                    <span class="material-icons">add</span>
                    Create New Dashboard
                </button>
            </div>
            <div class="dashboard-list">
                ${Object.entries(dashboards)
                  .map(
                    ([key, dashboard]) => `
                    <div class="dashboard-item" onclick="navigateTo('${key}')">
                        <span class="material-icons">dashboard</span>
                        ${dashboard.name}
                    </div>
                `
                  )
                  .join("")}
            </div>
        `;
}

function navigateTo(dashboardName) {
  const newPath = dashboardName
    ? `/dashboards/${dashboardName}`
    : "/dashboards";
  window.history.pushState({}, "", newPath);
  handleRoute();
}

function createTab(dashboardName) {
  const tabName = prompt("Enter tab name:");
  if (!tabName) return;

  dashboards[dashboardName].tabs.push({
    name: tabName,
    components: [],
  });

  saveDashboards();
  showDashboard(dashboardName);
}

function switchTab(dashboardName, tabIndex) {
  const tabs = document.querySelectorAll(".tab");
  const contents = document.querySelectorAll(".tab-content");
  tabs.forEach((tab) => tab.classList.remove("active"));
  contents.forEach((content) => content.classList.remove("active"));

  tabs[tabIndex].classList.add("active");
  contents[tabIndex].classList.add("active");
}

function createComponent(dashboardName, tabIndex) {
  const componentHTML = `
            <h4>
                <span class="material-icons">widgets</span>
                Component
            </h4>
            <form>
                <div class="form-group">
                    <label for="username">
                        <span class="material-icons">person</span>
                        Username
                    </label>
                    <input type="text" name="username">
                </div>
                <div class="form-group">
                    <label for="filename">
                        <span class="material-icons">description</span>
                        Filename
                    </label>
                    <input type="text" name="filename">
                </div>
                <div class="form-group">
                    <label for="content">
                        <span class="material-icons">edit_note</span>
                        Content
                    </label>
                    <textarea name="content" rows="4"></textarea>
                </div>
                <button type="button" onclick="refreshComponent(this)">
                    <span class="material-icons">refresh</span>
                    Refresh
                </button>
            </form>
        `;

  dashboards[dashboardName].tabs[tabIndex].components.push(componentHTML);
  saveDashboards();
  showDashboard(dashboardName);
}

function refreshComponent(button, command) {
  wsClient.sendCommand({
    obj: command.split(" ")[0],
    method: "refresh",
    params: {},
  });
}

function saveDashboards() {
  localStorage.setItem("dashboards", JSON.stringify(dashboards));
}

function loadDashboards() {
  const saved = localStorage.getItem("dashboards");
  if (saved) {
    dashboards = JSON.parse(saved);
  }
  updateNavigation();
}

function updateNavigation() {
  const nav = document.querySelector(".dashboard-nav");
  nav.innerHTML = `
            <a href="/dashboards" onclick="event.preventDefault(); navigateTo('')">
                <span class="material-icons">home</span>
                Home
            </a>
            ${Object.entries(dashboards)
              .map(
                ([key, dashboard]) => `
                <a href="/dashboards/${key}" 
                    onclick="event.preventDefault(); navigateTo('${key}')"
                    ${
                      window.location.pathname.includes(key)
                        ? 'class="active"'
                        : ""
                    }>
                    <span class="material-icons">space_dashboard</span>
                    ${dashboard.name}
                </a>
            `
              )
              .join("")}
        `;
}

function showDashboard(dashboardName) {
  const dashboard = dashboards[dashboardName];
  if (!dashboard) {
    showDashboardList();
    return;
  }

  const mainContent = document.getElementById("main-content");
  mainContent.innerHTML = `
        <div class="header">
            <h2><span class="material-icons">dashboard</span>${
              dashboard.name
            }</h2>
            <div class="header-actions">
                <button onclick="createTab('${dashboardName}')">
                    <span class="material-icons">add</span>
                    Create New Tab
                </button>
                <button class="delete-btn" onclick="deleteDashboard('${dashboardName}')">
                    <span class="material-icons">delete</span>
                </button>
            </div>
        </div>
        <div class="tabs">
            ${dashboard.tabs
              .map(
                (tab, index) => `
                <div class="tab ${index === 0 ? "active" : ""}" 
                     onclick="switchTab('${dashboardName}', ${index})">
                    <span class="material-icons">tab</span>
                    ${tab.name}
                    <span class="delete-btn" onclick="deleteTab('${dashboardName}', ${index}); event.stopPropagation();">
                        <span class="material-icons">close</span>
                    </span>
                </div>
            `
              )
              .join("")}
        </div>
        <div class="tab-contents">
            ${dashboard.tabs
              .map(
                (tab, index) => `
                <div class="tab-content ${
                  index === 0 ? "active" : ""
                }" id="tab-${index}">
                    <div class="header">
                        <h3>${tab.name}</h3>
                        <button onclick="createComponent('${dashboardName}', ${index})">
                            <span class="material-icons">add_box</span>
                            Add Component
                        </button>
                    </div>
                    <div class="components">
                        ${
                          Array.isArray(tab.components)
                            ? tab.components.join("")
                            : ""
                        }
                    </div>
                </div>
            `
              )
              .join("")}
        </div>
    `;

  initializeDragAndDrop(dashboardName, 0);
}

function deleteDashboard(dashboardName) {
  if (
    confirm(
      `Are you sure you want to delete the dashboard "${dashboards[dashboardName].name}"?`
    )
  ) {
    delete dashboards[dashboardName];
    saveDashboards();
    navigateTo("");
  }
}

function deleteTab(dashboardName, tabIndex) {
  const tabName = dashboards[dashboardName].tabs[tabIndex].name;
  if (confirm(`Are you sure you want to delete the tab "${tabName}"?`)) {
    dashboards[dashboardName].tabs.splice(tabIndex, 1);
    saveDashboards();
    showDashboard(dashboardName);
  }
}

function deleteComponent(button, dashboardName, tabIndex) {
  if (!confirm("Are you sure you want to delete this component?")) {
    return;
  }

  const component = button.closest(".component");
  const componentIndex = Array.from(component.parentNode.children).indexOf(
    component
  );

  // Remove from dashboards object
  dashboards[dashboardName].tabs[tabIndex].components.splice(componentIndex, 1);

  // Save to localStorage
  saveDashboards();
  showDashboard(dashboardName);
}

function createComponent(dashboardName, tabIndex) {
  const components = [
    {
      name: "SYSSTAT",
      description: "Display system statistics",
      hasParams: false,
    },
    {
      name: "CHAT",
      description: "Send chat messages",
      hasParams: true,
      command: "CHAT",
      params: [{ name: "message", label: "Message", type: "text" }],
    },
    {
      name: "VIEW_CHAT",
      description: "View chat history",
      hasParams: false,
    },
    {
      name: "DBQUERY",
      description: "Execute database queries",
      hasParams: true,
      params: [{ name: "query", label: "SQL Query", type: "text" }],
    },
    {
      name: "VIEW_DBQUERY",
      description: "View query results",
      hasParams: false,
    },
    {
      name: "FILEWATCH",
      description: "Monitor file changes",
      hasParams: false,
    },
    {
      name: "MESSAGE_ROTATE",
      description: "Rotate through messages",
      hasParams: false,
    },
    {
      name: "URLGET",
      description: "Fetch URL content",
      hasParams: true,
      params: [{ name: "url", label: "URL", type: "text" }],
    },
    {
      name: "TIMER",
      description: "Timer control",
      hasParams: true,
      params: [
        {
          name: "action",
          label: "Action",
          type: "select",
          options: ["start", "stop", "reset", "pause", "play"],
        },
        {
          name: "seconds",
          label: "Time (seconds)",
          type: "number",
        },
      ],
    },
    {
      name: "VIEW_TIMER",
      description: "View timer status",
      hasParams: false,
    },
  ];

  const dialog = document.createElement("div");
  dialog.className = "dialog";
  dialog.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
`;

  const dialogContent = document.createElement("div");
  dialogContent.style.cssText = `
    background: var(--surface-color);
    padding: 2rem;
    border-radius: 0.75rem;
    width: 90%;
    max-width: 600px;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: var(--shadow-md);
`;

  dialogContent.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
        <h3 style="margin: 0;">Select Component</h3>
        <button onclick="this.closest('.dialog').remove()" style="background: none; border: none;">
            <span class="material-icons">close</span>
        </button>
    </div>
    <div class="component-grid" style="display: grid; gap: 1rem;">
        ${components
          .map(
            (comp) => `
            <div class="component-option" 
                    onclick="handleComponentSelect('${dashboardName}', ${tabIndex}, ${JSON.stringify(
              comp
            ).replace(/"/g, "&quot;")})">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span class="material-icons">widgets</span>
                    <strong>${comp.name}</strong>
                </div>
                <p style="color: var(--text-secondary); margin: 0.5rem 0;">
                    ${comp.description}
                </p>
            </div>
        `
          )
          .join("")}
    </div>
`;

  dialog.appendChild(dialogContent);
  document.body.appendChild(dialog);

  // Add hover effect for component options
  const options = dialogContent.querySelectorAll(".component-option");
  options.forEach((option) => {
    option.addEventListener("mouseover", () => {
      option.style.backgroundColor = "var(--background-color)";
    });
    option.addEventListener("mouseout", () => {
      option.style.backgroundColor = "";
    });
  });
}

function handleComponentSelect(dashboardName, tabIndex, component) {
  if (!component.hasParams) {
    // For components without parameters, send command directly
    sendComponentCommand(dashboardName, tabIndex, component.name);
    document.querySelector(".dialog").remove();
    return;
  }

  // Create parameter input dialog
  const paramDialog = document.createElement("div");
  paramDialog.className = "dialog";
  paramDialog.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
`;

  const paramContent = document.createElement("div");
  paramContent.style.cssText = `
    background: var(--surface-color);
    padding: 2rem;
    border-radius: 0.75rem;
    width: 90%;
    max-width: 500px;
    box-shadow: var(--shadow-md);
`;

  paramContent.innerHTML = `
    <h3>${component.name} Parameters</h3>
    <form onsubmit="event.preventDefault(); handleParamSubmit(this, '${dashboardName}', ${tabIndex}, '${
    component.name
  }')">
        ${component.params
          .map(
            (param) => `
            <div class="form-group" style="margin-bottom: 1rem;">
                <label for="${param.name}">${param.label}</label>
                ${
                  param.type === "select"
                    ? `
                    <select name="${param.name}" required>
                        ${param.options
                          .map(
                            (opt) => `
                            <option value="${opt}">${opt}</option>
                        `
                          )
                          .join("")}
                    </select>
                `
                    : `
                    <input type="${param.type}" name="${param.name}" required>
                `
                }
            </div>
        `
          )
          .join("")}
        <button type="submit">Create Component</button>
    </form>
`;

  paramDialog.appendChild(paramContent);
  document.body.appendChild(paramDialog);
  document.querySelector(".dialog").remove();
}

function handleParamSubmit(form, dashboardName, tabIndex, componentName) {
  const formData = new FormData(form);
  let command = componentName;

  formData.forEach((value, key) => {
    command += " " + value;
  });

  sendComponentCommand(dashboardName, tabIndex, command);
  document.querySelector(".dialog").remove();
}

function sendComponentCommand(dashboardName, tabIndex, command) {
  fetch("/send_command/", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: `command=${encodeURIComponent(command)}`,
  })
    .then((response) => response.json())
    .then((data) => {
      const componentHTML = createComponentHTML(
        command,
        data.response,
        dashboardName,
        tabIndex
      );
      dashboards[dashboardName].tabs[tabIndex].components.push(componentHTML);
      saveDashboards();
      showDashboard(dashboardName);
    })
    .catch((error) => console.error("Error:", error));
}

function createComponentHTML(command, response, dashboardName, tabIndex) {
  const commandParts = command.split(" ");
  const componentType = commandParts[0];

  return `
        <div class="component" draggable="true">
            <div class="component-header">
                <h4>
                    <span class="material-icons">${getComponentIcon(
                      componentType
                    )}</span>
                    ${componentType}
                </h4>
                <button onclick="refreshComponent(this, '${command.replace(
                  /'/g,
                  "\\'"
                )}')" class="refresh-btn">
                    <span class="material-icons">refresh</span>
                </button>
                <button onclick="deleteComponent(this, '${dashboardName}', ${tabIndex})" class="delete-btn">
                        <span class="material-icons">delete</span>
                    </button>
            </div>
            <div class="component-content">
                <pre>${response || "No data"}</pre>
            </div>
        </div>
    `;
}

function selectComponent(dashboardName, tabIndex, componentName) {
  if (componentName === "SYSSTAT") {
    // Use the existing TCP client to send SYSSTAT command
    fetch("/send_command/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: "command=SYSSTAT",
    })
      .then((response) => response.json())
      .then((data) => {
        const componentHTML = `
            <div class="component-header">
                <h4>
                    <span class="material-icons">monitoring</span>
                    System Statistics
                </h4>
                <button onclick="refreshSysStat(this, '${dashboardName}', ${tabIndex})">
                    <span class="material-icons">refresh</span>
                    Refresh
                </button>
            </div>
            <div class="sysstat-content">
                <pre>${data.response}</pre>
            </div>
        `;

        dashboards[dashboardName].tabs[tabIndex].components.push(componentHTML);
        saveDashboards();
        showDashboard(dashboardName);
      })
      .catch((error) => console.error("Error:", error));
  }
  document.querySelector(".dialog").remove();
}

function refreshSysStat(button, dashboardName, tabIndex) {
  const componentDiv = button.closest(".component");
  fetch("/send_command/", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: "command=SYSSTAT",
  })
    .then((response) => response.json())
    .then((data) => {
      componentDiv.querySelector(".sysstat-content pre").textContent =
        data.response;
    })
    .catch((error) => console.error("Error:", error));
}

// Helper function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

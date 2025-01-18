$(document).ready(function () {
  // Initialize jQuery UI tabs
  $("#dashboard-tabs").tabs();

  // Initialize component settings dialog
  const settingsDialog = $("#settings-dialog").dialog({
    autoOpen: false,
    modal: true,
    width: 400,
  });

  // Handle drag and drop
  $(".component-item").draggable({
    helper: "clone",
    revert: "invalid",
  });

  $(".components-container").droppable({
    accept: ".component-item",
    drop: function (event, ui) {
      const componentType = ui.draggable.data("component");
      createComponent(componentType, this);
    },
  });

  // Component creation
  function createComponent(componentType, container) {
    // Show settings dialog to configure component
    showComponentSettings(componentType, (settings) => {
      // Send component creation command to server
      wsClient.sendCommand({
        obj: componentType,
        method: "create",
        params: settings,
      });
    });
  }

  // Component settings form
  function showComponentSettings(componentType, callback) {
    const settingsContent = $("#settings-content");
    settingsContent.empty();

    // Get component-specific settings form
    wsClient.sendCommand({
      obj: componentType,
      method: "get_settings_form",
    });

    $("#component-settings-form")
      .off("submit")
      .on("submit", function (e) {
        e.preventDefault();
        const settings = {};
        $(this)
          .serializeArray()
          .forEach((item) => {
            settings[item.name] = item.value;
          });
        callback(settings);
        settingsDialog.dialog("close");
      });

    settingsDialog.dialog("open");
  }

  // Add new tab
  $("#add-tab").click(function () {
    const tabCount = $("#dashboard-tabs ul li").length;
    const tabId = `tab-${tabCount}`;

    // Add tab
    $("<li>")
      .append(`<a href="#${tabId}">Dashboard ${tabCount}</a>`)
      .insertBefore("#add-tab");

    // Add tab content
    $("<div>")
      .attr("id", tabId)
      .addClass("dashboard-tab")
      .append(
        `<div class="components-container" id="components-${tabCount}"></div>`
      )
      .appendTo("#dashboard-tabs");

    // Refresh tabs
    $("#dashboard-tabs").tabs("refresh");

    // Initialize droppable for new container
    $(`#components-${tabCount}`).droppable({
      accept: ".component-item",
      drop: function (event, ui) {
        const componentType = ui.draggable.data("component");
        createComponent(componentType, this);
      },
    });
  });

  // Handle component updates from WebSocket
  wsClient.onComponentUpdate = function (componentData) {
    const component = $(`#component-${componentData.id}`);
    if (component.length) {
      component.find(".component-content").html(componentData.content);
    }
  };

  // Handle periodic updates
  setInterval(() => {
    $(".component[data-auto-refresh='true']").each(function () {
      const componentId = $(this).attr("id").replace("component-", "");
      wsClient.sendCommand({
        obj: componentId,
        method: "refresh",
      });
    });
  }, 5000); // Refresh every 5 seconds
});

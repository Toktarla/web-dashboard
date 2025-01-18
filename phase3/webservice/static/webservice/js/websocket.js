class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.callbacks = new Map();
    this.connect();
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log("Connected to WebSocket server");
    };

    this.ws.onmessage = (event) => {
      const response = JSON.parse(event.data);
      if (response.status === "success") {
        this.handleSuccess(response.value);
      } else {
        console.error("Server error:", response.reason);
      }
    };

    this.ws.onclose = () => {
      console.log("Disconnected from WebSocket server");
      // Attempt to reconnect after 5 seconds
      setTimeout(() => this.connect(), 5000);
    };
  }

  sendCommand(command) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(
        JSON.stringify({
          command: command,
        })
      );
    } else {
      console.error("WebSocket is not connected");
    }
  }

  handleSuccess(data) {
    // Update dashboard components based on response
    if (data.type === "component_update") {
      this.updateComponent(data.component);
    } else if (data.type === "notification") {
      this.showNotification(data.message);
    }
  }

  updateComponent(componentData) {
    const component = document.querySelector(
      `[data-component-id="${componentData.id}"]`
    );
    if (component) {
      component.querySelector(".component-content").innerHTML =
        componentData.content;
    }
  }

  showNotification(message) {
    // Implement notification display logic
    console.log("Notification:", message);
  }
}

// Initialize WebSocket client
const wsClient = new WebSocketClient("ws://localhost:8008");

from websockets.sync import server
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
import json
from agent import AgentThread
from observer import Observer

global_observer = Observer(4)

class WebSocketServer:
    def __init__(self, port, host, components):
        self.port = port
        self.host = host
        self.components = components
        
    def agent(self, websocket):
        peer = websocket.remote_address
        try:
            while True:
                message = websocket.recv()
                try:
                    data = json.loads(message)
                    response = self.handle_command(data)
                    websocket.send(json.dumps(response))
                except json.JSONDecodeError:
                    websocket.send(json.dumps({
                        "status": "fail",
                        "reason": "Invalid JSON format"
                    }))
        except ConnectionClosedOK:
            print(f"Client {peer} disconnected normally")
        except ConnectionClosedError as e:
            print(f"Client {peer} connection error: {e}")
            
    def handle_command(self, data):
        try:
            command = data.get("command")
            if not command:
                return {
                    "status": "fail",
                    "reason": "No command specified"
                }
                
            # Convert JSON command to string format for existing handler
            cmd_str = command
            if isinstance(command, dict):
                obj = command.get("obj")
                method = command.get("method")
                params = command.get("params", {})
                cmd_str = f"{obj}.{method}"
                if params:
                    param_str = " ".join(f"{k}={v}" for k, v in params.items())
                    cmd_str = f"{cmd_str} {param_str}"
            
            # Use existing TCP client to handle command
            response = self.components.get("agent").process_command(cmd_str)
            
            return {
                "status": "success",
                "value": response
            }
            
        except Exception as e:
            return {
                "status": "fail",
                "reason": str(e)
            }
            
    def run(self):
        print(f"WebSocket server starting on {self.host}:{self.port}")
        ws_server = server.serve(self.agent, host=self.host, port=self.port)
        ws_server.serve_forever() 
import socket
import threading
import json
from features.repo import Repo

class DashboardServer:
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', port))
        self.sock.listen(5)
        self.clients = {}  # username -> Agent mapping
        self.lock = threading.Lock()

    def start(self):
        print(f"Server started on port {self.port}")
        while True:
            client_sock, addr = self.sock.accept()
            agent = Agent(client_sock, self)
            agent.start()
class Agent(threading.Thread):
    def __init__(self, sock, server):
        super().__init__()
        self.sock = sock
        self.server = server
        self.username = None
        self.dashboard = None
        self.running = True
        self.component_params = {}

    def set_component_param(self, component_id, param_name, value):
        if component_id not in self.component_params:
            self.component_params[component_id] = {}
        self.component_params[component_id][param_name] = value
        
    def get_component_param(self, component_id, param_name):
        return self.component_params.get(component_id, {}).get(param_name)
    
    def component_updated(self, component):
        if self.dashboard:
            self.send_response(f"COMPONENT_UPDATE {component.name}")
            
    def handle_command(self, cmd_parts):
        if not cmd_parts:
            return

        cmd = cmd_parts[0].upper()
        
        if cmd == 'USER' and len(cmd_parts) > 1:
            self.handle_user(cmd_parts[1])
            
        elif cmd == 'ATTACH' and len(cmd_parts) > 1:
            self.handle_attach(int(cmd_parts[1]))
            
        elif cmd == 'LIST':
            self.handle_list()
            
        elif cmd == 'CREATE' and len(cmd_parts) > 1:
            self.handle_create(cmd_parts[1])
            
        elif cmd == 'SET_PARAM' and len(cmd_parts) >= 4:
            component_id = cmd_parts[1]
            param_name = cmd_parts[2]
            value = cmd_parts[3]
            self.set_component_param(component_id, param_name, value)
            self.send_response("Parameter set successfully")
            
        elif cmd == 'GET_PARAM' and len(cmd_parts) >= 3:
            component_id = cmd_parts[1]
            param_name = cmd_parts[2]
            value = self.get_component_param(component_id, param_name)
            self.send_response(str(value))
        
        elif cmd == 'SAVE':
            Repo.save_state('dashboard_state.pkl')
            self.send_response("State saved successfully")

        elif cmd == 'LOAD':
            Repo.load_state('dashboard_state.pkl')
            self.send_response("State loaded successfully")
        
        elif cmd == 'TRIGGER' and len(cmd_parts) >= 3:
            component_id = cmd_parts[1]
            event = cmd_parts[2]
            params = json.loads(cmd_parts[3]) if len(cmd_parts) > 3 else None
            self.handle_trigger(component_id, event, params)
            
        elif cmd == 'REFRESH' and len(cmd_parts) >= 2:
            component_id = cmd_parts[1]
            self.handle_refresh(component_id)
            
        else:
            self.send_response(f"ERROR: Unknown command '{cmd}'")

    def handle_trigger(self, component_id, event, params=None):
        try:
            component = self.dashboard.find_component(component_id)
            if component:
                component.trigger(event, params)
                self.send_response("Event triggered successfully")
            else:
                self.send_response(f"ERROR: Component {component_id} not found")
        except Exception as e:
            self.send_response(f"ERROR: {str(e)}")

    def handle_refresh(self, component_id):
        try:
            component = self.dashboard.find_component(component_id)
            if component:
                component.refresh()
                self.send_response("Component refreshed successfully")
            else:
                self.send_response(f"ERROR: Component {component_id} not found")
        except Exception as e:
            self.send_response(f"ERROR: {str(e)}")

    def run(self):
        while self.running:
            try:
                command = self.read_command()
                if not command:
                    break
                
                self.handle_command(command)
            except Exception as e:
                print(f"Error handling client: {e}")
                break
        
        self.cleanup()

    def read_command(self):
        try:
            data = self.sock.recv(1024).decode('utf-8')
            if not data:
                return None
            return data.strip().split()
        except:
            return None

    def handle_user(self, username):
        with self.server.lock:
            if username in self.server.clients:
                self.send_response("ERROR: Username already taken")
                return
            
            self.username = username
            self.server.clients[username] = self
            self.send_response(f"Welcome {username}")

    def handle_attach(self, dashboard_id):
        try:
            self.dashboard = Repo.attach(dashboard_id, self.username)
            self.send_response(f"Attached to dashboard {dashboard_id}")
        except Exception as e:
            self.send_response(f"ERROR: {str(e)}")

    def handle_list(self):
        dashboards = Repo.list()
        self.send_response(json.dumps(list(dashboards)))

    def handle_create(self, name):
        dashboard_id = Repo.create(name)
        self.send_response(f"Created dashboard {dashboard_id}")

    def send_response(self, message):
        try:
            self.sock.send(f"{message}\n".encode('utf-8'))
        except:
            self.running = False

    def cleanup(self):
        if self.username:
            with self.server.lock:
                del self.server.clients[self.username]
        
        try:
            self.sock.close()
        except:
            pass
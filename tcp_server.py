from utils.logger import log
from observer import Observer
from timer_thread import TimerThread
import asyncio
import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
import json
global_observer = Observer(4)


class TCPServer:
    def __init__(self, port, host, components, observer):
        self.port = port
        self.host = host
        self.username = None
        self.observer = observer
        vset = list(range(len(self.observer.values)))
        self.cond = self.observer.register(self, vset)
        self.components = components
        self.timer_thread = TimerThread()
        self.timer_thread.start()

    async def agent(self, wsock):
        peer = wsock.remote_address
        log(f"Connection established with {peer}")
        try:
            while True:
                inp = await wsock.recv()
                
                log(f"Received message from {peer}: {inp}")
                data = json.loads(inp)
                command = data.get("method", "")
                await self.process_command(command, wsock=wsock)
        except ConnectionClosedOK:
            log(f"Connection closed peacefully with {peer}")
        except ConnectionClosedError:
            log(f"Connection closed with error from {peer}")

    async def process_command(self, command, wsock):  # Accept wsock as a parameter
        log(f"Processing command: {command}")
        
        parts = command.split()
        if not parts:
            await wsock.send(json.dumps({"status": "fail", "value": "Empty command"}))
            return

        cmd = parts[0].upper()
        if cmd == "USER":
            if len(parts) < 2:
                await wsock.send(json.dumps({"status": "fail", "value": "Usage: USER <username>"}))
                return
            self.username = parts[1]
            await wsock.send(json.dumps({"status": "success", "value": f"Username set to {self.username}"}))

        elif cmd == "UPLOAD":
            if len(parts) < 3:
                await wsock.send(json.dumps({"status": "fail", "value": "Usage: UPLOAD <filename> <content>"}))
                return
            filename, content = parts[1], " ".join(parts[2:])
            try:
                self.components["FileShare"].upload(filename, content)
                await wsock.send(json.dumps({"status": "success", "value": f"Uploaded {filename}"}))
                self.notify_others(f"{self.username} uploaded a file: {filename}")
            except Exception as e:
                await wsock.send(json.dumps({"status": "fail", "value": f"Error uploading file: {e}"}))

        elif cmd == "DOWNLOAD":
            if len(parts) < 2:
                await wsock.send(json.dumps({"status": "fail", "value": "Usage: DOWNLOAD <filename>"}))
                return
            filename = parts[1]
            try:
                content = self.components["FileShare"].download(filename)
                await wsock.send(json.dumps({"status": "success", "value": f"Content: {content}"}))
                self.notify_others(f"{self.username} downloaded a file: {filename}")
            except FileNotFoundError:
                await wsock.send(json.dumps({"status": "fail", "value": f"File {filename} not found"}))

        elif cmd == "DELETE":
            if len(parts) < 2:
                await wsock.send(json.dumps({"status": "fail", "value": "Usage: DELETE <filename>"}))
                return
            filename = parts[1]
            try:
                self.components["FileShare"].delete(filename)
                await wsock.send(json.dumps({"status": "success", "value": f"Deleted {filename}"}))
                self.notify_others(f"{self.username} deleted a file: {filename}")
            except FileNotFoundError:
                await wsock.send(json.dumps({"status": "fail", "value": f"File {filename} not found"}))

        elif cmd == "CHAT":
            if len(parts) < 2:
                await wsock.send(json.dumps({"status": "fail", "value": "Usage: CHAT <message>"}))
                return
            message = " ".join(parts[1:])
            self.components["Chat"].param['mess'] = message
            self.components["Chat"].submit()
            await wsock.send(json.dumps({"status": "success", "value": f"Chat message added: {message}"}))
            self.notify_others(f"{self.username} sent a chat message.")

        elif cmd == "VIEW_CHAT":
            chat_view = self.components["Chat"].view()
            await wsock.send(json.dumps({"status": "success", "value": chat_view}))

        elif cmd == "DBQUERY":
            if len(parts) < 2:
                await wsock.send(json.dumps({"status": "fail", "value": "Usage: DBQUERY <query>"}))
                return
            query = " ".join(parts[1:])
            self.components["DBQuery"].env['query'] = query
            self.components["DBQuery"].refresh()
            await wsock.send(json.dumps({"status": "success", "value": "DB Query executed."}))
            self.notify_others(f"{self.username} executed a database query.")

        elif cmd == "VIEW_DBQUERY":
            query_results = self.components["DBQuery"].view()
            await wsock.send(json.dumps({"status": "success", "value": query_results}))

        elif cmd == "DBUPDATE":
            if len(parts) < 2:
                await wsock.send(json.dumps({"status": "fail", "value": "Usage: DBUPDATE <query>"}))
                return
            query = " ".join(parts[1:])
            self.components["DBUpdate"].set_query(query)
            self.components["DBUpdate"].execute({})
            await wsock.send(json.dumps({"status": "success", "value": f"DB Update executed: {query}"}))
            self.notify_others(f"{self.username} executed a database update.")

        elif cmd == "FILEWATCH":
            self.components["FileWatch"].refresh()
            file_watch_view = self.components["FileWatch"].view()
            await wsock.send(json.dumps({"status": "success", "value": file_watch_view}))
            self.notify_others(f"{self.username} accessed file watch.")

        elif cmd == "MESSAGE_ROTATE":
            self.components["MessageRotate"].refresh()
            message_view = self.components["MessageRotate"].view()
            await wsock.send(json.dumps({"status": "success", "value": message_view}))
            self.notify_others(f"{self.username} viewed message rotation.")

        elif cmd == "SYSSTAT":
            self.components["SysStat"].refresh()
            system_stats = self.components["SysStat"].view()
            await wsock.send(json.dumps({"status": "success", "value": system_stats}))
            self.notify_others(f"{self.username} accessed system stats.")

        elif cmd == "URLGET":
            if len(parts) < 2:
                await wsock.send(json.dumps({"status": "fail", "value": "Usage: URLGET <url>"}))
                return
            url = parts[1]
            self.components["URLGetter"].env['url'] = url
            self.components["URLGetter"].refresh()
            url_content = self.components["URLGetter"].view()
            await wsock.send(json.dumps({"status": "success", "value": url_content}))
            self.notify_others(f"{self.username} performed a URL fetch: {url}")

        elif cmd == "TIMER":
            if len(parts) < 3:
                await wsock.send(json.dumps({"status": "fail", "value": "Usage: TIMER <start/stop/reset/pause/play> <time_in_seconds>"}))
                return
            action = parts[1].lower()
            value = int(parts[2]) if len(parts) > 2 else 0
            if action == "start":
                self.components["Timer"].env['value'] = value
                self.components["Timer"].start()
                await wsock.send(json.dumps({"status": "success", "value": f"Timer started for {value} seconds."}))
            self.notify_others(f"{self.username} started the clock")
        elif cmd == "VIEW_TIMER":
            try:
                timer_status = self.components["Timer"].view()
                await wsock.send(json.dumps({"status": "success", "value": timer_status}))
            except Exception as e:
                await wsock.send(json.dumps({"status": "fail", "value": f"Error viewing timer: {e}"}))

        else:
            await wsock.send(json.dumps({"status": "fail", "value": "Unknown command"}))

    async def start_server(self):
        async with websockets.serve(self.agent, self.host, self.port):
            await asyncio.Future()  # Run forever

    def notify_others(self, message):
        with self.observer.mut:
            for observer, (vset, cond) in self.observer.observers.items():
                if observer != self:
                    try:
                        observer.send(f"Notification: {message}")
                    except Exception as e:
                        log(f"Error notifying observer: {e}")

    def run(self):
        asyncio.run(self.start_server())
        log("Server has started!")


    
 
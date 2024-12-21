from threading import Thread

from utils.logger import log


class AgentThread(Thread):
    def __init__(self, client_socket, address, components, observer):
        super().__init__(daemon=True)
        self.client_socket = client_socket
        self.address = address
        self.username = None
        self.components = components
        self.observer = observer
        vset = list(range(len(self.observer.values)))
        self.cond = self.observer.register(self, vset)


    def run(self):
        log(f"Connection established with {self.address}")
        try:
            while True:
                data = self.client_socket.recv(1024).decode("utf-8")
                if not data:
                    log(f"Connection closed by {self.address}")
                    break
                log(f"Command received: {data}")
                self.process_command(data.strip())
        except Exception as e:
            log(f"Error in thread for {self.address}: {e}")
        finally:
            self.client_socket.close()
            log(f"Connection with {self.address} closed.")

    def send(self, message):
        self.client_socket.sendall((message + "\n").encode("utf-8"))

    def process_command(self, command):
        log(f"Processing command: {command}")
        parts = command.split()
        if not parts:
            self.send("Empty command")
            return

        cmd = parts[0].upper()
        if cmd == "USER":
            if len(parts) < 2:
                self.send("Usage: USER <username>")
                return
            self.username = parts[1]
            self.send(f"Username set to {self.username}")

        elif cmd == "UPLOAD":
            if len(parts) < 3:
                self.send("Usage: UPLOAD <filename> <content>")
                return
            filename, content = parts[1], " ".join(parts[2:])
            try:
                self.components["FileShare"].upload(filename, content)
                self.send(f"Uploaded {filename}")
                self.notify_others(f"{self.username} uploaded a file: {filename}")
            except Exception as e:
                self.send(f"Error uploading file: {e}")

        elif cmd == "DOWNLOAD":
            if len(parts) < 2:
                self.send("Usage: DOWNLOAD <filename>")
                return
            filename = parts[1]
            try:
                content = self.components["FileShare"].download(filename)
                self.send(f"Content: {content}")
                self.notify_others(f"{self.username} downloaded a file: {filename}")
            except FileNotFoundError:
                self.send(f"File {filename} not found")
        # elif cmd == "TEST":
        #     if len(parts) < 3:
        #         self.send("Usage: TEST <component_name> <interval_seconds>")
        #         return
        #     component_name = parts[1]
        #     interval_seconds = int(parts[2])
        #     component = self.components.get(component_name)
        #
        #     if component:
        #         self.timer_thread.add_timer(component, interval_seconds)
        #         self.send(f"Interval seconds for {component_name} set to {interval_seconds} seconds.")
        #     else:
        #         self.send(f"Component {component_name} not found.")

        elif cmd == "DELETE":
            if len(parts) < 2:
                self.send("Usage: DELETE <filename>")
                return
            filename = parts[1]
            try:
                self.components["FileShare"].delete(filename)
                self.send(f"Deleted {filename}")
                self.notify_others(f"{self.username} deleted a file: {filename}")
            except FileNotFoundError:
                self.send(f"File {filename} not found")

        elif cmd == "CHAT":
            if len(parts) < 2:
                self.send("Usage: CHAT <message>")
                return
            message = " ".join(parts[1:])
            self.components["Chat"].param['mess'] = message
            self.components["Chat"].submit()
            self.send(f"Chat message added: {message}")
            self.notify_others(f"{self.username} sent a chat message.")

        elif cmd == "VIEW_CHAT":
            chat_view = self.components["Chat"].view()
            self.send(chat_view)

        elif cmd == "DBQUERY":
            if len(parts) < 2:
                self.send("Usage: DBQUERY <query>")
                return
            query = " ".join(parts[1:])
            self.components["DBQuery"].env['query'] = query
            self.components["DBQuery"].refresh()
            self.send("DB Query executed.")
            self.notify_others(f"{self.username} executed a database query.")

        elif cmd == "VIEW_DBQUERY":
            query_results = self.components["DBQuery"].view()
            self.send(query_results)

        elif cmd == "DBUPDATE":
            if len(parts) < 2:
                self.send("Usage: DBUPDATE <query>")
                return
            query = " ".join(parts[1:])
            self.components["DBUpdate"].set_query(query)
            self.components["DBUpdate"].execute({})
            self.send(f"DB Update executed: {query}")
            self.notify_others(f"{self.username} executed a database update.")

        elif cmd == "FILEWATCH":
            self.components["FileWatch"].refresh()
            file_watch_view = self.components["FileWatch"].view()
            self.send(file_watch_view)
            self.notify_others(f"{self.username} accessed file watch.")

        elif cmd == "MESSAGE_ROTATE":
            self.components["MessageRotate"].refresh()
            message_view = self.components["MessageRotate"].view()
            self.send(message_view)
            self.notify_others(f"{self.username} viewed message rotation.")

        elif cmd == "SYSSTAT":
            self.components["SysStat"].refresh()
            system_stats = self.components["SysStat"].view()
            self.send(system_stats)
            self.notify_others(f"{self.username} accessed system stats.")

        elif cmd == "URLGET":
            if len(parts) < 2:
                self.send("Usage: URLGET <url>")
                return
            url = parts[1]
            self.components["URLGetter"].env['url'] = url
            self.components["URLGetter"].refresh()
            self.send(self.components["URLGetter"].view())
            self.notify_others(f"{self.username} performed a URL fetch: {url}")

        elif cmd == "TIMER":
            if len(parts) < 3:
                self.send("Usage: TIMER <start/stop/reset/pause/play> <time_in_seconds>")
                return
            action = parts[1].lower()
            value = int(parts[2]) if len(parts) > 2 else 0
            if action == "start":
                self.components["Timer"].env['value'] = value
                self.components["Timer"].start()
                self.send(f"Timer started for {value} seconds.")
                self.notify_others(f"{self.username} started a timer for {value} seconds.")
            elif action == "stop":
                self.components["Timer"].stop()
                self.send("Timer stopped.")
                self.notify_others(f"{self.username} stopped the timer.")
            elif action == "reset":
                self.components["Timer"].env['value'] = value
                self.components["Timer"].reset()
                self.send("Timer reset.")
                self.notify_others(f"{self.username} reset the timer.")
            elif action == "pause":
                self.components["Timer"].pause()
                self.send("Timer paused.")
                self.notify_others(f"{self.username} paused the timer.")
            elif action == "play":
                self.components["Timer"].play()
                self.send("Timer resumed.")
                self.notify_others(f"{self.username} resumed the timer.")
            else:
                self.send("Invalid TIMER action. Use start, stop, reset, pause, or play.")

        elif cmd == "VIEW_TIMER":
            timer_status = self.components["Timer"].view()
            self.send(timer_status)

        else:
            self.send("Unknown command")

    def notify_others(self, message):
        with self.observer.mut:
            for observer, (vset, cond) in self.observer.observers.items():
                if observer != self:
                    try:
                        observer.send(f"Notification: {message}")
                    except Exception as e:
                        log(f"Error notifying observer: {e}")

import socket
from agent import AgentThread
from widgets.db_update import DBUpdate
from widgets.file_share import FileShare
from widgets.item import Item
from utils.logger import log
from observer import Observer
from timer_thread import TimerThread

global_observer = Observer(4)


class TCPServer:
    def __init__(self, port, host, components):
        self.port = port
        self.host = host
        self.components = components
        self.timer_thread = TimerThread()
        self.timer_thread.start()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        log(f"Server started on {self.host}:{self.port}")

    def run(self):
        while True:
            client_socket, address = self.sock.accept()
            agent = AgentThread(client_socket, address, self.components, global_observer) # self.timer_thread
            agent.start()


    
 
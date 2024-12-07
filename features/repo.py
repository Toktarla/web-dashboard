import uuid
from features.dash import Dash
from server import Agent, DashboardServer
from utils.db import create_user, remove_user
import pickle


class Repo:
    dashboards = {}
    components = {}
    users = {}

    @staticmethod
    def create(name):
        dashboard_id = uuid.uuid4().int >> 96
        dashboard = Dash(name)
        Repo.dashboards[dashboard_id] = dashboard

        return dashboard_id

    @staticmethod
    def list():
        print("Listing Dashboards:")
        for dash_id, dash in Repo.dashboards.items():
            attached_users = [user for user, attached_dash in Repo.users.items() if attached_dash == dash]
            user_list = ", ".join(attached_users) if attached_users else "No users attached"
            print(f"ID: {dash_id}, Name: {dash.name}, Users: {user_list}")
        return Repo.dashboards.keys()

    @staticmethod
    def attach(dash_id, user_name):
        Repo.users[user_name] = Repo.dashboards[dash_id]
        print(f"User '{user_name}' attached to dashboard ID {dash_id}.")
        create_user(user_name, dash_id)

        return Repo.users[user_name]

    @staticmethod
    def detach(dash_id, user_name):
        if user_name in Repo.users:
            remove_user(user_name)  # Remove user from the database
            del Repo.users[user_name]
            print(f"User '{user_name}' detached from dashboard ID {dash_id}.")
        else:
            print(f"User '{user_name}' not found.")

    @staticmethod
    def register_component(name, cls):
        Repo.components[name] = cls

    @staticmethod
    def list_components():
        print("Listing Available Components: " + ", ".join(Repo.components.keys()))
        return Repo.components.__len__()

    @staticmethod
    def create_component(name):
        if name in Repo.components:
            component = Repo.components[name]()
            if component.refresh_interval > 0:
                for client in DashboardServer.instance.clients.values():
                    if isinstance(client, Agent):
                        client.server.timer_thread.add_component(component, component.refresh_interval)
            return component
        raise ValueError(f"Component '{name}' not registered.")
    
    @staticmethod
    def save_state(filename):
        state = {
            'dashboards': Repo.dashboards,
            'users': Repo.users
        }
        with open(filename, 'wb') as f:
            pickle.dump(state, f)

    @staticmethod
    def load_state(filename):
        try:
            with open(filename, 'rb') as f:
                state = pickle.load(f)
                Repo.dashboards = state['dashboards']
                Repo.users = state['users']
        except FileNotFoundError:
            print(f"No saved state found at {filename}")
class Repo:
    _instance = None
    _objects = {}
    _components = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Repo, cls).__new__(cls)
        return cls._instance

    def create(self, name):
        obj_id = id(name)
        self._objects[obj_id] = {'name': name, 'tabs': []}
        return obj_id

    def list(self):
        return [(obj_id, info['name']) for obj_id, info in self._objects.items()]

    def attach(self, obj_id, user):
        obj = self._objects.get(obj_id)
        if obj:
            obj['attached'] = user
        return obj

    def detach(self, obj_id, user):
        obj = self._objects.get(obj_id)
        if obj and obj.get('attached') == user:
            obj.pop('attached', None)

    def delete(self, obj_id):
        self._objects.pop(obj_id, None)

    def register_component(self, type_name, cls):
        self._components[type_name] = cls

    def list_components(self):
        return list(self._components.keys())

    def create_component(self, type_name):
        component_class = self._components.get(type_name)
        return component_class() if component_class else None

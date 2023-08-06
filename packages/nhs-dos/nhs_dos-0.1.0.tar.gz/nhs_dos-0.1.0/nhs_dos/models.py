class Service:
    def __init__(self, service_json):
        self.json = service_json
        self.id = service_json['id']
        self.name = service_json['name']
        self.endpoints = []
        for ep in service_json['endpoints']:
            self.endpoints.append(Endpoint(ep))


class Endpoint:
    def __init__(self, endpoint):
        parts = endpoint['value'].split('\|')
        self.transport = endpoint['tag']
        self.order = endpoint['order']
        self.uri = parts[0]
        self.interaction = parts[1]
        self.format = parts[2]
        self.scenario = parts[3]
        self.message = parts[4]
        self.compressed = parts[5]


class ServiceList:
    def __init__(self, service_list: list=None):

        self._service_list = []

        for service in service_list:
            self._service_list.append(service)

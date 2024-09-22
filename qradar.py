class QRadar:
    def __init__(self, url, key, version, transport, verify=True):
        self.url, self.key, self.session = f"{url}/api", key, transport
        self.session.headers.update(
            {"Accept": "application/json", "Version": version, "SEC": key}
        )
        self.session.verify = verify
        self.api_methods = {
            f"{(method:=endpoint.get("http_method").lower())}{(path:=endpoint.get("path"))
            .translate({ord('{'):None, ord('}'): None, ord('/'): ord('_')})}": self.api_endpoint_factory(
                method, path
            )
            for endpoint in self.api_endpoint_factory("GET", "/help/endpoints")(
                filter=f"version={version}"
            )
        }

    def __getattr__(self, name: str):
        return self.api_methods.get(name) or super().__getattribute__(name)

    def api_endpoint_factory(self, method, url):
        return lambda path=None, json=None, **params: self.session.request(
            method,
            f"{self.url}/{url}{f'/{path}' if path else ''}".format(**params),
            params=params,
            json=json,
        ).json()

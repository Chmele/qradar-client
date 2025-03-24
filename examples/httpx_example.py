import httpx
from key import KEY


class QRadar:
    def __init__(self, url, key, version, transport, verify=True):
        self.url, self.key, self.session = f"{url}/api", key, transport
        self.session.headers.update(
            {"Accept": "application/json", "Version": version, "SEC": key}
        )
        self.session.verify = verify
        self.api_methods = {
            f"{(method:=endpoint.get("http_method").lower())}{(path:=endpoint.get("path"))
            .replace("/", "_")}": self.api_endpoint_factory(
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
            f"{self.url}/{url}{f'/{path}' if path else ''}",
            params=params,
            json=json,
        ).json()


q = QRadar("https://qradar.local", KEY, "22.0", httpx.Client(verify=False))
print(q.get_reference_data_sets("refset"))

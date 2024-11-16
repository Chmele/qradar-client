class QRadar:
    def __init__(self, url, key, version, transport, verify=True):
        self.url, self.session = f"{url}/api", transport
        self.session.headers.update(
            {"Accept": "application/json", "Version": version, "SEC": key}
        )
        self.session.verify = verify
        self.version = version

    def __await__(self):
        return self.set_methods().__await__()

    async def set_methods(self):
        self.__dict__.update(
            {
                f"""{(method:=endpoint.get("http_method").lower())}{(path:=endpoint.get("path"))
                .translate({ord('{'):None, ord('}'): None, ord('/'): ord('_')})}""": self.api_endpoint_factory(
                    method.upper(), path
                )
                for endpoint in await self.api_endpoint_factory(
                    "GET", "/help/endpoints"
                )(filter=f"version={self.version}")
            }
        )
        return self

    def api_endpoint_factory(self, method, url):
        async def endpoint(json=None, **params):
            response = await self.session.request(
                method,
                f"{self.url}{url}".format(**params),
                params=params,
                json=json,
            )
            return response.json()
        return endpoint

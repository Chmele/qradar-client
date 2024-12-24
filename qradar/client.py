class QRadar:
    def __init__(self, base_url, key, version, transport, verify=True):
        transport.verify = verify
        self.api_endpoint_factory = lambda method, url: lambda json=None, **params: transport.request(
            method, f"{base_url}/api{url}".format(**params), 
            params=params, json=json,
            headers={"Accept": "application/json", "Version": version, "SEC": key}
        ).json()
        self.__dict__.update({
            f"""{(method:=endpoint.get("http_method").lower())}{(path:=endpoint.get("path"))
            .translate({ord('{'): None, ord('}'): None, ord('/'): ord('_'), ord('-'): ord('_')})}""": self.api_endpoint_factory(
                method.upper(), path
            )
            for endpoint in self.api_endpoint_factory("GET", "/help/endpoints")(
                filter=f"version={version}",
                fields="http_method, path"
            )
        })
import httpx
from key import KEY

QRadar=lambda b,k,v,t:type("QRadar",(),{f"{(m:=e.get("http_method").lower())}{(p:=e.get("path")).translate({ord('{'):None,ord('}'):None,ord('/'):ord('_')})}":(lambda m,u:lambda j=None,**p:t.request(m,f"{b}/api/{u}".format(**p),params=p,json=j,headers={"Accept":"application/json","Version":v,"SEC":k},).json())(m,p)for e in(lambda m,u:lambda j=None,**p:t.request(m,f"{b}/api/{u}".format(**p),params=p,json=j,headers={"Accept":"application/json","Version":v,"SEC":k},).json())("GET","/help/endpoints")(filter=f"version={v}")})

q = QRadar("https://qradar.is.local", KEY, "22.0", httpx.Client(verify=False))
print(q.get_ariel_searches())

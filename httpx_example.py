import httpx
from key import KEY
from qradar import QRadar


q = QRadar("https://qradar.local", KEY, "22.0", httpx.Client(verify=False))
print(q.get_reference_data_sets("refset"))

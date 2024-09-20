# QRadar API python client for scripting

> python3.10 and above supported

Features:
- Pulls API schema from QRadar and creates client methods dynamically for the API version specified. This makes this client source code as small as possible;
- All the endpoints of QRadar API is mapped to a client method by name;
- No dependencies introduced, tested with httpx and requests http protocol libs with dependency injection, but ibviously will only work with libs that provide compatible requests-like interface for Session-like object. Of course, wrappers can solve the problem;

## Intended usage
Made to be used as full-featured copypaste drop-in client for scripts where pip installation way be unwanted, also it is lightweight alternative to qradar4py, where the method lookup table only takes 170 times more memory 🙂. Of course, it is not prohibited to import the `qradar.py` file as a module, as it made in examples.

## How to use
0) Copy the `qradar.py` file contents right after the imports of script
1) Initialize client as following:
```python
q = QRadar("https://qradar.local", KEY, "22.0", requests.Session(), verify=False) 
```
Having:
- qradar.is.local is QRadar console hostname
- KEY is API key created from console
- `"22.0"` - replaced with API version you want
- `requests` imported

> Also works with httpx, with minor differences. Refer to examples for details

2) Use client instance methods, forming the name of desired endpoint

For example, the endpoint `22.0 - GET - /reference_data/map_of_sets` is referenced by name `q.get_reference_data_map_of_sets`. The http method goes first, and the API endpoint path is trailing it, having the slashes replaced with underscores.

For endpoints such as `22.0 - GET - /reference_data/map_of_sets/{name}`
use the same method as above, with {name} part provided as first parameter:
`q.get_reference_data_map_of_sets('refmapofsetsname')`

For params such as filter, use keyword arguments `q.help_endpoint(filter=f"version={version}")`

For data posting, use second argument. It accepts json-serializable objects (lists, dicts, lists of dicts, etc.)

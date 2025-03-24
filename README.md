# QRadar API python client for scripting

> python3.10 and above supported

Features:
- Pulls API schema from QRadar and creates client methods dynamically for the API version specified. This makes this client source code as small as possible;
- Asyncronous and client with schema caching introduced
- All the endpoints of QRadar API is mapped to a client method by name;
- No dependencies introduced, tested with httpx and requests http protocol libs with dependency injection, but obviously will only work with libs that provide compatible requests-like interface for Session-like object. Of course, wrappers can help with using incompatible libs;
- Generates stub file for method hinting if needed. It takes ~10MB of disk space.

## Installation

`pip install qradar`

 or with requests/httpx correspondingly:

`pip install qradar[requests]`

`pip install qradar[httpx]`

## Intended usage
Made to be used as full-featured copypaste drop-in client for scripts where pip installation way be unwanted. Of course, it is not prohibited to install this package with pip.

## How to use any client (refer to examples for more)
0) Use any of `import` statements:
```python
from qradar import QRadar, QRadarAsync, QRadarCached
```
or copy the coppersonding `qradar/client.py` file contents
1) Initialize client as following:
```python
q = QRadar("https://qradar.is.local", KEY, "22.0", requests.Session(), verify=False) 
```
Having:
- qradar.is.local is QRadar console hostname or ip
- KEY is API key created from console
- `"22.0"` - replaced with API version you want
- `requests` imported (and installed)

> Also works with httpx, with minor differences. Refer to examples for details

2) Use client instance methods, forming the name of desired endpoint

>For example, the endpoint `22.0 - GET - /reference_data/map_of_sets` is referenced by name `q.get_reference_data_map_of_sets`. The http method goes first, and the API endpoint path is trailing it, having the slashes replaced with underscores.

> For endpoints such as `22.0 - GET - /reference_data/map_of_sets/{name}` use the `reference_data_map_of_sets_name`, with {name} part provided as keyword argument:
> `q.get_reference_data_map_of_sets_name(name='refmapofsetsname')`

> For params such as filter, use keyword arguments:
> `q.help_endpoint(filter=f"version={version}")`

> For data posting, use first non-keyword argument. It accepts json-serializable objects (lists, dicts, lists of dicts, etc.):
> `q.post_reference_data_map_of_sets({"data": ["data"]})`

## Generating .pyi file for intellisense
This option may be used for setting up more convenient development environment. Final script version should be delivered without API schema.

1) Clone the repository into project folder
2) Run `python3 schema_prefetch.py` having correct parameters in source code
3) `client.pyi` file must appear. As far as it is in one folder with `client.py`, the methods will be hinted with the names, arguments and description from QRadar API schema
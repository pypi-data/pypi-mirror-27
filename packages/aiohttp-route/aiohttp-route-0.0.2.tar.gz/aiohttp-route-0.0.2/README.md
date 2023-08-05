# aiohttp-route
`@route` decorator for aiohttp.web that needs no global variables

## Install

```sh
pip install aiohttp_route
```

## Example

### Basic

File structure:

.

├ views.py

└ run.py


`run.py`:

```py
from aiohttp import web
from aiohttp_route import router


app = web.Application()
routes = router(app, ['views'])
web.run_app(app, host='127.0.0.1', port=8080)
```

`views.py`:

```py
from aiohttp import web
from aiohttp_route import route


@route('GET', '/')
def handler(request):
    return web.HTTPNoContent()
```

### Single File

File structure:

.

└ run.py

`run.py`:

```py
from aiohttp import web
from aiohttp_route import route, router


@route('GET', '/')
def handler(request):
    return web.HTTPNoContent()

app = web.Application()
routes = router(app, ['run'])
web.run_app(app, host='127.0.0.1', port=8080)
```


### With namespaces

File structure:

.

└ my_app

    ├ __init__.py

    ├ views.py

    └ run.py


`run.py`:

 ```py
 from aiohttp import web
 from aiohttp_route import router


 app = web.Application()
 routes = router(app, ['my_app.views'])
 web.run_app(app, host='127.0.0.1', port=8080)
 ```

 `views.py`:

 ```py
 from aiohttp import web
 from aiohttp_route import route


 @route('GET', '/')
 def handler(request):
     return web.HTTPNoContent()
 ```

### Newstyle view functions

The `newstyle` parameter instructs `aiohttp_route` to pass url path variables as
call variables to the view function.

File structure and `run.py` remain the same.

`views.py`

```py
from aiohttp import web
from aiohttp_route import route


@route('GET', '/{uid}', newstyle=True)
def handler(request, uid):
    return web.HTTPNoContent()
```

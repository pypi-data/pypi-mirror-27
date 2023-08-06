flaskbuckle
-------------

Generate swagger documentation from your API implemented in Flask, and expose a
Swagger UI for this API. Tries to do as much as possible automatically, and when
automatically is not possible it tries to be as non-intrusive as possible.
Becomes much better if you bother to use type annotations in your application!

### Quickstart

1. ~~`pip install flaskbuckle`~~~ (coming soon)
2. Add to application configuration:
```python
from flaskbuckle import swagger
...
swagger.enable_swagger(app)
```
3. Access swagger ui at `http://flask-app-url/api/docs`
4. If necessary, access swaggerfile at
   `http://flask-app-url/api/docs/swagger.json`
To use this library, simply add `swagger.enable_swagger(app)` to your where you
configure your application object. This call will do nothing more but add some
routes to your application.

This library is best used with type annotations and docstrings in this manner:


```python
@app.route("/example/<int:parameter>")
def hello_world(parameter: int):
    """A small description of this view"""
    ...
```


### API

##### `swagger.enable_swagger(application: Flask, title="", version="", route="/api/docs")`
Enables swagger for this flask application. By default, the swaggerfile will be
exposed at `http://flask-app-url/api/docs/swagger.json` and Swagger UI will be
exposed at `http://flask-app-url/api/docs` .

Parameters:
- `application: Flask` - an instance of your flask application
- `title: str` - The title of your flask application
- `version: str` - The version string for your application, ex: `"1.0.0"`
- `route: str` - The path to expose swagger documentation on.

##### `@swagger.header(name: str, header_type=str)`
Decorator to mark that this endpoint takes a header parameter.

Parameters:
- `name: str` - The name of the header, ex: `"X-Custom-Header"`
- `header_type` - A type variable declaring what the type of the header is, ex:
  `str`, `Optional[int]`, `bool`

##### `@swagger.query_param(name: str, param_type=str)`
Decorator to mark that this endpoint takes a query string parameter.

Parameters:
- `name: str` - The name of the query string parameter, ex: `include`, `fields`
- `param_type` - A type variable declaring what the type of the header is, ex:
  `str`, `Optional[bool]`, `List[int]`

##### `@swagger.return_model(model: SwaggerModel, status_code: int)`
Decorator to mark that this endpoint has a return model. The return model shall
be a class inheriting from `swagger.SwaggerModel`, and shall have the format
explained in its section. Return models double as both schemas and examples for
the endpoint.

Parameters:
- `model: SwaggerModel` - A class extending from `SwaggerModel`. Note
  that you should not pass an instance of a class; you should reference the
  class directly.
- `status_code: int` - The status code that will return the declared model. ex:
  `200`

##### `class SwaggerModel`
A class describing a return model. Classes inheriting from this class describes
both schemas and examples for endpoints. An example:

```python
from flask_swagger import SwaggerModel

class ExampleModel(SwaggerModel):
    hello: str = "world"


class NestedExampleModel(SwaggerModel):
    foo: int = 1
    bar: SwaggerModel = ExampleModel
```

Would generate the following schemas:
```json
{
    "type": "object",
    "properties": {
        "hello": {
            "type": "string"
        }
    }
},
{
    "type": "object",
    "properties": {
        "foo": {
            "type": "integer",
            "format": "int64"
        },
        "bar": {
            "type": "object",
            "properties": {
                "hello": {
                    "type": "string"
                }
            }
        }
    }
}
```

And the following examples:
```json
{
    "hello": "world"
},
{
    "foo": 1,
    "bar": {
        "hello": "world"
    }
}
```


##### `class SwaggerException`
If at any time you've done something wrong (or gods forbid the implementation of
this library is incorrect), flaskbuckle wont hesitate to raise a
`SwaggerException`, hopefully with some information about why this occured.

##### `swagger.generate_swagger(application: Flask, title="", version="", path="/api/docs") -> dict`
If you need to get the swaggerfile as a dict programmatically for some reason,
flaskbuckle provides a function for this. Note that it *must* be called after
you've added your views to the application: calling it before wont do anything
good at all.

Parameters:
- `application: Flask` - an instance of your flask application
- `title: str` - The title of your flask application
- `version: str` - The version string for your application, ex: `"1.0.0"`
- `route: str` - If you've previously enabled swagger on a custom path you need
  to specify it here, else flaskbuckles own paths will be listed in the returned
  swagger spec.

### Notable swagger extensions
flaskbuckle will generate a `"x-nullable"`-key and set it to `true` for
anything declared with the type `Optional[T]`. As this is non-standard it will
not have any effect on SwaggerUI, but you may find that other tooling can
utilize this field (perhaps most notable for python developers is `flex`).

### TODO
Things that need to be done in this library, in order of priority.

- Replace the SwaggerModel-structure for representing Schemas/Examples - it is not
  flexible enough to provide the functionality we need. Replace with a dict-based
  approach (`key: Any => Tuple[Type, ExampleValue]`)
- Implement post body models
- Add referenced models to `definitions` and reference them via `$ref` instead
  of the naive approach currently used
- Add testing
- Refactor code to not be just a mess in one file
- Implement missing swagger features (I'm sure there are at least a few)


### Thanks to
Swashbuckle, which inspired this library (and its name, once I figured out my
working title was already used)


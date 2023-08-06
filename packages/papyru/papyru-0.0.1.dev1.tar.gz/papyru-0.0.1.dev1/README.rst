======
papyru
======

A minimal toolset to help developing RESTful services on top of django.

Requirements
============

- bravado is used for validation of models defined in a swagger.yaml.
- cerberus is used for userdefined validation of models.
- pyyaml is needed to parse yaml files.

Components
==========

The project is split in several mostly independent components.

Context
-------

A context parses input from the client and creates HTTP responses given
a response object, status and headers.
The input and response object are encoded and decoded according to the context.

Example:
          class ExampleResource(Resource):
              def post(self, request):
                  ctx = JSONContext(request)

                  return ctx.response(
                      body={'echo': ctx.data['user_message'],
                            status=HTTPStatus.CREATED,
                            headers={'some-header': 'example'}})

Problem
-------

Problems are objects representing some failure that causes the processing of the current
request to be canceled.
They are intended to be reported to the user given an HTTP error code, title and description.
When used with Resources, they can be thrown as exceptions.

Example:
          raise Problem.bad_request(detail="I don't like it.")

Resource
--------

A base class for RESTful resource implementations to be used as Django views.
Dispatching is handled based on the HTTP method of the request.
When handling a request, the instance-method named exactly like the lowercase version of
the HTTP method is called.
The response depends on the control flow of the specific handler.
If it returns normally, whatever value is returned from the handler is the response.
Otherwise the Resource tries to emit a meaningful error message.

- If a Problem was raised, it is returned as a response.
- If an ObjectDoesNotExist exception was raised, a Problem.not_found instance is returned.
- Otherwise the exception is wrapped in a Problem.internal_error

All Problems belonging to the 5XX-class of HTTP errors are logged to stdout.


Serializers
-----------

Serializers are used to translate objects from transport to internal representation and back.
Both representations can be chosen freely.

TODO

Validators
----------

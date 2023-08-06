
🐍λ✨ - lambda_decorators
=========================
|Version|_ |Docs|_ |Build|_

.. |Version| image:: https://img.shields.io/pypi/v/lambda-decorators.svg
.. _Version: https://pypi.python.org/pypi/lambda-decorators
.. |Docs| image:: http://readthedocs.org/projects/lambda-decorators/badge/?version=latest
.. _Docs: http://lambda-decorators.readthedocs.org/en/latest
.. |Build| image:: https://img.shields.io/travis/dschep/lambda-decorators/master.svg
.. _Build: https://travis-ci.org/dschep/lambda-decorators

A collection of useful decorators for making AWS Lambda handlers

*NOTE: this is in very early stages of development.*

``lambda_decorators`` is a collection of useful decorators for writing Python
handlers for `AWS Lambda <https://aws.amazon.com/lambda/>`_. They allow you to
avoid boiler plate for common things such as CORS headers, JSON serialization,
etc.

Quick example
-------------
.. code:: python

    # handler.py

    from lambda_decorators import cors_headers, json_http_resp, load_json_body

    @cors_headers
    @json_http_resp
    @load_json_body
    def handler(event, context):
        return {'hello': event['body']['name']}

When deployed to Lambda behind API Gateway and cURL'd:

.. code:: shell

   $ curl -d '{"name": "world"}' https://example.execute-api.us-east-1.amazonaws.com/dev/hello
   {"hello": "world"}

Install
-------
.. code:: shell

    pip install lambda-decorators


Writing your own
----------------
``lambda_decorators`` includes utilities to make building your own decorators
easier. The `before <http://lambda-decorators.rtfd.io#lambda_decorators.before>`_, `after <http://lambda-decorators.rtfd.io#lambda_decorators.after>`_, and `on_exception <http://lambda-decorators.rtfd.io#lambda_decorators.on_exception>`_ decorators
can be applied to your own functions to turn them into decorators for your
handlers. For example:


.. code:: python

    import logging
    from lambda_decorators import before

    @before
    def log_event(event, context):
        logging.debug(event)
        return event, context

    @log_event
    def handler(event, context):
        return {}

And if you want to make a decorator that provides two or more of
before/after/on_exception functionality, you can use
`LambdaDecorator <http://lambda-decorators.rtfd.io#lambda_decorators.LambdaDecorator>`_:

.. code:: python

    import logging
    from lambda_decorators import LambdaDecorator

    class log_everything(LambdaDecorator):
        def before(event, context):
            logging.debug(event, context)
            return event, context
        def after(retval):
            logging.debug(retval)
            return retval
        def on_exception(exception):
            logging.debug(exception)
            return {'statusCode': 500}

    @log_everything
    def handler(event, context):
        return {}


Why
---
Initially, I was inspired by `middy <https://github.com/middyjs/middy>`_ which
I've tried out in JavaScript and was happy with it. So naturally, I thought I'd
like to have something similar in Python too. But then as I thought about it
more, it seemed that when thinking of functions as the compute unit,
when using python, `decorators <https://wiki.python.org/moin/PythonDecorators>`_
pretty much are middleware! So instead of
building a middleware engine and a few middlewares, I just built a few
useful decorators and utilities to build them.

Included Decorators:
--------------------
* `async_handler <http://lambda-decorators.rtfd.io#lambda_decorators.async_handler>`_ - support for async handlers
* `cors_headers <http://lambda-decorators.rtfd.io#lambda_decorators.cors_headers>`_ - automatic injection of CORS headers
* `dump_json_body <http://lambda-decorators.rtfd.io#lambda_decorators.dump_json_body>`_ - auto-serialization of http body to JSON
* `json_http_resp <http://lambda-decorators.rtfd.io#lambda_decorators.json_http_resp>`_ - automatic serialization of python object to HTTP JSON response
* `load_json_body <http://lambda-decorators.rtfd.io#lambda_decorators.load_json_body>`_ - auto-deserialize of http body from JSON
* `no_retry_on_failure <http://lambda-decorators.rtfd.io#lambda_decorators.no_retry_on_failure>`_ - detect and stop retry attempts for scheduled lambdas

See each individual decorators for specific usage details and the example_
for some more use cases.

.. _example: https://github.com/dschep/lambda-decorators/tree/master/example

-----


`Full API Documentation <http://lambda-decorators.readthedocs.io/en/latest/>`_



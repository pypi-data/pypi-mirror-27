"""
This module provides base classes for services to expose functionality via APIs.
"""

import typing
from argparse import Namespace

import flask

from relevance.manager import ResourceNotFoundError
from relevance.settings import SettingsFactory


class Service(flask.Flask):
    """
    This class wraps the :class:`flask.Flask` application object and provides additional
    features to it, such as common error handling and response formatting.
    """
    _instances: typing.Dict[str, 'Service'] = {}

    def __init__(self, name: str, *args, **kwargs) -> None:
        """
        :param name: the name of the service.
        """
        self.svc_name = name
        self.data = Namespace()
        imp_name = 'relevance.{0}.service'.format(name)
        super().__init__(imp_name, *args, **kwargs)

        # Initialize settings
        loader = SettingsFactory(['/etc/relevance', './etc'])
        self.settings = loader.load(self.svc_name)

        self._register_default_handlers()

    def add_error_handler(self, ex, http_code=500, **payload) -> None:
        """
        Register a standard error handler in the service.

        :param ex: the Exception type or HTTP code to handle.
        :param http_code: the HTTP code to return.
        :param payload: an extra payload to attach to the message.
        """
        def handler(error):
            """
            Error handler function.
            """
            result = {
                'error': {
                    'type': error.__class__.__name__,
                    'resource': self.request.path,
                }
            }

            for key, value in payload.items():
                if hasattr(value, '__call__'):
                    result['error'][key] = value(error)
                else:
                    result['error'][key] = value

            return self.result(
                http_code if isinstance(error, Exception) else ex,
                result
            )

        self.errorhandler(ex)(handler)

    def _register_default_handlers(self) -> None:
        """
        Register the default request handlers for the service.
        """
        self.add_error_handler(
            405,
            desc='the requested method is not allowed for the specified resource',
            key=lambda x: self.request.method,
        )
        self.add_error_handler(
            404,
            type='PathNotFoundError',
            desc='cannot find the requested resource',
        )
        self.add_error_handler(
            ResourceNotFoundError, 404,
            desc='cannot find the requested resource',
            key=lambda x: str(x),  # pylint: disable=unnecessary-lambda
        )

    @classmethod
    def instance(cls, name: str, *args, **kwargs) -> 'Service':
        """
        Create or get an instance of a service.

        In some environments like multiprocessing, importing a global service object has
        not the intended effect. This method ensures that the instance that is retrieved
        is always the same across threads.

        If an instance `name` already exists, it will be returned. Otherwise, one will be
        created, stored and returned.

        :param name: the instance name.
        :return: a service object.
        """
        if name in cls._instances:
            return cls._instances[name]
        instance = cls(name, *args, **kwargs)
        cls._instances[name] = instance
        return instance

    @property
    def request(self) -> flask.request:
        """
        Get the current request.

        :return: the Flask request object.
        """
        return flask.request

    @staticmethod
    def result(status_code: int, content: object = None) -> flask.Response:
        """
        Obtain a response object.

        :param status_code: the status code to return.
        :param content: the content to return. If the content is a dictionary, a list
            or a tuple. It will be formatted to JSON. Otherwise, it will be returned as is.
        :return: a response object.
        """
        if content is None:
            response = flask.Response()
        elif isinstance(content, (dict, list, tuple)):
            response = flask.jsonify(content)
        else:
            response = flask.Response()
            response.content = content
        response.status_code = status_code
        return response

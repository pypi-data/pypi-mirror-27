"""
@file
@brief Creates and runs an Falcon application.
"""
import os
import sys
import logging
from pyquickhelper.cli.cli_helper import call_cli_function


def start_mlrestapi(name='dummy', host='127.0.0.1', port=8081, nostart=False, wsgi='waitress',
                    options='', fLOG=print):
    """
    Creates an :epkg:`falcon` application and
    runs it through a :epkg:`wsgi` server.

    :param name: class name or filename which defines the application
    :param host: host
    :param port: port
    :param nostart: do not start the wsgi server
    :param wsgi: wsgi framework which runs the falcon application
    :param options: additional options as a string (depends on the application)
    :param fLOG: logging function

    Only :epkg:`waitress` is implemented right now.
    Other option such as :epkg:`mod_wsgi` with :epkg:`Apache`.
    :epkg:`uwsgi` could be also be implemented.
    could be added in the future. The command line
    can be tested with a dummy application (``app_name='dummy'``).
    """
    try:
        from ..testing import dummy_application, dummy_application_image, dummy_application_fct, dummy_application_neighbors, dummy_application_neighbors_image
    except (ImportError, ValueError):
        folder = os.path.normpath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "..", ".."))
        sys.path.append(folder)
        from lightmlrestapi.testing import dummy_application, dummy_application_image, dummy_application_fct
        from lightmlrestapi.testing import dummy_application_neighbors, dummy_application_neighbors_image

    if name == "dummy":
        # Dummy application.
        app = dummy_application()

    elif name == "dummyfct":
        # Dummy application with a function.
        name = options
        if not os.path.exists(name):
            raise FileNotFoundError("Unable to find '{0}'.".format(name))
        path, loc = os.path.split(name)
        if path not in sys.path:
            sys.path.append(path)
            rem = True
        else:
            rem = False
        loc = os.path.splitext(loc)[0]
        try:
            mod = __import__(loc)
        except ImportError as e:
            if rem:
                sys.path.pop()
            with open(name, "r") as f:
                code = f.read()
            raise ImportError(
                "Unable to compile file '{0}'\n{1}".format(name, code)) from e
        if rem:
            sys.path.pop()
        if not hasattr(mod, 'restapi_predict'):
            with open(name, "r") as f:
                code = f.read()
            raise AttributeError(
                "Unable to find function 'restapi_predict' in file '{0}'\n{1}".format(name, code))
        app = dummy_application_fct(mod.restapi_predict)

    elif name == "dummyimg":
        # Dummy application with an image.
        app = dummy_application_image(options=options)

    elif name == "dummyknn":
        # Dummy application with neighbors.
        app = dummy_application_neighbors()

    elif name == "dummyknnimg":
        # Dummy application with neighbors and an image.
        app = dummy_application_neighbors_image(options=options)

    elif '.py' in name:
        raise NotImplementedError(
            "Unable to get application from filename '{}'. Not implemented.".format(name))

    else:
        raise NotImplementedError(
            "Application '{}' is not implemented.".format(name))

    if wsgi == 'waitress':
        from waitress import serve
        if not nostart:
            fLOG("[start_mlrestapi] serve(app, host='{}', port='{}')".format(host, port))
            logger = logging.getLogger('waitress')
            logger.setLevel(logging.INFO)
            serve(app, host=host, port=port)
        else:
            fLOG("[start_mlrestapi] do not run serve(app, host='{}', port='{}')".format(
                host, port))
    else:
        raise NotImplementedError(
            "Server '{}' is not implemented.".format(wsgi))

    return app


def _start_mlrestapi(fLOG=print, args=None):
    """
    Creates an falcon application and starts it through a wsgi application.

    @param      fLOG        logging function
    @param      args        to overwrite ``sys.args``

    .. cmdref::
        :title: Creates an falcon application and starts it through a wsgi application
        :cmd: start_mlrestapi=lightmlrestapi.cli.make_ml_app:_start_mlrestapi
        :lid: cmd_start_mlrestapi_cmd

        Creates an :epkg:`falcon` application and starts it through a :epkg:`wsgi` server.
    """
    epkg_dictionary = dict(falcon='https://falconframework.org/',
                           Apache='https://httpd.apache.org/',
                           mod_wsgi='https://modwsgi.readthedocs.io/en/develop/',
                           uwsgi='https://uwsgi-docs.readthedocs.io/en/latest/',
                           wsgi='https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface',
                           waitress='https://docs.pylonsproject.org/projects/waitress/en/latest/')
    call_cli_function(start_mlrestapi, args=args, fLOG=fLOG, skip_parameters=('fLOG',),
                      epkg_dictionary=epkg_dictionary)


if __name__ == "__main__":
    _start_mlrestapi()

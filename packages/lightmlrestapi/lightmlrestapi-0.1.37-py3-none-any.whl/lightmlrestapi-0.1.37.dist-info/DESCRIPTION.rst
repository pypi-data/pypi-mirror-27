
.. _l-README:

README
======

.. image:: https://travis-ci.org/sdpython/lightmlrestapi.svg?branch=master
    :target: https://travis-ci.org/sdpython/lightmlrestapi
    :alt: Build status

.. image:: https://ci.appveyor.com/api/projects/status/itkrtmperlhjm4xw?svg=true
    :target: https://ci.appveyor.com/project/sdpython/lightmlrestapi
    :alt: Build Status Windows

.. image:: https://circleci.com/gh/sdpython/lightmlrestapi/tree/master.svg?style=svg
    :target: https://circleci.com/gh/sdpython/lightmlrestapi/tree/master

.. image:: https://badge.fury.io/py/lightmlrestapi.svg
    :target: http://badge.fury.io/py/lightmlrestapi

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: http://opensource.org/licenses/MIT

.. image:: https://requires.io/github/sdpython/lightmlrestapi/requirements.svg?branch=master
     :target: https://requires.io/github/sdpython/lightmlrestapi/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://codecov.io/github/sdpython/lightmlrestapi/coverage.svg?branch=master
    :target: https://codecov.io/github/sdpython/lightmlrestapi?branch=master

.. image:: http://img.shields.io/github/issues/sdpython/lightmlrestapi.png
    :alt: GitHub Issues
    :target: https://github.com/sdpython/lightmlrestapi/issues

.. image:: https://badge.waffle.io/sdpython/lightmlrestapi.png?label=ready&title=Ready
    :alt: Waffle
    :target: https://waffle.io/sdpython/lightmlrestapi

.. image:: http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/_images/nbcov.png
    :target: http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/all_notebooks_coverage.html
    :alt: Notebook Coverage

**Links:**

* `GitHub/lightmlrestapi <https://github.com/sdpython/lightmlrestapi/>`_
* `documentation <http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/index.html>`_
* `Blog <http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/blog/main_0000.html#ap-main-0>`_

*lightmlrestapi* implements a light machine learning *REST API*
based on *falcon*. You can test a dummy *wsgi* server by running:

::

    start_mlrestapi --name=dummy

And then query it with:

::

    import requests
    import ujson
    features = ujson.dumps({'X': [0.1, 0.2]})
    r = requests.post('http://127.0.0.1:8081', data=features)
    print(r)
    print(r.json())

It should return:

::

    {'Y': [[0.4994216179, 0.4514893599, 0.0490890222]]}



Flask-XStatic-Files
===================

.. image:: https://travis-ci.org/agx/flask-xstatic-files.svg?branch=master
    :target: https://travis-ci.org/agx/flask-xstatic-files

.. highlight:: python

A `Flask`_ extionsion to serve `XStatic`_ files. Can be useful if you
don't use an asset pipeline and want to serve e.g. XStatic packaged
javascript files like `JQuery`_ directly.

Setup
-----
Upon initialization tell Flask about the XStatic modules you want to
use. This example uses JQuery and D3::

    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config.['XSTATIC_MODULES'] = ['jquery', 'd3']
    xsf = XStaticFiles(app)

The modules can be given as list or comma separated (``jquery,d3``).

Serving Files
-------------
The extension already installs a route handler for you so files under
``/xstatic/<module>/`` are served automatically. To generate these
URLs you can use ``url_for``::

  xsf.url_for('jquery', 'jquery.min.js')

In templates you can use ``xstatic_url_for``:

.. code-block:: html

    <script type=text/javascript src="{{ xstatic_url_for(module='jquery', path='jquery.min.js') }}"></script>

to generate these URLs.  This has the advantage that you can later
serve files from a static web server by adjusting ``XSTATIC_ROOT`` and
``XSTATIC_PROTO`` without having to modify any code.

In case you want to serve XStatic files from other URLs use ``serve``
or ``serve_or_404``::

  @app.route('/somewhere-else/jquery/jquery.min.js')
  def serve_jquery():
      return xsf.serve_or_404('jquery', 'jquery.min.js')

.. _Flask: http://flask.pocoo.org/
.. _XStatic: https://xstatic.readthedocs.io/en/latest/
.. _JQuery: https://pypi.python.org/pypi/XStatic-jQuery

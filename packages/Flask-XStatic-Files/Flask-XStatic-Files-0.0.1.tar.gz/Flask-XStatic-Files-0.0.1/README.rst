Flask-XStatic
=============

.. image:: https://travis-ci.org/agx/flask-xstatic-files.svg?branch=master
    :target: https://travis-ci.org/agx/flask-xstatic-files

A flask extionsion to serve xstatic files. Can be useful if you don't use an
asset pipeline and server e.g. xstatic packaged javascript files directly.

Setup
-----
Upon initialization tell flask about the xstatic modules you want to
use::

    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config.update(dict(
        XSTATIC_MODULES="jquery,d3",
    ))
    xsf = XStaticFiles(app)

Serving files
-------------
Install a minimal route handler::

    @app.route('/xstatic/<module>/<path:filename>')
    def xstatic(module, filename):
        return xsf.serve_or_404(module, filename)

In your templates you can then use xstatic_url_for::

    <script type=text/javascript src="{{ xstatic_url_for(module='jquery', path='jquery.min.js') }}"></script>

This has the advantage that you can later serve files from a static
web server by adjusting 'XSTATIC_ROOT' and 'XSTATIC_PROTO' without
having to modify any code.

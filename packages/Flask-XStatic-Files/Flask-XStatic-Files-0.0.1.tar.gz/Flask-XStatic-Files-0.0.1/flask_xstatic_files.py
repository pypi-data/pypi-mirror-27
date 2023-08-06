# vim: set fileencoding=utf-8 :
#
# (C) 2017 Guido Guenther <agx@sigxcpu.org>
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
Tiny flask extionsion to serve xstatic files
"""

import os
from flask import current_app, abort
from flask.helpers import send_file
import xstatic.main

# Find the stack on which we want to store the sqlalchemy session.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


try:
    FileNotFoundError
except NameError:
    # Python2
    FileNotFoundError = IOError


class XStaticFiles(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('XSTATIC_MODULES', None)
        app.config.setdefault('XSTATIC_ROOT', '/xstatic')
        app.config.setdefault('XSTATIC_PROTO', 'http')
        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

        self.app.jinja_env.globals['xstatic_url_for'] = self.url_for

    def _load(self):
        modules = current_app.config['XSTATIC_MODULES']
        if not modules:
            return {}
        modules = modules.split(',')
        pkg = __import__('xstatic.pkg', fromlist=modules)
        url = current_app.config['XSTATIC_ROOT']
        proto = current_app.config['XSTATIC_PROTO']
        xsf = {}
        for name in modules:
            mod = getattr(pkg, name)
            xs = xstatic.main.XStatic(mod, root_url=url, protocol=proto)
            xsf[xs.name] = xs
        return xsf

    def teardown(self, exception):
        pass

    @property
    def xsf(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'xsf'):
                ctx.xsf = self._load()
            return ctx.xsf

    def url_for(self, module, path):
        return self.xsf[module].url_for(path)

    def serve(self, module, path):
        return send_file(os.path.join(self.xsf[module].base_dir, path))

    def serve_or_404(self, module, path):
        try:
            return self.serve(module, path)
        except FileNotFoundError:
            abort(404)

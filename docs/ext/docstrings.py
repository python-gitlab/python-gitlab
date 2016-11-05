import itertools
import os

import jinja2
import six
import sphinx
import sphinx.ext.napoleon as napoleon
from sphinx.ext.napoleon.docstring import GoogleDocstring


def classref(value, short=True):
    tilde = '~' if short else ''
    return ':class:`%sgitlab.objects.%s`' % (tilde, value.__name__)


def setup(app):
    app.connect('autodoc-process-docstring', _process_docstring)
    app.connect('autodoc-skip-member', napoleon._skip_member)

    conf = napoleon.Config._config_values

    for name, (default, rebuild) in six.iteritems(conf):
        app.add_config_value(name, default, rebuild)
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}


def _process_docstring(app, what, name, obj, options, lines):
    result_lines = lines
    docstring = GitlabDocstring(result_lines, app.config, app, what, name, obj,
                                options)
    result_lines = docstring.lines()
    lines[:] = result_lines[:]


class GitlabDocstring(GoogleDocstring):
    _j2_env = None

    def _build_j2_env(self):
        if self._j2_env is None:
            self._j2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
                os.path.dirname(__file__)), trim_blocks=False)
            self._j2_env.filters['classref'] = classref

        return self._j2_env

    def _build_manager_doc(self):
        env = self._build_j2_env()
        template = env.get_template('manager_tmpl.j2')
        output = template.render(cls=self._obj.obj_cls)

        return output.split('\n')

    def _build_object_doc(self):
        env = self._build_j2_env()
        template = env.get_template('object_tmpl.j2')
        output = template.render(obj=self._obj)

        return output.split('\n')

    def __init__(self, *args, **kwargs):
        super(GitlabDocstring, self).__init__(*args, **kwargs)

        if hasattr(self._obj, 'obj_cls') and self._obj.obj_cls is not None:
            self._parsed_lines = self._build_manager_doc()
        elif hasattr(self._obj, 'canUpdate') and self._obj.canUpdate:
            self._parsed_lines = self._build_object_doc()

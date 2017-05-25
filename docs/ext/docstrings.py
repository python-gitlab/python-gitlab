import inspect
import itertools
import os

import jinja2
import six
import sphinx
import sphinx.ext.napoleon as napoleon
from sphinx.ext.napoleon.docstring import GoogleDocstring


def classref(value, short=True):
    if not inspect.isclass(value):
        return ':class:%s' % value
    tilde = '~' if short else ''
    string = '%s.%s' % (value.__module__, value.__name__)
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
    def _build_doc(self, tmpl, **kwargs):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(
            os.path.dirname(__file__)), trim_blocks=False)
        env.filters['classref'] = classref
        template = env.get_template(tmpl)
        output = template.render(**kwargs)

        return output.split('\n')

    def __init__(self, *args, **kwargs):
        super(GitlabDocstring, self).__init__(*args, **kwargs)

        if getattr(self._obj, '__name__', None) == 'Gitlab':
            mgrs = []
            gl = self._obj('http://dummy', private_token='dummy')
            for item in vars(gl).items():
                if hasattr(item[1], 'obj_cls'):
                    mgrs.append(item)
            self._parsed_lines.extend(self._build_doc('gl_tmpl.j2',
                                                      mgrs=sorted(mgrs)))
        elif hasattr(self._obj, 'obj_cls') and self._obj.obj_cls is not None:
            self._parsed_lines.extend(self._build_doc('manager_tmpl.j2',
                                                      cls=self._obj.obj_cls))
        elif hasattr(self._obj, 'canUpdate') and self._obj.canUpdate:
            self._parsed_lines.extend(self._build_doc('object_tmpl.j2',
                                                      obj=self._obj))

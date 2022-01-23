import inspect
import os

import jinja2
import sphinx
import sphinx.ext.napoleon as napoleon
from sphinx.ext.napoleon.docstring import GoogleDocstring


def classref(value, short=True):
    return value

    if not inspect.isclass(value):
        return f":class:{value}"
    tilde = "~" if short else ""
    return f":class:`{tilde}gitlab.objects.{value.__name__}`"


def setup(app):
    app.connect("autodoc-process-docstring", _process_docstring)
    app.connect("autodoc-skip-member", napoleon._skip_member)

    conf = napoleon.Config._config_values

    for name, (default, rebuild) in conf.items():
        app.add_config_value(name, default, rebuild)
    return {"version": sphinx.__display_version__, "parallel_read_safe": True}


def _process_docstring(app, what, name, obj, options, lines):
    result_lines = lines
    docstring = GitlabDocstring(result_lines, app.config, app, what, name, obj, options)
    result_lines = docstring.lines()
    lines[:] = result_lines[:]


class GitlabDocstring(GoogleDocstring):
    def _build_doc(self, tmpl, **kwargs):
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), trim_blocks=False
        )
        env.filters["classref"] = classref
        template = env.get_template(tmpl)
        output = template.render(**kwargs)

        return output.split("\n")

    def __init__(
        self, docstring, config=None, app=None, what="", name="", obj=None, options=None
    ):
        super().__init__(docstring, config, app, what, name, obj, options)

        if name.startswith("gitlab.v4.objects") and name.endswith("Manager"):
            self._parsed_lines.extend(self._build_doc("manager_tmpl.j2", cls=self._obj))

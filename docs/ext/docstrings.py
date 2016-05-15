import itertools
import os

import jinja2
import six
import sphinx
import sphinx.ext.napoleon as napoleon
from sphinx.ext.napoleon.docstring import GoogleDocstring


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
    def _build_doc(self):
        cls = self._obj.obj_cls
        opt_get_list = cls.optionalGetAttrs
        opt_list_list = cls.optionalListAttrs
        md_create_list = list(itertools.chain(cls.requiredUrlAttrs,
                                              cls.requiredCreateAttrs))
        opt_create_list = cls.optionalCreateAttrs

        opt_get_keys = "None"
        if opt_get_list:
            opt_get_keys = ", ".join(['``%s``' % i for i in opt_get_list])

        opt_list_keys = "None"
        if opt_list_list:
            opt_list_keys = ", ".join(['``%s``' % i for i in opt_list_list])

        md_create_keys = opt_create_keys = "None"
        if md_create_list:
            md_create_keys = ", ".join(['``%s``' % i for i in md_create_list])
        if opt_create_list:
            opt_create_keys = ", ".join(['``%s``' % i for i in
                                         opt_create_list])

        md_update_list = list(itertools.chain(cls.requiredUrlAttrs,
                                              cls.requiredUpdateAttrs))
        opt_update_list = cls.optionalUpdateAttrs

        md_update_keys = opt_update_keys = "None"
        if md_update_list:
            md_update_keys = ", ".join(['``%s``' % i for i in md_update_list])
        if opt_update_list:
            opt_update_keys = ", ".join(['``%s``' % i for i in
                                         opt_update_list])

        tmpl_file = os.path.join(os.path.dirname(__file__), 'template.j2')
        with open(tmpl_file) as fd:
            template = jinja2.Template(fd.read(), trim_blocks=False)
            output = template.render(filename=tmpl_file,
                                     cls=cls,
                                     md_create_keys=md_create_keys,
                                     opt_create_keys=opt_create_keys,
                                     md_update_keys=md_update_keys,
                                     opt_update_keys=opt_update_keys,
                                     opt_get_keys=opt_get_keys,
                                     opt_list_keys=opt_list_keys)

        return output.split('\n')

    def __init__(self, *args, **kwargs):
        super(GitlabDocstring, self).__init__(*args, **kwargs)

        if not hasattr(self._obj, 'obj_cls') or self._obj.obj_cls is None:
            return

        self._parsed_lines = self._build_doc()

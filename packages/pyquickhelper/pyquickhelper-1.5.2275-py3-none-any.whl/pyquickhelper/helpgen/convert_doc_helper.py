"""
@file
@brief Helpers to convert docstring to various format

.. versionadded:: 1.0
"""
# -- HELP BEGIN EXCLUDE --

from .utils_sphinx_doc import private_migrating_doxygen_doc

# -- HELP END EXCLUDE --

from .utils_sphinx_doc import migrating_doxygen_doc
from ..texthelper.texts_language import TITLES
from ..loghelper.flog import noLOG
from . helpgen_exceptions import HelpGenConvertError
from .conf_path_tools import find_graphviz_dot, find_latex_path
from .mock_app_sphinx import MockSphinxApp

import sys
import re
import textwrap
import os
import warnings
from docutils import core, languages
from docutils.io import StringInput, StringOutput
from sphinx.environment import BuildEnvironment, default_settings
from sphinx import __display_version__ as sphinx__display_version__
from sphinx.ext.mathjax import html_visit_displaymath


try:
    from sphinx.util.docutils import is_html5_writer_available
except ImportError:
    # Available only after Sphinx >= 1.6.1.
    def is_html5_writer_available():
        return False

if sys.version_info[0] == 2:
    from StringIO import StringIO
else:
    from io import StringIO


def default_sphinx_options(fLOG=noLOG, **options):
    """
    Define or override default options for Sphinx, listed below.

    .. runpython::

        from pyquickhelper.helpgen.convert_doc_helper import default_sphinx_options
        options = default_sphinx_options()
        for k, v in sorted(options.items()):
            print("{0} = {1}".format(k, v))

    .. versionadded:: 1.4
    """
    res = {'output_encoding': options.get('output_encoding', 'unicode'),
           'doctitle_xform': options.get('doctitle_xform', True),
           'initial_header_level': options.get('initial_header_level', 2),
           'input_encoding': options.get('input_encoding', 'utf8'),
           'blog_background': options.get('blog_background', False),
           'sharepost': options.get('sharepost', None),
           'todoext_link_only': options.get('todoext_link_only', False),
           'mathdef_link_only': options.get('mathdef_link_only', True),
           'blocref_link_only': options.get('blocref_link_only', False),
           'faqref_link_only': options.get('faqref_link_only', False),
           'nbref_link_only': options.get('nbref_link_only', False),
           'todo_link_only': options.get('todo_link_only', False),
           'language': options.get('language', 'en'),
           'outdir': options.get('outdir', '.'),
           'imagedir': options.get('imagedir', '.'),
           'confdir': options.get('confdir', '.'),
           'doctreedir': options.get('doctreedir', '.'),
           'math_number_all': options.get('math_number_all', False),
           # graphviz
           'graphviz_output_format': options.get('graphviz_output_format', 'png'),
           'graphviz_dot': options.get('graphviz_dot', find_graphviz_dot(exc=False)),
           # latex
           'imgmath_image_format': options.get('imgmath_image_format', 'png'),
           # containers
           'todo_include_todos': [],
           'out_blogpostlist': [],
           'out_runpythonlist': [],
           'todoext_include_todosext': [],
           'mathdef_include_mathsext': [],
           'blocref_include_blocrefs': [],
           'faqref_include_faqrefs': [],
           'exref_include_exrefs': [],
           'nbref_include_nbrefs': [],
           'warning_stream': StringIO(),
           }

    if res['imgmath_image_format'] == 'png':
        res['imgmath_latex'] = options.get(
            'imgmath_latex', find_latex_path(exc=False))
        res['imgmath_dvipng'] = options.get(
            'imgmath_dvipng', os.path.join(res['imgmath_latex'], "dvipng.exe") if res['imgmath_latex'] is not None else None)
        if res['imgmath_dvipng'] is not None and not os.path.exists(res['imgmath_dvipng']):
            fLOG("[warning], unable to find: " + str(res['imgmath_dvipng']))
            # we pass as latex is not necessarily installed or needed
        env_path = os.environ.get("PATH", "")
        if res['imgmath_latex'] is not None and res['imgmath_latex'] not in env_path:
            if len(env_path) > 0:
                env_path += ";"
            env_path += res['imgmath_latex']

        if res['imgmath_latex'] is not None:
            if sys.platform.startswith("win"):
                res['imgmath_latex'] = os.path.join(
                    res['imgmath_latex'], "latex.exe")
            else:
                res['imgmath_latex'] = os.path.join(
                    res['imgmath_latex'], "latex")

    for k, v in options.items():
        if k not in res:
            res[k] = v

    return res


def rst2html(s, fLOG=noLOG, writer="sphinx", keep_warnings=False,
             directives=None, language="en", warnings_log=False,
             **options):
    """
    converts a string into HTML format

    @param      s               string to converts
    @param      fLOG            logging function (warnings will be logged)
    @param      writer          *None* or an instance such as ``HTMLWriterWithCustomDirectives()`` or
                                ``custom`` or ``sphinx``
    @param      keep_warnings   keep_warnings in the final HTML
    @param      directives      new directives to add (see below)
    @param      language        language
    @param      options         Sphinx options see `Render math as images <http://www.sphinx-doc.org/en/stable/ext/math.html#module-sphinx.ext.imgmath>`_,
                                a subset of options is used, see @see fn default_sphinx_options
    @param      warnings_log    send warnings to log (True) or to the warning stream(False)
    @return                     HTML format

    *directives* is None or a list of 5-uple:

    * a directive name
    * a directive class: see `Sphinx Directive <http://sphinx-doc.org/extdev/tutorial.html>`_, see also @see cl RunPythonDirective as an example
    * a docutils node: see @see cl runpython_node as an example
    * two functions: see @see fn visit_runpython_node, @see fn depart_runpython_node as an example

    .. exref::
        :title: How to test a Sphinx directive?

        The following code defines a simple directive defined based on an existing one.
        It also defined what to do if a new node is inserted in the documentation.

        ::

            from docutils import nodes
            from pyquickhelper.helpgen import rst2html

            class runpythonthis_node(nodes.Structural, nodes.Element):
                pass

            class RunPythonThisDirective (RunPythonDirective):
                runpython_class = runpythonthis_node

            def visit_node(self, node):
                self.body.append("<p><b>visit_node</b></p>")
            def depart_node(self, node):
                self.body.append("<p><b>depart_node</b></p>")

            content = '''
                        test a directive
                        ================

                        .. runpythonthis::

                            print("this code shoud appear" + "___")
                        '''.replace("                    ", "")
                        # to remove spaces at the beginning of the line

            tives = [ ("runpythonthis", RunPythonThisDirective,
                    runpythonthis_node,
                    visit_node, depart_node) ]

            html = rst2html(content, fLOG=fLOG,
                            writer="custom", keep_warnings=True,
                            directives=tives)

        Unfortunately, this functionality is only tested on Python 3.
        It might only work on Python 2.7.
        The function produces files if the document contains latex
        converted into image.

   .. faqref::
       :title: How to get more about latex errors?
       :index: latex

        Sphinx is not easy to use when it comes to debug latex expressions.
        I did not find an easy way to read the error returned by latex about
        a missing bracket or an unknown command. I fianlly added a short piece
        of code in ``sphinx.ext.imgmath.py`` just after the call to
        the executable indicated by *imgmath_latex*

        ::

            if b'...' in stdout or b'LaTeX Error' in stdout:
                print(self.builder.config.imgmath_latex_preamble)
                print(p.returncode)
                print("################")
                print(latex)
                print("..........")
                print(stdout.decode("ascii").replace("\r", ""))
                print("-----")
                print(stderr)

        It displays the output if an error happened.

    .. faqref::
        :title: How to hide command line window while compiling latex?
        :lid: command line window

        Sphinx calls latex through command line. On Windows, a command line window
        can annoyingly show up anytime a formula is compile. The following
        line can be added to hide it:

        ::

            startupinfo = STARTUPINFO()
            startupinfo.dwFlags |= STARTF_USESHOWWINDOW

        And ``, startupinfo=startupinfo`` must be added to lines ``p = Popen(...``.

    .. versionadded:: 1.0

    .. versionchanged:: 1.3
        Parameters *writer*, *keep_warnings* were added to specifiy a custom writer
        and to keep the warnings. By default, the function now interprets *Sphinx*
        directives and not only *docutils* ones.
        Parameter *directives* was added to add a directive before parsing the RST.

    .. versionchanged:: 1.4
        Add directives *todoext*, *todo*, *mathdef*, *blocref*, *faqref*,*nbref*, *exref*,
        parameter *language* was added.
        Add directives *graphviz*, *math*.
        Parse more extensive Sphinx syntax.
    """
    _nbeq = [0, None]

    def custom_html_visit_displaymath(self, node):
        if not hasattr(node, "number"):
            node["number"] = None
        try:
            return html_visit_displaymath(self, node)
        except AttributeError as e:
            if "math_number_all" in str(e) and sys.version_info[:2] <= (2, 7):
                # Python 2.7 produces the following error:
                # AttributeError: No such config value: math_number_all
                # we skip
                return []
            else:
                raise e

    if writer in ["custom", "sphinx"]:
        mockapp, writer, title_names = MockSphinxApp.create(
            "sphinx", directives)
        writer_name = "pseudoxml"
    else:
        raise NotImplementedError()

    if writer is None and directives is not None and len(directives) > 0:
        raise NotImplementedError(
            "the writer must not be null if custom directives will be added, check the documentation of the fucntion")

    settings_overrides = default_settings.copy()
    settings_overrides.update({k: v[0]
                               for k, v in mockapp.new_options.items()})

    # next
    defopt = default_sphinx_options(**options)
    settings_overrides.update(defopt)
    warning_stringio = defopt["warning_stream"]
    _nbeq[1] = warning_stringio

    config = mockapp.config
    if sphinx__display_version__ >= "1.6":
        config.init_values()
    else:
        config.init_values(fLOG)
    config.blog_background = False
    config.sharepost = None

    writer.add_configuration_options(mockapp.new_options)
    for k in {'outdir', 'imagedir', 'confdir', 'doctreedir'}:
        setattr(writer.builder, k, settings_overrides[k])

    if sphinx__display_version__ >= "1.6":
        env = BuildEnvironment(mockapp)
    else:
        env = BuildEnvironment(None, None, config=config)
    env.temp_data["docname"] = "string"
    mockapp.builder.env.temp_data["docname"] = "string"
    settings_overrides["env"] = env

    lang = languages.get_language(language)
    for name in title_names:
        if name not in lang.labels:
            lang.labels[name] = TITLES[language][name]

    for k, v in sorted(settings_overrides.items()):
        fLOG("[rst2html] {0}={1}{2}".format(
            k, v, " --- added" if hasattr(config, k) else ""))
    for k, v in sorted(settings_overrides.items()):
        if hasattr(writer.builder.config, k) and writer.builder.config[k] != v:
            writer.builder.config[k] = v

    # something is screwing with sphinx or docutils, it is due to
    # direct call to nbconvert or sphinx
    # raise an exception for unknown role pending_xref
    output, pub = core.publish_programmatically(source=s, source_path=None, destination_path=None, writer=writer,
                                                writer_name=writer_name, settings_overrides=settings_overrides,
                                                source_class=StringInput, destination_class=StringOutput,
                                                destination=None, reader=None, reader_name='standalone',
                                                parser=None, parser_name='restructuredtext', settings=None,
                                                settings_spec=None, config_section=None, enable_exit_status=False)

    doctree = pub.document
    mockapp.emit('doctree-read', doctree)
    parts = pub.writer.parts

    warnval = settings_overrides["warning_stream"].getvalue()
    if warnval is not None and len(warnval) > 0:
        if warnings_log:
            fLOG(warnval)
        else:
            warnings.warn(warnval)

    if not keep_warnings:
        exp = re.sub(
            '(<div class="system-message">(.|\\n)*?</div>)', "", parts["whole"])
    else:
        exp = parts["whole"]

    return exp


def correct_indentation(text):
    """
    tries to improve the indentation before running docutil

    @param      text        text to correct
    @return                 corrected text

    .. versionadded:: 1.0
    """
    title = {}
    rows = text.split("\n")
    for row in rows:
        row = row.replace("\t", "    ")
        cr = row.lstrip()
        ind = len(row) - len(cr)

        tit = cr.strip("\r\n\t ")
        if len(tit) > 0 and tit[0] in "-+=*^" and tit == tit[0] * len(tit):
            title[ind] = title.get(ind, 0) + 1

    if len(title) > 0:
        mint = min(title.keys())
    else:
        mint = 0
    if mint > 0:
        newrows = []
        for row in rows:
            i = 0
            while i < len(row) and row[i] == ' ':
                i += 1

            rem = min(i, mint)
            if rem > 0:
                newrows.append(row[rem:])
            else:
                newrows.append(row)

        return "\n".join(newrows)
    else:
        return text


def docstring2html(function_or_string, format="html", fLOG=noLOG, writer="sphinx"):
    """
    converts a docstring into a HTML format

    @param      function_or_string      function, class, method or doctring
    @param      format                  output format
    @param      fLOG                    logging function
    @param      writer                  *None* or an instance such as ``HTMLWriterWithCustomDirectives()``
    @return                             (str) HTML format or (IPython.core.display.HTML)

    .. exref::
        :title: Produce HTML documentation for a function or class

        The following code can display the dosstring in HTML format
        to display it in a notebook.

        @code
        from pyquickhelper.helpgen import docstring2html
        import sklearn.linear_model
        docstring2html(sklearn.linear_model.LogisticRegression)
        @endcode

    The output format is defined by:

        * html: IPython HTML object
        * rawhtml: HTML as text + style
        * rst: rst
        * text: raw text

    .. versionadded:: 1.0

    .. versionchanged:: 1.3
        Parameter *writer* was added to specifiy a custom writer.

    .. versionchanged:: 1.4
        Does not crash anymore when the documentation is None.
    """
    if not isinstance(function_or_string, str):
        doc = function_or_string.__doc__
    else:
        doc = function_or_string

    if format == "text":
        return doc

    if doc is None:
        return ""

    stats, javadoc = migrating_doxygen_doc(doc, "None", log=False)
    rows = javadoc.split("\n")
    rst = private_migrating_doxygen_doc(
        rows, index_first_line=0, filename="None")
    rst = "\n".join(rst)
    ded = textwrap.dedent(rst)

    if format == "rst":
        return ded

    try:
        html = rst2html(ded, fLOG=fLOG, writer=writer)
    except Exception:
        # we check the indentation
        ded = correct_indentation(ded)
        try:
            html = rst2html(ded, fLOG=fLOG, writer=writer)
        except Exception as e:
            lines = ded.split("\n")
            lines = ["%04d  %s" % (i + 1, _.strip("\n\r"))
                     for i, _ in enumerate(lines)]
            raise HelpGenConvertError(
                "unable to process:\n{0}".format("\n".join(lines))) from e

    if format == "html":
        from IPython.core.display import HTML
        return HTML(html)
    elif format == "rawhtml":
        return html
    else:
        raise ValueError(
            "unexected format: " + format + ", should be html, rawhtml, text, rst")


.. _l-sphinxextc:

Sphinx Extensions
=================

I use this module to automate most of the process
which compiles and publishes the material for my teachings.
One part of that is a series of
:epkg:`sphinx` extensions. A couple assume
that the module they are documenting follows the same
design as this one, the others are design free. The whole list
is available at
:ref:`List of Sphinx commands added by pyquickhelper <f-sphinxext-pyq>`.

.. contents::
    :local:

Simple extensions
-----------------

:epkg:`Sphinx` implements many
`markups <http://www.sphinx-doc.org/en/stable/markup/index.html#sphinxmarkup>`_.
This module adds a couple of them. Many cheat sheets
(see `cheat sheet 1 <https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`_,
`cheat sheet 2 <http://docs.sphinxdocs.com/en/latest/cheatsheet.html>`_,
`Sphinx Memo <http://rest-sphinx-memo.readthedocs.io/en/latest/ReST.html>`_)
can be found on internet.
Most if the time, this extension need a change in the
configuration file *conf.py* before using them to document.

*autosignature*: display the signature of a class or function
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Location: :class:`docassert setup <pyquickhelper.sphinxext.sphinx_autosignature.AutoSignatureDirective>`.

In *conf.py*:

::

    extensions = [ ...
        'pyquickhelper.sphinxext.sphinx_autosignature']

Sometimes you need to show the signature of a function twice in
your documentation. However, the instruction ``.. autofunction::``
can be added only otherwise it produces two entries in the index
with the same id. Assuming, you have used ``.. autofunction::`` somewhere,
you can recall the signture of a function or a class
by using ``.. autosignature::``. It will automatically add a link
to the text added by ``.. autofunction::`` or ``.. autoclass::``.

.. sidebar:: autosignature

    ::

        .. autosignature:: pyquickhelper.sphinxext.sphinx_autosignature.AutoSignatureDirective
            :nomembers:

.. autosignature:: pyquickhelper.sphinxext.sphinx_autosignature.AutoSignatureDirective

*bigger*: bigger size
+++++++++++++++++++++

In *conf.py*:

::

    extensions = [ ...
        'pyquickhelper.sphinxext.sphinx_bigger_extension']

This extension just changes the size of a text if the output is HTML.

.. sidebar:: bigger

    ::

        * :bigger:`default size`
        * :bigger:`::1:size 1`
        * :bigger:`::5:size 5`
        * :bigger:`::10:size 10`

* :bigger:`default size`
* :bigger:`::1:size 1`
* :bigger:`::5:size 5`
* :bigger:`::10:size 10`

*docassert*: check list of documented parameters
++++++++++++++++++++++++++++++++++++++++++++++++

Location: :func:`docassert setup <pyquickhelper.sphinxext.sphinx_docassert_extension.setup>`.

This extension does nothing but generating warnings if a function or a class
documents a misspelled parameter (not in the signature) or if one
parameter is missing from the documentation.

In *conf.py*:

::

    extensions = [ ...
        'pyquickhelper.sphinxext.sphinx_docassert_extension']

Sphinx outputs some warnings:

::

    WARNING: [docassert] '_init' has undocumented parameters 'translator_class' (in 'pyquickhelper\_doc\sphinxdoc\source\pyquickhelper\helpgen\sphinxm_convert_doc_sphinx_helper.py').

.. _l-sphinx-epkg:

*epkg*: cache references
++++++++++++++++++++++++

Location: :func:`epkg_role <pyquickhelper.sphinxext.sphinxext_epkg_extension.epkg_role>`.

In *conf.py*:

::

    extensions = [ ...
        'pyquickhelper.sphinxext.sphinx_epkg_extension']

    epkg_dictionary = {
        'pandoc': 'http://johnmacfarlane.net/pandoc/',                                       # 1
        'pandas': ('http://pandas.pydata.org/pandas-docs/stable/',                           # 2
            ('http://pandas.pydata.org/pandas-docs/stable/generated/pandas.{0}.html', 1)),   # 3
        }

The variable ``epkg_dictionary`` stores the list of url to display. It can be a simple
string or a list of possibililies with multiple parameters. The three options above can
used like this. The last one allows one parameter separated by ``:``.

.. sidebar:: epkg

    ::

        * Option 1: :epkg:`pandoc`
        * Option 2: :epkg:`pandas`,
        * Option 3: :epkg:`pandas:DataFrame`

* Option 1: :epkg:`pandoc`
* Option 2: :epkg:`pandas`,
* Option 3: :epkg:`pandas:DataFrame`

The last link is broken before the current file is not python
file but a *rst*. The file extension must be specified.
For some websites, url and functions do not follow the same rule.
A function must be used in this case to handle the mapping.

::

    def weird_mapping(input):
        # The function receives whatever is between `...`.
        ...
        return anchor, url

This function must be placed at the end or be the only available option.

::

    epkg_dictionary = { 'weird_site': weird_mapping }

However, because it is impossible to use a function as a value
in the configuration because :epkg:`*py:pickle` does not handle
this scenario (see `PicklingError on environment when config option value is a callable <https://github.com/sphinx-doc/sphinx/issues/1424>`_),
``my_custom_links`` needs to be replaced by:
``("module_where_it_is_defined.my_custom_links", None)``.
The role *epkg* will import it based on its name.

.. _l-runpython-tutorial:

*runpython*: execute a script
+++++++++++++++++++++++++++++

Location: :class:`RunPythonDirective <pyquickhelper.sphinxext.sphinxext_runpython_extension.RunPythonDirective>`.

In *conf.py*:

::

    extensions = [ ...
        'pyquickhelper.sphinxext.sphinxext_runpython_extension']

Documentation means many examples which needs to be updated when a change
happen unless the documentation runs the example itself and update its output.
That's what this directive does. It adds as raw text whatever comes out
throught the standard output.

.. sidebar:: runpython

    ::

        .. runpython::
            :showcode:

            import os
            for i, name in enumerate(os.listdir(".")):
                print(i, name)

.. runpython::
    :showcode:

    import os
    for i, name in enumerate(os.listdir(".")):
        print(i, name)

The output can also be compiled as RST format and the code can be hidden.
It is useful if the documentation is a copy/paste of some external process
or function. This function can be directly called from the documentation.
The output must be converted into RST format. It is then added to the
documentation. It is quite useful to display the version of some installed
modules.

.. sidebar:: runpython and rst

    ::

        .. runpython::
            :rst:

            import pandas, numpy, sphinx

            for i, mod in [sphinx, pandas, numpy]:
                print("* version of *{0}*: *{1}*".format(
                    getattr(mod, "__name__"), getattr(mod, "__version__"))

.. runpython::
    :rst:

    import os
    for i, name in enumerate(os.listdir(".")):
        print("* file **{0}**: *{1}*".format(i, name))

If the code throws an exception (except a syntax error),
it can be caught by adding the option ``:exception:``.
The directive displays the traceback.

.. runpython::
    :showcode:
    :exception:

    import os
    for i, name in enumerate(os.listdir("not existing")):
        pass

*sharenet*: add link to share
+++++++++++++++++++++++++++++

Location: :func:`sharenet_role <pyquickhelper.sphinxext.sphinxext_sharenet_extension.sharenet_role>`.

In *conf.py*:

::

    extensions = [ ...
        'pyquickhelper.sphinxext.sphinx_sharenet_extension']

The role or :class:`directive <pyquickhelper.sphinxext.sphinx_sharenet_extension.ShareNetDirective>`
adds button to easily share the page on Facebook, Linkedin or Twitter.

.. sharenet::
    :facebook: 1
    :linkedin: 2
    :twitter: 3
    :head: False

.. sidebar:: sharenet

    ::

        .. sharenet::
            :facebook: 1
            :linkedin: 2
            :twitter: 3
            :head: False

The integer indicates the order in which they need to be displayed.
It is optional. The option ``:head: False`` specifies the javascript
part is added to the html body and not the header.
The header can be overwritten by other custom commands.

*postcontents*: dynamic contents
++++++++++++++++++++++++++++++++

Location: :class:`PostContentsDirective <pyquickhelper.sphinxext.sphinxext_postcontents_extension.PostContentsDirective>`.

In *conf.py*:

::

    extensions = [ ...
        'pyquickhelper.sphinxext.sphinx_postcontents_extension']

The directive ``.. contents::`` display a short table of contents with what Sphinx
knows when entering the page. It will not include any title an instruction could dynamically
add to the page. Typically:

::

    .. runpython::
        :rst:

        print("Dynamic title")
        print("+++++++++++++")

This title added by the instruction :ref:`l-runpython-tutorial` is not
considered by ``.. contents::``. The main reason is the direction resolves
titles when entering the page and not after the *doctree* was modified.
The directive ``.. postcontents::`` inserts a placeholder in the *doctree*.
It is filled by function
:func:`transform_postcontents <pyquickhelper.sphinxext.sphinxext_postcontents_extension.transform_postcontents>`
before the final page is created (event ``'doctree-resolved'``).
It looks into the page and adds a link to each local sections.

Bloc extensions
---------------

They pretty much follows the same design. They highlight a paragraph
and this paragraph can be recalled anywhere on another page. Some options
differs depending on the content.

Example: faqref
+++++++++++++++

Location: :class:`FaqRef <pyquickhelper.sphinxext.sphinx_faqref_extension.FaqRef>`.

In *conf.py*:

::

    extensions = [ ...
        'pyquickhelper.sphinxext.sphinx_faqref_extension']

    faqref_include_faqrefs = True

This extension adds a *todo*:

.. sidebar:: faqref

    ::

        .. faqref::
            :title: How to add a FAQ?
            :tag: faqexample
            :lid: this-faq-example

            Description of the issue.

.. faqref::
    :title: How to add a FAQ?
    :tag: faqexample

    Description of the issue.

The tag is important when recalling all of these. You can also an internal
reference to :ref:`it <this-faq-example>` with option ``:lid:``.
Option `:contents:` add a list of all nodes @see cl faqref_node
included in the list.

.. sidebar:: faqreflist

    ::

        .. faqreflist::
            :tag: faqexample
            :contents:

.. faqreflist::
    :tag: faqexample
    :contents:

List of bloc extensions
+++++++++++++++++++++++

* :class:`blocref <pyquickhelper.sphinxext.sphinx_blocref_extension.BlocRef>`:
  to add a definition (or any kind of definition)
* :class:`cmdref <pyquickhelper.sphinxext.sphinx_cmdref_extension.CmdRef>`:
  to documentation a script the module makes available on the command line
* :class:`exref <pyquickhelper.sphinxext.sphinx_exref_extension.ExRef>`:
  to add an example
* :class:`faqref <pyquickhelper.sphinxext.sphinx_faqref_extension.FaqRef>`:
  to add a FAQ
* :class:`mathdef <pyquickhelper.sphinxext.sphinx_mathdef_extension.MathDef>`:
  to add a mathematical definition (or any kind of definition)
* :class:`nbref <pyquickhelper.sphinxext.sphinx_nbref_extension.NbRef>`:
  to add a magic command
* :class:`todoext <pyquickhelper.sphinxext.sphinx_todoext_extension.TodoExt>`:
  to add an issue or a work item

If same design as pyquickhelper
-------------------------------

*pyquickhelper* was created to automate the creation of the documentation
for a python module. It does what this extension
`sphinx-automodapi <http://sphinx-automodapi.readthedocs.io/en/latest/>`_
does and a little bit more:

* It automatically converts notebooks into RST, HTML, and slides.
  The RST format is included in the documentation and links to the other
  format are added.
* It automatically creates a
  :ref:`notebook gallery <l-notebooks>` and an
  :ref:`example gallery <examples-gallery>`.
* It creates a RST pages for each source file in subfoldeer ``src``.
* It converts `javadoc <https://fr.wikipedia.org/wiki/Javadoc>`_
  style into Sphinx style.
* It handles a :ref:`blog <ap-main-0>`.

This design is described by an empty module:

* `documentation <http://www.xavierdupre.fr/app/python3_module_template/helpsphinx2/index.html>`_
* `github/python3_module_template <https://github.com/sdpython/python3_module_template/>`_

Blog Post
+++++++++

I added this extension to write some news connected to the module
but probably not true anymore in a couple of years. Blog post can added as a file
following the template
``_doc/sphinxdoc/source/blog/<year>/YYYY-MM-DD_anything.rst``.

::

    .. blogpost::
        :title: The title of the post
        :keywords: documentation, startup
        :date: 2017-05-21
        :categories: documentation
        :lid: id-for-reference

        Content of the post.

*githublink*: link to source in github
++++++++++++++++++++++++++++++++++++++

Location: :func:`githublink_role <pyquickhelper.sphinxext.sphinx_githublink_extension.githublink_role>`.

In *conf.py*:

::

    extensions = [ ...
        'pyquickhelper.sphinxext.sphinx_githublink_extension']

It only works if the project is hosted on GitHub.
The role insert a link on the corresponding file with the corresponding line in GitHub
wherever it is inserted.

In *conf.py*:

::

    githublink_options = {
        'anchor': "source on GitHub",
        'user': 'sdpython'
    }

In the documentation:

.. sidebar:: githublink

    ::

        * :githublink:`%|rst-doc`
        * :githublink:`link on the same file on GitHub|rst-doc`
        * :githublink:`%|rst-doc|5`
        * :githublink:`%|py-doc`

* :githublink:`%|rst-doc`
* :githublink:`link on the same file on GitHub|rst-doc`
* :githublink:`%|rst-doc|5`
* :githublink:`%|py-doc`

The suffix ``-doc`` tells the source file is part of the subfolder
``_doc/sphinx/source`` and not ``src``. It is not needed in this case.

Parameters
++++++++++

Finally, I tried different styles to document a function.
Most of them produce the same output. That's the purpose
of the module: :ref:`f-fakefunctiontodocumentation`.

Different styles:

:func:`f1 <pyquickhelper.helpgen._fake_function_to_documentation.f1>`:

::

    def f1(a, b):
       """
        Addition 1

        @param      a       parameter a
        @param      b       parameter b
        @return             ``a+b``
        """
        return a + b

:func:`f2 <pyquickhelper.helpgen._fake_function_to_documentation.f2>`:

::

    def f2(a, b):
        """Addition 2
        @param      a       parameter a
        @param      b       parameter b
        @return             ``a+b``"""
        return a + b

:func:`f3 <pyquickhelper.helpgen._fake_function_to_documentation.f3>`:

::

    def f3(a, b):
        """
        Addition 3

        :param a: parameter a
        :param b: parameter a
        :returns: ``a+b``
        """
        return a + b

:func:`f4 <pyquickhelper.helpgen._fake_function_to_documentation.f4>`:

::

    def f4(a, b):
        """Addition 4
        :param a: parameter a
        :param b: parameter a
        :returns: ``a+b``"""
        return a + b

:func:`f5 <pyquickhelper.helpgen._fake_function_to_documentation.f5>`:

::

    def f5(a, b):
        """
        Addition 5

        Parameters
        ----------

        a: parameter a

        b: parameter b

        Returns
        -------
        ``a+b``
        """
        return a + b

:func:`f6 <pyquickhelper.helpgen._fake_function_to_documentation.f6>`:

::

    def f6(a, b):
        """
        Addition 6

        Args:
            a: parameter a
            b: parameter b

        Returns:
            ``a+b``
        """

For developpers: unit test an extension
---------------------------------------

I did not find any easy solution to test a Sphinx extension I create.
The main idea consists in mocking Sphinx. It works to some extend.
Sphinx is also quite difficult to run in memory. Every thing is design
to use files. I finally decided to spend some time on Sphinx
to be able to run it to convert a RST into HTML and RST.
That's the purpose of the next function:

.. autosignature:: pyquickhelper.helpgen.sphinxm_convert_doc_helper.rst2html

The HTML conversion is quite difficult to read:

.. runpython::
    :showcode:

    from textwrap import dedent
    from pyquickhelper.helpgen import rst2html

    text = """

    .. faqref::
        :title: How to add a FAQ?
        :tag: faqexample2

        Some description.

    .. faqreflist::
        :tag: faqexample2
        :contents:

    """

    text = dedent(text)
    conv = rst2html(text)
    print(conv)

That's why I prefer RST:

.. runpython::
    :showcode:

    from textwrap import dedent
    from pyquickhelper.helpgen import rst2html

    text = """

    .. faqref::
        :title: How to add a FAQ?
        :tag: faqexample2

        Some description.

    .. faqreflist::
        :tag: faqexample2
        :contents:

    """

    text = dedent(text)
    conv = rst2html(text, writer="rst")
    print(conv)

The function does not seem to show anything for the instruction ``.. faqreflist::``
because it is only calling :epkg:`docutils` without using everything
:epkg:`Sphinx` adds to it. Let's change that.

.. runpython::
    :showcode:

    from textwrap import dedent
    from pyquickhelper.helpgen import rst2html

    text = """

    .. faqref::
        :title: How to add a FAQ?
        :tag: faqexample2

        Some description.

    .. faqreflist::
        :tag: faqexample2
        :contents:

    """

    text = dedent(text)
    conv = rst2html(text, writer="rst", layout="sphinx")
    print(conv)

You can see now what the directive produces once the tree of nodes (doctree)
is unfold. It is easy to write a unit test based on that. The first part is the
:func:`rst2html <pyquickhelper.helpgen.sphinxm_convert_doc_helper.rst2html>`,
the second part is a ReST builder in extension
:mod:`rst_builder <pyquickhelper.sphinxext.sphinx_rst_builder>`.
To use it, just add it to the list of extensions in ``conf.py``:

::

    extensions = [ ...
        'pyquickhelper.sphinxext.sphinx_rst_builder']

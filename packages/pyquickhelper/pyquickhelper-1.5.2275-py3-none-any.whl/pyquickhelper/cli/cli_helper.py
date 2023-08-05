"""
@file
@brief Automate the creation of a parser based on a function.

.. versionadded:: 1.5
"""
from __future__ import print_function
import argparse
import inspect
from docutils import nodes
from ..helpgen import docstring2html


def create_cli_parser(f, prog=None, layout="sphinx", skip_parameters=('fLOG',)):
    """
    Automatically creates a parser based on a function,
    its signature with annotation and its documentation (assuming
    this documentation is written using Sphinx syntax).

    @param      f               function
    @param      prog            to give the parser a different name than the function name
    @param      use_sphinx      simple documentation only requires :epkg:`docutils`,
                                richer requires :epkg:`sphinx`
    @param      skip_parameters do not expose these parameters
    @return                     :epkg:`*py:argparse:ArgumentParser`

    If an annotation offers mutiple types, the first one will be used for the command line.
    """
    docf = f.__doc__
    doctree = docstring2html(f, writer="doctree", layout=layout)

    # documentation
    docparams = {}
    for node_list in doctree.traverse(nodes.field_list):
        for node in node_list.traverse(nodes.field):
            text = list(filter(lambda c: c.astext().startswith(
                "param "), node.traverse(nodes.Text)))
            body = list(node.traverse(nodes.field_body))
            if len(text) == 1 and len(body) == 1:
                text = text[0]
                body = body[0]
                name = text.astext()
                name = name[5:].strip()
                doc = body.astext()
                if name in docparams:
                    raise ValueError(
                        "Parameter '{0}' is documented twice.\n{1}".format(name, docf))
                docparams[name] = doc

    def clear_node_list(doctree):
        for node_list in doctree.traverse(nodes.field_list):
            node_list.clear()

    # create the parser
    fulldoc = docstring2html(f, writer="rst", layout='sphinx',
                             filter_nodes=clear_node_list)

    # add arguments with the signature
    signature = inspect.signature(f)
    parameters = signature.parameters
    parser = argparse.ArgumentParser(prog=prog or f.__name__, description=fulldoc,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    if skip_parameters is None:
        skip_parameters = []
    names = {"h": "already taken"}
    for k, p in parameters.items():
        if k in skip_parameters:
            continue
        if k not in docparams:
            raise ValueError(
                "Parameter '{0}' is not documented in\n{1}.".format(k, docf))
        create_cli_argument(parser, p, docparams[k], names)

    # end
    return parser


def create_cli_argument(parser, param, doc, names):
    """
    Add an argument for :epkg:`*py:argparse:ArgumentParser`.

    @param      parser      :epkg:`*py:argparse:ArgumentParser`
    @param      param       parameter (from the signature)
    @param      doc         documentation for this parameter
    @param      names       for shortnames

    If an annotation offers mutiple types, the first one will be used for the command line.
    """
    p = param
    if p.annotation and p.annotation != inspect._empty:
        typ = p.annotation
    else:
        typ = type(p.default)
    if typ is None:
        raise ValueError(
            "Unable to infer type of '{0}' ({1})".format(p.name, p))

    if len(p.name) > 3:
        shortname = p.name[0]
        if shortname in names:
            shortname = p.name[0:2]
            if shortname in names:
                shortname = p.name[0:3]
                if shortname in names:
                    shortname = None
    else:
        shortname = None

    if p.name in names:
        raise ValueError(
            "You should change the name of parameter '{0}'".format(p.name))

    pnames = ["--" + p.name]
    if shortname:
        pnames.insert(0, "-" + shortname)
        names[shortname] = p.name

    if isinstance(typ, list):
        # Multiple options for the same parameter
        typ = typ[0]

    if typ in (int, str, float, bool):
        default = None if p.default == inspect._empty else p.default
        if default is not None:
            parser.add_argument(*pnames, type=typ, help=doc, default=default)
        else:
            parser.add_argument(*pnames, type=typ, help=doc)
    else:
        raise NotImplementedError(
            "typ='{0}' not supported (parameter '{1}')".format(typ, p))


def call_cli_function(f, args=None, parser=None, fLOG=print, skip_parameters=('fLOG',)):
    """
    Call a function *f* given parsed arguments.

    @param      f               function to call
    @param      args            arguments to parse (if None, it considers sys.argv)
    @param      parser          parser (can be None, in that case, @see fn create_cli_parser is called)
    @param      fLOG            logging function
    @param      skip_parameters see @see fn create_cli_parser

    This function is used in command line @see fn pyq_sync.
    Its code can can be used as an example. The command line can be tested
    as:

    ::

        class TextMyCommandLine(unittest.TestCase):

            def test_mycommand_line_help(self):
                fLOG(
                    __file__,
                    self._testMethodName,
                    OutputPrint=__name__ == "__main__")

                rows = []

                def flog(*l):
                    rows.append(l)

                mycommand_line(args=['-h'], fLOG=flog)

                r = rows[0][0]
                if not r.startswith("usage: mycommand_line ..."):
                    raise Exception(r)
    """
    if parser is None:
        parser = create_cli_parser(f, skip_parameters=skip_parameters)
    if args is not None and (args == ['--help'] or args == ['-h']):
        fLOG(parser.format_help())
    else:
        try:
            args = parser.parse_args(args=args)
        except SystemExit:
            if fLOG:
                fLOG(parser.format_usage())
            args = None

        if args is not None:
            signature = inspect.signature(f)
            parameters = signature.parameters
            kwargs = {}
            has_flog = False
            for k in parameters:
                if k == "fLOG":
                    has_flog = True
                    continue
                if hasattr(args, k):
                    kwargs[k] = getattr(args, k)
            if has_flog:
                f(fLOG=fLOG, **kwargs)
            else:
                f(**kwargs)

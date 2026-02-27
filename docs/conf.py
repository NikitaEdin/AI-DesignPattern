# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import ast
import glob
import os
import re
import shutil
import sys

docs_dir = os.path.dirname(os.path.abspath(__file__))

source_dirs = [
    os.path.abspath(os.path.join(docs_dir, '../CodeGenerator')),
    os.path.abspath(os.path.join(docs_dir, '../PatternRecogniser')),
    os.path.abspath(os.path.join(docs_dir, '../PatternRecommender')),
]

for source_dir in source_dirs:
    sys.path.insert(0, source_dir)

# -- Project information -----------------------------------------------------
project = 'AI-DesignPattern'
copyright = '2026, Nikita Lanetsky'
author = 'Nikita Lanetsky'
release = '0.5'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Suppress cross-reference ambiguity warnings that arise when two stub
# packages expose identically-named modules (e.g. pr_stubs.workflow_interface
# and prec_stubs.workflow_interface both define AnalysisResult).
suppress_warnings = ['ref.python']

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_imports_from_file(filepath):
    """Return the set of top-level module names imported by *filepath*."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.name.split('.')[0]
                    if name not in sys.builtin_module_names:
                        imports.add(name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    name = node.module.split('.')[0]
                    if name not in sys.builtin_module_names and not name.startswith('.'):
                        imports.add(name)
        return imports
    except Exception:
        return set()


def _get_mock_imports(source_dirs):
    """Collect all internal module names + third-party imports to mock."""
    all_modules = set()
    all_imports = set()
    for source_dir in source_dirs:
        for py_file in glob.glob(os.path.join(source_dir, '*.py')):
            base = os.path.basename(py_file)
            if base.startswith('_'):
                continue
            all_modules.add(base[:-3])
            all_imports.update(_get_imports_from_file(py_file))
    common_stdlib = {
        'os', 'sys', 're', 'json', 'argparse', 'typing', 'datetime',
        'glob', 'shutil', 'collections', 'functools', 'itertools', 'pathlib',
        'enum', 'dataclasses', 'abc', 'math', 'time', 'copy', 'io',
        'matplotlib', 'seaborn', 'pandas', 'numpy', 'PIL',
        'sklearn', 'openai', 'anthropic',
    }
    filtered = {
        imp for imp in all_imports
        if imp not in sys.builtin_module_names and imp not in common_stdlib
    }
    return sorted(all_modules | filtered)


# Matches glob-style wildcards, e.g. ``*.py``, that docutils mis-parses
# as italic-start markers.
_RST_GLOB_RE = re.compile(r'\*(\.\w+)')

# Matches triple-quoted Python docstrings (both flavours).
_DOCSTRING_RE = re.compile(r'(""".*?"""|\'\'\'.*?\'\'\')', re.DOTALL)


def _sanitise_py(content):
    """Escape ``*.ext`` in docstrings only.

    Uses a double backslash (``\\\\*.ext`` in the source file) so that:
    - Python 3.12 does **not** emit ``SyntaxWarning: invalid escape sequence``
      (``\\\\`` is a valid escape for a literal backslash).
    - docutils sees ``\\*.ext`` in the compiled string and renders it as
      the literal text ``*.ext`` without an italic-start warning.

    Glob patterns in ordinary string literals are intentionally left alone.
    """
    def _fix(m):
        return _RST_GLOB_RE.sub(r'\\\\*\1', m.group(0))

    return _DOCSTRING_RE.sub(_fix, content)


# ---------------------------------------------------------------------------
# autodoc_mock_imports – computed once at conf-load time
# ---------------------------------------------------------------------------

autodoc_mock_imports = _get_mock_imports(source_dirs)


# ---------------------------------------------------------------------------
# builder-inited hook: generate stub packages + RST files automatically
# ---------------------------------------------------------------------------

def _generate_stubs(app):
    """
    Called when Sphinx initialises the builder.

    For each source directory we:
    1. Wipe and recreate a neutral stub folder (e.g. ``cg_stubs/``).
    2. Copy every top-level ``.py`` file into it, sanitising docstrings.
    3. Write a minimal RST file for each module.

    The RST toctrees in ``code_generator.rst`` etc. use ``glob: <stub>/*``
    so they pick up the generated files automatically.
    """
    _docs_dir = os.path.dirname(os.path.abspath(__file__))

    dir_configs = [
        ('cg_stubs',   '../CodeGenerator'),
        ('pr_stubs',   '../PatternRecogniser'),
        ('prec_stubs', '../PatternRecommender'),
    ]

    for stubs_subdir, rel_source_path in dir_configs:
        stubs_dir  = os.path.join(_docs_dir, stubs_subdir)
        source_dir = os.path.abspath(os.path.join(_docs_dir, rel_source_path))

        # Always start fresh so removed/renamed source files don't linger.
        if os.path.exists(stubs_dir):
            shutil.rmtree(stubs_dir)
        os.makedirs(stubs_dir)

        # Make it an importable package.
        with open(os.path.join(stubs_dir, '__init__.py'), 'w'):
            pass

        # Collect and copy source files.
        copied = []
        for py_file in sorted(glob.glob(os.path.join(source_dir, '*.py'))):
            base = os.path.basename(py_file)
            if base.startswith('_'):
                continue
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(os.path.join(stubs_dir, base), 'w', encoding='utf-8') as f:
                f.write(_sanitise_py(content))
            copied.append(base[:-3])   # strip .py suffix → module name

        # Write one RST stub per module.
        # IMPORTANT: the underline must immediately follow the title text
        # (no blank line between them) for docutils to recognise it as a
        # section title.  An empty module still shows up in the TOC this way.
        for script_name in copied:
            underline = '=' * len(script_name)
            rst_content = (
                f'{script_name}\n'
                f'{underline}\n'
                '\n'
                f'.. automodule:: {stubs_subdir}.{script_name}\n'
                '   :members:\n'
                '   :undoc-members:\n'
                '   :show-inheritance:\n'
                '   :special-members: __init__\n'
            )
            rst_path = os.path.join(stubs_dir, f'{script_name}.rst')
            with open(rst_path, 'w', encoding='utf-8') as f:
                f.write(rst_content)

    # Ensure docs_dir itself is importable (needed for ``cg_stubs``, etc.).
    if _docs_dir not in sys.path:
        sys.path.insert(0, _docs_dir)


def setup(app):
    app.connect('builder-inited', _generate_stubs)


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

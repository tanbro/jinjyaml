try:
    import importlib.metadata as importlib_metadata  # type: ignore
except ImportError:
    import importlib_metadata  # type: ignore


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


project = "jinjyaml"
copyright = "2023, liu xue yan"
author = "liu xue yan"
# full version
version = importlib_metadata.version(project)
# major/minor version
release = ".".join(version.split(".")[:2])


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx_inline_tabs",
    "sphinx_copybutton",
]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "requirements.txt"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# html_theme = "alabaster"
html_static_path = ["_static"]
html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/tanbro/sqlalchemy-dlock",
    "source_branch": "main",
    "source_directory": "docs/",
    "top_of_page_button": "edit",
}

# Configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "jinja2": ("https://jinja.palletsprojects.com/", None),
}

# -- Options for autodoc ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
autodoc_typehints = "description"

# # Don't show class signature with the class' name.
# autodoc_class_signature = "separated"

autoclass_content = "both"
autodoc_member_order = "bysource"

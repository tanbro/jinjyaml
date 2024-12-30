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

# -- Options for autodoc ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

# autodoc_mock_imports = ["typing", "jinja2", "yaml"]
# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
autodoc_typehints = "both"
# Don't show class signature with the class' name.
# autodoc_class_signature = "separated"
autoclass_content = "both"
autodoc_member_order = "bysource"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx_tippy",
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
    "source_repository": "https://github.com/tanbro/jinjyaml",
    "source_branch": "master",
    "source_directory": "docs/",
    "top_of_page_button": "edit",
}


# -- Options for intersphinx ----------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "jinja2": ("https://jinja.palletsprojects.com/", None),
}

# -- Options for Napoleon settings ---------------------------------------
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True


# -- Options for myst_parser ----------------------------------------------------
myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

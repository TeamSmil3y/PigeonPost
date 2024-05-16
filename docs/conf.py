# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pigeonpost'
copyright = '2023, TeamSmiley'
author = 'TeamSmiley'
release = '0.4.10'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['autoapi.extension', 'sphinxawesome_theme.highlighting']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autoapi_dirs = ['../src/pigeon']
autoapi_type = "python"
autoapi_template_dir = "_templates/autoapi"
# see more at https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_options
autoapi_options = [
    # display children of an object
    "members",
    # display special members e.g. __str__ in python
    #"special-members",
    # display private objects e.g. _foo in python
    #"private-members",
    # display members without docstring
    "undoc-members",
    # display a list of base classes below the class signature
    "show-inheritance",
    # wether to include autosummary directives in generated module documentation
    #"show-module-summary",
    # for objects imported into a package, display objects imported from the same top level package or module. This option does not effect objects imported into a module
    "imported-members",
]
# "signature", "description", "both" or "none"
autodoc_typehints = "signature"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinxawesome_theme'
html_static_path = ['_static']
html_css_files = ['css/style.css']
html_favicon = '_static/pigeon_round.png'
_html_logo = '_static/pigeon_round.png'
html_theme_options = {
    "logo_light": _html_logo,
    "logo_dark": _html_logo
}
import pkg_resources


__version__ = pkg_resources.require("ak-django-oauth-toolkit")[0].version

default_app_config = "oauth2_provider.apps.DOTConfig"

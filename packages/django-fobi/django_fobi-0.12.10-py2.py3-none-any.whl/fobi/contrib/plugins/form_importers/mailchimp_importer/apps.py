__title__ = 'fobi.contrib.plugins.form_importers.mailchimp_importer.apps'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

try:
    __all__ = ('Config',)

    from django.apps import AppConfig

    class Config(AppConfig):
        """Config."""

        name = 'fobi.contrib.plugins.form_importers.mailchimp_importer'
        label = 'fobi_contrib_plugins_form_importers_mailchimp_importer'

except ImportError:
    pass

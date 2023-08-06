__title__ = 'fobi.contrib.themes.foundation5.widgets.form_elements.' \
            'dummy_foundation5_widget.apps'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('Config',)

try:
    from django.apps import AppConfig

    class Config(AppConfig):
        """Config."""

        name = 'fobi.contrib.themes.foundation5.widgets.form_elements.' \
               'dummy_foundation5_widget'
        label = 'fobi_contrib_themes_foundation5_widgets_form_elements_' \
                'dummy_foundation5_widget'

except ImportError:
    pass

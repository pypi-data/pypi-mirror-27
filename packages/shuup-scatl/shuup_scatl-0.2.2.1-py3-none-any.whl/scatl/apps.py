from shuup.apps import AppConfig as ShuupAppConfig


class AppConfig(ShuupAppConfig):
    name = 'scatl'
    verbose_name = 'Catalog filters addon'
    label = 'scatl'
    provides = {
        'api_populator': ['scatl.api.api_populator:populate'],
        'front_urls_post': ['scatl.urls:urlpatterns'],
        'xtheme_plugin': ['scatl.plugins:ScatlPlugin'],
    }

from django.conf import settings as django_settings
from askbot.deps.django_authopenid import default_settings
from askbot.utils.loading import load_module

class ExtendableSettings(object):
    def __init__(self):
        self.settings_stores = list()

    def append(self, settings_store):
        self.settings_stores.append(settings_store)

    def __getattr__(self, attr_name):
        for store in self.settings_stores:
            if hasattr(store, attr_name):
                return getattr(store, attr_name)
        raise KeyError('setting %s not found' % attr_name)

settings = ExtendableSettings()
settings.append(django_settings)

extra_settings_path = getattr(django_settings, 'EXTRA_SETTINGS_MODULE', None)
if extra_settings_path:
    module = load_module(extra_settings_path)
    extra_settings_path.append(module)

settings.append(default_settings)

import importlib
from pathlib import Path
from typing import Any
import pigeon.conf.settings as settings
import types


class ManagerMeta(type):
    """
    Used to overwrite __getattr__ of the Manager class, leading to the ability to overwrite attributes of the
    pigeon.conf.settings module::

        # accessing attributes not part of the Manager class will return getattr(pigeon.conf.settings, attr), therefore:
        Manager.my_setting = my_value

    This works since __getattr__ is only called as a fallback if __getattribute__ cannot find the attribute in question,
    thus not breaking access to attributes of the Manager class, but returning attributes of the settings class if the
    specified attribute is not found in the Manager class.
    """
    def __getattr__(self, key: str) -> Any:
        # get attribute from settings
        key = key.upper()
        if(hasattr(settings, key)): return getattr(settings, key)


class Manager(metaclass=ManagerMeta):
    """
    Used to manage settings and load specified middleware which is only loaded at runtime.

    To override settings either the method Manager.override or the Manager.__get_attr__ method is used::

        # override settings using a module or similar behaving object
        my_settings: types.ModuleType = ...
        Manager.override(my_settings)

        # override settings one at a time by accessing the attributes (__getattr__)
        Manager.my_setting = my_value
    """
    @classmethod
    def _setup(cls):
        """
        Configures any settings that need to be computed at runtime (e.g. typed views).
        """
        # import mime parsers
        for mimetype, parser in cls.mime_parsers.items():
            _module, _class = parser.rsplit('.', 1)
            cls.mime_parsers[mimetype] = getattr(importlib.import_module(_module), _class)

        # import mime generators
        for mimetype, generators in cls.mime_generators.items():
            _module, _class = generators.rsplit('.', 1)
            cls.mime_generators[mimetype] = getattr(importlib.import_module(_module), _class)

        cls.cors_allowed_headers = [header.lower() for header in cls.cors_allowed_headers]


    @classmethod
    def override(cls, new_settings: types.ModuleType | Any):
        """
        Overrides current settings with new settings provided.
        """
        # get all non-standard attributes as dict:
        # attributes = {<attribute_name>:<attribute_value>}
        attributes = {attr: getattr(new_settings, attr) for attr in dir(new_settings) if not attr.startswith('__')}

        # override any attributes that also exist in settings
        for attribute, value in attributes.items():
            if hasattr(settings, attribute):
                old = getattr(settings, attribute)
                if isinstance(old, dict):
                    # if attribute is a dict only change values set in new_settings.attribute
                    old.update(value)
                else:
                    setattr(settings, attribute, value)

        # try to convert attributes containing filepaths to pathlib.Path if they are set
        path_attributes = ['STATIC_FILES_DIR', 'MEDIA_FILES_DIR', 'TEMPLATES_DIR', 'CERTIFICATE_PATH', 'PRIVATE_KEY_PATH']
        for attribute in path_attributes:
            if value := getattr(settings, attribute):
                setattr(settings, attribute, Path(value))

from pathlib import Path
import pigeon.conf.settings as settings
import pigeon.conf.registry as registry
import pigeon.utils.logger as logger

def setup():
    """
    Configures any settings that need to be computed at runtime (e.g. typed views).
    """
    # set verbosity for logger
    logger.VERBOSITY = settings.VERBOSITY


def override(new_settings):
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

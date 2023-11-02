from pathlib import Path
import pigeon.conf.settings as settings
import pigeon.conf.registry as registry


def setup():
    """
    Configures any settings that need to be computed at runtime (e.g. typed views).
    """
    # configure typed views
    configure_typed_views()


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


def configure_typed_views():
    """
    Builds typed views used by middleware in content-negotiation.
    """
    # reverse and restructure views dictionary like {(<func.__name__>,<func.__module__>):url, ...} for easier processing
    # of views in next step.
    reversed_views = dict()
    for url, func in settings.VIEWS.items():
        key = (func.__name__, func.__module__)
        if reversed_views.get(key):
            reversed_views[key].append(url)
        else:
            reversed_views[key] = [url]
            
    # add typed funcs to views
    print(reversed_views)
    print(registry.TYPED_VIEWS)
    for func, content_type in registry.TYPED_VIEWS:
        # determine in which view the current function is listed in and then add it to it
        key = (func.__name__, func.__module__)
        if reversed_views.get(key):
            for url in reversed_views[key]:
                if settings.TYPED_VIEWS.get(url):
                    settings.TYPED_VIEWS[url][content_type] = func
                else:
                    settings.TYPED_VIEWS[url] = {content_type: func}
                

    print(settings.TYPED_VIEWS)
    # add untyped funcs to views as type */*
    for url, func in settings.VIEWS.items():
        if settings.TYPED_VIEWS.get(url):
            if func not in settings.TYPED_VIEWS[url].values():
                settings.TYPED_VIEWS[url]['*/*'] = func
        else:
            settings.TYPED_VIEWS[url] = {'*/*': func}
            
    print(settings.TYPED_VIEWS)
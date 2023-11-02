import pigeon.conf.registry as registry


def content_type(accept):
    """
    Allows overloading functions by giving them a different content_type.
    The decorator is used when defining views to allow developers to give multiple options for content-negotiation.
    The standard middleware will choose one of the views dependent on content-negotiation.
    """
    def _content_type(func):
        registry.TYPED_VIEWS.append((func, accept.lower()))
        return func
    return _content_type

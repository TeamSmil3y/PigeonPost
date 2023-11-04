class MiddlewareTags:
    """
    Used to tag requests by middleware. Tags will be further used when processing
    requeqst (especially in postprocessing) to further analyze the nature of the request
    and set appropriate headers.
    
    A tag can be accessed using MiddlewareTags().<tagname> and will either return its respective
    value or False if it has not been set. This allows for processing of tags even if they have not
    been set.
    
    To set a tag
    """
    def __init__(self):
        self._tags = dict()

    def __getattr__(self, key):
        return self._tags.get(key) or False

    def set(self, key, value):
        self._tags[key] = value

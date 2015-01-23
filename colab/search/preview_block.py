class PreviewBlock():
    '''
    Class to define the fields of the collaboration block
        that are displayed at dashboard and profile pages.
    '''
    tag = None
    title = None
    description = None
    fullname = None
    modified = None
    modified_by = None
    url = None
    type = None
    modified_by_url = None
    collaborator_username = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

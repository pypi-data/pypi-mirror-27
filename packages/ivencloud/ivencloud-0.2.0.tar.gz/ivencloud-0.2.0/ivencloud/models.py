

# Object to be returned after calling activate and senddata functions

class Task:
    def __init__(self, iven_code, value=""):
        self.iven_code = iven_code
        self.value = value


class Error:
    def __init__(self, iven_code, message):
        self.iven_code = iven_code
        self.message = message


class IvenResponse:
    """ this object could be filled differently according to the related request.
        Users should check the fields if they not null or zero,
        otherwise they are set to the data came from the server.
    """

    def __init__(self):
        self.error = None
        self.task = None
        self.status = 0
        self.api_key = None
        self.iven_code = 0
        self.description = None
        self.need_conf_update = False
        self.need_firm_update = False

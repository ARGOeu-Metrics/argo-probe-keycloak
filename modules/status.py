class Status:
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3

    def __init__(self):
        self._code = self.OK
        self._msg = ""

    def set_critical(self, msg):
        self._code = self.CRITICAL
        self._msg = msg

    def set_ok(self, msg):
        self._code = self.OK
        self._msg = msg

    def get_code(self):
        return self._code

    def get_message(self):
        return self._msg

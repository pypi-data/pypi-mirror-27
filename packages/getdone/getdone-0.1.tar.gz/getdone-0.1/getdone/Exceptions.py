class InvalidTaskException(Exception):
    def __init__(self, error_msg):
        Exception.__init__(self, error_msg)
    pass

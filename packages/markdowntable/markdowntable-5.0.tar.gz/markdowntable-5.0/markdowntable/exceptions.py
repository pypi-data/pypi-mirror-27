from __future__ import unicode_literals

class MarkdownTableException(Exception):
    def __init__(self, deubg):
        super(MarkdownTableException,self).__init__()
        Exception.__init__(self, 'There is an error with your Markdown Table. Printing debug information. \n {debug}'.format(debug = debug))

class SuppressedError(MarkdownTableException):
    """docstring for SuppressedError."""

    def __init__(self, error, message, debug):
        """
        :rtype: None
        """
        super(SuppressedError, self).__init__()
        Exception.__init__(self, '''An error has occured. Printing error. information:
        Error Name: {n}
        Error Message: {m}
        Debug Info: {d}'''.format(n=error,m=message,d=debug))

class TooManyValues(MarkdownTableException):
    def __init__(self, columns):
        Exception.__init__(self, 'You entered in too many row values. Please only enter {} row names.'.format(str(columns))')
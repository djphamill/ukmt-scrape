class ErrorHandler(object):
    """
    Abstract class for the error handlers
    """

    ERROR_FILEPATH = '/tmp/error.txt'

    def __init__(self, year, question_number, error_cause):
        self.error_cause = error_cause
        self.year = year
        self.question_number = question_number

        self.handle_error()
    
    def handle_error(self):
        """
        Write an error to the error file
        """
        with open(self.ERROR_FILEPATH, 'a') as f:
            f.write(f"{self.year}/{self.question_number}: {self.error_cause}\n")
        
        print(f'... FAILURE: {self.error_name}')

class ResponseFailureErrorHandler(ErrorHandler):
    """
    Error handler for handling when the response from the HTTP request is not 200
    """

    def __init__(self, year, question_number, image_as_string):
        super(ResponseFailureErrorHandler, self).__init__(year, question_number, image_as_string)
    
    @property
    def error_name(self):
        return 'HTTP response error'


class CannotSliceImageErrorHandler(ErrorHandler):
    """
    Error handler for handling when the text cannot be sliced according to the slicing rulse
    """

    def __init__(self, year, question_number, image_as_string):
        super(CannotSliceImageErrorHandler, self).__init__(year, question_number, image_as_string)
    
    @property
    def error_name(self):
        return 'Could not slice image text'


class HandleError(object):
    """
    A class to point to the correc error handler for different error types arrising from the extract
    """
    RESPONSE_FAILURE = ResponseFailureErrorHandler
    CANNOT_SLICED_IMAGE = CannotSliceImageErrorHandler
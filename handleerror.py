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
        print(f'... FAILURE: {self._type()}')
        
    def _type(self):
        return self.__class__.__name__
    
    def handle_error(self):
        """
        Write an error to the error file
        """
        with open(self.ERROR_FILEPATH, 'a') as f:
            f.write(f"{self.year}/{self.question_number}: {self.error_cause}\n")

class ResponseFailureErrorHandler(ErrorHandler):
    """
    Error handler for handling when the response from the HTTP request is not 200
    """

    def __init__(self, year, question_number, image_as_string):
        super(ResponseFailureErrorHandler, self).__init__(year, question_number, image_as_string)

class CannotSliceImageErrorHandler(ErrorHandler):
    """
    Error handler for handling when the text cannot be sliced according to the slicing rulse
    """

    def __init__(self, year, question_number, image_as_string):
        super(CannotSliceImageErrorHandler, self).__init__(year, question_number, image_as_string)


class HandleError(object):
    """
    A class to handle different types of errors arrising from the extract
    """
    RESPONSE_FAILURE = ResponseFailureErrorHandler
    CANNOT_SLICED_IMAGE = CannotSliceImageErrorHandler
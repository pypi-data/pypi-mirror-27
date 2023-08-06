"""
errors.py - Define custom errors for the client. Errors are parsed from the XML returned by the NextBus service.
            Not all errors are documented so this may not detect all possible errors from the API service.
"""
import re

# In the event of an error the nextbus api may return a 200 OK with some error message in the XML attributes.
# Define some regular expressions for parsing the error messages to determine which error was sent back.
BAD_AGENCY_REGEXP = re.compile(r"\s+Agency\s+parameter\s+\"a=(.+)\"\s+is\s+not\s+valid\.\s+")

BAD_ROUTE_FOR_AGENCY_REGEXP = re.compile(r"\s+Could\s+not\s+get\s+route\s+\"(.+)\"\s+for\s+agency\s+tag\s+"
                                         r"\"(.+)\".\s+One\s+of\s+the\s+tags\s+could\s+be\s+bad\.\s+")

BAD_STOP_FOR_ROUTE_REGEXP = re.compile(r"\s+For\s+agency=(.+)\s+stop\s+s=(.+)\s+is\s+on\s+none\s+of\s+the\s+"
                                       r"directions\s+for\s+r=(.+)\s+so\s+cannot\s+determine\s+which\s+stop\s+to\s+"
                                       r"provide\s+data\s+for\.\s+")


BAD_STOP_ID_INTEGER_REGEXP = re.compile(r"\s+stopId \"(.+)\" is not a valid stop id integer\s+")
BAD_STOP_ID_FOR_AGENCY = re.compile(r"\s+stopId=(.+)\s+is not valid for agency=(.+)\s+")
MISSING_QUERY_PARAMETER = re.compile(r"\s+(.+)\s+parameter\s+\"(.+)\"\s+must\s+be\s+specified\s+in\s+query\s+string\s+")


class UnknownNextBusError(Exception):
    """
    Generic exception raised when an Error element is returned, but it isn't one of the ones defined
    in this module.
    """
    def __init__(self, element):
        message = "Nextbus service returned an error: {0}".format(element.text)
        super().__init__(message)


class MissingQueryParameterError(Exception):
    """
    Exception raised when a request is missing a query parameter.

    Attributes:
          name -- Name of the query parameter
          parameter -- The missing query parameter
          message -- explanation of the error
    """

    def __init__(self, name='', parameter='', message=None):
        """
        Construct a custom Exception for MissingQueryParameterError

        :param name: Name of the query parameter
        :param parameter: The missing query parameter
        :param message: Message for the error
        """
        message = message or "{0} parameter \"{1}\" must be specified in query string".format(name, parameter)
        super().__init__(message)
        self.name = name
        self.parameter = parameter


class InvalidAgencyError(Exception):
    """
    Exception raised when the requested agency does not exist.

    Attributes:
          agency -- Tag for the requested agency.
          message -- explanation of the error.
    """

    def __init__(self, agency, message=None):
        """
        Construct the InvalidAgencyError

        :param agency: Agency tag as a string
        :param message: Message for the error.
        """
        message = message or "Agency parameter \"a={0}\" is not valid".format(agency)
        super().__init__(message)
        self.agency = agency


class InvalidRouteForAgencyError(Exception):
    """
    Exception raised when the requested route does not exist for a given agency.

    Attributes:
          agency -- Tag for the requested agency.
          route -- Tag for the requested route.
          message -- explanation of the error.
    """

    def __init__(self, agency, route, message=None):
        """
        Construct the InvalidRouteForAgencyError

        :param agency: Agency tag as a string
        :param message: Message for the error.
        """
        message = message or "Could not get route \"{0}\" for agency tag \"{1}\"".format(agency, route)
        super().__init__(message)
        self.agency = agency
        self.route = route


class InvalidStopForRouteError(Exception):
    """
    Exception raised when the requested stop does not exist for a given route.

    Attributes:
          agency -- Tag for the requested agency.
          route -- Tag for the requested route.
          stop -- ID of the requested stop.
          message -- explanation of the error.
    """

    def __init__(self, agency, route, stop, message=None):
        """
        Construct the InvalidStopForRouteError

        :param agency: Agency tag as a string
        :param message: Message for the error.
        """
        message_text = "For agency={0} stop s={1} is on none of the directions for r={2} so cannot determine which " \
            "stop to provide data for.".format(agency, stop, route)
        message = message or message_text
        super().__init__(message)
        self.agency = agency
        self.route = route
        self.stop = stop


class InvalidStopIdError(Exception):
    """
    Exception raised when the requested stop id is not valid.

    Attributes:
          stop -- ID of the requested stop.
          message -- explanation of the error.
    """

    def __init__(self, stop_id, message=None):
        """
        Construct an InvalidStopIdError

        :param stop_id: stopId tag as a string
        :param message: Message for the error.
        """
        message = message or "stopId \"{0}\" is not a valid stop id integer".format(stop_id)
        super().__init__(message)
        self.stop_id = stop_id


class InvalidStopIdForAgencyError(Exception):
    """
    Exception raised when the requested stop does not exist for a given agency.

    Attributes:
          agency -- Tag for the requested agency.
          stop -- ID of the requested stop.
          message -- explanation of the error.
    """

    def __init__(self, stop_id='', agency='', message=None):
        """
        Construct the InvalidStopIdForAgencyError

        :param stop_id: stopId tag as a string
        :param agency: agency tag as a string
        :param message: Message for the error.
        """
        message = message or "stopId={0} is not valid for agency={1}".format(stop_id, agency)
        super().__init__(message)
        self.stop_id = stop_id

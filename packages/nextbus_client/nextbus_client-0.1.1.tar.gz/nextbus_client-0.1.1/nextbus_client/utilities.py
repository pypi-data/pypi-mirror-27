"""
utilities.py - Provides some helper methods for the client.
"""
from xml.etree.ElementTree import Element
from . import errors


def validate_xml_element(element, tag):
    """
    Make sure that the given XML element is the right type of object with the correct tag.

    Just raises exceptions if the element is the incorrect type or has the wrong tag.

    :param element: The XML element
    :param tag: The expected value for the tag attribute
    """

    if isinstance(element, Element):
        if element.tag != tag:
            raise ValueError("xml_element must be an xml.etree.ElementTree.Element with tag '{0}'. "
                             "Got '{1}'".format(tag, element.tag))
    else:
        raise TypeError("xml_element must be of type xml.etree.ElementTree.Element Got {0}.".format(type(element)))


def parse_error_xml(error_xml):
    """
    The NextBus API will often return 200 OK with the error details in the body. Parse these and raise the
    appropriate exceptions.

    :param error_xml: The XML ElementTree for the Error.
    """

    # Check if a query parameter was missing.
    match = errors.MISSING_QUERY_PARAMETER.match(error_xml.text)
    if match:
        raise errors.MissingQueryParameterError()

    # Check if the error is an invalid agency tag
    match = errors.BAD_AGENCY_REGEXP.match(error_xml.text)
    if match:
        raise errors.InvalidAgencyError(agency=match.group(1))

    # Check if the error is a bad route for the given agency
    match = errors.BAD_ROUTE_FOR_AGENCY_REGEXP.match(error_xml.text)
    if match:
        raise errors.InvalidRouteForAgencyError(route=match.group(1), agency=match.group(2))

    # Check if the error is a bad stop ID for the given route
    match = errors.BAD_STOP_FOR_ROUTE_REGEXP.match(error_xml.text)
    if match:
        raise errors.InvalidStopForRouteError(agency=match.group(1), stop=match.group(2), route=match.group(3))

    # Check if the error is a bad stop (non-integer) stop ID
    match = errors.BAD_STOP_ID_INTEGER_REGEXP.match(error_xml.text)
    if match:
        raise errors.InvalidStopIdError(stop_id=match.group(1))

    # Check if the error is a bad stop for a given agency.
    match = errors.BAD_STOP_ID_FOR_AGENCY.match(error_xml.text)
    if match:
        raise errors.InvalidStopIdForAgencyError(stop_id=match.group(1), agency=match.group(2))

    if match is None:
        raise errors.UnknownNextBusError(error_xml)

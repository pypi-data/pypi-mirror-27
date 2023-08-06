"""
client.py - Provides a Python interface for the NexBus api commands
"""
from xml.etree import ElementTree
from requests import get
from requests.compat import urljoin
from .agency import Agency
from .route import Route
from .route_config import RouteConfig
from .predictions import Predictions
from .utilities import parse_error_xml


class Client(object):
    """
    The client class provides the interface for making calls to the NextbusClient web api.
    """

    DEFAULT_URL = 'http://webservices.nextbus.com/service/publicXMLFeed'

    def __init__(self, api_url=DEFAULT_URL, headers=None):
        self.api_url = api_url
        self.headers = headers or {'Accept-Encoding': 'gzip, deflate'}

    def _api_call(self, command):
        """
        Make a call to the API and parse the XML values to an xml.etree.ElementTree.Element object

        Will check the XML element output for errors and raise the appropriate Exceptions

        :param command: String containing the api command to call
        :return: Element parsed from the rest response
        """

        request_url = urljoin(self.api_url, "?command={0}".format(command))
        response = get(request_url, headers=self.headers)
        parsed_xml = ElementTree.fromstring(response.content)
        error = parsed_xml.find('Error')
        if isinstance(error, ElementTree.Element):
            # Handle if the API returned an error. This will likely raise an exception so nothing
            # needs to be returned.
            parse_error_xml(error)

        return parsed_xml

    def agency_list(self):
        """
        Returns the list of agencies

        :return: A list of Agency objects parsed from the returned XML.
        """
        agency_list = self._api_call('agencyList')
        agencies = list()
        for agency in agency_list.findall('agency'):
            agencies.append(Agency(xml_element=agency))

        return agencies

    def route_list(self, agency_tag):
        """
        Returns the list of routes for an agency

        :return: A list of Route objects parsed from the returned XML.
        """
        route_list = self._api_call("routeList&a={0}".format(agency_tag))
        routes = list()
        for route in route_list.findall('route'):
            routes.append(Route(xml_element=route))

        return routes

    def route_config(self, agency_tag, route_tag):
        """
        Returns the values from the routeConfig endpoint as a RouteConfig object

        :param agency_tag: The tag attribute for an Agency as a String
        :param route_tag: The tag attribute for a Route as a String
        :return: The RouteConfig for the given Agency and Route
        """

        route_config_xml_elements = self._api_call('routeConfig&a={0}&r={1}'.format(agency_tag, route_tag))
        return RouteConfig(xml_element=route_config_xml_elements.find('route'))

    def predictions(self, agency_tag, stop_tag=None, stop_id=None, route_tag=None, use_short_titles=False):
        """
        Return predictions for the given stop. Must provide at least a stop_id or a stop_tag as a keyword argument.

        :param agency_tag: Tag for the agency for the requested stop.
        :param stop_tag: Tag for the specified stop.
        :param stop_id: Numeric stopId (as a string) for the requested stop
        :param route_tag: Route tag parameter specifies the route for the requested stop. Optional when using stopId.
        :param use_short_titles: Boolean value, whether to return shortened titles suitable for smaller screens.

        :return: A Predictions object with the parameters for the requested stop
        """
        command = "predictions&a={0}".format(agency_tag)
        if stop_id:
            command += "&stopId={0}".format(stop_id)
            if route_tag:
                command += "&routeTag={0}".format(route_tag)
        else:
            if not route_tag or not stop_tag:
                raise AttributeError("Must specify a route_tag and stop_tag when not using a stop_id.")
            command += "&r={0}&s={1}".format(route_tag, stop_tag)

        if use_short_titles:
            command += "&useShortTitles=true"
        predictions_xml_elements = self._api_call(command)
        return Predictions(xml_element=predictions_xml_elements.find('predictions'))

    def multi_stop_predictions(self, agency_tag, route_tag, *args, use_short_titles=False):
        """
        Retrieve predictions for multiple stops.

        :param agency_tag: Tag for the agency to get predictions for
        :param route_tag: Tag for the route to get predictions for
        :param use_short_titles: Specify whether to return shortened names for routes, directions, and agencies.
        :param args: Stop tags to get predictions for. Can specify multiple stops for the same route.
        :return: List of nextbus_client.predictions.Predictions objects.
        """
        command = "predictionsForMultiStops&a={0}".format(agency_tag)
        # Add all of the stops with the route tag to the command string
        for stop in args:
            command += "&stops={0}|{1}".format(route_tag, stop)

        if use_short_titles:
            command += "&useShortTitles=true"

        predictions_xml = self._api_call(command)
        predictions = []
        for prediction in predictions_xml.findall('predictions'):
            predictions.append(Predictions(xml_element=prediction))

        return predictions

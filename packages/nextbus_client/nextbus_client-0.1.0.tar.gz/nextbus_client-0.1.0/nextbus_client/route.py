"""
route.py - Class models a Route as returned by the Nexbus API's routeList command.
"""
from .utilities import validate_xml_element


class Route(object):
    """
    Class models a Route for the routeList command
    """
    ELEMENT_TAG = 'route'

    def __init__(self, **kwargs):
        """
        Default constructor takes kwargs for the Route attributes or an xml_element.

        If an xml_element is given default to that. Otherwise use kwargs.

        :param kwargs: keyword arguments for Route object attributes, or xml_element=xml.etree.ElementTree
        """
        source = kwargs
        if 'xml_element' in kwargs:
            source = kwargs.get('xml_element')
            validate_xml_element(source, self.ELEMENT_TAG)

        self.tag = source.get('tag', '')
        self.title = source.get('title', '')
        self.short_title = source.get('shortTitle', '')

    def to_dict(self):
        """
        Parse the Route to a dictionary.

        :return: Dictionary of Route attributes
        """
        return {'tag': self.tag,
                'title': self.title,
                'shortTitle': self.short_title}

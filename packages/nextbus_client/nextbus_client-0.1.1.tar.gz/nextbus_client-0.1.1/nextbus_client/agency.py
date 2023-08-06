"""
agency.py - Model for an Agency from the NextBus API
"""
from .utilities import validate_xml_element


class Agency(object):
    """
    Class models and Agency for the agencyList api command.
    """
    ELEMENT_TAG = 'agency'

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
        self.region_title = source.get('regionTitle', '')
        self.short_title = source.get('shortTitle', '')

    def to_dict(self):
        """
        Parse the Agency to a dictionary.

        :return: Dictionary of Agency attributes
        """
        return {'tag': self.tag,
                'title': self.title,
                'regionTitle': self.region_title,
                'shortTitle': self.short_title}

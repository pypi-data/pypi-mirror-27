import xml.etree.ElementTree as XML
import uuid


defn = 'jenkins.plugins.parameter__separator.ParameterSeparatorDefinition'

def separator(parser, xml_parent, data):

    """
    yaml: separator
    A separator parameter.

    Example::
      parameters:
        - separator:

    Extended example::
      parameters:
        - separator:
            sectionHeader: "<your_header>"
            sectionHeaderStyle: "<your_header_style>"
            separatorStyle: "<your_style>"
    """

    s_p = XML.SubElement(xml_parent,
                         defn)
    s_p.set('plugin', 'parameter-separator@1.0')

    XML.SubElement(s_p, 'name').text = \
        "separator-{0}".format(uuid.uuid4())
    XML.SubElement(s_p, 'sectionHeader').text = \
        data.get('sectionHeader', '')
    XML.SubElement(s_p, 'sectionHeaderStyle').text = \
        data.get('sectionHeaderStyle', '')
    XML.SubElement(s_p, 'separatorStyle').text = \
        data.get('separatorStyle', '')

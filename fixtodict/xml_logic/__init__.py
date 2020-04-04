from .elem_abbreviation import xml_to_abbreviations, xml_to_abbreviation
from .elem_category import xml_to_categories, xml_to_category
from .elem_component import (
    xml_to_components,
    xml_to_component,
    embed_msg_contents_into_component,
)
from .elem_datatype import xml_to_datatypes, xml_to_datatype
from .elem_enum import xml_to_enums, xml_to_enum
from .elem_field import xml_to_fields, xml_to_field, embed_enums_into_field
from .elem_message import (
    xml_to_messages,
    xml_to_message,
    embed_msg_contents_into_message,
)
from .elem_phrase import xml_to_phrases, xml_to_phrase, embed_docs
from .elem_msg_content import xml_to_msg_contents, xml_to_msg_content
from .elem_section import xml_to_sections, xml_to_section

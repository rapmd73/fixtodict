import unittest
from xml.etree import ElementTree
from fixtodict.repo_basic import *


class TestBasicRepository(unittest.TestCase):

    ABBREVIATIONS_XML = [
        """
        <Abbreviation Term="Funding">
            <AbbrTerm>Fndng</AbbrTerm>
            <Usage>FundingSource component</Usage>
        </Abbreviation>
        """, """
        <Abbreviation added="FIX.5.0SP1" addedEP="77">
            <Term>Detail</Term>
            <AbbrTerm>Detl</AbbrTerm>
        </Abbreviation>
        """, """
        <Abbreviation added="FIX.4.4">
           <Term>ExchangeForPhysical</Term>
           <AbbrTerm>EFP</AbbrTerm>
        </Abbreviation>
        """
    ]

    ABBREVIATIONS_DICT = [{
        "Fndng": {
            "term": "Funding",
            "usage": "FundingSource component",
        }
    }, {
        "Detl": {
            "term": "Detail",
            "added": ["fix", "5", "0", "1", "77"]
        }
    }, {
        "EFP": {
            "term": "ExchangeForPhysical",
            "added": ["fix", "4", "4", "0"]
        }
    }]

    def test_abbreviation(self):
        for (s, expected) in zip(TestBasicRepository.ABBREVIATIONS_XML,
                                 TestBasicRepository.ABBREVIATIONS_DICT):
            xml = ElementTree.fromstring(s)
            actual = xml_to_abbreviation(xml)
            self.assertEqual(actual, expected)

    DATATYPES_XML = [
        """
        <Datatype added="FIX.4.3">
            <Name>Length</Name>
            <BaseType>int</BaseType>
            <Description>lulz</Description>
            <XML>
                <BuiltIn>0</BuiltIn>
                <Base>xs:nonNegativeInteger</Base>
            </XML>
        </Datatype>
        """, """
        <Datatype added="FIX.4.2">
            <Name>LocalMktDate</Name>
            <BaseType>String</BaseType>
            <Description>foobar</Description>
            <Example>BizDate="2003-09-10"</Example>
            <XML>
                <BuiltIn>0</BuiltIn>
                <Base>xs:date</Base>
                <Description>spam</Description>
                <Example>BizDate="2003-09-10"</Example>
            </XML>
        </Datatype>
        """
    ]

    DATATYPES_DICT = [{
        "Length": {
            "baseDatatype": "int",
            "description": "lulz",
            "added": ['fix', '4', '3', '0'],
        }
    }, {
        "LocalMktDate": {
            "baseDatatype": "String",
            "examples": ['BizDate="2003-09-10"'],
            "description": "foobar",
            "added": ['fix', '4', '2', '0'],
        }
    }]

    def test_datatypes(self):
        for (s, expected) in zip(TestBasicRepository.DATATYPES_XML,
                                 TestBasicRepository.DATATYPES_DICT):
            xml = ElementTree.fromstring(s)
            actual = xml_to_datatype(xml)
            self.assertEqual(actual, expected)

    FIELDS_XML = [
        """
        <Field Tag="2841">
            <Name>UnderlyingRefID</Name>
            <Type>String</Type>
            <AbbrName>UndlyRefID</AbbrName>
            <NotReqXML>0</NotReqXML>
            <Description>Identifies ...</Description>
        </Field>
        """
    ]

    FIELDS_DICT = [{
        "2841": {
            "name": "UnderlyingRefID",
            "type": "String",
            "description": "Identifies ..."
        }
    }]

    def test_fields(self):
        for (s, expected) in zip(TestBasicRepository.FIELDS_XML,
                                 TestBasicRepository.FIELDS_DICT):
            xml = ElementTree.fromstring(s)
            actual = xml_to_field(xml)
            self.assertEqual(actual, expected)

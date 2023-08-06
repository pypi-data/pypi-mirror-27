import sys
import unittest
import logging

import asn1tools

sys.path.append('tests/files')
sys.path.append('tests/files/ietf')
sys.path.append('tests/files/3gpp')

from foo import FOO
from bar import BAR
from all_types import ALL_TYPES
from information_object import INFORMATION_OBJECT
from x680 import X680
from x691_a1 import X691_A1
from x691_a2 import X691_A2
from x691_a3 import X691_A3
from x691_a4 import X691_A4
from rrc_8_6_0 import RRC_8_6_0
from rrc_14_4_0 import RRC_14_4_0
from s1ap_14_4_0 import S1AP_14_4_0
from lpp_14_3_0 import LPP_14_3_0
from rfc1155 import RFC1155
from rfc1157 import RFC1157
from rfc2986 import RFC2986
from rfc3161 import RFC3161
from rfc3279 import RFC3279
from rfc3281 import RFC3281
from rfc3447 import RFC3447
from rfc3852 import RFC3852
from rfc4210 import RFC4210
from rfc4211 import RFC4211
from rfc4511 import RFC4511
from rfc5280 import RFC5280
from zforce import ZFORCE


class Asn1ToolsParseTest(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        logging.basicConfig()
        logging.getLogger('asn1tools.parser').setLevel(logging.DEBUG)

    def tearDown(self):
        logging.getLogger('asn1tools.parser').setLevel(logging.ERROR)

    def test_parse_foo(self):
        actual = asn1tools.parse_files('tests/files/foo.asn')
        self.assertEqual(actual, FOO)

    def test_parse_bar(self):
        actual = asn1tools.parse_files('tests/files/bar.asn')
        self.assertEqual(actual, BAR)

    def test_parse_all_types(self):
        actual = asn1tools.parse_files('tests/files/all_types.asn')
        self.assertEqual(actual, ALL_TYPES)

    def test_parse_information_object(self):
        actual = asn1tools.parse_files('tests/files/information_object.asn')
        self.assertEqual(actual, INFORMATION_OBJECT)

    def test_parse_x680(self):
        actual = asn1tools.parse_files('tests/files/x680.asn')
        self.assertEqual(actual, X680)

    def test_parse_x691_a1(self):
        actual = asn1tools.parse_files('tests/files/x691_a1.asn')
        self.assertEqual(actual, X691_A1)

    def test_parse_x691_a2(self):
        actual = asn1tools.parse_files('tests/files/x691_a2.asn')
        self.assertEqual(actual, X691_A2)

    def test_parse_x691_a3(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            actual = asn1tools.parse_files('tests/files/x691_a3.asn')
            self.assertEqual(actual, X691_A3)

        self.assertEqual(
            str(cm.exception),
            "Invalid ASN.1 syntax at line 10, column 22: 'SEQUENCE >!<"
            "(SIZE(2, ...)) OF ChildInformation OPTIONAL,': Expected \"{\".")

    def test_parse_x691_a4(self):
        actual = asn1tools.parse_files('tests/files/x691_a4.asn')
        self.assertEqual(actual, X691_A4)

    def test_parse_rrc_8_6_0(self):
        actual = asn1tools.parse_files('tests/files/3gpp/rrc_8_6_0.asn')
        self.assertEqual(actual, RRC_8_6_0)

    def test_parse_rrc_14_4_0(self):
        actual = asn1tools.parse_files('tests/files/3gpp/rrc_14_4_0.asn')
        self.assertEqual(actual, RRC_14_4_0)

    def test_parse_s1ap_14_4_0(self):
        actual = asn1tools.parse_files('tests/files/3gpp/s1ap_14_4_0.asn')
        self.assertEqual(actual, S1AP_14_4_0)

    def test_parse_lpp_14_3_0(self):
        actual = asn1tools.parse_files('tests/files/3gpp/lpp_14_3_0.asn')
        self.assertEqual(actual, LPP_14_3_0)

    def test_parse_rfc1155(self):
        actual = asn1tools.parse_files('tests/files/ietf/rfc1155.asn')
        self.assertEqual(actual, RFC1155)

    def test_parse_rfc1157(self):
        actual = asn1tools.parse_files('tests/files/ietf/rfc1157.asn')
        self.assertEqual(actual, RFC1157)

    def test_parse_rfc2986(self):
        actual = asn1tools.parse_files('tests/files/ietf/rfc2986.asn')
        self.assertEqual(actual, RFC2986)

    def test_parse_rfc3161(self):
        actual = asn1tools.parse_files('tests/files/ietf/rfc3161.asn')
        self.assertEqual(actual, RFC3161)

    def test_parse_rfc3279(self):
        actual = asn1tools.parse_files('tests/files/ietf/rfc3279.asn')
        self.assertEqual(actual, RFC3279)

    def test_parse_rfc3281(self):
        actual = asn1tools.parse_files('tests/files/ietf/rfc3281.asn')
        self.assertEqual(actual, RFC3281)

    def test_parse_rfc3447(self):
        actual = asn1tools.parse_files('tests/files/ietf/rfc3447.asn')
        self.assertEqual(actual, RFC3447)

    def test_parse_rfc3852(self):
        actual = asn1tools.parse_files('tests/files/ietf/rfc3852.asn')
        self.assertEqual(actual, RFC3852)

    def test_parse_rfc4210(self):
        actual = asn1tools.parse_files('tests/files/ietf/rfc4210.asn')
        self.assertEqual(actual, RFC4210)

    def test_parse_rfc4211(self):
        actual = asn1tools.parse_files('tests/files/ietf/rfc4211.asn')
        self.assertEqual(actual, RFC4211)

    def test_parse_rfc4511(self):
        actual = asn1tools.parse_files('tests/files/ietf/rfc4511.asn')
        self.assertEqual(actual, RFC4511)

    def test_parse_rfc5280(self):
        actual = asn1tools.parse_files('tests/files/ietf/rfc5280.asn')
        self.assertEqual(actual, RFC5280)

    def test_parse_zforce(self):
        actual = asn1tools.parse_files('tests/files/zforce.asn')
        self.assertEqual(actual, ZFORCE)

    def test_parse_imports_global_module_reference(self):
        actual = asn1tools.parse_string('A DEFINITIONS ::= BEGIN '
                                        'IMPORTS '
                                        'a FROM B '
                                        'c, d FROM E global-module-reference '
                                        'f, g FROM H {iso(1)}; '
                                        'END')

        expected = {
            'A': {
                'extensibility-implied': False,
                'imports': {
                    'B': ['a'],
                    'E': ['c', 'd'],
                    'H': ['f', 'g']
                },
                'object-classes': {},
                'object-sets': {},
                'types': {},
                'values': {}
            }
        }

        self.assertEqual(actual, expected)

    def test_parse_error_empty_string(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('')

        self.assertEqual(str(cm.exception),
                         "Invalid ASN.1 syntax at line 1, column 1: '>!<': "
                         "Expected modulereference.")

    def test_parse_error_begin_missing(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A DEFINITIONS ::= END')

        self.assertEqual(str(cm.exception),
                         "Invalid ASN.1 syntax at line 1, column 19: "
                         "'A DEFINITIONS ::= >!<END': Expected BEGIN.")

    def test_parse_error_end_missing(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A DEFINITIONS ::= BEGIN')

        self.assertEqual(str(cm.exception),
                         "Invalid ASN.1 syntax at line 1, column 24: "
                         "'A DEFINITIONS ::= BEGIN>!<': Expected END.")

    def test_parse_error_type_assignment_missing_assignment(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A DEFINITIONS ::= BEGIN A END')

        self.assertEqual(str(cm.exception),
                         "Invalid ASN.1 syntax at line 1, column 27: "
                         "'A DEFINITIONS ::= BEGIN A >!<END': "
                         "Expected ::=.")

    def test_parse_error_value_assignment_missing_assignment(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A DEFINITIONS ::= BEGIN a INTEGER END')

        self.assertEqual(str(cm.exception),
                         "Invalid ASN.1 syntax at line 1, column 35: "
                         "'A DEFINITIONS ::= BEGIN a INTEGER >!<END': "
                         "Expected ::=.")

    def test_parse_error_sequence_missing_type(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A DEFINITIONS ::= BEGIN'
                                   '  A ::= SEQUENCE { a } '
                                   'END')

        self.assertEqual(
            str(cm.exception),
            "Invalid ASN.1 syntax at line 1, column 45: 'A DEFINITIONS ::= BEGIN "
            " A ::= SEQUENCE { a >!<} END': Expected Type.")

    def test_parse_error_sequence_missing_member_name(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A DEFINITIONS ::= BEGIN'
                                   '  A ::= SEQUENCE { A } '
                                   'END')

        self.assertEqual(
            str(cm.exception),
            "Invalid ASN.1 syntax at line 1, column 43: 'A DEFINITIONS ::= "
            "BEGIN  A ::= SEQUENCE { >!<A } END': Expected \"}\".")

    def test_parse_error_definitive_identifier(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A {} DEFINITIONS ::= BEGIN '
                                   'END')

        self.assertEqual(
            str(cm.exception),
            "Invalid ASN.1 syntax at line 1, column 4: 'A {>!<} DEFINITIONS "
            "::= BEGIN END': Expected {{identifier Suppress:(\"(\") - "
            "definitiveNumberForm - Suppress:(\")\")} | identifier | "
            "definitiveNumberForm}.")

    def test_parse_error_missing_union_member_beginning(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A DEFINITIONS ::= BEGIN '
                                   'B ::= INTEGER (| SIZE (1))'
                                   'END')

        self.assertEqual(
            str(cm.exception),
            "Invalid ASN.1 syntax at line 1, column 40: 'A DEFINITIONS ::= BEGIN "
            "B ::= INTEGER (>!<| SIZE (1))END': Expected one or more constraints.")

    def test_parse_error_missing_union_member_middle(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A DEFINITIONS ::= BEGIN '
                                   'B ::= INTEGER (SIZE (1) | | (0))'
                                   'END')

        self.assertEqual(
            str(cm.exception),
            "Invalid ASN.1 syntax at line 1, column 49: \'A DEFINITIONS "
            "::= BEGIN B ::= INTEGER (SIZE (1) >!<| | (0))END\': Expected \")\".")

    def test_parse_error_missing_union_member_end(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A DEFINITIONS ::= BEGIN '
                                   'B ::= INTEGER (SIZE (1) |)'
                                   'END')

        self.assertEqual(
            str(cm.exception),
            "Invalid ASN.1 syntax at line 1, column 49: \'A DEFINITIONS "
            "::= BEGIN B ::= INTEGER (SIZE (1) >!<|)END\': Expected \")\".")

    def test_parse_error_size_constraint_missing_parentheses(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A DEFINITIONS ::= BEGIN '
                                   'B ::= INTEGER (SIZE 1)'
                                   'END')

        self.assertEqual(
            str(cm.exception),
            "Invalid ASN.1 syntax at line 1, column 45: \'A DEFINITIONS ::= "
            "BEGIN B ::= INTEGER (SIZE >!<1)END\': Expected \"(\".")

    def test_parse_error_size_constraint_missing_size(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A DEFINITIONS ::= BEGIN '
                                   'B ::= INTEGER (SIZE ())'
                                   'END')

        self.assertEqual(
            str(cm.exception),
            "Invalid ASN.1 syntax at line 1, column 46: 'A DEFINITIONS ::= "
            "BEGIN B ::= INTEGER (SIZE (>!<))END': Expected one or more "
            "constraints.")

    def test_parse_error_tag_class_number_missing(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A DEFINITIONS ::= BEGIN '
                                   'B ::= [] INTEGER '
                                   'END')

        self.assertEqual(
            str(cm.exception),
            "Invalid ASN.1 syntax at line 1, column 32: 'A DEFINITIONS "
            "::= BEGIN B ::= [>!<] INTEGER END': Expected ClassNumber.")

    def test_parse_error_missing_type(self):
        with self.assertRaises(asn1tools.ParseError) as cm:
            asn1tools.parse_string('A DEFINITIONS ::= BEGIN '
                                   'B ::= '
                                   'END')

        self.assertEqual(
            str(cm.exception),
            "Invalid ASN.1 syntax at line 1, column 31: 'A DEFINITIONS ::= BEGIN "
            "B ::= >!<END': Expected Type.")


if __name__ == '__main__':
    unittest.main()

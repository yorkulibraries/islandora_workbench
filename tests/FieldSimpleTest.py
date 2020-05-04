import sys
import os
import unittest

sys.path.append('modules')

from field_simple import update


class TestSimpleField(unittest.TestCase):

    def test_replace_single_value(self):
        config = {'update_mode': 'replace', 'subdelimiter': '|'}
        field_definition = {'cardinality': -1}
        csv_row_value = 'Testing'
        node_field_values = {}
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_foo', '10')
        self.assertDictEqual(res[0], {'value': 'Testing'})

    def test_replace_multi_value(self):
        config = {'update_mode': 'replace', 'subdelimiter': '|'}
        field_definition = {'cardinality': -1}
        csv_row_value = 'Testing|Multiple values'
        node_field_values = {}
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_foo', '10')
        self.assertDictEqual(res[0], {'value': 'Testing'})
        self.assertDictEqual(res[1], {'value': 'Multiple values'})

    def test_append_values(self):
        config = {'update_mode': 'append', 'subdelimiter': '|'}
        field_definition = {'cardinality': -1}
        csv_row_value = 'Second|Third'
        node_field_values = dict()
        node_field_values['field_foo'] = [{'value': 'I was here first'}]
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_foo', '10')
        self.assertDictEqual(res[0], {'value': 'I was here first'})
        self.assertDictEqual(res[1], {'value': 'Second'})
        self.assertDictEqual(res[2], {'value': 'Third'})


if __name__ == '__main__':
    unittest.main()

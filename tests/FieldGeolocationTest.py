import sys
import os
import unittest

sys.path.append('modules')

from field_geolocation import update


class TestGeolocationField(unittest.TestCase):

    def test_replace_single_value(self):
        config = {'update_mode': 'replace', 'subdelimiter': '|'}
        field_definition = {'cardinality': -1}
        csv_row_value = '41.2221, -111.112'
        node_field_values = {'lat': '49.16667', 'lng': '-123.93333'}
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_foo_geo', '100')
        self.assertDictEqual(res[0], {'lat': '41.2221', 'lng': '-111.112'})

    def test_append_single_value(self):
        config = {'update_mode': 'append', 'subdelimiter': '|'}
        field_definition = {'cardinality': -1}
        csv_row_value = '41.2222, -111.111'
        node_field_values = [{'lat': '49.16667', 'lng': '-123.93333'}]
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_foo_geo', '100')
        self.assertDictEqual(res[0], {'lat': '49.16667', 'lng': '-123.93333'})
        self.assertDictEqual(res[1], {'lat': '41.2222', 'lng': '-111.111'})

    def test_replace_multi_value(self):
        config = {'update_mode': 'replace', 'subdelimiter': ';'}
        field_definition = {'cardinality': -1}
        csv_row_value = '41.2223, -111.113;32.111,1.222'
        node_field_values = {'lat': '49.16667', 'lng': '-123.93333'}
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_foo_geo', '10')
        self.assertEqual(len(res), 2)
        self.assertDictEqual(res[0], {'lat': '41.2223', 'lng': '-111.113'})
        self.assertDictEqual(res[1], {'lat': '32.111', 'lng': '1.222'})

    def test_append_multi_values(self):
        config = {'update_mode': 'append', 'subdelimiter': ';'}
        field_definition = {'cardinality': -1}
        csv_row_value = '41.9223, -111.913;32.911,1.922'
        node_field_values = [{'lat': '49.16668', 'lng': '-123.93334'}]
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_foo', '10')
        self.assertEqual(len(res), 3)
        self.assertDictEqual(res[0], {'lat': '49.16668', 'lng': '-123.93334'})
        self.assertDictEqual(res[1], {'lat': '41.9223', 'lng': '-111.913'})
        self.assertDictEqual(res[2], {'lat': '32.911', 'lng': '1.922'})


if __name__ == '__main__':
    unittest.main()

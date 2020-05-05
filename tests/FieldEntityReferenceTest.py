import sys
import os
import unittest

sys.path.append('modules')

from field_entity_reference import update


class TestEntityReferenceField(unittest.TestCase):

    # Unlimited cardinality.
    def test_replace_single_term_value(self):
        config = {'update_mode': 'replace', 'subdelimiter': '|'}
        field_definition = {'field_type': 'entity_reference', 'target_type': 'taxonomy_term', 'vocabularies': ['genre'], 'cardinality': -1}
        csv_row_value = '5'
        node_field_values = {}
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_genre', '10')
        self.assertDictEqual(res[0], {'target_id': '5', 'target_type': 'taxonomy_term'})

    def test_replace_multi_term_value(self):
        config = {'update_mode': 'replace', 'subdelimiter': '|'}
        field_definition = {'field_type': 'entity_reference', 'target_type': 'taxonomy_term', 'vocabularies': ['genre'], 'cardinality': -1}
        csv_row_value = '2|4'
        node_field_values = {'target_id': '1', 'target_type': 'taxonomy_term'}
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_genre', '10')
        self.assertDictEqual(res[0], {'target_id': '2', 'target_type': 'taxonomy_term'})
        self.assertDictEqual(res[1], {'target_id': '4', 'target_type': 'taxonomy_term'})

    def test_append_term_values(self):
        config = {'update_mode': 'append', 'subdelimiter': '|'}
        field_definition = {'field_type': 'entity_reference', 'target_type': 'taxonomy_term', 'vocabularies': ['genre'], 'cardinality': -1}
        csv_row_value = '6|8'
        node_field_values = dict()
        node_field_values['field_genre'] = [{'target_id': '5', 'target_type': 'taxonomy_term'}]
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_genre', '10')
        self.assertDictEqual(res[0], {'target_id': '5', 'target_type': 'taxonomy_term'})
        self.assertDictEqual(res[1], {'target_id': '6', 'target_type': 'taxonomy_term'})
        self.assertDictEqual(res[2], {'target_id': '8', 'target_type': 'taxonomy_term'})

    def test_replace_single_noderef_value(self):
        config = {'update_mode': 'replace', 'subdelimiter': '|'}
        field_definition = {'field_type': 'entity_reference', 'target_type': 'node', 'cardinality': -1}
        csv_row_value = '100'
        node_field_values = {}
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_member_of', '10')
        self.assertDictEqual(res[0], {'target_id': '100', 'target_type': 'node_type'})

    def test_replace_multi_noderef_value(self):
        config = {'update_mode': 'replace', 'subdelimiter': '|'}
        field_definition = {'field_type': 'entity_reference', 'target_type': 'node', 'cardinality': -1}
        csv_row_value = '20|40'
        node_field_values = {'target_id': '30', 'target_type': 'node_type'}
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_member_of', '10')
        self.assertDictEqual(res[0], {'target_id': '20', 'target_type': 'node_type'})
        self.assertDictEqual(res[1], {'target_id': '40', 'target_type': 'node_type'})

    def test_append_noderef_value(self):
        config = {'update_mode': 'append', 'subdelimiter': '|'}
        field_definition = {'field_type': 'entity_reference', 'target_type': 'node', 'cardinality': -1}
        csv_row_value = '31|41'
        node_field_values = dict()
        node_field_values['field_member_of'] = [{'target_id': '21', 'target_type': 'node_type'}]
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_member_of', '10')
        self.assertDictEqual(res[0], {'target_id': '21', 'target_type': 'node_type'})
        self.assertDictEqual(res[1], {'target_id': '31', 'target_type': 'node_type'})
        self.assertDictEqual(res[2], {'target_id': '41', 'target_type': 'node_type'})

    # Cardinality is limited.
    def test_replace_multi_term_value_limited_cardinality(self):
        config = {'update_mode': 'replace', 'subdelimiter': '|'}
        field_definition = {'field_type': 'entity_reference', 'target_type': 'taxonomy_term', 'vocabularies': ['genre'], 'cardinality': 2}
        csv_row_value = '2|4|5'
        node_field_values = {'target_id': '1', 'target_type': 'taxonomy_term'}
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_genre', '10')
        self.assertEqual(len(res), 2)
        self.assertDictEqual(res[0], {'target_id': '2', 'target_type': 'taxonomy_term'})
        self.assertDictEqual(res[1], {'target_id': '4', 'target_type': 'taxonomy_term'})

    def test_append_multi_term_value_limited_cardinality(self):
        config = {'update_mode': 'append', 'subdelimiter': '|'}
        field_definition = {'field_type': 'entity_reference', 'target_type': 'taxonomy_term', 'vocabularies': ['genre'], 'cardinality': 2}
        csv_row_value = '3|4'
        node_field_values = dict()
        node_field_values['field_genre'] = [{'target_id': '1', 'target_type': 'taxonomy_term'}]
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_genre', '10')
        self.assertEqual(len(res), 2)
        self.assertDictEqual(res[0], {'target_id': '1', 'target_type': 'taxonomy_term'})
        self.assertDictEqual(res[1], {'target_id': '3', 'target_type': 'taxonomy_term'})

    def test_replace_multi_noderef_value_limited_cardinality(self):
        config = {'update_mode': 'replace', 'subdelimiter': '|'}
        field_definition = {'field_type': 'entity_reference', 'target_type': 'node', 'cardinality': 2}
        csv_row_value = '20|40|50'
        node_field_values = {'target_id': '30', 'target_type': 'node_type'}
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_member_of', '10')
        self.assertEqual(len(res), 2)
        self.assertDictEqual(res[0], {'target_id': '20', 'target_type': 'node_type'})
        self.assertDictEqual(res[1], {'target_id': '40', 'target_type': 'node_type'})

    def test_append_noderef_value_limited_cardinality(self):
        config = {'update_mode': 'append', 'subdelimiter': '|'}
        field_definition = {'field_type': 'entity_reference', 'target_type': 'node', 'cardinality': 2}
        csv_row_value = '31|41'
        node_field_values = dict()
        node_field_values['field_member_of'] = [{'target_id': '21', 'target_type': 'node_type'}]
        res = update(config, field_definition, csv_row_value, node_field_values, 'field_member_of', '10')
        self.assertEqual(len(res), 2)
        self.assertDictEqual(res[0], {'target_id': '21', 'target_type': 'node_type'})
        self.assertDictEqual(res[1], {'target_id': '31', 'target_type': 'node_type'})


if __name__ == '__main__':
    unittest.main()

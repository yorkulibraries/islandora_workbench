from workbench_utils import *


def update(config, field_definition, csv_row_value, node_field_values, custom_field_name, node_id):
    if field_definition['field_type'] == 'entity_reference':
        if field_definition['target_type'] == 'taxonomy_term':
            target_type = 'taxonomy_term'
            field_vocabs = get_field_vocabularies(config, field_definition)
            if config['subdelimiter'] in csv_row_value:
                prepared_tids = []
                delimited_values = csv_row_value.split(config['subdelimiter'])
                for delimited_value in delimited_values:
                    tid = prepare_term_id(config, field_vocabs, delimited_value)
                    tid = str(tid)
                    prepared_tids.append(tid)
                csv_row_value = config['subdelimiter'].join(prepared_tids)
            else:
                csv_row_value = prepare_term_id(config, field_vocabs, csv_row_value)
                csv_row_value = str(csv_row_value)

        if field_definition['target_type'] == 'node':
            target_type = 'node_type'

        if field_definition['cardinality'] == 1:
            subvalues = csv_row_value.split(config['subdelimiter'])
            custom_field_json = [{'target_id': subvalues[0], 'target_type': target_type}]
            if len(subvalues) > 1:
                log_field_cardinality_violation(custom_field_name, node_id, '1')
        # Cardinality has a limit.
        elif field_definition['cardinality'] > 1:
            if config['update_mode'] == 'append':
                # Append to existing values.
                existing_target_ids = get_target_ids(node_field_values[custom_field_name])
                num_existing_values = len(existing_target_ids)
            else:
                existing_target_ids = []
                num_existing_values = 0

            if config['subdelimiter'] in csv_row_value:
                field_values = []
                subvalues = csv_row_value.split(config['subdelimiter'])
                for subvalue in subvalues:
                    if subvalue in existing_target_ids:
                        existing_target_ids.remove(subvalue)
                num_values_to_add = field_definition['cardinality'] - num_existing_values
                subvalues = subvalues[:num_values_to_add]
                if len(subvalues) > 0:
                    logging.warning("Adding all values in CSV field %s for node %s would exceed maximum number of " +
                                    "allowed values (%s), so only adding %s values.", custom_field_name, node_id, field_definition['cardinality'], num_values_to_add)
                    logging.info("Updating node %s with %s values from CSV record.", node_id, num_values_to_add)
                    for subvalue in subvalues:
                        field_values.append({'target_id': subvalue, 'target_type': target_type})
                    if config['update_mode'] == 'append':
                        custom_field_json = node_field_values[custom_field_name] + field_values
                    else:
                        custom_field_json = field_values
                else:
                    logging.info("Not updating field %s node for %s, provided values do not contain any new values for this field.", custom_field_name, node_id)
            else:
                if num_existing_values + 1 <= field_definition['cardinality']:
                    custom_field_json = node_field_values[custom_field_name] + [{'target_id': csv_row_value, 'target_type': 'taxonomy_term'}]
                else:
                    logging.warning("Not updating field %s node for %s, adding provided value would exceed maxiumum number of allowed values.", custom_field_name, node_id)
        # Cardinality is unlimited.
        else:
            # Append to existing values.
            if config['subdelimiter'] in csv_row_value:
                field_values = []
                subvalues = csv_row_value.split(config['subdelimiter'])
                for subvalue in subvalues:
                    field_values.append({'target_id': subvalue, 'target_type': target_type})
                    if config['update_mode'] == 'append':
                        custom_field_json = node_field_values[custom_field_name] + field_values
                    else:
                        custom_field_json = field_values
            else:
                if config['update_mode'] == 'append':
                    custom_field_json = node_field_values[custom_field_name] + [{'target_id': csv_row_value, 'target_type': 'taxonomy_term'}]
                else:
                    custom_field_json = [{'target_id': csv_row_value, 'target_type': target_type}]

    return custom_field_json

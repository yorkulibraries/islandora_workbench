from workbench_utils import *


def update(config, field_definition, csv_row_value, node_field_values, custom_field_name, node_id):
    # Cardinality is unlimited.
    if field_definition['cardinality'] == -1:
        if config['subdelimiter'] in csv_row_value:
            field_values = []
            subvalues = split_geolocation_string(config, csv_row_value)
            for subvalue in subvalues:
                field_values.append(subvalue)
            if config['update_mode'] == 'append':
                # Append to existing values.
                custom_field_json = node_field_values + field_values
            else:
                custom_field_json = field_values
        else:
            field_value = split_geolocation_string(config, csv_row_value)
            if config['update_mode'] == 'append':
                # Append to existing values.
                custom_field_json = node_field_values + field_value
            else:
                custom_field_json = field_value
    # Cardinality has a limit.
    elif field_definition['cardinality'] > 1:
        if config['subdelimiter'] in csv_row_value:
            field_values = []
            subvalues = split_geolocation_string(config, csv_row_value)
            if len(subvalues) > field_definition['cardinality']:
                log_field_cardinality_violation(custom_field_name, node_id, field_definition['cardinality'])
            subvalues = subvalues[:field_definition['cardinality']]
            for subvalue in subvalues:
                    field_values.append(subvalue)
            custom_field_json = field_values
        else:
            field_value = split_geolocation_string(config, csv_row_value)
            custom_field_json = field_value
    # Cardinality is 1.
    else:
        field_values = split_geolocation_string(config, csv_row_value)
        custom_field_json = [field_values[0]]
        if len(field_values) > 1:
            log_field_cardinality_violation(custom_field_name, node_id, field_definition['cardinality'])

    return custom_field_json

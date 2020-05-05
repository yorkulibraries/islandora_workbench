from workbench_utils import *


def update(config, field_definition, csv_row_value, node_field_values, custom_field_name, node_id):
    if field_definition['cardinality'] == 1:
        subvalues = csv_row_value.split(config['subdelimiter'])
        node_field_value = [{'value': subvalues[0]}]
        if len(subvalues) > 1:
            log_field_cardinality_violation(custom_field_name, node_id, '1')
    elif field_definition['cardinality'] > 1:
        # Append to existing values.
        if config['subdelimiter'] in csv_row_value:
            field_values = []
            subvalues = csv_row_value.split(config['subdelimiter'])
            if len(subvalues) > field_definition['cardinality']:
                log_field_cardinality_violation(custom_field_name, node_id, field_definition['cardinality'])
            subvalues = subvalues[:field_definition['cardinality']]
            for subvalue in subvalues:
                field_values.append({'value': subvalue})
            if config['update_mode'] == 'append':
                custom_field_json = node_field_values[custom_field_name] + field_values
            else:
                custom_field_json = field_values
        else:
            if config['update_mode'] == 'append':
                custom_field_json = node_field_values[custom_field_name] + [{'value': csv_row_value}]
            else:
                custom_field_json = [{'value': csv_row_value}]
    # Cardinatlity is unlimited.
    else:
        # Append to existing values.
        if config['subdelimiter'] in csv_row_value:
            field_values = []
            subvalues = csv_row_value.split(config['subdelimiter'])
            for subvalue in subvalues:
                field_values.append({'value': subvalue})
            if config['update_mode'] == 'append':
                custom_field_json = node_field_values[custom_field_name] + field_values
            else:
                custom_field_json = field_values
        else:
            if config['update_mode'] == 'append':
                custom_field_json = node_field_values[custom_field_name] + [{'value': csv_row_value}]
            else:
                custom_field_json = [{'value': csv_row_value}]

    return custom_field_json

def clear_nones(value):
    if isinstance(value, list):
        return [clear_nones(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {
            key: clear_nones(val)
            for key, val in value.items()
            if val is not None
        }
    else:
        return value

def get_property_as_list(property_name):
    if property_name is None:
        return []
    if not isinstance(property_name, list):
        return [property_name]
    return property_name

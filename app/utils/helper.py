

def filter_data(model, data):
    return {key: value for key, value in data.items() if hasattr(model, key)}


def set_attrs(obj, data: dict):
    if data:
        for key, value in data.items():
            if value is None:
                continue
            setattr(obj, key, value)
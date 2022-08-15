import json


def update_metadata(metadata, **kwargs):
    decoded_metadata = bytes(metadata).decode()
    parsed_metadata = json.loads(decoded_metadata)

    parsed_metadata.update(kwargs)

    return json.dumps(parsed_metadata).encode()

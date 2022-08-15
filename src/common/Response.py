import json


class Response:
    def __new__(self, status, data=None, msg=None):
        body = {}

        if data:
            body.update(data)
        if msg:
            body["message"] = msg

        return {
            "statusCode": status,
            "body": json.dumps(body),
        }

import json as _json
import uuid


class JSON(_json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'json'):
            return obj.json
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, uuid.UUID):
            return obj.hex
        # Let the base class default method raise the TypeError
        return _json.JSONEncoder.default(self, obj)

    def loads(self, bytes):
        return _json.loads(bytes, encoding='utf-8')


js = JSON()

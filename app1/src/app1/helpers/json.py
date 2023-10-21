import decimal
import json
from datetime import date, datetime


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        # Let the base class default method raise the TypeError
        return super().default(self, obj)


class CustomDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs
        )

    @staticmethod
    def parse_item(value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                pass

            try:
                return decimal.Decimal(value)
            except decimal.InvalidOperation:
                pass
        return value

    def object_hook(self, obj):
        for key in obj:
            if isinstance(obj[key], list):
                new = []
                for item in obj[key]:
                    new.append(self.parse_item(item))
                obj[key] = new
            else:
                obj[key] = self.parse_item(obj[key])
        return obj


def custom_json_serializer(obj, pretty=False):
    kwargs = {"sort_keys": True, "indent": 4} if pretty else {}

    return json.dumps(obj, cls=CustomEncoder, **kwargs)


def custom_json_deserializer(string):
    return json.loads(string, cls=CustomDecoder)

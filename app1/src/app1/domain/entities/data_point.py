from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Optional, Union
from .base import Value

class DataPoint(Value):
    def __init__(
        self,
        name: str,
        value: Union[int, float, Decimal, str, date, List, Dict],
    ):
        self.name = name
        self.value = value

    @classmethod
    def create(cls, name, value):
        return cls(name, value)


class DataPoints:
    def __init__(self):
        self.data_points = dict()

    def add(self, datapoint: DataPoint):
        self.data_points[datapoint.name] = datapoint

    def add_from(self, name, value):
        datapoint = DataPoint.create(name, value)
        self.data_points[datapoint.name] = datapoint

    def find_many(self, names: List[str]):
        to_match = set(names)
        return [
            item for item in self.data_points.values() if item.name in to_match
        ]

    def find(self, name):
        datapoints = self.find_many([name])
        if datapoints:
            return datapoints[0]

    def filter_to_dict(self, names):
        return {item.name: item.value for item in self.find_many(names)}

    def to_dict(self):
        return {item.name: item.value for item in self.data_points.values()}

    def __repr__(self):
        return repr({repr(x) for x in self.data_points.values()})

import json

from Models.TimeRange import TimeRange


class StatisticsResource:
    def __init__(self, randomNumberAverage: float, timeRange: TimeRange, minute: int):
        self.randomNumberAverage = randomNumberAverage
        self.timeRange = timeRange
        self.minute = minute

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

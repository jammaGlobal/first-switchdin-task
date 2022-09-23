import json

from Models.TimeRange import TimeRange


class StatisticsResource:
    def __init__(self, randomNumberAverage: float, timeRange: TimeRange):
        self.randomNumberAverage = randomNumberAverage
        self.timeRange = timeRange

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

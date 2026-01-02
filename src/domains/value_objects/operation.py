import json

from src.domains.value_objects.business_hours import BusinessHours


class Operation:
    def __init__(self, weekly_hours: list[BusinessHours]):
        if not weekly_hours:
            raise ValueError('Horário de funcionamento não pode ser vazio')

        self._validate_days(weekly_hours)
        self.weekly_hours = weekly_hours

    def _validate_days(self, weekly_hours: list[BusinessHours]):
        days = [business_hour.day for business_hour in weekly_hours]
        if len(days) != len(set(days)):
            raise ValueError('Dias duplicados foram adicionados')

    def has_open_day(self):
        return any(business_hour.is_open() for business_hour in self.weekly_hours)

    def to_dict(self):
        return {
            "weekly_hours": [
                business_hour.to_dict()
                for business_hour in self.weekly_hours
            ]
        }

    def to_json(self):
        return json.dumps(self.to_dict())

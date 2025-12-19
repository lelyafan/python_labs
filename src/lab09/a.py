from dataclasses import dataclass
from datetime import datetime, date
from typing import ClassVar

@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float
    __date_format: ClassVar[str] = "%Y-%m-%d"
    def __post_init__(self):
        self._validate_birthdate()
        self._validate_gpa()
    def _validate_birthdate(self):
        try:
            datetime.strptime(self.birthdate, self.__date_format)
        except ValueError:
            raise ValueError(f"Дата должна быть в формате {self.__date_format}")
    def _validate_gpa(self):
        if not (0 <= self.gpa <= 5):
            raise ValueError("GPA должен быть в диапазоне от 0 до 5")
    def age(self) -> int:
        birth_date = datetime.strptime(self.birthdate, self.__date_format).date()
        today = date.today()
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age
    def to_dict(self) -> dict:
        return {
            "fio": self.fio,
            "birthdate": self.birthdate,
            "group": self.group,
            "gpa": self.gpa
        }
    @classmethod
    def from_dict(cls, d: dict) -> 'Student':
        return cls(
            fio = d["fio"],
            birthdate = d["birthdate"],
            group = d["group"],
            gpa= d ["gpa"]
        )
    def __str__(self):
        return f"{self.fio}, {self.group}, GPA: {self.gpa:.2f}, возраст: {self.age()} лет"
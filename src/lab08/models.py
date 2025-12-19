from dataclasses import dataclass
from datetime import date, datetime


DATE_FORMAT = "%Y-%m-%d"


@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float

    @staticmethod
    def _validate_birthdate(value: str) -> date:
        try:
            return datetime.strptime(value, DATE_FORMAT).date()
        except ValueError:
            raise ValueError(
                f"Некорректный формат даты '{value}'. Ожидается {DATE_FORMAT}"
            )

    @staticmethod
    def _validate_gpa(value: float) -> float:
        try:
            gpa_value = float(value)
        except (TypeError, ValueError):
            raise ValueError("Средний балл должен быть числом")

        if not 0 <= gpa_value <= 5:
            raise ValueError("Средний балл должен быть в диапазоне от 0 до 5")
        return gpa_value

    def __post_init__(self) -> None:
        self._birthdate_dt = self._validate_birthdate(self.birthdate)
        self.gpa = self._validate_gpa(self.gpa)

    def age(self) -> int:
        today = date.today()
        years = today.year - self._birthdate_dt.year
        if (today.month, today.day) < (
            self._birthdate_dt.month,
            self._birthdate_dt.day,
        ):
            years -= 1
        return years

    def to_dict(self):
        return {
            "fio": self.fio,
            "birthdate": self.birthdate,
            "group": self.group,
            "gpa": self.gpa,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            fio=data["fio"],
            birthdate=data["birthdate"],
            group=data["group"],
            gpa=data["gpa"],
        )

    # @classmethod
    # def from_dict(data):
    #     return Student(
    #         fio=data["fio"],
    #         birthdate=data["birthdate"],
    #         group=data["group"],
    #         gpa=data["gpa"],
    #     )

    def __str__(self) -> str:
        return f"{self.fio} ({self.group}), {self.age()} лет, GPA {self.gpa:.2f}"
    

s1 = Student("a  a a", '2020-01-01', 'b', 5.0)
print(Student.__dict__)

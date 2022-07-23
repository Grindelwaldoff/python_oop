from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class InfoMessage():
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training():
    """Базовый класс тренировки."""
    HOUR_IN_MIN: int = 60  # константа для перевода часов в минуты
    LEN_STEP: float = 0.65  # константа: длина шага
    METERS_IN_KILOMETERS: int = 1000

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.METERS_IN_KILOMETERS

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Функция не переопределена,'
                                  'данный тип тренировки не поддерживается')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(str(self), self.duration,
                           self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    # коэфициенты необходимые для подсчета каллорий потраченных во время бега
    PHYSICAL_ACTIVITY_COEF: int = 18  # коэффициент физической активности
    CALORIE_COEF: int = 20  # еще один коэффициент физической активности

    def __str__(self):
        return 'Running'

    def get_spent_calories(self) -> float:
        res: float = (self.PHYSICAL_ACTIVITY_COEF * self.get_mean_speed()
                      - self.CALORIE_COEF)

        return (res * self.weight / self.METERS_IN_KILOMETERS
                * self.duration * self.HOUR_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    ACTIVITY_LEVEL_COEF: float = 0.035  # коэффициент физической активности
    TRAINING_COEF: float = 0.029  # еще один коэффициент физической активности

    def __str__(self):
        return 'SportsWalking'

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 height: int):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        part: float = self.get_mean_speed()**2 // self.height
        res = (self.ACTIVITY_LEVEL_COEF * self.weight + part
               * self.TRAINING_COEF * self.weight)
        return res * self.duration * self.HOUR_IN_MIN


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # константа: расстояние проходимое за один гребок

    def __str__(self):
        return 'Swimming'

    def __init__(self, action, duration, weight, length_pool: int,
                 count_pool: int, ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.METERS_IN_KILOMETERS

    def get_mean_speed(self) -> float:
        pool_par = self.length_pool * self.count_pool
        return pool_par / self.METERS_IN_KILOMETERS / self.duration

    def get_spent_calories(self) -> float:
        avg_speed = self.get_mean_speed()
        return (avg_speed + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: List[int]) -> Any:
    """Прочитать данные полученные от датчиков."""
    trainings_type: Dict[str, Any] = {  # поставить аннотацию Training вместо
                                        # Any не получается, выдает ошибку,
                                        # хотя код работает
        'SWM': Swimming,
        'WLK': SportsWalking,
        'RUN': Running
    }

    check = 0
    while check == 0:
        if workout_type in trainings_type and workout_type == 'SWM':
            check = 1
            return trainings_type[workout_type](*data)
        elif workout_type in trainings_type and workout_type == 'WLK':
            check = 1
            return trainings_type[workout_type](*data)
        elif workout_type in trainings_type and workout_type == 'RUN':
            check = 1
            return trainings_type[workout_type](*data)

        raise ValueError


def main(training: Training) -> None:
    """Главная функция."""
    res = training.show_training_info()
    print(res.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

from dataclasses import dataclass
from typing import Any, List


@dataclass
class TrainingParameters:
    action: int
    duration: int
    weight: int


@dataclass
class TrainingRes:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float


class InfoMessage(TrainingRes):
    """Информационное сообщение о тренировке."""
    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training(TrainingParameters):
    """Базовый класс тренировки."""
    HOUR_IN_MIN = 60
    LEN_STEP: float = 0.65  # константа: длина шага
    M_IN_KM = 1000
    training_type: str = ''

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> Any:
        """Получить количество затраченных калорий."""
        try:
            return self.get_spent_calories()
        except Exception:
            print('Подсчет каллорий для данного вида '
                  'тренировки пока недоступен.')
            return 0

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type, self.duration,
                           self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CONST_1: int = 18
    CONST_2: int = 20
    training_type = 'Running'

    def get_spent_calories(self) -> float:
        time = self.duration * self.HOUR_IN_MIN
        res: float = (self.CONST_1 * self.get_mean_speed() - self.CONST_2)

        return res * self.weight / self.M_IN_KM * time


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CONST_1: float = 0.035
    CONST_2: float = 0.029

    training_type = 'SportsWalking'

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 height: int):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:

        avg_speed: float = self.get_mean_speed()
        part: float = avg_speed**2 // self.height
        res: float = (self.CONST_1 * self.weight +
                      part * self.CONST_2 * self.weight)

        return res * self.duration * self.HOUR_IN_MIN


class Swimming(Training):
    """Тренировка: плавание."""
    training_type = 'Swimming'
    LEN_STEP: float = 1.38  # константа: расстояние проходимое за один гребок

    def __init__(self, action, duration, weight, length_pool: int,
                 count_pool: int, ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        pool_par = self.length_pool * self.count_pool
        return pool_par / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        avg_speed = self.get_mean_speed()
        return (avg_speed + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: List[int]) -> Any:
    """Прочитать данные полученные от датчиков."""
    action = data[0]
    duration = data[1]
    weight = data[2]

    trainings_type = {
        'SWM': Swimming(action, duration,
                        weight,
                        length_pool=data[-2],
                        count_pool=data[-1]),

        'WLK': SportsWalking(action,
                             duration,
                             weight,
                             height=data[-2]),

        'RUN': Running(action, duration, weight)
    }

    try:
        return trainings_type[workout_type]
    except Exception:
        return print('Данная тренировка пока не поддерживается.')


def main(training: Training) -> None:
    """Главная функция."""
    try:
        res = training.show_training_info()
        print(res.get_message())
    except Exception:
        print('')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

from __future__ import annotations


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:

        self.type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        res: str = (f'Тип тренировки: {self.type}; Длительность: '
                    f'{self.duration:.3f} ч.; Дистанция: {self.distance:.3f} '
                    f'км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал:'
                    f' {self.calories:.3f}.')
        return res


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    training_type: str = ''

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return self.get_spent_calories()

    def show_training_info(self):  # мне в проверке выдает ошибку: show_training_info() должен возвращать объект класса InfoMessage, когда я исправляю эту ошибку и запускаю проверку заново, оно говорит, что get_message должно возвращать str.... Вопрос как мне сделать так чтобы show_training_info() возвращала InfoMessage, обращаясь к get_message(), которая в свою очередь должна возвращать строку???
        """Вернуть информационное сообщение о выполненной тренировке."""
        mes = InfoMessage(self.training_type, self.duration,
                          self.get_distance(),
                          self.get_mean_speed(), self.get_spent_calories())

        return mes.get_message()


class Running(Training):
    """Тренировка: бег."""
    training_type = 'Running'

    def __init__(self, action, duration, weight) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        avg_speed: float = self.get_mean_speed()
        time = self.duration * 60
        M_IN_KM = 1000
        res: float = (coeff_calorie_1 * avg_speed - coeff_calorie_2)

        return res * self.weight / M_IN_KM * time

    def show_training_info(self) -> str:
        return super().show_training_info()


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type = 'SportsWalking'

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 height: int,):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_1: float = 0.035
        coeff_2: float = 0.029
        avg_speed: float = self.get_mean_speed()
        part: float = avg_speed**2 // self.height
        res: float = (coeff_1 * self.weight + part * coeff_2 * self.weight)

        return res * self.duration * 60

    def show_training_info(self) -> str:
        return super().show_training_info()


class Swimming(Training):
    """Тренировка: плавание."""
    training_type = 'Swimming'
    LEN_STEP = 1.38
    M_IN_KM = 1000

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

    def show_training_info(self) -> str:
        return super().show_training_info()


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    action = data[0]
    duration = data[1]
    weight = data[2]
    if workout_type == 'SWM':
        length_pool = data[3]
        count_pool = data[4]
        return Swimming(action, duration, weight, length_pool, count_pool)

    elif workout_type == 'WLK':
        height = data[3]
        return SportsWalking(action, duration, weight, height)

    return Running(action, duration, weight)


def main(training: Training) -> None:
    """Главная функция."""
    self = training.show_training_info()
    print(self)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

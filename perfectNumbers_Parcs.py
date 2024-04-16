from Pyro4 import expose
import random

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        numbers = self.read_input()

        # Розділяємо вхідний список чисел між доступними воркерами
        # Визначаємо розмір групи чисел для кожного воркера
        chunk_size = len(numbers) // len(self.workers)
        mapped = []
        for i, worker in enumerate(self.workers):
            group_start_index = i * chunk_size

            # Останній воркер "забирає" залишок чисел
            group_end_index = None if i == len(self.workers) - 1 else (i + 1) * chunk_size
            # Виконуємо пошук досконалих чисел в кожній групі й повертаємо список досконалих чисел погрупно
            mapped.append(worker.mymap(numbers[group_start_index:group_end_index]))

        # Збираємо результати з усіх воркерів
        perfect_numbers = []
        for future in mapped:   # 'future' - об'єкт Pyro4, що дозволяє викликати 'mymap' асинхронно
            perfect_numbers += future.value

        # Виводимо результати
        self.write_output([str(number) for number in perfect_numbers])

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(numbers):
        # Проходимось по кожному числу групи й повертаємо його якщо воно досконале
        return [number for number in numbers if Solver.is_perfect(number)]

    @staticmethod
    @expose
    def is_perfect(n):
        if n < 2:
            return False
        # Досконале число - число, яке є половиною суми всіх своїх додатних дільників, враховуючи себе
        divisors_sum = sum([i for i in range(1, n//2 + 1) if n % i == 0])
        return divisors_sum == n

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            numbers = [int(line.strip()) for line in f.readlines()]
        return numbers

    def write_output(self, perfect_numbers):
        with open(self.output_file_name, 'w') as f:
            for number in perfect_numbers:
                f.write(number + '\n')
        print("output done")
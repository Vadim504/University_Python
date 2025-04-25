import random
import json
from datetime import datetime
import os

class TestingSystem:
    def __init__(self):
        self.questions = []
        self.results = []
        self.current_test = None

    def load_questions(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split('|')
                    if len(parts) != 7:
                        print(f"Ошибка формата: {line}")
                        continue

                    self.questions.append({
                        'text': parts[0],
                        'options': parts[1:6],
                        'answer': int(parts[6])
                    })

            if not self.questions:
                print("Файл вопросов пуст или имеет неверный формат")
                return False

            print(f"Загружено {len(self.questions)} вопросов")
            return True

        except Exception as e:
            print(f"Ошибка загрузки вопросов: {e}")
            return False

    def shuffle_questions(self):
        random.shuffle(self.questions)
        for q in self.questions:
            correct = q['options'][q['answer'] - 1]
            random.shuffle(q['options'])
            q['answer'] = q['options'].index(correct) + 1

    def start_test(self):
        if not self.questions:
            print("Нет загруженных вопросов")
            return

        self.shuffle_questions()
        self.current_test = {
            'user': input("Введите ваше имя: "),
            'start_time': datetime.now(),
            'answers': [],
            'total': len(self.questions),
            'correct': 0
        }

        print(f"\nНачинаем тест! Всего вопросов: {self.current_test['total']}")
        print("Для ответа введите номер варианта (1-5) или 0 для пропуска\n")

        for i, q in enumerate(self.questions, 1):
            print(f"\nВопрос {i}/{self.current_test['total']}:")
            print(q['text'])

            for idx, opt in enumerate(q['options'], 1):
                print(f"{idx}. {opt}")

            while True:
                try:
                    answer = input("Ваш ответ (1-5): ").strip()
                    if answer == '0':
                        print("Вопрос пропущен")
                        self.current_test['answers'].append(None)
                        break

                    answer = int(answer)
                    if 1 <= answer <= 5:
                        is_correct = (answer == q['answer'])
                        if is_correct:
                            print("Правильно!")
                            self.current_test['correct'] += 1
                        else:
                            print(f"Неправильно! Правильный ответ: {q['answer']}")

                        self.current_test['answers'].append({
                            'question': q['text'],
                            'user_answer': answer,
                            'correct_answer': q['answer'],
                            'is_correct': is_correct
                        })
                        break
                    else:
                        print("Пожалуйста, введите число от 1 до 5")
                except ValueError:
                    print("Пожалуйста, введите число")

        self.current_test['end_time'] = datetime.now()
        self.show_results()
        self.save_results()

    def show_results(self):
        if not self.current_test:
            return

        score = (self.current_test['correct'] / self.current_test['total']) * 100
        duration = self.current_test['end_time'] - self.current_test['start_time']

        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
        print("=" * 50)
        print(f"Пользователь: {self.current_test['user']}")
        print(f"Время начала: {self.current_test['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Время окончания: {self.current_test['end_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Продолжительность: {duration}")
        print(f"Всего вопросов: {self.current_test['total']}")
        print(f"Правильных ответов: {self.current_test['correct']}")
        print(f"Процент правильных ответов: {score:.2f}%")
        print("=" * 50)

    def save_results(self):
        if not self.current_test:
            return

        score = (self.current_test['correct'] / self.current_test['total']) * 100
        duration = self.current_test['end_time'] - self.current_test['start_time']

        # Формируем строку с результатами для записи в файл
        result_text = (
            f"Результаты тестирования\n"
            f"=======================\n"
            f"Пользователь: {self.current_test['user']}\n"
            f"Время начала: {self.current_test['start_time'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Время окончания: {self.current_test['end_time'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Продолжительность: {duration}\n"
            f"Всего вопросов: {self.current_test['total']}\n"
            f"Правильных ответов: {self.current_test['correct']}\n"
            f"Процент правильных ответов: {score:.2f}%\n"
            f"=======================\n\n"
        )
        try:
            with open('.venv/results.txt', 'a', encoding='utf-8') as f:  # Открываем файл в режиме добавления ('a')
                f.write(result_text)
            print("\nРезультаты сохранены в файл: results.txt")
        except Exception as e:
            print(f"Ошибка сохранения результатов: {e}")
    def show_statistics(self):
        if not os.path.exists('test_results.json'):
            print("Нет сохраненных результатов")
            return

        try:
            with open('test_results.json', 'r', encoding='utf-8') as f:
                results = json.load(f)

            print("\n" + "=" * 50)
            print("СТАТИСТИКА ТЕСТИРОВАНИЯ")
            print("=" * 50)
            for r in results:
                print(f"\nПользователь: {r['user']}")
                print(f"Дата: {r['start_time']}")
                print(f"Результат: {r['correct_answers']}/{r['total_questions']} ({r['score']}%)")
                print("-" * 50)
        except Exception as e:
            print(f"Ошибка загрузки статистики: {e}")


def main():
    system = TestingSystem()

    if not os.path.exists('questions.txt'):
        print("Создаем шаблон файла questions.txt")
        with open('.venv/questions.txt', 'w', encoding='utf-8') as f:
            f.write("Какой язык программирования используется для веб-разработки?|Python|JavaScript|Java|C++|Ruby|2\n")
            f.write("Какая столица Франции?|Берлин|Лондон|Париж|Мадрид|Рим|3\n")
        print("Файл questions.txt создан. Добавьте свои вопросы в этом формате.")
        return

    if not system.load_questions('questions.txt'):
        return

    while True:
        print("\n" + "=" * 50)
        print(" СИСТЕМА ТЕСТИРОВАНИЯ")
        print("=" * 50)
        print("1. Начать тест")
        print("2. Показать статистику")
        print("3. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            system.start_test()
        elif choice == '2':
            system.show_statistics()
        elif choice == '3':
            break
        else:
            print("Некорректный ввод. Попробуйте еще раз.")

if __name__ == "__main__":
    main()
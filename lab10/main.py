import pyttsx3
from vosk import Model, KaldiRecognizer
import pyaudio
import requests
import json


hello_message = """Для выхода скажите 'Закрыть'"""
start_message = 'Система запущена. Говорите'
base_joke_text = 'Not set'
joke_error_message = 'Ошибка поиска шутки'
wrong_message = 'Нeправильная команда'
update_message = 'Обновляем шутку'
record_message = 'Шутка записана'


class Joke():
    def __init__(self, type=base_joke_text, category=base_joke_text, part_1=base_joke_text, part_2=None):
        self.type = type
        self.category = category
        self.text = ''
        if part_2 is not None:
            self.text = '- ' + part_1 + '\n- ' + part_2
        else:
            self.text = part_1


def talk(text, lang='ru'):
    if lang == 'ru':
        tts = pyttsx3.init()
        voices = tts.getProperty('voices')
        tts.setProperty('rate', 200)
        tts.setProperty('voice', voices[0].id)
        tts.say(text)
        tts.runAndWait()
    elif lang == 'en':
        tts_en = pyttsx3.init()
        voices = tts_en.getProperty('voices')
        tts_en.setProperty('rate', 150)
        tts_en.setProperty('voice', voices[1].id)
        tts_en.setProperty('voice', 'en-US')
        tts_en.say(text)
        tts_en.runAndWait()


def record_volume():
    data = stream.read(4000, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        return result.get("text", "")


def response(text, current_joke):
    match text:
        case 'создать':
            print(update_message)
            talk(update_message)
            data = get_data()
            if data['error']:
                print('Ошибка')
                talk(joke_error_message)
                return current_joke
            if data['type'] == 'single':
                new_joke = Joke('Монолог', data['category'], data['joke'])
            elif data['type'] == 'twopart':
                new_joke = Joke(
                    'Диалог', data['category'], data['setup'], data['delivery'])
            current_joke = new_joke
        case 'тип':
            print('Тип шутки: ' + current_joke.type)
            talk(current_joke.type)
        case 'прочесть':
            print(current_joke.text)
            talk(current_joke.text, 'en')
        case 'категория':
            print(current_joke.category)
            talk(current_joke.category, 'en')
        case 'записать':
            with open('jokes.txt', 'a') as f:
                f.write(current_joke.text + '\n')
                f.write('\n')
            print(record_message)
            talk(record_message)
        case _:
            print(wrong_message)
            talk(wrong_message)

    return current_joke


def get_data():
    url = 'https://v2.jokeapi.dev/joke/Any?safe-mode'
    response = requests.get(url)
    return json.loads(response.text)


model = Model('vosk-model-small-ru-0.22')
recognizer = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                input=True, frames_per_buffer=8000)
stream.start_stream()
print('\n' * 5)
print(hello_message)
print("""Доступные команды:
Создать - создает новую шутку
Тип - тип шутки
Прочесть - рассказать шутку
Категория - тематика шутки
Записать - запись в файл
      """)
talk(hello_message)
print(start_message)
talk(start_message)
current_joke = Joke()
while True:
    text = record_volume()
    if text == 'закрыть':
        print('Выход...')
        break
    if text is not None and len(text) > 0:
        # print(text, len(text))
        current_joke = response(text, current_joke)
stream.stop_stream()

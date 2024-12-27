import logging
import requests
import telebot

TELEGRAM_TOKEN = '8031939902:AAHZyXKVHCkdmrMTvWB6HkpY7LgATOy9liM'

# Список избранных городов
favorite_cities = []

bot = telebot.TeleBot(TELEGRAM_TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


city_translation = {
    "Москва": "Moscow",
    "Санкт-Петербург": "Saint Petersburg",
    "Новосибирск": "Novosibirsk",
    "Екатеринбург": "Yekaterinburg",
    "Нижний Новгород": "Nizhny Novgorod",
    "Казань": "Kazan",
    "Челябинск": "Chelyabinsk",
    "Омск": "Omsk",
    "Самара": "Samara",
    "Ростов-на-Дону": "Rostov-on-Don",
}

# Получение списка городов России из словаря city_translation
def get_cities_in_russia():
    return list(city_translation.keys())

# Получение информации о конкретном городе
def get_city_info(city_name):
    city_name_english = translate_city_name(city_name)

    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    querystring = {"namePrefix": city_name_english, "countryIds": "RU", "limit": "1"}
    
    headers = {
        "X-RapidAPI-Key": "91501e0d93msh70e9063638f467cp114b89jsn4aa0f7d8a2fb",
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            city = data['data'][0]
            return f"Город: {city['city']}\nСтрана: {city['country']}\nШирота: {city['latitude']}\nДолгота: {city['longitude']}\nНаселение: {city['population']}"
        else:
            return "Город не найден."
    else:
        return "Ошибка при получении информации о городе."

# Функция перевода города на английский
def translate_city_name(city_name):
    return city_translation.get(city_name, city_name)

# Добавление города в избранное
def add_to_favorites(city_name):
    if city_name not in favorite_cities:
        favorite_cities.append(city_name)
        return f"Город {city_name} добавлен в избранное!"
    else:
        return f"Город {city_name} уже в избранном."

# Вывод списка избранных городов
def show_favorites():
    if favorite_cities:
        return "\n".join(favorite_cities)
    else:
        return "Ваш список избранных городов пуст."

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я помогу тебе с городами России. Используй следующие команды:\n"
                                      "/cities - список городов России\n"
                                      "/info <город> - информация о городе\n"
                                      "/add_favorite <город> - добавить город в избранное\n"
                                      "/favorites - список избранных городов")

# Обработчик команды /cities
@bot.message_handler(commands=['cities'])
def cities(message):
    cities = get_cities_in_russia()
    if cities:
        bot.send_message(message.chat.id, "\n".join(cities))
    else:
        bot.send_message(message.chat.id, "Города не найдены.")

# Обработчик команды /info <город>
@bot.message_handler(commands=['info'])
def city_info(message):
    city_name = message.text[6:].strip()
    if city_name:
        info = get_city_info(city_name)
        bot.send_message(message.chat.id, info)
    else:
        bot.send_message(message.chat.id, "Укажите название города после команды /info.")

# Обработчик команды /add_favorite <город>
@bot.message_handler(commands=['add_favorite'])
def add_favorite(message):
    city_name = message.text[14:].strip()
    if city_name:
        result = add_to_favorites(city_name)
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, "Укажите название города после команды /add_favorite.")

# Обработчик команды /favorites
@bot.message_handler(commands=['favorites'])
def favorites(message):
    result = show_favorites()
    bot.send_message(message.chat.id, result)

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Я вас не понял. Пожалуйста, используйте доступные команды.")

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)


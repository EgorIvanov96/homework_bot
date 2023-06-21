import telegram
import sys
import logging
import os
import requests
import time
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(message)s'
)
handler.setFormatter(formatter)

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

homework_statuses = {}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверяем доступность переменных окружения."""
    variables = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
    logging.critical('Нет одного из ключей доступа')
    return all(variables)


def send_message(bot, message):
    """Отправляем сообщение в Телеграм."""
    try:
        logger.debug('Сообщение отправлено')
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as error:
        logger.error(f'Сообщение не отправлено. Ошибка {error}')


def get_api_answer(timestamp):
    """Делаем запрос к единственному эндпоинту API-сервиса."""
    payload = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    except Exception:
        logging.exception('Ошибка при запросе')
    if response.status_code != 200:
        raise KeyError(
            f'Ошибка! Код ошибки:{response.status_code}'
        )
    return response.json()


def check_response(response):
    """Проверка ответа API."""
    try:
        response = response['homeworks']
    except KeyError:
        raise KeyError('Не хватает ключа')
    if type(response) != list:
        raise TypeError('Данные не в виде списка')
    return True


def parse_status(homework):
    """Статус финального проекта."""
    sections = ['status', 'homework_name']

    for section in sections:
        if section not in homework:
            logger.error(f'Отсутствуют данные {section}')
            raise KeyError(f'Отсутствуют данные {section}')

    hm_status = homework['status']
    homework_name = homework['homework_name']
    homework_statuses[homework_name] = hm_status
    if hm_status not in HOMEWORK_VERDICTS:
        logger.debug('Финальный проект не проверен')
        raise KeyError('Статус проверкт финального')
    verdict = HOMEWORK_VERDICTS[hm_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    logging.basicConfig(
        level=logging.DEBUG,
        filename='main.log',
        filemode='w',
        format='%(asctime)s, %(levelname)s, %(message)s'
    )

    if check_tokens():
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
    else:
        return ValueError('Отсутствуют данные')

    while True:
        try:
            timestamp = int(time.time())
            response = get_api_answer(timestamp)
            # print(response)
            check_response(response)
            if len(response['homeworks']) != 0:
                check_response(response)
                message = parse_status(response['homeworks'][0])
                send_message(bot, message)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()

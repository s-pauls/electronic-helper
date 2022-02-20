"""
Новое уведомление: Viber
Заголовок: Благодать (Гомель)s
Текст: Анастасия: Приветствую дорогая церковь. Прошу молитвенной поддержки...
...
Много строк
"""


class RemoteBotDefaultTemplateParser:
    def __init__(self, text: str):
        self._text: str = text

    def get_caption(self) -> str:
        for line in self._text.splitlines():
            if line.startswith('Заголовок:'):
                return line.replace('Заголовок: ', '')
        return ''

    def get_sender_name(self) -> str:
        for line in self._text.splitlines():
            if line.startswith('Текст:'):
                arr = line.split(': ')
                if len(arr) >= 2:
                    return arr[1]
        return ''

    def get_message_text(self) -> str:
        _text: str = ''
        _text_started: bool = False
        for line in self._text.splitlines():

            # если нашлась строка, которая начинается на 'Текст:'
            # мы уже на следующей строке
            # добавляем все последующие строки
            if _text_started:
                _text = _text + '\r\n' + line

            # ищем первую строку, которая начинается на 'Текст:'
            if not _text_started and line.startswith('Текст:'):
                _text_started = True
                arr = line.split(': ')
                if len(arr) > 2:
                    _text = arr[2]

        return _text

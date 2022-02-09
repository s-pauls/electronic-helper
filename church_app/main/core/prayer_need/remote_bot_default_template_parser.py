"""
Новое уведомление: Viber
Заголовок: Благодать (Гомель)s
Текст: Анастасия: Приветствую дорогая церковь.прошу молитвенной поддержки...
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
        for line in self._text.splitlines():
            if line.startswith('Текст:'):
                arr = line.split(': ')
                if len(arr) > 2:
                    return arr[2]
        return ''

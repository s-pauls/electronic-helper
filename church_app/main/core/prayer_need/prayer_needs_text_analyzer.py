KEY_WORDS = 'молитве,молиться,молится,молитва,помолитесь,помолитесь за,молитвенной поддержки'


class PrayerNeedsTextAnalyzer:
    def __init__(self, text):
        self._text = text

    def is_pray_need(self) -> bool:
        lowered_text = self._text.lower()
        key_words_array = KEY_WORDS.split(',')

        for key_word in key_words_array:
            if key_word in lowered_text:
                return True

        return False

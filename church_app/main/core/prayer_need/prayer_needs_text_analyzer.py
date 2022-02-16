# KEY_WORDS = 'молитве,молиться,молится,молитва,молитвы,помолитесь,помолись,молитвенной поддержки'
KEY_WORDS = 'молит,помолись,маліт,малит'
# молит - русский и украинский вариант
# маліт - белорусский вариант
# малит - неграмотный вариант


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

"""Let's learn Python"""
import string

class StrManipulator(object):
    """First Class"""

    def process_string(self, unsan_str):
        """Process string into useful list"""
        table = str.maketrans({key: None for key in string.punctuation})
        return unsan_str.translate(table).lower().split()

    def char2num(self, char):
        """Given char into encoded number string"""
        if isinstance(char, str) and len(char) == 1:
            if ord(char)-97 < 10:
                return '0' + str(ord(char)-97)
            else:
                return str(ord(char)-97)

    def str2num(self, word):
        """Given string into encoded number string"""
        enc_str = ""
        i = 0
        while i < len(word):
            enc_str += self.char2num(word[i])
            i += 1
        return enc_str

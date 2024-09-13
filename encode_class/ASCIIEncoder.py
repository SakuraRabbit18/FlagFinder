#from BaseEncoder import BaseEncoder
from encode_class import BaseEncoder
import re

class ASCIIEncoderDecimal(BaseEncoder):
    def __init__(self):
        super().__init__()
        self.name = 'ascii_decimal'
        self.description = 'ascii编码十进制编码器，尝试识别类似102 108 97 103格式的编码并尝试解码'

    def encode(self):
        return ' '.join(str(ord(c)) for c in self.text)
    
    def decode(self, text):
        try:
            return ''.join(chr(int(c)) for c in text.split())
        except:
            return None
    
    def generate_regex(self):
        return re.escape(self.encode_text) + r'\ \d+(?:\s+\d+)*'
    
    
if __name__ == '__main__':
    encoder = ASCIIEncoderDecimal()
    encoder.set_text('flag')
    print(encoder.encode_text)
    print(encoder.re)
    s = "102 108 97 103 123 49 50 51 125"
    pattern = re.compile(encoder.re,re.IGNORECASE)
    result = pattern.finditer(s)
    for match in result:
        print(match.group())
        print(encoder.decode(match.group()))
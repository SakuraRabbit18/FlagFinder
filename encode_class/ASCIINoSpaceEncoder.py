#from BaseEncoder import BaseEncoder
from encode_class import BaseEncoder
import re

class ASCIINoSpaceEncoder(BaseEncoder):
    def __init__(self):
        super().__init__()
        self.name = 'ascii_no_space'
        self.description = 'ascii编码编码器，尝试识别类似10210897103123495051125格式的编码并尝试解码'
    
    def encode(self):
        return ''.join(str(ord(c)) for c in self.text)
    
    def decode(self, text):
        try:
            return ''.join(chr(int(text[i:i+3])) for i in range(0, len(text), 3))
        except:
            return None
    
    def generate_regex(self):
        return re.escape(self.encode_text) + r'\d+'
    
if __name__ == '__main__':
    encoder = ASCIINoSpaceEncoder()
    encoder.set_text('flag')
    print(encoder.encode_text)
    print(encoder.re)
    s = "10210897103123495051125"
    pattern = re.compile(encoder.re,re.IGNORECASE)
    result = pattern.finditer(s)
    for match in result:
        print(match.group())
        print(encoder.decode(match.group()))
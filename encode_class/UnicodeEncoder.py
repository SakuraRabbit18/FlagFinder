from encode_class import BaseEncoder
import re
#from BaseEncoder import BaseEncoder

class UnicodeEncoder(BaseEncoder):
    def __init__(self):
        super().__init__()
        self.name = 'unicode'
        self.description = 'unicode编码编码器，尝试识别类似\\u0066\\u006c\\u0061\\u0067格式的编码并尝试解码'
    
    def encode(self):
        return ''.join([f'\\u{ord(c):04x}' for c in self.text])
    
    def decode(self, text):
        try:
            return text.encode('utf-8').decode('unicode_escape')
        except:
            return None
    
    def generate_regex(self):
        return re.escape(self.encode_text) + r'(?:\\u[0-9A-Fa-f]{4})+'
    
    
    
if __name__ == '__main__':
    encoder = UnicodeEncoder()
    encoder.set_text('flag')
    print(encoder.re)
    s = "hhhha\\u0066\\u006c\\u0061\\u0067\\u007b\\u0031\\u0032\\u0033\\u007djhkjjh"
    pattern = re.compile(encoder.re,re.IGNORECASE)
    result = pattern.finditer(s)
    for match in result:
        print(match.group())
        print(encoder.decode(match.group()))
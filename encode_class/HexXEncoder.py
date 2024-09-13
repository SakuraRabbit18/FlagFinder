#from BaseEncoder import BaseEncoder
from encode_class import BaseEncoder
import re

class HexEncoder(BaseEncoder):
    def __init__(self):
        super().__init__()
        self.name = 'hex_x'
        self.description = 'hex编码编码器，尝试识别类似\\x66\\x6c\\x61\\x67格式的编码并尝试解码'
    
    def encode(self):
        return ''.join([f'\\x{c:02x}' for c in self.text.encode('utf-8')])
    
    def decode(self, text):
        try:
            return bytes.fromhex(text.replace('\\x', '')).decode('utf-8')
        except:
            return None
    
    def generate_regex(self):
        return re.escape(self.encode_text) + r'(\\x[0-9a-fA-F]{2})+'

    
if __name__ == '__main__':
    encoder = HexEncoder()
    encoder.set_text('flag')
    print(encoder.re)
    s = "23123kkkkljiojoijknolkn\\x66\\x6c\\x61\\x67\\x7b\\x37\\x46\\x6f\\x4d\\x32\\x53\\x74\\x6b\\x68\\x65\\x50\\x7a\\x7deRQRWEWQ"
    pattern = re.compile(encoder.re,re.IGNORECASE)
    result = pattern.finditer(s)
    for match in result:
        print(match.group())
        print(encoder.decode(match.group()))
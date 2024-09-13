from encode_class import BaseEncoder

#from BaseEncoder import BaseEncoder
import base64
import re

class Base64Encoder(BaseEncoder):
    def __init__(self):
        super().__init__()
        self.name = 'base64'
        self.description = 'Base64编码编码器，尝试识别类似ZmxhZ3sxMjM0fQ==的编码并尝试解码'
    
    def encode(self):
        return base64.b64encode(self.text.encode('utf-8')).decode('utf-8')
    
    def decode(self, text):
        try:
            return base64.b64decode(text).decode('utf-8')
        except:
            return None
    
    def generate_regex(self):
        return re.escape(self.encode_text[:4]) + r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?' 
    
if __name__ == '__main__':
    encoder = Base64Encoder()
    encoder.set_text('flag')
    print(encoder.encode_text)
    print(encoder.re)
    s = "ZmxhZ3sxMjM0fQ=="
    pattern = re.compile(encoder.re,re.IGNORECASE)
    result = pattern.finditer(s)
    for match in result:
        print(match.group())
        print(encoder.decode(match.group()))
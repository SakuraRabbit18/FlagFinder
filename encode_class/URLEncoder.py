import re
from encode_class import BaseEncoder
import urllib.parse

class URLEncoder(BaseEncoder):
    def __init__(self):
        super().__init__()
        self.name = 'url'
        self.description = "url编码编码器，尝试识别类似flag%7B123%7D格式的编码并尝试解码"
        
    def encode(self):
        return urllib.parse.quote(self.text)
    
    def decode(self, text):
        try:
            return urllib.parse.unquote(text)
        except:
            return None
    
    def generate_regex(self):
        return re.escape(self.encode_text) + r'(?:%[0-9A-Fa-f]{2})+'
from encode_class import BaseEncoder
import re
#from BaseEncoder import BaseEncoder


class UnicodeEncoderHtmlEntity(BaseEncoder):
    def __init__(self):
        super().__init__()
        self.name = 'unicode_html_entity'
        self.description = 'Unicode的HTML实体编码格式编码器，尝试识别类似&#102;&#49;&#97;&#103;格式的编码并尝试解码'
    
    def encode(self):
        return ''.join([f'&#{ord(c)};' for c in self.text])
    
    def decode(self, text):
        try:
            return re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)
        except:
            return None
    
    def generate_regex(self):
        return re.escape(self.encode_text) + r'(?:&#\d+;)+'

if __name__ == '__main__':
    encoder = UnicodeEncoderHtmlEntity()
    encoder.set_text('f')
    print(encoder.re)
    s = "hhhha&#102;&#108;&#97;&#103;&#123;&#49;&#50;&#51;&#125;jhkjjh"
    pattern = re.compile(encoder.re,re.IGNORECASE)
    result = pattern.finditer(s)
    for match in result:
        print(match.group())
        print(encoder.decode(match.group()))
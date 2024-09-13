import re
from encode_class import BaseEncoder


class HexEncoder(BaseEncoder):
    def __init__(self):
        super().__init__()
        self.name = 'hex'  
        self.description = 'hex编码编码器，尝试识别类似666c6167格式的编码并尝试解码'

    def encode(self):
        return self.text.encode('utf-8').hex()

    def decode(self,text):
        try:
            return bytes.fromhex(text).decode('utf-8')
        except:
            return None
    
    def generate_regex(self):
        # 生成匹配编码文本开头的正则表达式
        # 取编码后文本的前8个字符（或更少）
        hex_prefix = self.encode_text[:min(len(self.encode_text), 8)] 
        return r'' + re.escape(hex_prefix) + r'[0-9a-fA-F]*'


if __name__ == '__main__':
    str = "-1%27+union+select+0x3C3F70687020247374723D2255563C4F424C3E4C42483C5452473E4755523C53594E543E223B206563686F2822666C61677B222E7374725F726F7431332824737472292E227D22293B3F3E,2+into+outfile+%27/var/www/html/822666C61677B222E7374725F726F74313328247374.php%27--+&Submit=Submit HTTP/1.1"
    encoder = HexEncoder()
    encoder.set_text("flag")
    pattern = re.compile(encoder.re,re.IGNORECASE)
    print(encoder.re)
    result = pattern.findall(str)[0]
    if result:
        print(encoder.decode(result))
    else:
        print("No match found")

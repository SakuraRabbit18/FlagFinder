from encode_class import BaseEncoder
#from BaseEncoder import BaseEncoder
import re

class ASCIIEncoderBin(BaseEncoder):
    def __init__(self):
        super().__init__()
        self.name = 'ascii_binary'
        self.description = 'ASCII编码二进制编码器，尝试识别类似01100110 01101100 01100001 01100111格式的编码并尝试解码'

    def encode(self):
        return ' '.join(format(ord(c), '08b') for c in self.text)
    
    def decode(self, text):
        try:
            binary_values = text.split()
            return ''.join(chr(int(value, 2)) for value in binary_values)
        except:
            return None
    
    def generate_regex(self):
        # 匹配8位二进制数字的模式，可以重复多次，用空格分隔
        return re.escape(self.encode_text) + r' \d+(?:\s+\d+)*'
    
if __name__ == '__main__':
    encoder = ASCIIEncoderBin()
    encoder.set_text('flag')
    print("Encoded text:", encoder.encode_text)
    print("Regex pattern:", encoder.re)
    
    # 测试样例
    s = "01100110 01101100 01100001 01100111 01111011 00110001 00110010 00110011 01111101"
    pattern = re.compile(encoder.re, re.IGNORECASE)
    result = pattern.finditer(s)
    for match in result:
        print("Matched:", match.group())
        print("Decoded:", encoder.decode(match.group()))
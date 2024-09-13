from encode_class import BaseEncoder
#from BaseEncoder import BaseEncoder
import re

class ASCIIEncoderBinaryNoSpace(BaseEncoder):
    def __init__(self):
        super().__init__()
        self.name = 'ascii_binary_no_space'
        self.description = 'ASCII编码二进制无空格编码器，尝试识别类似01100110011011000110000101100111格式的编码并尝试解码'

    def encode(self):
        return ''.join(format(ord(c), '08b') for c in self.text)
    
    def decode(self, text):
        try:
            return ''.join(chr(int(text[i:i+8], 2)) for i in range(0, len(text), 8))
        except:
            return None
    
    def generate_regex(self):
        # 匹配连续的8位二进制数字模式，总长度必须是8的倍数
        return re.escape(self.encode_text) + r'[01]{8}(?:[01]{8})*'
    
if __name__ == '__main__':
    encoder = ASCIIEncoderBinaryNoSpace()
    encoder.set_text('flag')
    print("Encoded text:", encoder.encode_text)
    print("Regex pattern:", encoder.re)
    
    # 测试样例
    s="011001100110110001100001011001110111101100110001001100100011001101111101"
    pattern = re.compile(encoder.re, re.IGNORECASE)

    result = pattern.finditer(s)
    for match in result:
        print("Matched:", match.group())
        print("Decoded:", encoder.decode(match.group()))
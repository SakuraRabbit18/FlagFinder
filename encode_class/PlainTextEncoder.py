from encode_class import BaseEncoder
#from BaseEncoder import BaseEncoder
import re

class PlainTextEncoder(BaseEncoder):
    def __init__(self):
        super().__init__()
        self.name = 'plain_text'
        self.description = '明文编码器，用于直接匹配未编码的文本'

    def encode(self):
        return self.text

    def decode(self, text):
        return text
    
    def generate_regex(self):
        # 匹配以指定文本开头，后跟任意字符（非贪婪），以}结尾
        return re.escape(self.text) + r'\{.*?\}'+ '|' + re.escape(self.text)

if __name__ == '__main__':
    encoder = PlainTextEncoder()
    encoder.set_text('flag')
    print("Encoded text:", encoder.encode_text)
    print("Regex pattern:", encoder.re)

    # 测试样例
    s = "This is a test flag{123} and another FLAG{456} here. Also testflag{789}test and flag{abc}. flag{} flag{test}flag"
    pattern = re.compile(encoder.re, re.IGNORECASE)
    result = pattern.finditer(s)
    for match in result:
        print("Matched:", match.group())
        print("Decoded:", encoder.decode(match.group()))

    # 测试不同的文本
    test_texts = ['flag', 'FLAG', 'test', 'key']
    for test in test_texts:
        encoder.set_text(test)
        print(f"\nTesting '{test}':")
        print("Regex pattern:", encoder.re)
        result = re.finditer(encoder.re, s, re.IGNORECASE)
        for match in result:
            print("Matched:", match.group())
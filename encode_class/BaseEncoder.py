class BaseEncoder:
    def __init__(self):
        self.text = ''
        self.name = 'base'
        self.description = '无描述'
    
    def set_text(self, text):
        self.text = text
        self.encode_text = self.encode()
        self.re = self.generate_regex()
        
    def encode(self):
        pass
    
    def decode(self, text):
        pass
    
    def generate_regex(self):
        pass
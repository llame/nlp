#逆向最大匹配
class IMM(object):
    def __init__(self,dic_path):
        self.dictionary=set()
        self.maximum=0

        #读取词典
        with open(dic_path,'r',encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                self.dictionary.add(line)
                if len(line)>self.maximum:
                    self.maximum=len(line)

    def cut(self,text):
        result=[]
        index=len(text)
        while index>0:
            word=None
            for size in range(self.maximum,0,-1):
                if index-size<0:
                    continue
                piece=text[(index-size):index]
                if piece in self.dictionary:
                    word=piece
                    result.append(word)
                    index=index-size
                    break
            ##如果词典中，不包含该词
            if word  is None:
                    result.append(text[(index-1):index])
                    index=index-1
        return result[::-1]

def main():
    text='南京市长江大桥'
    tokenizer=IMM('data/1-imm_dic.utf8')
    result=tokenizer.cut(text)
    print(result)




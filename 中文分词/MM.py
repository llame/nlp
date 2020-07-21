# 逆向最大匹配
class MM(object):
    def __init__(self, dic_path):
        self.dictionary = set()
        self.maximum = 0

        # 读取词典
        with open(dic_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.dictionary.add(line)
                if len(line) > self.maximum:
                    self.maximum = len(line)

    def cut(self, text):
        result = []
        index = 0
        while index < len(text):
            word = None
            for size in range(self.maximum, 0, -1):
                if index + size > len(text):
                    continue
                piece = text[index:(index + size)]
                if piece in self.dictionary:
                    word = piece
                    result.append(word)
                    index = index + size
                    break
            # 如果词典中，不包含该词
            if word is None:
                result.append(text[index:(index + 1)])
                index = index + 1
        return result

#（正向最大匹配）算法
if __name__ == "__main__":
    text = '南京市长江大桥'
    tokenizer = MM('data/1-imm_dic.utf8')
    result = tokenizer.cut(text)
    print(result)

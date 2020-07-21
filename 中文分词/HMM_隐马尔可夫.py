class HMM(object):
    def __init__(self):
        import os

        # 主要是用于存取算法中间结果，不用每次训练模型
        self.model_file = 'data/2-hmm_model.pkl'

        # 状态集合
        self.state_list = ['B', 'M', 'E', 'S']
        self.load_para = False
        pass
    # 用于加载已计算的中间结果，当需要重新训练时，需要初始化清空结果

    def try_load_model(self, trained):
        if trained:
            import pickle
            with open(self.model_file, 'rb') as f:
                self.A_dic = pickle.load(f)
                self.B_dic = pickle(f)
                self.Pi_dic = pickle(f)
                self.load_para = True

        else:
            # 状态转移概率（状态-》状态的条件概率）
            self.A_dic = {}
            # 发射概率（状态-》词语的条件概率）
            self.B_dic = {}
            # 状态的初始概率
            self.Pi_dic = {}
            self.load_para = False

    # 计算转移概率、发射概率以及初始概率
    def train(self, path):

        # 重置概率举证
        self.try_load_model(False)

        # 统计状态出现的次数，求p（0）
        Count_dic = {}

        # 初始化参数
        def init_parameters():
            for state in self.state_list:
                self.A_dic[state] = {s: 0.0 for s in self.state_list}
                self.Pi_dic[state] = 0.0
                self.B_dic[state] = {}
                Count_dic[state] = 0

        def make_label(text):
            out_text = []
            if len(text) == 1:
                out_text.append('S')
            else:
                out_text += ['B'] + ['M'] * (len(text) - 2) + ['E']
            return out_text

        init_parameters()
        line_num = -1

        # 观察者集合，主要是字及标点等
        words = set()
        with open(path, encoding='utf-8') as f:
            for line in f:
                line_num += 1

                line = line.strip()
                if not line:
                    continue

                word_list = [i for i in line if i != ' ']
                words |= set(word_list)  # 更新字的集合

                linelist = line.split()

                line_state = []
                for w in linelist:
                    line_state.extend(make_label(w))
                print(len(word_list))
                print(len(line_state))
                assert len(word_list) == len(line_state)

                for k, v in enumerate(line_state):
                    Count_dic[v] += 1
                    if k == 0:
                        self.Pi_dic[v] += 1
                    else:
                        self.A_dic[line_state[k - 1]][v] += 1  # 计算转移概率
                        self.B_dic[line_state[k]][word_list[k]] = self.B_dic[line_state[k]].get(word_list[k], 0) + 1  # 计算发射概率

        self.Pi_dic = {k: v * 1.0 / line_num for k, v in self.Pi_dic.items()}
        self.A_dic = {k: {k1: v1 / Count_dic[k]for k1, v1 in v.items()} for k, v in self.A_dic.items()}

        # 加1平滑
        self.B_dic = {k: {k1: (v1 + 1) / Count_dic[k] for k1, v1 in v.items()} for k, v in self.B_dic.items()}

        import pickle
        # pickle.dump(self.A_dic,f)
        # pickle.dump(self.B_dic,f)
        # pickle.dump(self.Pi_dic,f)
        return self

    def viterbi(self, text, states, start_p, trans_p, emit_p):
        v = [{}]
        path = {}
        for y in states:
            v[0][y] = start_p[y] * emit_p[y].get(text[0], 0)
            path[y] = [y]
        for t in range(1, len(text)):
            v.append({})
            newpath = {}

            # 检验训练的发射概率矩阵中是否有该字
            neverSeen = text[t] not in emit_p['S'].keys() and  \
                text[t] not in emit_p['M'].keys() and  \
                text[t] not in emit_p['B'].keys() and  \
                text[t] not in emit_p['E'].keys()

            for y in states:
                emitp = emit_p[y].get(text[t], 0) if not neverSeen else 1.0  # 设置未知单独成词
                (prob, state) = max([(v[t - 1][y0] * trans_p[y0].get(y, 0) * emitp, y0) for y0 in states if v[t - 1][y0] > 0])
                v[t][y] = prob
                newpath[y] = path[state] + [y]

            path = newpath

        if emit_p['M'].get(text[-1], 0) > emit_p['S'].get(text[-1], 0):
            (prob, state) = max([(v[len(text) - 1][y], y) for y in ('E', 'M')])
        else:
            (prob, state) = max([(v[len(text) - 1][y], y) for y in states])

        return (prob, path[state])

    def cut(self, text):

        prob, pos_list = self.viterbi(text, self.state_list, self.Pi_dic, self.A_dic, self.B_dic)
        print(str(pos_list))
        begin, next = 0, 0
        for i, char in enumerate(text):
            pos = pos_list[i]
            if pos == 'B':
                begin = i
            elif pos == 'E':
                yield text[begin:i + 1]
                next = i + 1
            elif pos == 'S':
                yield char
                next = i + 1
        if next < len(text):
            yield text[next:]

#隐马尔可夫
if __name__ == '__main__':
    hmm = HMM()
    hmm.train('data/3-trainCorpus.txt_utf8')
    text = '一名青年安静地坐在窗台上,隔着窗户玻璃看着屋内'
    res = hmm.cut(text)
    print(str(list(res)))

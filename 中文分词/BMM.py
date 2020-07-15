from 中文分词 import IMM
from 中文分词 import MM

##双向最大匹配(将选取词数切分最小)
if __name__=='__main__':
    text = '南京市长江大桥'
    path_dic='data/1-imm_dic.utf8'

    tokenizer_IMM = IMM.IMM(path_dic)
    tokenizer_MM=MM.MM(path_dic)

    ##逆向最大分词
    result_IMM=tokenizer_IMM.cut(text)

    ##正向最大分词
    result_MM=tokenizer_MM.cut(text)

    if len(result_IMM)>len(result_MM):
        print('双向分词结果：'+str(result_MM))
    elif  len(result_IMM)==len(result_MM):
        print('双向分词结果：' + str(result_MM)+' 或 '+str(result_IMM))
    else:
        print('双向分词结果：' + str(result_IMM))



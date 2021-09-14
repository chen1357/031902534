import sys
import string
from pypinyin import lazy_pinyin 

class chinese:
    def __init__(self, word):
        self.word=word
        self.count=0#出现次数
        self.length=len(word)#长度
        self.pinyin=lazy_pinyin(word)#拼音
        self.pinyinLen=[]
        for pinyin in self.pinyin:
            self.pinyinLen.append(len(pinyin))
    def check(self,wd):
        text=""
        str="".join(lazy_pinyin(wd[0]))
        if str[0] == self.pinyin[0][0] or wd[0].lower()== self.pinyin[0][0] :
            i=0
            j=0
            while(j<len(wd)):
                if i == self.length:
                    break
                str1 = "".join(lazy_pinyin(wd[j]))
                if wd[j].lower() == self.pinyin[i][0] or str1 == self.pinyin[i] :
                    text+=wd[j]
                    i+=1
                elif j+self.pinyinLen[i]<=len(wd) and (wd[j:j+self.pinyinLen[i]]).lower()==self.pinyin[i]:
                    text+=wd[j:j+self.pinyinLen[i]]
                    j=j+self.pinyinLen[i]-1
                    i+=1
                elif wd[j].lower() ==self.pinyin[i][0]:
                    text+=wd[j]
                    i+=1
                elif wd[j] in string.digits+string.ascii_letters+"[\n`~!@#$%^&*()+-_=|{}':;',\\[\\].<>/?~！\"@#￥%……&*()——+|{}【】‘；：”“’。， 、？]":
                    text+=wd[j]
                else:
                    break
                j+=1
            if i==self.length :
                self.count+=1
                return text
        return "0"

class english:
    def __init__(self, word):
        self.word=word
        self.count=0#出现次数
        self.length=len(word)#长度
    def check(self,wd):
        text=""
        i=0
        if wd[0].lower() == self.word[0].lower():
            i=1
            text+=wd[0]
            for j in range(1,len(wd)):
                if i == self.length:
                    break
                if wd[j].lower() == self.word[i].lower():
                    text+=wd[j]
                    i+=1
                elif wd[j] in string.digits+"[\n`~!@#$%^&*()+=|{}':;',\\[\\].<>/?~！@#￥%……&*()——+|{}【】\"‘；：”“’。， 、？]":
                    text+=wd[j]
                else:
                    break
            if i==self.length:
                return text
        return "0"

           









#文件地址读取
wordsAddress=(sys.argv[1])#命令行传敏感词文件地址
fileAddress=(sys.argv[2])#文件地址
answerAddress=(sys.argv[3])#答案文件地址









#敏感词读取
wordsFile=open(wordsAddress,'r',encoding='utf-8')#打开文件
chiWords=[]#敏感词列表
engWords=[]
for line in wordsFile.readlines():#读取敏感词
    line=line.strip()
    if line[0] in string.ascii_letters:
        engWords.append(english(line))
    else:
        chiWords.append(chinese(line))
wordsFile.close()#关闭文件



#文本检测
file=open(fileAddress,'r',encoding='utf-8')#打开文件
lineCount=0
result=[]
totalCount=0#敏感词个数
for line in file.readlines():#读取每行
    lineCount+=1
    line=line.strip()
    i=0
    while(i<len(line)):
        for wd in engWords:
            text=wd.check(line[i:])
            if text!="0":
                totalCount+=1
                result.append("Line{}: <{}> {}".format(lineCount,wd.word,text))
                i+=wd.length-1
                break
        for wd in chiWords:
            text=wd.check(line[i:])
            if text!="0":
                totalCount+=1
                result.append("Line{}: <{}> {}".format(lineCount,wd.word,text))
                i+=wd.length-1
                break
        i+=1
file.close()

#写入文件
with open(answerAddress,'w',encoding='utf-8') as answer:
    answer.write("Total: {} ".format(totalCount)+'\n')
    answer.write('\n'.join(result))

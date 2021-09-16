import sys
import string
from pypinyin import lazy_pinyin 
import seperation

class chinese:
    def __init__(self, word):
        self.word=word
        self.length=len(word)#长度
        self.pinyin=lazy_pinyin(word)#拼音
        self.pinyinLen=[]#拼音长度
        self.seperation=[]
        for pinyin in self.pinyin:
            self.pinyinLen.append(len(pinyin))
        for w in word:
            s=seperation.seperate(w)
            if s !="0":
                self.seperation.append(s)
            else:
                self.seperation.append("")
    def testing(self,wd):
        text=""
        str="".join(lazy_pinyin(wd[0]))
        if str[0] == self.pinyin[0][0] or wd[0].lower()== self.pinyin[0][0] or wd[0]==self.seperation[0][0]:
            i=0
            j=0
            insert=0
            while(j<len(wd)):
                if i == self.length or insert > 20 :
                    break
                str1 = "".join(lazy_pinyin(wd[j]))
                if j+2 <=len(wd) and wd[j:j+2]==self.seperation[i]:#拆字
                    text+=wd[j:j+2]
                    j+=1
                    i+=1
                    insert=0
                elif str1 == self.pinyin[i] :#同音字或原文 
                    text+=wd[j]
                    i+=1
                    insert=0
                elif j+self.pinyinLen[i]<=len(wd) and (wd[j:j+self.pinyinLen[i]]).lower()==self.pinyin[i]:#全拼音
                    text+=wd[j:j+self.pinyinLen[i]]
                    j=j+self.pinyinLen[i]-1
                    i+=1
                    insert=0
                elif wd[j].lower() ==self.pinyin[i][0]:#拼音首字母
                    text+=wd[j]
                    i+=1
                    insert=0
                elif wd[j] in string.digits+string.ascii_letters+"[\n`~!@#$%^&*()+-_=|{}《》':;',\\[\\].<>/?~！\"@#￥%……&*()——+|{}【】‘；：”“’。， 、？]":
                    text+=wd[j]
                    insert+=1
                else:
                    break
                j+=1
            if i!=self.length:
                text=""
        return text,len(text)

class english:
    def __init__(self, word):
        self.word=word
        self.length=len(word)#长度
    def testing(self,wd):
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
                elif wd[j] in string.digits+"[\n`~!@#$%^&*()+=|{}':;',\\[\\].<>《》/?~！@#￥%……&*()——+|{}【】\"‘；：”“’。， 、？]":
                    text+=wd[j]
                else:
                    break
            if i!=self.length:
                    text=""
        return text,len(text)

def fileOpen(path):#打开文件
    try:
        f=open(path,'r+',encoding='utf-8')
    except IOError:
        print("文件不存在")
        raise IOError("文件不存在")
    else:
        return f


def getWords(address):#获取敏感词
    chinesew=[]#中文
    englishw=[]#英文
    file=fileOpen(address)
    for line in file.readlines():
        line=line.strip()
        if line[0] in string.ascii_letters:
            englishw.append(english(line))
        else:
            chinesew.append(chinese(line))
    file.close()
    return chinesew,englishw




def search(lines,chiWords,engWords):
    lineCount=0
    result=[]
    totalCount=0#敏感词个数
    textLen=0
    for line in lines:#读取每行
        lineCount+=1
        line=line.strip()
        i=0
        while(i<len(line)):
            for wd in engWords:
                text,textLen=wd.testing(line[i:])
                if textLen:
                    totalCount+=1
                    result.append("Line{}: <{}> {}".format(lineCount,wd.word,text))
                    i+=textLen-1
                    break
            for wd in chiWords:
                text,textLen=wd.testing(line[i:])
                if textLen:
                    totalCount+=1
                    result.append("Line{}: <{}> {}".format(lineCount,wd.word,text))
                    i+=textLen-1
                    break
            i+=1
    return result,totalCount


def parament():#命令行参数检查
    if len(sys.argv) != 4:
        print("命令行参数错误")
        raise Exception("命令行参数错误")

def main():
    parament()

    #文件地址读取
    wordsAddress=(sys.argv[1])#敏感词文件
    textAddress=(sys.argv[2])#内容文件
    answerAddress=(sys.argv[3])#答案文件

    #敏感词读取
    chiWords,engWords=getWords(wordsAddress)#中文，英文

    #文本检测
    textFile=fileOpen(textAddress)
    lines=textFile.readlines()
    result,total=search(lines,chiWords,engWords)
    textFile.close()

    #写入文件
    answerFile=fileOpen(answerAddress)
    answerFile.write("Total: {} ".format(total)+'\n')
    answerFile.write('\n'.join(result))
    answerFile.close()


if __name__ == '__main__':
    main()

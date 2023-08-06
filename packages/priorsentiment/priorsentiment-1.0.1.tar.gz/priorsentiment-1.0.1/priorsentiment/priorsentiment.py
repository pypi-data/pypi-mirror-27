# This is final version of cs510 final project
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import nltk
# process the data let it change to the structure word_tag
class Prepro:
    def __init__(self,data):
        self.wtlist = []
        self.data = data
    def word_tag(self):
        for i in range(len(self.data)):
            sen = self.data[i]

            sen = sen.replace('[', '')
            sen = sen.replace(']', '')
            sen = sen.lower()

            if sen != '':
                word_list = nltk.word_tokenize(sen)
                word_tags = nltk.pos_tag(word_list)
                write = ''
                for j in range(len(word_tags)):
                    word = word_tags[j][0]
                    tag = word_tags[j][1]
                    if j != len(word_tags) - 1:
                        write += word + '_' + tag + ' '
                    else:
                        write += word + '_' + tag
                self.wtlist.append(write)
        return self.wtlist
    def word_tag_sen(self):
        sen = self.data
        sen = sen.replace('[', '')
        sen = sen.replace(']', '')
        sen = sen.lower()

        if sen != '':
            word_list = nltk.word_tokenize(sen)
            word_tags = nltk.pos_tag(word_list)
            write = ''
            for j in range(len(word_tags)):
                word = word_tags[j][0]
                tag = word_tags[j][1]
                if j != len(word_tags) - 1:
                    write += word + '_' + tag + ' '
                else:
                    write += word + '_' + tag
        return write

# The data structure used in this lib
class W_pos:
    def __init__(self,oword):
        templ = oword.split('_')
        self.word = templ[0]
        self.tag = templ[1]

# This class is used for calculate the prior score
class Pri_sc:
    def __init__(self,pos_data,neg_data):
        temppos = Prepro(pos_data)
        wtpos = temppos.word_tag()
        tempneg = Prepro(neg_data)
        wtneg = tempneg.word_tag()
        self.pos_data = wtpos
        self.neg_data = wtneg
        self.pri_score = {}
        self.poscount = defaultdict(int)
        self.negcount = defaultdict(int)
        self.all_pairs = []
        self.train_pos()
        self.train_neg()
        self.all_pairs = list(set(self.all_pairs))
        self.calculate_sc()
    def train_pos(self):
        for sen in self.pos_data:
            templist = sen.split()
            tempword = []
            temptag = []
            for w in templist:
                tempwp = W_pos(w)
                tempword.append(tempwp.word)
                temptag.append(tempwp.tag)
            for i in range(len(temptag) - 1):
                if self.checkrule(i,temptag):
                    self.poscount[(tempword[i],tempword[i+1])] += 1
                    self.all_pairs.append((tempword[i], tempword[i + 1]))
    def train_neg(self):
        for sen in self.neg_data:
            templist = sen.split()
            tempword = []
            temptag = []
            for w in templist:
                tempwp = W_pos(w)
                tempword.append(tempwp.word)
                temptag.append(tempwp.tag)
            for i in range(len(temptag) - 1):
                if self.checkrule(i,temptag):
                    self.negcount[(tempword[i],tempword[i+1])] += 1
                    self.all_pairs.append((tempword[i],tempword[i+1]))
    def checkrule(self,index,taglist):
        t1 = taglist[index]
        t2 = taglist[index + 1]
        if (index + 2) < len(taglist):
            t3 = taglist[index + 2]
        else:
            t3 = 'None'
        nnl = ['NN', 'NNS']
        rbl = ['RB', 'RBR', 'RBS']
        vbl = ['VB', 'VBD', 'VBN', 'VBG']
        if t1 == 'JJ':
            if t2 in nnl:
                return 1
            if t2 == 'JJ':
                if t3 not in nnl:
                    return 1
        elif t1 in nnl:
            if t2 == 'JJ':
                if t3 not in nnl:
                    return 1
        elif t1 in rbl:
            if t2 == 'JJ':
                if t3 not in nnl:
                    return 1
            if t2 in vbl:
                return 1
        elif t1 in ['VB', 'VBD', 'VBN', 'VBG', 'VBP', 'VBZ']:
            if t2 == 'JJ':
                if t3 in ['IN', '.', 'TO']:
                    return 1
        return 0

    def calculate_sc(self):
        for pair in self.all_pairs:
            tempamount = max(10,(self.poscount[pair]+self.negcount[pair]))

            self.pri_score[pair] = (self.poscount[pair] - self.negcount[pair])/tempamount
    def get_score(self):
        return self.pri_score



# This is used for calculating the score and can output files
class SO:
    def __init__(self,pos_data,neg_data):
        self.pri = Pri_sc(pos_data,neg_data)
        self.pri_score = self.pri.pri_score
        self.posl = []
        self.negl = []
        self.neul = []
        self.url = "http://search.yahoo.com/search?p=%s"
        soup_poor = BeautifulSoup(requests.get(self.url % '"poor"').text, 'lxml')
        time.sleep(2)
        soup_excellent = BeautifulSoup(requests.get(self.url % '"excellent"').text, 'lxml')
        time.sleep(2)
        self.hit_excellent = int(
            soup_excellent.find_all(attrs={"class": "compPagination"})[0].span.contents[0].replace(',', '').split()[0])
        time.sleep(2)
        self.hit_poor = int(
            soup_poor.find_all(attrs={"class": "compPagination"})[0].span.contents[0].replace(',', '').split()[0])
        time.sleep(2)


    def cal_sen(self,sen):
        tempsen = Prepro(sen)
        wtsen = tempsen.word_tag_sen()
        self.wjds = {}
        self.words = []
        self.tags = []
        senl = wtsen.split()
        for i in senl:
            tempwp = W_pos(i)
            self.words.append(tempwp.word)
            self.tags.append(tempwp.tag)
        self.gotpair()
        self.calscore()
        orsen = ''
        for i in self.words:
            orsen += i + ' '
        self.process(orsen)
    def gotpair(self):
        self.avpairs = []
        for i in range(len(self.tags) - 1):
            if self.checkrule(i):
                self.avpairs.append((self.words[i],self.words[i+1]))


    def checkrule(self, index):
        t1 = self.tags[index]
        t2 = self.tags[index + 1]
        if (index + 2) < len(self.tags):
            t3 = self.tags[index + 2]
        else:
            t3 = 'None'
        nnl = ['NN', 'NNS']
        rbl = ['RB', 'RBR', 'RBS']
        vbl = ['VB', 'VBD', 'VBN', 'VBG']
        if t1 == 'JJ':
            if t2 in nnl:
                return 1
            if t2 == 'JJ':
                if t3 not in nnl:
                    return 1
        elif t1 in nnl:
            if t2 == 'JJ':
                if t3 not in nnl:
                    return 1
        elif t1 in rbl:
            if t2 == 'JJ':
                if t3 not in nnl:
                    return 1
            if t2 in vbl:
                return 1
        elif t1 in ['VB', 'VBD', 'VBN', 'VBG','VBP','VBZ']:
            if t2 == 'JJ':
                if t3 in ['IN','.','TO']:
                    return 1


        return 0

    def calscore(self):
        self.sosc = 0
        if len(self.avpairs) != 0:

            for word_pair in self.avpairs:

                word1 = word_pair[0]
                word2 = word_pair[1]
                phrase_excellent, phrase_poor = self.get_hits(word1, word2)
                if phrase_excellent != 0 and phrase_poor != 0:
                    temp_sosc = np.log2(phrase_excellent * self.hit_poor / (phrase_poor * self.hit_excellent))
                    temp_sosc = (1/(1+np.exp(-temp_sosc))-0.5)*2
                    if word_pair in self.pri_score:
                        temp_final = 0.8 * self.pri_score[word_pair] + 0.2 * temp_sosc
                    else:
                        temp_final = temp_sosc
                    self.sosc += temp_final

            self.sosc = self.sosc / float(len(self.avpairs))



    def get_hits(self,word1,word2):
        phrase_excellent, phrase_poor = 0,0
        phrase = '"'+word1+' '+word2+'"'
        query1 = phrase + ' NEAR ' +'"excellent"'
        query2 = phrase + ' NEAR ' +'"poor"'
        r1 = requests.get(self.url % query1)
        time.sleep(2)
        r2 = requests.get(self.url % query2)
        time.sleep(2)
        soup1 = BeautifulSoup(r1.text, 'lxml')
        time.sleep(2)
        soup2 = BeautifulSoup(r2.text, 'lxml')
        time.sleep(2)
        if len(soup1.find_all(attrs={"class": "compPagination"}))>0:
            phrase_excellent = int(soup1.find_all(attrs={"class": "compPagination"})[0].span.contents[0].replace(',','').split()[0])
        time.sleep(2)
        if len(soup2.find_all(attrs={"class": "compPagination"}))>0:
            phrase_poor = int(soup2.find_all(attrs={"class": "compPagination"})[0].span.contents[0].replace(',','').split()[0])
        self.wjds[(word1,word2)] = (phrase_excellent,phrase_poor)
        return phrase_excellent,phrase_poor

    def process(self,sen):
        if self.sosc > 0:
            self.posl.append(sen)
        elif self.sosc == 0:
            self.neul.append(sen)
        else:
            self.negl.append(sen)


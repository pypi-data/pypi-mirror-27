import re

# TODO: need a smarter splitter. Currently relies on initial capitalization
def text2sentences(text):
    '''
    >>> text2sentences('Abc, def. Ghi jkl. Mno pqr.')
    ['Abc, def.', 'Ghi jkl.', 'Mno pqr.']
    '''

    sentenceDivider = '([.!?][\)]?) (?=[\(]?[A-Z])'
    temp = []
    s = re.split(sentenceDivider,text+' A')
    for i in range(0,len(s)-1,2):
        temp.append(s[i] + s[i+1])
    return temp

def sentence2words(sentence):
    '''
    >>> sentence2words('Abc, def (gh ij) klm nop.')
    ['Abc', ',', 'def', '(', 'gh', 'ij', ')', 'klm', 'nop', '.']
    '''

    s = sentence.split(' ')
    temp = []
    for e in s:
        temp += re.split(r'([,\(\).!?])',e)
    return [e for e in temp if e != '']

def text2words(text):
    '''
    >>> text2words('Abc, def. Ghi jkl. Mno pqr.')
    [['Abc', ',', 'def', '.'], ['Ghi', 'jkl', '.'], ['Mno', 'pqr', '.']]
    '''

    return [sentence2words(sentence) for sentence in text2sentences(text)]

class Text(object):
    def __init__(self,s,keepCapitals=False,stripPunct=True):
        self.source = text2words(s)

        if stripPunct:
            self.source = [[w for w in s if w not in ',.!?"'] for s in self.source]

        if not keepCapitals:
            self.source = [[w.lower() for w in s] for s in self.source]

        self.d = {}
        for sentence in self.source:
            for word in sentence:
                self.d[word] = self.d.get(word,0)+1
        self.total = sum(self.d.values())

    def freq(self,w):
        return self.d.get(w,0)/self.total

    def count(self,w):
        return self.d.get(w,0)

    def nGram(self,n,atLeast=None,atMost=None):
        freqs = {}
        for s in self.source:
            for t in range(len(s)-n+1):
                slug = ' '.join(s[t:t+n])
                freqs[slug] = freqs.get(slug,0)+1

        temp = []
        for k,v in freqs.items():
            if atLeast == None or v >= atLeast:
                if atMost == None or v <= atMost:
                    temp.append((v,k.split(' ')))
        return temp

    def nGramFiltered(self,f,atLeast=None,atMost=None):
        temp = []
        for n,p in self.nGram(len(f),atLeast,atMost):
            if all([a==b or b == None for a,b in zip(p,f)]):
                temp.append((n,p))
        return temp



#!/usr/bin/env python
# -*- coding: utf-8 -
'''
Created on 2016年7月2日

@author: Angel
'''
try:
    import nltk, sys, logging, time, re, json
    from xml.sax.saxutils import escape
except:
    sys.exit('Some package is missing... Perhaps <re>?')
import seg
import seg.analyse

wordEngStop = nltk.corpus.stopwords.words('english')
porter = nltk.PorterStemmer()

log_console = logging.StreamHandler(sys.stderr)
default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.DEBUG)
default_logger.addHandler(log_console)

fix = lambda text: escape(text.encode('utf-8'))

dl = {}
def token_pre(s):
    s = re.sub('[^a-zA-Z]', " ", s)
    strs = re.split(r'\s+', s.lower())
    strs = [porter.stem(w).encode('utf-8') for w in strs if w not in wordEngStop if len(w) > 2]
    return strs
#     return ' '.join(strs)

def cuttest(test_sent):
    result = seg.cut(test_sent)
    return '  '.join(result).lstrip(' ')

def seg_process(context):
    content = cuttest(context.strip().replace(" ", ""))
    return content

def DelLastChar(str):
    str_list = list(str)
    str_list.pop()
    return "".join(str_list)

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if len(str([uchar])) > 8:
        return True
    else:
        return False

def process(context, flag):
    print flag
    if flag:
        cn_context = context
        cn_keyWord = seg_process(cn_context)
    #     print keyWord
        cn_keyWord = []
        for x, w in seg.analyse.extract_tags(cn_context, withWeight=True):
#             print('%s %s' % (x, w))
            cn_keyWord.append(x)
        cn_key_json = "{\n\t\"key\":["
        for key in cn_keyWord:
            cn_key_json += " \"" + key + "\","
        cn_key_json = DelLastChar(cn_key_json)
        cn_key_json += "]\n}"
        print cn_key_json
    else:
        en_context = context
        en_tokens = nltk.word_tokenize(en_context)
        en_keyWord = token_pre(' '.join(en_tokens))
        en_key_json = "{\n\t\"key\":["
        for key in en_keyWord:
            en_key_json += " \"" + key + "\","
        en_key_json = DelLastChar(en_key_json)
        en_key_json += "]\n}"
        print en_key_json

if __name__ == '__main__':
    t1 = time.time()
    context = "Where is my Key? Welcome to Girl Hackens"
#     context = "我的钥匙在哪了谷歌编程女神范"
    flag = False
    if is_chinese(context):
        en_context = context
        flag = True
    process(context, flag)
    default_logger.debug("All cost %.3f seconds." % (time.time() - t1))
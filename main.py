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
import md5

wordEngStop = nltk.corpus.stopwords.words('english')
porter = nltk.PorterStemmer()

log_console = logging.StreamHandler(sys.stderr)
default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.DEBUG)
default_logger.addHandler(log_console)

dl = {}
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')

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
    match = zhPattern.search(uchar)
    if match:
        return True
    else:
        return False

def process(context):
    context = context.decode('gbk', 'ignore')
#     print type(context)
    flag = False
    if is_chinese(context):
        flag = True
    
    if flag:
        context = seg_process(context)
        keyWord = []
        for x, w in seg.analyse.extract_tags(context, withWeight=True):
#             print('%s %s' % (x, w))
            keyWord.append(x.encode('utf-8'))
    else:
        tokens = nltk.word_tokenize(context)
        keyWord = token_pre(' '.join(tokens))
#         en_key_json = "{\n\t\"key\":["
#         for key in en_keyWord:
#             en_key_json += " \"" + key + "\","
#         en_key_json = DelLastChar(en_key_json)
#         en_key_json += "]\n}"
#         print en_key_json
    key_json = ""
#     value = " ".join(keyWord)
#     print type(keyWord[0])
    key_values_dic = {}
    key_values_dic['key'] = keyWord
    key_json = json.dumps(key_values_dic)
#     key_json = json.dumps(keyWord)
#     print str(key_values_dic)
#     print type(key_json)
#     print key_json
    return key_json
if __name__ == '__main__':
    use_msg = 'Use as:\n">>> python memery.py yourSentences"\n\nThis will parse a train str, extract keyword then return keyword json.'
    if len(sys.argv) != 2: sys.exit(use_msg)
#     context = sys.stdin
#     context = "Where is my Key? Welcome to Girl Hackens"
#     context = "谷歌变成女神范"
    context = sys.argv[1]
#     filename = sys.argv[2]
#     print type(context)
    key_json = process(context)
    print key_json

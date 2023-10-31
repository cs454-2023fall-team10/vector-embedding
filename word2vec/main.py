from gensim.models import Word2Vec
from konlpy.tag import Okt

# https://jeongminhee99.tistory.com/72
def parse_sentence (sentence) :
    okt = Okt()
    results = ""
    line = sentence
    #형태소 분석하기 -- (3)
    #단어의 기본형 사용
    malist = okt.pos(line, norm=True, stem=True)
    r = []
    for word in malist:
        if not word[1] in ["Josa", "Eomi", "Punctuation"]:
            r.append(word[0])
    rl = (" ".join(r)).strip()
    results = rl
    
    return results

model = Word2Vec.load("./models/model")

# 문장의 유사성
s1 = '제주도는 아름다운 섬 입니다'
s2 = '독도는 아름다운 섬 입니다' #corrected variable name

distance1 = model.wv.n_similarity(parse_sentence(s1).split(), parse_sentence(s2).split())

print(distance1)
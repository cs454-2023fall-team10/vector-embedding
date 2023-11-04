from gensim.models import Word2Vec
from konlpy.tag import Okt
import load_data, preprocess, make_model

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

def test() :
    model = Word2Vec.load("./models/model")

    # 문장의 유사성
    s1 = '현재 채널팀이 내 전공 관련 포지션을 채용중인지 물어보고 싶어'
    s2 = '채용중인 포지션'
    s3 = '채널팀 알아보기'

    distance1 = model.wv.n_similarity(parse_sentence(s1).split(), parse_sentence(s2).split())
    distance2 = model.wv.n_similarity(parse_sentence(s1).split(), parse_sentence(s3).split())

    print(distance1)
    print(distance2)


if __name__ == '__main__' :
    test()
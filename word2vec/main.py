from gensim.models import Word2Vec
from konlpy.tag import Okt
import load_data, preprocess, make_model
import utils

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

def get_best_sentence(intent, choices, model) :
    max_similarity = 0
    best_choice_idx = 0

    for i in range(len(choices)) :
        distance = model.wv.n_similarity(parse_sentence(intent).split(), parse_sentence(choices[i]).split())
        if distance > max_similarity :
            max_similarity = distance
            best_choice_idx = i
        
    print(choices[best_choice_idx].strip(), "(Score: %.4f)" % (max_similarity))
    return best_choice_idx


if __name__ == "__main__" :
  model = Word2Vec.load("./models/model")
  intent = "채널팀에 대해 알아보고 싶어"
  file_name = "jobs-homepage.json"

  dic = utils.load_and_parse(file_name)
  section = dic["sections"][0]
  while True :
    (raw_choices, choices) = utils.get_choices(section)
    if len(choices) != 0 :
      top_result_idx = get_best_sentence(intent, choices, model)
      section_id = raw_choices[top_result_idx]["nextSectionId"]
      section = utils.get_sections(section_id, dic)
      continue

    else : # Reach last destination
      print("reached at the bottom")
      break
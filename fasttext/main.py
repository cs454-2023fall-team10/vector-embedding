from gensim.models import fasttext
from konlpy.tag import Okt
import load_data, preprocess, make_model
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
        
    # print(choices[best_choice_idx].strip(), "(Score: %.4f)" % (max_similarity))
    return best_choice_idx


if __name__ == "__main__" :
  if len(sys.argv) < 5 :
    utils.usage()
  
  file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), sys.argv[1])
  intents_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), sys.argv[2])

  MAX_NUMBER = int(sys.argv[3])
  DEPTH_THRESHOLD = int(sys.argv[4])

  try :
    model_name = sys.argv[5].rstrip()
  except :
    model_name = "./models/cc.ko.300.bin"
  
  model = fasttext.load_facebook_vectors(model_name)
  
  dic = utils.load_and_parse(file_path)

  intents = utils.get_intents(intents_path, MAX_NUMBER)
  
  out = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "result/out.txt"), "w")
  for intent in intents :
    section = dic["sections"][0]
    path = []
    count = 0

    while count < DEPTH_THRESHOLD :
      path.append(section["id"])
      (raw_choices, choices) = utils.get_choices(section)
      if len(choices) != 0 :
        top_result_idx = get_best_sentence(intent, choices, model)
        section_id = raw_choices[top_result_idx]["nextSectionId"]
        section = utils.get_sections(section_id, dic)
        count += 1
        continue

      else : # Reach last destination
        # print("reached at the bottom")
        break
    
    out.write("%s\t%s\n"%(intent, path))
  
  out.close()
from sentence_transformers import SentenceTransformer, util
import numpy as np
import utils

def get_best_sentence(intent, choices, model) :
  choice_embeddings = model.encode(choices)

  top_k = 1
  intent_embedding = model.encode(intent)
  cos_scores = util.pytorch_cos_sim(intent_embedding, choice_embeddings)[0]
  cos_scores = cos_scores.cpu()
  top_result = np.argpartition(-cos_scores, range(top_k))[0:top_k]

  print(choices[top_result].strip(), "(Score: %.4f)" % (cos_scores[top_result]))
  return top_result
  

if __name__ == "__main__" :
  model = SentenceTransformer('jhgan/ko-sroberta-multitask')
  intent = "채널팀에 대해 알아보고 싶어"
  file_name = "lead-homepage.json"

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


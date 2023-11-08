from sentence_transformers import SentenceTransformer, util
import numpy as np
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

def get_best_sentence(intent, choices, model) :
  choice_embeddings = model.encode(choices)

  top_k = 1
  intent_embedding = model.encode(intent)
  cos_scores = util.pytorch_cos_sim(intent_embedding, choice_embeddings)[0]
  cos_scores = cos_scores.cpu()
  top_result = np.argpartition(-cos_scores, range(top_k))[0:top_k]

  # print(choices[top_result].strip(), "(Score: %.4f)" % (cos_scores[top_result]))
  return top_result
  

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
    model_name = 'jhgan/ko-sroberta-multitask'

  model = SentenceTransformer(model_name)
  
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


from pororo import Pororo
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils

def get_best_sentence(intent, choices, model) :
    max_similarity = 0
    best_choice_idx = 0

    for i in range(len(choices)) :
        distance = model(intent.strip(), choices[i].strip())
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

  model = Pororo(task="similarity", lang="ko")
  
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
from pororo import Pororo
import utils

def get_best_sentence(intent, choices, model) :
    max_similarity = 0
    best_choice_idx = 0

    for i in range(len(choices)) :
        distance = model(intent.strip(), choices[i].strip())
        if distance > max_similarity :
            max_similarity = distance
            best_choice_idx = i
        
    print(choices[best_choice_idx].strip(), "(Score: %.4f)" % (max_similarity))
    return best_choice_idx


if __name__ == "__main__" :
  model = Pororo(task="similarity", lang="ko")
  intent = "서류를 제출하고 싶어"
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
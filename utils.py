import json, os

def load_and_parse(file_path) :
    with open(file_path, "r") as f :
        j = f.read()
        dic = parse_json(j)
        return dic

def parse_json(j) :
    return json.loads(j)

def get_choices(d) :
    ret = []
    raw_choices = []
    try :
        raw_choices = d["buttons"]
        for button in raw_choices :
            ret.append(button["text"])
    except :
        pass
    
    return (raw_choices, ret)

def get_sections(section_id, dic) :
    for section in dic["sections"] :
        if section["id"] == section_id :
            return section
    
    return {}

def get_intents(intents_path, MAX_NUMBER) :
    intents = []
    count = 0
    with open(intents_path) as f :
        for line in f :
            if count > MAX_NUMBER :
                break
            intents.append(line.rstrip())
            count += 1
    
    return intents

def usage() :
    print("Usage: python main.py <json_file_path> <intents_file_path> <NUM_OUTPUTS> <DEPTH_THRESHOLDS> <(Optional) model_name>")
    print("For <json_file_path>, <intents_file_path>, relative path should be used")
    exit(-1)

if __name__ == "__main__" :
    file_name = "jobs-homepage.json"
    print(load_and_parse(file_name))
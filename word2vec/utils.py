import json, os

def load_and_parse(file_name) :
    with open(os.path.join("../chatbot-dataset/examples", file_name), "r") as f :
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

if __name__ == "__main__" :
    file_name = "jobs-homepage.json"
    print(load_and_parse(file_name))
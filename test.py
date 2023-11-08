import json

information_dict = {'x':1,'y':2}
with open("eval_information.json", "w", encoding='utf-8') as f:
            json.dump(information_dict, f, indent=2, sort_keys=True, ensure_ascii=False) 
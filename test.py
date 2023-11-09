<<<<<<< HEAD
a = '48h'
b = a.split("h")
print(b)
=======
import json

information_dict = {'x':1,'y':2}
with open("eval_information.json", "w", encoding='utf-8') as f:
            json.dump(information_dict, f, indent=2, sort_keys=True, ensure_ascii=False) 
>>>>>>> a624bf59ed273e253c032a3993b0565922aa81f2

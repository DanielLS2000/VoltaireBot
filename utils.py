import json
import re

def salvar_campanhas(campanhas):
    with open('campanhas.json', 'w', encoding='utf-8') as f:
        json.dump([campanha.to_dict() for campanha in campanhas], f, ensure_ascii=False, indent=4)

def hora_valida(time_input):
    return re.match(r'^[0-2][0-9]:[0-5][0-9]$', time_input)

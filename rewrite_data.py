import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

json_file = BASE_DIR / 'data/ingredients.json'

data = []

with open(file=json_file, mode='r') as file:
    json_data = json.load(file)
    pk = 1
    for fields in json_data:
        data.append({
            'model': 'recipes.ingredient',
            'pk': pk,
            'fields': fields
        })
        pk += 1

with open(file=json_file, mode='w', encoding='UTF-8') as file:
    json.dump(obj=data, fp=file, ensure_ascii=False)

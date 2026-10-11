import json
import os

from main import import_coupled_kratos, save_onto

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

fixture_path = os.path.join(
    root_dir,
    'examples',
    'synthetic',
    'coupled-system.json')

with open(fixture_path, encoding='utf-8') as fixture_file:
    data = json.load(fixture_file)

import_coupled_kratos(data, 'Synthetic coupled system')
save_onto()

import pandas as pd
import os

categorizado = pd.read_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "categorizado.json"))

count = 0
# iterate dataframe using iterrows
for index, row in categorizado.iterrows():
    # if 'Inclusão e Diversidade' in row.to_dict()['eixo']:
    if len(row.to_dict()['eixo']) == 0:
        count += 1
print(count)
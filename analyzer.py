import os
import pandas as pd

print(*[filename.split(".")[0] for filename in os.listdir("./opinions")], sep="\n") #* wypakowuje wartości z listy na osobne zmienne
product_id = input("Podaj identyfikator produktu: ")

opinions = pd.read_json(f"opinions/{product_id}.json")
print(opinions)
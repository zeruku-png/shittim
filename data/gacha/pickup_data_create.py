import csv
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

data = []

# star_1.txtから読み込み
with open("../characters/star_1.txt", "r", encoding="utf-8") as f:
    for name in f.readlines():
        name = name.strip()
        data.append({"name": name, "rarity": 1, "is_pickup": False})

# star_2.txtから読み込み
with open("../characters/star_2.txt", "r", encoding="utf-8") as f:
    for name in f.readlines():
        name = name.strip()
        data.append({"name": name, "rarity": 2, "is_pickup": False})

# star_3.txtから読み込み
with open("../characters/star_3.txt", "r", encoding="utf-8") as f:
    for name in f.readlines():
        name = name.strip()
        data.append({"name": name, "rarity": 3, "is_pickup": False})

pickup_name = input("ピックアップキャラクターの名前を入力してください。\n>> ")
for n, character in enumerate(data):
    if character["name"] == pickup_name:
        data[n]["is_pickup"] = True
        print(pickup_name + "をピックアップに設定しました。")

print()

gacha_name = input("募集の名前を入力してください。\n>> ")

# CSVファイルに書き出し
with open(f"{gacha_name}.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["name", "rarity", "is_pickup"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

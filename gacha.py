import csv
import random
import json
import utils


def get_characters(file_path):
    characters = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            name, rarity, is_pickup = row
            characters.append(
                {"name": name, "rarity": int(rarity), "is_pickup": is_pickup == "True"}
            )
    return characters


def get_gacha_characters(characters):
    pickup_characters = [c for c in characters if c["is_pickup"]]
    star3_characters = [
        c for c in characters if c["rarity"] == 3 and not c["is_pickup"]
    ]
    star2_characters = [
        c for c in characters if c["rarity"] == 2 and not c["is_pickup"]
    ]
    star1_characters = [
        c for c in characters if c["rarity"] == 1 and not c["is_pickup"]
    ]

    return {
        "pickup": pickup_characters,
        "star3": star3_characters,
        "star2": star2_characters,
        "star1": star1_characters,
    }


def gacha_pickup(gacha_characters):
    pickup_rate = 0.007
    star3_rate = 0.023
    star2_rate = 0.185
    star1_rate = 0.785
    return random.choice(
        gacha_characters[
            random.choices(
                ["pickup", "star3", "star2", "star1"],
                weights=[pickup_rate, star3_rate, star2_rate, star1_rate],
                k=1,
            )[0]
        ]
    )


def gacha_no_pickup(gacha_characters):
    star3_rate = 0.03
    star2_rate = 0.185
    star1_rate = 0.785
    return random.choice(
        gacha_characters[
            random.choices(
                ["star3", "star2", "star1"],
                weights=[star3_rate, star2_rate, star1_rate],
                k=1,
            )[0]
        ]
    )


with open(
    r".\data\gacha\id_to_path.json",
    "r",
    encoding="utf-8",
) as f:
    gacha_path = json.load(f)


with open(
    r".\data\gacha\id_to_name.json",
    "r",
    encoding="utf-8",
) as f:
    gacha_name = json.load(f)


def main(name, num):
    gacha_characters = get_gacha_characters(get_characters(gacha_path[name]))
    result = [
        gacha_pickup(gacha_characters)
        if gacha_characters["pickup"]
        else gacha_no_pickup(gacha_characters)
        for n in range(num)
    ]

    return utils.create_gacha_embed(name=gacha_name[name], datas=result)

import discord
import datetime
import os
import json


def help_embed():
    embed = discord.Embed(
        title="コマンドのヘルプです！", description="現在、コマンドが3個あります！", color=0x8CD4EF
    )
    embed.add_field(name="/help", value="このメッセージを表示します！", inline=False)
    embed.add_field(name="/vchelp", value="VC関連のコマンドのヘルプを表示します！", inline=False)
    embed.add_field(
        name="/gacha [ピックアップの種類] [回数]",
        value="実際のゲーム内のガチャと同じ確率のガチャシミュレーターが使えます！",
        inline=False,
    )
    return embed


def vc_help_embed():
    embed = discord.Embed(
        title="vcに関するコマンドのヘルプです！",
        description="現在、コマンドが3個あります！",
        color=0x8CD4EF,
    )
    embed.add_field(name="/name", value="VCのチャンネルの名前を変更します！", inline=False)
    embed.add_field(name="/bitrate", value="VCのビットレートを変更します！", inline=False)
    embed.add_field(
        name="/limit",
        value="VCの最大参加人数を変更します！",
        inline=False,
    )
    return embed


def create_gacha_embed(name, datas):
    title = f"「{name}」の募集結果です！"
    description = ""

    for data in datas:
        rarity = data["rarity"]
        emoji = (
            f"<:{rarity}_:1066862728423161877>"
            if rarity == 1
            else f"<:{rarity}_:1066862727433298000>"
            if rarity == 2
            else f"<:{rarity}_:1066862724765728838>"
        )
        name = (
            f"{data['name']}"
            if not data["is_pickup"]
            else f"(**Pick up!**) **{data['name']}**"
        )
        description += f"{emoji} {name} | "

    else:
        emoji_map = {
            1: "<:1_:1066862728423161877>",
            2: "<:2_:1066862727433298000>",
            3: "<:3_:1066862724765728838>",
        }
        description = f"{len(datas)}連分の結果を表示します！"
        newlines = []
        newline = ""

        for i, data in enumerate(datas, start=1):
            emoji = emoji_map.get(data["rarity"], "<:3_:1066862724765728838>")
            pickup = " (**Pick Up!**)" if data["is_pickup"] else ""
            character_name = (
                f"__**{data['name']}**__" if data["rarity"] == 3 else f"{data['name']}"
            )

            newline += (
                f"{emoji} {character_name}{pickup}\n"
                if i % 5 == 0
                else f"{emoji} {character_name}{pickup} | "
            )

            if i % 10 == 0:
                newlines.append(newline)
                newline = ""

    embed = discord.Embed(
        title=title,
        description=description,
        color=0x8CD4EF,
        timestamp=datetime.datetime.now(),
    )
    embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/539015808962002946/801431311385362442/image0.png"
    )

    for i, line in enumerate(newlines, start=1):
        start = i * 10 - 9
        end = i * 10

        if line.count("<:1_:1066862728423161877>") == 10:
            embed.add_field(
                name=f"{start} ~ {end}連目の結果です！(この10連は最低保障です...)",
                value=line,
                inline=False,
            )
        else:
            embed.add_field(name=f"{start} ~ {end}連目の結果です！", value=line, inline=False)

    return embed


def choices_generate():
    folder_path = r".\data\gacha"
    id_to_path = json.load(
        open(
            r".\data\gacha\id_to_path.json",
            "r",
            encoding="utf-8",
        )
    )

    text = [
        discord.app_commands.Choice(name=os.path.splitext(file)[0], value=key)
        for key, path in id_to_path.items()
        for file in os.listdir(folder_path)
        if file.endswith(".csv") and os.path.join(folder_path, file) == path
    ]

    return text

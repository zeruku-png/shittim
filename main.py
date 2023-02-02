import discord
from discord.ext import commands
import gacha as gc
import utils

TOKEN = "token"
cmd = "a!"

client = commands.Bot(intents=discord.Intents.default(), command_prefix=cmd)
guild = discord.Object(795846837730279445)
tree = client.tree

version = "2周年"
voice_channel_status = {}


@client.event
async def on_ready():
    print(
        f"Logged in as {client.user.name}#{client.user.discriminator} ({client.user.id})"
    )
    print("------------------------------")
    await tree.sync(guild=guild)
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.listening, name=version),
    )


@tree.command(name="help", description="コマンドのヘルプを表示します！", guild=guild)
async def help(ctx: discord.Interaction):
    await ctx.response.send_message(
        embed=utils.help_embed(), ephemeral=True, delete_after=120
    )


@tree.command(name="vchelp", description="VCに関するコマンドのヘルプを表示します！", guild=guild)
async def vchelp(ctx: discord.Interaction):
    await ctx.response.send_message(
        embed=utils.vc_help_embed(), ephemeral=True, delete_after=120
    )


@client.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id == 804226790347374602:
        channel = discord.utils.get(member.guild.channels, id=804226790347374602)
        category = channel.category
        new_channel = await category.create_voice_channel(
            name="新しいチャンネル", bitrate=64000, user_limit=99
        )
        await member.move_to(new_channel)
        voice_channel_status[new_channel.id] = member.id

    if before.channel and before.channel.id != 804226790347374602:
        if (
            len(before.channel.members) == 0
            and before.channel.category.id == 796263632056221727
        ):
            await before.channel.delete()


@tree.command(name="name", description="ボイスチャンネルの名前を変更できます。", guild=guild)
async def name(ctx: discord.Interaction, text: str):
    if ctx.user.voice:
        try:
            if voice_channel_status[ctx.user.voice.channel.id] == ctx.user.id:
                await ctx.user.voice.channel.edit(name=text)
                await ctx.response.send_message(
                    f"先生が参加しているボイスチャンネルの名前を「{text}」に変更しました！",
                    ephemeral=True,
                    delete_after=30,
                )
            else:
                await ctx.response.send_message(
                    f"{ctx.user.display_name}先生は、このチャンネルのオーナーでは無いみたいです。\nチャンネルの名前を変更できるのは、このチャンネルの作者の先生だけです！",
                    ephemeral=True,
                    delete_after=30,
                )
        except Exception as e:
            await ctx.response.send_message(
                f"不明なエラーが発生してしまったみたいです...\nエラーメッセージ: {e}",
                ephemeral=True,
                delete_after=30,
            )

    else:
        await ctx.response.send_message(
            "ボイスチャンネルに参加していないみたいです...", ephemeral=True, delete_after=30
        )


@tree.command(name="bitrate", description="ボイスチャンネルのビットレートを変更できます。", guild=guild)
async def bitrate(
    ctx: discord.Interaction, num: discord.app_commands.Range[int, 8, 384]
):
    if ctx.user.voice:
        try:
            if voice_channel_status[ctx.user.voice.channel.id] == ctx.user.id:
                await ctx.user.voice.channel.edit(bitrate=num * 1000)
                await ctx.response.send_message(
                    f"先生が参加しているボイスチャンネルのビットレートを「**{str(num)}Kbps**」に変更しました！",
                    ephemeral=True,
                    delete_after=30,
                )
            else:
                await ctx.response.send_message(
                    f"{ctx.user.display_name}先生は、このチャンネルのオーナーでは無いみたいです。\nチャンネルのビットレートを変更できるのは、このチャンネルの作者の先生だけです！",
                    ephemeral=True,
                    delete_after=30,
                )
        except Exception as e:
            await ctx.response.send_message(
                f"不明なエラーが発生してしまったみたいです...\nエラーメッセージ: {e}",
                ephemeral=True,
                delete_after=30,
            )

    else:
        await ctx.response.send_message(
            "ボイスチャンネルに参加していないみたいです...", ephemeral=True, delete_after=30
        )


@tree.command(name="limit", description="ボイスチャンネルの最大参加人数を変更できます。", guild=guild)
async def limit(ctx: discord.Interaction, num: discord.app_commands.Range[int, 2, 99]):
    if ctx.user.voice:
        try:
            if voice_channel_status[ctx.user.voice.channel.id] == ctx.user.id:
                await ctx.user.voice.channel.edit(user_limit=num)
                await ctx.response.send_message(
                    f"先生が参加しているボイスチャンネルの最大参加人数を「**{str(num)}人**」に変更しました！",
                    ephemeral=True,
                    delete_after=30,
                )
            else:
                await ctx.response.send_message(
                    f"{ctx.user.display_name}先生は、このチャンネルのオーナーでは無いみたいです。\n最大参加人数を変更できるのは、このチャンネルの作者の先生だけです！",
                    ephemeral=True,
                    delete_after=30,
                )
        except Exception as e:
            await ctx.response.send_message(
                f"不明なエラーが発生してしまったみたいです...\nエラーメッセージ: {e}",
                ephemeral=True,
                delete_after=30,
            )

    else:
        await ctx.response.send_message(
            "ボイスチャンネルに参加していないみたいです...", ephemeral=True, delete_after=30
        )


@discord.app_commands.choices(text=utils.choices_generate())
@tree.command(name="gacha", description="ガチャが引けます。100連が最大ですが、端数は端折られます。", guild=guild)
async def gacha(
    ctx: discord.Interaction, text: str, num: discord.app_commands.Range[int, 10, 100]
):
    result = gc.main(text, (num // 10) * 10)
    await ctx.response.send_message(embed=result)


def main():
    client.run(TOKEN)


if __name__ == "__main__":
    main()

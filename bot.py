
import asyncio
import random

import youtube_dl
import discord
from discord import user, reaction
from discord.ext import commands
import datetime

import json
stuff_that_gets_fished = ["fish", "rarefish", "jellyfish", "junk", "coinbomb", "sand", "seaweed", "exotic_fish", "pizza", "padlock", "phone", "laptop", "landmine"]
stuff_that_gets_hunted = ["rabbit", "boar", "bug", "junk", "skunk", "deer"]
from urllib import parse, request
import re

from discord.ext.commands import command, CheckFailure
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix="^", description='A Simple, Yet Complex Bot!')

mainshop = [{"name":"Landmine","price":33500,"description":"-Defense"},
            {"name":"Pizza","price":250000,"description":"-Powerup"},
            {"name":"Cheese", "price": 20000, "description": "-Powerup"},
            {"name":"Bread", "price": 2000, "description": "-Powerup"},
            {"name":"Fakeid", "price": 6000, "description": "-Spy"},
            {"name":"Phone", "price": 11200, "description": "-Communication"},
            {"name":"Fidget Spinner", "price": 90000, "description": "-Collectable"},
            {"name":"Candy", "price": 1000, "description": "-Powerup"},
            {"name":"Laptop", "price": 30000, "description": "-Communication"},
            {"name":"UFO Object", "price": 400000, "description": "-Exotic Collectable"},
            {"name":"Poster", "price": 10000, "description": "-Powerup"},
            {"name":"Padlock", "price": 16000, "description": "-Powerup"}]


@bot.command()
async def shop(ctx):
    em = discord.Embed(title="Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name=name, value=f"${price} | {desc}")

    await ctx.send(embed=em)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def test(ctx):
    await ctx.send('Hiiii')


@test.error
async def test_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@bot.command(aliases=["lb"])
async def leaderboard(ctx,x = 3):
    users = await get_bank_data()
    leader_board ={}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)

    em = discord.Embed(title=f"Top {x} Richest Players", description="The Richest Players In The World.")
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member1 = await bot.fetch_user(id_)
        name = member1.name
        em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)

# @bot.command()
# async def buy(ctx,item,amount = 1):
#     await open_account(ctx.author)
#
#     res = await buy_this(ctx.author,item,amount)
#
#     if not res[0]:
#         if res[1]==1:
#             await ctx.send("That object isn't there.")
#             return
#         if res[1]==2:
#             await ctx.send(f"You don't have enough money in your wallet to buy {amount}")
#     await ctx.send(f"You just bought {amount} {item}. Item transferred to you inventory.")
# #
# # @bot.command()
# # async def bag(ctx):
# #     await open_account(ctx.author)
# #     user = ctx.author
# #     users = await get_bank_data()
# #
# #     # try:
# #     #     inv1010101010 = users[str(user.id)]["inv"]
# #
# async def buy_this(user,item_name,amount):
#     item_name = item_name.lower()
#     name_ = None
#     for item in mainshop:
#         name = item["name"].lower()
#         if name == item_name:
#             name_ = name
#             price = item["price"]
#             break
#
#     if name_ == None:
#         return [False,1]
#
#     cost = price*amount
#
#     users = await get_bank_data()
#
#     bal = await update_bank(user)
#     inv1 = await update_inv(user)
#
#     try:
#         index = 0
#         t = None
#         for thing in users[str(user.id)]["inv"]:
#             n = thing["item"]
#             if n == item_name:
#                 old_amt = thing["amount"]
#                 new_amt = old_amt + amount
#                 users[str(user.id)]["bag"][index]["amount"] += new_amt
#                 t = 1
#                 break
#             index+=1
#         if t == None:
#             obj = {"item":item_name , "amount" : amount}
#             users[str(user.id)][f"{item_name}"] += {amount}
#             # users[str(user.id)]["bag"].append(obj)
#     except:
#         obj = {"item":item_name , "amount": amount}
#         users[str(user.id)]["bag"] = [obj]
#
#     with open("mainbank.json", "w") as f:
#         json.dump(users, f)
#
#     await update_bank(user,cost*-1,"wallet")
#
#     return [True,"Worked"]


@bot.command(aliases=["bal", "open_bal"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f"{ctx.author.name}'s balance",color=discord.Color.blue())
    em.add_field(name="Wallet Balance", value=f'{wallet_amt}')
    em.add_field(name="Bank Balance", value=f'{bank_amt}')
    await ctx.send(embed = em)

@balance.error
async def bal_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    earnings = random.randrange(101)

    await ctx.send(f'Someone gave you {earnings} coins')

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        users = json.dump(users, f)

@beg.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    daily = 25000

    await ctx.send(f'Here are your daily coins! 25,000 straight into your wallet!')

    users[str(user.id)]["wallet"] += daily

    with open("mainbank.json", "w") as f:
        users = json.dump(users, f)

@bot.command()
@commands.cooldown(1, 2678400, commands.BucketType.user)
async def monthly(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    monthly = 350000

    await ctx.send(f'Here are your daily coins! 350,000 straight into your wallet!')

    users[str(user.id)]["wallet"] += monthly

    with open("mainbank.json", "w") as f:
        users = json.dump(users, f)

@bot.command()
@commands.cooldown(1, 604800, commands.BucketType.user)
async def weekly(ctx):
    valid_users = ["749465698828288051"]
    if str(ctx.author.id) in valid_users:
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        weekly = 150000

        await ctx.send(f'Here are your weekly coins! 150000 straight into your wallet!')

        users[str(user.id)]["wallet"] += weekly

        with open("mainbank.json", "w") as f:
            users = json.dump(users, f)

    if str(ctx.author.id) not in valid_users:
        await ctx.send('``Error You Are Not A Supporter Of This Bot. Ergo You Do Not Get To Use This Command``')
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    users = await get_bank_data()
    userr = ctx.author
    if amount == None:
        await ctx.send("Please enter the amount.")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)


    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount, "bank")
    users[str(userr.id)]["bank"] -= amount
    users[str(userr.id)]["wallet"] += amount

    await ctx.send(f"You withdrew {amount} coins!")

    with open("mainbank.json", "w") as f:
        users = json.dump(users, f)

@withdraw.error
async def with_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 2700, commands.BucketType.user)
async def work(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    userr = ctx.author

    work_statements = ["BREAK IS OVER SO TO WORK", "HEY NOW ISNT NOT A TIME FOR JOKING AROUND", "HEY I WON THE LOTTERY", "MMM TIME TO LEAVE WORK"]
    Random_work_statement = random.choice(work_statements)

    await ctx.send(f"Work for Normal Officer - ``1 Hours of work``")
    bal = await update_bank(ctx.author)
    amount = random.randrange(15000)
    em = discord.Embed(title=f"**Great Work!**", description=f"You were given ⏣ {amount} for an hour of work.", color=discord.Color.blurple())
    em.set_footer(text="Working as a Normal Officer. CoolDown Initiated: 45 Minutes")
    await ctx.channel.send(embed=em)

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount, "bank")
    users[str(userr.id)]["wallet"] += amount

    with open("mainbank.json", "w") as f:
        users = json.dump(users, f)

@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def deposit(ctx,amountt = None):
    await open_account(ctx.author)
    users = await get_bank_data()
    userr = ctx.author
    if amountt == None:
        await ctx.send("Please enter the amount.")
        return

    bal = await update_bank(ctx.author)

    amountt = int(amountt)


    await update_bank(ctx.author,amountt)
    await update_bank(ctx.author,-1*amountt, "bank")
    users[str(userr.id)]["wallet"] -= amountt
    users[str(userr.id)]["bank"] += amountt

    await ctx.send(f"You deposited {amountt} coins!")

    with open("mainbank.json", "w") as f:
        users = json.dump(users, f)

@deposit.error
async def dep_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 7200, commands.BucketType.user)
async def bankrob(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    userr = ctx.author
    bal = await update_bank(ctx.author)


    amount = random.randrange(100000)
    steal_statements = ["You were caught. You lost ``20,000!``", f"You got away with ``{amount}``"]
    # Random_bank_statement = random.choice(steal_statements)
    choice1 = f"You got away with ``{amount}``"
    choice2 = 'You were caught. You lost ``20,000!``'
    Random_bank_choice = random.choice(steal_statements)

    if choice1 in Random_bank_choice:
        # choice1 = 'You got away with ``{amount}``'
        await ctx.send(f"{choice1}   :money_with_wings: ")
        await update_bank(ctx.author,amount)
        await update_bank(ctx.author,-1*amount, "bank")
        users[str(userr.id)]["wallet"] += amount
        with open("mainbank.json", "w") as f:
            users = json.dump(users, f)

    if choice2 in Random_bank_choice:
        ded_amount = 20000
        await ctx.send(f"{choice2}   :moneybag:  ")
        await update_bank(ctx.author,ded_amount)
        await update_bank(ctx.author,-1*ded_amount, "bank")
        users[str(userr.id)]["wallet"] -= ded_amount
        with open("mainbank.json", "w") as f:
            users = json.dump(users, f)

@bankrob.error
async def bankrob_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command(aliases=["inv", "open_inv"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def inventory(ctx):
    await init_inv(ctx.author)
    user = ctx.author

    users = await get_inv_data()
    fish_amt = users[str(user.id)]["fish"]
    rarefish_amt = users[str(user.id)]["rarefish"]
    jellyfish_amt = users[str(user.id)]["jellyfish"]
    junk_amt = users[str(user.id)]["junk"]
    coinbomb_amt = users[str(user.id)]["coinbomb"]
    boar_amt = users[str(user.id)]["boar"]
    rabbit_amt = users[str(user.id)]["rabbit"]
    bug_amt = users[str(user.id)]["bug"]
    skunk_amt = users[str(user.id)]["skunk"]
    deer_amt = users[str(user.id)]["deer"]
    seaweed_amt = users[str(user.id)]["seaweed"]
    sand_amt = users[str(user.id)]["sand"]
    hunt_amt = users[str(user.id)]["huntingrifle"]
    fishing_amt = users[str(user.id)]["fishingrod"]


    emoji = discord.utils.get(bot.emojis, name='rarefish')
    emoji1 = discord.utils.get(bot.emojis, name='junk')
    emoji2 = discord.utils.get(bot.emojis, name='sand')
    emoji3 = discord.utils.get(bot.emojis, name='jellyfish')
    emoji4 = discord.utils.get(bot.emojis, name='coinbomb')
    emoji5 = discord.utils.get(bot.emojis, name='common_fish')
    emoji6 = discord.utils.get(bot.emojis, name='common_bug')
    emoji7 = discord.utils.get(bot.emojis, name='rare_deer')
    emoji8 = discord.utils.get(bot.emojis, name='seaweed')
    emoji9 = discord.utils.get(bot.emojis, name='sand')
    emoji10 = discord.utils.get(bot.emojis, name='fishingrod')
    emoji11 = discord.utils.get(bot.emojis, name='huntingrifle')
    emoji12 = discord.utils.get(bot.emojis, name='UFO_object')
    emoji13 = discord.utils.get(bot.emojis, name='poster')
    emoji14 = discord.utils.get(bot.emojis, name='padlock')
    emoji15 = discord.utils.get(bot.emojis, name='laptop')
    emoji16 = discord.utils.get(bot.emojis, name='exotic_fish')
    emoji17 = discord.utils.get(bot.emojis, name='candy')
    emoji18 = discord.utils.get(bot.emojis, name='fidget_spinner')
    emoji19 = discord.utils.get(bot.emojis, name='phone')
    emoji20 = discord.utils.get(bot.emojis, name='fakeid')
    emoji21 = discord.utils.get(bot.emojis, name='fresh_bread')
    emoji22 = discord.utils.get(bot.emojis, name='cheese')
    emoji23 = discord.utils.get(bot.emojis, name='pizza')
    emoji24 = discord.utils.get(bot.emojis, name='landmine')

    ufo_amt = users[str(user.id)]["UFO_object"]
    poster_amt = users[str(user.id)]["poster"]
    padlock_amt = users[str(user.id)]["padlock"]
    laptop_amt = users[str(user.id)]["laptop"]
    efish_amt = users[str(user.id)]["exotic_fish"]
    fidget_spinner_amt = users[str(user.id)]["fidget_spinner"]
    candy_amt = users[str(user.id)]["candy"]
    fakeid_amt = users[str(user.id)]["fakeid"]
    phone_amt = users[str(user.id)]["phone"]
    bread_amt = users[str(user.id)]["bread"]
    cheese_amt = users[str(user.id)]["cheese"]
    pizza_amt = users[str(user.id)]["pizza"]
    landmine_amt = users[str(user.id)]["landmine"]

    emb = discord.Embed(title=f"{ctx.author.name}'s inventory",color=discord.Color.red())
    emb.add_field(name="``Landmine ``", value=(str(emoji24) + f'  {landmine_amt}'))
    emb.add_field(name="``Pizza ``", value=(str(emoji23) + f'  {pizza_amt}'))
    emb.add_field(name="``Cheese ``", value=(str(emoji22) + f'  {cheese_amt}'))
    emb.add_field(name="``Fresh bread ``", value=(str(emoji21) + f'  {bread_amt}'))
    emb.add_field(name="``Fakeid ``", value=(str(emoji20) + f'  {fakeid_amt}'))
    emb.add_field(name="``Phone ``", value=(str(emoji19) + f'  {phone_amt}'))
    emb.add_field(name="``Fidget Spinner ``", value=(str(emoji18) + f'  {fidget_spinner_amt}'))
    emb.add_field(name="``Candy ``", value=(str(emoji17) + f'  {candy_amt}'))
    emb.add_field(name="``Exotic Fish ``", value=(str(emoji16) + f'  {efish_amt}'))
    emb.add_field(name="``Laptop ``", value=(str(emoji15) + f'  {laptop_amt}'))
    emb.add_field(name="``UFO Object ``", value=(str(emoji12) + f'  {ufo_amt}'))
    emb.add_field(name="``Poster ``", value=(str(emoji13) + f'  {poster_amt}'))
    emb.add_field(name="``Padlock ``", value=(str(emoji14) + f'  {padlock_amt}'))
    emb.add_field(name="``Fish ``", value=(str(emoji5) + f'  {fish_amt}'))
    emb.add_field(name="``RareFish ``", value=(str(emoji) + f'  {rarefish_amt}'))
    emb.add_field(name="``JellyFish ``", value=(str(emoji3) + f'  {jellyfish_amt}'))
    emb.add_field(name="``Junk ``", value=(str(emoji1) + f'  {junk_amt}'))
    emb.add_field(name="``Seaweed ``", value=(str(emoji8) + f'  {seaweed_amt}'))
    emb.add_field(name="``Coinbomb ``", value=(str(emoji4) + f'  {coinbomb_amt}'))
    emb.add_field(name="``Rabbit ``", value=f' :rabbit2:     {rabbit_amt}')
    emb.add_field(name="``Boar ``", value=f' :boar:    {boar_amt}')
    emb.add_field(name="``Bug ``", value=(str(emoji6) + f'    {bug_amt}'))
    emb.add_field(name="``Skunk ``", value=f' :skunk:     {skunk_amt}')
    emb.add_field(name="``Deer ``", value=(str(emoji7) + f'    {deer_amt}'))
    emb.add_field(name="``Sand ``", value=(str(emoji9) + f'    {sand_amt}'))
    emb.add_field(name="``Fishing Rod ``", value=(str(emoji10) + f'    {fishing_amt}'))
    emb.add_field(name="``Hunting Rifle ``", value=(str(emoji11) + f'    {hunt_amt}'))

    await ctx.send(embed = emb)

@inventory.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)

async def buy_landmine(ctx, amount : int):
    landmine_sell_amount = 33500
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    final = landmine_sell_amount*amount
    userr = ctx.author
    choice22 = f"You bought {amount} landmines!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"landmine")
    users[str(userr.id)]["landmine"] += amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] -= final
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@buy_landmine.error
async def landmine(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def buy_pizza(ctx, amount : int):
    pizza_sell_amount = 250000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    final = pizza_sell_amount*amount
    choice22 = f"You bought {amount} pizzas!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"pizza")
    users[str(userr.id)]["pizza"] += amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] -= final
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@buy_pizza.error
async def pizza(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def buy_cheese(ctx, amount : int):
    cheese_sell_amount = 20000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    final = cheese_sell_amount*amount
    choice22 = f"You bought {amount} cheese!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"cheese")
    users[str(userr.id)]["cheese"] += amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] -= final
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@buy_cheese.error
async def cheese(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def buy_bread(ctx, amount : int):
    bread_sell_amount = 2000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    final = bread_sell_amount*amount
    userr = ctx.author
    choice22 = f"You bought {amount} bread!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"bread")
    users[str(userr.id)]["bread"] += amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] -= final
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@buy_bread.error
async def bread(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def buy_fakeid(ctx, amount : int):
    fakeid_sell_amount = 6000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    final = fakeid_sell_amount*amount
    userr = ctx.author
    choice22 = f"You bought {amount} fakeid!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"fakeid")
    users[str(userr.id)]["fakeid"] += amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] -= final
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@buy_fakeid.error
async def fakeid(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def buy_phone(ctx, amount : int):
    phone_sell_amount = 11200
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    final = phone_sell_amount*amount
    choice22 = f"You bought {amount} phones!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"phone")
    users[str(userr.id)]["phone"] += amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] -= final
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@buy_phone.error
async def phoe(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def buy_fidget_spinner(ctx, amount : int):
    fidget_spinner_sell_amount = 90000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    final = fidget_spinner_sell_amount*amount
    userr = ctx.author
    choice22 = f"You bought {amount} fidger_spinner!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"fidget_spinner")
    users[str(userr.id)]["fidget_spinner"] += amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] -= fidget_spinner_sell_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@buy_fidget_spinner.error
async def fidget(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def buy_candy(ctx, amount : int):
    cndy_sell_amount = 1000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    final = cndy_sell_amount*amount
    userr = ctx.author
    choice22 = f"You bought {amount} candy!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"candy")
    users[str(userr.id)]["candy"] += amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] -= final
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@buy_candy.error
async def candy(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def buy_laptop(ctx, amount : int):
    laptop_sell_amount = 30000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    final = laptop_sell_amount*amount
    choice22 = f"You bought {amount} laptop!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"laptop")
    users[str(userr.id)]["laptop"] += amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] -= final
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@buy_laptop.error
async def laptop(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def buy_ufo_object(ctx, amount : int):
    ufo_sell_amount = 400000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    final = ufo_sell_amount*amount
    userr = ctx.author
    choice22 = f"You bought {amount} ufo objects!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"UFO_object")
    users[str(userr.id)]["UFO_object"] += amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] -= final
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@buy_ufo_object.error
async def ufo(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def buy_poster(ctx, amount : int):
    poster_sell_amount = 400000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    final = poster_sell_amount*amount
    userr = ctx.author
    choice22 = f"You bought {amount} posters!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"poster")
    users[str(userr.id)]["poster"] += amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += final
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@buy_poster.error
async def poster(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def buy_padlock(ctx, amount : int):
    pad_sell_amount = 16000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    final = pad_sell_amount*amount
    userr = ctx.author
    choice22 = f"You bought {amount} padlocks!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"padlock")
    users[str(userr.id)]["padlock"] += amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] -= final
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@buy_padlock.error
async def padlock(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def use_landmine(ctx, amount : int):
    lvl_amount = 15.0
    await init_inv(ctx.author)
    await open_account(ctx.author)
    await open_level(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    usersss = await get_level_data()
    userr = ctx.author
    choice22 = f"You used {amount} landmine!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"landmine")
    users[str(userr.id)]["landmine"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        usersss[str(userr.id)]["damage_level"] += lvl_amount
        with open("level.json", "w") as f:
            usersss = json.dump(usersss, f)

@use_landmine.error
async def ulandmine(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def use_pizza(ctx, amount : int):
    lvl_amount = 10.0
    await init_inv(ctx.author)
    await open_account(ctx.author)
    await open_level(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    usersss = await get_level_data()
    userr = ctx.author
    choice22 = f"You used {amount} pizza!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"pizza")
    users[str(userr.id)]["pizza"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        usersss[str(userr.id)]["level"] += lvl_amount
        with open("level.json", "w") as f:
            usersss = json.dump(usersss, f)

@use_pizza.error
async def upizza(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def use_cheese(ctx, amount : int):
    lvl_amount = 2.0
    await init_inv(ctx.author)
    await open_account(ctx.author)
    await open_level(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    usersss = await get_level_data()
    userr = ctx.author
    choice22 = f"You used {amount} cheese!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"cheese")
    users[str(userr.id)]["cheese"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        usersss[str(userr.id)]["level"] += lvl_amount
        with open("level.json", "w") as f:
            usersss = json.dump(usersss, f)

@use_cheese.error
async def usecheese_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

#
# @bot.command()
# async def use_fakeid(ctx, amount : int):
#     lvl_amount = 1.0
#     await init_inv(ctx.author)
#     await open_account(ctx.author)
#     await open_level(ctx.author)
#     userss = await get_bank_data()
#     users = await get_inv_data()
#     usersss = await get_level_data()
#     usersrs = await get_active_items()
#     await open_active_items(ctx.author)
#     thing = "**Fake ID** - 1d"
#     userr = ctx.author
#     await ctx.send(f"{ctx.author.mention} dont worry you are safe with your fake id.")
#     await update_active_items(ctx.author, thing, f"items")
#     usersrs[str(userr.id)]["items"] += thing
#     with open("active_items.json", "w") as a:
#         users = json.dump(users, a)
#         choice22 = f"You used {amount} fakeids!"
#         await ctx.send(f"{choice22}")
#         await update_inv(ctx.author, amount, f"fakeid")
#         users[str(userr.id)]["fakeid"] -= amount
#         with open("inv.json", "w") as w:
#             users = json.dump(users, w)
#             usersss[str(userr.id)]["stealth_level"] += lvl_amount
#             with open("level.json", "w") as f:
#                 usersss = json.dump(usersss, f)


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def use_candy(ctx, amount : int):
    lvl_amount = 0.5
    await init_inv(ctx.author)
    await open_account(ctx.author)
    await open_level(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    usersss = await get_level_data()
    userr = ctx.author
    choice22 = f"You used {amount} candys!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"candy")
    users[str(userr.id)]["candy"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        usersss[str(userr.id)]["level"] += lvl_amount
        with open("level.json", "w") as f:
            usersss = json.dump(usersss, f)

@use_candy.error
async def candy_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def use_poster(ctx, amount : int):
    lvl_amount = 0.5
    await init_inv(ctx.author)
    await open_account(ctx.author)
    await open_level(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    usersss = await get_level_data()
    userr = ctx.author
    choice22 = f"You used {amount} posters!"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"poster")
    users[str(userr.id)]["poster"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        usersss[str(userr.id)]["level"] += lvl_amount
        with open("level.json", "w") as f:
            usersss = json.dump(usersss, f)

@use_poster.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@bot.command()
@commands.cooldown(1, 35, commands.BucketType.user)
async def fish(ctx):
    random_fish_Choose = random.choice(stuff_that_gets_fished)
    item_amount = random.randrange(1, 5)
    await init_inv(ctx.author)
    users = await get_inv_data()
    userr = ctx.author

    buy_rod_amount = 1
    choice22 = f"You cast out your line and brought back ``{item_amount} {random_fish_Choose}``!"
    fishtime = users[str(userr.id)]["fishingrod"]
    if fishtime>0:
        choice22 = f"You cast out your line and brought back ``{item_amount} {random_fish_Choose}``!"
        await ctx.send(f"{choice22}")
        await update_inv(ctx.author, item_amount, f"{random_fish_Choose}")
        users[str(userr.id)][f"{random_fish_Choose}"] += item_amount
        with open("inv.json", "w") as w:
            users = json.dump(users, w)
    else:
        await ctx.send('You do not have a fishing rod. Buy one using the command. ``^buy_rod``')

@bot.command()
async def buy_rod(ctx):
    await init_inv(ctx.author)
    users = await get_inv_data()
    userr = ctx.author
    await open_account(ctx.author)
    userss = await get_bank_data()
    buy_amount = 1
    fish_cost = 18000
    await ctx.send('You have just bought a fishing rod. Fish command unlocked: ``^fish``')
    await update_inv(ctx.author, buy_amount, "fishingrod")
    users[str(userr.id)]["fishingrod"] += buy_amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] -= fish_cost
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)



@bot.command()
async def buy_rifle(ctx):
    await init_inv(ctx.author)
    users = await get_inv_data()
    userr = ctx.author
    await open_account(ctx.author)
    userss = await get_bank_data()
    buy_amount = 1
    hunt_cost = 15000
    await ctx.send('You have just bought a hunting rifle. Hunt command unlocked: ``^hunt``')
    await update_inv(ctx.author, buy_amount, "huntingrifle")
    users[str(userr.id)]["huntingrifle"] += buy_amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] -= hunt_cost
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@bot.command()
@commands.cooldown(1, 35, commands.BucketType.user)
async def hunt(ctx):

    random_hunt_Choose = random.choice(stuff_that_gets_hunted)
    await init_inv(ctx.author)
    users = await get_inv_data()
    userr = ctx.author
    hunttime = users[str(userr.id)]["huntingrifle"]
    hunt_amount = random.randrange(1, 5)
    if hunttime>0:
        choice22 = f"You went hunting in the woods and brought back {hunt_amount}``{random_hunt_Choose}!``!"
        await ctx.send(f"{choice22}")
        await update_inv(ctx.author, hunt_amount, f"{random_hunt_Choose}")
        users[str(userr.id)][f"{random_hunt_Choose}"] += hunt_amount
        with open("inv.json", "w") as w:
            users = json.dump(users, w)
    else:
        await ctx.send('You do not have a hunting rifle. Buy one using the command. ``^buy_rifle``')




@bot.command()
async def sell_sand(ctx, amount : int):
    sand_sell_amount = 1000
    await init_inv(ctx.author)
    users = await get_inv_data()
    userr = ctx.author
    await open_account(ctx.author)
    money_amount = sand_sell_amount * amount
    userss = await get_bank_data()
    userrr = ctx.author
    choice22 = f"You sold {amount} sand! For ⏣ {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"sand")
    users[str(userr.id)]["sand"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userrr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_sand.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_rarefish(ctx, amount : int):
    rarefish_sell_amount = 1000
    await init_inv(ctx.author)
    users = await get_inv_data()
    userr = ctx.author
    await open_account(ctx.author)
    money_amount = rarefish_sell_amount * amount
    userss = await get_bank_data()
    userrr = ctx.author
    choice22 = f"You sold {amount} rarefish! For ⏣ {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"rarefish")
    users[str(userr.id)]["rarefish"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userrr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_rarefish.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error
@bot.command()
async def sell_fish(ctx, amount : int):
    fish_sell_amount = 400
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    money_amount = fish_sell_amount*amount
    choice22 = f"You sold {amount} fish! For ⏣ {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"fish")
    users[str(userr.id)]["fish"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)
@sell_fish.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_landmine(ctx, amount : int):
    landmine_sell_amount = 3350
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    money_amount = amount*landmine_sell_amount
    choice22 = f"You sold {amount} landmines! For ⏣ {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"landmine")
    users[str(userr.id)]["landmine"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_landmine.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_pizza(ctx, amount : int):
    pizza_sell_amount = 25000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    money_amount = amount*pizza_sell_amount
    choice22 = f"You sold {amount} pizzas! For ⏣ {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"pizza")
    users[str(userr.id)]["pizza"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_pizza.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_cheese(ctx, amount : int):
    cheese_sell_amount = 2000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    money_amt = cheese_sell_amount*amount
    choice22 = f"You sold {amount} cheese! For ⏣ {money_amt}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"cheese")
    users[str(userr.id)]["cheese"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amt
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_cheese.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_bread(ctx, amount : int):
    bread_sell_amount = 200
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    m_amt = amount*bread_sell_amount
    choice22 = f"You sold {amount} bread! For ⏣ {m_amt}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"bread")
    users[str(userr.id)]["bread"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += m_amt
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_bread.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_fakeid(ctx, amount : int):
    fakeid_sell_amount = 600
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    money_amt = amount*fakeid_sell_amount
    choice22 = f"You sold {amount} fakeid! For ⏣ {money_amt}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"fakeid")
    users[str(userr.id)]["fakeid"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amt
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)
@sell_fakeid.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_phone(ctx, amount : int):
    phone_sell_amount = 1120
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    money_amt = amount*phone_sell_amount
    choice22 = f"You sold {amount} phones! For ⏣ {money_amt}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"phone")
    users[str(userr.id)]["phone"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_phone.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_fidget_spinner(ctx, amount : int):
    fidget_spinner_sell_amount = 9000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    money_amt = amount*fidget_spinner_sell_amount
    choice22 = f"You sold {amount} fidger_spinner! For ⏣ {money_amt}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"fidget_spinner")
    users[str(userr.id)]["fidget_spinner"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amt
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_fidget_spinner.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_candy(ctx, amount : int):
    cndy_sell_amount = 100
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    money_amt = amount*cndy_sell_amount
    choice22 = f"You sold {amount} candy! For ⏣ {money_amt}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"candy")
    users[str(userr.id)]["candy"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amt
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_candy.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_efish(ctx, amount : int):
    efish_sell_amount = 15000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author

    money_amt = amount*efish_sell_amount
    choice22 = f"You sold {amount} exotic fish! For ⏣ {money_amt}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"exotic_fish")
    users[str(userr.id)]["exotic_fish"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amt
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_efish.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_laptop(ctx, amount : int):
    laptop_sell_amount = 3000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    money_amt = amount*laptop_sell_amount
    choice22 = f"You sold {amount} laptop! For ⏣ {money_amt}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"laptop")
    users[str(userr.id)]["laptop"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amt
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_laptop.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_ufo_object(ctx, amount : int):
    ufo_sell_amount = 40000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    money_amt = amount*ufo_sell_amount
    choice22 = f"You sold {amount} ufo objects! For ⏣ {money_amt}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"UFO_object")
    users[str(userr.id)]["UFO_object"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amt
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_ufo_object.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@bot.command()
async def sell_poster(ctx, amount : int):
    poster_sell_amount = 40000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    userr = ctx.author
    money_amt = amount*poster_sell_amount
    choice22 = f"You sold {amount} posters! For ⏣ {money_amt}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"poster")
    users[str(userr.id)]["poster"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amt
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_poster.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_padlock(ctx, amount : int):
    pad_sell_amount = 4000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    money_amt = amount*pad_sell_amount
    userr = ctx.author
    choice22 = f"You sold {amount} padlocks!  For ⏣ {money_amt}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"padlock")
    users[str(userr.id)]["padlock"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amt
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_padlock.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_jellyfish(ctx, amount : int):
    jellyfish_sell_amount = 6600
    await init_inv(ctx.author)
    users = await get_inv_data()
    await open_account(ctx.author)
    userss = await get_bank_data()
    userr = ctx.author
    money_amount = jellyfish_sell_amount * amount
    choice22 = f"You sold {amount} jellyfish! For ⏣ {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"jellyfish")
    users[str(userr.id)]["jellyfish"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_jellyfish.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_junk(ctx, amount : int):
    junk_sell_amount = 500
    await init_inv(ctx.author)
    users = await get_inv_data()
    await open_account(ctx.author)
    userss = await get_bank_data()
    money_amount = junk_sell_amount * amount
    userr = ctx.author
    choice22 = f"You sold {amount} junk! For ⏣ {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"junk")
    users[str(userr.id)]["junk"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_junk.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_seaweed(ctx, amount : int):
    seaweed_sell_amount = 2000
    await init_inv(ctx.author)
    await open_account(ctx.author)
    userss = await get_bank_data()
    users = await get_inv_data()
    money_amount = seaweed_sell_amount * amount
    userr = ctx.author
    choice22 = f"You sold {amount} seaweed! For ⏣ {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"seaweed")
    users[str(userr.id)]["seaweed"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_seaweed.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_coinbomb(ctx, amount: int):
    coinbomb_sell_amount = 6600
    await open_account(ctx.author)
    userss = await get_bank_data()
    await init_inv(ctx.author)
    money_amount = coinbomb_sell_amount * amount
    users = await get_inv_data()
    userr = ctx.author
    choice22 = f"You sold {amount} coinbomb! For ⏣ {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"coinbomb")
    users[str(userr.id)]["coinbomb"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_coinbomb.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_rabbit(ctx, amount: int):
    rabbit_sell_amount = 6600
    await open_account(ctx.author)
    userss = await get_bank_data()
    await init_inv(ctx.author)
    users = await get_inv_data()
    money_amount = rabbit_sell_amount * amount
    userr = ctx.author
    choice22 = f"You sold {amount} rabbit! For ⏣ {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"rabbit")
    users[str(userr.id)]["rabbit"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_rabbit.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_boar(ctx, amount: int):
    boar_sell_amount = 12000
    await open_account(ctx.author)
    userss = await get_bank_data()
    await init_inv(ctx.author)
    users = await get_inv_data()
    money_amount = boar_sell_amount * amount
    userr = ctx.author
    choice22 = f"You sold {amount} boar! For ⏣ {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"boar")
    users[str(userr.id)]["boar"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_boar.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_bug(ctx, amount: int):
    bug_sell_amount = 200
    await open_account(ctx.author)
    userss = await get_bank_data()
    await init_inv(ctx.author)
    money_amount = bug_sell_amount * amount
    users = await get_inv_data()
    userr = ctx.author
    choice22 = f"You sold {amount} bug! For ⏣ {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"bug")
    users[str(userr.id)]["bug"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_bug.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_skunk(ctx, amount: int):
    skunk_sell_amount = 3200
    await open_account(ctx.author)
    userss = await get_bank_data()
    await init_inv(ctx.author)
    users = await get_inv_data()
    userr = ctx.author
    money_amount = skunk_sell_amount * amount
    choice22 = f"You sold {amount} skunk! For⏣  {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"skunk")
    users[str(userr.id)]["skunk"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_skunk.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command()
async def sell_deer(ctx, amount: int):
    deer_sell_amount = 13000
    await open_account(ctx.author)
    userss = await get_bank_data()
    await init_inv(ctx.author)
    users = await get_inv_data()
    userr = ctx.author
    money_amount = deer_sell_amount * amount
    choice22 = f"You sold {amount} deer! For ⏣ {money_amount}"
    await ctx.send(f"{choice22}")
    await update_inv(ctx.author, amount, f"deer")
    users[str(userr.id)]["deer"] -= amount
    with open("inv.json", "w") as w:
        users = json.dump(users, w)
        userss[str(userr.id)]["wallet"] += money_amount
        with open("mainbank.json", "w") as f:
            userss = json.dump(userss, f)

@sell_deer.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error

@bot.command(aliases=["info"])
async def level(ctx):
    await open_level(ctx.author)
    user = ctx.author
    await open_account(ctx.author)
    userss = await get_bank_data()
    await init_inv(ctx.author)
    users = await get_inv_data()
    await init_inv(ctx.author)
    usersss = await get_level_data()
    coins_amt = userss[str(user.id)]["wallet"]
    bankc_amt = userss[str(user.id)]["bank"]
    lvl_amt = usersss[str(user.id)]["level"]
    stealth_lvl_amt = usersss[str(user.id)]["stealth_level"]
    rich_level = coins_amt / 100000
    dmg_lvl_amt = usersss[str(user.id)]["damage_level"]
    user_items = users[str(user.id)]
    total_items = 0

    for key in user_items:
        total_items += user_items[key]
    # for key in active_amt:


#■■□□□□□□□□
    Percentage_amt = random.randrange(1, 99)
    net = coins_amt*1.2
    em = discord.Embed(title=f"{ctx.author.name}'s profile",color=discord.Color.red())
    em.add_field(name="**Level**", value=f'``{lvl_amt}`` \n ■■■□□□□□□')
    em.add_field(name="**Coins**", value=f'**Wallet**: ⏣ {coins_amt} \n **Bank**: ⏣ {bankc_amt} \n **Net**: ⏣ {net} \n **Multi**: {Percentage_amt}%')
    em.add_field(name="**Inventory**", value=f'``{total_items}`` items. (24 total).')
    em.add_field(name="**Misc**", value=f'Works as a Normal Officer. \n Rich: {rich_level}')
    em.add_field(name="**Stealth Level**", value=f'{stealth_lvl_amt}')
    em.add_field(name="**Damage Level**", value=f'{dmg_lvl_amt}')
    await ctx.send(embed = em)




@monthly.error
async def monthy_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@weekly.error
async def week_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@daily.error
async def daily_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@hunt.error
async def hunt_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@fish.error
async def fish_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f} seconds'.format(error.retry_after)
        await ctx.send(msg)
    else:
        raise error


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        users = json.dump(users, f)
    return True

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users

async def update_bank(user,change = 0,mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return user



async def init_inv(user):

    users = await get_inv_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["fish"] = 0
        users[str(user.id)]["sand"] = 0
        users[str(user.id)]["rarefish"] = 0
        users[str(user.id)]["jellyfish"] = 0
        users[str(user.id)]["junk"] = 0
        users[str(user.id)]["coinbomb"] = 0
        users[str(user.id)]["rabbit"] = 0
        users[str(user.id)]["boar"] = 0
        users[str(user.id)]["bug"] = 0
        users[str(user.id)]["skunk"] = 0
        users[str(user.id)]["deer"] = 0
        users[str(user.id)]["seaweed"] = 0
        users[str(user.id)]["huntingrifle"] = 0
        users[str(user.id)]["fishingrod"] = 0
        users[str(user.id)]["UFO_object"] = 0
        users[str(user.id)]["poster"] = 0
        users[str(user.id)]["padlock"] = 0
        users[str(user.id)]["laptop"] = 0
        users[str(user.id)]["exotic_fish"] = 0
        users[str(user.id)]["fidget_spinner"] = 0
        users[str(user.id)]["candy"] = 0
        users[str(user.id)]["fakeid"] = 0
        users[str(user.id)]["phone"] = 0
        users[str(user.id)]["bread"] = 0
        users[str(user.id)]["cheese"] = 0
        users[str(user.id)]["pizza"] = 0
        users[str(user.id)]["landmine"] = 0

    with open("inv.json", "w") as w:
        users = json.dump(users, w)

    return True

async def get_inv_data():
    with open("inv.json", "r") as w:
        users = json.load(w)

    return users


async def update_inv(user, items, mode):

    users = await get_inv_data()

    users[str(user.id)][mode] += items

    with open("inv.json", "w") as w:
        json.dump(users, w)

    return user



async def open_level(user):

    users = await get_level_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["level"] = 0
        users[str(user.id)]["stealth_level"] = 0
        users[str(user.id)]["damage_level"] = 0

    with open("level.json", "w") as r:
        users = json.dump(users, r)
    return True

async def get_level_data():
    with open("level.json", "r") as r:
        users = json.load(r)

    return users


async def update_level(user, items, mode):

    users = await get_level_data()

    users[str(user.id)][mode] += items

    with open("level.json", "w") as r:
        json.dump(users, r)

    return user

#

bot.run(TOKEN)
import discord
import os
import gspread
import datetime
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
from discord.ext import commands, tasks
from discord import guild, embeds, Embed, Bot, SlashCommand, slash_command, InteractionResponse
intents = discord.Intents.all()
client = commands.Bot(command_prefix = '$', intents = intents, case_insensitive = True)
gc = gspread.service_account(filename = "paranoid-kp-bot-43a1e7152411.json") # replace with the service account for the bot in googles apis (https://docs.gspread.org/en/latest/oauth2.html)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1JwbiWu68ZE0gCfDUTqsTAs3l2QwfhPDX2d95ZrLAxFw/edit#gid=597740150") # replace with the master sheet for para
ws = sh.get_worksheet(0) # points tracking
ws2 = sh.get_worksheet(1) # boss attend tracking
ws3 = sh.get_worksheet(2) # loot win tracking
akp_bosses = {"rev": 5, "unox5": 5,"unox6": 15,"base": 30,"prime": 45,"gele": 90,"bt":0,"dino": 0,"factions":10,"baseloss": 15,"primeloss": 22.5,"geleloss": 45,"btloss":0,"dinoloss": 0}
bkp_bosses = {"rev": 3, "unox5": 3,"unox6": 5,"base": 10,"prime": 15,"gele": 30,"bt":90,"dino": 0,"factions":10,"baseloss": 5,"primeloss": 7.5,"geleloss": 15,"btloss":45,"dinoloss": 0}
dkp_bosses = {"rev": 1, "unox5": 1,"unox6": 5,"base": 5,"prime": 10,"gele": 20,"bt":30,"dino": 90,"factions":10,"baseloss": 2.5,"primeloss": 5,"geleloss": 10,"btloss":15,"dinoloss": 45}
guilds=[814048353603813376,1116453904922726544] 
bot = discord.Bot(debug_guilds = guilds)

@client.command(guild_ids = guilds)
async def info(ctx):
    embed = discord.Embed(title = "Info Dump", colour=discord.Color.orange())
    embed.add_field(name = "Bosses", value = "rev, unox5, unox6, base, prime, gele, bt, dino, factions", inline = True)
    embed.add_field(name = "Lost Bosses", value = "baseloss, primeloss, geleloss, btloss, dinoloss", inline = True)
    await ctx.send(embed=embed)

@client.command(guild_ids = guilds)
async def addmem(ctx, name):
    user_list = ws.col_values(1)
    if name not in user_list:
        body =[name,0,0,0,0,0,0,0,0,0]
        ws.append_row(body)
        await ctx.send(name + " was added to the list")
    else:
        await ctx.send(name + " is already in the list!")


@client.command(guild_ids = guilds)
async def leaderboard(ctx, kp, number):
    if int(number) > 100:
        await ctx.send("bot is configured for 100 players max")
    else:
        kp = kp.upper()
        embed = discord.Embed(title = kp + " Leaderboard top " + str(number), colour=discord.Color.orange())
        if kp == "AKP":
            kplist = ws.col_values(2)
            namelist = ws.col_values(1)
            del kplist[0]
            del namelist[0]
            floatkplist = list(map(float, kplist))
            comblist = list(zip(namelist,floatkplist))
            sortedkplist = sorted(comblist,reverse=True,key=lambda xkp: xkp[1])
            for i in range(int(number)):
                embed.add_field(name =  sortedkplist[i][0], value = sortedkplist[i][1], inline = False)
        if kp == "BKP":
            kplist = ws.col_values(3)
            namelist = ws.col_values(1)
            del kplist[0]
            del namelist[0]
            floatkplist = list(map(float, kplist))
            comblist = list(zip(namelist,floatkplist))
            sortedkplist = sorted(comblist,reverse=True,key=lambda xkp: xkp[1])
            for i in range(int(number)):
                embed.add_field(name =  sortedkplist[i][0], value = sortedkplist[i][1], inline = False)
        if kp == "DKP":
            kplist = ws.col_values(4)
            namelist = ws.col_values(1)
            del kplist[0]
            del namelist[0]
            floatkplist = list(map(float, kplist))
            comblist = list(zip(namelist,floatkplist))
            sortedkplist = sorted(comblist,reverse=True,key=lambda xkp: xkp[1])
            for i in range(int(number)):
                embed.add_field(name =  sortedkplist[i][0], value = sortedkplist[i][1], inline = False)
        await ctx.send(embed=embed)

@client.command(guild_ids = guilds)
async def lifeleaderboard(ctx, kp, number):
    if int(number) > 100:
        await ctx.send("bot is configured for 100 players max")
    else:
        kp = kp.upper()
        embed = discord.Embed(title = "lifetime " + kp + " Leaderboard top " + str(number), colour=discord.Color.orange())
        if kp == "AKP":
            kplist = ws.col_values(8)
            namelist = ws.col_values(1)
            del kplist[0]
            del namelist[0]
            floatkplist = list(map(float, kplist))
            comblist = list(zip(namelist,floatkplist))
            sortedkplist = sorted(comblist,reverse=True,key=lambda xkp: xkp[1])
            for i in range(int(number)):
                embed.add_field(name =  sortedkplist[i][0], value = sortedkplist[i][1], inline = False)
        if kp == "BKP":
            kplist = ws.col_values(9)
            namelist = ws.col_values(1)
            del kplist[0]
            del namelist[0]
            floatkplist = list(map(float, kplist))
            comblist = list(zip(namelist,floatkplist))
            sortedkplist = sorted(comblist,reverse=True,key=lambda xkp: xkp[1])
            for i in range(int(number)):
                embed.add_field(name =  sortedkplist[i][0], value = sortedkplist[i][1], inline = False)
        if kp == "DKP":
            kplist = ws.col_values(10)
            namelist = ws.col_values(1)
            del kplist[0]
            del namelist[0]
            floatkplist = list(map(float, kplist))
            comblist = list(zip(namelist,floatkplist))
            sortedkplist = sorted(comblist,reverse=True,key=lambda xkp: xkp[1])
            for i in range(int(number)):
                embed.add_field(name =  sortedkplist[i][0], value = sortedkplist[i][1], inline = False)
        await ctx.send(embed=embed)

@client.command(guild_ids = guilds)
async def win(ctx, kp, members):
    kp = kp.lower()
    user_list = ws.col_values(1)
    memlist = members.split(",")
    winnerlist = []
    for mem in memlist:
        if mem in user_list:
            cell = ws.find(mem.lower())
            row_num = cell.row
            if kp == "akp":
                winnerlist.append((mem,float(ws.cell(row_num, 2).value)))
            if kp == "bkp":
                winnerlist.append((mem,float(ws.cell(row_num, 3).value)))
            if kp == "dkp":
                winnerlist.append((mem,float(ws.cell(row_num, 4).value)))
    sortedkplist = sorted(winnerlist,reverse=True,key=lambda xkp: xkp[1])
    await ctx.send("Winner: " + sortedkplist[0][0])

@client.command(guild_ids = guilds)
async def reap(ctx, playername, kp, perc, itemname):
    user_list = ws.col_values(1)
    playername = playername.lower()
    kp = kp.upper()
    if playername in user_list:
        cell = ws.find(playername)
        row_num = cell.row
        if kp == "AKP":
            akp = ws.cell(row_num, 2).value
            nkp = float(akp) * (100 - float(perc)) / 100
            ws.update_cell(row_num, 2, nkp)
            newreaped = float(ws.cell(row_num, 5).value) + round(float(akp) - float(nkp), 2)
            ws.update_cell(row_num, 5, newreaped)
        if kp == "BKP":
            akp = ws.cell(row_num, 3).value
            nkp = float(akp) * (100 - float(perc)) / 100
            ws.update_cell(row_num, 3, nkp)
            newreaped = float(ws.cell(row_num, 6).value) + round(float(akp) - float(nkp), 2)
            ws.update_cell(row_num, 6, newreaped)
        if kp == "DKP":
            akp = ws.cell(row_num, 4).value
            nkp = float(akp) * (100 - float(perc)) / 100
            ws.update_cell(row_num, 4, nkp)
            newreaped = float(ws.cell(row_num, 7).value) + round(float(akp) - float(nkp), 2)
            ws.update_cell(row_num, 7, newreaped)
        msg = f"{playername} has been reaped for {round(float(akp) - float(nkp), 2)}, {perc}% of their {kp} for {itemname}"
        ws3.append_row([f"commanduser: {ctx.message.author} at {datetime.datetime.now().strftime('%a %d %b %Y, %I:%M%p')} " + msg])
        await ctx.send(msg)
    else:
        await ctx.send(f"{playername} not in list! No Points reaped")

@client.command(guild_ids = guilds)
async def boss(ctx, name, members):
    memlist = list(members.split(","))
    emb_msg = ''
    user_list = ws.col_values(1)
    name = name.lower()
    ratelimit = False
    #await ctx.defer()
    for mem in memlist:
            if mem in user_list:
                try:
                    if mem not in emb_msg:
                        cell = ws.find(mem.lower())
                        row_num = cell.row
                        akp = ws.cell(row_num, 2).value
                        bkp = ws.cell(row_num, 3).value
                        dkp = ws.cell(row_num, 4).value
                        nakp = float(akp) + akp_bosses[name]
                        nbkp = float(bkp) + bkp_bosses[name]
                        ndkp = float(dkp) + dkp_bosses[name]
                        ws.update_cell(row_num, 2, nakp)
                        ws.update_cell(row_num, 3, nbkp)
                        ws.update_cell(row_num, 4, ndkp)
                        emb_msg += mem + ' '
                    else:
                        await ctx.send(mem + " added multiple times on this attendance, credited once")
                except:
                    ratelimit = True
            else:
                await ctx.send(f"{mem} not in list!")
    if ratelimit:
        await ctx.send("An error occurred, likely rate limit hit. Please wait a minute and add the rest of the players on this attendance then")
    if emb_msg != '':
        embed = discord.Embed(title = f" {name} point update", description = f"{emb_msg} have gained {akp_bosses[name]} AKP, {bkp_bosses[name]} BKP, {dkp_bosses[name]} DKP", colour= 0x3498db)
        ws2.append_row([f"commanduser: {ctx.message.author} at {datetime.datetime.now().strftime('%a %d %b %Y, %I:%M%p')} {emb_msg} have gained {akp_bosses[name]} AKP, {bkp_bosses[name]} BKP, {dkp_bosses[name]} DKP"])
    elif emb_msg == '':
        embed = discord.Embed(title = "No valid users found!")
    await ctx.send(embed=embed)

@client.command(guild_ids = guilds)
async def bossminus(ctx, name, members):
    memlist = list(members.split(","))
    emb_msg = ''
    user_list = ws.col_values(1)

    #await ctx.defer()
    for mem in memlist:
            if mem in user_list:
                cell = ws.find(mem)
                row_num = cell.row
                akp = ws.cell(row_num, 2).value
                bkp = ws.cell(row_num, 3).value
                dkp = ws.cell(row_num, 4).value
                nakp = float(akp) - akp_bosses[name]
                nbkp = float(bkp) - bkp_bosses[name]
                ndkp = float(dkp) - dkp_bosses[name]
                ws.update_cell(row_num, 2, nakp)
                ws.update_cell(row_num, 3, nbkp)
                ws.update_cell(row_num, 4, ndkp) 
                emb_msg += mem + ' '

            else:
                await ctx.send(f"{mem} not in list!")
    if emb_msg != '':
        embed = discord.Embed(title = f" {name} point update", description = f"{emb_msg} have lost {akp_bosses[name]} AKP, {bkp_bosses[name]} BKP, {dkp_bosses[name]} DKP", colour= 0x3498db)
        ws2.append_row([f"commanduser: {ctx.message.author} at {datetime.datetime.now().strftime('%a %d %b %Y, %I:%M%p')}{emb_msg} have lost {akp_bosses[name]} AKP, {bkp_bosses[name]} BKP, {dkp_bosses[name]} DKP"])
    elif emb_msg == '':
        embed = discord.Embed(title = "No valid users found!")
    await ctx.send(embed=embed)

@client.command()
async def points(ctx, clanmem):
    user = str(clanmem).lower()
    user_list = ws.col_values(1)
    if user in user_list:
        
        ind = user_list.index(user) +1
        user_points = ws.row_values(ind)
        embed = discord.Embed(title = f"{user}'s points", colour=discord.Color.orange())
        embed.add_field(name = "AKP", value = user_points[1], inline = True)
        embed.add_field(name = "BKP", value = user_points[2], inline = False)
        embed.add_field(name = "DKP", value = user_points[3], inline = False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("User not found!")
client.run(TOKEN)
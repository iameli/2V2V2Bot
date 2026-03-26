import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random

load_dotenv()


############ Weapons Tables #############

LightW = [
"Light Sniper",
"Light Throwing Knives",
"Light M11",
"Light LH1",
"Light M26 Matter",
"Light Blunderbuss",
"Light ARN-220",
"Light Dagger",
"Light 93R",
"Light Sword",
"Light Bow",
"Light V95",
"Light XP-54"
]

MediumW = [
"Medium AKM",
"Medium Model 1887",
"Medium Famas",
"Medium Dual Blades",
"Medium Cerberus",
"Medium CL-40",
"Medium Crossbow"
"Medium P90",
"Medium CB-01 Repeater",
"Medium Shield",
"Medium Pike",
"Medium R. 357 Revolver",
"Medium FCAR"
]

HeavyW = [
"Heavy .50 Akimbo",
"Heavy MiniGun",
"Heavy SHAK50",
"Heavy KS-23",
"Heavy Flamethrower",
"Heavy MGL32",
"Heavy BFR Titan",
"Heavy Spear ",
"Heavy SledgeHammer",
"Heavy Lewis Gun",
"Heavy SA1216",
"Heavy M60"
]


Weapons = LightW + MediumW + HeavyW


############ Abilities Tables #############

Abilities = [
"Light Invis",
"Light Dash",
"Light Grapple",
"Medium Turret",
"Medium Heal",
"Medium Wibble",
"Medium Boop",
"Heavy Shield",
"Heavy Chain",
"Heavy Smash",
"Heavy Goo"
]

############ Silly Modes Tables #############


Modes = [
"Snipers and Stabbers - One sniper, One backstabber",
"Live by the blade, die by the blade - One Minigun, One dual blades",
"https://youtu.be/YPX__g3LpUY?t=10 - No weapons or equipment with gunpowder",
"TF2 Special - Medium Heal Beam and Heavy Minigun",
"Chaos - One medium grenade launcher, One Heavy Grenade Launcher",
"Flame On - One Cerebus and One Flamethrower",
"GUN TIME"
]

############ Tokens and Functions #############

token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding = 'utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print("We are ready to go")



@bot.command(name="two", aliases=["Two", "TWO", "dos", "DOS"])
async def two_v_check(ctx):
    # Check if the user is actually in a voice channel
    if ctx.author.voice and ctx.author.voice.channel:
        voice_channel = ctx.author.voice.channel
        member_count = len(voice_channel.members)
        
        # Calculate how many more are needed for 6 people (2v2v2)
        needed = 6 - member_count
        
        if needed <= 0:
            await ctx.send(f"We have {member_count} people! Lets fucking go!")
        else:
            await ctx.send(f"We are {needed} away from 2v2v2s.")
    else:
        await ctx.send("You need to be in a voice channel to use this command!")



@bot.command(name="ability", aliases=["abilities", "Ability", "Abilities", "ABILITY", "ABILITIES"])
async def rand_ability(ctx, count: int = 1):
    if ctx.author.voice and ctx.author.voice.channel:
        # Limit count so the message doesn't get too long/broken
        count = max(1, min(count, 5)) 
        
        members = ctx.author.voice.channel.members
        lines = []
        
        for member in members:
            # random.sample picks multiple UNIQUE items from the list
            selected = random.sample(Abilities, count)
            # Join the choices with " | "
            choices_str = " | ".join(selected)
            lines.append(f"**{member.display_name}** -- {choices_str}")
        
        await ctx.send("\n".join(lines))
    else:
        await ctx.send("You need to be in a voice channel first!")



@bot.command(name="weapon", aliases=["WEAPON", "weapons", "Weapons", "WEAPONS"])
async def rand_weapon(ctx, count: int = 1):
    if ctx.author.voice and ctx.author.voice.channel:
        count = max(1, min(count, 5))
        
        members = ctx.author.voice.channel.members
        lines = []
        
        for member in members:
            # Using random.sample to ensure they don't get the same gun twice
            selected = random.sample(Weapons, count)
            choices_str = " | ".join(selected)
            lines.append(f"**{member.display_name}** -- {choices_str}")
        
        await ctx.send("\n".join(lines))
    else:
        await ctx.send("You need to be in a voice channel first!")



@bot.command(name="teams", aliases=["TEAMS", "Teams", "team", "Team", "TEAM"])
async def split_teams(ctx, num_teams: int):
    # 1. Check if user is in a voice channel
    if not ctx.author.voice or not ctx.author.voice.channel:
        return await ctx.send("You need to be in a voice channel to split teams!")

    members = ctx.author.voice.channel.members
    
    # 2. Basic validation
    if num_teams <= 1:
        return await ctx.send("You need at least 2 teams!")
    if num_teams > len(members):
        return await ctx.send(f"Not enough people to make {num_teams} teams!")

    # 3. Shuffle the list of people
    random.shuffle(members)

    # 4. Create the teams
    teams = [[] for _ in range(num_teams)]
    for i, member in enumerate(members):
        teams[i % num_teams].append(member.display_name)

    # 5. Format the output
    response = "📊 **Teams Generated:**\n"
    for i, team_members in enumerate(teams):
        response += f"**Team {i+1}:** {', '.join(team_members)}\n"
    await ctx.send(response)

@bot.command(name="class", aliases=["Class", "CLASS"])
async def rand_all_classes(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        members = ctx.author.voice.channel.members
        lines = []
        
        for member in members:
            # Pick one
            l_pick = random.choice(LightW)
            m_pick = random.choice(MediumW)
            h_pick = random.choice(HeavyW)
            
            # Combine them with the | separator
            choices_str = f"{l_pick} | {m_pick} | {h_pick}"
            lines.append(f"**{member.display_name}** -- {choices_str}")
        
        await ctx.send("\n".join(lines))
    else:
        await ctx.send("You need to be in a voice channel first!")


@bot.command(name="mode", aliases=["Mode", "modes", "MODES", "Chodes"])
async def pick_mode(ctx):
    selected_mode = random.choice(Modes)
    
    # Check if Gun Time rolled
    if selected_mode == "GUN TIME":
        # Pull one random weapon from your big Weapons list
        bonus_weapon = random.choice(Weapons)
        response = f"**{selected_mode}** (Weapon: **{bonus_weapon}**)"
    else:
        # Standard response for regular modes
        response = f"**{selected_mode}**"
        
    await ctx.send(response)





bot.run(token, log_handler=handler, log_level=logging.DEBUG)
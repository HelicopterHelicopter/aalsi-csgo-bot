from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")

def get_matches(url):
    headers = {'User-Agent':'DiscordDOTAbot/v1.0(jhljheel@gmail.com)'}
    response = requests.get(url,headers=headers)
    content = response.content
    page_html = response.json()['parse']['text']['*']
    
    soup = BeautifulSoup(page_html,"lxml")
    games = []
    matches = soup.find_all('table',class_="wikitable wikitable-striped infobox_matches_content")
    for match in matches:
        game = {}
        cells = match.find_all("td")
        try:
            game['team1'] = cells[0].find('span',class_='team-template-text').find('a').get('title')
            game['team2'] = cells[2].find('span',class_='team-template-text').find('a').get('title')
            game['start_time'] = cells[3].find('span',class_='timer-object').get_text()
            game['tournament'] = cells[3].find('div').get_text()

            try:
                game['twitch_channel'] = cells[3].find('span',class_="timer-object".get('data-stream-twitch'))
            except AttributeError:
                pass

            games.append(game)

        except AttributeError:
            continue

    return games

url = "https://liquipedia.net/counterstrike/api.php?action=parse&format=json&page=Liquipedia:Matches"


notable_teams = ["Ninjas in Pyjamas","BIG","G2 Esports","Complexity Gaming","FaZe Clan","Team Liquid","OG","Astralis","Natus Vincere","Team Vitality","MOUZ"]

def get_notable_matches(matches):
    imp_matchs = []
    for match in matches:
        if match['team1'] in notable_teams or match['team2'] in notable_teams:
            imp_matchs.append(match)

    return imp_matchs

#def UTC_to_IST(DateTime):
#    date_time_list = DateTime.split('-')

def get_tournaments():
    tournament_url = "https://liquipedia.net/counterstrike/api.php?action=parse&format=json&page=S-Tier_Tournaments"
    headers = {'User-Agent':'DiscordDOTAbot/v1.0(jhljheel@gmail.com)'}
    response = requests.get(tournament_url,headers=headers)
    content = response.content
    page_html = response.json()['parse']['text']['*']
    soup = BeautifulSoup(page_html,"lxml")
    tournament_allyears = soup.find_all('div',attrs={'class':'divTable table-full-width tournament-card'})
    latest_year = tournament_allyears[0]
    tournaments_html = latest_year.find_all('div',class_='divRow')
    tournaments = []
    for tournament in tournaments_html:
        tournament_data = {}
        tournament_data['name'] = tournament.find('div',attrs={'class':'divCell Tournament Header'}).find('b').get_text()
        tournament_data['date'] = tournament.find('div',attrs={'class':'divCell EventDetails Date Header'}).get_text()
        tournament_data['prizepool'] = tournament.find('div',attrs={'class':'divCell EventDetails Prize Header'}).get_text()
        tournaments.append(tournament_data)

    return tournaments


@bot.event
async def on_ready():
    print("Bot is online.")

@bot.command()
async def match(ctx):
    matches = get_matches(url)

    imp_matches = get_notable_matches(matches)
    l = len(imp_matches)
    actual_l = int(l/2)
    actual_imp_matches = imp_matches[0:actual_l]
    embed = discord.Embed(title="Upcoming CSGO matches")
    embed.set_thumbnail(url="https://i.pinimg.com/originals/b1/02/24/b10224ae75edd5debd06c44662cbcb30.png")
    embed.set_author(name="Aalsi CSGO Bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="Jai Aalsi CSGO")

    for match in actual_imp_matches:
        team1 = match["team1"]
        team2 = match["team2"]
        match_time = match["start_time"]
        tournament = match['tournament']
        embed.add_field(name=f"{team1} vs {team2}",value=f"Match starts at {match_time}.\n {tournament}")

    await ctx.send(embed=embed)
    

@bot.command()
async def tournaments(ctx):
    tournaments = get_tournaments()
    embed = discord.Embed(title="Current Year CSGO tournament schedule")
    embed.set_thumbnail(url="https://i.pinimg.com/originals/b1/02/24/b10224ae75edd5debd06c44662cbcb30.png")
    embed.set_author(name="Aalsi CSGO bot", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="Only S-tier tournaments. Jai Aalsi CSGO")

    for tournament in reversed(tournaments):
        tournament_name = tournament['name']
        date = tournament['date']
        prizepool = tournament['prizepool']
        embed.add_field(name=tournament_name,value=f"Dates- {date} with a prizepool of {prizepool}")

    await ctx.send(embed=embed)
    
@bot.command()
async def helicopter(ctx):
    await ctx.send("HELIKOPTER 🚁 HELIKOPTER 🚁 HELIKOPTER 🚁HELIKOPTER🚁 HELIKOPTER 🚁HELIKOPTER 🚁PARAKOFER 🚁HELIKOPTER🚁 HELIKOPTER 🚁HELIKOPTER🚁 HELIKOPTER 🚁 HELIKOPTER 🚁 HELIKOPTER 🚁 HELIKOPTER 🚁 HELIKOPTER 🚁 HELIKOPTER 🚁 HELIKOPTER 🚁 HELIKOPTER 🚁 HELIKOPTER")


bot.run(DISCORD_TOKEN)

import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pytz import timezone
import traceback

def get_webpage():
    url = "https://kyberscorner.com/destiny2/lost-sectors/"
    data = requests.get(url).text
    soup = bs(data, 'html.parser')
    return soup

# Returns table containing lost sector information
def get_table(soup):
    x = 0
    for table in soup.find_all('table'):
        if x == 3:
            return(table)
        x+=1
        
def is_today(date):
    format = '%m/%d/%Y'
    datetime_object = datetime.strptime(date, format)
    date = datetime_object.strftime(format)
    tz = timezone('US/Eastern')
    today = datetime.now(tz)
    today = today.strftime(format)
    
    if (date == today):
        return True
    else:
        return False

# Returns link of lost sector image
def get_link():
    first = True
    table = get_table(get_webpage())
    for row in table.tbody.find_all('tr'):
        columns = row.find_all('td')
        
        if first:
            first = False
            continue
        
        if (columns != []):
            date = columns[0].text.strip()
            
            if (is_today(date)):
                link = [a['href'] for a in columns[1].find_all('a', href=True) if a.text][0]
                return link

class ls(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @tasks.loop(seconds=1800)
    async def lost_sector(self):
        try:
            tz = timezone('US/Eastern')
            time = datetime.now(tz)
            hour = time.hour
            
            # Send message at 1pm EST (When the lost sector is changed)
            if hour == 13:
                channel = self.client.get_channel(987140972301393951)
                today = datetime.today().strftime('%m/%d/%Y')
                embed=discord.Embed(description=f"**Daily Lost Sector ({today})**", color=discord.Colour.random())
                embed.set_image(url=get_link())
                await channel.send(embed=embed)
        except:
            print(traceback.format_exc())
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.lost_sector.start()

def setup(client):
    client.add_cog(ls(client))
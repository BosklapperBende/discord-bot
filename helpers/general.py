import requests
from datetime import datetime, time, timedelta
import asyncio
import random

type_of_jokes = {
  'alg':	'algemene mop',
  'arts':	'doktermop',
  'be':	'mop over Belgen',
  'mu':	'muziekmop',
  'nl':	'mop over Hollanders',
  'one':	'oneliner',
  'xxx':	'seksistische mop'
}

def get_live_scores():
  rows = []
  url = "https://prod-public-api.livescore.com/v1/api/react/live/soccer/0.00?MD=1"
  jsonData = requests.get(url).json()
  for stage in jsonData['Stages']:
    if "CompId" in stage.keys():
      if stage["CompId"] in ["54", "73", "65"]:
        rows.append(stage["CompN"] + ":")
        events = stage['Events']
        for event in events:
          homeTeam = event['T1'][0]['Nm']
          homeScore = event['Tr1']

          awayTeam = event['T2'][0]['Nm']
          awayScore = event['Tr2']

          matchClock = event['Eps']

          string = "\n>\t{} - {} ({}')\t[{} - {}]".format(
            homeTeam, awayTeam, matchClock, homeScore, awayScore)
          rows.append(string)
  return rows

async def wait_until_time(uur: int, wait_on_monday: bool = False):
    now = datetime.utcnow()
    if ((wait_on_monday) & (datetime.today().weekday() != 0)) | (now.time() > time(uur,0,0)):  
      tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
      seconds = (tomorrow - now).total_seconds()  
      await asyncio.sleep(seconds)  
    while True:
      now = datetime.utcnow() 
      target_time = datetime.combine(now.date(), time(uur,0,0)) 
      seconds_until_target = (target_time - now).total_seconds()
      await asyncio.sleep(seconds_until_target) 
      return 

def get_joke():
  cat_id, description = random.choice(list(type_of_jokes.items()))
  url = "http://api.apekool.nl/services/jokes/getjoke.php?type={}".format(cat_id)
  jsonData = requests.get(url).json()
  return (description, jsonData['joke'])

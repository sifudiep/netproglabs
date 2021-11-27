from urllib import request
from datetime import date, timedelta
import re, json, sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()


days = 10
for i in range(days):
    # 1. Fetch HTML data from https://www.svtplay.se/kanaler?date=2021-11-30
    url = f"https://www.svtplay.se/kanaler?date={date.today() + timedelta(days=i)}"

    data = request.urlopen(url).read()
    html = data.decode("UTF-8")

    # 2. Use Regex to find data regarding Rapport

    # Get JSON data inside SCRIPT tag as STRING
    stringJson = re.findall(r'<script id="__NEXT_DATA__" type=?"application\/json">(.*?)<\/script>', html)

    # Convert JSON string to JSON Object
    data = json.loads(stringJson[0])['props']['urqlState']
    value = list(data.values())[0]

    # Convert JSON String inside data parameter to JSON OBJECT
    channels = json.loads(value['data'])['channels']['channels']

    for channel in channels:
        channelId = channel['id']
        for program in channel['schedule']:
            if (program['name'] == "Rapport"):
                print("----------------------")
                print(program['start'].split('T')[0])
                print(program['name'])
                print(channelId)
                print(program['startTime'])
                print(program['subHeading'])
                print(program['description'])

                c.execute("INSERT OR IGNORE INTO emissions (name, startTime, subHeading, description, airingDate) VALUES (?, ?, ?, ?, ?)", (program['name'], program['startTime'], program['subHeading'], program['description'], program['start'].split('T')[0]))


conn.commit()
conn.close()
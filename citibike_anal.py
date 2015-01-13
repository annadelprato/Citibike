#citibike_analysis
#imports

import pandas as pd
import sqlite3 as lite
import collections
import requests
import datetime


#access SQL3 as lite
con = lite.connect('citi_bike.db')
cur = con.cursor()

#read in the data
#Note: SQL query is embedded in the function and the index column for the DataFrame is set to the value of the execution time.
df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

id_bikes = collections.defaultdict(int)

r = requests.get('http://www.citibikenyc.com/stations/json')
r.json()
r.json()
r.json().keys()
r.json()['stationBeanList']

for station in r.json()['stationBeanList']:
    id_bikes[station['id']] = station['availableBikes']


hour_change = collections.defaultdict(int)
for col in df.columns:
    station_vals = df[col].tolist()
    station_id = col[1:] #trim the "_"
    station_change = 0
    for k,v in enumerate(station_vals):
        if k < len(station_vals) - 1:
            station_change += abs(station_vals[k] - station_vals[k+1])
hour_change[int(station_id)] = station_change #convert the station id back to integer

def keywithmaxval(d):
    # create a list of the dict's keys and values; 
        v = list(d.values())
        k = list(d.keys())
        return k[v.index(max(v))] 

# assign the max key to max_station
max_station = keywithmaxval(hour_change)

#query sqlite for reference information
cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print "The most inactive station is station id %s at %s latitude: %s longitude: %s " % data
#print "With " + str(hour_change[379]) + " bicycles coming and going in the hour between " + datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S') + " and " + datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')
print "With " + str(hour_change[379]) + " bicycles coming and going in the hour between " + datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%H:%M:%S') + " and " + datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%H:%M:%S')

import matplotlib.pyplot as plt

plt.bar(hour_change.keys(), hour_change.values())
plt.show()

#The most inactive station is 3002 at South End Ave and Liberty Street longitude: 40.711512 and latitude: -74.015756 with 0 bicycles coming and 
#going in the hour between 2:15:02 and 5:35:01.
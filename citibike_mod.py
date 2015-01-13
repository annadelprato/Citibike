#import time
#pauses program of number of specified seconds
#time.sleep(60)

#pushes code in for loop that runs 60 times (once per minute)

#for i in range(60):
    #insert code here
    #time.sleep(60) 

#completed code should look "something"like this    
import time
from dateutil.parser import parse
import collections
import sqlite3 as lite
import requests

con = lite.connect('citi_bike.db')
cur = con.cursor()

for i in range(60):
    r = requests.get('http://www.citibikenyc.com/stations/json')
    exec_time = parse(r.json()['executionTime'])

    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime("%H" "%M" "%S"),))
    con.commit()

    id_bikes = collections.defaultdict(int)
    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']

    for k, v in id_bikes.iteritems():
        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime("%H" "%M" "%S") + ";")
    con.commit()

    time.sleep(60)

con.close() #close the database connection when done
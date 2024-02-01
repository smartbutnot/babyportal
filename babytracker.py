import os
import sqlite3
import paho.mqtt.client as mqtt

# Function to publish message to MQTT
def publish_mqtt(topic, message):
    client = mqtt.Client()
    client.username_pw_set("USERNAME","PASSWORD") # replace with your MQTT broker username and password
    client.connect("IPADDRESS", 1883)  # Replace with your MQTT broker address and port

    client.publish(topic, message)
    client.disconnect()

# Check if file exists
file_path = '/root/babytracker.db'  # Replace with your SQLite database file path
if not os.path.exists(file_path):
    print("File does not exist.")
    exit()

# List of queries with corresponding MQTT topics
queries = [
    {
        # Total time spent breastfeeding today (i.e. on the current date)
        "query": "select IFNULL(SUM(LeftDuration+RightDuration+BothDuration),0) from Nursing where strftime('%Y%m%d', DATETIME(Time,'unixepoch')) = strftime('%Y%m%d', 'now');",
        "topic": "baby/nursing"
    },
    {
        # Total time spent breastfeeding on the left side today
        "query": "select IFNULL(SUM(LeftDuration),0) from Nursing where strftime('%Y%m%d', DATETIME(Time,'unixepoch')) = strftime('%Y%m%d', 'now');",
        "topic": "baby/nursingleft"
    },
    {
        # Total time spent breastfeeding on the right side today
        "query": "select IFNULL(SUM(RightDuration),0) from Nursing where strftime('%Y%m%d', DATETIME(Time,'unixepoch')) = strftime('%Y%m%d', 'now');",
        "topic": "baby/nursingright"
    },
    {
        # Total time spent bottle feeding today
        "query": "select CAST(SUM(Amount) AS INTEGER) from Pumped where strftime('%Y%m%d', DATETIME(Time,'unixepoch')) = strftime('%Y%m%d', 'now');",
        "topic": "baby/bottle"
    },
    {
        # Number of poos (nappyies logged as either "dirty" or "mixed") today
        "query": "select COUNT(status) from Diaper where amount>0 AND status>0 AND strftime('%Y%m%d', DATETIME(Time,'unixepoch')) = strftime('%Y%m%d', 'now');",
        "topic": "baby/poo"
    },
    {
        # Number of wees (nappyies logged as either "wet" or "mixed") today
        "query": "select COUNT(status) from Diaper where amount>0 AND strftime('%Y%m%d', DATETIME(Time,'unixepoch')) = strftime('%Y%m%d', 'now');",
        "topic": "baby/wee"
    },
    {
        # ml of milk pumped today
        "query": "select IFNULL(CAST(SUM(Amount) AS INTEGER),0) from Pump where strftime('%Y%m%d', DATETIME(Time,'unixepoch')) = strftime('%Y%m%d', 'now');",
        "topic": "baby/pumping"
    },
    {
        # Hours and minutes since last feed (breast or bottle)
        "query": "select strftime('%H:%M',time((strftime('%s','now')-Time),'unixepoch')),Time from Nursing UNION select strftime('%H:%M',time((strftime('%s','now')-Time),'unixepoch')),Time from Pumped ORDER by Time DESC LIMIT 1;",
        "topic": "baby/lastfeed"
    },
    {
        # Hours and minutes since last nappy
        "query": "select strftime('%H:%M',time((strftime('%s','now')-Time),'unixepoch')) from Diaper ORDER by Time DESC LIMIT 1;",
        "topic": "baby/lastnappy"
    }

    # Add more queries with topics as needed
]

# Connect to SQLite database
conn = sqlite3.connect(file_path)
cursor = conn.cursor()

# Execute queries and publish results to respective topics
for item in queries:
    query = item["query"]
    topic = item["topic"]
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            # Publish result to MQTT topic
            publish_mqtt(topic, str(result[0]))
        else:
            print(f"No results for query: {query}")
    except sqlite3.Error as e:
        print(f"Error executing query: {query}\nError: {e}")

# Close database connection
conn.close()

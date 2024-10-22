import json
import ciso8601
import os

json_file = os.environ.get("JSON_FILE")

with open(json_file, 'r') as f:
    data = json.load(f)

msg_count = len(data["messages"])
cur_count = 0

start_raw_ts = data["messages"][0]["timestamp"]
start_ts = ciso8601.parse_datetime(start_raw_ts)

print(f"Session Start: {start_ts.strftime('%a %b %d %H:%M:%S %Y')}")

old_ts = None

for msg in data["messages"]:
    content = msg["content"].replace("\n", " -|- ")
    raw_ts = msg["timestamp"]
    author = msg["author"]["name"]

    ts = ciso8601.parse_datetime(raw_ts)

    if old_ts is None:
        old_ts = ts

    if old_ts.day != ts.day:
        print(f"Session Time: {ts.strftime('%a %b %d %H:%M:%S %Y')}")

    old_ts = ts
    time = ts.strftime("%H:%M")
    print(f"[{time}] <{author}> {content}")
    cur_count += 1

    if cur_count == msg_count:
        print(f"Session End: {ts.strftime('%a %b %d %H:%M:%S %Y')}")

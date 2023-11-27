import json
import random

n = 100
floors = 20

random.seed(1004)
requests = []
for i in range(n):
    source, destination = random.randint(1, floors), random.randint(1, floors)
    while source == destination:
        destination = random.randint(1, floors)
    requests.append({"time": random.randint(0, 10), "id": i, "source": source, "dest": destination})

requests.sort(key= lambda x: x["time"])

with open("long_sample.json", "w") as f:
    for r in requests:
        f.write(json.dumps(r) + "\n")  

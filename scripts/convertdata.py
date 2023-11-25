import requests
import json
url = "https://gist.githubusercontent.com/max107/6571147/raw/1849675dceead974319c02214456565ad6e77164/Regions.json"

a = requests.get(url)

csv_ = ["State,Unemployment,Name"]

b= a.json()
print(len(b))

done = {"type":"FeatureCollection","features":[]}

for j,i in enumerate(b):
    csv_.append(f"A{j},{1+j/10},{i}")
    done["features"].append({"type":"Feature","id":f"A{j}","properties":{"name":i},"geometry":{"type":"Polygon","coordinates":[[[i[1],i[0]] for i in b[i]["0"]]]}})

with open("russia.json", 'w',encoding="utf-8",) as f:
    f.write(json.dumps(done))
    
with open("russia.csv", 'w',encoding="utf-8",) as f:
    f.write('\n'.join(csv_))
    
    

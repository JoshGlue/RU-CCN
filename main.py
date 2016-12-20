import requests as r
import json

livedata = r.get("https://www.google.com/finance/info?q=AMS:HEIA,AMS:AGN,AMS:AD,AMS:AKZA,AMS:MT,AMS:ASML,AMS:BAMNB,AMS:BOKA,AMS:DSM,AMS:FUR,AMS:HEIA,AMS:HEIO,AMS:RDSA,AMS:RDSB")
livedata = livedata.text.replace("//", "")
livedata = json.loads(livedata)
print(livedata)
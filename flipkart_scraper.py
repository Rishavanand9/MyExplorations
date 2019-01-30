from lxml import html
import requests
import time
import json

output=[]

for i in range(1,51):
    page = "https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=" + str(i)
    data = requests.get(page)
    time.sleep(0.100)

    doc = html.fromstring(data.content)
    mobiles = doc.xpath('//a[@class="_31qSD5"]')
    time.sleep(0.100)

    
    for j in range(len(mobiles)):

        m = mobiles[j].xpath('.//div[@class="_1-2Iqu row"]')
        name = m[0].xpath('.//div[@class="_3wU53n"]/text()')
        specs = m[0].xpath('.//li[@class="tVe95H"]/text()')
        price=m[0].xpath('.//div[@class="_1vC4OE _2rQ-NK"]/text()')
        time.sleep(0.100)
        resp = {}
        resp['Name'] = name[0]
        resp['Specs'] = specs
        resp['Price'] = price[0]
        output.append(resp)
        
with open('Mobiles.json','w') as outfile:
    json.dump(output,outfile,indent=4,ensure_ascii=False)
print(len(output))
 

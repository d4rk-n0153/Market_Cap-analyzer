from bs4 import BeautifulSoup as bsp
import json
import requests as rq
import jdatetime as jd
from pandas import *
from time import sleep
urls=[]
market_cap=[]

Symbols_counts=int(input('Please enter the number of your desired symbol: '))
dat=input('Please enter the desired date: ').split('/')
sym=[input(f'pls type ur symbol {i}: ') for i in range (1,Symbols_counts+1)]
gdate=str(jd.date(int(dat[0]),int(dat[1]),int(dat[2])).togregorian()).replace('-','')


headers={
        #Accept: */*
        #Accept-Encoding: gzip, deflate
        'Accept-Language':'en-US',
        #'Cache-Control': 'no-cache',
        #'Connection':'keep-alive',
        #'Cookie':'_ga=GA1.2.1843003826.1607405830; _gid=GA1.2.864430428.1624673785; __qca=P0-1856150858-1624680910808; ASP.NET_SessionId=be4aok1ffxxnmkyogchg2qmt; _gat_gtag_UA_63076930_1=1',
        #'Host': 'cdn.tsetmc.com',
        #'Pragma': 'no-cache',
        #Referer: http://cdn.tsetmc.com/Loader.aspx?ParTree=15131P&i=46348559193224090&d=20210621
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    }
url='https://d4rk-n0153.github.io/tsetmc/market-watch2.html'
#url='http://tradersarena.ir/data/market-watch?mt=0&fi=none&_=1624808150318'

response=rq.get(url)

data=json.loads(response.content.decode('utf-8-sig'))


#symbols=[data[0].get(b) for i in range (0,len(data))]
nums=[data[0].get(b) for b in sym]
dick=dict(zip(sym,nums))


for k in sym:
    urls.append(f'http://cdn.tsetmc.com/Loader.aspx?ParTree=15131P&i={dick.get(k)}&d={gdate}')
for s in range(len(urls)):
    responses=rq.get(urls[s])
    if 'ClosingPriceData=[]' not in responses.text and 'GeneralError.aspx' not in responses.text and responses.status_code==200:
        soup=bsp(responses.text,'html.parser')
        s1=soup.select('script')
        a=((((str(s1[4])).replace('<script>var InstSimpleData=', '')).replace('</script>','')).split(';'))
        Total_share=int((a[0].split(','))[8])
        last_price=((((str(s1[5]).split(';'))[1]).split(','))[-10]).replace("'","")
        market_cap.append((int(last_price)*int(Total_share)))
        
        print(urls[s])
    else:
        while  'GeneralError.aspx?' in responses.text or responses.status_code!=200:
            sleep(1)
            responses=rq.get(urls[s])
            print(urls[s]+':error code is: '+ str(responses.status_code))
            if 'ClosingPriceData=[]' not in responses.text and 'GeneralError.aspx' not in responses.text and responses.status_code==200:
                 
                 soup=bsp(responses.text,'html.parser')
                 s1=soup.select('script')
                 a=((((str(s1[4])).replace('<script>var InstSimpleData=', '')).replace('</script>','')).split(';'))
                 Total_share=int((a[0].split(','))[8])
                 last_price=((((str(s1[5]).split(';'))[1]).split(','))[-10]).replace("'","")
                 market_cap.append((int(last_price)*int(Total_share)))
            if 'ClosingPriceData=[]'  in responses.text and 'GeneralError.aspx' not in responses.text and responses.status_code==200:
                 market_cap.append(None)
                 continue
                 

df=DataFrame(index=(sym),columns=(sym))
df.insert(len(market_cap),'ارزش بازار(میلیارد تومان)','none')

for num1 in range(len(market_cap)):
    for num2 in range(len(market_cap)):
        df.loc[str(sym[num1]),str(sym[num2])]=(market_cap[num1]/market_cap[num2])
        df.loc[str(sym[num1]),'ارزش بازار(میلیارد تومان)']=round(market_cap[num1]/10000000000)
               
writer=ExcelWriter('MarketCap.xlsx', mode='w')
df.to_excel(writer,sheet_name=gdate)
writer.save()
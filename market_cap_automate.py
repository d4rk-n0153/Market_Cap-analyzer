from json import loads as l
import requests as rq
import jdatetime as jd
from pandas import *

url_ztitad=[]
url_lastprice=[]
total_shares=[]
lastPrices=[]
Symbols_counts=int(input('Please enter the number of your desired symbol: '))
dat=input('Please enter the desired date: ').split('/')
sym=[input(f'pls type ur symbol {i}: ') for i in range (1,Symbols_counts+1)]
gdate=str(jd.date(int(dat[0]),int(dat[1]),int(dat[2])).togregorian()).replace('-','')


url_database='https://d4rk-n0153.github.io/tsetmc/market-watch2.html'


response=rq.get(url)

data=l(response.content.decode('utf-8-sig'))




nums=[data[0].get(b) for b in sym]
dick=dict(zip(sym,nums))


for k in sym:
    urlztitad=f'http://cdn.tsetmc.com/api/Instrument/GetInstrumentHistory/{dick.get(k)}/{gdate}'
    urllastprice=f'http://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceHistory/{dick.get(k)}/{gdate}'
    if urlztitad not in url_ztitad:
        url_ztitad.append(urlztitad)
    if urllastprice not in url_lastprice:
        url_lastprice.append(urllastprice)
for ztitad in range(len(url_ztitad)):
    response_zTitad=rq.get(url_ztitad[ztitad])
    total_share=l(response_zTitad.text)['instrumentHistory'].get('zTitad')
    total_shares.append(total_share)
for last_price in range(len(url_lastprice)):
    response_lastprice=rq.get(url_lastprice[last_price])
    lastPrice=l(response_lastprice.text)['closingPriceHistory'][0].get('pClosing')
    lastPrices.append(lastPrice)

market_cap=[lastPrices[i]*total_shares[i]/(10000000000) for i in range(len(lastPrices))]
                         
df=DataFrame(index=(sym),columns=(sym))
df.insert(len(market_cap),'ارزش بازار(میلیارد تومان)','none')
for num1 in range(len(market_cap)):
    for num2 in range(len(market_cap)):
            df.loc[str(sym[num1]),str(sym[num2])]=(market_cap[num1]/market_cap[num2])
            df.loc[str(sym[num1]),'ارزش بازار(میلیارد تومان)']=round(market_cap[num1])
                   
writer=ExcelWriter('MarketCap.xlsx', mode='w')
df.to_excel(writer,sheet_name=gdate)
writer.save()
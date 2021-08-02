import pandas as pd
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

def get_comments(target_address):
    result = []
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    html = requests.get(target_address)
    soup = BeautifulSoup(html.text, 'html.parser')
    posts = soup.find_all('div', {'class' : 'comment_content__AvzPV'})
    for i in posts:
        result.append(i.text.strip())
    return result
def getInvesting(ticker):
    target_address = 'https://www.google.com/search?q='+ticker+'+investing'
    html = requests.get(target_address)
    soup = BeautifulSoup(html.text, 'html.parser')
    posts = soup.select('.kCrYT a ')
    #for chooes first herf 
    href = str(posts[0].attrs['href'])
    #then href is 'https:/www.investing/equities/stock&~~~~~~ 
    #so 1.find  start-index : index('equities') , end-index : index('&')
    # and slicing href[start : end]
    start = href.find('equities')
    end = href.find('&')
    print(href[start:end])
    return "https://www.investing.com/" +href[start:end]+'-commentary'

def writeExcel(df, name):
    writer = pd.ExcelWriter(name+'.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='welcome', index=False)
    writer.save()

if __name__ == '__main__':
    sp500 = pd.read_excel('sp500.xlsx' ,sheet_name= 0)
    pool = Pool(30)
    investingAddr = pool.map(getInvesting , sp500['ticker'].tolist())
    comments = pool.map(get_comments ,investingAddr)
    sp500_comments = pd.DataFrame({"ticker" : sp500['ticker'] , "investingAddr" : sp500["investingAddr"] 
                   , "comments" : comments})
    writeExcel(sp500_comments , 'sp500_comments')
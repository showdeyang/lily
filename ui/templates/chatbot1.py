# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import numpy as np
import random
import math
import json
import time
from multiprocessing import Pool
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor
import jieba
from multiprocessing import Pool

headers = json.loads('''{
        "connection": "keep-alive",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache"
        }''')

def inclusion(query, question):
    c1 = 0
    for char in query:
        if char in question:
            c1 += 1
            
    c2 = 0
    for char in question:
        if char in query:
            c2 += 1
            
    score = c1*c2
    return score

def _async_requests(urls):
    """
    Sends multiple non-blocking requests. Returns
    a list of responses.
 
    :param urls:
        List of urls
    """
     
    session = FuturesSession(max_workers=50)
    futures = [session.get(url, headers=headers) for url in urls]
    return [future.result() for future in futures]

def parallelScrape(queryUrls):
    results = []
    responses = _async_requests(queryUrls)
    
    for response in responses:
        
        soup = BeautifulSoup(response.content,'lxml')
        sups = soup.findAll('sup')
        [sup.decompose() for sup in sups]
        #question = soup.find("span",{"class":"ask-title"}).get_text()
        answerElems = soup.findAll("div",{"class":"para"})
        
        #commentElem = soup.findAll('span',{'alog-action':'qb-comment-btnbestbox'}) + soup.findAll('span',{'alog-action':'qb-comment-btn'}) 
        
        answers = []
        for answerElem in answerElems:
            answer = answerElem.get_text().strip().replace('\n','').replace('\xa0','').replace('\u3000','')
            if answer != '':
                if '。' in answer or '；' in answer:
                    answers.append(answer)
        resultDict = {'q': soup.h1.text, "a": answers}
        results.append(resultDict)
    return results

def getUrls(query):
    html = requests.get('https://baike.baidu.com/search/none?word=' + query, headers=headers).content
    soup = BeautifulSoup(html,'lxml')
    links = soup.findAll('a', {'class':'result-title'})
    urls = [link['href'] for link in links]
    u = []
    for url in urls:
        if 'http' not in url:
            url = 'https://baike.baidu.com' + url
            u.append(url)
        else:
            u.append(url)
    #print(urls)
    return u



def f(query,answers):
    args = [(query, answer) for answer in answers]
    with Pool() as p:
            fitnesses = p.starmap(inclusion,args)    
    return fitnesses

def reply(query):
    urls = getUrls(query)
    results = parallelScrape(urls)
    answers = []
    for result in results:
        answers += result['a']
        
    fitnesses = f(query, answers)
    if fitnesses == []:
        return None
    maxFit = random.choice([fit for fit in fitnesses if fit >= np.percentile(fitnesses,90)])
            
    fitInd = fitnesses.index(maxFit)

    return answers[fitInd]
    

query = input('>>>')  
while query != 'bye lily':
    answer = reply(query)
    print(answer)
    query = input('>>>')
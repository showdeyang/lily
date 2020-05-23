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


#session = FuturesSession(executor=ThreadPoolExecutor(max_workers=12))

with open('./fitness.model','r') as f:
        model = f.read()
        #print(model)
        geneMean = json.loads(model)

queryUrlPrefix = 'https://zhidao.baidu.com/search?word='

def inclusion(query, question):
    count = 0
    for char in query:
        if char in question:
            count += 1
    return count

def _async_requests(urls):
    """
    Sends multiple non-blocking requests. Returns
    a list of responses.
 
    :param urls:
        List of urls
    """
     
    session = FuturesSession(max_workers=50)
    futures = [session.get(url) for url in urls]
    return [future.result() for future in futures]

def lenDiff(query,question):
    return len(question) - len(query)

def qbadness(query,question):
    badness = len(question) + len(query) - 2*inclusion(query,question)
    return badness

def calFitness(reply,gene=geneMean):
    query = reply['query']
    feature = []
    qbad = qbadness(query,reply['q'])
    #print(reply['l'])
    like = int(reply['l'])
    
    if len(reply['a']) == 0:
        alen = 10000
    else: 
        alen = 0.01*(len(reply['a'])**2)
    
    infodiff = 0 if math.fabs(len(reply['a']) - len(query)) < 10 else math.fabs(len(reply['a']) - len(query)) 
    ainc = inclusion(reply['a'],query) if inclusion(reply['a'],query) < 10 else 10
    rtime = reply['t'].split('-')
    #print(time)
    try:
        elapse = int(rtime[0]) + int(rtime[1])/12.0 + int(rtime[2])/366.0 - 2018
    except ValueError:
        elapse = 0
    #print(elapse)
    feature = [qbad,like,alen,infodiff,ainc,elapse]
    
    fitness = np.matmul(gene,feature)
    return fitness


def parallelScrape(queryUrls,questions):
    results = []
    responses = _async_requests(queryUrls)
    
    for response in responses:
        
        soup = BeautifulSoup(response.content,'lxml')
        question = questions[responses.index(response)]
        #question = soup.find("span",{"class":"ask-title"}).get_text()
        answerElems = soup.findAll("div",{"accuse":"aContent"})
        
        timesElem = [elem.get_text() for elem in soup.findAll("span",{"class":"wgt-replyer-all-time"})]
        times = [elem.replace('推荐于','').replace('\n','') for elem in timesElem]
        
        likesElem = soup.findAll('span',{'alog-action':'qb-zan-btnbestbox'}) + soup.findAll('span',{'alog-action':'qb-zan-btn'}) 
        likes = [elem['data-evaluate'] for elem in likesElem]
        
        #commentElem = soup.findAll('span',{'alog-action':'qb-comment-btnbestbox'}) + soup.findAll('span',{'alog-action':'qb-comment-btn'}) 
        
        answers = []
        for answerElem in answerElems:
            answer = answerElem.get_text().strip().replace('\n','').replace('展开全部','')
            answers.append(answer)
        resultDict = {'q': question, "a": answers, 't': times, 'l': likes}
        results.append(resultDict)
    return results

#Knowledge Graph from BaiduBaike
    
def reply(query, queryUrlPrefix=queryUrlPrefix, geneMean=geneMean):
    if query == 'bye lily':
        return "下次再聊！"
    elif query is '':
        return ""
    else:
        queryUrl = queryUrlPrefix + query
    
        #Get result urls
        html = requests.get(queryUrl).content
        soup = BeautifulSoup(html,"lxml")
        elems = soup.find("div",{"class":"list-inner"}).findAll("dt",{"class":"dt mb-4 line"})
        urls = [elem.a['href'] for elem in elems]
        questions = [elem.a.get_text() for elem in soup.findAll('dt',{'class':'dt mb-4 line'})]
        
        queryUrls = urls

        #time2 = time.time()
        #######Scraping Urls ################
    #    

        results = parallelScrape(queryUrls,questions)
        #time3 = time.time()    
        
        #############################################
        #Now all possible QAs are in resultDict. Analyse resultDict to get the best reply answer.
        #First decide which question is relevant.
        replies = []
        for result in results:
            for ans in result['a']:
                
                ind = result['a'].index(ans)
                replies.append({'q': result['q'], 'query': query, "a": ans, 't': result['t'][ind], 'l': result['l'][ind]})
        if replies == []:
            return "聊别的吧..."
        #Now we have replies, map replies to features, and then apply reinforcement learning.
        #time4 = time.time()
        #gene = [np.random.normal(g,0) for g in geneMean]
        gene = geneMean
        # + g*random.random()
        #features=  []
        #fitnesses = [] 
        
        #replies = [(reply, query, gene) for reply in replies]
        
        with Pool() as p:
            fitnesses = p.map(calFitness,replies)        
        
#        for reply in replies:
            
            #ind = replies.index(reply)
            #print(ind)
#            feature = []
#            qbad = qbadness(query,reply['q'])
#            #print(reply['l'])
#            like = int(reply['l'])
#            
#            if len(reply['a']) == 0:
#                alen = 10000
#            else: 
#                alen = 0.01*(len(reply['a'])**2)
#            
#            infodiff = 0 if math.fabs(len(reply['a']) - len(query)) < 10 else math.fabs(len(reply['a']) - len(query)) 
#            ainc = inclusion(reply['a'],query) if inclusion(reply['a'],query) < 10 else 10
#            rtime = reply['t'].split('-')
#            #print(time)
#            try:
#                elapse = int(rtime[0]) + int(rtime[1])/12.0 + int(rtime[2])/366.0 - 2018
#            except ValueError:
#                elapse = 0
#            #print(elapse)
#            feature = [qbad,like,alen,infodiff,ainc,elapse]
#            
#            fitness = np.matmul(gene,feature)
            #fitnesses.append(fitness)

        try:
            maxFit = random.choice([fit for fit in fitnesses if fit >= np.percentile(fitnesses,75)])
            
            fitInd = fitnesses.index(maxFit)

            return replies[fitInd]['a']
        except ValueError:
            return "聊别的吧..."
#            
#answer = reply('厌氧工艺应注意事项')
#print(answer)
#
#
#    


import requests
from bs4 import BeautifulSoup
from threading import Thread
import time
from configparser import ConfigParser

def getSearchResults(question, mkt = "de-DE", promote = "Webpages", answerCount = 1):
    conf = ConfigParser()
    conf.read('../config.ini')
    subscription_key = conf['environ']['bing_key']
    assert subscription_key

    search_url = "https://api.bing.microsoft.com/v7.0/search"

    search_term = question

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": search_term, "mkt": mkt, "promote": promote, "answerCount": answerCount}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    return search_results['webPages']['value']

def getKeyPhrases(question):
    conf = ConfigParser()
    conf.read('../config.ini')
    subscription_key = conf['environ']['keyphrases_key']
    assert subscription_key

    url = "https://quiztextana.cognitiveservices.azure.com/text/analytics/v3.1/keyPhrases"

    headers = {"Ocp-Apim-Subscription-Key": subscription_key, "Content-Type": "application/json"}
    body = {"documents": [{ 
        "id": "1",
        "language":"de",
        "text": question
    }]}

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    search_results = response.json()

    #print(search_results['documents'][0]['keyPhrases'])
    return " ".join(search_results['documents'][0]['keyPhrases'])


def loadPageAndCount(url, answerHits, verbose=False):
    #print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        resp = requests.get(url, headers=headers, timeout=2)
        if resp.status_code == 200:
            if verbose: print("Page loaded")
            soup = BeautifulSoup(resp.content, "html.parser")
            for data in soup(['style', 'script']):
                data.decompose()
            webtext = ' '.join(soup.stripped_strings).lower()

            for option in answerHits.keys():
                answerHits[option] = answerHits.get(option, 0) + webtext.count(option)
        else:
            if verbose: print(f"Cannot load Webpage, skip. Code: {resp.status_code}")
            
    except requests.exceptions.ReadTimeout:
        if verbose: print('Connection timed out, skip.')
        
    except requests.exceptions.ConnectionError:
        if verbose: print('Connection Error, skip.')

    #print(answerHits)
    return answerHits

def printOutput(answerHits):
    #os.system('cls')
    strings = [f'{option}\t{"#" * hits}' for option, hits in answerHits.items()]
    print('\n'.join(strings))


def assesAnswers(pages, answers):
    answerHits = dict()

    # Quick first assesment from preloaded snippets
    for page in pages:
        for option in answers:
            answerHits[option] = answerHits.get(option, 0) + page['snippet'].lower().count(option)
    print(answerHits)
    
    threads = []
    # Crawl Result Webpages for answers
    for page in pages:
        t = Thread(target=loadPageAndCount, args=(page['url'], answerHits))
        threads.append(t)
        t.start()
        #answerHits = loadPageAndCount(page['url'], answerHits)
        #printOutput(answerHits)

    for t in threads:
        t.join()

    return answerHits

#st = time.time()
#pages = getSearchResults('Zu welchem Land gehört Grönland?')
#print(pages)

#options = assesAnswers(pages, ["dänemark", "norwegen", "kanada", "usa"])

#print(options)
#print(f'Time passed: {time.time() - st}')
#getKeyPhrases("Wie heißt die jüdische Königin, die ihr Volk durch ihre selbstlosen Handlungen vor der sicheren Zerstörung rettete?")
import requests
from bs4 import BeautifulSoup
import os

def getSearchResults(question, mkt = "de-DE", promote = "Webpages", answerCount = 1):
    subscription_key = "eddcaabfa56c47ef83327f98f8207ace"
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
    subscription_key = "40c678adf7bf4ba5a47a84fc1124914d"
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

    print(search_results['documents'][0]['keyPhrases'])
    return " ".join(search_results['documents'][0]['keyPhrases'])


### MULTI THREADING here
def loadPageAndCount(url, answerHits):
    #print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        resp = requests.get(url, headers=headers, timeout=2)
        if resp.status_code == 200:
            print("Page loaded")
            soup = BeautifulSoup(resp.content, "html.parser")
            for data in soup(['style', 'script']):
                data.decompose()
            webtext = ' '.join(soup.stripped_strings).lower()

            for option in answerHits.keys():
                answerHits[option] = answerHits.get(option, 0) + webtext.count(option)
        else:
            print(f"Cannot load Webpage, skip. Code: {resp.status_code}")
            
    except requests.exceptions.ReadTimeout:
        print('Connection timed out, skip.')
        
    except requests.exceptions.ConnectionError:
        print('Connection Error, skip.')

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
    
    # Crawl Result Webpages for answers
    for page in pages:
        answerHits = loadPageAndCount(page['url'], answerHits)
        #printOutput(answerHits)
            
    return answerHits


#pages = getSearchResults('Welche Art von Tier ist ein "Ungarisches Nackthals"?')
#print(pages)

#options = assesAnswers(pages, ["frosch", "insekt", "marder", "vogel"])

#print(options)

#getKeyPhrases("Wie heißt die jüdische Königin, die ihr Volk durch ihre selbstlosen Handlungen vor der sicheren Zerstörung rettete?")
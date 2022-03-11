import bing_searcher as bs
import screenshot as sc
import ocr
import io

img_bytes = io.BytesIO()

img = sc.screenshot()
img.save(img_bytes, "png")
#print(ocr.getOcrText(img_bytes.getvalue()))
question = ocr.getQuestionAndAnswers(ocr.getOcrText(img_bytes.getvalue()), img.width, img.height)
print(question)

if len(question['Q'].split(" ")) > 9: 
    search_query = bs.getKeyPhrases(question['Q'])
else:
    search_query = question['Q']

print(f'Search Query: {search_query}')

pages = bs.getSearchResults(search_query)

options = bs.assesAnswers(pages, [question['A1'].lower(), question['A2'].lower(), question['A3'].lower(), question['A4'].lower()])

print(options)
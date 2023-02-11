from PIL import Image, ImageFile
import pytesseract
import requests
from pdf2image import convert_from_path, convert_from_bytes

response = requests.get("https://www.colmanweb.co.uk/problemsolving/ukmt/2005/2005.2.pdf", stream=True)

[page] = convert_from_bytes(response.content)
page.save('output.jpg')
print(pytesseract.image_to_string(page))


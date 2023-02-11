import requests

response = requests.get("https://www.colmanweb.co.uk/problemsolving/ukmt/2005/2005.2.pdf", stream=True)

print(response.status_code)

with open('output', 'wb') as fd:
    for chunk in response.iter_content(chunk_size=128):
        fd.write(chunk)

from urllib import parse, request
import json
import requests
import os

class GenerateGifs():
    def __init__(self):
        self.url = "http://api.giphy.com/v1/gifs/search"
        self.clean_wd()

    def clean_wd(self):
        directory = ['./gifs']
        for direct in directory:
            files = os.listdir(direct)
            files = [os.path.join(direct, i) for i in files]
            for file in files:
                    if os.path.isfile(file):
                        os.remove(file)


    def generate_gif(self, query: str, filename:str, debug=False):
        params = parse.urlencode({
            "q": query,
            "rating": "pg-13",
            "api_key": "YOUR-API-KEY REFER GIPHY DEVELOPER PROGRAM",
            "limit" : "5",
        })
        if debug: print('sending request ', query, self.url)
        url_data = "".join(("".join((self.url, "?", params))))
        print(url_data)
        with request.urlopen(url_data) as response:
            data = json.loads(response.read())
            
        # if debug: print('response', query, data)
        json_data = json.dumps(data, sort_keys=True, indent=4)

        with open("gif_req.json", "w") as f:
            f.write(json_data)
        
        for gif in data['data']:
            if gif['username'] != "Persistventures":
                print('accepted ', gif['username'])
                url = gif['images']['original_mp4']['mp4']
                print(url)

                if debug: print('downloading', query, url)
                res = requests.get(url)

                with open(filename, 'wb') as f:
                    f.write(res.content)
                if debug: print('downloaded', query + 'at', filename)
                break
            else:
                print('rejected', gif['username'])
                
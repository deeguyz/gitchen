import requests
import json

def jsonToTXT (jsonfile):
    return json.dumps(jsonfile)

def getJsonFiles(ingredients):
    print(ingredients)

    apiParams = {"q": ingredients, "app_id": "cc561a21", "app_key": "ca711054268b16aca9ac013484e0efd8"}
    request = requests.get("https://api.edamam.com/search", params=apiParams)

    return request.json() #access a specific recipe given a q
    #print(request.json()["hits"][0]) #access a specific recipe given a q


    print(jsonToTXT(request.json()["hits"][0])) #access a specific recipe given a q
    #print(request.json()["count"]) #access a specific recipe given a q

#print(jsonToTXT(request.json()["hits"][0])) #access a specific recipe given a q

#print(request.json()["count"]) #access results count

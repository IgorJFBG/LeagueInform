import requests as req
from translation import language

def ChampionList(id):
    versions = req.get('https://ddragon.leagueoflegends.com/api/versions.json')
    versions = versions.json()
    latest = versions[0]

    url = f'https://ddragon.leagueoflegends.com/cdn/{latest}/data/{language}/champion.json'
    champions = req.get(url)
    champions = champions.json()["data"]

    for champion in champions.values():
        if champion["key"] == str(id):
            return champion


def GetChampionNameOrganized(id):
    champion = ChampionList(id)
    championName = champion["name"]
    for i in range(14-len(championName)):
        championName = " "+championName
    return championName


def GetChampionName(id):
    champion = ChampionList(id)
    return champion["name"]
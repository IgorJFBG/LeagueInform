import os
import platform

import requests as req

import leagueChampions
import translationPortuguese

KEY = "sua-chave-aqui"  # altera todo dia
# resgate sua chave api de desenvolvimento em: https://developer.riotgames.com/
URL = "https://br1.api.riotgames.com/"


def GetError(error):
    print(f"Erro {error}")
    if   error == 403:      print("Atualize a chave de acesso. ")
    elif error == 404:      print("Usuário não encontrado. ")


def GetUser(user):
    text = f"{URL}lol/summoner/v4/summoners/by-name/{user}?api_key={KEY}"
    return req.get(text)


def GetRanked(id):
    text = f"{URL}lol/league/v4/entries/by-summoner/{id}?api_key={KEY}"
    return req.get(text)


def GetMasteries(id):
    text = f"{URL}lol/champion-mastery/v4/champion-masteries/by-summoner/{id}?api_key={KEY}"
    return req.get(text)


def GetMasteriesScore(id):
    text = f"{URL}lol/champion-mastery/v4/scores/by-summoner/{id}?api_key={KEY}"
    return req.get(text)


def ClearScreen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


while True:
    ClearScreen()
    user = input("Digite o nome do invocador: ")
    result = GetUser(user)
    if result.status_code == 200:
        summoner = result.json()
        print(f"Invocador: {summoner['name']} | Nível: {summoner['summonerLevel']}")

        result = GetMasteriesScore(summoner["id"])
        print(f"Maestria: {result.json()}\n")

        result = GetRanked(summoner["id"])
        for ranked in result.json():
            print(
                f"{translationPortuguese.traduz(ranked['queueType'])}: {translationPortuguese.traduz(ranked['tier'])} {ranked['rank']} | PDL: {ranked['leaguePoints']} ")
            print(f"Vitórias: {ranked['wins']} | Derrotas: {ranked['losses']}\n")

        result = GetMasteries(summoner["id"])
        for mastery in result.json():
            if mastery["championLevel"] >= 4:

                chestText = ""
                if mastery["chestGranted"]:
                    chestText = "garantido. ✔️"
                else:
                    chestText = "disponível.🎁"

                # champion = leagueChampions.getChampion(mastery['championId'])

                if   mastery['championLevel'] == 7: masteryText = "Maestria 7 🔵"
                elif mastery['championLevel'] == 6: masteryText = "Maestria 6 🟣"
                elif mastery['championLevel'] == 5: masteryText = "Maestria 5 🔴"
                else:                               masteryText = "Maestria 4 🟤"

                untilNextText = ""
                if mastery["championPointsUntilNextLevel"] != 0:
                    untilNextText = f"{mastery['championPointsUntilNextLevel']} pontos até Maestria 5 🔴."

                print(
                    f"{leagueChampions.getChampionName(mastery['championId'])}: {masteryText}\t{mastery['championPoints']} pontos.\tBaú {chestText}\t{untilNextText}")
    else:
        GetError(result.status_code)

    again = input("\nDeseja pesquisar outro invocador? ").lower()
    while again != "sim" and again != "nao" and again != "não":
        again = input("\nDeseja pesquisar outro invocador? ")
    if again == "nao" or again == "não":
        break

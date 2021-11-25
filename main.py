import requests as req
import champions
import utility as util
from translation import translation
from translation import language

tagLine = "br1"
KEY = "RGAPI-235a0700-f17a-486f-b171-96e26eb4b96b"  # altera todo dia
# resgate sua chave api de desenvolvimento em: https://developer.riotgames.com/
URL = f"https://{tagLine}.api.riotgames.com/"

summoner = None

def ChangeLanguage():
    list = {1: "pt_BR", 2: "en_US"}
    
    print(f"\n{translation[language]['SELECT_LANGUAGE']}")
    print("[1] Português")
    print("[2] English")
    print(f"[0] {translation[language]['CANCEL']}")
    while True:
        select = int(input(" >> "))
        if (select >= 1 and select <= 2):
            return list[select]
        elif select == 0:
            break
    return None

def GetUser():
    while True:
        user = input(translation[language]["TYPE_SUMMONERS_NAME"])
        print(translation[language]['SEARCHING'])
        url = f"{URL}lol/summoner/v4/summoners/by-name/{user}?api_key={KEY}"
        result = req.get(url)
        if result.status_code == 200:
            print(f"\n{translation[language]['SUMMONER_FOUND']}")
            return result.json() 
        else:
            try:
                print(f"{translation[language]['ERROR']} {result.status_code}. {translation[language][str(result.status_code)]}")
            except(Exception):
                print(f"{translation[language]['ERROR']} {result.status_code}")
            while True:
                again = input("\n" + translation[language]["ANOTHER_SUMMONER"]).lower()
                if again == "sim" or again == "nao" or again == "não":
                    break
            if again == "nao" or again == "não":
                break
    return None

def GetTagLine(puuid):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={KEY}"
    result = req.get(url)
    account = result.json()
    return account["tagLine"]

def GetFreeChampionRotation():
    url = f"{URL}lol/platform/v3/champion-rotations?api_key={KEY}"
    result = req.get(url)
    print(translation[language]["FREE_CHAMPION_ROTATION"])
    rotations = result.json()
    
    freeChampions = []
    count = 0
    if result.status_code == 200:
        for champion in rotations["freeChampionIds"]:
            print(f"{int((count/len(rotations['freeChampionIds']))*100)}% 🧝\033[F")
            freeChampions.append(champions.GetChampionName(champion))
            count += 1
        print(translation[language]["ORGANIZING"])
        print(util.Sort(freeChampions))
        print(f"\n{translation[language]['FREE_CHAMPION_ROTATION_FOR_NEW_PLAYERS']}")
    else:
        print(translation[language][str(result.status_code)])
    
    freeChampionsForNewPlayers = []
    count = 0
    if result.status_code == 200:
        for champion in rotations["freeChampionIdsForNewPlayers"]:
            print(f"{int((count/len(rotations['freeChampionIdsForNewPlayers']))*100)}% 🧝\033[F")
            freeChampionsForNewPlayers.append(champions.GetChampionName(champion))
            count += 1
        print(translation[language]["ORGANIZING"])
        print(util.Sort(freeChampionsForNewPlayers))
    else:
        print(translation[language][str(result.status_code)])
    
def GetRanked(id):
    url = f"{URL}lol/league/v4/entries/by-summoner/{id}?api_key={KEY}"
    result = req.get(url)
    rankeds = result.json()
    if (rankeds == []):
        print(translation[language]["NO_LEAGUE_RANK"])
    for ranked in rankeds:
        # League of Legends
        print(f"{translation[language][ranked['queueType']]}: {translation[language][ranked['tier']]} {ranked['rank']} | PDL: {ranked['leaguePoints']}")
        print(f"{translation[language]['VICTORIES']}: {ranked['wins']} | {translation[language]['DEFEATS']}: {ranked['losses']}\n")

def GetMasteries(id):
    url = f"{URL}lol/champion-mastery/v4/champion-masteries/by-summoner/{id}?api_key={KEY}"
    result = req.get(url)
    masteries = result.json()
    for mastery in masteries:
        if mastery["championLevel"] >= 4:
            chestText = ""
            if mastery["chestGranted"]:
                chestText = f"{translation[language]['GRANTED']}"
            else:
                chestText = f"{translation[language]['AVAILABLE']}"
            
            if   mastery['championLevel'] == 7: masteryText = f"{translation[language]['MASTERY_7']}"
            elif mastery['championLevel'] == 6: masteryText = f"{translation[language]['MASTERY_6']}"
            elif mastery['championLevel'] == 5: masteryText = f"{translation[language]['MASTERY_5']}"
            else:                               masteryText = f"{translation[language]['MASTERY_4']}"

            untilNextText = ""
            if mastery["championPointsUntilNextLevel"] != 0:
                untilNextText = f"{str(mastery['championPointsUntilNextLevel'])} {translation[language]['UNTIL_NEXT_MASTERY_TEXT']} {translation[language]['MASTERY_5']}"

            print(f"{champions.GetChampionNameOrganized(mastery['championId'])}:  {masteryText}  {mastery['championPoints']} {translation[language]['POINTS']}.  {translation[language]['CHEST']} {chestText}  {untilNextText}")

def GetAvailableChests(id):
    url = f"{URL}lol/champion-mastery/v4/champion-masteries/by-summoner/{id}?api_key={KEY}"
    result = req.get(url)
    available = []
    countavailable = 0
    countgranted = 0
    masteries = result.json()
    for mastery in masteries:
        print(f"{countavailable} 🎁\t|\t{countgranted} ✔️\t|\t{int(((countavailable+countgranted)/len(masteries))*100)}%\033[F")
        if mastery["chestGranted"]:
            countgranted += 1
        else:
            available.append(champions.GetChampionName(mastery['championId']))
            countavailable += 1
    print(translation[language]["ORGANIZING"])
    print(util.Sort(available))

def GetOptions(summoner):
    util.ClearScreen()
    if (summoner != None):
        print(f"{translation[language]['SUMMONER']}: {summoner['name']} # {tagLine.upper()} | {translation[language]['LEVEL']}: {summoner['summonerLevel']}")

        result = req.get(f"{URL}lol/champion-mastery/v4/scores/by-summoner/{summoner['id']}?api_key={KEY}")
        print(f"{translation[language]['MASTERY_POINTS']}: {result.json()}\n")
    else:
        print(f"{translation[language]['NO_SUMMONER']} | {translation[language]['LEVEL']}: ---")
        print(f"{translation[language]['MASTERY_POINTS']}: ---\n")
    
    print(translation[language]["SELECT_OPTION"])
    print(f"[1] {translation[language]['SEARCH_SUMMONER']}")
    print(f"[2] {translation[language]['SHOW_CHAMPION_ROTATION']}")
    if (summoner != None):
        print(f"[3] {translation[language]['SHOW_SUMMONERS_RANK']}")
        print(f"[4] {translation[language]['SHOW_SUMMONERS_MASTERIES']}")
        print(f"[5] {translation[language]['SHOW_AVAILABLE_CHESTS']}")
    print(f"[9] {translation[language]['CHANGE_LANGUAGE']}")
    print(f"[0] {translation[language]['EXIT']}")

#main
while True:
    util.ClearScreen()
    GetOptions(summoner)
    try:
        command = int(input(" >> "))
    except:
        command = -1
    
    # Encontrar invocador
    if command == 1:
        newSummoner = GetUser()
        if (newSummoner != None):
            summoner = newSummoner
            tagLine = GetTagLine(summoner["puuid"]).lower()
            
    # Rotação grátis de campeões
    elif command == 2:          GetFreeChampionRotation()
    
    # Elo / Rank
    elif command == 3:          
        if summoner != None:    GetRanked(summoner["id"])
        else:                   print(translation[language]["INVALID_OPTION"])
    
    # Maestrias
    elif command == 4:          
        if summoner != None:    GetMasteries(summoner["id"])
        else:                   print(translation[language]["INVALID_OPTION"])
    
    # Baús disponíveis
    elif command == 5:          
        if summoner != None:    GetAvailableChests(summoner["id"])
        else:                   print(translation[language]["INVALID_OPTION"])
        
    # Trocar idioma
    elif command == 9:          language = ChangeLanguage()
    
    # Sair do programa
    elif (command == 0): break
    else: print(translation[language]["INVALID_OPTION"])
    util.Wait(language)
        
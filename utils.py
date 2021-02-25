import constants
import logger as log


def create_url(region, search, parameters):
    url = "https://"

    url += return_region_endpoint(region)
    url += return_search_path(search, parameters)

    if not ("?" in url):
        url += "?"
    url += "api_key=" + constants.API_KEY

    return url


def find_extension(file_name):
    split = file_name.split(".")

    return split[-1]


def return_region_endpoint(region):
    result = constants.SWITCHER_REGION.get(region, None)

    if result is None:
        error_message = constants.ERROR_NOT_IMPLEMENTED + "Region (" + str(region) + \
                        ") not found in the constants class."
        log.inform(error_message, finalize=True)

    return result


def return_search_path(search, parameters):
    search_path = ""
    # Summoner's All Champions Mastery -> parameters = [summonerId]
    #   summonerId can be found by requesting the summoner's info
    if search == "ACM":
        search_path = "/lol/champion-mastery/v4/champion-masteries/by-summoner/" + parameters
    # Challenger player's rank list -> parameters = [queue]
    #   queue can be:
    #       RANKED_SOLO_5x5
    #       RANKED_FLEX_SR
    #       RANKED_FLEX_TT
    elif search == "LC":
        search_path = "/lol/league/v4/challengerleagues/by-queue/" + parameters
    # Grandmaster player's rank list -> parameters = [queue]
    elif search == "LG":
        search_path = "/lol/league/v4/grandmasterleagues/by-queue/" + parameters
    # Master player's rank list -> parameters = [queue]
    elif search == "LM":
        search_path = "/lol/league/v4/masterleagues/by-queue/" + parameters
    # Match's Info -> parameters = [matchId]
    #   matchId can be found by requesting a list of matches (ML)
    elif search == "MI":
        search_path = "/lol/match/v4/matches/" + str(parameters)
    # Matches List -> parameters = [accountId, queueId, seasonId, beginIndex, endIndex]
    #   accountId can be found by requesting the summoner's info
    #   queueId and seasonId can be found in https://developer.riotgames.com/game-constants.html
    #       more than one queueId can be passed
    #   beginIndex and endIndex indicate the range of latest matches that you want to search for
    elif search == "ML":
        search_path = "/lol/match/v4/matchlists/by-account/" + parameters[0]
        if len(parameters) > 1:
            search_path += "?"
            for x in range(1, len(parameters), 2):
                search_path += parameters[x] + "=" + str(parameters[x+1])
                search_path += "&"
    # Summoners's Champion Mastery Specific -> parameters = [summonerId, championId]
    #   championId is a number that represents a champion in the game and can be translated using a SQL search,
    #       after running scripts.gather_champions_data(file_name)
    #   the file can be obtained here: http://ddragon.leagueoflegends.com/cdn/<VERSION>/data/en_US/champion.json
    #   changing <VERSION> by the version of the game you want to search, for a list of versions, check:
    #   https://ddragon.leagueoflegends.com/api/versions.json
    elif search == "SCM":
        search_path = "/lol/champion-mastery/v4/champion-masteries/by-summoner/" + parameters[0] + \
               "/by-champion/" + str(parameters[1])
    # Summoner's Info -> parameters = [accountId]
    elif search == "SIA":
        search_path = "/lol/summoner/v4/summoners/by-account/" + parameters
    # Summoner's Info -> parameters = [summonerName]
    elif search == "SIN":
        search_path = "/lol/summoner/v4/summoners/by-name/" + parameters
    # Summoner's Info -> parameters = [PUUID]
    elif search == "SIP":
        search_path = "/lol/summoner/v4/summoners/by-puuid/" + parameters
    # Summoner's Info -> parameters = [summonerId]
    elif search == "SIS":
        search_path = "/lol/summoner/v4/summoners/" + parameters
    # Summoners's Mastery Score -> parameters = [summonerId]
    elif search == "SMS":
        search_path = "/lol/champion-mastery/v4/scores/by-summoner/" + parameters
    # Summoner's Rank -> parameters = [summonerId]
    elif search == "SR":
        search_path = "/lol/league/v4/entries/by-summoner/" + parameters
    else:
        error_message = constants.ERROR_NOT_IMPLEMENTED + search + " not implemented." \
                        + "For possible searches check the code documentation."
        log.inform(error_message, finalize=True)

    return search_path

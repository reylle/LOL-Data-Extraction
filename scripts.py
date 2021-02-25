import api_object
import constants
import io_helper as ioh
import logger as log
import random
import utils

from os import listdir
from os.path import isfile, join


def find_matches(platform_id):
    api_obj = api_object.ApiObject()
    match_list_path = constants.DATA_DIR + 'MatchesLists/'
    files = [f for f in listdir(match_list_path) if isfile(join(match_list_path, f))]
    length = len(files)
    index = 0

    for file in files:
        index += 1
        log.inform('Extracting matches from list ' + str(index) + '/' + str(length))
        match_list = ioh.load_pickle(join(match_list_path, file))
        for match in match_list['matches']:
            match_id = match['gameId']
            if not file_exists(str(match_id), constants.DATA_DIR + 'Matches/'):
                api_obj.url = utils.create_url(platform_id, 'MI', match_id)
                match_info = api_obj.request_json()
                if match_info is not None:
                    ioh.save_pickle(match_info, constants.DATA_DIR + 'Matches/' + str(match_id))


def find_players(initial_platform, initial_player_name, begin_time, end_time, num_players):
    api_obj = api_object.ApiObject()
    api_obj.url = utils.create_url(initial_platform, 'SIN', initial_player_name)

    summoner_info = api_obj.request_json()
    if summoner_info is None:
        log.inform('Initial player not suitable, try another one.', finalize=True)

    puuid = summoner_info['puuid']
    ioh.save_pickle(summoner_info, constants.DATA_DIR + 'Players/' + puuid + '-' + initial_platform)

    account_id = summoner_info['accountId']
    platform_id = initial_platform
    players_extracted = 0

    while players_extracted < num_players:
        log.inform('Player ' + str(players_extracted + 1) + ' being extracted...')
        start_time = begin_time
        match_ids = []
        while start_time < end_time:
            if start_time + 604799000 <= end_time:
                stop_time = start_time + 604799000
            else:
                stop_time = end_time
            api_obj.url = utils.create_url(platform_id, 'ML', [account_id, 'beginTime', start_time,
                                                               'endTime', stop_time])
            match_list = api_obj.request_json()
            if match_list is not None:
                ioh.save_pickle(match_list, constants.DATA_DIR + 'MatchesLists/' + puuid + '-' +
                                str(start_time) + '-' + str(stop_time))
                for match in match_list['matches']:
                    if match['gameId'] not in match_ids:
                        match_ids += [match['gameId']]
            start_time += 604800000

        players_extracted += 1
        account_id = None
        while account_id is None and players_extracted < num_players:
            match_chosen = match_ids[random.randrange(0, len(match_ids))]
            api_obj.url = utils.create_url(platform_id, 'MI', match_chosen)
            match_info = api_obj.request_json()
            if match_info is not None:
                for participant in match_info['participantIdentities']:
                    aux_platform = participant['player']['currentPlatformId']
                    aux_account_id = participant['player']['currentAccountId']
                    if len(aux_account_id) < 5:
                        continue
                    api_obj.url = utils.create_url(aux_platform, 'SIA', aux_account_id)
                    aux_player_info = api_obj.request_json()
                    if aux_player_info is not None:
                        puuid = aux_player_info['puuid']
                        if not file_exists(puuid + '-' + aux_platform, constants.DATA_DIR + 'Players/'):
                            ioh.save_pickle(aux_player_info, constants.DATA_DIR + 'Players/' +
                                            puuid + '-' + aux_platform)
                            account_id = aux_account_id
                            platform_id = aux_platform
                            break


def gather_players_match_history_daily(platform_id, account_id, begin_time, end_time):
    api_obj = api_object.ApiObject()
    pointer = begin_time
    aux = 604799999
    f = open(constants.DATA_DIR + 'play_history_daily.csv', 'a')

    while pointer + aux <= end_time:
        url = utils.create_url(platform_id, 'ML', [account_id, 'beginTime', pointer, 'endTime', pointer + aux,
                                                   'beginIndex', 0, 'endIndex', 100])
        api_obj.url = url
        match_list = api_obj.request_json()

        if match_list is not None:
            days = []
            for match in match_list['matches']:
                pointer_2 = pointer
                timestamp = match['timestamp']
                while timestamp > pointer_2 and timestamp >= pointer_2 + 86400000:
                    pointer_2 += 86400000
                if pointer_2 not in days:
                    days += [pointer_2]
                    f.write(account_id + ';' + str(pointer_2) + '\n')
                if len(days) >= 7:
                    break
        pointer += aux + 1

    if pointer <= end_time:
        url = utils.create_url(platform_id, 'ML', [account_id, 'beginTime', pointer, 'endTime', end_time + 86399999,
                                                   'beginIndex', 0, 'endIndex', 100])
        api_obj.url = url
        match_list = api_obj.request_json()

        if match_list is not None:
            days = []
            for match in match_list['matches']:
                pointer_2 = pointer
                timestamp = match['timestamp']
                while timestamp > pointer_2 and timestamp >= pointer_2 + 86400000:
                    pointer_2 += 86400000
                if pointer_2 not in days:
                    days += [pointer_2]
                    f.write(account_id + ';' + str(pointer_2) + '\n')
    f.close()


def file_exists(file_name, path):
    files = [f for f in listdir(path) if isfile(join(path, f))]

    for file in files:
        if file_name == file.split('.')[0]:
            return True
    return False

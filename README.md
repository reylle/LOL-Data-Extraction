# LOL-Data-Extraction
A script that utilizes the League Of Legends (LOL) developer's Application Programming Interface (API), controls the number of packages sent regarding the limitation imposed by the API, and verifies the response, to acquire data related to players login history and matches' outcome results.

PRE-REQUISITES:

  1 - Have a LOL developers' API key;
  
  2 - In your python virtual environment, installed the following packages:
  
      Request;
      Pandas.

STEPS:

  1 - Modify the information in the constants class to match your configurations:
  
        Change the API_KEY that can be generated in the LOL developers website: https://developer.riotgames.com/;
        
        Change the data directory where you want the data files to be saved.
      
  2 - Find a Summoner's nickname:
  
      You can use a site similar to https:\\op.gg.
  
  3 - Run scripts.find_players(initial_platform, initial_player_name, begin_time, end_time, num_players), where:
  
      initial_platform is the platform of the chosen player. It can be "BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2", "NA1", "OC1", "TR1", or "RU";
      initial_player_name is the Summoners' nickname of the player chosen;
      begin_time is the time in milliseconds of the first date of the data collention (ex: Feb. 24 2021 UTC 23:00:00 -> 1614218400000);
      end_time is the time in milliseconds of the final date of the data collention;
      num_players is the quantity of players that will have their data extracted.
      This function generates files '.p' with the information of the players' profiles and their matches lists.
      
  4 - Run scripts.find_matches(platform_id), where:
  
      platform_id is the platform in which the players were extracted.
      This function returns the information regarding the matches' outcome statistics (kills, deaths, assists, true damage dealt...).
      
  5 - Run scripts.gather_players_match_history_daily(platform_id, account_id, begin_time, end_time), where:
  
      platform_id is the platform in which the player chosen played;
      account_id is the players' accountID, it can be obtained from the '.p' files created in the 'Players/' folder;
      begin_time is the time in milliseconds of the first date of the data collention (ex: Feb. 24 2021 UTC 23:00:00 -> 1614218400000);
      end_time is the time in milliseconds of the final date of the data collention.
      This function generates a '.txt' containig the players' accountID and the time in milliseconds of the days played.

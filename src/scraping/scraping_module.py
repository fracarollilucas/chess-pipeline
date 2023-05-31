import chessdotcom
import json


def get_titles_from_json(filename):
    with open(filename, "r") as f:
        players_titles_dict = json.load(f)

    return players_titles_dict


def get_list_of_usernames(title):
    list_of_usernames = chessdotcom.get_titled_players(title).json["players"]

    return list_of_usernames


def get_current_database(filename):
    # obs: mesma funcao que get_titles_from_json()
    with open(filename, "r") as f:
        current_database = json.load(f)

    return current_database


def create_list_of_players_profiles(usernames):
    list_of_profiles = [
        chessdotcom.get_player_profile(username).json for username in usernames
    ]

    return list_of_profiles


def create_list_of_players_stats(usernames):
    list_of_stats = [
        chessdotcom.get_player_stats(username).json for username in usernames
    ]

    return list_of_stats


def create_player_dict(player_profile, player_stats):
    data_of_interest_from_profile = ["username", "name", "country"]
    data_of_interest_from_stats = ["rating"]

    values_of_interest_from_profile = [
        player_profile["player"].get(info, "null")
        for info in data_of_interest_from_profile
    ]
    values_of_interest_from_stats = [
        player_stats["stats"]["chess_rapid"]["last"].get(info, "null")
        if "chess_rapid" in player_stats["stats"].keys()
        else "null"
        for info in data_of_interest_from_stats
    ]

    data_of_interest = (
        data_of_interest_from_profile + data_of_interest_from_stats
    )
    values_of_interest = (
        values_of_interest_from_profile + values_of_interest_from_stats
    )
    player_dict = {
        key: value
        for (key, value) in zip(data_of_interest, values_of_interest)
    }

    return player_dict


def create_list_of_player_dicts(
    list_of_players_profiles, list_of_players_stats
):
    list_of_player_dicts = [
        create_player_dict(profile, stats)
        for (profile, stats) in zip(
            list_of_players_profiles, list_of_players_stats
        )
    ]

    return list_of_player_dicts


def save_database(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

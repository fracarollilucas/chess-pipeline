import scraping_module


def main():
    current_data = scraping_module.get_current_database("players_data.json")

    title_abbreviations = scraping_module.get_titles_from_json(
        "title_abbreviations.json"
    )
    abbrev = title_abbreviations["national master"]

    players_usernames = scraping_module.get_list_of_usernames(abbrev)
    players_profiles = scraping_module.create_list_of_players_profiles(
        players_usernames
    )
    players_stats = scraping_module.create_list_of_players_stats(
        players_usernames
    )

    total_data = scraping_module.create_list_of_player_dicts(
        players_profiles, players_stats
    )

    scraping_module.save_database(total_data, "players_data.json")

    print("Players' data saved successfully!")


if __name__ == "__main__":
    main()

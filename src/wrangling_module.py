import json
import pandas as pd
import sqlalchemy
import configparser

def get_current_database(filename):
    # obs: mesma funcao que get_titles_from_json()
    with open(filename, "r") as f:
        current_database = json.load(f)

    return current_database


def get_country_codes(filename):
    # obs: mesma funcao que get_titles_from_json()
    with open(filename, "r") as f:
        current_database = json.load(f)

    return current_database


def create_countries_dict(countries_list):
    codes = {}
    for country in countries_list:
        codes[country["alpha-2"]] = country["name"]

    return codes


def filter_nulls(players_data):
    return list(
        filter(lambda player: "null" not in player.values(), players_data)
    )


def update_country(player):
    code = player["country"].split("/")[-1]
    player.update({"country": code})

    return player

def update_players_countries(players):
    return [update_country(player) for player in players]

def update_players_names(players_df):
    players_df["first_name"] = players_df["name"].str.split().str[0]
    players_df["last_name"] = players_df["name"].str.split().str[-1]
    new_players_df = players_df.drop(["name"], axis=1)

    return new_players_df

def reorder_columns(df, new_order_list):
    return df[new_order_list]

def load(df, tbl, credentials):
    uid, pwd, port, server, dbname = credentials

    if_exists = 'replace' if tbl != 'countries' else 'fail'

    try: 
        rows_imported = 0
        engine = sqlalchemy.create_engine(f'postgresql://postgres:{pwd}@{server}:{port}/{dbname}')
        print(f'Importing row {rows_imported} to {rows_imported + len(df)}... for table {tbl}')

        df.to_sql(f'stg_{tbl}', engine, if_exists=if_exists, index=False)
        rows_imported += len(df)

        print('Data imported successfully!')
    
    except ValueError:
        pass

    except Exception as e:
        print(f'Data load error: {str(e)}')

def get_credentials(conf_path):
    parser = configparser.ConfigParser()
    parser.read(conf_path)
    server = parser.get("postgres_config", "server")
    port = parser.get("postgres_config", "port")
    username = parser.get("postgres_config", "username")
    dbname = parser.get("postgres_config", "database")
    password = parser.get("postgres_config", "password")

    credentials = [username, password, port, server, dbname]
    return credentials
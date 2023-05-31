import pandas as pd
import wrangling_module
from datetime import date

players_data = wrangling_module.get_current_database("scraping/players_data.json")

filtered_players = wrangling_module.filter_nulls(players_data)

players_countries_updated = wrangling_module.update_players_countries(filtered_players)

players_df = pd.DataFrame.from_dict(players_countries_updated)

first_normal_form_df = wrangling_module.update_players_names(players_df)

df_renamed = first_normal_form_df.rename(columns={'country':'country_code'})

new_column_order = ["username", "first_name", "last_name", "country_code", "rating"]

df_reordered = wrangling_module.reorder_columns(df_renamed, new_column_order)

ratings_df = df_reordered[["username", "rating"]]
ratings_df.assign(date=date.today())

players_df_final = df_reordered.drop(["rating"], axis=1)

countries = wrangling_module.get_country_codes("country_codes.json")
countries_dict = wrangling_module.create_countries_dict(countries)

countries_df = pd.DataFrame.from_dict(countries)

credentials = wrangling_module.get_credentials('pipeline.conf')

wrangling_module.load(players_df_final, 'players', credentials)
wrangling_module.load(countries_df, 'countries', credentials)
wrangling_module.load(ratings_df, 'ratings', credentials)
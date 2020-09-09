import json

import pandas as pd
import requests
from kaggle import api

column_order = [
    "id",
    "name",
    "type",
    "desc",
    "atk",
    "def",
    "level",
    "race",
    "attribute",
    "scale",
    "archetype",
    "linkval",
    "linkmarkers",
    "image_url",
    "image_url_small",
    "ban_tcg",
    "ban_ocg",
    "ban_goat",
]


def get_card_list():
    all_cards_response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")
    all_cards = json.loads(all_cards_response.text)
    return all_cards["data"]


def prepare_for_dataframe(card):

    for pop_data in ["card_sets", "card_prices"]:
        card.pop(pop_data, None)

    for extract_first_data in ["card_images"]:
        attr_list = card.pop(extract_first_data, [])
        if attr_list:
            card[extract_first_data] = attr_list[0]

    for ext_data in ["banlist_info", "card_images"]:
        for attr, val in card.pop(ext_data, dict()).items():
            if attr not in card:
                card[attr] = val

    return card


def main():
    card_list = get_card_list()
    cards_clean = [prepare_for_dataframe(card) for card in card_list]
    cards_df = pd.DataFrame(cards_clean)

    assert set(cards_df.columns) == set(column_order)

    cards_df[column_order].to_csv("data/cards.csv", index=False)
    api.dataset_create_version("data", "Weekly dataset update", quiet=True)


if __name__ == "__main__":
    main()

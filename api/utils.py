from hltv_async_api import Hltv
from django.conf import settings
from .hltv_scraper import HLTVScraper
import csv


# -------------------- START TEAM -------------------- #
def get_team_info() -> dict:
    """Get team profile from HLTV."""
    data = HLTVScraper.get_team_profile(
        settings.TEAM_ID,
        settings.TEAM_NAME
    )
    return data

def get_team_matches(offset: int | str = 1):
    """Get team matches from HLTV."""
    data = HLTVScraper.get_team_matches(settings.TEAM_ID, int(offset))
    return data
# -------------------- END TEAM -------------------- #


# -------------------- START PLAYER -------------------- #
def search_player(name: str):
    """Search player by name from HLTV"""
    data = HLTVScraper.search_player(name)
    return data 

def get_player_profile(id: str, player_name: str):
    """Get player profile from HLTV."""
    data = HLTVScraper.get_player_profile(id, player_name)
    return data

def get_player_stats_overview(id: str, player_name: str):
    """Get player statistics overview from HLTV."""
    data = HLTVScraper.get_player_stats_overview(id, player_name)
    return data
# -------------------- END PLAYER -------------------- #


# -------------------- START MATCHES -------------------- #
def get_upcoming_matches():
    """Get upcoming matches from HLTV."""
    data = HLTVScraper.get_upcoming_matches()
    return data

def get_match_details(id: str, match_name: str):
    """Get match details from HLTV."""
    data = HLTVScraper.get_match(id, match_name)
    return data
# -------------------- END MATCHES -------------------- #


# -------------------- START TABLEAU -------------------- #
def csv_to_dict_from_path(path: str) -> list[dict]:
    with open(path, "rb") as raw:
        start = raw.read(4)

    if start.startswith(b'\xff\xfe'):
        encoding = "utf-16"
    elif start.startswith(b'\xfe\xff'):
        encoding = "utf-16-be"
    elif start.startswith(b'\xef\xbb\xbf'):
        encoding = "utf-8-sig"
    else:
        encoding = "utf-8"

    with open(path, "r", encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter="\t")

        result = []
        for row in reader:
            clean = {k.strip(): (v.strip() if v is not None else "") 
                     for k, v in row.items()}
            result.append(clean)

    return result
# -------------------- END TABLEAU -------------------- #

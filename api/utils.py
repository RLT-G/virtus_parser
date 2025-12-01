from hltv_async_api import Hltv
from django.conf import settings
from .hltv_scraper import HLTVScraper


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


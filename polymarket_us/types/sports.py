"""Sports type definitions."""

from typing import TypedDict


class League(TypedDict, total=False):
    """Sports league."""

    id: str
    name: str
    slug: str


class Sport(TypedDict, total=False):
    """Sport details."""

    id: str
    name: str
    slug: str
    leagues: list[League]


class SportsTeamProvider(TypedDict):
    """Sports team provider ID."""

    provider: str
    id: str


class SportsTeam(TypedDict, total=False):
    """Sports team details."""

    id: int
    name: str
    abbreviation: str
    league: str
    record: str
    logo: str
    alias: str
    safe_name: str
    home_icon: str
    away_icon: str
    color_primary: str
    provider_ids: list[SportsTeamProvider]


class GetSportsResponse(TypedDict):
    """Response for listing sports."""

    sports: list[Sport]


class GetSportsTeamsParams(TypedDict, total=False):
    """Parameters for getting teams."""

    team_ids: list[str]
    provider: str
    league: str


class GetSportsTeamsResponse(TypedDict):
    """Response for getting teams."""

    teams: dict[str, SportsTeam]

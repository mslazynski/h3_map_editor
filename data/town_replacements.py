import os
import random
from enum import IntEnum, Enum, auto
from dataclasses import dataclass
from typing import Optional

from data.towns import ID as TownID
from data.objects import ID as ObjectID
import src.file_io as io

from gzip import open
import src.handler_01_general as h1
import src.handler_02_players_and_teams as h2
import src.handler_03_conditions as h3
import src.handler_04_heroes as h4
import src.handler_05_additional_flags as h5
import src.handler_06_rumors_and_events as h6
import src.handler_07_terrain as h7
import src.handler_08_objects as h8



replacements: dict[TownID, tuple[TownID, ...]] = {
    TownID.rampart: (TownID.castle, 
                     TownID.conflux,
                     TownID.cove,
                     TownID.dungeon, 
                     TownID.factory, 
                     TownID.fortress, 
                     TownID.inferno,
                     TownID.necropolis,
                     TownID.stronghold,
                     TownID.tower)
}


def random_replacement_for(town: TownID, context) -> TownID | None:
    if town in replacements:
        return random.choice(replacements[town])
    return None

allowed_towns: tuple[TownID] = tuple(
    town for town in TownID if town != TownID.NONE and town not in replacements
)

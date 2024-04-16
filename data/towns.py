#!/usr/bin/env python3
import os
from enum import IntEnum
from typing import Optional

import random
import src.file_io as io

from gzip import open
from data.objects import ID as ObjectID
import src.handler_01_general as h1
import src.handler_02_players_and_teams as h2
import src.handler_03_conditions as h3
import src.handler_04_heroes as h4
import src.handler_05_additional_flags as h5
import src.handler_06_rumors_and_events as h6
import src.handler_07_terrain as h7
import src.handler_08_objects as h8


class ID(IntEnum):
    NONE = 65535 

    castle = 0
    rampart = 1
    tower = 2
    inferno = 3
    necropolis = 4
    dungeon = 5
    stronghold = 6 
    fortress = 7
    conflux = 8
    cove = 9
    factory = 10

    

def towns_definitions() -> dict[ID, dict]:
    with open(os.path.join(os.path.dirname(__file__), "towns.h3m"), 'rb') as io.in_file:
        general = h1.parse_general()
        h2.parse_player_specs()
        h3.parse_conditions()
        h2.parse_teams()
        h4.parse_starting_heroes(general)
        h5.parse_flags()
        h6.parse_rumors()
        h4.parse_hero_data()
        h7.parse_terrain(general)
        object_defs = h8.parse_object_defs()

        return {
            object_def["subtype"]: object_def
            for object_def in object_defs
            if object_def["type"] == ObjectID.Town
        }
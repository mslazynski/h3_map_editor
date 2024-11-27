import os
import random
from enum import IntEnum, Enum, auto
from dataclasses import dataclass
from typing import Optional

from data.creatures import ID as CreatureID
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


class CreatureLevel(IntEnum):
    Level_1 = 1
    Level_2 = 2,
    Level_3 = 3,
    Level_4 = 4,
    Level_5 = 5,
    Level_6 = 6,
    Level_7 = 7

    @staticmethod
    def from_object_id(object_id: ObjectID) -> Optional['CreatureLevel']:
        match object_id:
            case ObjectID.Random_Monster_1:
                return CreatureLevel.Level_1
            case ObjectID.Random_Monster_2:
                return CreatureLevel.Level_2
            case ObjectID.Random_Monster_3:
                return CreatureLevel.Level_3
            case ObjectID.Random_Monster_4:
                return CreatureLevel.Level_4
            case ObjectID.Random_Monster_5:
                return CreatureLevel.Level_5
            case ObjectID.Random_Monster_6:
                return CreatureLevel.Level_6
            case ObjectID.Random_Monster_7:
                return CreatureLevel.Level_7
            case ObjectID.Random_Monster:
                return random.choice(tuple(level for level in CreatureLevel))
            case _:
                return None


class ReplacementContext(Enum):
    ALWAYS = auto()
    ENEMY = auto()
    FRIEND = auto()

@dataclass
class Replacement:
    id: CreatureID
    multiplier: float = 1.0


creatures_per_level: dict[CreatureLevel, tuple[CreatureID, ...]] = {
    CreatureLevel.Level_1: (
        CreatureID.Pikeman,
        CreatureID.Centaur,
        CreatureID.Gremlin,
        CreatureID.Imp,
        CreatureID.Skeleton,
        CreatureID.Troglodyte,
        CreatureID.Goblin,
        CreatureID.Gnoll,
        CreatureID.Pixie,
        CreatureID.Nymph,
        CreatureID.Halfling,
        CreatureID.Halberdier,
        CreatureID.Centaur_Captain,
        CreatureID.Master_Gremlin,
        CreatureID.Familiar,
        CreatureID.Skeleton_Warrior,
        CreatureID.Infernal_Troglodyte,
        CreatureID.Hobgoblin,
        CreatureID.Gnoll_Marauder,
        CreatureID.Sprite,
        CreatureID.Oceanid,
        CreatureID.Halfling_Grenadier,
        CreatureID.Peasant
    ),
    CreatureLevel.Level_2: (
        CreatureID.Archer,
        CreatureID.Dwarf,
        CreatureID.Stone_Gargoyle,
        CreatureID.Gog,
        CreatureID.Walking_Dead,
        CreatureID.Harpy,
        CreatureID.Wolf_Rider,
        CreatureID.Lizardman,
        CreatureID.Air_Elemental,
        CreatureID.Crew_Mate,
        CreatureID.Mechanic,
        CreatureID.Marksman,
        CreatureID.Battle_Dwarf,
        CreatureID.Obsidian_Gargoyle,
        CreatureID.Magog,
        CreatureID.Zombie,
        CreatureID.Harpy_Hag,
        CreatureID.Wolf_Raider,
        CreatureID.Lizard_Warrior,
        CreatureID.Storm_Elemental,
        CreatureID.Seaman,
        CreatureID.Engineer,
        CreatureID.Rogue,
        CreatureID.Boar,
        CreatureID.Leprechaun
    ),
    CreatureLevel.Level_3: (
        CreatureID.Griffin,
        CreatureID.Wood_Elf,
        CreatureID.Stone_Golem,
        CreatureID.Hell_Hound,
        CreatureID.Wight,
        CreatureID.Beholder,
        CreatureID.Orc,
        CreatureID.Serpent_Fly,
        CreatureID.Water_Elemental,
        CreatureID.Pirate,
        CreatureID.Armadillo,
        CreatureID.Royal_Griffin,
        CreatureID.Grand_Elf,
        CreatureID.Iron_Golem,
        CreatureID.Cerberus,
        CreatureID.Wraith,
        CreatureID.Evil_Eye,
        CreatureID.Orc_Chieftain,
        CreatureID.Dragon_Fly,
        CreatureID.Ice_Elemental,
        CreatureID.Corsair,
        CreatureID.Bellwether_Armadillo,
        CreatureID.Sea_Dog,
        CreatureID.Nomad,
        CreatureID.Mummy
    ),
    CreatureLevel.Level_4: (
        CreatureID.Swordsman,
        CreatureID.Pegasus,
        CreatureID.Mage,
        CreatureID.Demon,
        CreatureID.Vampire,
        CreatureID.Medusa,
        CreatureID.Ogre,
        CreatureID.Basilisk,
        CreatureID.Fire_Elemental,
        CreatureID.Stormbird,
        CreatureID.Automaton,
        CreatureID.Crusader,
        CreatureID.Silver_Pegasus,
        CreatureID.Arch_Mage,
        CreatureID.Horned_Demon,
        CreatureID.Vampire_Lord,
        CreatureID.Medusa_Queen,
        CreatureID.Ogre_Mage,
        CreatureID.Greater_Basilisk,
        CreatureID.Energy_Elemental,
        CreatureID.Ayssid,
        CreatureID.Sentinel_Automaton,
        CreatureID.Sharpshooter,
        CreatureID.Satyr,
        CreatureID.Steel_Golem
    ),
    CreatureLevel.Level_5: (
        CreatureID.Monk,
        CreatureID.Dendroid_Guard,
        CreatureID.Genie,
        CreatureID.Pit_Fiend,
        CreatureID.Lich,
        CreatureID.Minotaur,
        CreatureID.Roc,
        CreatureID.Gorgon,
        CreatureID.Earth_Elemental,
        CreatureID.Sea_Witch,
        CreatureID.Sandworm,
        CreatureID.Zealot,
        CreatureID.Dendroid_Soldier,
        CreatureID.Master_Genie,
        CreatureID.Pit_Lord,
        CreatureID.Power_Lich,
        CreatureID.Minotaur_King,
        CreatureID.Thunderbird,
        CreatureID.Mighty_Gorgon,
        CreatureID.Magma_Elemental,
        CreatureID.Sorceress,
        CreatureID.Olgoi_Khorkhoi,
        CreatureID.Troll,
        CreatureID.Gold_Golem,
        CreatureID.Fangarm
    ),
    CreatureLevel.Level_6: (
        CreatureID.Cavalier,
        CreatureID.Unicorn,
        CreatureID.Naga,
        CreatureID.Efreeti,
        CreatureID.Black_Knight,
        CreatureID.Manticore,
        CreatureID.Cyclops,
        CreatureID.Wyvern,
        CreatureID.Psychic_Elemental,
        CreatureID.Nix,
        CreatureID.Gunslinger,
        CreatureID.Champion,
        CreatureID.War_Unicorn,
        CreatureID.Naga_Queen,
        CreatureID.Efreet_Sultan,
        CreatureID.Dread_Knight,
        CreatureID.Scorpicore,
        CreatureID.Cyclops_King,
        CreatureID.Wyvern_Monarch,
        CreatureID.Magic_Elemental,
        CreatureID.Nix_Warrior,
        CreatureID.Bounty_Hunter,
        CreatureID.Diamond_Golem,
        CreatureID.Enchanter
    ),
    CreatureLevel.Level_7: (
        CreatureID.Angel,
        CreatureID.Green_Dragon,
        CreatureID.Giant,
        CreatureID.Devil,
        CreatureID.Bone_Dragon,
        CreatureID.Red_Dragon,
        CreatureID.Behemoth,
        CreatureID.Hydra,
        CreatureID.Firebird,
        CreatureID.Sea_Serpent,
        CreatureID.Couatl,
        CreatureID.Dreadnought,
        CreatureID.Archangel,
        CreatureID.Gold_Dragon,
        CreatureID.Titan,
        CreatureID.Arch_Devil,
        CreatureID.Ghost_Dragon,
        CreatureID.Black_Dragon,
        CreatureID.Ancient_Behemoth,
        CreatureID.Phoenix,
        CreatureID.Haspid,
        CreatureID.Crimson_Couatl,
        CreatureID.Juggernaut,
        CreatureID.Faerie_Dragon,
        CreatureID.Rust_Dragon,
        CreatureID.Crystal_Dragon,
        CreatureID.Azure_Dragon,
    )
}

creature_replace_always: dict[CreatureID, tuple[Replacement, ...]] = {
    CreatureID.Pegasus: (
        Replacement(CreatureID.Vampire),
        Replacement(CreatureID.Fire_Elemental),
        Replacement(CreatureID.Automaton)
    ),
    CreatureID.Silver_Pegasus: (
        Replacement(CreatureID.Vampire_Lord),
        Replacement(CreatureID.Energy_Elemental),
        Replacement(CreatureID.Sentinel_Automaton)
    ),
    CreatureID.Unicorn: (
        Replacement(CreatureID.Black_Knight),
        Replacement(CreatureID.Naga),
        Replacement(CreatureID.Nix),
        Replacement(CreatureID.Psychic_Elemental)
    ),
    CreatureID.War_Unicorn: (
        Replacement(CreatureID.Dread_Knight),
        Replacement(CreatureID.Naga_Queen),
        Replacement(CreatureID.Nix_Warrior),
        Replacement(CreatureID.Magic_Elemental)
    ),
    CreatureID.Green_Dragon: (
        Replacement(CreatureID.Firebird, 1.5),
        Replacement(CreatureID.Bone_Dragon, 1.5),
        Replacement(CreatureID.Devil),
        Replacement(CreatureID.Angel, 0.9),
    ),
    CreatureID.Gold_Dragon: (
        Replacement(CreatureID.Phoenix, 1.5),
        Replacement(CreatureID.Ghost_Dragon, 1.5),
        Replacement(CreatureID.Arch_Devil),
        Replacement(CreatureID.Archangel, 0.9),
    ),
    CreatureID.Faerie_Dragon: (
        Replacement(CreatureID.Crystal_Dragon, 0.8),
    ),
    CreatureID.Rust_Dragon: (
        Replacement(CreatureID.Crystal_Dragon, 0.9),
    ),
    CreatureID.Azure_Dragon: (
        Replacement(CreatureID.Crystal_Dragon, 1.5),
    )
}

creature_replace_enemy: dict[CreatureID, tuple[Replacement, ...]] = {
    CreatureID.Griffin: (
        Replacement(CreatureID.Wight),
        Replacement(CreatureID.Serpent_Fly),
        Replacement(CreatureID.Fire_Elemental, 0.9)
    ),
    CreatureID.Royal_Griffin: (
        Replacement(CreatureID.Wraith),
        Replacement(CreatureID.Dragon_Fly),
        Replacement(CreatureID.Fire_Elemental)
    ),
    CreatureID.Armadillo: (
        Replacement(CreatureID.Stone_Golem),
        Replacement(CreatureID.Hell_Hound),
        Replacement(CreatureID.Mummy),
        Replacement(CreatureID.Nomad),
    ),
    CreatureID.Bellwether_Armadillo: (
        Replacement(CreatureID.Iron_Golem),
        Replacement(CreatureID.Cerberus),
        Replacement(CreatureID.Mummy),
        Replacement(CreatureID.Nomad),
    ),
    CreatureID.Stormbird: (
        Replacement(CreatureID.Vampire),
        Replacement(CreatureID.Fire_Elemental),
        Replacement(CreatureID.Automaton)
    ),
    CreatureID.Ayssid: (
        Replacement(CreatureID.Vampire_Lord),
        Replacement(CreatureID.Energy_Elemental),
        Replacement(CreatureID.Sentinel_Automaton)
    ),
    CreatureID.Manticore: (
        Replacement(CreatureID.Wyvern),
        Replacement(CreatureID.Efreeti),
        Replacement(CreatureID.Master_Genie, 1.1),
        Replacement(CreatureID.Sandworm, 1.1),
    ),
    CreatureID.Scorpicore: (
        Replacement(CreatureID.Wyvern_Monarch),
        Replacement(CreatureID.Efreet_Sultan),
        Replacement(CreatureID.Master_Genie, 1.25),
        Replacement(CreatureID.Olgoi_Khorkhoi, 1.1)
    ),
    CreatureID.Couatl: (
        Replacement(CreatureID.Bone_Dragon),
        Replacement(CreatureID.Firebird),
        Replacement(CreatureID.Devil, 0.9),
        Replacement(CreatureID.Angel, 0.8),
    ),
    CreatureID.Crimson_Couatl: (
        Replacement(CreatureID.Ghost_Dragon),
        Replacement(CreatureID.Phoenix),
        Replacement(CreatureID.Arch_Devil, 0.8),
        Replacement(CreatureID.Archangel, 0.7),
    ),
    CreatureID.Red_Dragon: (
        Replacement(CreatureID.Firebird, 1.5),
        Replacement(CreatureID.Bone_Dragon, 1.5),
        Replacement(CreatureID.Devil),
        Replacement(CreatureID.Angel, 0.9),
    ),
    CreatureID.Black_Dragon: (
        Replacement(CreatureID.Phoenix, 1.5),
        Replacement(CreatureID.Ghost_Dragon, 1.5),
        Replacement(CreatureID.Arch_Devil),
        Replacement(CreatureID.Archangel, 0.9),
    ),
    CreatureID.Hydra: (
        Replacement(CreatureID.Behemoth),
        Replacement(CreatureID.Dreadnought),
        Replacement(CreatureID.Sea_Serpent)
    ),
    CreatureID.Chaos_Hydra: (
        Replacement(CreatureID.Ancient_Behemoth),
        Replacement(CreatureID.Juggernaut),
        Replacement(CreatureID.Haspid, 0.8)
    )
}

creature_replacements: dict[ReplacementContext, dict[CreatureID, tuple[Replacement, ...]]] = {
    ReplacementContext.ALWAYS: creature_replace_always,
    ReplacementContext.ENEMY: creature_replace_enemy,
    ReplacementContext.FRIEND: {}
}

def random_replacement_for(creature: CreatureID, context: ReplacementContext) -> Replacement | None:
    for ctx in {context, ReplacementContext.ALWAYS}:
        replacements = creature_replacements[ctx]
        if creature in replacements:
            return random.choice(replacements[creature])
    return None

dont_generate_cratures: frozenset[CreatureID] = frozenset(creature_replace_always.keys()).union(creature_replace_enemy.keys())
allowed_creatures_per_level: dict[CreatureLevel, tuple[CreatureID, ...]] = {
    level: tuple(c for c in creatures if c not in dont_generate_cratures)
    for level, creatures in creatures_per_level.items()
}

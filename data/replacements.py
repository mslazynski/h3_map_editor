import os
import random
from enum import Enum, auto
from dataclasses import dataclass

from data.creatures import ID as CreatureID, CreatureLevel, creatures_per_level


class ReplacementContext(Enum):
    ALWAYS = auto()
    ENEMY = auto()
    FRIEND = auto()

@dataclass
class Replacement:
    id: CreatureID
    multiplier: float = 1.0


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


dont_generate_creatures: set[CreatureID] = set(creature_replace_always.keys()).union(creature_replace_enemy.keys())
allowed_creatures_per_level: dict[CreatureLevel, tuple[CreatureID, ...]] = {
    level: tuple(c for c in creatures if c not in dont_generate_creatures)
    for level, creatures in creatures_per_level.items()
}

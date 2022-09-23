

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar

from pokeapi.typ import APIType, HasEndpoint, HasName


@dataclass
class Berry(HasName):
    """ Berries are small fruits that can provide HP and status condition restoration, stat enhancement, and even damage negation when eaten by Pokémon. Check out Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/berry/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # Time it takes the tree to grow one stage, in hours. Berry trees go through four of these growth stages before they can be picked.
    growth_time: int

    # The maximum number of these berries that can grow on one tree in Generation IV.
    max_harvest: int

    # The power of the move "Natural Gift" when used with this Berry.
    natural_gift_power: int

    # The size of this Berry, in millimeters.
    size: int

    # The smoothness of this Berry, used in making Pokéblocks or Poffins.
    smoothness: int

    # The speed at which this Berry dries out the soil as it grows. A higher rate means the soil dries more quickly.
    soil_dryness: int

    # The firmness of this berry, used in making Pokéblocks or Poffins.
    firmness: NamedAPIResource[BerryFirmness]

    # A list of references to each flavor a berry can have and the potency of each of those flavors in regard to this berry.
    flavors: list[BerryFlavorMap]

    # Berries are actually items. This is a reference to the item specific data for this berry.
    item: NamedAPIResource[Item]

    # The type inherited by "Natural Gift" when used with this Berry.
    natural_gift_type: NamedAPIResource[Type]

@dataclass
class BerryFlavorMap(APIType):
    # How powerful the referenced flavor is for this berry.
    potency: int

    # The referenced berry flavor.
    flavor: NamedAPIResource[BerryFlavor]

@dataclass
class BerryFirmness(HasName):
    """ Berries can be soft or hard. Check out Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/berry-firmness/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # A list of the berries with this firmness.
    berries: list[NamedAPIResource[Berry]]

    # The name of this resource listed in different languages.
    names: list[Name]

@dataclass
class BerryFlavor(HasName):
    """ Flavors determine whether a Pokémon will benefit or suffer from eating a berry based on their nature. Check out Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/berry-flavor/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # A list of the berries with this flavor.
    berries: list[FlavorBerryMap]

    # The contest type that correlates with this berry flavor.
    contest_type: NamedAPIResource[ContestType]

    # The name of this resource listed in different languages.
    names: list[Name]

@dataclass
class FlavorBerryMap(APIType):
    # How powerful the referenced flavor is for this berry.
    potency: int

    # The berry with the referenced flavor.
    berry: NamedAPIResource[Berry]


@dataclass
class ContestType(HasName):
    """ Contest types are categories judges used to weigh a Pokémon's condition in Pokémon contests. Check out Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/contest-type/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The berry flavor that correlates with this contest type.
    berry_flavor: NamedAPIResource[BerryFlavor]

    # The name of this contest type listed in different languages.
    names: list[ContestName]

@dataclass
class ContestName(APIType):
    # The name for this contest.
    name: str

    # The color associated with this contest's name.
    color: str

    # The language that this name is in.
    language: NamedAPIResource[Language]

@dataclass
class ContestEffect(HasEndpoint):
    """ Contest effects refer to the effects of moves when used in contests. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/contest-effect/"

    # The identifier for this resource.
    id: int

    # The base number of hearts the user of this move gets.
    appeal: int

    # The base number of hearts the user's opponent loses.
    jam: int

    # The result of this contest effect listed in different languages.
    effect_entries: list[Effect]

    # The flavor text of this contest effect listed in different languages.
    flavor_text_entries: list[FlavorText]

@dataclass
class SuperContestEffect(HasEndpoint):
    """ Super contest effects refer to the effects of moves when used in super contests. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/super-contest-effect/"

    # The identifier for this resource.
    id: int

    # The level of appeal this super contest effect has.
    appeal: int

    # The flavor text of this super contest effect listed in different languages.
    flavor_text_entries: list[FlavorText]

    # A list of moves that have the effect when used in super contests.
    moves: list[NamedAPIResource[Move]]


@dataclass
class EncounterMethod(HasName):
    """ Methods by which the player might can encounter Pokémon in the wild, e.g., walking in tall grass. Check out Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/encounter-method/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # A good value for sorting.
    order: int

    # The name of this resource listed in different languages.
    names: list[Name]

@dataclass
class EncounterCondition(HasName):
    """ Conditions which affect what pokemon might appear in the wild, e.g., day or night. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/encounter-condition/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of possible values for this encounter condition.
    values: list[NamedAPIResource[EncounterConditionValue]]

@dataclass
class EncounterConditionValue(HasName):
    """ Encounter condition values are the various states that an encounter condition can have, i.e., time of day can be either day or night. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/encounter-condition-value/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The condition this encounter condition value pertains to.
    condition: NamedAPIResource[EncounterCondition]

    # The name of this resource listed in different languages.
    names: list[Name]


@dataclass
class EvolutionChain(HasEndpoint):
    """ Evolution chains are essentially family trees. They start with the lowest stage within a family and detail evolution conditions for each as well as Pokémon they can evolve into up through the hierarchy. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/evolution-chain/"

    # The identifier for this resource.
    id: int

    # The item that a Pokémon would be holding when mating that would trigger the egg hatching a baby Pokémon rather than a basic Pokémon.
    baby_trigger_item: NamedAPIResource[Item]

    # The base chain link object. Each link contains evolution details for a Pokémon in the chain. Each link references the next Pokémon in the natural evolution order.
    chain: ChainLink

@dataclass
class ChainLink(APIType):
    # Whether or not this link is for a baby Pokémon. This would only ever be true on the base link.
    is_baby: bool

    # The Pokémon species at this point in the evolution chain.
    species: NamedAPIResource[PokemonSpecies]

    # All details regarding the specific details of the referenced Pokémon species evolution.
    evolution_details: list[EvolutionDetail]

    # A List of chain objects.
    evolves_to: list[ChainLink]

@dataclass
class EvolutionDetail(APIType):
    # The item required to cause evolution this into Pokémon species.
    item: NamedAPIResource[Item]

    # The type of event that triggers evolution into this Pokémon species.
    trigger: NamedAPIResource[EvolutionTrigger]

    # The id of the gender of the evolving Pokémon species must be in order to evolve into this Pokémon species.
    gender: int

    # The item the evolving Pokémon species must be holding during the evolution trigger event to evolve into this Pokémon species.
    held_item: NamedAPIResource[Item]

    # The move that must be known by the evolving Pokémon species during the evolution trigger event in order to evolve into this Pokémon species.
    known_move: NamedAPIResource[Move]

    # The evolving Pokémon species must know a move with this type during the evolution trigger event in order to evolve into this Pokémon species.
    known_move_type: NamedAPIResource[Type]

    # The location the evolution must be triggered at.
    location: NamedAPIResource[Location]

    # The minimum required level of the evolving Pokémon species to evolve into this Pokémon species.
    min_level: int

    # The minimum required level of happiness the evolving Pokémon species to evolve into this Pokémon species.
    min_happiness: int

    # The minimum required level of beauty the evolving Pokémon species to evolve into this Pokémon species.
    min_beauty: int

    # The minimum required level of affection the evolving Pokémon species to evolve into this Pokémon species.
    min_affection: int

    # Whether or not it must be raining in the overworld to cause evolution this Pokémon species.
    needs_overworld_rain: bool

    # The Pokémon species that must be in the players party in order for the evolving Pokémon species to evolve into this Pokémon species.
    party_species: NamedAPIResource[PokemonSpecies]

    # The player must have a Pokémon of this type in their party during the evolution trigger event in order for the evolving Pokémon species to evolve into this Pokémon species.
    party_type: NamedAPIResource[Type]

    # The required relation between the Pokémon's Attack and Defense stats. 1 means Attack > Defense. 0 means Attack = Defense. -1 means Attack < Defense.
    relative_physical_stats: int

    # The required time of day. Day or night.
    time_of_day: str

    # Pokémon species for which this one must be traded.
    trade_species: NamedAPIResource[PokemonSpecies]

    # Whether or not the 3DS needs to be turned upside-down as this Pokémon levels up.
    turn_upside_down: bool

@dataclass
class EvolutionTrigger(HasName):
    """ Evolution triggers are the events and conditions that cause a Pokémon to evolve. Check out Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/evolution-trigger/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of pokemon species that result from this evolution trigger.
    pokemon_species: list[NamedAPIResource[PokemonSpecies]]


@dataclass
class Generation(HasName):
    """ A generation is a grouping of the Pokémon games that separates them based on the Pokémon they include. In each generation, a new set of Pokémon, Moves, Abilities and Types that did not exist in the previous generation are released. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/generation/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # A list of abilities that were introduced in this generation.
    abilities: list[NamedAPIResource[Ability]]

    # The name of this resource listed in different languages.
    names: list[Name]

    # The main region travelled in this generation.
    main_region: NamedAPIResource[Region]

    # A list of moves that were introduced in this generation.
    moves: list[NamedAPIResource[Move]]

    # A list of Pokémon species that were introduced in this generation.
    pokemon_species: list[NamedAPIResource[PokemonSpecies]]

    # A list of types that were introduced in this generation.
    types: list[NamedAPIResource[Type]]

    # A list of version groups that were introduced in this generation.
    version_groups: list[NamedAPIResource[VersionGroup]]

@dataclass
class Pokedex(HasName):
    """ A Pokédex is a handheld electronic encyclopedia device; one which is capable of recording and retaining information of the various Pokémon in a given region with the exception of the national dex and some smaller dexes related to portions of a region. See Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/pokedex/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # Whether or not this Pokédex originated in the main series of the video games.
    is_main_series: bool

    # The description of this resource listed in different languages.
    descriptions: list[Description]

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of Pokémon catalogued in this Pokédex and their indexes.
    pokemon_entries: list[PokemonEntry]

    # The region this Pokédex catalogues Pokémon for.
    region: NamedAPIResource[Region]

    # A list of version groups this Pokédex is relevant to.
    version_groups: list[NamedAPIResource[VersionGroup]]

@dataclass
class PokemonEntry(APIType):
    # The index of this Pokémon species entry within the Pokédex.
    entry_number: int

    # The Pokémon species being encountered.
    pokemon_species: NamedAPIResource[PokemonSpecies]

@dataclass
class Version(HasName):
    """ Versions of the games, e.g., Red, Blue or Yellow. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/version/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The name of this resource listed in different languages.
    names: list[Name]

    # The version group this version belongs to.
    version_group: NamedAPIResource[VersionGroup]

@dataclass
class VersionGroup(HasName):
    """ Version groups categorize highly similar versions of the games. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/version-group/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # Order for sorting. Almost by date of release, except similar versions are grouped together.
    order: int

    # The generation this version was introduced in.
    generation: NamedAPIResource[Generation]

    # A list of methods in which Pokémon can learn moves in this version group.
    move_learn_methods: list[NamedAPIResource[MoveLearnMethod]]

    # A list of Pokédexes introduces in this version group.
    pokedexes: list[NamedAPIResource[Pokedex]]

    # A list of regions that can be visited in this version group.
    regions: list[NamedAPIResource[Region]]

    # The versions this version group owns.
    versions: list[NamedAPIResource[Version]]


@dataclass
class Item(HasName):
    """ An item is an object in the games which the player can pick up, keep in their bag, and use in some manner. They have various uses, including healing, powering up, helping catch Pokémon, or to access a new area. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/item/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The price of this item in stores.
    cost: int

    # The power of the move Fling when used with this item.
    fling_power: int

    # The effect of the move Fling when used with this item.
    fling_effect: NamedAPIResource[ItemFlingEffect]

    # A list of attributes this item has.
    attributes: list[NamedAPIResource[ItemAttribute]]

    # The category of items this item falls into.
    category: NamedAPIResource[ItemCategory]

    # The effect of this ability listed in different languages.
    effect_entries: list[VerboseEffect]

    # The flavor text of this ability listed in different languages.
    flavor_text_entries: list[VersionGroupFlavorText]

    # A list of game indices relevent to this item by generation.
    game_indices: list[GenerationGameIndex]

    # The name of this item listed in different languages.
    names: list[Name]

    # A set of sprites used to depict this item in the game.
    sprites: ItemSprites

    # A list of Pokémon that might be found in the wild holding this item.
    held_by_pokemon: list[ItemHolderPokemon]

    # An evolution chain this item requires to produce a bay during mating.
    baby_trigger_for: APIResource[EvolutionChain]

    # A list of the machines related to this item.
    machines: list[MachineVersionDetail]

@dataclass
class ItemSprites(APIType):
    # The default depiction of this item.
    default: str

@dataclass
class ItemHolderPokemon(APIType):
    # The Pokémon that holds this item.
    pokemon: NamedAPIResource[Pokemon]

    # The details for the version that this item is held in by the Pokémon.
    version_details: list[ItemHolderPokemonVersionDetail]

@dataclass
class ItemHolderPokemonVersionDetail(APIType):
    # How often this Pokémon holds this item in this version.
    rarity: int

    # The version that this item is held in by the Pokémon.
    version: NamedAPIResource[Version]

@dataclass
class ItemAttribute(HasName):
    """ Item attributes define particular aspects of items, e.g. "usable in battle" or "consumable". """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/item-attribute/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # A list of items that have this attribute.
    items: list[NamedAPIResource[Item]]

    # The name of this item attribute listed in different languages.
    names: list[Name]

    # The description of this item attribute listed in different languages.
    descriptions: list[Description]

@dataclass
class ItemCategory(HasName):
    """ Item categories determine where items will be placed in the players bag. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/item-category/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # A list of items that are a part of this category.
    items: list[NamedAPIResource[Item]]

    # The name of this item category listed in different languages.
    names: list[Name]

    # The pocket items in this category would be put in.
    pocket: NamedAPIResource[ItemPocket]

@dataclass
class ItemFlingEffect(HasName):
    """ The various effects of the move "Fling" when used with different items. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/item-fling-effect/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The result of this fling effect listed in different languages.
    effect_entries: list[Effect]

    # A list of items that have this fling effect.
    items: list[NamedAPIResource[Item]]

@dataclass
class ItemPocket(HasName):
    """ Pockets within the players bag used for storing items by category. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/item-pocket/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # A list of item categories that are relevant to this item pocket.
    categories: list[NamedAPIResource[ItemCategory]]

    # The name of this resource listed in different languages.
    names: list[Name]


@dataclass
class Location(HasName):
    """ Locations that can be visited within the games. Locations make up sizable portions of regions, like cities or routes. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/location/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The region this location can be found in.
    region: NamedAPIResource[Region]

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of game indices relevent to this location by generation.
    game_indices: list[GenerationGameIndex]

    # Areas that can be found within this location.
    areas: list[NamedAPIResource[LocationArea]]

@dataclass
class LocationArea(HasName):
    """ Location areas are sections of areas, such as floors in a building or cave. Each area has its own set of possible Pokémon encounters. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/location-area/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The internal id of an API resource within game data.
    game_index: int

    # A list of methods in which Pokémon may be encountered in this area and how likely the method will occur depending on the version of the game.
    encounter_method_rates: list[EncounterMethodRate]

    # The region this location area can be found in.
    location: NamedAPIResource[Location]

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of Pokémon that can be encountered in this area along with version specific details about the encounter.
    pokemon_encounters: list[PokemonEncounter]

@dataclass
class EncounterMethodRate(APIType):
    # The method in which Pokémon may be encountered in an area..
    encounter_method: NamedAPIResource[EncounterMethod]

    # The chance of the encounter to occur on a version of the game.
    version_details: list[EncounterVersionDetails]

@dataclass
class EncounterVersionDetails(APIType):
    # The chance of an encounter to occur.
    rate: int

    # The version of the game in which the encounter can occur with the given chance.
    version: NamedAPIResource[Version]

@dataclass
class PokemonEncounter(APIType):
    # The Pokémon being encountered.
    pokemon: NamedAPIResource[Pokemon]

    # A list of versions and encounters with Pokémon that might happen in the referenced location area.
    version_details: list[VersionEncounterDetail]

@dataclass
class PalParkArea(HasName):
    """ Areas used for grouping Pokémon encounters in Pal Park. They're like habitats that are specific to Pal Park. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/pal-park-area/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of Pokémon encountered in thi pal park area along with details.
    pokemon_encounters: list[PalParkEncounterSpecies]

@dataclass
class PalParkEncounterSpecies(APIType):
    # The base score given to the player when this Pokémon is caught during a pal park run.
    base_score: int

    # The base rate for encountering this Pokémon in this pal park area.
    rate: int

    # The Pokémon species being encountered.
    pokemon_species: NamedAPIResource[PokemonSpecies]

@dataclass
class Region(HasEndpoint):
    """ A region is an organized area of the Pokémon world. Most often, the main difference between regions is the species of Pokémon that can be encountered within them. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/region/"

    # The identifier for this resource.
    id: int

    # A list of locations that can be found in this region.
    locations: list[NamedAPIResource[Location]]

    # The name for this resource.
    name: str

    # The name of this resource listed in different languages.
    names: list[Name]

    # The generation this region was introduced in.
    main_generation: NamedAPIResource[Generation]

    # A list of pokédexes that catalogue Pokémon in this region.
    pokedexes: list[NamedAPIResource[Pokedex]]

    # A list of version groups where this region can be visited.
    version_groups: list[NamedAPIResource[VersionGroup]]


@dataclass
class Machine(HasEndpoint):
    """ Machines are the representation of items that teach moves to Pokémon. They vary from version to version, so it is not certain that one specific TM or HM corresponds to a single Machine. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/machine/"

    # The identifier for this resource.
    id: int

    # The TM or HM item that corresponds to this machine.
    item: NamedAPIResource[Item]

    # The move that is taught by this machine.
    move: NamedAPIResource[Move]

    # The version group that this machine applies to.
    version_group: NamedAPIResource[VersionGroup]


@dataclass
class Move(HasName):
    """ Moves are the skills of Pokémon in battle. In battle, a Pokémon uses one move each turn. Some moves can be used outside of battle as well, usually for the purpose of removing obstacles or exploring new areas. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/move/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The percent value of how likely this move is to be successful.
    accuracy: int

    # The percent value of how likely it is this moves effect will happen.
    effect_chance: int

    # Power points. The number of times this move can be used.
    pp: int

    # A value between -8 and 8. Sets the order in which moves are executed during battle. See Bulbapedia for greater detail.
    priority: int

    # The base power of this move with a value of 0 if it does not have a base power.
    power: int

    # A detail of normal and super contest combos that require this move.
    contest_combos: ContestComboSets

    # The type of appeal this move gives a Pokémon when used in a contest.
    contest_type: NamedAPIResource[ContestType]

    # The effect the move has when used in a contest.
    contest_effect: APIResource[ContestEffect]

    # The type of damage the move inflicts on the target, e.g. physical.
    damage_class: NamedAPIResource[MoveDamageClass]

    # The effect of this move listed in different languages.
    effect_entries: list[VerboseEffect]

    # The list of previous effects this move has had across version groups of the games.
    effect_changes: list[AbilityEffectChange]

    # List of Pokemon that can learn the move
    learned_by_pokemon: list[NamedAPIResource[Pokemon]]

    # The flavor text of this move listed in different languages.
    flavor_text_entries: list[MoveFlavorText]

    # The generation in which this move was introduced.
    generation: NamedAPIResource[Generation]

    # A list of the machines that teach this move.
    machines: list[MachineVersionDetail]

    # Metadata about this move
    meta: MoveMetaData

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of move resource value changes across version groups of the game.
    past_values: list[PastMoveStatValues]

    # A list of stats this moves effects and how much it effects them.
    stat_changes: list[MoveStatChange]

    # The effect the move has when used in a super contest.
    super_contest_effect: APIResource[SuperContestEffect]

    # The type of target that will receive the effects of the attack.
    target: NamedAPIResource[MoveTarget]

    # The elemental type of this move.
    type: NamedAPIResource[Type]

@dataclass
class ContestComboSets(APIType):
    # A detail of moves this move can be used before or after, granting additional appeal points in contests.
    normal: ContestComboDetail

    # A detail of moves this move can be used before or after, granting additional appeal points in super contests.
    super: ContestComboDetail

@dataclass
class ContestComboDetail(APIType):
    # A list of moves to use before this move.
    use_before: list[NamedAPIResource[Move]]

    # A list of moves to use after this move.
    use_after: list[NamedAPIResource[Move]]

@dataclass
class MoveFlavorText(APIType):
    # The localized flavor text for an api resource in a specific language.
    flavor_text: str

    # The language this name is in.
    language: NamedAPIResource[Language]

    # The version group that uses this flavor text.
    version_group: NamedAPIResource[VersionGroup]

@dataclass
class MoveMetaData(APIType):
    # The status ailment this move inflicts on its target.
    ailment: NamedAPIResource[MoveAilment]

    # The category of move this move falls under, e.g. damage or ailment.
    category: NamedAPIResource[MoveCategory]

    # The minimum number of times this move hits. Null if it always only hits once.
    min_hits: int

    # The maximum number of times this move hits. Null if it always only hits once.
    max_hits: int

    # The minimum number of turns this move continues to take effect. Null if it always only lasts one turn.
    min_turns: int

    # The maximum number of turns this move continues to take effect. Null if it always only lasts one turn.
    max_turns: int

    # HP drain, in percent of damage done.
    drain: int

    # The amount of hp gained by the attacking Pokemon, in percent of it's maximum HP.
    healing: int

    # Critical hit rate bonus.
    crit_rate: int

    # The likelihood this attack will cause an ailment.
    ailment_chance: int

    # The likelihood this attack will cause the target Pokémon to flinch.
    flinch_chance: int

    # The likelihood this attack will cause a stat change in the target Pokémon.
    stat_chance: int

@dataclass
class MoveStatChange(APIType):
    # The amount of change.
    change: int

    # The stat being affected.
    stat: NamedAPIResource[Stat]

@dataclass
class PastMoveStatValues(APIType):
    # The percent value of how likely this move is to be successful.
    accuracy: int

    # The percent value of how likely it is this moves effect will take effect.
    effect_chance: int

    # The base power of this move with a value of 0 if it does not have a base power.
    power: int

    # Power points. The number of times this move can be used.
    pp: int

    # The effect of this move listed in different languages.
    effect_entries: list[VerboseEffect]

    # The elemental type of this move.
    type: NamedAPIResource[Type]

    # The version group in which these move stat values were in effect.
    version_group: NamedAPIResource[VersionGroup]

@dataclass
class MoveAilment(HasName):
    """ Move Ailments are status conditions caused by moves used during battle. See Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/move-ailment/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # A list of moves that cause this ailment.
    moves: list[NamedAPIResource[Move]]

    # The name of this resource listed in different languages.
    names: list[Name]

@dataclass
class MoveBattleStyle(HasName):
    """ Styles of moves when used in the Battle Palace. See Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/move-battle-style/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The name of this resource listed in different languages.
    names: list[Name]

@dataclass
class MoveCategory(HasName):
    """ Very general categories that loosely group move effects. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/move-category/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # A list of moves that fall into this category.
    moves: list[NamedAPIResource[Move]]

    # The description of this resource listed in different languages.
    descriptions: list[Description]

@dataclass
class MoveDamageClass(HasName):
    """ Damage classes moves can have, e.g. physical, special, or non-damaging. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/move-damage-class/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The description of this resource listed in different languages.
    descriptions: list[Description]

    # A list of moves that fall into this damage class.
    moves: list[NamedAPIResource[Move]]

    # The name of this resource listed in different languages.
    names: list[Name]

@dataclass
class MoveLearnMethod(HasName):
    """ Methods by which Pokémon can learn moves. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/move-learn-method/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The description of this resource listed in different languages.
    descriptions: list[Description]

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of version groups where moves can be learned through this method.
    version_groups: list[NamedAPIResource[VersionGroup]]

@dataclass
class MoveTarget(HasName):
    """ Targets moves can be directed at during battle. Targets can be Pokémon, environments or even other moves. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/move-target/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The description of this resource listed in different languages.
    descriptions: list[Description]

    # A list of moves that that are directed at this target.
    moves: list[NamedAPIResource[Move]]

    # The name of this resource listed in different languages.
    names: list[Name]


@dataclass
class Ability(HasName):
    """ Abilities provide passive effects for Pokémon in battle or in the overworld. Pokémon have multiple possible abilities but can have only one ability at a time. Check out Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/ability/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # Whether or not this ability originated in the main series of the video games.
    is_main_series: bool

    # The generation this ability originated in.
    generation: NamedAPIResource[Generation]

    # The name of this resource listed in different languages.
    names: list[Name]

    # The effect of this ability listed in different languages.
    effect_entries: list[VerboseEffect]

    # The list of previous effects this ability has had across version groups.
    effect_changes: list[AbilityEffectChange]

    # The flavor text of this ability listed in different languages.
    flavor_text_entries: list[AbilityFlavorText]

    # A list of Pokémon that could potentially have this ability.
    pokemon: list[AbilityPokemon]

@dataclass
class AbilityEffectChange(APIType):
    # The previous effect of this ability listed in different languages.
    effect_entries: list[Effect]

    # The version group in which the previous effect of this ability originated.
    version_group: NamedAPIResource[VersionGroup]

@dataclass
class AbilityFlavorText(APIType):
    # The localized name for an API resource in a specific language.
    flavor_text: str

    # The language this text resource is in.
    language: NamedAPIResource[Language]

    # The version group that uses this flavor text.
    version_group: NamedAPIResource[VersionGroup]

@dataclass
class AbilityPokemon(APIType):
    # Whether or not this a hidden ability for the referenced Pokémon.
    is_hidden: bool

    # Pokémon have 3 ability 'slots' which hold references to possible abilities they could have. This is the slot of this ability for the referenced pokemon.
    slot: int

    # The Pokémon this ability could belong to.
    pokemon: NamedAPIResource[Pokemon]

@dataclass
class Characteristic(HasEndpoint):
    """ Characteristics indicate which stat contains a Pokémon's highest IV. A Pokémon's Characteristic is determined by the remainder of its highest IV divided by 5. Check out Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/characteristic/"

    # The identifier for this resource.
    id: int

    # The remainder of the highest stat/IV divided by 5.
    gene_modulo: int

    # The possible values of the highest stat that would result in a Pokémon recieving this characteristic when divided by 5.
    possible_values: list[int]

@dataclass
class EggGroup(HasName):
    """ Egg Groups are categories which determine which Pokémon are able to interbreed. Pokémon may belong to either one or two Egg Groups. Check out Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/egg-group/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of all Pokémon species that are members of this egg group.
    pokemon_species: list[NamedAPIResource[PokemonSpecies]]

@dataclass
class Gender(HasName):
    """ Genders were introduced in Generation II for the purposes of breeding Pokémon but can also result in visual differences or even different evolutionary lines. Check out Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/gender/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # A list of Pokémon species that can be this gender and how likely it is that they will be.
    pokemon_species_details: list[PokemonSpeciesGender]

    # A list of Pokémon species that required this gender in order for a Pokémon to evolve into them.
    required_for_evolution: list[NamedAPIResource[PokemonSpecies]]

@dataclass
class PokemonSpeciesGender(APIType):
    # The chance of this Pokémon being female, in eighths; or -1 for genderless.
    rate: int

    # A Pokémon species that can be the referenced gender.
    pokemon_species: NamedAPIResource[PokemonSpecies]

@dataclass
class GrowthRate(HasName):
    """ Growth rates are the speed with which Pokémon gain levels through experience. Check out Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/growth-rate/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The formula used to calculate the rate at which the Pokémon species gains level.
    formula: str

    # The descriptions of this characteristic listed in different languages.
    descriptions: list[Description]

    # A list of levels and the amount of experienced needed to atain them based on this growth rate.
    levels: list[GrowthRateExperienceLevel]

    # A list of Pokémon species that gain levels at this growth rate.
    pokemon_species: list[NamedAPIResource[PokemonSpecies]]

@dataclass
class GrowthRateExperienceLevel(APIType):
    # The level gained.
    level: int

    # The amount of experience required to reach the referenced level.
    experience: int

@dataclass
class Nature(HasName):
    """ Natures influence how a Pokémon's stats grow. See Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/nature/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The stat decreased by 10% in Pokémon with this nature.
    decreased_stat: NamedAPIResource[Stat]

    # The stat increased by 10% in Pokémon with this nature.
    increased_stat: NamedAPIResource[Stat]

    # The flavor hated by Pokémon with this nature.
    hates_flavor: NamedAPIResource[BerryFlavor]

    # The flavor liked by Pokémon with this nature.
    likes_flavor: NamedAPIResource[BerryFlavor]

    # A list of Pokéathlon stats this nature effects and how much it effects them.
    pokeathlon_stat_changes: list[NatureStatChange]

    # A list of battle styles and how likely a Pokémon with this nature is to use them in the Battle Palace or Battle Tent.
    move_battle_style_preferences: list[MoveBattleStylePreference]

    # The name of this resource listed in different languages.
    names: list[Name]

@dataclass
class NatureStatChange(APIType):
    # The amount of change.
    max_change: int

    # The stat being affected.
    pokeathlon_stat: NamedAPIResource[PokeathlonStat]

@dataclass
class MoveBattleStylePreference(APIType):
    # Chance of using the move, in percent, if HP is under one half.
    low_hp_preference: int

    # Chance of using the move, in percent, if HP is over one half.
    high_hp_preference: int

    # The move battle style.
    move_battle_style: NamedAPIResource[MoveBattleStyle]

@dataclass
class PokeathlonStat(HasName):
    """ Pokeathlon Stats are different attributes of a Pokémon's performance in Pokéathlons. In Pokéathlons, competitions happen on different courses; one for each of the different Pokéathlon stats. See Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/pokeathlon-stat/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The name of this resource listed in different languages.
    names: list[Name]

    # A detail of natures which affect this Pokéathlon stat positively or negatively.
    affecting_natures: NaturePokeathlonStatAffectSets

@dataclass
class NaturePokeathlonStatAffectSets(APIType):
    # A list of natures and how they change the referenced Pokéathlon stat.
    increase: list[NaturePokeathlonStatAffect]

    # A list of natures and how they change the referenced Pokéathlon stat.
    decrease: list[NaturePokeathlonStatAffect]

@dataclass
class NaturePokeathlonStatAffect(APIType):
    # The maximum amount of change to the referenced Pokéathlon stat.
    max_change: int

    # The nature causing the change.
    nature: NamedAPIResource[Nature]

@dataclass
class Pokemon(HasName):
    """ Pokémon are the creatures that inhabit the world of the Pokémon games. They can be caught using Pokéballs and trained by battling with other Pokémon. Each Pokémon belongs to a specific species but may take on a variant which makes it differ from other Pokémon of the same species, such as base stats, available abilities and typings. See Bulbapedia for greater detail. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/pokemon/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The base experience gained for defeating this Pokémon.
    base_experience: int

    # The height of this Pokémon in decimetres.
    height: int

    # Set for exactly one Pokémon used as the default for each species.
    is_default: bool

    # Order for sorting. Almost national order, except families are grouped together.
    order: int

    # The weight of this Pokémon in hectograms.
    weight: int

    # A list of abilities this Pokémon could potentially have.
    abilities: list[PokemonAbility]

    # A list of forms this Pokémon can take on.
    forms: list[NamedAPIResource[PokemonForm]]

    # A list of game indices relevent to Pokémon item by generation.
    game_indices: list[VersionGameIndex]

    # A list of items this Pokémon may be holding when encountered.
    held_items: list[PokemonHeldItem]

    # A link to a list of location areas, as well as encounter details pertaining to specific versions.
    location_area_encounters: str

    # A list of moves along with learn methods and level details pertaining to specific version groups.
    moves: list[PokemonMove]

    # A list of details showing types this pokémon had in previous generations
    past_types: list[PokemonTypePast]

    # A set of sprites used to depict this Pokémon in the game. A visual representation of the various sprites can be found at PokeAPI/sprites
    sprites: PokemonSprites

    # The species this Pokémon belongs to.
    species: NamedAPIResource[PokemonSpecies]

    # A list of base stat values for this Pokémon.
    stats: list[PokemonStat]

    # A list of details showing types this Pokémon has.
    types: list[PokemonType]

@dataclass
class PokemonAbility(APIType):
    # Whether or not this is a hidden ability.
    is_hidden: bool

    # The slot this ability occupies in this Pokémon species.
    slot: int

    # The ability the Pokémon may have.
    ability: NamedAPIResource[Ability]

@dataclass
class PokemonType(APIType):
    # The order the Pokémon's types are listed in.
    slot: int

    # The type the referenced Pokémon has.
    type: NamedAPIResource[Type]

@dataclass
class PokemonFormType(APIType):
    # The order the Pokémon's types are listed in.
    slot: int

    # The type the referenced Form has.
    type: NamedAPIResource[Type]

@dataclass
class PokemonTypePast(APIType):
    # The last generation in which the referenced pokémon had the listed types.
    generation: NamedAPIResource[Generation]

    # The types the referenced pokémon had up to and including the listed generation.
    types: list[PokemonType]

@dataclass
class PokemonHeldItem(APIType):
    # The item the referenced Pokémon holds.
    item: NamedAPIResource[Item]

    # The details of the different versions in which the item is held.
    version_details: list[PokemonHeldItemVersion]

@dataclass
class PokemonHeldItemVersion(APIType):
    # The version in which the item is held.
    version: NamedAPIResource[Version]

    # How often the item is held.
    rarity: int

@dataclass
class PokemonMove(APIType):
    # The move the Pokémon can learn.
    move: NamedAPIResource[Move]

    # The details of the version in which the Pokémon can learn the move.
    version_group_details: list[PokemonMoveVersion]

@dataclass
class PokemonMoveVersion(APIType):
    # The method by which the move is learned.
    move_learn_method: NamedAPIResource[MoveLearnMethod]

    # The version group in which the move is learned.
    version_group: NamedAPIResource[VersionGroup]

    # The minimum level to learn the move.
    level_learned_at: int

@dataclass
class PokemonStat(APIType):
    # The stat the Pokémon has.
    stat: NamedAPIResource[Stat]

    # The effort points the Pokémon has in the stat.
    effort: int

    # The base value of the stat.
    base_stat: int

@dataclass
class PokemonSprites(APIType):
    # The default depiction of this Pokémon from the front in battle.
    front_default: str

    # The shiny depiction of this Pokémon from the front in battle.
    front_shiny: str

    # The female depiction of this Pokémon from the front in battle.
    front_female: str

    # The shiny female depiction of this Pokémon from the front in battle.
    front_shiny_female: str

    # The default depiction of this Pokémon from the back in battle.
    back_default: str

    # The shiny depiction of this Pokémon from the back in battle.
    back_shiny: str

    # The female depiction of this Pokémon from the back in battle.
    back_female: str

    # The shiny female depiction of this Pokémon from the back in battle.
    back_shiny_female: str

@dataclass
class LocationAreaEncounter(HasEndpoint):
    """ Pokémon Location Areas are ares where Pokémon can be found. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/pokemon/"

    # The location area the referenced Pokémon can be encountered in.
    location_area: NamedAPIResource[LocationArea]

    # A list of versions and encounters with the referenced Pokémon that might happen.
    version_details: list[VersionEncounterDetail]

@dataclass
class PokemonColor(HasName):
    """ Colors used for sorting Pokémon in a Pokédex. The color listed in the Pokédex is usually the color most apparent or covering each Pokémon's body. No orange category exists; Pokémon that are primarily orange are listed as red or brown. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/pokemon-color/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of the Pokémon species that have this color.
    pokemon_species: list[NamedAPIResource[PokemonSpecies]]

@dataclass
class PokemonForm(HasName):
    """ Some Pokémon may appear in one of multiple, visually different forms. These differences are purely cosmetic. For variations within a Pokémon species, which do differ in more than just visuals, the 'Pokémon' entity is used to represent such a variety. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/pokemon-form/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The order in which forms should be sorted within all forms. Multiple forms may have equal order, in which case they should fall back on sorting by name.
    order: int

    # The order in which forms should be sorted within a species' forms.
    form_order: int

    # True for exactly one form used as the default for each Pokémon.
    is_default: bool

    # Whether or not this form can only happen during battle.
    is_battle_only: bool

    # Whether or not this form requires mega evolution.
    is_mega: bool

    # The name of this form.
    form_name: str

    # The Pokémon that can take on this form.
    pokemon: NamedAPIResource[Pokemon]

    # A list of details showing types this Pokémon form has.
    types: list[PokemonFormType]

    # A set of sprites used to depict this Pokémon form in the game.
    sprites: PokemonFormSprites

    # The version group this Pokémon form was introduced in.
    version_group: NamedAPIResource[VersionGroup]

    # The form specific full name of this Pokémon form, or empty if the form does not have a specific name.
    names: list[Name]

    # The form specific form name of this Pokémon form, or empty if the form does not have a specific name.
    form_names: list[Name]

@dataclass
class PokemonFormSprites(APIType):
    # The default depiction of this Pokémon form from the front in battle.
    front_default: str

    # The shiny depiction of this Pokémon form from the front in battle.
    front_shiny: str

    # The default depiction of this Pokémon form from the back in battle.
    back_default: str

    # The shiny depiction of this Pokémon form from the back in battle.
    back_shiny: str

@dataclass
class PokemonHabitat(HasName):
    """ Habitats are generally different terrain Pokémon can be found in but can also be areas designated for rare or legendary Pokémon. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/pokemon-habitat/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of the Pokémon species that can be found in this habitat.
    pokemon_species: list[NamedAPIResource[PokemonSpecies]]

@dataclass
class PokemonShape(HasName):
    """ Shapes used for sorting Pokémon in a Pokédex. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/pokemon-shape/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The "scientific" name of this Pokémon shape listed in different languages.
    awesome_names: list[AwesomeName]

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of the Pokémon species that have this shape.
    pokemon_species: list[NamedAPIResource[PokemonSpecies]]

@dataclass
class AwesomeName(APIType):
    # The localized "scientific" name for an API resource in a specific language.
    awesome_name: str

    # The language this "scientific" name is in.
    language: NamedAPIResource[Language]

@dataclass
class PokemonSpecies(HasName):
    """ A Pokémon Species forms the basis for at least one Pokémon. Attributes of a Pokémon species are shared across all varieties of Pokémon within the species. A good example is Wormadam; Wormadam is the species which can be found in three different varieties, Wormadam-Trash, Wormadam-Sandy and Wormadam-Plant. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/pokemon-species/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # The order in which species should be sorted. Based on National Dex order, except families are grouped together and sorted by stage.
    order: int

    # The chance of this Pokémon being female, in eighths; or -1 for genderless.
    gender_rate: int

    # The base capture rate; up to 255. The higher the number, the easier the catch.
    capture_rate: int

    # The happiness when caught by a normal Pokéball; up to 255. The higher the number, the happier the Pokémon.
    base_happiness: int

    # Whether or not this is a baby Pokémon.
    is_baby: bool

    # Whether or not this is a legendary Pokémon.
    is_legendary: bool

    # Whether or not this is a mythical Pokémon.
    is_mythical: bool

    # Initial hatch counter: one must walk 255 × steps before this Pokémon's egg hatches, unless utilizing bonuses like Flame Body's.
    hatch_counter: int

    # Whether or not this Pokémon has visual gender differences.
    has_gender_differences: bool

    # Whether or not this Pokémon has multiple forms and can switch between them.
    forms_switchable: bool

    # The rate at which this Pokémon species gains levels.
    growth_rate: NamedAPIResource[GrowthRate]

    # A list of Pokedexes and the indexes reserved within them for this Pokémon species.
    pokedex_numbers: list[PokemonSpeciesDexEntry]

    # A list of egg groups this Pokémon species is a member of.
    egg_groups: list[NamedAPIResource[EggGroup]]

    # The color of this Pokémon for Pokédex search.
    color: NamedAPIResource[PokemonColor]

    # The shape of this Pokémon for Pokédex search.
    shape: NamedAPIResource[PokemonShape]

    # The Pokémon species that evolves into this Pokemon_species.
    evolves_from_species: NamedAPIResource[PokemonSpecies]

    # The evolution chain this Pokémon species is a member of.
    evolution_chain: APIResource[EvolutionChain]

    # The habitat this Pokémon species can be encountered in.
    habitat: NamedAPIResource[PokemonHabitat]

    # The generation this Pokémon species was introduced in.
    generation: NamedAPIResource[Generation]

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of encounters that can be had with this Pokémon species in pal park.
    pal_park_encounters: list[PalParkEncounterArea]

    # A list of flavor text entries for this Pokémon species.
    flavor_text_entries: list[FlavorText]

    # Descriptions of different forms Pokémon take on within the Pokémon species.
    form_descriptions: list[Description]

    # The genus of this Pokémon species listed in multiple languages.
    genera: list[Genus]

    # A list of the Pokémon that exist within this Pokémon species.
    varieties: list[PokemonSpeciesVariety]

@dataclass
class Genus(APIType):
    # The localized genus for the referenced Pokémon species
    genus: str

    # The language this genus is in.
    language: NamedAPIResource[Language]

@dataclass
class PokemonSpeciesDexEntry(APIType):
    # The index number within the Pokédex.
    entry_number: int

    # The Pokédex the referenced Pokémon species can be found in.
    pokedex: NamedAPIResource[Pokedex]

@dataclass
class PalParkEncounterArea(APIType):
    # The base score given to the player when the referenced Pokémon is caught during a pal park run.
    base_score: int

    # The base rate for encountering the referenced Pokémon in this pal park area.
    rate: int

    # The pal park area where this encounter happens.
    area: NamedAPIResource[PalParkArea]

@dataclass
class PokemonSpeciesVariety(APIType):
    # Whether this variety is the default variety.
    is_default: bool

    # The Pokémon variety.
    pokemon: NamedAPIResource[Pokemon]

@dataclass
class Stat(HasName):
    """ Stats determine certain aspects of battles. Each Pokémon has a value for each stat which grows as they gain levels and can be altered momentarily by effects in battles. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/stat/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # ID the games use for this stat.
    game_index: int

    # Whether this stat only exists within a battle.
    is_battle_only: bool

    # A detail of moves which affect this stat positively or negatively.
    affecting_moves: MoveStatAffectSets

    # A detail of natures which affect this stat positively or negatively.
    affecting_natures: NatureStatAffectSets

    # A list of characteristics that are set on a Pokémon when its highest base stat is this stat.
    characteristics: list[APIResource[Characteristic]]

    # The class of damage this stat is directly related to.
    move_damage_class: NamedAPIResource[MoveDamageClass]

    # The name of this resource listed in different languages.
    names: list[Name]

@dataclass
class MoveStatAffectSets(APIType):
    # A list of moves and how they change the referenced stat.
    increase: list[MoveStatAffect]

    # A list of moves and how they change the referenced stat.
    decrease: list[MoveStatAffect]

@dataclass
class MoveStatAffect(APIType):
    # The maximum amount of change to the referenced stat.
    change: int

    # The move causing the change.
    move: NamedAPIResource[Move]

@dataclass
class NatureStatAffectSets(APIType):
    # A list of natures and how they change the referenced stat.
    increase: list[NamedAPIResource[Nature]]

    # A list of nature sand how they change the referenced stat.
    decrease: list[NamedAPIResource[Nature]]

@dataclass
class Type(HasName):
    """ Types are properties for Pokémon and their moves. Each type has three properties: which types of Pokémon it is super effective against, which types of Pokémon it is not very effective against, and which types of Pokémon it is completely ineffective against. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/type/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # A detail of how effective this type is toward others and vice versa.
    damage_relations: TypeRelations

    # A list of details of how effective this type was toward others and vice versa in previous generations
    past_damage_relations: list[TypeRelationsPast]

    # A list of game indices relevent to this item by generation.
    game_indices: list[GenerationGameIndex]

    # The generation this type was introduced in.
    generation: NamedAPIResource[Generation]

    # The class of damage inflicted by this type.
    move_damage_class: NamedAPIResource[MoveDamageClass]

    # The name of this resource listed in different languages.
    names: list[Name]

    # A list of details of Pokémon that have this type.
    pokemon: list[TypePokemon]

    # A list of moves that have this type.
    moves: list[NamedAPIResource[Move]]

@dataclass
class TypePokemon(APIType):
    # The order the Pokémon's types are listed in.
    slot: int

    # The Pokémon that has the referenced type.
    pokemon: NamedAPIResource[Pokemon]

@dataclass
class TypeRelations(APIType):
    # A list of types this type has no effect on.
    no_damage_to: list[NamedAPIResource[Type]]

    # A list of types this type is not very effect against.
    half_damage_to: list[NamedAPIResource[Type]]

    # A list of types this type is very effect against.
    double_damage_to: list[NamedAPIResource[Type]]

    # A list of types that have no effect on this type.
    no_damage_from: list[NamedAPIResource[Type]]

    # A list of types that are not very effective against this type.
    half_damage_from: list[NamedAPIResource[Type]]

    # A list of types that are very effective against this type.
    double_damage_from: list[NamedAPIResource[Type]]

@dataclass
class TypeRelationsPast(APIType):
    # The last generation in which the referenced type had the listed damage relations
    generation: NamedAPIResource[Generation]

    # The damage relations the referenced type had up to and including the listed generation
    damage_relations: TypeRelations


@dataclass
class Language(HasName):
    """ Languages for translations of API resource information. """

    endpoint: ClassVar[str] = "https://pokeapi.co/api/v2/language/"

    # The identifier for this resource.
    id: int

    # The name for this resource.
    name: str

    # Whether or not the games are published in this language.
    official: bool

    # The two-letter code of the country where this language is spoken. Note that it is not unique.
    iso639: str

    # The two-letter code of the language. Note that it is not unique.
    iso3166: str

    # The name of this resource listed in different languages.
    names: list[Name]

#
# Common Models
#

t_API = TypeVar("t_API", bound=APIType)
@dataclass
class APIResource(APIType, Generic[t_API]):
    # The URL of the referenced resource.
    url: str

@dataclass
class Description(APIType):
    # The localized description for an API resource in a specific language.
    description: str

    # The language this name is in.
    language: NamedAPIResource[Language]

@dataclass
class Effect(APIType):
    # The localized effect text for an API resource in a specific language.
    effect: str

    # The language this effect is in.
    language: NamedAPIResource[Language]

@dataclass
class Encounter(APIType):
    # The lowest level the Pokémon could be encountered at.
    min_level: int

    # The highest level the Pokémon could be encountered at.
    max_level: int

    # A list of condition values that must be in effect for this encounter to occur.
    condition_values: list[NamedAPIResource[EncounterConditionValue]]

    # Percent chance that this encounter will occur.
    chance: int

    # The method by which this encounter happens.
    method: NamedAPIResource[EncounterMethod]

@dataclass
class FlavorText(APIType):
    # The localized flavor text for an API resource in a specific language. Note that this text is left unprocessed as it is found in game files. This means that it contains special characters that one might want to replace with their visible decodable version. Please check out this issue to find out more.
    flavor_text: str

    # The language this name is in.
    language: NamedAPIResource[Language]

    # The game version this flavor text is extracted from.
    version: NamedAPIResource[Version]

@dataclass
class GenerationGameIndex(APIType):
    # The internal id of an API resource within game data.
    game_index: int

    # The generation relevent to this game index.
    generation: NamedAPIResource[Generation]

@dataclass
class MachineVersionDetail(APIType):
    # The machine that teaches a move from an item.
    machine: APIResource[Machine]

    # The version group of this specific machine.
    version_group: NamedAPIResource[VersionGroup]

@dataclass
class Name(APIType):
    # The localized name for an API resource in a specific language.
    name: str

    # The language this name is in.
    language: NamedAPIResource[Language]

@dataclass
class NamedAPIResource(APIResource[t_API]):
    # The name of the referenced resource.
    name: str

    # The URL of the referenced resource.
    url: str

@dataclass
class VerboseEffect(APIType):
    # The localized effect text for an API resource in a specific language.
    effect: str

    # The localized effect text in brief.
    short_effect: str

    # The language this effect is in.
    language: NamedAPIResource[Language]

@dataclass
class VersionEncounterDetail(APIType):
    # The game version this encounter happens in.
    version: NamedAPIResource[Version]

    # The total percentage of all encounter potential.
    max_chance: int

    # A list of encounters and their specifics.
    encounter_details: list[Encounter]

@dataclass
class VersionGameIndex(APIType):
    # The internal id of an API resource within game data.
    game_index: int

    # The version relevent to this game index.
    version: NamedAPIResource[Version]

@dataclass
class VersionGroupFlavorText(APIType):
    # The localized name for an API resource in a specific language.
    text: str

    # The language this name is in.
    language: NamedAPIResource[Language]

    # The version group which uses this flavor text.
    version_group: NamedAPIResource[VersionGroup]
 
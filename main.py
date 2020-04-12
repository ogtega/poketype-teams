import pandas as pd
from typing import List, Set, Tuple, Dict

# Use pandas to create a dataframe of the pokemon type matchups
table = pd.read_csv(
    'https://raw.githubusercontent.com' +
    '/robinsones/pokemon-chart/master/chart.csv',
    index_col=0
)


# Return a floating-point number representing the effectiveness of a type
# combo to any one type
def getMatchup(t: Tuple[str], o: str) -> float:
    return (table.loc[o, t[0]] if len(t) == 1
            else table.loc[o, t[0]] * table.loc[o, t[1]])


types: List[str] = table.index.values[1:]

impossible: Set[Tuple[str]] = set([
    ('Fire', 'Grass'), ('Fairy', 'Fire'), ('Electric', 'Fighting'),
    ('Ice', 'Poison'), ('Fighting', 'Ground'), ('Fairy', 'Fighting'),
    ('Poison', 'Psychic'), ('Poison', 'Steel'), ('Fairy', 'Ground'),
    ('Bug', 'Dragon'), ('Bug', 'Dark'), ('Ghost', 'Rock'),
])

legends:  Set[Tuple[str]] = set([
    ('Fire', 'Water'), ('Fire', 'Steel'), ('Dragon', 'Ice'),
    ('Fighting', 'Rock'), ('Fighting', 'Ghost'), ('Ghost', 'Psychic'),
    ('Dragon', 'Psychic')
])

tcombos: Set[Tuple[str]] = set()

# Create every unique combination of any one or two types
for t in types:
    for tt in types:
        # If the types are different create a sorted tuple of the types
        if t is not tt:
            tcombos.add(tuple(sorted([t, tt])))
        else:
            tcombos.add(tuple([t]))

tcombos = ((tcombos - impossible) - legends)

# A dictionary with weights as the key for easy iteration
weakness: Dict[Tuple[str], Set[str]] = {}
resistance: Dict[Tuple[str], Set[str]] = {}

# Find all weak and resistant type match ups for each type combo
for c in tcombos:
    weak: Set[str] = set()
    resist: Set[str] = set()

    for t in types:
        # The type combo is resistant to this type
        if getMatchup(c, t) <= 0.5:
            resist.add(t)
        # The type combo is weak to this type
        if getMatchup(c, t) >= 2:
            weak.add(t)

    weakness[c] = weak.difference(resist)
    resistance[c] = resist


def buildTeam(
        team: List[Tuple[str]] = [],
        combos: Set[Tuple[str]] = tcombos,
        weak: Set[str] = set()
) -> List[List[Tuple[str]]]:
    teams = list()
    comboList = list(combos)

    if len(team) == 6:
        return [team]
    else:
        for i in range(len(comboList)):
            c = comboList[i]

            if len(weakness[c] & weak) == 0:
                rem = set(comboList[i+1:])
                teams = teams + buildTeam(team + [c], rem, weak | weakness[c])
    return teams


def weight(tm):
    res = set()
    weak = set()

    for t in tm:
        res = resistance[t] | res
        weak = weakness[t] | weak
    weak = weak - res
    return len(res) / len(weak | res)


for team in sorted(buildTeam(), key=weight, reverse=True):
    w = weight(team)
    if w >= 1:
        print(f'{w:.2f}: {team}')

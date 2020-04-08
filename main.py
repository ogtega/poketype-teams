import pandas as pd
from functools import reduce
from typing import List, Set, Tuple, Dict

# Use pandas to create a dataframe of the pokemon type matchups
table = pd.read_csv(
    'https://raw.githubusercontent.com/robinsones/pokemon-chart/master/chart.csv',
    index_col=0
)

# Return a floating-point number representing the effectiveness of a type combo to any one type
def getMatchup(t: Tuple[str], o: str) -> float:
    return (table.loc[o, t[0]] if len(t) is 1 else table.loc[o, t[0]] * table.loc[o, t[1]])

types: List[str] = table.index.values[1:]

impossible: Set[Tuple[str]] = set([
    ('Fire', 'Steel'), ('Fairy', 'Fire'), ('Electric', 'Fighting'),
    ('Ice', 'Poison'), ('Fighting', 'Ground'), ('Fairy', 'Fighting'),
    ('Poison', 'Psychic'), ('Poison', 'Steel'), ('Fairy', 'Ground'),
    ('Bug', 'Dragon'), ('Bug', 'Dark'), ('Ghost', 'Rock')
])

legends:  Set[Tuple[str]] = set([
    ('Fire', 'Water'), ('Fire, Steel'), ('Dragon', 'Ice'), ('Fighting', 'Rock'),
    ('Fighting', 'Ghost'), ('Ghost', 'Psychic'), ('Dragon', 'Psychic'), ('Dragon', 'Fairy')
])

tcombos: Set[Tuple[str]] = set()
# Create every unique combination of any one or two types
for t in types:
    for tt in types:
        # If the types are different create a tuple of the types sorted alphabetically
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

def buildTeam(team: List[Tuple[str]] = [], combos: Set[Tuple[str]] = tcombos, weak: Set[str] = set(), n: int = 0):
    teams = list()
    comboList = list(combos)

    for i in range(len(comboList)):
        c = comboList[i]

        if len(weakness[c] & weak) is 0:
            if n is 5:
                teams.append(team + [c])
            else:
                for p in buildTeam(team + [c], set(comboList[i+1:]), weak | weakness[c], n + 1):
                    teams = teams + [p]
    return teams


for team in buildTeam():
    print(team)

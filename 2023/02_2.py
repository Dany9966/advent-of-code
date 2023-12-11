import re

test_string = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

LIMITS = {"red": 12, "green": 13, "blue": 14}


def get_game_power(game):

    def _get_max_cubes(color):
        pattern = r'([0-9]+) %s' % color
        cubes = re.findall(pattern, extractions)
        print("Found %s cubes: %s" % (color, cubes))
        return max([int(c) for c in cubes])

    game_num, extractions = re.split(':', game)
    m = re.match(r'Game ([0-9]+)', game_num)
    if m:
        return (_get_max_cubes('red') *
                _get_max_cubes('blue') *
                _get_max_cubes('green'))
    return 0


if __name__ == '__main__':
    with open('input/02.txt') as f:
        powers = [get_game_power(g) for g in f.read().splitlines()]
        print(sum(powers))

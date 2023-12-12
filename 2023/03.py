import re

test_string = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def find_symbols(line):
    line_symbol_idxs = []
    for m in re.finditer(r'[^0-9.]', line):
        line_symbol_idxs.append(m.start())
    return line_symbol_idxs


def find_nums(line_idx, line):
    line_num_idxs = {line_idx: []}
    for m in re.finditer(r'[0-9]+', line):
        idx_tuple = (line_idx, m.start(), m.end())
        line_num_idxs[line_idx].append((m.start(), m.end(), int(m.group(0))))
    return line_num_idxs


def find_part_numbers(puzzle_input):
    part_numbers = []
    SYMBOL_INDEXES = []
    NUM_INDEXES = dict()
    for line_idx, line in enumerate(puzzle_input.splitlines()):
        for sym_idx in find_symbols(line):
            SYMBOL_INDEXES.append((line_idx, sym_idx))
        NUM_INDEXES.update(find_nums(line_idx, line))
    # print(SYMBOL_INDEXES)
    # print(NUM_INDEXES)

    for symbol_line, symbol_idx in SYMBOL_INDEXES:
        valid_idxs = {symbol_idx - 1, symbol_idx, symbol_idx + 1}
        for line_idx in [symbol_line - 1, symbol_line, symbol_line + 1]:
            for num in NUM_INDEXES.get(line_idx, []):
                start, end, value = num
                num_idxs = set([i for i in range(start, end)])
                if valid_idxs.intersection(num_idxs):
                    part_numbers.append(value)
                    # NUM_INDEXES[line_idx].remove(num)
    return part_numbers


def find_star_symbols(line):
    line_star_idxs = []
    for m in re.finditer(r'[*]', line):
        line_star_idxs.append(m.start())
    return line_star_idxs


def find_gear_ratios(puzzle_input):
    gear_ratios = []
    SYMBOL_INDEXES = []
    NUM_INDEXES = dict()
    for line_idx, line in enumerate(puzzle_input.splitlines()):
        for sym_idx in find_star_symbols(line):
            SYMBOL_INDEXES.append((line_idx, sym_idx))
        NUM_INDEXES.update(find_nums(line_idx, line))

    for symbol_line, symbol_idx in SYMBOL_INDEXES:
        gear_part_numbers = []
        valid_idxs = {symbol_idx - 1, symbol_idx, symbol_idx + 1}
        for line_idx in [symbol_line - 1, symbol_line, symbol_line + 1]:
            for num in NUM_INDEXES.get(line_idx, []):
                start, end, value = num
                num_idxs = set([i for i in range(start, end)])
                if valid_idxs.intersection(num_idxs):
                    gear_part_numbers.append(value)

        if len(gear_part_numbers) == 2:
            gear_ratios.append(gear_part_numbers[0] * gear_part_numbers[1])
    return gear_ratios


if __name__ == '__main__':
    with open('input/03.txt') as f:
        # Part I
        # found_part_numbers = find_part_numbers(f.read())
        # print(sum(found_part_numbers))

        # Part II
        print(sum(find_gear_ratios(f.read())))

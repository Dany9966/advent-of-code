import re

test_string = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def parse_almanac(almanac_input):
    almanac_data = {
        "seeds": [],
        "seed_to_soil": [],
        "soil_to_fertilizer": [],
        "fertilizer_to_water": [],
        "water_to_light": [],
        "light_to_temperature": [],
        "temperature_to_humidity": [],
        "humidity_to_location": [],
    }

    list_to_parse = None
    for line in almanac_input.splitlines():
        if line:
            if line.startswith('seeds:'):
                almanac_data['seeds'] = [
                    int(n) for n in line.split(':')[1].strip().split(' ')]
                continue
            if line.startswith('seed-to-soil map:'):
                list_to_parse = almanac_data['seed_to_soil']
                continue
            if line.startswith('soil-to-fertilizer map:'):
                list_to_parse = almanac_data['soil_to_fertilizer']
                continue
            if line.startswith('fertilizer-to-water map:'):
                list_to_parse = almanac_data['fertilizer_to_water']
                continue
            if line.startswith('water-to-light map:'):
                list_to_parse = almanac_data['water_to_light']
                continue
            if line.startswith('light-to-temperature map:'):
                list_to_parse = almanac_data['light_to_temperature']
                continue
            if line.startswith('temperature-to-humidity map:'):
                list_to_parse = almanac_data['temperature_to_humidity']
                continue
            if line.startswith('humidity-to-location map:'):
                list_to_parse = almanac_data['humidity_to_location']
                continue
            if list_to_parse is not None:
                list_to_parse.append([int(n) for n in line.strip().split(' ')])

    return almanac_data


def get_seeds_location(almanac_data):
    seed_to_location = {}
    mapping_steps = [
        'seed_to_soil', 'soil_to_fertilizer', 'fertilizer_to_water',
        'water_to_light', 'light_to_temperature', 'temperature_to_humidity',
        'humidity_to_location']

    def _step(map_name, source):
        tmp = None
        for m in almanac_data[map_name]:
            dest_start, source_start, length = m
            if source_start <= source <= (source_start + length):
                tmp = dest_start + (source - source_start)
                break
        if tmp is None:
            tmp = source
        return tmp

    for n in range(0, (len(almanac_data['seeds']) // 2)):
        start_seed = almanac_data['seeds'][n * 2]
        length = almanac_data['seeds'][n * 2 + 1]
        for seed in (range(start_seed, start_seed + length)):
            step_result = seed
            for step in mapping_steps:
                step_result = _step(step, step_result)
            seed_to_location[seed] = step_result
    return seed_to_location


def get_min_seed(almanac_data):
    seeds = almanac_data.pop('seeds', [])
    location_ranges = []

    def _step(source_ranges, map_name):
        steps_ranges = []
        for source in source_ranges:
            source_start, source_end = source
            source_start_overlap_range = None
            source_end_overlap_range = None
            for mapping in almanac_data[map_name]:
                ms_start, length = mapping[1:3]
                # md_end = md_start = length
                ms_end = ms_start + length
                ms_range = range(ms_start, ms_end)
                if not source_start_overlap_range and source_start in ms_range:
                    source_start_overlap_range = mapping
                if not source_end_overlap_range and source_end in ms_range:
                    source_end_overlap_range = mapping

            if not any([source_start_overlap_range, source_end_overlap_range]):
                steps_ranges.append((source_start, source_end))
            elif all([source_start_overlap_range, source_end_overlap_range]):
                md_start1, ms_start1, length1 = source_start_overlap_range
                md_start2, ms_start2, length2 = source_end_overlap_range
                steps_ranges.append(
                    (md_start1 + (source_start - ms_start1),
                     md_start2 + (source_end - ms_start2)))
            elif source_start_overlap_range:
                md_start, ms_start, length = source_start_overlap_range
                ms_end = ms_start + length
                md_end = md_start + length
                steps_ranges.extend([
                    (md_start + (source_start - ms_start), md_end),
                    (ms_end + 1, source_end)])
            elif source_end_overlap_range:
                md_start, ms_start, length = source_end_overlap_range
                steps_ranges.extend([
                    (source_start, ms_start - 1),
                    (md_start, md_start + (source_end - ms_start))])

        return steps_ranges

    for i in range(0, len(seeds), 2):
        seed_start = seeds[i]
        seed_end = seed_start + seeds[i + 1]
        seed_ranges = [(seed_start, seed_end)]
        for mapping_name in almanac_data.keys():
            seed_ranges = _step(seed_ranges, mapping_name)
        location_ranges.extend(seed_ranges)
    if location_ranges:
        location_ranges.sort()
        return location_ranges[0][0]


if __name__ == '__main__':
    # with open('input/05.txt') as f:
    #     almanac = parse_almanac(f.read())
    almanac = parse_almanac(test_string)
    print(get_min_seed(almanac))

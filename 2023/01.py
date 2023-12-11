DIGIT_NUMS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9}


def calibrate_line(line):
    first_digit = None
    last_digit = None

    i = 0
    j = len(line)
    while not all([first_digit, last_digit]):
        if not first_digit:
            try:
                first_digit = int(line[i])
            except ValueError:
                s1 = {line[i:i+3], line[i:i+4], line[i:i+5]}
                s_int = s1.intersection(set(DIGIT_NUMS.keys()))
                if s_int:
                    first_digit = DIGIT_NUMS[list(s_int)[0]]
                    print("First digit of line '%s' is %d" %
                          (line, first_digit))
                else:
                    i += 1

        if not last_digit:
            try:
                last_digit = int(line[j-1])
            except ValueError:
                s1 = {line[j-3:j], line[j-4:j], line[j-5:j]}
                s_int = s1.intersection(set(DIGIT_NUMS.keys()))
                if s_int:
                    last_digit = DIGIT_NUMS[list(s_int)[0]]
                    print("Last digit of line '%s' is %d" %
                          (line, last_digit))
                else:
                    j -= 1

    return first_digit * 10 + last_digit


def calibrate(test_lines):
    lines = test_lines.splitlines()
    return sum([calibrate_line(line) for line in lines if line])


if __name__ == '__main__':
    with open('input/01_1.txt') as f:
        print(calibrate(f.read()))

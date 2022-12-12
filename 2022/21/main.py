import re

from tools import parse_lines, print_part

MONKEY_JOB_PATTERN = r"(\w+): (.*)"
JOB_PATTERN = r"(\w+) ([\+\/\-\*]) (\w+)"


def str2digit(string: str) -> int | str:
    return int(string) if string.isdigit() else string


@print_part
def solve(filepath: str, part: int = 1):
    # fmt: off
    monkeys_and_jobs = {
        re.match(MONKEY_JOB_PATTERN, line).group(1):
            re.match(MONKEY_JOB_PATTERN, line).group(2)
        for line in parse_lines(filepath)
    }
    monkeys_with_numbers = {monkey: job for monkey, job in monkeys_and_jobs.items() if job.isdigit()}
    monkeys_without_numbers = {monkey: job for monkey, job in monkeys_and_jobs.items() if not job.isdigit()}
    # fmt: on

    if part == 1:
        while "root" in monkeys_without_numbers.keys():
            for nice_monkey, number in monkeys_with_numbers.copy().items():
                for monkey, job in monkeys_without_numbers.copy().items():
                    if nice_monkey in job:
                        job = job.replace(nice_monkey, number)
                        try:
                            monkeys_with_numbers[monkey] = str(int(eval(job)))
                            del monkeys_without_numbers[monkey]
                        except NameError:
                            monkeys_without_numbers[monkey] = job

        print(monkeys_with_numbers["root"])

    if part == 2:
        root_job = monkeys_without_numbers["root"]
        operand1, operator, operand2 = re.match(JOB_PATTERN, root_job).groups()

    #     for monkey, job in monkeys_without_numbers.items():


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)

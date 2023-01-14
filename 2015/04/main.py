from hashlib import md5

from tools import print_ans, print_part


@print_part
def solve(part: int = 1):
    key_alp = "iwrupvqb"
    key_num = 60_000 if part == 1 else 9_000_000
    num_zeroes = 5 if part == 1 else 6
    while True:
        key = key_alp + str(key_num)
        hash_str = md5(key.encode("utf-8")).hexdigest()[:num_zeroes]
        if hash_str == "0" * num_zeroes:
            print_ans(key_num)
            break
        key_num += 1


if __name__ == "__main__":
    solve(part=1)
    solve(part=2)

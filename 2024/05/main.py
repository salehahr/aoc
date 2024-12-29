from typing import Collection, Sequence

from tools import get_numbers, parse_lines, print_ans, print_part

Update = Sequence[int]
Rule = tuple[int, int]


def rule_ok(update_: Update, rule_: Rule, is_ok: bool) -> bool:
    p1_, p2_ = rule_
    if is_ok:
        return update_.index(p1_) < update_.index(p2_)
    else:
        return update_.index(p1_) > update_.index(p2_)


def applicable_rules(update_: Update, rules_: Collection[Rule]) -> tuple[Rule, ...]:
    return tuple(filter(lambda r: set(r).issubset(set(update_)), rules_))


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath)
    sep_idx = lines.index("")
    rules = tuple(map(get_numbers, lines[:sep_idx]))
    updates = tuple(map(get_numbers, lines[sep_idx + 1 :]))

    def rules_ok(update_: Update, is_ok: bool) -> bool:
        if is_ok:
            return all(
                map(
                    lambda r: rule_ok(update_, r, is_ok),
                    applicable_rules(update_, rules),
                )
            )
        else:
            return any(
                map(
                    lambda r: rule_ok(update_, r, is_ok),
                    applicable_rules(update_, rules),
                )
            )

    if part == 1:
        ans = sum(
            u[len(u) // 2] for u in filter(lambda u: rules_ok(u, is_ok=True), updates)
        )
        print_ans(ans, correct_ans=4689)
        return

    ans = 0
    for update in filter(lambda u: rules_ok(u, is_ok=False), updates):
        rules_for_update = applicable_rules(update, rules)
        for nok_rule in filter(
            lambda r: rule_ok(update, r, is_ok=False), rules_for_update
        ):
            _, p1 = nok_rule
            orig_pos = tuple(update.index(p) for p in nok_rule)
            nums_after_p0 = update[orig_pos[0] + 1 :]
            if rules_after_p0 := [
                r
                for r in applicable_rules([p1, *nums_after_p0], rules_for_update)
                if p1 == r[1]
            ]:
                new_pos_p1 = max(update.index(n) for n, _ in rules_after_p0)
            else:
                new_pos_p1 = orig_pos[0]

            update.pop(orig_pos[1])
            update.insert(new_pos_p1, p1)

        assert rules_ok(update, is_ok=True)
        ans += update[len(update) // 2]

    print_ans(ans, correct_ans=6336)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)

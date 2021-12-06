from collections import defaultdict
import copy


def parse_input():
    # Parse file input
    fish_timers = defaultdict(int)

    with open("input/6.txt") as f:
        raw_fish_timers = [int(timer) for timer in f.readlines()[0].split(",")]

        for timer in raw_fish_timers:
            fish_timers[timer] += 1

    return fish_timers


def solve(fish_timers, days):
    for day in range(days):
        # Save the number of reproducing fish.
        reproducing_fish = fish_timers[0]

        # Decrement the timer on all fish/
        for time_to_live in range(8):
            fish_timers[time_to_live] = fish_timers[time_to_live + 1]

        # Update reproducing fish.
        fish_timers[6] += reproducing_fish
        fish_timers[8] = reproducing_fish

    return fish_timers


def solve_part_one(fish_timers):
    final_fish_timers = solve(fish_timers, days=80)
    answer = sum(final_fish_timers.values())
    print(f"Part one: {answer} lanternfish")
    assert 390011 == answer


def solve_part_two(fish_timers):
    final_fish_timers = actual_old_solve(fish_timers, days=256)
    answer = sum(final_fish_timers.values())
    print(f"Part two: {answer} lanternfish")
    assert 1746710169834 == answer


def main():
    fish_timers = parse_input()
    solve_part_one(copy.deepcopy(fish_timers))
    solve_part_two(copy.deepcopy(fish_timers))


main()

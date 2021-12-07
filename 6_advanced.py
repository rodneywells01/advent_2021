# https://www.reddit.com/r/adventofcode/comments/ra3f5i/2021_day_6_part_3_day_googol/

from collections import defaultdict
import copy

import time



correct_first_8_days = {0: 300, 1: 505, 2: 533, 3: 552, 4: 575, 5: 600, 6: 600, 7: 600}



def parse_input():
    # Parse file input
    fish_timers = defaultdict(int)

    with open("input/6.txt") as f:
        raw_fish_timers = [int(timer) for timer in f.readlines()[0].split(",")]

        for timer in raw_fish_timers:
            fish_timers[timer] += 1

    return fish_timers



def display_ordered_dict(my_dict): 
    ordered_keys = list(my_dict.keys())
    ordered_keys.sort()
    formatted_output = "{"
    for key in ordered_keys: 
        formatted_output += f"{key}: {my_dict[key]}, "
    formatted_output += "}"
    print(formatted_output)


def solve(fish_timers, days):
    reproducing_idx = 0 
    for day in range(days):
        # print(f"Day {day} | {day * 1.0/days}%")

        reproducing_fish = fish_timers[reproducing_idx]
        # print(f"{reproducing_fish} fish reproducing!")
        # fish_timers[reproducing_idx] += reproducing_fish
        fish_timers[(reproducing_idx + 7) % 9] += reproducing_fish

        # Increment reproducing idx 
        reproducing_idx += 1
        reproducing_idx = reproducing_idx % 9

        # display_ordered_dict(fish_timers)

        # if sum(fish_timers.values()) != correct_first_8_days[day]: 
        #     raise Exception(f"Incorrect fish count on day {day}. Received {sum(fish_timers.values())}, Expected {correct_first_8_days[day]}")
        # else: 
        #     print(f"Day {day} is CORRECT")


    return fish_timers



def solve_old(fish_timers, days):
    fish_log = dict()
    for day in range(days):
        # Save the number of reproducing fish.
        # print(f"Day {day} | {day * 1.0/days}%")
        reproducing_fish = fish_timers[0]

        # Decrement the timer on all fish/
        for time_to_live in range(8):
            fish_timers[time_to_live] = fish_timers[time_to_live + 1]

        # Update reproducing fish.
        fish_timers[6] += reproducing_fish
        fish_timers[8] = reproducing_fish

        
        # display_ordered_dict(fish_timers)

        fish_log[day] = sum(fish_timers.values())

    return fish_timers


def solve_quickie_old(fish_timers):
    final_fish_timers = solve_old(fish_timers, days=8)
    answer = sum(final_fish_timers.values())
    print(f"Quickie: {answer} lanternfish")

def solve_quickie_new(fish_timers):
    final_fish_timers = solve(fish_timers, days=80)
    answer = sum(final_fish_timers.values())
    print(f"Quickie: {answer} lanternfish")
    assert 390011 == answer


def solve_part_one(fish_timers):
    final_fish_timers = solve(fish_timers, days=80)
    answer = sum(final_fish_timers.values())
    print(f"Part one: {answer} lanternfish")
    assert 390011 == answer


def solve_part_two(fish_timers):
    final_fish_timers = solve(fish_timers, days=256)
    answer = sum(final_fish_timers.values())
    print(f"Part two: {answer} lanternfish")
    assert 1746710169834 == answer

def solve_part_three(fish_timers):
    print("Solving Part three")
    final_fish_timers = solve(fish_timers, days=pow(10,100))
    answer = sum(final_fish_timers.values())
    print(f"Part three: {answer} lanternfish")


def performance_testing(fish_timers, days=1000): 

    print(f"Computing {'{:,}'.format(days)} days")
    print("Old method")
    tic = time.perf_counter()
    final_fish_timers = solve_old(fish_timers, days=days)
    answer = sum(final_fish_timers.values())
    toc = time.perf_counter()
    print(f"Finished old method in {toc - tic:0.4f} seconds")


    print(f"New method")
    tic = time.perf_counter()
    final_fish_timers = solve(fish_timers, days=days)
    answer = sum(final_fish_timers.values())
    toc = time.perf_counter()
    print(f"Finished new method in {toc - tic:0.4f} seconds")



def main():
    fish_timers = parse_input()
    # solve_quickie_old(copy.deepcopy(fish_timers))
    # solve_quickie_new(copy.deepcopy(fish_timers))
    # solve_part_one(copy.deepcopy(fish_timers))
    # solve_part_two(copy.deepcopy(fish_timers))
    performance_testing(copy.deepcopy(fish_timers), days=2000000)


main()

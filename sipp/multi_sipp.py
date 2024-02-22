"""

Extension of SIPP to multi-robot scenarios

author: Ashwin Bose (@atb033)

See the article: 10.1109/ICRA.2011.5980306

"""

import argparse
import yaml
from math import fabs, log2, ceil, floor
from graph_generation import SippGraph, State
from sipp import SippPlanner
import random
import threading

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help="input file containing map and dynamic obstacles")
    parser.add_argument("output", help="output file with the schedule")
    
    args = parser.parse_args()
    
    # Read Map
    with open(args.map, 'r') as map_file:
        try:
            map = yaml.load(map_file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)

    # Output file
    output = dict()
    output["schedule"] = dict()

    # take log n permutations to get a good mix
    permutation_count = floor(log2(len(map["agents"])))
    # print(permutation_count)
    # get permutations of agents
    permutations = []
    perm_counter = permutation_count
    while perm_counter != 0:
        new_perm = list(range(len(map["agents"])))
        random.shuffle(new_perm)
        if new_perm in permutations:
            continue
        permutations.append(new_perm)
        perm_counter -= 1

    # print(list(range(len(map["agents"]))))
    has_collisions = False
    cost = 0
    
    # do the first one and if it doesn't have collisions, stop
    for i in range(len(map["agents"])):
        sipp_planner = SippPlanner(map,i)
    
        if sipp_planner.compute_plan():
            plan, has_collision = sipp_planner.get_plan()
            has_collisions = has_collisions or has_collision
            output["schedule"].update(plan)
            map["dynamic_obstacles"].update(plan)
            cost += len(list(plan.values())[0])

            with open(args.output, 'w') as output_yaml:
                yaml.safe_dump(output, output_yaml)  
        else: 
            print("Plan not found")
    
    
    # if it has no collisions, return, we are done
    if not has_collisions: 
        print(f"Plan found with cost of {cost}")
        return

    # for each permutation type, redo 
    print("Collision detected, multithreading search")
    
    def compute_cost_thread(perm):
        # Read Map
        with open(args.map, 'r') as map_file:
            try:
                _map = yaml.load(map_file, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                print(exc)

        # Output file
        output = dict()
        output["schedule"] = dict()
        # calculate
        thread_cost = 0
        for i in perm:
            sipp_planner = SippPlanner(_map,i)
        
            if sipp_planner.compute_plan():
                plan, _ = sipp_planner.get_plan()
                output["schedule"].update(plan)
                map["dynamic_obstacles"].update(plan)
                thread_cost += len(list(plan.values())[0])
            else: 
                print("Plan not found")
        
        return thread_cost
    
    costs = {}
    threads = []
    for perm in permutations:
        t = threading.Thread(target=lambda p: costs.update({tuple(p):compute_cost_thread(p)}), args=(perm,))
        threads.append(t)
        t.start()
    # finish running threads
    for t in threads:
        t.join()
    print(costs)
    
    print(f"Plan found with cost of {min(list(costs.values()))}")

if __name__ == "__main__":
    main()

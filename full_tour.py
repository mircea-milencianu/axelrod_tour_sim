"""
TOUR_TYPE: string
    Custom name for the tournament. e.g: simple_all_strategies;
    Defines the folder in all results will be placed.
RUN_SCOPE: string
    Defines the scope of run. ex: dev, first strategy set, second strategy set, all strategies;
    Used to prefix for the result files.
SINGLE_RUN: bool
    Defines the type of run. 
        True:   single run;
        False:  multiple runs with a constant DEVIATION that changes by a fixed step; REQUIRES STEP TO BE DEFINED!
STEP: int
    Value for which the DEVIATION decreases.
    The desired behaviour is to start with a large deviation and get close to 0, meaning a default tournament.
DISTRIBUTION: string
    The type of distribution from where the number of turns are extracted.
        normal:     normal distribution
        uniform:    uniform distribution
TURNS: int
    Number of turns in a supergame. A single turn round is a simple game.
REPETITIONS: int
    The number of repetitions of a supergame.
"""
from random import uniform
import axelrod as axl
from rich import print
import json

from timeit import default_timer as timer

from axelrod import tournament
from axelrod import result_set


strategy_groups = {
    "dev": [axl.Cooperator(), axl.Defector(), axl.TitForTat()],
    "first": [s() for s in axl.axelrod_first_strategies],
    "second": [
        s() for s in axl.axelrod_second_strategies
    ],  # IN CASE OF ERROR: check the init file for this set of strategies; custom created;
    "all": [s() for s in axl.all_strategies],
}

with open("tournament_cfg.json") as json_file:
    cfg = json.load(json_file)

print(cfg)
TOUR_NAME = cfg["name"]  # should be a choice
RUN_SCOPE = cfg["scope"]
PLAYERS = strategy_groups[cfg["strategy_set"]]
SINGLE_RUN = cfg["single_run"]
DEVIATION = cfg["deviation"]
STEP = cfg["step"]
DISTRIBUTION = cfg["distribution"]  # "uniform"
TURNS = cfg["turns"]
REPETITIONS = cfg["repetitions"]
PROCESSES = cfg["processes"]


def play_step_tournaments(players):
    local_deviation = DEVIATION

    while local_deviation >= 1:
        play_tournament(
            players, f"{TOUR_NAME}_with_step_{STEP}_value_{local_deviation}"
        )
        local_deviation = local_deviation - STEP


def play_tournament(players, tour_type):
    ### Tournament setup
    filename = ""
    if DISTRIBUTION == "uniform":
        tournament = axl.Tournament(
            players,
            turns=TURNS,
            uniform=True,
            deviation=DEVIATION,
            repetitions=REPETITIONS,
        )
        filename = "uniform_distribution_tournament"

    elif DISTRIBUTION == "normal":
        tournament = axl.Tournament(
            players,
            turns=TURNS,
            normal=True,
            deviation=DEVIATION,
            repetitions=REPETITIONS,
        )
        filename = "normal_distribution_tournament"
    else:
        tournament = axl.Tournament(players, turns=TURNS, repetitions=REPETITIONS)
        filename = "default_tournament"

    ### Play tournament
    result_set_mc = tournament.play(
        filename="{}.csv".format(filename), processes=PROCESSES
    )  #
    matrix_mc = axl.ResultMatrix(
        filename="{}.csv".format(filename),
        players=players,
        repetitions=REPETITIONS,
        tour_type=tour_type,  #'montecarlo'
        run_scope=RUN_SCOPE,
    )
    # winner_matrix = matrix_mc.create()


def main():
    start = timer()
    if SINGLE_RUN is True:
        play_tournament(PLAYERS, TOUR_NAME)
    else:
        play_step_tournaments(PLAYERS)
    end = timer()

    run_summary = {
        "run_time": end - start,
        "processes": PROCESSES,
        "run_scope": RUN_SCOPE,
        "tournament_name": TOUR_NAME,
        "single_run": SINGLE_RUN,
        "distribution": DISTRIBUTION,
        "turns": TURNS,
        "repetitions": REPETITIONS,
        "deviation": DEVIATION,
        "step": STEP,
        ## Add category for tour run results
    }
    with open("results_{}/run_summary.json".format(TOUR_NAME), "w") as fp:
        json.dump(run_summary, fp)


if __name__ == "__main__":
    main()

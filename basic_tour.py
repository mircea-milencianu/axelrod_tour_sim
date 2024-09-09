import axelrod as axl
from rich import print

from timeit import default_timer as timer

from axelrod import tournament
from axelrod import result_set

TURNS = 200
REPETITIONS = 100
RUN_TYPE = "dev"

player_set = {
    "dev_tour": [axl.Cooperator(), axl.Defector(), axl.TitForTat()],
    "first_tour": [s() for s in axl.axelrod_first_strategies],
    "second_tour": [
        s() for s in axl.axelrod_second_strategies
    ],  # this is created by me and can be found in the init file for the axl library; in case of error
    "all": [s() for s in axl.all_strategies],
}

def step_run(players, deviation):

    tournament_mc = axl.Tournament(
        players, turns=TURNS, uniform=True, deviation=deviation, repetitions=REPETITIONS
    )
    result_set_mc = tournament_mc.play(filename="tournament_mc.csv", processes=4)  #
    end = timer()
    matrix_mc = axl.ResultMatrix(
        filename="tournament_mc.csv",
        players=players,
        repetitions=REPETITIONS,
        # deviation=deviation,
        tour_type='montecarlo',
        run_type=RUN_TYPE
    )
    winner_matrix = matrix_mc.create()

def main():
    ### INIT ###
    # players = player_set["first_tour"] + player_set["second_tour"]
    players = player_set["dev_tour"]

    ### run basic tour with no dev
    tournament_default = axl.Tournament(players, turns=TURNS, repetitions=REPETITIONS)
    result_set_default = tournament_default.play(
        filename="tournament_default.csv", processes=4
    )  
    matrix_default = axl.ResultMatrix(
        filename="tournament_default.csv",
        players=players,
        repetitions=REPETITIONS,
        tour_type='default',

        # deviation=None,
        run_type=RUN_TYPE
    )
    winner_matrix = matrix_default.create()
    ### run basic tour with no dev ###############################

    deviation = 100
    step = 5
    while deviation >= 80:
        step_run(players, deviation)
        deviation = deviation - step
    

if __name__ == "__main__":
    main()

from .action_names import *

WEIGHTED_RPSLS = {
    (ROCK, ROCK): (0, 0),
    (ROCK, PAPER): (-1, 1),
    (ROCK, SCISSORS): (2, -2),
    (ROCK, LIZARD): (3, -3),
    (ROCK, SPOCK): (-1, 1),
    
    (PAPER, ROCK): (1, -1),
    (PAPER, PAPER): (0, 0),
    (PAPER, SCISSORS): (-2, 2),
    (PAPER, LIZARD): (-3, 3),
    (PAPER, SPOCK): (1, -1),
    
    (SCISSORS, ROCK): (-2, 2),
    (SCISSORS, PAPER): (3, -3),
    (SCISSORS, SCISSORS): (0, 0),
    (SCISSORS, LIZARD): (1, -1),
    (SCISSORS, SPOCK): (-1, 1),
    
    (LIZARD, ROCK): (-3, 3),
    (LIZARD, PAPER): (2, -2),
    (LIZARD, SCISSORS): (-1, 1),
    (LIZARD, LIZARD): (0, 0),
    (LIZARD, SPOCK): (3, -3),
    
    (SPOCK, ROCK): (1, -1),
    (SPOCK, PAPER): (-1, 1),
    (SPOCK, SCISSORS): (2, -2),
    (SPOCK, LIZARD): (-3, 3),
    (SPOCK, SPOCK): (0, 0)
}
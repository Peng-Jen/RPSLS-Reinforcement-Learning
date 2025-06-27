from .action_names import *

CLASSIC_RPSLS = {
    (ROCK, ROCK): (0, 0),
    (ROCK, PAPER): (0, 1),
    (ROCK, SCISSORS): (1, 0),
    (ROCK, LIZARD): (1, 0),
    (ROCK, SPOCK): (0, 1),
    
    (PAPER, ROCK): (1, 0),
    (PAPER, PAPER): (0, 0),
    (PAPER, SCISSORS): (0, 1),
    (PAPER, LIZARD): (0, 1),
    (PAPER, SPOCK): (1, 0),
    
    (SCISSORS, ROCK): (0, 1),
    (SCISSORS, PAPER): (1, 0),
    (SCISSORS, SCISSORS): (0, 0),
    (SCISSORS, LIZARD): (1, 0),
    (SCISSORS, SPOCK): (0, 1),
    
    (LIZARD, ROCK): (0, 1),
    (LIZARD, PAPER): (1, 0),
    (LIZARD, SCISSORS): (0, 1),
    (LIZARD, LIZARD): (0, 0),
    (LIZARD, SPOCK): (1, 0),
    
    (SPOCK, ROCK): (1, 0),
    (SPOCK, PAPER): (0, 1),
    (SPOCK, SCISSORS): (1, 0),
    (SPOCK, LIZARD): (0, 1),
    (SPOCK, SPOCK): (0, 0)
}
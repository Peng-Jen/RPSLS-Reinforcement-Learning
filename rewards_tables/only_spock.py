from .action_names import *

ONLY_SPOCK = {
    (ROCK, ROCK): (0, 0),
    (ROCK, PAPER): (0, 0),
    (ROCK, SCISSORS): (0, 0),
    (ROCK, LIZARD): (0, 0),
    (ROCK, SPOCK): (0, 1),
    
    (PAPER, ROCK): (0, 0),
    (PAPER, PAPER): (0, 0),
    (PAPER, SCISSORS): (0, 0),
    (PAPER, LIZARD): (0, 0),
    (PAPER, SPOCK): (0, -1),
    
    (SCISSORS, ROCK): (0, 0),
    (SCISSORS, PAPER): (0, 0),
    (SCISSORS, SCISSORS): (0, 0),
    (SCISSORS, LIZARD): (0, 0),
    (SCISSORS, SPOCK): (0, 1),
    
    (LIZARD, ROCK): (0, 0),
    (LIZARD, PAPER): (0, 0),
    (LIZARD, SCISSORS): (0, 0),
    (LIZARD, LIZARD): (0, 0),
    (LIZARD, SPOCK): (0, -1),
    
    (SPOCK, ROCK): (1, 0),
    (SPOCK, PAPER): (-1, 0),
    (SPOCK, SCISSORS): (1, 0),
    (SPOCK, LIZARD): (-1, 0),
    (SPOCK, SPOCK): (1, 1)
}
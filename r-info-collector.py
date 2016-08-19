"""
Written by Matthew Cook
Created August 9, 2016
mattheworion.cook@gmail.com

Crawls github repositories for R scripts.  Reads the files and collects the
most common libraries and functions used in the scripts. 

Used for the data collection needed to convert common R scripts into Python
scripts.

What it does:
    -Collects files from Github repos
    -Reads files, recording names of libraries and function calls
    -Stores information collected in database.
        -Database collects amount of times libraries/functions are used
         together
"""
from urllib import robotparser

robot = robotparser.RobotFileParser()
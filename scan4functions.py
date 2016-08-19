"""
Written by Matthew Cook
Created August 12, 2016
mattheworion.cook@gmail.com

This script is used to detect R specific function calls.  It will then
log each function call and check it against the collection of known
conversions.  If the function isn't in the known conversions, it will issue
a notification to the user what was not converted and where it occurs in the 
file (which line).

TODO: Fix variable definitions to be private
"""
import re

# Common to multiple regexes
fill = '.*?'	# Non-greedy match on filler
arrow = '(<)' + '(-)'
params = '(\\(.*\\))'
fname = '((?:[a-z][a-z]+))'

#### Regex for function call #####
fcall = re.compile(
                fill +
                arrow +
                fill +
                fname + 
                params,
                re.IGNORECASE | re.DOTALL)
                
#### Regex for function definition ######
fdefine = '(function)'	# Word 2

fdef = re.compile(
                fname +
                fill +
                arrow +
                fill +
                fdefine +
                params,
                re.IGNORECASE | re.DOTALL)

# Define list to store found function definitions
func_defs = []

# Define dictionary to store found function calls (non-user defined) and 
# their lines
r_calls = {}

# Read file
def scan4Functions(filename):
    """Scans for R style function calls ignoring user-defined"""
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            if not line.lstrip().startswith('#'):
                s_def = fdef.search(line)            
                if not s_def.group(1) in func_defs:
                    func_defs.append(s_def)
    
                s_call = fcall.search(line)
                if not s_call.group(2) in func_defs:
                    r_calls.update({s_call : line})
    return r_calls

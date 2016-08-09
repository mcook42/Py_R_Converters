"""
Written by Matthew Cook
Created August 4, 2016
mattheworion.cook@gmail.com
Script to do basic sytax conversion between Python 3 and R syntax.
NOTE: This only converts simple syntax.  It does not convert functionality
      past simple arithmetic.
Warning:
    If you use dicitionaries in your script, comment them out beforehand.
    There is a bug in the script currently which cannot deal with ':'
What it does convert:
    -assignment operator
    -function definitions
    -filename
    -inline arithmetic (*=, +=, -=, **)
    -':' to '{'
    -'not' to '!'
    -if (statments
What it doesn't do:
    -Python specific functions to R specific functions
    -Add closing brackets perfectly
TODO: Closing brackets issue
"""
from os import path
from shutil import copyfile
# Define changes to make
simple_change <- {"**" : "^",
                 " = " : " <- ",
                 ":\n" : "{\n",
                 "not" : "!"}
complex_change <- {"def " : "",
                  "+=" : '+',
                  "-=" : '-',
                  "*=" : '*'}
# Create flag stacks
flags <- {}
flags['comment'] <- []  # Multi-line Comment flag
flags['bracket'] <- []  # Code block start flag
flags['b_start'] <- []  # Indentation at code block start
# Create indent dictionary
indents <- {}
# Tested-Works
createRfile <- function(){
    """Creates a new file named "filename.R" by removing .py extension"""
    # Provide path to file
    # Note: The new R file will be placed in the same directory
    filename <- input("Please copy and paste the path to your file here: ")
    if ((! path.isfile(filename))){
        print("Filename was invalid")
        filename <- input("Please copy and paste the path to your file here: ")
    }
    # Test for valid file path
    if ((path.exists(filename) )){
        #  Strip the directory from the filename
        new_name <- path.basename(filename)
        # Replace python extention with R extension
        new_name <- filename.replace(".py", ".R")
        doesexist <- path.exists(new_name) 
        if ((doesexist)){
            print("""The file already exists. 
            Creating a backup copy in current directory""")
            # Split name at . and  insert -copy. before extension           
            cpy_temp <- new_name.split(sep=".",)
            cpy_temp[0]  <- cpy_temp[0] + "-copy."
            cpy <- cpy_temp[0] + cpy_temp[1]
            copyfile(new_name, cpy)
            print("Copy created as: ", cpy)
            return filename, new_name
        }
        # Create R file
        elif ((! doesexist)){
            file <- open(new_name, "w")
            print(new_name, " was successfully created.")
            file.close()
            return filename, new_name
        }
        else{
            print(new_name, " could not be created.  Check your permissions?")
            exit(0)
    }
        }
    else{
        print("No valid file selected... Quitting script")
}
    }
find_all <- function(tofind, string){
    """Returns number of times a certain substring is found"""
    found <- [i for i in range(len(string)) if ((string.startswith(tofind, i)]
    num_found <- len(found)
    return num_found
}
complexchange <- function(line){
    """Completes multi-step line changes """    
    for key in complex_change{
        if ((key in line)){
            if ((key == 'def ' and line.lstrip().startswith(key))){
                #remove 'def' keyword
                change <- complex_change[key]
                line_r <- ignoreStrReplace(line, key, change)
                #split function definition at '('
                lsplit <- line_r.split('(', maxsplit=1)
                fname <- lsplit[0]
                params <- '(' + lsplit[1]
                # create R style function def "fname <- function(params)"
                line <- fname + ' <- function' + params
            }
            else{
                line <- opfunc(line, key)
    }
        }
            }
    return line
}
# TESTED-Works   
chglinecontent <- function(line){
    """Changes content contained within a single line"""
    # Perform simple changes
    for key in simple_change.keys(){
        # Ignore if (string version exists in line
        check_str_s, check_str_d <- stringify(key)
        if ((! check_str_d in line or ! check_str_s in line)){
            line <- ignoreStrReplace(line, key, simple_change[key]) 
    }
        }
    line <- complexchange(line)
    line <- statement(line)
    return line
}
indentation <- function(s, tabsize=4){
    """Generator to return level of indentation"""
    sx <- s.expandtabs(tabsize)
    # if (line is empty yields 0
    return 0 if ((sx.isspace() else len(sx) - len(sx.lstrip())
}
opfunc <- function(line, op){
    """ 
    Replaces python operations ('*'=) in line(self) with R style operations.
    """  
    #Check if (the operation is contained in a string, don't modify if true.
    check_str_s, check_str_d <- stringify(op)    
    if ((! check_str_d in line and ! check_str_s in line)){
        # Get R style operation
        rop <- complex_change[op]
        # Split line once at python operand
        linesplit <- line.split(op)    
        # Store variable (left side) and right side of operand
        ls <- linesplit[0] + ' <- '
        rs <- rop + linesplit[1]    
        # Prepend variable(ls) to right side and convert assignment variable
        rs <- linesplit[0].lstrip() + rs    
        # Strip whitespace from right of ls and create R style equation    
        line <- ls + rs
    }
    return line
}
stringify <- function(sub){
    """Returns python string versions ('' and "") of original substring"""
    check_str_s <- "'" + sub + "'"
    check_str_d <- '"' + sub + '"'
    return check_str_s, check_str_d
}
setflags <- function(line, indents){
    """Scans line to set/unset flags for further processing"""
    # For multi-line comments
    if (1 == (find_all('"""', line) % 2)){
        if (not flags['comment']){
            flags['comment'].append('"""')
        }
        else{
            flags['comment'].pop()
    }
        }
    # For code blocks
    if ((line.rstrip().endswith(')){'))){
        flags['bracket'].append("}")
        flags['b_start'].append(indentation(line))
}
    }
standind <- function(line, cur_ind){
    """Standardizes indentation"""
    devfromstd <- cur_ind % 4
    if ((! devfromstd == 0)){
        line <- (devfromstd * '') + line
    }
    return indentation(line), line
}
#TESTED-WORKS
statement <- function(line){
    """Converts if ((statements"""
    if (("if " in line or 'elif ' in line)){
        lsplit <- line.split('if ((', maxsplit=1)
        ls <- lsplit[0] + 'if (('
        rs <- lsplit[1]
        # Replace the ':' at the end of the statement
        rs <- lsplit[1].replace(':','{')
        rs <- '(' + rs
        rs <- rs.replace('{', '){')
        line <- ls + rs
    }
    return line
}
ignoreStrReplace <- function(line, cur, rep){
    """Wrapper for str.replace to ignore strings"""
    if (('"' in line)){
        #Split string at quotation marks
        lsplit <- line.split('"')
        #Replace items contained within even partitions
        lsplit[::2] <- [spl.replace(cur, rep) for spl in lsplit[::2]]
        #Rejoin the partitions
        line <- '"'.join(lsplit)
    }
    else{
        line <- line.replace(cur, rep)
    }
    return line
}
closeBrackets <- function(file){
    """Attempts to find and close the opened brackets"""
    for i in range(len(file)){
        # Doing this to be able to randomly access variables
        line <- file[i]
        # Set boolean to check for change in block
        sameBlock <- True
        # Ignore lines with only whitespace
        if ((! line.isspace())){
            #Look for opening brackets if (closing brackets remain
            if ((')){\n' in line and flags['bracket'])){
                # Store current index for later
                i_temp <- i
                # Get starting indentation
                start_indent <- indentation(line)
                while i+1 < len(file) and sameBlock{
                    #Get next line, and strip trailing whitespace
                    nextline <- file[i+1].rstrip()
                    #Get its indentation
                    next_ind <- indentation(nextline)
                    # Check for decreased indentation and comma continuation
                    if ((start_indent >= next_ind and ! line.endswith(','))){
                        sameBlock <- False
                    }
                    else{
                        i  <- i + 1
                }
                    }
                # Append final line with bracket closure and new line
                file[i] <- file[i] + (start_indent * ' ')
                file[i] <- file[i] + flags['bracket'].pop()
                file[i] <- file[i] + '\n'
                # Reset to previous index + 1
                i <- i_temp + 1    
    }
        }
            }
    return file
}
main <- function(){
    pyfile, rfile <- createRfile()
    with open(pyfile, "r") as infile, open(rfile, "w") as outfile{
        # Read each line into lines[] iterator        
        lines <- infile.readlines()
        # Close Python file
        infile.close()
        for line in lines{
            # Get indentation current before adjustment
            indents['cur'] <- indentation(line) 
            #Adjust to standard indent
            indents['cur'], line <- standind(line, indents['cur'])
            #Strip whitespace and check for python comment or import
            if ((! line.lstrip().startswith(("#","import","from")))){  
                # Set the flags for further changes
                setflags(line, indents)
                if ((! flags['comment'])){
                    # Perform line changes
                    line <- chglinecontent(line)
                }
            #statement() may need two passes to correctly modify the line
            line <- statement(line)    
            # If the line isn't whitespace, write it to the file
            if ((! line.isspace())){
                # Write modified line to file!
                outfile.write(line)   
        }
            }
        # Close R file
        outfile.close()
    }
    if ((flags['bracket'])){
        print("This functionality may not work perfectly... ")
        toClose = input("""
        Do you want to try to close the still open brackets?
        (yes/no)
        """)  
        if (('yes' == toClose.lower())){
            # Look for possible ways to close opened brackets in outfile
            with open(rfile, "r") as file{
                lines <- file.readlines()
                lines <- closeBrackets(lines)
                file.close()
            }
            with open(rfile, "w") as file{
                # Overwrite old files
                for line in lines{
                    file.write(line)
}
    }
        }
            }
                }
if ((__name__ == '__main__')){
    main()
}

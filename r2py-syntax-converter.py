"""
Written by Matthew Cook
Created August 9, 2016
mattheworion.cook@gmail.com

Script to do basic sytax conversion between R and Python 3 syntax.

What it does convert:
    -assignment operator
    -function definitions
    -filename
    -'{' to ':'
    -'!' to 'not'
    -if statments
    -remove ';' line endings

What it doesn't do:
    -Python specific functions to R specific functions
    -Add closing brackets with perfect indentation

"""

from os import path, scandir
from shutil import copyfile

# Define simple changes to make
simple_change = {"^" : "**",
                 "<-" : " = ",
                 "{\n" : ":\n",
                 "!" : "not",
                 ";" : "",
                 "length" : "len",
                 "rm(" : "del("}                 


def createPyfile(filename):
    """Creates a new file named "filename.py" by removing .R extension"""

    # Test for valid file path
    if path.exists(filename) :
        #  Strip the directory from the filename
        new_name = path.basename(filename)
        # Replace python extention with R extension
        new_name = filename.replace(".R", ".py")

        doesexist = path.exists(new_name)

        if doesexist:
            print("""The file already exists.
            Creating a backup copy in current directory""")

            # Split name at . and  insert -copy. before extension
            cpy_temp = new_name.split(sep=".",)
            cpy_temp[0] += "-copy."
            cpy = cpy_temp[0] + cpy_temp[1]

            copyfile(new_name, cpy)
            print("Copy created as: ", cpy)
            return filename, new_name

        # Create R file
        elif not doesexist:
            file = open(new_name, "w")
            print(new_name, " was successfully created.")
            file.close()
            return filename, new_name

        else:
            print(new_name, " could not be created.  Check your permissions?")
            exit(0)

    else:
        print("No valid file selected... Quitting script")


def brackets(line):
    """Replace '{' with ':' and remove '}'"""
    line = ignoreStrReplace(line, '{', ':')
    line = ignoreStrReplace(line, '}', '')
    return line


def ignoreStrReplace(line, cur, rep, count=None):
    """Wrapper for str.replace to ignore strings"""
    # Lazy fix to count being None
    if not count:
        count = 50
    if '"' in line:
        #Split string at quotation marks
        lsplit = line.split('"')
        #Replace items contained within even partitions
        lsplit[::2] = [spl.replace(cur, rep, count) for spl in lsplit[::2]]
        #Rejoin the partitions
        line = '"'.join(lsplit)
    else:
        line = line.replace(cur, rep, count)
    return line


def statement(line):
    """Convert R if statements to Python if statements"""
    if line.lstrip().startswith('if'):
        line = ignoreStrReplace(line, '(', '', count=1)
        line = ignoreStrReplace(line, ')', '', count=1)        
    if 'else if' in line:
        line = ignoreStrReplace(line, 'else if', 'elif')
        
    return line


def chglinecontent(line):
    """Returns changed line after modifications"""
    line = function(line)
    line = statement(line)
    line = brackets(line)
    line = dollarsign(line)
    # Perform simple changes
    for key in simple_change.keys():
        # Ignore if string version exists in line
        check_str_s, check_str_d = stringify(key)
        if not check_str_d in line or not check_str_s in line:
            line = ignoreStrReplace(line, key, simple_change[key])

    return line

  
def stringify(sub):
    """Returns python string versions ('' and "") of original substring"""
    check_str_s = "'" + sub + "'"
    check_str_d = '"' + sub + '"'
    return check_str_s, check_str_d


def function(line):
    """Returns python-style function definition"""
    if 'function' in line and '(' in line and ')' in line:
        line = line.replace('function', '')
        line = line.replace('<-', '')
        lsplit = line.split('(', maxsplit=1)
        # Get name and parameters. Strip whitespace
        fname = lsplit[0].strip()
        params = lsplit[1].strip()
        # create python style function definition (def name(parameters))
        params = '(' + params
        line = 'def ' + fname + params
    return line


def dollarsign(line):
    """Return line with $ notation replaced by dictionary reference"""
    #Note: Works only if code is vectorized.  Possibly consider regex to fix.
    if '$' in line:
        line = line.replace('$', '[')
        line = line.replace('\n', ']\n')
    return line

def editfiles(rfile, pyfile):
    """Does single file editing"""
    with open(rfile, "r") as infile, open(pyfile, "w") as outfile:
            # Read each line into lines[]
            lines = infile.readlines()
            # Close R file
            infile.close()
            for line in lines:
                if line.lstrip().startswith('#'):
                    #Skip commented lines
                    pass
                else:
                    # Perform changes
                    line = chglinecontent(line)
                outfile.write(line)
            #Close python file
            outfile.close()


def main():
    #Ask user if converting file or folder of files
    choice = input("""Do you want to convert a single file or a folder full?
    Enter 'single' for single file or 'folder' for folder of files:""")
    #For single file
    if choice.lower() == 'single':
        # Provide path to file
        # Note: The new python file will be placed in the same directory
        filename = input("Please copy and paste the path to your file here: ")  
        if not path.isfile(filename):
            print("Filename was invalid")
            filename = input("Please copy and paste the path to your file here: ")
            #Create python file
            rfile, pyfile = createPyfile(filename)
            editfiles(rfile, pyfile)        
        
    #For mutiple files in a folder
    elif choice.lower() == 'folder':
        folder = input("Please enter the path to your folder: ")
        if path.isdir(folder):
            message = "Are you sure you want to convert all of " 
            message += folder
            message += " ? (yes/no)"
            dblcheck = input(message)
            if dblcheck.lower().startswith('n'):
                print("Ok... Exiting program now.")
                exit(0)
            for file in scandir(folder):
                filepath = file.path
                if path.isfile(filepath) and filepath.endswith('.R'):
                    rfile, pyfile = createPyfile(filepath)
                    editfiles(rfile, pyfile)


if __name__ == '__main__':
    main()


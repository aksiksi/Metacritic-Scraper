from sys import argv
import module

# Main program starts here
print "\nMetacritic Score Grabber v0.1"
print "-----------------------------\n"

# If no argument provided, assumes it's -out
try:
    param = argv[1]
except IndexError:
    param = '-out'

# Argument selection
if param == '-csv':
    try:
        module.csv(argv[2])
    except IndexError:
        print "Invalid usage. Please use -help or refer to readme provided for usage info.\n"
elif param == '-text':
    try:
        module.file(argv[2])
    except IndexError:
        print "Invalid usage. Please use -help or refer to readme provided for usage info.\n"
elif param == '-out':
    module.console()
elif param == '-help':
    print "Accepted parameters: -csv, -file, -here, or -help:\n"
    print "-csv: reads input from csv (game,console) and writes to a new csv."
    print "-text: reads input from file (game:console) and writes to a new file."
    print "-out: prompts to enter data (game:console) and outputs to terminal. If no argument is entered, -out will be assumed."
    print "-help: prints this info on screen.\n"
else:
    print "Unknown argument. Please use -help or refer to the readme if you don't know what to use.\n"
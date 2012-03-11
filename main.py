import httplib2
import time
from sys import argv

def file(path):
    game_console = {}

    # Populate dictionary with game:console from file.
    f = open(path)
    for line in f:
        arr = line.partition(':')
        game_console[''.join(arr[0])] = (''.join(arr[2])).rstrip('\n')
    f.close()
    
    s = time.time()
    
    output = scrape(game_console)
    
    # Write results to file
    f = open('scores.txt', 'w')
    f.write('Metacritic Score Grabber v0.1 - Output\n')
    f.write('--------------------------------------\n\n')
    
    for g, c in game_console.items():
        current = output[g]
        f.write("{0} on {1}: ".format(g, c) + '\n')
        if 'Game' not in current:
            f.write('\n- Metascore is: ' + current[0] + '\n')
            f.write('- Userscore is: ' + str(current[1]) + '\n')
            f.write('- Combined score is: ' + str(current[2]) + '\n')
            f.write('\n\n')
        else:
            f.write('\n' + current + '\n\n')
            
    f.write("Done in %f seconds." % (time.time()-s))

def console():
    game_console = {}

    while True:
        data = raw_input("Enter game:console (-1 to stop) -> ")
        if data == '-1':
            break
        if ':' in data:
            arr = data.partition(':')
            game_console[''.join(arr[0])] = ''.join(arr[2]) # Parses game:console to dict format
        else:
            print "Woah. Please make sure to use the ':' as a seperator. Try again."
    print ""

    # Start timer
    s = time.time()

    if game_console:
        output = scrape(game_console)
    else:
        print "Nothing to print.\n"

    # Print scores from output to screen
    for g, c in game_console.items():
        current = output[g]
        print "{0} on {1}: ".format(g, c),
        if len(current) > 1:
            print "Metascore = {0},".format(current[0]),
            print "Userscore = {0},".format(current[1]),
            print "Combined score = {0}".format(current[2])
        else:
            print current

    print "Done in %f seconds." % (time.time()-s)

def csv(path):
    game_console = {}

    # Populate dictionary with game:console from file.
    f = open(path)
    for line in f:
        arr = line.partition(',')
        game_console[''.join(arr[0])] = (''.join(arr[2])).rstrip()
    f.close()
    
    # Start timer
    s = time.time()
    
    output = scrape(game_console)
    
    # Write results to file
    f = open('scores.csv', 'w')
    #f.write('Metacritic Score Grabber v0.1 - Output\r')
    #f.write('\r')
    f.write('Game,Console,Metascore,Userscore,Combined Score\r')
    
    for g, c in game_console.items():
        current = output[g]
        f.write("{0},{1},".format(g, c))
        if 'Game' not in current:
            f.write(str(current[0]) + ',')
            if current[0] == 'Not available':
                f.write('N/A,N/A\r')
            else:
                f.write(str(current[1]) + ',')
                f.write(str(current[2]) + '\r')
        else:
            f.write('-,-,-\r')
    f.close()
            
    print "Done in %f seconds." % (time.time()-s)

def scrape(game_console):
    count = 0
    total = len(game_console)
    output = {}

    print "Working..."
    print ""

    for g, c in game_console.items():
        # Gets source code of game page
        Http = httplib2.Http()
        source = Http.request("http://www.metacritic.com/game/{0}/{1}".format(c.replace(' ', '-').lower(), g.replace(' ', '-').lower()))[1]

        # Checks if game name and/or console name is correct.
        if '<span class="error_type">Page Not Found</span>' in source:
            count += 1
            print "{0} of {1} failed...".format(count, total)
            output[g] = "Game or console is incorrect."
        else:
            # Finds metascore
            index = source.find('"v:average">')
            index += len('"v:average">')
            meta_score = source[index] + source[index+1]

            # Finds userscore
            index = source.find('"score_value">')
            index += len('"score_value">')
            try:
                user_score = float(source[index] + '.' + source[index+2])
            except ValueError:
                user_score = 'Not available'

            # Finds combined score
            try:
                combined_score = ((int(meta_score) / 10.0) + float(user_score)) / 2.0
            except ValueError:
                combined_score = 'Not available'

            # Append results to dict
            output[g] = (meta_score, user_score, combined_score)

            # Track and print scraping progress
            count += 1
            print "{0} of {1} completed...".format(count, total)
    print ""
    return output

# Main program starts here
print "\nMetacritic Score Grabber v0.1"
print "-----------------------------\n"

# If no argument provided, assume its -here
try:
    param = argv[1]
except IndexError:
    param = '-here'

# Argument selection
if param == '-csv':
    try:
        csv(argv[2])
    except IndexError:
        print "Invalid usage. Please use -help or refer to comments at the top of the script for usage info.\n"
elif param == '-file':
    try:
        file(argv[2])
    except IndexError:
        print "Invalid usage. Please use -help or refer to comments at the top of the script for usage info.\n"
elif param == '-here':
    console()
elif param == '-help':
    print "Accepted parameters: -csv, -file, -here, or -help:\n"
    print "-csv: reads input from csv (game,console) and writes to a new csv."
    print "-file: reads input from file (game:console) and writes to a new file."
    print "-here: prompts to enter data (game:console) and outputs to terminal. If no argument is entered, -here will be assumed."
    print "-help: prints this info on screen.\n"
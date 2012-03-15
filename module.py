import time
import httplib2

def file(path):
    game = []
    console = []

    # Populate lists with game:console from file.
    f = open(path)
    for line in f:
        arr = line.partition(':')
        game.append(''.join(arr[0]).strip())
        console.append((''.join(arr[2])).strip())
    f.close()
    
    # Start timer
    s = time.time()
    
    output = scrape(game, console)
    
    # Write results to file
    f = open('scores.txt', 'w')
    f.write('Metacritic Score Grabber v0.1 - Output\n')
    f.write('--------------------------------------\n\n')

    count = 0
    
    for g, c in zip(game, console):
        current = output[count]
        f.write("{0} on {1}: ".format(g, c) + '\n')
        if 'Game' not in current:
            f.write('\n- Metascore is: ' + str(current[0]) + '\n')
            f.write('- Userscore is: ' + str(current[1]) + '\n')
            f.write('- Combined score is: ' + str(current[2]) + '\n')
            f.write('\n\n')
        else:
            f.write('\n' + current + '\n\n')
        count += 1
            
    f.write("Done in %f seconds." % (time.time()-s))
    f.close()

def console():
    game = []
    console = []

    while True:
        data = raw_input("Enter game:console (-1 to stop) -> ")
        if data == '-1':
            break
        if ':' in data:
            arr = data.partition(':')
            game.append(''.join(arr[0]))
            console.append(''.join(arr[2])) # Parses game:console to dict format
        else:
            print "Woah. Please make sure to use the ':' as a seperator. Try again.\n"
    print ""

    # Start timer
    s = time.time()

    if game and console:
        output = scrape(game, console)
    else:
        print "Nothing to print.\n"

    count = 0

    # Print scores from output to screen
    for g, c in zip(game, console):
        current = output[count]
        print "{0} on {1}: ".format(g, c),
        if 'Game' not in current:
            print "Metascore = {0},".format(current[0]),
            print "Userscore = {0},".format(current[1]),
            print "Combined score = {0}".format(current[2])
        else:
            print current
        count += 1

    print "\nDone in %f seconds.\n" % (time.time()-s)

def csv(path):
    game = []
    console = []

    # Populate lists with game,console from .csv
    f = open(path)
    for line in f:
        arr = line.partition(',')
        game.append(''.join(arr[0]).strip())
        console.append((''.join(arr[2])).strip())
    f.close()

    # Start timer
    s = time.time()

    output = scrape(game, console)
    
    # Write results to file
    f = open('scores.csv', 'w')
    f.write('Game,Console,Metascore,Userscore,Combined Score\r') # Table headers
    count = 0 # Count current game

    for g, c in zip(game, console):
        current = output[count]
        f.write("{0},{1},".format(g, c))
        if 'Game' not in current:
            if current[0] == 'Not available':
                f.write('N/A,')
            else:
                f.write(str(current[0]) + ',')
            if current[1] == 'Not available':
                f.write('N/A,N/A\r')
            else:
                f.write(str(current[1]) + ',' + str(current[2]) + '\r')
        else:
            f.write('-,-,-\r')
        count += 1
    f.close()
            
    print "Done in %f seconds." % (time.time()-s)

def scrape(game, console):
    count = 0
    total = len(game)
    output = []

    print "Working..."
    print ""

    for g, c in zip(game, console):
        # Gets source code of game page
        Http = httplib2.Http()
        source = Http.request("http://www.metacritic.com/game/{0}/{1}".format(c.replace(' ', '-').lower(), g.replace(' ', '-').lower()))[1]

        # Checks if game name and/or console name is correct
        if '<span class="error_type">Page Not Found</span>' in source:
            count += 1
            print "{0} of {1} failed...".format(count, total)
            output.append("Game or console is incorrect")
        else:
            # Finds metascore
            index = source.find('"v:average">')
            index += len('"v:average">')
            try:
                meta_score = int(source[index] + source[index+1])
            except ValueError:
                meta_score = 'Not available'

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
            output.append((meta_score, user_score, combined_score))

            # Track and print scraping progress
            count += 1
            print "{0} of {1} completed...".format(count, total)
    print ""
    return output
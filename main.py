# Written for Demcon decode challenge #4 - Festival schedule generator
# Author: Niels Davenne
# Date: 16/08/2024
# -----------------------

### Libraries & imports  
import csv
from prettytable import PrettyTable
from prettytable import SINGLE_BORDER

### Variables declaration

# Show_data.txt list to dictionary importer:
shows = {} # Dictionaries
shows_buffer = {}
shows_remaining = {}

max_end = 0  # Keeps track of latest time that a show runs

# Create empty list to keep track of number of stages. This wil later become a nested list.
stage = []

# Make the final table element
table = PrettyTable()


### Read data set
with open('show_data.txt') as r:
    reader = csv.reader(r, delimiter=' ')
    for row in reader:
        shows.update({row[0]:{'start':int(row[1]),'end':int(row[2])}})

        # (Nested) dictionary form:
        # shows['show_x',[start,end]]
        # dict     str     int  int

        if(max_end < int(row[2])):  # While we're at it, keep track of the longest running show for later use.
            max_end = int(row[2])

shows_remaining = shows             # Set shows_remaining with complete list of all shows (first time only)


### Main functions
# ============================================================

# Check for overlap in show performance times:
def checkOverlap(show1,show2):
    _start1 = show1['start']
    _end1 = show1['end']
    _start2 = show2['start']
    _end2 = show2['end']

    if(_end1<_start2 or _end2 < _start1): #Simple but effective method to test for any overlap
        return 0 # There is no overlap
    else:
        return 1 # There is overlap

def getShowDuration(show):
    _start1 = show['start']
    _end1 = show['end']
    _duration = _end1 - _start1
    return _duration

    
def scheduleStage(i):
    global shows_buffer
    global shows_remaining          # Needed to prevent issues with accessibility (?)
    shows_buffer = {}               # Flush show buffer list
    shows_buffer = shows_remaining  # Fill buffer with only the shows remaining
    shows_remaining = {}            # Flush remaining shows list

    # Check if next show can be added to current stage.
    for key in shows_buffer.keys():

        if (len(stage[i]) > 0):
            for j in range(len(stage[i])):
                # print('For ' + key + ', starting run ' + str(j+1) + '/' + str(len(stage[i])))
                # print(stage[i][j])
                # print(shows_buffer[stage[i][j]])
                if(checkOverlap(shows_buffer[key], shows_buffer[stage[i][j]])): # Yes, this took quite some iterations to get right. I made it hard on myself :)
                    # overlap, copy over to remaining shows list
                    shows_remaining.update({key:shows_buffer.get(key)})
                    # print (key + str(', overlap: ' + str(checkOverlap(shows[key],stage[i][j]))))
                    break
                else:
                    # no overlap
                    # print(key + ' checked with ' + str(stage[i][j]) + ', no. ' + str(j+1) + '/' + str(len(stage[i])) + '. No overlap. Proceeding...')
                    if (j == len(stage[i])-1):
                        stage[i].append(key)
                        # print(str(key) + ' added to stage list')
                    # continue
                
        else:
            # print('no shows to compare to in stage, adding ' + str(key))
            stage[i].append(key)   


### Calculate scheduling
# Try to fill as much shows on one stage as possible, then move onto the next.
index = 0
while (len(shows_remaining)>0):
    stage.append([])
    scheduleStage(index)
    # print('Completed scheduling of stage ' + str(index))
    index+=1

### Show final results
print('\n') # Empty line
print('Shows per stage:')
print('----------------------------------')

# First, let's show the results per stage; which shows are assigned to which stage.
for k in range(len(stage)):
    print('Stage ' + str(k+1) + ': ' + str(stage[k]))

# Create table layout
# Let's create a more visual overview of which show plays when (columns), per stage (rows)
time_list = ['time (h)']
for i in range(max_end):
    time_list.append(str(i+1))
table.field_names = time_list   # Assign all times in hours to first row of table

tstage = [] # 'Table' version of the stage (nested) list, used to create the rows per stage.
for k in range(len(stage)):
    tstage.append(['-'] * (max_end+1))  # Assign empty '-' content to whole row at first

for k in range(len(stage)):             # Then overwrite the placholder data with the number of the actual show running.
    for l in range(len(stage[k])):
        start_time = shows[stage[k][l]]['start']
        duration = getShowDuration(shows[stage[k][l]])
        for m in range(duration+1):     # Which happens here.
            show_no = stage[k][l]
            show_no = show_no.strip("show_")
            tstage[k][start_time + m] = show_no
    tstage[k][0] = str("Stage " + str(k+1))
    table.add_row(tstage[k])

table.set_style(SINGLE_BORDER)  # Finally, sert style & print the table
print('\nShows schedule table:')
print(table)
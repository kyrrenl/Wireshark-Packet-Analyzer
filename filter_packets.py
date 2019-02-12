def filter(filename, num) :

    #print 'opening file'
    filteredfile = "Node" + str(num) + "_filtered.txt"
    f = open(filename,'r')
    w = open(filteredfile, 'w')
    line = f.readline() #Line for reading
    summaryLine = line  #header line 
    while line : #While the line read hasn't reached the end of the file
        #If line has 'echo' in it, continue to read and write lines to the filtered file 
		#until the next header line is reached.
        if ('Echo' in line) : 
	    w.write(summaryLine)
	    while ((summaryLine not in line)) :
		w.write(line)
		line = f.readline()
        line = f.readline()

    #print 'called filter function in filter_packets.py'
    f.close()
    w.close()


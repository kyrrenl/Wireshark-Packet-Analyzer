#structure of hex in capture:
#source IP: row 0010 col 11-14
########dest IP: row 0010 - 0020 col 15-02\
#total len: row 0010 col 1-2
#ttl: row 0010 col 7
#ID: 0010 3-4
#PROTOCOL field: 0010 8
#type ICMP(reply/request) 0020 3
#IDTENTIFIER 0020 7-8
#Sequence number 0020 9-10

def parse(ipAddr,filename) :
	sourceIPhex = [] #List of source IP in hex
	destIPhex = []   #List of destination IP in hex
	totalLenhex = [] #List of packet length in hex
	ttlhex = []      #List of packet ttls in hex
	reqOrReplyhex = [] #ICMP type 
	seqNumhex = []   #List of sequence number in hex
	temp = []
	packetTime = []
	record = ""
	dest = ""
	count = 0
	
        #Open given filtered file and populate lists with 
	#values from hex portion
	f = open(filename,'r')
	line = f.readline()
	while line:
		if (line.startswith("0010")):
			data = line.split(' ')
			sourceIPhex.append(data[12:16])
			dest = data[16:18]
			totalLenhex.append(data[2:4])
			ttlhex.append(data[8])
			count += 1
		elif (line.startswith("0020")):
			data=line.split(' ')
			dest += data[2:4]
			reqOrReplyhex.append(data[4])
			seqNumhex.append(data[10:12])

		if(ipAddr in line) : 
	    		record = line.split(" ")
	    		record = list(filter(None, record))
	    		temp.append(record)

		if (len(dest) == 4) :
		    destIPhex.append(dest)
		    dest = ""
	 
		line = f.readline()	
	f.close()
	#Remove remove unwanted data from list
    	for iter in temp :
		del iter[2:15] #removes information after time in packet
		iter.pop(0) #remove the packet number
		packetTime.append(iter[0])

	#Create lists that will hold converted hex values
	sourceIPdec = []
	destIPdec = [] 
	totalLendec = []
	ttldec = []
	replyOrRequeststr = []
	seqNumdec = []
	summaryList = []

	#Convert source IP from hex to decimal
	for iter in sourceIPhex:
	    #print iter
	    oct1 = int(str(iter[0]),16)
	    oct2 = int(str(iter[1]),16)
	    oct3 = int(str(iter[2]),16)
	    oct4 = int(str(iter[3]),16)
	    
	    result = str(oct1) + "." + str(oct2) + "." + str(oct3) + "." + str(oct4)
	    sourceIPdec.append(result)

	#Convert destination IP from hex to decimal
	for iter in destIPhex:
	    #print iter
	    oct1 = int(str(iter[0]),16)
	    oct2 = int(str(iter[1]),16)
	    oct3 = int(str(iter[2]),16)
	    oct4 = int(str(iter[3]),16)
	    
	    result = str(oct1) + "." + str(oct2) + "." + str(oct3) + "." + str(oct4)
	    destIPdec.append(result)

	#Convert length header from hex to decimal
	for iter in totalLenhex:
	    test = str(iter[0]) + str(iter[1])
	    oct1 = int(test,16)
	    octTotal = (oct1-28)
	    totalLendec.append(octTotal)

	#Convert ttl hex to decimal
	for iter in ttlhex:
	    test = str(iter)
	    oct1 = int(test,16)
	    result = str(oct1) 
	    ttldec.append(result)


	#determine if packet is request or reply
	for iter in reqOrReplyhex:
	    test = str(iter)
	    if(test == '08') :
		packetType = 'request'
	    elif(test == '00') :
		packetType = 'reply'
	    replyOrRequeststr.append(packetType)

	#convert seqNum hex to decimal
	for iter in seqNumhex:
	    test = str(iter[0]) + str(iter[1])
	    oct1 = int(test,16)
	    seqNumdec.append(oct1)

	#for loop onto sumLine string 
	# and creates the summaryLine list by spliting on the , of the sumLine string
	z = 0
	sumLine = ""
	#tempList = []
	for z in range(0,count) :

	    sumLine += str(packetTime[z]) + "," + str(sourceIPdec[z]) + "," + str(destIPdec[z]) + "," + str(totalLendec[z]) + "," + str(replyOrRequeststr[z]) + "," + str(seqNumdec[z]) + ","+ ("ttl=" +str(ttldec[z]))
	    summaryList.append(sumLine.split(","))
	    sumLine = ""
	    z += 1
	return summaryList




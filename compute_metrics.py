def compute(L,ipAddr) :

    reply_received = []
    reply_sent = []
    request_received = []
    request_sent = []
    tot_replies_sent_b = 0
    tot_replies_rec_b = 0

    #Lists for holding bytes of frame size requests sent/received
    tot_request_sent_b = 0
    tot_request_rec_b = 0
    
    #Lists for holding data of ICMP Payload requests sent/recieved
    tot_request_sent_d = 0
    tot_request_rec_d = 0
	
    for iter in L :
	#Populate lists for echo requests sent and replies received
	if(ipAddr in iter[1] ):
	    if('reply' in iter[4]) : 
	        reply_sent.append(iter)
	    if('request' in iter[4]) :
	        request_sent.append(iter)
	#Populate lists for echo requests received and replies sent
	if(ipAddr in iter[2] ) :
	    if('reply' in iter[4]) : 
	        reply_received.append(iter)
	    if('request' in iter[4]) :
	        request_received.append(iter)

    #DATA SIZE METRICS length
    for iter in reply_sent:
        tot_replies_sent_b = tot_replies_sent_b + float(iter[3])

    for iter in reply_received:
        tot_replies_rec_b = tot_replies_rec_b + float(iter[3])
    
    #Total Echo Request data sent
    for iter in request_sent:
	#ICMP Payload
        tot_request_sent_d = tot_request_sent_d + float(iter[3])
	#frame size
	tot_request_sent_b = tot_request_sent_b + (float(iter[3]) + 42)
    

    #Total Echo Request data received
    for iter in request_received:
	#ICMP Payload
        tot_request_rec_d = tot_request_rec_d + float(iter[3])
	#Frame size
	tot_request_rec_b = tot_request_rec_b + (float(iter[3]) + 42)
	
	
    #TIME BASED(4 METRICS)
    # 1. Avg ping round trip (kB/sec)subtract time from (request and reply)(L[0][1])from (l[0][0]) 
    #If reply/ iter[4] is the same If seq/ iter[5] is the same   
    sum1 = len(request_sent)
    i=0
    l1sum=0
    l2sum=0
    rtt=0
    rtt_sum=0
    while i < sum1:
        seqnum = str(request_sent[i][5])
        seqnum2 = str(reply_received[i][5])
        if(seqnum == seqnum2):
            #print "Sequence numbers are the same" + seqnum + " " + seqnum2
            l1sum = float(request_sent[i][0])
            l2sum = float(reply_received[i][0])
	    #reply_received
            rtt = l2sum - l1sum 
            rtt_sum = rtt_sum + rtt         
        i = i+1
    rtt_total_sum = rtt_sum
    rtt_sum=(rtt_sum / sum1)
    rtt_sum_ms=(rtt_sum / 100.0) * 100000

    # 2. Echo req. Throughput(kB/sec) sum of frame size all request packets and divide by sum of RTT 
    throughput = ((tot_request_sent_b / 1000)/ rtt_total_sum)

    # 3. Gooput: sum of all ICMP payloads of request sent by node divided by sum of all ping RTT
    goodput = ((tot_request_sent_d/1000) / rtt_total_sum)

    # 4. Avg Reply Delay: time between destination node reciving request and reply.
    sums = len(request_received)
    #print reply_sent[0]
    total=0
    replyDelay=0
    x=0
    while x < sums:
        seqnum = str(request_received[x][5])
        seqnum2 = str(reply_sent[x][5])
        if(seqnum == seqnum2):
            l1sum = float(request_received[x][0])
            l2sum = float(reply_sent[x][0])
            replyDelay +=  l2sum-l1sum
            x += 1
            total += 1
    
    replyDelay = replyDelay / total
    replyDelay_ms = replyDelay /100

    #DISTANCE BASED METRIC(1 METRIC)
    # 1. Avg# of hops per request
    y = 0
    hop_sum= len(request_sent)
    ttl_sum =0.0
    while y < hop_sum:
        ttl_seq1 = str(request_sent[y][5])
        ttl_seq2 = str(reply_received[y][5])

        if(ttl_seq1 == ttl_seq2):
            ttl1 = str(request_sent[y][6])
            ttl1 = ttl1.split('=')
            ttl1 = int(ttl1[1])

            ttl2 = str(reply_received[y][6])
            ttl2 = ttl2.split('=')
            ttl2 = int(ttl2[1])
			
            ttl_sum += (ttl1 - ttl2) + 1
            y +=1
    ttl_sum = ttl_sum / hop_sum

    #Print total number of echo request/reply sent/recieved
    print("Total Number of Echo Requests Sent: " + str(len(request_sent)))
    print("Total Number of Echo Requests Received: " + str(len(request_received)))
    print("Total Number of Echo Replies Sent: " + str(len(reply_sent)))
    print("Total Number of Echo Replies Received: " + str(len(reply_received)))

    #Print total number of BYTEs and Data sent for echo request/replies
    print("Total Number of Echo Request Bytes Sent: " + str(tot_request_sent_b))
    print("Total Number of Echo Request Bytes Received: " + str(tot_request_rec_b))
    print("Total Number of Echo Request Data Sent: " + str(tot_request_sent_d))
    print("Total Number of Echo Request Data Received: " + str(tot_request_rec_d))

    #Print average RTTs (ms)
    print "\nRTT is: " + str(round(rtt_sum_ms,2)) +" Milliseconds"
 
    #Print echo request throughput
    print "Throughput is: " + str(round(throughput,1)) + " kb/sec"
    #Print echo request goodput
    print "Goodput is: " + str(round(goodput,1)) + " kb/sec"

    #Print average reply delay (ms)
    print "Reply Delay is: " + str(round(replyDelay * 1000000,2))

    #Print average echo request hop count
    print "Average echo request hop count: " + str(round(ttl_sum,2))

    output= []

    #Populate output list with computed metrics 
    output.append("")	
    output.append(("Echo Requests Sent,Echo Requests Received,Echo Replies Sent,Echo Replies Received").split(","))
    output.append((str(len(request_sent)) +","+ str(len(request_received)) +","+
    str(len(reply_sent)) +","+ str(len(reply_received))).split(","))
    output.append(("Echo Request Bytes Sent (bytes),Echo Request Data Sent (bytes)").split(","))
    output.append((str(tot_request_sent_b) +","+ str(tot_request_sent_d)).split(","))
    output.append(("Echo Request Bytes Received (bytes),Echo Request Data Received (bytes)").split(","))
    output.append((str(tot_request_rec_b) +","+ str(tot_request_rec_d)).split(","))
    output.append("")
    output.append(("Average RTT" + "," +str(round(rtt_sum_ms,2))).split(","))
    output.append(("Echo Request Throughput (kB/sec)" +","+ str(round(throughput,1))).split(","))
    output.append(("Echo Request Goodput (kB/sec)" +","+ str(round(goodput,1))).split(","))
    output.append(("Average Reply Delay (microseconds)" +","+ str(round(replyDelay * 1000000,2))).split(","))
    output.append(("Average Echo Request Hop Count" +","+ str(round(ttl_sum,2))).split(","))
    output.append("")

    #Return list of computed metrics
    return output

from filter_packets import *
from packet_parser import *
from compute_metrics import *
import os
import csv

#Remove csv file if it exists
if os.path.exists("output.csv") :
    os.remove("output.csv")


#Open node1-5 files to filter ICMP echo/request entries
print "Filtering Files"
x = 1
length = 6
for x in range (1,length) :
    filename = "Node" + str(x) + ".txt"
    filter(filename, x)

#Open filtered node1-5 files to parse information
print "Parsing filtered files"
node1 = parse("192.168.100.1","Node1_filtered.txt")
node2 = parse("192.168.100.2","Node2_filtered.txt")
node3 = parse("192.168.200.1","Node3_filtered.txt")
node4 = parse("192.168.200.2","Node4_filtered.txt")
#node5 = parse("192.168","Node5_filtered.txt") #node 5 will be parsed with all nodes in mind- NOT USED FOR ANY CALCULATIONS

#Compute metrics using parsed values
print "Computing metrics using parsed data"
print "\nNODE 1"
n1 = compute(node1,"192.168.100.1")
print "\nNODE 2"
n2 = compute(node2,"192.168.100.2")
print "\nNODE 3"
n3 = compute(node3,"192.168.200.1")
print "\nNODE 4"
n4 = compute(node4,"192.168.200.2")
#print "\nNODE 5"
#compute(node5,"192.168") #node 5 - NOT USED FOR ANY CALCULATIONS

#Computed metrics to csv file
print "\nWriting computed metrics to output.csv"
with open('output.csv', 'a+') as outputCSV :
        writer = csv.writer(outputCSV, delimiter=",")
	#Write Node1 metrics
	writer.writerow(["Node 1"])
	for line in n1 :
	    writer.writerow(line)

	#Write Node2 metrics
	writer.writerow(["Node 2"])
	for line in n2 :
	    writer.writerow(line)

	#Write Node2 metrics
	writer.writerow(["Node 3"])
	for line in n3 :
	    writer.writerow(line)

	#Write Node2 metrics
	writer.writerow(["Node 4"])
	for line in n4:
	    writer.writerow(line)







import random 

sites = 633
sites = 1570
#sites = 33
a = [random.randint(1,6300) for x in range(sites)]
#print a

start = 0
for end in range(10,sites,10):
    #print "i", end
    print " ",
    for i in a[start:end]:
        print i,",",
    print ""    
    start = end

    

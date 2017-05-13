import csv
from matplotlib import pyplot as plt

def loaddata(filename):
    f = open(filename,encoding="utf-8")
    csvr = csv.reader(f)
    re = []
    for line in csvr:
        re.append(line)
    f.close()
    return re
j151 = loaddata("Java151.csv")
j152 = loaddata("Java152.csv")
j153 = loaddata("Java153.csv")
#get score
s151 = [ int(x[7].replace(" ","")) for x in j151 ]
s152 = [ int(x[7].replace(" ","")) for x in j152 ]
s153 = [ int(x[7].replace(" ","")) for x in j153 ]

#avg
avg151 = sum(s151)/len(j151)
avg152 = sum(s152)/len(j152)
avg153 = sum(s153)/len(j153)
avgCS = (avg151+avg152+avg153)/3.0

print("avg151=%f\navg152=%f\navg153=%f\n"%(avg151,avg152,avg153))

#square error
se151 = sum([ (x-avg151)**2 for x in s151 ])
se152 = sum([ (x-avg152)**2 for x in s152 ])
se153 = sum([ (x-avg153)**2 for x in s153 ])

print("se151=%f\nse152=%f\nse153=%f\n"%(se151,se152,se153))
print("se151=%f\nse152=%f\nse153=%f\n"%(se151,se152,se153))

#plot
plt.plot(s151,label="Class 151")
plt.hold(b=True)
plt.plot(s152,label="Class 152")
plt.plot(s153,label="Class 153")
#plt.plot(,avgCS,label="Avg. Score")
plt.xlabel("student#")
plt.ylabel("score")
plt.legend(loc='best')
plt.show()
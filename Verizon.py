#file = open('/Users/rajan/Downloads/houseList.csv', 'r')


import csv,random,geopy.distance as gp

house_data =[]
ant_data = []
seeds = []
k=200
n=50

#reading the house data
f = open('/Users/rajan/Downloads/houses.csv','r')
reader = csv.reader(f)
for row in reader:
#    print(row)
    house_data.append(row)
f.close()

#reading the antenna data
f = open('/Users/rajan/Downloads/antennas.csv','r')
reader = csv.reader(f)
for row in reader:
#    print(row)
    ant_data.append(row)
f.close()

#formatting the data as required
house_data = house_data[1:]
ant_data = ant_data[1:]

for row in house_data:
    del row[1]

for row in ant_data:
    del row[1]




#generate seeds
def seed_gen(k):
    random.shuffle(house_data)
    seeds = house_data[0:k]
    print(seeds)
    return seeds

seeds = seed_gen(k)
cnt =1

while(cnt <n):

    clusters =[]

    for i in range(k):
            add_cl = []
            add_cl.append(i)
            clusters.append(add_cl)

    #Assign Clusters
    for j in range(len(house_data)) :
            min_dist = []
            for i in range(len(seeds)):
                #print(seeds[j][2])
                dist = pow(float(seeds[i][1]) - float(house_data[j][1]),2) + pow(float(seeds[i][2]) - float(house_data[j][2]),2)
                min_dist.append(dist)
    #        print(min_dist)

            cluster_category = min_dist.index(min(min_dist))
            clusters[cluster_category].append(j)

    updated_seeds = []

    #update seeds as required
    for i in range(k):
            us =[]
            x=0
            y=0
            for j in range(1,len(clusters[i])):
                x+=float(house_data[clusters[i][j]][1])
                y+=float(house_data[clusters[i][j]][2])
            us.append(i)
            us.append((float)(x/j))
            us.append((float)(y/j))
            #print us
            updated_seeds.append(us)
    seeds = updated_seeds

    #print(seeds)
    cnt+=1

#find the closest antenna to the seeds
antennas = []
ant_cat = []
for i in range(k):
    min_ant = []
    for j in range(len(ant_data)):
        dist = pow(float(seeds[i][1]) - float(ant_data[j][1]),2) + pow(float(seeds[i][2]) - float(ant_data[j][2]),2)
        min_ant.append(dist)

    ant_cat = min_ant.index(min(min_ant))
    antennas.append(ant_cat)

#for i in range(k):
#    print(ant_data[antennas[i]][0] + ":" + str(clusters[i][1:]))

#find the farthest house from the antenna in the cluster to decide the type of antenna to be used

finaldist = []

for j in range(len(clusters)):
    maximum = 0
    for i in range(len(clusters[j])):
        c1=[ant_data[antennas[j]][1],ant_data[antennas[j]][2]]
        c2=[house_data[clusters[j][i]][1],house_data[clusters[j][i]][2]]
        dist=(gp.great_circle(c1,c2).feet)
        if(dist>maximum):
            maximum = dist
    finaldist.append(maximum)


final_ant=[]

#make the final list with antenna loc and type
for i in range(len(antennas)):
    ant=[]
    ant.append(ant_data[antennas[i]][0])

    if(finaldist[i]<100):
        type_ant = "T-1"
    elif(finaldist[i]<200):
        type_ant = "T-2"
    elif(finaldist[i]<300):
        type_ant = "T-3"
    elif(finaldist[i]<400):
        type_ant = "T-4"
    else:
        type_ant="T-5"

    ant.append(type_ant)
    final_ant.append(ant)

print(final_ant)
#print(clusters)
#for i in range(0,k):
#    print(clusters[i])

file1 = open('/Users/rajan/Desktop/ant.csv', "w")
line = "AntennaLocationCode,AntennaType \n"

for i in range(len(clusters)):
    line += final_ant[i][0] + "," + final_ant[i][1] + "\n"
file1.write(line)
file1.close()

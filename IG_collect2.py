import requests
import sys
import random
import csv
from operator import itemgetter

keys = []
inFile = open("./keys", "r")
for line in inFile:
    line = line.strip()
    keys.append(line)

access_token = str(keys[0])
client_secret = str(keys[1])

base_url = 'https://api.instagram.com/v1/'

def get_loc_search(lat, lng, distance):
    distance = 10
    request_url = (base_url + 'locations/search?lat=%s&lng=%s&distance=%s&access_token=%s') % (lat, lng, distance, access_token)
    print 'GET REQUEST URL : %s' % (request_url)

    out_data = requests.get(request_url).json()
    product = []
    i = 0

    if out_data['meta']['code'] == 200:
        if len(out_data['data']):
                #here's where most of the magic happens
                try:
                    while i < (len(out_data['data'])+1):
                        i += 1
                        #collecting all the data
                        #product = an individual location
                        product_id = out_data['data'][i]['id'].encode("utf-8")
                            
                        product_lat = out_data['data'][i]['latitude']
                        product_long = out_data['data'][i]['longitude']

                        #tuple the GPS for ease of use later, incase we need to
                        geo_tup= (product_lat, product_long)
                            
                        product_name = out_data['data'][i]['name'].encode("utf-8")

                        temp = []
                        temp.append(product_id)
                        temp.append(product_lat)
                        temp.append(product_long)
                        temp.append(product_name)
                    
                        product.append(temp)

                except:
                    print("Done!")

        else:
            return None

    else:
        print( 'STATUS CODE OTHER THAN 200 RECIEVED!')
        print(out_data['meta']['error_type'])

        quit()

    return(product)

def location_info(location):
  
    loc_id = location[0]
    request_url = (base_url + 'locations/%s/media/recent?access_token=%s') % (loc_id, access_token)
    print 'GET REQUEST URL : %s' % (request_url)
    
    out_data = requests.get(request_url).json()

    if out_data['meta']['code'] == 200:
       # print(out_data['data'][0]['likes']['count'])
        print(out_data['data'])
    else:
        print( 'STATUS CODE OTHER THAN 200 RECIEVED!')
        print(out_data['meta']['error_type'])


def media_location_info(location):
  
    loc_id = location[0]
    loc_lat = location[1]
    loc_lng = location[2]

    request_url = (base_url + 'media/search?lat=%s&lng=%s&distance=100&access_token=%s') % (loc_lat, loc_lng, access_token)
    print 'GET REQUEST URL : %s' % (request_url)
    
    #out_data = requests.get(request_url).json()
    #you'd use below if you weren't sandboxed
    #if out_data['meta']['code'] == 200:

    sandboxed = True
    if sandboxed:
        print("FAKE QUERY")
        #since the app is sandboxed we can only look at
        #this data for self and users within the sandbox (up to 10)
        #print(out_data['data'][0]['likes']['count'])
        
        #so we need to simulate likes for local media.
        seed = random.randint(0, 300)
        seed_min = (seed - random.randint(0,50))
        seed_max = (seed + random.randint(0,50))
        i = 0
        sim_likes = []

        while i <= 25:
            sim_likes.append(random.randint(seed_min, seed_max))
            
            i += 1

        like_avg = sum(sim_likes) / len(sim_likes)
            
        location.append(like_avg)
        return(location)

    else:
        print( 'STATUS CODE OTHER THAN 200 RECIEVED!')
        print(out_data['meta']['error_type'])
    
def main():
    # lat = (input("enter LATITUDE"))
    # lng = (input("enter LONGITUDE"))

    lat = 30.2672
    lng = -97.74131
    distance = 10
    temp_list = (get_loc_search(lat, lng, distance))
    loc_list = []

    #test
    loc_list.append(temp_list[0])

    #need to fix this loop to ignore duplicates
    for x in range(0,30):

        next_lat = temp_list[len(temp_list)-1][1]
        next_lng = temp_list[len(temp_list)-1][2]
        for loc in temp_list:
            #sort
            i = 0
            print("step 0")
            if len(loc_list):
                print("step 1")
                while i < len(loc_list):
                    #below line prints the ID
                    #print(loc_list[i][0])
                    print("step 2")
                    #if new location == location already in list
                    if loc[0] == loc_list[i][0]:
                        #terminate the loop and don't append it to loc_list
                        print("DUPLICATE")
                        break
    
                    if i == len(loc_list)-1:
                        print(loc_list)
                        loc_list.append(loc)

                    i += 1

        temp_list = (get_loc_search(next_lat, next_lng, distance))
   
    finished = []
    print("writing to analysis.csv")
    heading = ['ID', 'LATITUDE', 'LONGITUDE', 'NAME', 'AVG_LIKES']

    with open("analysis.csv", 'w') as endfile:
        out_writer = csv.writer(endfile, delimiter = '|')
        out_writer.writerow(heading)

        for loc in loc_list:
            row = (media_location_info(loc))
            out_writer.writerow(row)
            finished.append(row)

    print(finished)
    
main()

import requests
import sys
import time

keys = []
inFile = open("/home/colin/Desktop/GEO_IG/keys", "r")
for line in inFile:
    line = line.strip()
    keys.append(line)

access_token = str(keys[0])
client_secret = str(keys[1])

base_url = 'https://api.instagram.com/v1/'

def get_loc_search(lat, lng, distance):

    request_url = (base_url + 'locations/search?lat=%s&lng=%s&access_token=%s') % (lat, lng, access_token)
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

    request_url = (base_url + 'media/search?lat=%s&lng=%s&distance=1000&access_token=%s') % (loc_lat, loc_lng, access_token)
    print 'GET REQUEST URL : %s' % (request_url)
    
    out_data = requests.get(request_url).json()

    if out_data['meta']['code'] == 200:
       # print(out_data['data'][0]['likes']['count'])
        print(out_data['data'])
    else:
        print( 'STATUS CODE OTHER THAN 200 RECIEVED!')
        print(out_data['meta']['error_type'])
    
def main():
    # lat = (input("enter LATITUDE"))
    # lng = (input("enter LONGITUDE"))

    lat = 30.2672
    lng = -97.74131
    distance = 1

    loc_list = (get_loc_search(lat, lng, distance))
    
    for loc in loc_list:
        media_location_info(loc)
        break
main()

import requests
import sys

keys = []
inFile = open("/home/colin/Desktop/GEO_IG/keys", "r")
for line in inFile:
    line = line.strip()
    keys.append(line)

access_token = str(keys[0])
client_secret = str(keys[1])

base_url = 'https://api.instagram.com/v1/'

def get_user_id(insta_username):
    request_url = (base_url + 'users/search?q=%s&access_token=%s') % (insta_username, access_token)
    print 'GET REQUEST URL : %s' % (request_url)

    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print( 'STATUS CODE OTHER THAN 200 RECIEVED!')
        print(user_info['meta']['error_type'])

        quit()

#id_var = get_user_id('colin_higgins911')

def get_loc_search(lat, lng):

    request_url = (base_url + 'locations/search?lat=%s&lng=%s&access_token=%s') % (lat, lng, access_token)
    print 'GET REQUEST URL : %s' % (request_url)

    out_data = requests.get(request_url).json()

    if out_data['meta']['code'] == 200:
        if len(out_data['data']):
            return out_data['data'][0]['name']
        else:
            return None

    else:
        print( 'STATUS CODE OTHER THAN 200 RECIEVED!')
        print(out_data['meta']['error_type'])

        quit()

def main():
    # lat = (input("enter LATITUDE"))
    # lng = (input("enter LONGITUDE"))

    lat = 30.2672
    lng = -97.74131

    print(get_loc_search(lat, lng))

main()

import requests 
import datetime
from geopy.geocoders import Nominatim
from random import uniform

# Function to get the latitude and longitude of an address
def get_coordinates(address):
    api_key = "*******************"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url).json()
    lat = response["results"][0]["geometry"]["location"]["lat"]
    lng = response["results"][0]["geometry"]["location"]["lng"]
    return lat, lng

# Random location in bay area
geolocator = Nominatim(user_agent="geoapiExercises")

def get_random_location(bbox):
    location = geolocator.reverse(f"{uniform(bbox[0], bbox[2]):.7f}, {uniform(bbox[1], bbox[3]):.7f}", timeout=10)
    return location

# San Francisco Bay Area bounding box coordinates
#bbox = [37.639097, -123.173825, 38.343068, -121.696143]
#San jose bounding box coordinates
#bbox = [37.2281, -121.9836, 37.4828, -121.6644]
bbox = [37.2281, -121.9836, 37.447516, -121.890449]



random_location = get_random_location(bbox)
print(random_location.raw["lat"], random_location.raw["lon"])

# Example usage

fire_stations = ["5125 Wilson Way, Alviso, CA 95002", "1248 S Blaney Ave, San Jose, CA 95129","6461 Bose Ln, San Jose, CA 95120","2840 The Villages Pkwy, San Jose, CA 95135","98 Martha St, San Jose, CA 95112","3292 Sierra Rd, San Jose, CA 95132","1380 N 10th St, San Jose, CA 95112","511 S Monroe St, San Jose, CA 95128","2001 S King Rd, San Jose, CA 95122","2191 Lincoln Ave, San Jose, CA 95125"]
coordinates = []
for address in fire_stations:
    lat, lng = get_coordinates(address)
    coordinates.append((lat, lng))


lat2 = random_location.raw["lat"]
lng2 = random_location.raw["lon"]
print(f"latitude: {lat}, longitude: {lng}")
print(random_location)
#print(f"latitude: {lat2}, longitude: {lng2}")

# Random location in bay area



def call_ambulance(lat, lng):
    # API key for Google Maps Distance Matrix API
    api_key = "*******************"
    # URL for the API call
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={lat},{lng}&destinations={random_location.raw['lat']},{random_location.raw['lon']}&key={api_key}"
    # Make the API call and get the response
    response = requests.get(url).json()
    # Check if the API returned an error
    if "error_message" in response:
        print("Error: " + response["error_message"])
    elif "rows" not in response or "elements" not in response["rows"][0] or "duration" not in response["rows"][0]["elements"][0]:
        print("Error: Invalid response from API")
    else:
        # Get the estimated travel time from the API response
        duration = response["rows"][0]["elements"][0]["duration"]["value"]
        print("duration:" + str(duration))
        # Calculate the estimated time of arrival
        eta = datetime.datetime.now() + datetime.timedelta(seconds=duration)
        return eta

def find_smallest_eta(coordinates):
    etas = []
    for lat, lng in coordinates:
        etas.append(call_ambulance(lat, lng))
    smallest = etas[0]
    for eta in etas:
        if eta <= smallest:
            smallest = eta
    return smallest

# ????????? ????????? ?????????
def replace_substring(s, old_substring, new_substring):
    return s.replace(old_substring, new_substring)

#coordinates = [(lat, lng), (lat3, lng3), (lat4, lng4)]
smallest_eta = find_smallest_eta(coordinates)
print(smallest_eta)
trans_eta = datetime.datetime.strftime(smallest_eta, '%Y???%m???%d???')
trans_eta2 = datetime.datetime.strftime(smallest_eta, '%H???%M???')
answer = input("?????? ?????? ?????????: " + str(trans_eta) + " " + str(trans_eta2) + " ?????????. ??? ?????? ????????????????????????? ")
now = datetime.datetime.now()
eta_seconds = int((smallest_eta - now).total_seconds())
if answer == 'y':
    print(eta_seconds)
    print("?????? ?????? ?????????: " + str(int(eta_seconds/60)) + "????????????.")
    print("?????? ??????: ", round((abs(eta_seconds)*0.01), 2), " ???????????????.")
if answer == 'n':
    print("?????? ????????? ???????????? ???????????? ??????????????????.")
    print("???????????? ???????????? ???????????????.")
    word = ", San Jose"
    v = 1
    list_address = []
    for i in coordinates:
        faddress = str(geolocator.reverse(i, exactly_one=True))
        index = faddress.find(word)
        cut_string = faddress[:index]
        modified_string = replace_substring(cut_string, "Fire Station", 'DVC')
        list_address.append(cut_string)
        print(str(v)+ ") " + modified_string)
        v = v + 1
    answer2 = input("???????????? ????????? ????????? ??????????????????: ")
    print(str(list_address[int(answer2) - 1]) + " ??? ???????????? ?????????????????????.")
    lat2, lng2 = get_coordinates(fire_stations[int(answer2)])
    opt = call_ambulance(lat2, lng2)
    print(opt)
    opt_eta = datetime.datetime.strftime(opt, '%Y???%m???%d???')
    print(opt_eta)
    opt_eta2 = datetime.datetime.strftime(opt, '%H???%M???')
    print(opt_eta2)
    opt_seconds = int((opt - now).total_seconds())
    answer = print("?????? ?????? ?????????: " + str(opt_eta) + " " + str(opt_eta2) + " ?????????.")
    print("?????? ?????? ?????????: " + str(int(opt_seconds/60)) + "????????????.")
    print("?????? ??????: ", round((abs(opt_seconds)*0.01), 2), " ???????????????.")

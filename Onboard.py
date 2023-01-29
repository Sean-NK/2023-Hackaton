import requests 
import datetime
from geopy.geocoders import Nominatim
from random import uniform


RED = '\033[91m'
GREEN = '\033[92m'
MAGENTA = '\033[95m'
END = '\033[0m'
RED_BG = '\033[101m'
GREEN_BG = '\033[102m'

print("*" * 40)
print("ONBOARD 앱을 실행하셨습니다!  ")
print("*" * 40)


# Function to get the latitude and longitude of an address
def get_coordinates(address):
    api_key = "***********************"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url).json()
    lat = response["results"][0]["geometry"]["location"]["lat"]
    lng = response["results"][0]["geometry"]["location"]["lng"]
    return lat, lng

# Random location in bay area
geolocator = Nominatim(user_agent="geoapiExercises")

# Function to make random location of the accident.
def get_random_location(bbox):
    location = geolocator.reverse(f"{uniform(bbox[0], bbox[2]):.7f}, {uniform(bbox[1], bbox[3]):.7f}", timeout=10)
    return location


#San jose bounding box coordinates
#bbox = [37.2281, -121.9836, 37.4828, -121.6644]
bbox = [37.2281, -121.9836, 37.447516, -121.890449]


# Check the latitude and longtitude of random location.
random_location = get_random_location(bbox)
print(RED + "사고발생지: " + END + str(random_location))

# Just to make sure it is right latitude and longtitude
# print(random_location.raw["lat"], random_location.raw["lon"])

# Getting all the address of our center where are in the San Jose area.
fire_stations = ["5125 Wilson Way, Alviso, CA 95002", "1248 S Blaney Ave, San Jose, CA 95129","6461 Bose Ln, San Jose, CA 95120","2840 The Villages Pkwy, San Jose, CA 95135","98 Martha St, San Jose, CA 95112","3292 Sierra Rd, San Jose, CA 95132","1380 N 10th St, San Jose, CA 95112","511 S Monroe St, San Jose, CA 95128","2001 S King Rd, San Jose, CA 95122","2191 Lincoln Ave, San Jose, CA 95125"]
coordinates = []
for address in fire_stations:
    lat, lng = get_coordinates(address)
    coordinates.append((lat, lng))

# Origin to randomPlace
def otr(lat, lng):
    # API key for Google Maps Distance Matrix API
    api_key = "AIzaSyBhWkYip650cJNOlOWUalhq3IBKitF96HE"
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

        # Debugging
        # print("duration:" + str(duration))


        # Calculate the estimated time of arrival
        eta = datetime.datetime.now() + datetime.timedelta(seconds=duration)
        return eta

def rtd(lat, lng):
    # API key for Google Maps Distance Matrix API
    api_key = "AIzaSyBhWkYip650cJNOlOWUalhq3IBKitF96HE"
    # URL for the API call
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={random_location.raw['lat']},{random_location.raw['lon']}&destinations={lat},{lng}&key={api_key}"
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

        # Debugging
        # print("duration:" + str(duration))


        # Calculate the estimated time of arrival
        eta = datetime.datetime.now() + datetime.timedelta(seconds=duration)
        return eta

def find_smallest_eta(coordinates):
    etas = []
    index = 0
    minindex=0
    for lat, lng in coordinates:
        etas.append(otr(lat, lng))
    smallest = etas[0]
    for eta in etas:
        index = index+1
        if eta <= smallest:
            smallest = eta
            minindex = index
            des = fire_stations[int(minindex-1)]
    return smallest, des


#coordinates = [(lat, lng), (lat3, lng3), (lat4, lng4)]
smallest_eta, des = find_smallest_eta(coordinates)
print(RED + "가장 가까운 ONBOARD 차량 위치: " + END + str(des))
trans_eta = datetime.datetime.strftime(smallest_eta, '%Y년%m월%d일')
trans_eta2 = datetime.datetime.strftime(smallest_eta, '%H시%M분')
print(RED + "예상 도착 시간은: " + END + str(trans_eta) + " " + str(trans_eta2) + " 입니다.")
now = datetime.datetime.now()
eta_seconds = int((smallest_eta - now).total_seconds())
print(RED + "예상 소요 시간은: " + END + str(int(eta_seconds/60)) + "분입니다.")
# print("이용 가격: ", round((abs(eta_seconds)*0.01), 2), " 달러입니다.")

print("*" * 40)
answer = input(MAGENTA + "원하시는 목적지를 입력해주시기 바랍니다: " + END)
dlat, dlng = get_coordinates(answer)
deta = rtd(dlat,dlng)
trans_deta = datetime.datetime.strftime(deta, '%Y년%m월%d일')
trans_deta2 = datetime.datetime.strftime(deta, '%H시%M분')
print(MAGENTA + "원하시는 목적지에 도착하는 예상 시각 :"  + END + str(trans_deta) + " " + str(trans_deta2))

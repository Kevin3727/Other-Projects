import datetime
import googlemaps
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.externals import joblib
import numpy as np
import pickle

api_key = 'AIzaSyBCMFjJGoVWaTZkTbWvLtIifxQ92krQU0E'

gm = googlemaps.Client(key=api_key)

regrLog = joblib.load('../regr/regr_30_log.pkl')

p8Log = pickle.load(open('p8Log.p', 'rb'))
p2Log = pickle.load(open('p2Log.p', 'rb'))

dayOfWeek = {0: 'Monday',
             1: 'Tuesday',
             2: 'Wednesday',
             3: 'Thursday',
             4: 'Friday',
             5: 'Saturday',
             6: 'Sunday'}


def day_time(day, time):
    day_ = dayOfWeek[int(day)]
    time_ = time
    return [day_, time_]


def get_error_log(x):
    """returns log errors of x"""
    return np.where(x < 3.6, p8Log(x), p2Log(x))


def get_location(address='new york'):
    """returns latitude and longitude of the input address"""
    geocode_result = gm.geocode(address)[0]
    lat = geocode_result['geometry']['location']['lat']
    lng = geocode_result['geometry']['location']['lng']
    return [lat, lng]


def get_address(name):
    try:
        addr_ = str(gm.geocode(name)[0]['formatted_address'])
    except:
        addr_ = name
    return addr_


def seconds_to_string(time):
    """returns string of time input (seconds) in d:h:m:s"""
    time = str(datetime.timedelta(seconds=time)).split(':')
    if time[0] == '0':
        time_out = str(time[1]) + ' minutes and ' +\
            str(time[2].split('.')[0]) + ' seconds'
    else:
        time_out = str(time[0]) + ' hours, ' +\
            str(time[1]) + ' minutes and ' +\
            str(time[2].split('.')[0]) + ' seconds'
    return time_out


def get_duration(address_orig, address_dest, day, time_str, txt=False):
    """returns duration of travel and its uncertainty"""
    time = (((int(time_str.split(':')[0]) * 60) + int(time_str.split(':')[1]))) * 60
    pick_up = get_location(address_orig)
    drop_off = get_location(address_dest)
    X = np.array([pick_up[0], pick_up[1],
                  drop_off[0], drop_off[1],
                  time, int(day)])
    y = regrLog.predict(X.reshape(1, -1))[0]
    # y = np.log10(3247.99) # for test
    yerr = get_error_log(y)
    if txt:
        t_up = np.power(10, (y + yerr))
        t_up = seconds_to_string(t_up)
        t_down = np.power(10, (y - yerr))
        t_down = seconds_to_string(t_down)
        t = np.power(10, y)
        t = seconds_to_string(t)
        return [t, t_down, t_up]
    else:
        return [y, yerr]

import random
import datetime

def data_gen(paths):
    startDate = datetime.datetime(2021, 10, 1, 00, 00)
    final_paths = []
    for i in range(1):
        for j in range(1):
            final_paths.extend(data_gen_day(paths, startDate, True))
            startDate += datetime.timedelta(days = 1)
        #for j in range(2):
        #    final_paths.extend(data_gen_day(paths, startDate, False))
        #    startDate += datetime.timedelta(days = 1)

    print(len(final_paths))
    return final_paths

def data_gen_day(paths, startDate, weekday):
    daily_paths = []
    if weekday:
        hourly_paths = week_day_times_gen()
    else:
        hourly_paths = weekend_times_gen()
    cur_hour = startDate
    # for each hour, there is a number of paths generated
    for num in hourly_paths:
        for _ in range(max(num, 1)):
            # generate rando path and add user path to final result
            daily_paths.append(gen_user_path(random.choice(paths), cur_hour))
        cur_hour = cur_hour + datetime.timedelta(hours=1)

    return daily_paths

A = {}
A[0] = 50, 120
A[1] = 50, 70
A[2] = 20, 30
A[3] = 10, 20

A[4] = 10, 100
A[5] = 20, 30
A[6] = 50, 150
A[7] = 200, 400

A[8] = 300, 700
A[9] = 300, 500
A[10] = 300, 500
A[11] = 500, 900

A[12] = 400, 700
A[13] = 400, 700
A[14] = 200, 500
A[15] = 250, 600

A[16] = 200, 400
A[17] = 300, 600
A[18] = 500, 900
A[19] = 500, 800

A[20] = 300, 600
A[21] = 300, 500
A[22] = 200, 300
A[23] = 50, 200

def week_day_times_gen():
    Actual = []

    for hour in A:
        min, max = A[hour]
        Actual.append(random.randrange(min, max))
    
    return Actual

def weekend_times_gen():
    Actual = []

    for hour in A:
        min, max = A[hour]
        Actual.append(random.randrange(min/2, max/2))
    
    return Actual

def gen_user_path(path, start_time):
    result = []

    time = start_time + datetime.timedelta(minutes=random.randrange(60))

    timestamp = 0
    speed, timestep = 100000, 15

    lat_sigma, lon_sigma = 0.0001, 0.0001

    for point in path:
        lat = point["lat"]
        lon = point["lon"]
        if not result:
            result.append({
                "lat": lat, 
                "lon": lon, 
                "time": time,
            })
        else:
            dist = ((lat - result[-1]["lat"]) ** 2 + (lon - result[-1]["lon"]) ** 2) ** 0.5
            timestamp += dist * speed
            if timestamp > timestep:
                timestamp -= timestep
                time += datetime.timedelta(seconds=timestep + random.uniform(-timestep / 4, timestep / 4))
                result.append({
                    "lat": lat + random.gauss(0, lat_sigma),
                    "lon": lon + random.gauss(0, lon_sigma),
                    "time": time,
                })
    return result
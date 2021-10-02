import random
import datetime

def data_gen(paths):
    startDate = datetime.datetime(2021, 9, 1, 00, 00)
    final_paths = []
    for i in range(4):
        for j in range(5):
            final_paths.extend(data_gen_day(paths, startDate, True))
            startDate += datetime.timedelta(days = 1)
        for j in range(2):
            final_paths.extend(data_gen_day(paths, startDate, False))
            startDate += datetime.timedelta(days = 1)
    return final_paths

def data_gen_day(paths, startDate, weekday):
    path_num = len(paths)
    daily_paths = []
    if weekday:
        hourly_paths = week_day_times_gen()
    else:
        hourly_paths = weekend_times_gen()
    cur_hour = startDate
    # for each hour, there is a number of paths generated
    for num in hourly_paths:
        for i in range(num):
            # generate rando path and add user path to final result
            path_rando = paths[random.randrange(path_num)]
            daily_paths.extend(gen_user_path(path_rando, cur_hour))
        cur_hour = cur_hour + datetime.timedelta(hours=1)
    return dailY_paths


def week_day_times_gen():
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

    Actual = []

    for hour in A:
        min, max = A[hour]
        Actual.append(random.randrange(min, max))
    
    return Actual

def weekend_times_gen():
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

    Actual = []

    for hour in A:
        min, max = A[hour]
        Actual.append(random.randrange(min/2, max/2))
    
    return Actual

def gen_user_path(path, start_time):
    result = []
    min_start = random.randrange(60)
    time = start_time + datetime.timedelta(minutes=random.randrange(60))
    time_between_points = 5
    for point in path:
        # Q: what to do, just keep the time, or strech so it fits?
        lat, lon = point
        result.append((lat, lon, time))
        time += datetime.timedelta(seconds = random.randrange(5))
    return result
        
import random
import datetime 

def gen_data(points):
    data_points = list()
    for point in points:
        lat, lon, alt = point
        data_points.extend(gen_data(lat, lon, alt))
    return data_points


def gen_data(lat, lon, alt):
    new_points = list()
    lat_variation = 0.0005
    alt_varation = 10
    startDate = datetime.datetime(2021, 9, 1,13,00)
    times = gen_time_rando(startDate, 1000)
    for time in times:
        new_lat = lat + random.uniform(0, lat_variation) 
        new_lon = lon + random.uniform(0, lat_variation)
        new_alt = alt + random.uniform(0, alt_varation)  
        new_points.append([new_lat, new_lon, new_alt, time])
    return new_points
     
def gen_time_rando(start, length):
   current = start
   res_time = list()
   while length >= 0:
      curr = current + datetime.timedelta(days = random.randrange(30), hours = random.randrange(24), minutes=random.randrange(60))
      res_time.append(curr)
      length-=1



    


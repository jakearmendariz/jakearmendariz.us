'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
convert.py

Just a static class to convert distances for strava calculations

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class Convert():
    @staticmethod
    def to_minutes(time):
        arr = [int(i) for i in time.split(':') if i.isdigit()]
        return arr[0]*60 + arr[1] + float(arr[2])/60
    
    @staticmethod
    def to_hours(time):
        return Convert.to_minutes(time)/60
    
    @staticmethod
    def to_miles(distance):
        return distance/1609.34
    
    @staticmethod
    def get_mph(distance, time):
        if Convert.is_time_str(time):
            time = Convert.to_hours(time)
        if(time == 0):
            return 0
        return round(float(distance)/Convert.seconds_to_hours(time), 2)
    
    @staticmethod
    def seconds_to_hours(seconds: int) -> float:
        return float(seconds)/3600.0
    
    @staticmethod
    def get_pace(distance, time):
        if Convert.is_time_str(time):
            time = Convert.to_minutes(time)
        if(distance == 0):
            return 0
        return float(float(time)/60.0)/distance
    
    @staticmethod
    def is_time_str(time):
        return (not isinstance(time, int) and not isinstance(time, float))
    
    @staticmethod
    def minutes_to_str(minutes):
        seconds = str(round((minutes%1)*60))
        if(len(seconds) == 1 and minutes%1 < 0.16):
            seconds = '0' + seconds
        elif(len(seconds) == 1):
            seconds = seconds + '0'
        return str(int(minutes)) + ':' + seconds
    
    @staticmethod
    def elavation_to_str(elevation):
        return "{:,}".format(elevation)
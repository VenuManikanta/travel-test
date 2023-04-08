import pandas as pd
from datetime import datetime, timedelta



def find_closest_pair(num1, num2):
    df = pd.read_csv('askme/static/clean_airport.csv')
    df = df.copy()
    df.dropna(subset = ['IATA Code','Airport Name'], inplace = True)     # Remove rows with NaN
    # df = df.drop(['IATA Code','Airport Name'], axis=1)

    list1 = df['Latitude Decimal Degrees']
    list2 = df['Longitude Decimal Degrees']
    min_distance = float('inf')
    closest_pair = None
    
    for x, y in zip(list1, list2):
        distance = abs(float(num1) - float(x)) + abs(float(num2) - float(y))
        if distance < min_distance:
            min_distance = distance
            closest_pair = (x, y)
            
    return (df.iloc[list(list1).index(closest_pair[0])]['IATA Code'],df.iloc[list(list1).index(closest_pair[0])]['City/Town'],df.iloc[list(list1).index(closest_pair[0])]['Country'])

def generate_urls(from_iata_code, to_destination):
    df = pd.read_csv('askme/static/clean_airport.csv')
    df = df.copy()
    df.dropna(subset = ['IATA Code','Airport Name'], inplace = True)

    today = datetime.today()
    today_date = str(today.year)+'-'+str(today.month)+'-'+str(today.day)
    tomorrow = today + timedelta(days=1)
    tomorrow_date = str(tomorrow.year)+'-'+str(tomorrow.month)+'-'+str(tomorrow.day)
    hotel = "https://www.expedia.co.in/Hotel-Search?destination={}&selected=&d1={}&startDate={}&d2={}&endDate={}&adults=2".format(str(to_destination), today_date, today_date, tomorrow_date, tomorrow_date)
    a = [i.lower() for i in df['City/Town']]
    if to_destination.lower() in a:
        destiny = df.iloc[a.index(to_destination.lower())]['IATA Code']
    else:
        destiny = to_destination
    departure = str(tomorrow.day)+'/'+str(tomorrow.month)+'/'+str(tomorrow.year)
    flight = "https://www.expedia.co.in/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:{},to:{},departure:{}TANYT&options=cabinclass:economy&fromDate={}&d1={}&passengers=adults:1,infantinlap:N".format(from_iata_code, destiny, departure, departure, tomorrow_date)
    return (hotel, flight)

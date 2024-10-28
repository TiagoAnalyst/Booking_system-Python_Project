import pandas as pd
import numpy as np
import datetime
import requests
from io import StringIO

#----------------------------------------
#URL of the the raw CSV files from GitHub

url="https://raw.githubusercontent.com/TiagoAnalyst/Booking_system_dash-Python_Project/refs/heads/main/Data%20files/Recycling%20centre%20A%20-%20bookings.csv"
url2="https://raw.githubusercontent.com/TiagoAnalyst/Booking_system_dash-Python_Project/refs/heads/main/Data%20files/Recycling%20centre%20A%20-%20max.%20capacity.csv"

# Attempt to fetch the CSV files using requests

try:
    response = requests.get(url, timeout=10) # timeout
    response2 = requests.get(url2, timeout=10) #timeout increased

    url_data = response.content.decode('utf-8')
    url2_data =  response2.content.decode('utf-8')
    
    #Read the CSV data into a DataFrame
    BookingDetails = pd.read_csv(StringIO(url_data))
    BookingCapacity = pd.read_csv(StringIO(url2_data))

except requests.exceptions.RequestException as e:
    print(f"Error fetching the file: {e}")

#----------------------------------------
#Data preparation - Booking main dataset

BookingDetails = (
    BookingDetails
    .rename(
        columns={
            'Mattresses (from your home only)':'Mattresses',
            'Clothes and textiles (mixed)':'clothes and textiles',
            'Site':'Transport type',
        }
    )
    .assign(
        Booking_date = lambda x: pd.to_datetime(x['Booking date/time'], format='%d/%m/%Y  %H:%M').dt.strftime('%d/%m/%Y'),
        Booking_time = lambda y: pd.to_datetime(y['Booking date/time'], format='%d/%m/%Y  %H:%M').dt.strftime('%H:%M'),
        Booking_dayofweek = lambda z: pd.to_datetime(z['Booking_date'], dayfirst=True).dt.day_name(),
        Booking_month = lambda a: pd.to_datetime(a['Booking_date'], dayfirst=True).dt.month_name(),
        Booking_year= lambda b: pd.to_datetime(b['Booking_date'], dayfirst=True).dt.year,
        Booking_month_no = lambda i: pd.to_datetime(i['Booking_date'], format='%d/%m/%Y').dt.month,
        Financial_year = lambda k: k.apply(
            lambda t: f"{t['Booking_year']-1}-{t['Booking_year']}" if t['Booking_month_no']<4 else f"{t['Booking_year']}-{t['Booking_year']+1}",
            axis=1
        )
    )
    .drop(columns=['Booking date/time'])
    .assign(
        **{'Booking created': pd.to_datetime(BookingDetails['Booking created'], format="%d/%m/%Y %H:%M", errors='coerce').dt.date}
    )
    .assign(
        **{
        'Transport type': lambda b: b['Transport type'].apply(lambda b: b[b.find('(')+1:b.find(')')]).str.lower()
        }
    )
)

    # data excluding booking status "cancelled by the customer"

BookingDetails_attendance=BookingDetails[BookingDetails['BookingStatus'].isin(['Completed','No show'])]

#----------------------------------------
#Data preparation - Booking total capacity

BookingCapacity = (
    BookingCapacity
    .assign(
        **{
        'Vehicle type': lambda x: x['Vehicle type'].apply(lambda y: y[y.find('(')+1:y.find(')')]).str.lower()
        }
    )
    .rename(
        columns={
            'Date':'Booking_date'
        }
    )
)

#------------------------------------------
#Data preparation - Booking total capacity vs no. bookings made

BookingCapacity_total=BookingCapacity.groupby('Booking_date')['Number of spaces'].sum().reset_index(name="No. Bookings capacity")

    # merge of both tables - final table

vartemp = BookingDetails_attendance.groupby('Booking_date')['BookingStatus'].count().reset_index(name="No. Bookings made")

BookingsDetails_Capacity = pd.merge(
    BookingCapacity_total,
    vartemp, 
    left_on=None)

BookingsDetails_Capacity = (
    BookingsDetails_Capacity
        .assign(
            Booking_month = lambda a: pd.to_datetime(a['Booking_date'], dayfirst=True).dt.month_name(),
            Booking_year= lambda b: pd.to_datetime(b['Booking_date'], dayfirst=True).dt.year,
            Booking_month_no = lambda i: pd.to_datetime(i['Booking_date'], format='%d/%m/%Y').dt.month,
            Financial_year = lambda y:y.apply(
                lambda t: f"{t['Booking_year']-1}-{t['Booking_year']}" if t['Booking_month_no']<4 else f"{t['Booking_year']}-{t['Booking_year']+1}",
            axis=1
            )
        )
)

#------------------------------------------
#Dropdown list

dropdown_list_month =  BookingDetails['Booking_month'].unique()
dropdown_list_fy = BookingDetails['Financial_year'].unique()
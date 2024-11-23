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
    booking_details = pd.read_csv(StringIO(url_data))
    booking_capacity = pd.read_csv(StringIO(url2_data))

except requests.exceptions.RequestException as e:
    print(f"Error fetching the file: {e}")

#----------------------------------------
#Data preparation - Booking main dataset

booking_details = (
    booking_details
    .rename(
        columns={
            'Mattresses (from your home only)':'Mattresses',
            'Clothes and textiles (mixed)':'Clothes and textiles',
            'Site':'transport type',
            'Wooden furniture (whole or dismantled)':'Wooden furniture',
            'Batteries (car & household)':'Batteries',
            'Large domestic appliances (e.g. washing machines)':'Large domestic appliances',
            'Gas bottles (small)':'Gas bottles',
            'Tyres (maximum 2)':'Tyres',
            'Plastics (bottles/pots/tubs/trays)':'Plastics - recyclables',
            'Non-recyclables (black bin)':'Non-recyclables',
            'Plastics (other)':'Plastics - Non recyclable',
            'Paint (and dry empty metal paint cans)':'Paint',
            'Garden wood (decking/fencing/shed)':'Garden wood',
            'Wooden flooring (including laminate)':'Wooden flooring',
            'Asbestos (needs to be double wrapped)':'Asbestos',
            'Kitchen and bathroom fixtures and fixings':'Kitchen and bathroom fixtures',
            'Garden cuttings and prunings':'Green waste'
        }
    )
    .assign(
        **{
            'Booking date/time': pd.to_datetime(booking_details['Booking date/time'], format="%d/%m/%Y %H:%M", errors='coerce'),
            'transport type': lambda b: b['transport type'].apply(lambda b: b[b.find('(')+1:b.find(')')]).str.lower(),
            'booking_date': lambda b: b['Booking date/time'].dt.strftime('%d/%m/%Y'),
            'booking_time': lambda b: b['Booking date/time'].dt.strftime('%H:%M'),
            'booking_dayofweek': lambda z: z['Booking date/time'].dt.day_name(),
            'booking_month': lambda a: a['Booking date/time'].dt.month_name(),
            'booking_year': lambda b: b['Booking date/time'].dt.year,
            'booking_month_no': lambda i: i['Booking date/time'].dt.month,
            'financial_year': lambda k: k.apply(
                lambda t:f"{t['booking_year']-1}-{t['booking_year']}" if t['booking_month_no']<4 else f"{t['booking_year']}-{t['booking_year']+1}",
                axis=1
            )
        }
    )
)

    # data excluding booking status "cancelled by the customer"



#----------------------------------------
#Data preparation - Booking total capacity

booking_capacity = (
    booking_capacity
    .rename(
        columns={
            'Date':'booking_date'
        }
    )
    .assign(
        **{
        'Vehicle_type': lambda x: x['Vehicle type'].apply(lambda y: y[y.find('(')+1:y.find(')')]).str.lower()
        }
    )
)

booking_capacity_total=booking_capacity.groupby('booking_date')['Number of spaces'].sum().reset_index(name="No. Bookings capacity")

#------------------------------------------
#Data preparation - Booking total capacity vs no. bookings made

bookings_details_summary = booking_details[booking_details['BookingStatus'].isin(['Completed','No show'])].groupby('booking_date')['BookingStatus'].count().reset_index(name="No. Bookings made")

bookings_details_capacity = pd.merge(
    booking_capacity_total,
    bookings_details_summary, 
    left_on=None
)

bookings_details_capacity = (
    bookings_details_capacity
        .assign(
            booking_date = lambda a: pd.to_datetime(a['booking_date'], dayfirst=True),
            booking_month = lambda a: a['booking_date'].dt.month_name(),
            booking_year= lambda b: b['booking_date'].dt.year,
            booking_dayofweek = lambda z: z['booking_date'].dt.day_name(),
            booking_month_no = lambda i: i['booking_date'].dt.month,
            financial_year = lambda y:y.apply(
                lambda t: f"{t['booking_year']-1}-{t['booking_year']}" if t['booking_month_no']<4 else f"{t['booking_year']}-{t['booking_year']+1}",
            axis=1
            )
        )
)

#------------------------------------------
#Dropdown list

dropdown_list_month =  ['January','February','March','April','May','June','July','August','September','October','November','December']
dropdown_list_fy = booking_details['financial_year'].unique()

#-------------------------------------------
#Other lists 

ordered_weekday = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
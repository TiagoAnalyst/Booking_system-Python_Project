import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from Data_prep import BookingsDetails_Capacity, BookingDetails, BookingDetails_attendance

def bookingsVScapacity(slct_fy,slct_month):

    BookingsDetails_Capacity_filt = BookingsDetails_Capacity.loc[(BookingsDetails_Capacity['Financial_year'] == slct_fy) & (BookingsDetails_Capacity['Booking_month'] == slct_month)]
    BookingsDetails_Capacity_filt.loc[:,'Booking_date'] = pd.to_datetime(BookingsDetails_Capacity_filt['Booking_date'],format='%d/%m/%Y', dayfirst=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=BookingsDetails_Capacity_filt['Booking_date'],
            y=BookingsDetails_Capacity_filt['No. Bookings made'],
            name='No. of bookings',
            marker_color = 'cornflowerblue'
        ),secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=BookingsDetails_Capacity_filt['Booking_date'],
            y=BookingsDetails_Capacity_filt['No. Bookings capacity'],
            name='Daily capacity',
            ),
        secondary_y=True
    )

    fig.update_xaxes(title_text="Day of month")\
        .update_yaxes(title_text="<b>Bookings capacity</b>", secondary_y=False)\
        .update_yaxes(range = [0,400])\
        .update_xaxes(
            tickformat='%d',
            tickmode='array',
            tickvals=BookingsDetails_Capacity_filt['Booking_date'])\
        .update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1),
            paper_bgcolor='#343a40',
            plot_bgcolor='#343a40',
            font_color='white',
            title={
                'text': "Number of bookings made vs bookings capacity",
                'font': dict(size=25),
                'yref':'paper'
            }
        )
    return fig

def booking_classification(slct_fy,slct_month):

    bookings_classification = BookingDetails[(BookingDetails['Financial_year']==slct_fy) & (BookingDetails['Booking_month'] == slct_month)]['BookingStatus'].value_counts().reset_index()
    bookings_classification.columns=['BookingStatus','Count']
        
    fig =px.pie(
        bookings_classification, 
        names = 'BookingStatus',
        values='Count',
        hole =.4,
        color_discrete_sequence=px.colors.sequential.Brwnyl
        )
    
    fig.update_layout(
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=1,
            xanchor="center",
            x=1,
        ),
        font_color='white',
        title={
            'text': 'Booking Status distribution',
            'font': dict(size=25),
            'yref': 'paper'
        }
    )
    
    return fig

def gauge_chart(slct_fy, slct_month):

    BookingsDetails_Capacity_filt = BookingsDetails_Capacity.query(f"Financial_year=='{slct_fy}' & Booking_month == '{slct_month}'")

    Gauge_chart = (BookingsDetails_Capacity_filt['No. Bookings made'].sum()/BookingsDetails_Capacity_filt['No. Bookings capacity'].sum())*100

    fig = go.Figure(
            go.Indicator(
                mode= "gauge+number",
                value=Gauge_chart,
                number = {'suffix':"%"},
                domain={'x':[0,1],'y':[0,1]},
                gauge ={'axis': {'range': [0,100]},
                        'bar':{'color':'lightgrey'},
                        'steps':[
                            {'range':[0,80],'color':'rgba(50, 205, 50, 0.2)'},
                            {'range':[80,90],'color':'rgba(255, 255, 0, 0.2)'},
                            {'range':[90,100],'color':'rgba(250, 128, 114, 0.2)'}
                        ]
                }
            )
    )

    fig.update_layout(
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white',
        
        title={
            'text':"Bookings capacity usage",
            'font': dict(size=25),
            'yref': 'paper'
        }
    )
    
    return fig

def average_bookings_week(slct_fy, slct_month):

    Ordered_weekday = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    BookingDetails_filtered = BookingDetails_attendance.loc[(BookingDetails['Financial_year']==slct_fy) & (BookingDetails['Booking_month'] == slct_month)]
    
    # Table with average number of bookings per week day 
    Bookings_dayofweek_list=[]
    
    for i in Ordered_weekday:
        var_temp = BookingDetails_filtered.loc[(BookingDetails_filtered['Booking_dayofweek']==i)].copy()
        if not var_temp.empty:
            var_temp2 = var_temp['BookingStatus'].count()/var_temp['Booking_date'].nunique()
        else:
            var_temp2=0

        Bookings_dayofweek_list.append({'Booking_dayofweek':i,'Avg_bookings': var_temp2})

    Bookings_dayofweek_table = pd.DataFrame(Bookings_dayofweek_list)

        #determine the day with the highest average
    max_avg_booking_day = Bookings_dayofweek_table.loc[Bookings_dayofweek_table['Avg_bookings'].idxmax(),'Booking_dayofweek']

        # chart colors
    colors=['cornflowerblue']*len(Bookings_dayofweek_table)
    max_day_index = Bookings_dayofweek_table.index[Bookings_dayofweek_table['Booking_dayofweek']== max_avg_booking_day].tolist()[0]
    colors[max_day_index] = 'navy'

    
    # chart 
       
    # chart colours
    name_short = lambda x: x[:3]
    Weekday_short = [name_short(day) for day in Ordered_weekday]
    
    fig = go.Figure(
        go.Bar(
            x=Weekday_short,
            y=Bookings_dayofweek_table['Avg_bookings'],
            marker_color = colors
        )
    )

    fig.update_layout(
        title ={
             'text':'Average no. of bookings per day of week',
             'font': dict(size=25),
             'yref':'paper'
        },
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig 
  

def most_visitors_month(slct_fy, slct_month):
    most_visitors_data = BookingDetails_attendance.loc[(BookingDetails['Financial_year']==slct_fy) & (BookingDetails['Booking_month'] == slct_month)]
    most_visitors = most_visitors_data['Registration plate'].value_counts().reset_index().head(10)
    most_visitors.columns=['Registration plate','No. of visits']

    fig = go.Figure(
        data=[go.Table(
            header=dict(
                values=list(most_visitors.columns),
                fill_color='#343a40',
                align='left'),
            cells=dict(
                values=[most_visitors['Registration plate'],most_visitors['No. of visits']],
                fill_color='#343a40',
                align='left')
        )]
    )

    fig.update_layout(
        title ={
             'text':'Number of visits by Vehicle Reg.',
             'font': dict(size=25),
             'yref':'paper'
        },
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def evolution_bookings(slct_fy):

    Month_ordered=['Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar']

    BookingsDetails_Capacity_filt = BookingsDetails_Capacity.loc[BookingsDetails_Capacity['Financial_year'] == slct_fy]

    BookingsDetails_Capacity_filt=BookingsDetails_Capacity_filt.groupby('Booking_month')[['No. Bookings made','No. Bookings capacity']].sum().reset_index()

    BookingsDetails_Capacity_filt['Monthly usage']=((BookingsDetails_Capacity_filt['No. Bookings made']/BookingsDetails_Capacity_filt['No. Bookings capacity'])*100).round(2)

    name_short = lambda x: x[:3]
    month_short = [name_short(month) for month in Month_ordered]

    fig = go.Figure(
        go.Scatter(
            x=month_short,
            y= BookingsDetails_Capacity_filt['Monthly usage'],
            name='Capacity usage',
            marker_color = 'black'
        )
    )
    
    colors = ['limegreen','yellow','salmon']
    shapes = []
    intervals = [[0,60],[60,80],[80,100]]

    for a,b in enumerate(intervals):
        shapes.append(dict(type="rect",
                           xref="paper",
                           yref="y",
                           x0=0,
                           y0=b[0],
                           x1=1,
                           y1=b[1],
                           fillcolor=colors[a],
                           opacity=0.1,
                           layer="below",
                           line_width=0))

    fig.update_xaxes(title_text="Financial year")\
        .update_yaxes(title_text="Percentage (%)")\
        .update_yaxes(range = [0,100])\
        .update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            paper_bgcolor='#343a40',
            font_color='white',
            title={
                'text': "Evolution of booking capacity usage",
                'font': dict(size=25),
                'yref':'paper'
            },
            shapes=shapes
        )
    return fig

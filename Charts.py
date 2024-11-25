import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from Data_prep import bookings_details_capacity, booking_details, booking_capacity

# functions - variables/tables

def bookings_details_capacity_filt(slct_fy,slct_month):

    filtered_data = bookings_details_capacity.loc[(bookings_details_capacity['financial_year'] == slct_fy) & (bookings_details_capacity['booking_month'] == slct_month)]

    return filtered_data

def bookings_details_attendance(slct_fy,slct_month):

    booking_details_filt=booking_details[(booking_details['BookingStatus'].isin(['Completed','No show'])) & (booking_details['financial_year'] == slct_fy) & (booking_details['booking_month'] == slct_month)]

    return booking_details_filt

def recycling_materials():

    Recyclables_material = [
            'Batteries', 
            'Books',
            'Clothes and textiles', 
            'Cooking oil', 
            'Engine oil',
            'Fluorescent tubes', 
            'Fridges and freezers',
            'Green waste', 
            'Gas bottles', 
            'Glass bottles and jars',
            'Hazardous household chemicals', 
            'Large domestic appliances',
            'Mattresses', 
            'Paper and cardboard',
            'Plastics - recyclables',
            'Scrap metal',
            'Small electrical appliances', 
            'Toner cartridges', 
            'TVs and monitors',
            'Tyres', 
            'Wooden furniture', 
        ]
    
    return Recyclables_material

def non_recycling_materials():

    non_recyclables_materials = [
            'Bulky non-recyclables', 
            'Carpet and lino',
            'Plastics - Non recyclable',
            'Non-recyclables', 
            'Paint'
        ]
    return non_recyclables_materials

def DIY_material():

    diy_material_list = [
            'Asbestos', 
            'Garden wood',
            'Kitchen and bathroom fixtures', 
            'Plasterboard', 
            'Soil and turf',
            'Wooden flooring'
        ]
    return diy_material_list

def materials_brought_table_recycling(slct_fy,slct_month):

    All_materials_summary = materials_brought_table(slct_fy,slct_month)

    Recyclables_material = All_materials_summary[recycling_materials()]

    return Recyclables_material

def materials_brought_table_non_recyclables(slct_fy,slct_month):

    All_materials_summary = materials_brought_table(slct_fy,slct_month)

    Non_recyclables_material = All_materials_summary[non_recycling_materials()]

    return Non_recyclables_material

def materials_brought_table_DIY(slct_fy,slct_month):

    All_materials_summary = materials_brought_table(slct_fy,slct_month)

    DIY_material_list = All_materials_summary[DIY_material()]

    return DIY_material_list

def month_order():

    month_ordered =[
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]

    return month_ordered

# functions - charts(fy,month)

def bookingsVScapacity(slct_fy,slct_month):

    filtered_data = bookings_details_capacity_filt(slct_fy,slct_month)

    filtered_data.loc[:,'booking_date'] = pd.to_datetime(filtered_data['booking_date'],format='%d/%m/%Y', dayfirst=True)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=filtered_data['booking_date'],
            y=filtered_data['No. Bookings made'],
            name='No. of bookings',
            marker_color = 'cornflowerblue'
        ),secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=filtered_data['booking_date'],
            y=filtered_data['No. Bookings capacity'],
            name='Daily capacity',
            ),
        secondary_y=True
    )

    fig.update_yaxes(
            title_text="No. of bookings",
            autorange = False,
            secondary_y=False,
            range = [0,410],
            dtick=50
        )\
        .update_xaxes(
            title_text="Day of month",
            tickformat='%d',
            tickmode='array',
            tickvals=filtered_data['booking_date']
        )\
        .update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            paper_bgcolor='#343a40',
            plot_bgcolor='#343a40',
            font_color='white',
            title={
                'text': "Number of bookings made vs bookings capacity",
                'font': dict(size=25),
                'yref':'paper'
            }
        )\
        .update_yaxes(
            secondary_y=True,
            range = [0,410],
            showticklabels = False
        )
    
    return fig

def booking_classification(slct_fy,slct_month):

    bookings_classification = (booking_details[(booking_details['financial_year'] == slct_fy) &
                                               (booking_details['booking_month'] == slct_month)]['BookingStatus']
                                               .value_counts().reset_index())
    
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
    )\
    .update_traces(
        texttemplate='%{percent:.1%}'
    )
    
    return fig

def gauge_chart(slct_fy, slct_month):

    filtered_data = bookings_details_capacity_filt(slct_fy,slct_month)

    Gauge_chart = (filtered_data['No. Bookings made'].sum()/filtered_data['No. Bookings capacity'].sum())*100

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
            'text':"Booking system capacity usage",
            'font': dict(size=25),
            'yref': 'paper'
        }
    )
    
    return fig

def average_bookings_week(slct_fy, slct_month):

    ordered_weekday = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    booking_details_attendance = bookings_details_attendance(slct_fy,slct_month)
    
    # Table with average number of bookings per week day 
    Bookings_dayofweek_list=[]
    
    for i in ordered_weekday:
        data_weekday = booking_details_attendance.loc[(booking_details_attendance['booking_dayofweek']==i)].copy()
        if not data_weekday.empty:
            data_per_weekday = data_weekday['BookingStatus'].count()/data_weekday['booking_date'].nunique()
        else:
            data_per_weekday=0

        Bookings_dayofweek_list.append({'booking_dayofweek':i,'avg_bookings': data_per_weekday})

    Bookings_dayofweek_table = pd.DataFrame(Bookings_dayofweek_list)

        #determine the day with the highest average
    max_avg_booking_day = Bookings_dayofweek_table.loc[Bookings_dayofweek_table['avg_bookings'].idxmax(),'booking_dayofweek']

        # chart colors

    colors=['cornflowerblue']*len(Bookings_dayofweek_table)
    max_day_index = Bookings_dayofweek_table.index[Bookings_dayofweek_table['booking_dayofweek']== max_avg_booking_day].tolist()[0]
    colors[max_day_index] = 'navy'

    
    # chart 
       
    # chart colours
    name_short = lambda x: x[:3]
    Weekday_short = [name_short(day) for day in ordered_weekday]
    
    fig = go.Figure(
        go.Bar(
            x=Weekday_short,
            y=Bookings_dayofweek_table['avg_bookings'],
            marker_color = colors
        )
    )

    fig.update_layout(
            title ={
                'text':'Average no. bookings per day of week',
                'font': dict(size=25),
                'yref':'paper'
            },
            paper_bgcolor='#343a40',
            plot_bgcolor='#343a40',
            font_color='white'
        )\
        .update_yaxes(
            title_text="No. of Bookings", 
            range = [0,360]
        )\
        .update_xaxes(
        title_text="Day of Week"
        )

    return fig
  
def most_visitors_month(slct_fy, slct_month):


    most_visitors_data = bookings_details_attendance(slct_fy,slct_month)
    most_visitors = most_visitors_data['Registration plate'].value_counts().reset_index().head(10)
    most_visitors.columns=['Registration plate','No. of visits']

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(most_visitors.columns),
                    fill_color='#a5a6a9',
                    align='center',
                    font=dict(
                        color='black',
                        size=20
                    )
                ),
                cells=dict(
                    values=[
                        most_visitors['Registration plate'],
                        most_visitors['No. of visits']
                    ],
                    fill_color='#f2f2f2',
                    align='center',
                    font=dict(
                        color='black'
                    )
                )
            )
        ]
    )

    fig.update_layout(
        title ={
             'text':'Top 10 most frequent visitors by vehicle veg.',
             'font': dict(size=25),
             'yref':'paper'
        },
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def busiest_times_per_dayofweek(slct_fy,slct_month):

    ordered_weekday = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    BookingDetails_filtered = bookings_details_attendance(slct_fy,slct_month)

    BookingCapacity_filtered = bookings_details_capacity_filt(slct_fy,slct_month)

    Number_of_timeslots = len(booking_details['booking_time'].unique())

    # average number of bookings per week day 
    Average_weekday_capacity = pd.DataFrame(BookingCapacity_filtered.groupby('booking_dayofweek')['No. Bookings capacity'].mean())

    # average timeslot capacity per week day
    Average_timeslot_capacity = Average_weekday_capacity.div(Number_of_timeslots, axis = 0)


    timeslots_weekday = pd.crosstab(BookingDetails_filtered['booking_dayofweek'], BookingDetails_filtered['booking_time'])

    Count_weekdays = BookingDetails_filtered[['booking_dayofweek','booking_date']].drop_duplicates('booking_date').value_counts('booking_dayofweek')

    average_timeslots_weekday = timeslots_weekday.div(Count_weekdays, axis = 0)

    Average_timeslot_usage = (average_timeslots_weekday.div(Average_timeslot_capacity['No. Bookings capacity'], axis = 0).round(3)*100)

    Average_timeslot_usage.index.name=None

    Average_timeslot_usage_reformat = Average_timeslot_usage.T.sort_values('booking_time', ascending=False)

    available_columns = [col for col in ordered_weekday if col in Average_timeslot_usage_reformat.columns]

    Average_timeslot_usage_reformat = Average_timeslot_usage_reformat[available_columns]

    Average_timeslot_usage_reformat.columns = Average_timeslot_usage_reformat.columns.astype(str).str[:3]

    fig = px.imshow(
        Average_timeslot_usage_reformat, 
        color_continuous_scale='tealrose',
        aspect='auto'
        )

    num_rows, num_cols = Average_timeslot_usage_reformat.shape

    # Add vertical gridlines
    for col in range(1, num_cols):
        fig.add_shape(
            type="line",
            x0=col - 0.5, x1=col - 0.5,
            y0=-0.5, y1=num_rows - 0.5,
            line=dict(color="white", width=1)
    )

    # Add horizontal gridlines
    for row in range(1, num_rows):
        fig.add_shape(
            type="line",
            x0=-0.5, x1=num_cols - 0.5,
            y0=row - 0.5, y1=row - 0.5,
            line=dict(color="white", width=1)
    )

    fig.update_xaxes(
        tickangle=0,
        title_text= 'Week day',
        showgrid=True,
        gridcolor = 'white'
        )\
        .update_yaxes(
        title_text='Booking timeslots',
        showgrid=True,
        gridcolor = 'white'
        )

    fig.update_layout(
        title ={ 
            'text':'Timeslots capacity usage per day of week',
            'font': dict(size=25),
            'yref':'paper'
        },
        paper_bgcolor='#343a40',
        font_color='white',
        width = 800,
        height = 450,
        margin = dict(
            l=20,
            r=20,
            t=100,
            b=80
        ),
        xaxis=dict(showgrid=True, gridcolor='white'),  # Gridlines for x-axis
        yaxis=dict(showgrid=True, gridcolor='white')   # Gridlines for y-axis
        )\
        .update_coloraxes(colorbar=dict(
            tickvals=[20,40,60,80,100],
            ticktext=['20%','40%','60%','80%','100%']
        ))

    return fig

def materials_brought_table(slct_fy,slct_month):

    booking_details_filt = bookings_details_attendance(slct_fy,slct_month)
    All_materials = booking_details_filt.iloc[:,5:37]
    All_materials = All_materials.replace('No','N')

    All_materials_summary = {}

    for col in All_materials.columns:
        column_summary = All_materials[col].value_counts()
        All_materials_summary[col]= column_summary

    All_materials_summary = pd.DataFrame(All_materials_summary, index=['Y'])

    return All_materials_summary

def materials_brought_summary(slct_fy,slct_month):

    materials_recycling = materials_brought_table_recycling(slct_fy,slct_month).values.sum()
    materials_non_recyclables = materials_brought_table_non_recyclables(slct_fy,slct_month).values.sum()
    materials_DIY = materials_brought_table_DIY(slct_fy,slct_month).values.sum()

    summary ={'Recycling':materials_recycling,'Non recyclables':materials_non_recyclables,'DIY waste': materials_DIY}

    materials_summary = pd.DataFrame(data=summary, index = [0])

    fig =px.pie(
        names = materials_summary.columns,
        values=materials_summary.iloc[0,:],
        hole =.4,
        color_discrete_sequence=['darkgreen','lightgrey','darkorange']
        )
    
    fig.update_layout(
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="center",
            x=1,
        ),
        font_color='white',
        title={
            'text': 'Waste brought by composition',
            'font': dict(size=25),
            'yref': 'paper'
        },
        margin = dict(
            l=20,
            r=20,
            t=100,
            b=80
        )
    )

    return fig

def materials_brought_recycling_cat(slct_fy,slct_month):

    Recyclables_material = materials_brought_table_recycling(slct_fy,slct_month)

    Recyclables_material = Recyclables_material.iloc[-1,:].sort_values(ascending=True).tail(10)

    fig = go.Figure(
        go.Bar(
            x=Recyclables_material,
            y=Recyclables_material.index,
            orientation= "h",
            marker_color = 'darkgreen'
        )
    )

    fig.update_xaxes(
            range = [0,2510]
        )

    fig.update_layout(
        title ={
             'text':'Most recyclable waste brought (Top 10)',
             'font': dict(size=25),
             'yref':'paper'
        },
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )
    
    return fig

def materials_brought_non_recyclables_cat(slct_fy,slct_month):

    Non_recyclables_material = materials_brought_table_non_recyclables(slct_fy,slct_month)

    Non_recyclables_material = Non_recyclables_material.iloc[-1,:].sort_values(ascending=True)

    fig = go.Figure(
        go.Bar(
            x=Non_recyclables_material,
            y=Non_recyclables_material.index,
            orientation= "h",
            marker_color ='lightgrey'
        )
    )

    fig.update_xaxes(
        range = [0,2510]
    )

    fig.update_layout(
        title ={
             'text':'Most non-recyclable waste brought',
             'font': dict(size=25),
             'yref':'paper'
        },
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )
    
    return fig

def materials_brought_DIY_cat(slct_fy,slct_month):

    materials_brought_DIY_cat = materials_brought_table_DIY(slct_fy,slct_month)

    materials_brought_DIY_cat = materials_brought_DIY_cat.iloc[-1,:].sort_values(ascending=True)

    fig = go.Figure(
        go.Bar(
            x=materials_brought_DIY_cat,
            y=materials_brought_DIY_cat.index,
            orientation= "h",
            marker_color = 'darkorange'
        )
    )

    fig.update_xaxes(
        range = [0,2510]
    )

    fig.update_layout(
        title ={
             'text':'Most DIY waste brought',
             'font': dict(size=25),
             'yref':'paper'
        },
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )
    
    return fig


# functions - charts(fy)

def evolution_bookings(slct_fy):

    slct_fy='2021-2022'

    month_ordered = month_order()

    bookings_details_capacity_filt = bookings_details_capacity.loc[bookings_details_capacity['financial_year'] == slct_fy]

    bookings_details_capacity_filt=bookings_details_capacity_filt.groupby('booking_month')[['No. Bookings made','No. Bookings capacity']].sum().reset_index()

    bookings_details_capacity_filt = (
        bookings_details_capacity_filt
        .assign(
            **{
                'monthly_usage': lambda x: (x['No. Bookings made']/x['No. Bookings capacity']*100).round(2),
                'booking_month': lambda i: pd.Categorical(i['booking_month'], categories=month_ordered,ordered=True)
            }
        )
    )

    bookings_details_capacity_filt = bookings_details_capacity_filt.sort_values('booking_month')

    month_short = bookings_details_capacity_filt['booking_month'].astype(str).str[0:3]

    fig = go.Figure(
        go.Scatter(
            x=month_short,
            y= bookings_details_capacity_filt['monthly_usage'],
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
                            opacity=0.4,
                            layer="below",
                            line_width=0))

    fig.update_xaxes(
        title_text="Month"
        )\
        .update_yaxes(
            title_text="Usage level (%)",
            range = [0,100]
        )\
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
                'text': "Evolution of booking system capacity usage",
                'font': dict(size=25),
                'yref':'paper'
            },
            shapes=shapes
        )
    
    return fig

def materials_category_fy(slct_fy):

    booking_details_filt=booking_details[
        (booking_details['BookingStatus'].isin(['Completed','No show'])) & 
        (booking_details['financial_year'] == slct_fy)]

    all_columns_need = recycling_materials() + non_recycling_materials() + DIY_material() + ['booking_month']

    All_materials = booking_details_filt[all_columns_need].replace('No','N').set_index('booking_month')

    materials_monthly_summary = All_materials.groupby('booking_month').apply(lambda x: (x == 'Y').sum())
    materials_monthly_summary_ordered_ = materials_monthly_summary.sum().sort_values(ascending=False).index

    materials_monthly_summary = materials_monthly_summary[materials_monthly_summary_ordered_]

    materials_monthly_summary_row_pct = materials_monthly_summary.div(materials_monthly_summary.sum(axis=1), axis=0) * 100

    Month_ordered= month_order() 

    materials_monthly_summary_row_pct_filt = (
        materials_monthly_summary_row_pct
        .iloc[:,:10]
        .reset_index()
        .assign(
            booking_month = lambda i: pd.Categorical(
                i['booking_month'], categories=Month_ordered, ordered=True)
            )
        .sort_values('booking_month')
    )       

    month_short = materials_monthly_summary_row_pct_filt['booking_month'].astype(str).str[:3]

    materials_table = materials_monthly_summary_row_pct_filt.iloc[:,1:]

    fig = go.Figure()

    for material in materials_table.columns:
            fig.add_trace(
                go.Scatter(
                    x=month_short,
                    y=materials_table[material],
                    mode = 'lines+markers',
                    name = material
                )
            )

    fig.update_layout(
        xaxis_title="Month",
        legend_title="materials",
        paper_bgcolor='#343a40',
            plot_bgcolor='#a5a6a9',
            font_color='white',
            title={
                'text': "Top 10 materials most disposed by residents",
                'font': dict(size=25),
                'yref':'paper'
            }
        )\
        .update_yaxes(
            title_text="Percentage (%)",
            range = [0,15]
        )\
        .update_xaxes(
            showgrid=False
        )

    return fig
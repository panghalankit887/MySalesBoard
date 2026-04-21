import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px


# Style Part
st.markdown("""
<style>
.nav-item {
    display: flex;
    align-items: center;
    justify-content : center;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    padding: 8px 8px;
    margin-bottom: 10px;
    cursor: pointer;
    background: white;
    transition: all 0.3s ease;
    width :  80px;
}
.nav-item:hover {
    background: #fff5f5;
    border-color: #ff6b6b;
    transform: scale(1.03);
}
.nav-item.active {
    background: #ff6b6b;
    border-color: #ff6b6b;
    box-shadow: 0 4px 10px rgba(255,107,107,0.3);
}
.nav-item img {
    width: 40px;
    height: 40px;
    border-radius: 6px;
}

.nav-arrow {
    font-size: 18px;
    color: #333;
    font-weight: bold;
}
            

div[data-testid="stButton"] > button {
    padding : 15px 15px ;
}

</style>
""", unsafe_allow_html=True)




# Importing the csv file

df =pd.read_csv("cake_sales_data.csv", parse_dates=["Order_Date"])
df["Month"] = df["Order_Date"].dt.strftime("%B")



# Calculatng the required data 
total_sale =  df["Sales_Amount"].sum()
total_profit = df["Profit"].sum()
total_order = df["Order_ID"].unique()
total_order_count= df["Order_ID"].count()
average_discount = df["Discount"].mean()


sale_over_time =  df.groupby('Order_Date')['Sales_Amount'].sum().reset_index()
region_stats  = df.groupby("Region").agg({
    'Sales_Amount': 'sum',
    'Profit': 'sum',
    'Order_ID' : 'count'
}).reset_index()

region_stats = region_stats.rename(columns={"Order_ID": 'Order_Count'})
region_stats = region_stats.sort_values("Sales_Amount", ascending= False)


revenue_by_flabor =  df.groupby("Product_Name")["Sales_Amount"].sum().reset_index()
revenue_by_flabor = revenue_by_flabor.sort_values('Sales_Amount', ascending=False)



sales_by_category = df.groupby("Product_Name")["Sales_Amount"].sum().reset_index()
sales_by_category = sales_by_category.sort_values("Sales_Amount", ascending=False)


#  Filling  the Important data 
st.set_page_config(
    page_title="Cake Sales Dashboard",
    page_icon="media/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "https://www.google.com/",
        'Report a bug': None,
        'About': """
# 🎂 Cake Sales Pro
        
**Version:** 2.1.0  
**Built with:** Streamlit, Plotly, Pandas  
**Data Source:** Internal Sales Database
> Made BY :rainbow[Ravi]

*For  Prcatice use  only*
        """
    
    }
)




# Sidebar Navigation
st.sidebar.markdown(">### Menu")

if 'current_page' not in st.session_state:
    st.session_state.current_page = "dashboard"
nav_options = [
    {"icon": "https://static.vecteezy.com/system/resources/previews/020/274/037/non_2x/dashboard-icon-for-your-website-design-logo-app-ui-free-vector.jpg", "label": "Dashboard", "key": "dashboard"},
    {"icon": "https://cdn-icons-png.flaticon.com/256/1467/1467210.png", "label": "Sales Analytics", "key": "analytics"},
    {"icon": "https://i.pinimg.com/564x/f2/3c/6b/f23c6bc64414337d86315880fe8be715.jpg", "label": "Products", "key": "products"},
    {"icon": "https://cdn-icons-png.flaticon.com/512/8163/8163551.png", "label": "Customers", "key": "customers"},
    {"icon": "https://www.iconpacks.net/icons/2/free-settings-icon-3110-thumb.png", "label": "Settings", "key": "settings"}
]



for option in nav_options:
    active = "active" if st.session_state.current_page == option["key"] else ""

    page= ''
    with st.sidebar.container():
        cols = st.columns([2,1.5])
        with cols[0]:
            # st.image(option["icon"], width=35)
            st.markdown(f"""
            <div class="nav-item {active}">
                <img src="{option['icon']}">
<!--            <span>{option['label']}</span>  -->
            </div>
            """, unsafe_allow_html=True)
       
        with cols[1]:
            if st.button('->', key=f"nav_{option['key']}"):
                st.session_state.current_page = option["key"]
                st.rerun()

current_page = st.session_state.current_page


with st.sidebar.container():
    col1,col2 = st.columns(2)

    with col1 :
        if st.button("🎈"):
            st.balloons()
    with col2:
        if st.button("❄️"):
            st.snow()


# Pages on the basis of the selection from the navbar
if current_page  == "dashboard":
    st.subheader("Sales Dashboard ")

    with st.container(border= True):

        mainrow1 = st.container()
        mainrow2 = st.container()

        with mainrow1 :
            col1, col2 = st.columns([1,2])

            with col1 : 
                row1 = st.container()
                row2 = st.container()
                with row1:
                    part1, part2 = st.columns(2)
                    with part1:
                        with st.container(border=True, height=210):
                            st.markdown("> Total Sales Profit Over Year")
                            st.subheader(f" INR : {total_profit}")
                    with part2:
                        with st.container(border=True,height=210):
                            st.markdown("> Total Order Over Year")
                            st.subheader(f"{total_order_count}")
                with row2 :
                    part1, part2 = st.columns(2)
                    with part1:
                        with st.container(border=True, height=210):
                            st.markdown("> Total Revenue")
                            st.subheader(f" INR : {total_sale}")
                    with part2:
                        with st.container(border=True, height=210):
                            st.markdown("> Average Discount on Products")
                            st.subheader(f"{average_discount:.2f} %")



            with col2:
                with st.container(border=True  ):
                    st.subheader("📈 Sales Over Time")
                    st.metric(label= " 💰 Total Sales" ,  value= f"{total_sale:,.0f}")


                    # Ploting line graph

                    with st.container():
                        fig, ax = plt.subplots(figsize=(4.5,3))
                        ax.plot(sale_over_time["Order_Date"], sale_over_time["Sales_Amount"], color="#ff6b6b", linewidth=2)
                        ax.fill_between(sale_over_time["Order_Date"], sale_over_time["Sales_Amount"],color="#ff6b6b", alpha=0.3)
                        ax.set_title("Sale Over Time ", fontsize = 16, fontweight = "bold")
                        ax.set_xlabel("Date")
                        ax.set_ylabel("Sales (₹)")
                        plt.xticks(rotation = 45)
                            
                        st.plotly_chart(fig, use_container_width=True)


    

        with mainrow2  : 
            col1, col2, col3=  st.columns([1.8,1.4,1])
            with col1:
                fig =  px.bar(
                    region_stats,
                    y = 'Region',
                    x = "Sales_Amount",
                    title =  '<b>Sales by Region</b>',
                    color  =  'Sales_Amount',
                    color_continuous_scale = "blues",
                    hover_data = ['Order_Count', 'Profit'],
                    orientation= 'h'
                )

                fig.update_layout(
                    yaxis_title = "Region",
                    xaxis_title = "Sales Amount (INR)",
                    plot_bgcolor = 'rgba(0,0,0,0)',
                    paper_bgcolor = 'rgba(0,0,0,0)',
                    font  =  dict(size = 12)
                )


                # Format hover template

                fig.update_traces(
                    hovertemplate='<b>%{x}</b><br>Sales: ₹%{y:,.0f}<br>Orders: %{customdata[0]}<br>Profit: ₹%{customdata[1]:,.0f}<extra></extra>'
                    )    

                fig.update_yaxes(tickprefix = '₹', tickformat = ',.0f')

                st.plotly_chart(fig, use_container_width=True)

                

                colm1, colm2, colm3, colm4 = st.columns(4)
                with colm1:
                    st.write("> Total Sales", f"₹{region_stats['Sales_Amount'].sum():,.0f}")
                with colm2:
                    st.write("> Highest Region", region_stats.iloc[0]['Region'])
                with colm3:
                    st.write("> Avg per Region", f"₹{region_stats['Sales_Amount'].mean():,.0f}")
                with colm4:
                    st.write("> Regions", len(region_stats))
            

            with col2 :
                    with st.container(border= True):
                        fig = px.pie(
                            revenue_by_flabor,
                            values="Sales_Amount",
                            names= "Product_Name",
                            title= '<b>Revenue Distribution By Cake Flavor</b>',
                            hole=0.4, 
                            color_discrete_sequence=px.colors.sequential.Viridis
                        )

                        fig.update_traces(
                            textposition ="inside",
                            textinfo = 'percent+label',
                            hovertemplate='<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<br>Percentage: %{percent}'
                        )

                        st.plotly_chart(fig,use_container_width=True)

            with col3:
                    fig = px.bar(
                        sales_by_category,
                        x = "Product_Name",
                        y= "Sales_Amount",
                        title='<b>Sales by Product Category</b>',
                    )

                    fig.update_layout(
                        xaxis_title='Product Category',
                        yaxis_title='Sales Amount (INR)',
                        showlegend=False
                    )
                    fig.update_yaxes(tickprefix='₹')

                    st.plotly_chart(fig,use_container_width= True)


elif current_page  == "analytics":
    st.subheader(" Sales Analytics")
    st.markdown("Detailed analysis and insights into your sales performance")


    st.subheader("🔧 Filters")
    col1,col2, col3 = st.columns([2,3.5,2.8])


    with col1:
        st.markdown('> **Select date range**')
        min_date = df['Order_Date'].min()
        max_date = df['Order_Date'].max()

        date_range= st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value= max_date,
            label_visibility="collapsed"
        )

    with col2:
        st.markdown('> **Select Regions**')
        regions  =  st.multiselect(
            " Regions",
            options=df["Region"].unique(),
            default= df["Region"].unique()
        )
    
    with col3 : 
        st.markdown('> **Select Channels**')
        Channels = st.multiselect(
            "Channels",
            options=df["Channel"].unique(),
            default= df["Channel"].unique()
        )

    filter_df = df.copy()
    if len(date_range)==2:
        filter_df =  filter_df[
            (filter_df['Order_Date']>=  pd.to_datetime(date_range[0]))&
            (filter_df['Order_Date']<=  pd.to_datetime(date_range[1]))
        ]

    if regions :
        filter_df =  filter_df[filter_df["Region"].isin(regions)]

    if Channels:
        filter_df =  filter_df[filter_df["Channel"].isin(Channels)]


    st.markdown(">## Key Performance Indicator ##")

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        with st.container(border= True):
            total_sales =  filter_df['Sales_Amount'].sum()
            st.metric("Total Sales", f'{total_sales:,.0f}')

    with col2:
        with st.container(border= True):
            total_Profit =  filter_df['Profit'].sum()
            st.metric("Total profit", f'{total_profit:,.0f}')

    with col3:
        with st.container(border= True):
            average_ordervalue =  filter_df['Sales_Amount'].mean()
            st.metric("Average Order Value ", f'{average_ordervalue:,.0f}')
        
    with col4:
        with st.container(border= True):
            total_order  =  filter_df["Order_ID"].count()
            st.metric("Total Order ", f'{total_order}')




    st.markdown(">## View Top-Selling Products ##")

    top_Product =  filter_df.groupby('Product_Name').agg({
        'Sales_Amount': 'sum',
        'Profit': 'sum',
        'Quantity' :  'sum',
        'Order_ID'  :  'count'
    }).reset_index()

    top_Product  =  top_Product.rename(columns={'Order_ID': 'Order_Count'})
    top_Product  =  top_Product.sort_values('Sales_Amount', ascending=False) 

    fig =px.bar(
        top_Product.head(10),
        x='Sales_Amount',
        y='Product_Name',
        title='Top Product by Revenue',
        orientation='h',
        color='Sales_Amount',
        color_continuous_scale='viridis'
    )

    fig.update_xaxes(tickprefix = '₹' , title = 'Sales Amount')
    fig.update_yaxes(title = 'Product Name')

    st.plotly_chart(fig, use_container_width= True)
    # https://chat.deepseek.com/a/chat/s/4fb37c98-7e51-4090-80bc-f7f6b9af1761


    st.markdown(">## Comapre Monthluy Trend ##")

    mothly_trend = filter_df.copy()
    mothly_trend['YearMonth'] = mothly_trend['Order_Date'].dt.to_period('M').astype(str)

    Mothly_Sales = mothly_trend.groupby('YearMonth').agg({
        'Sales_Amount': 'sum',
        'Profit': 'sum',
        'Order_ID' : 'count'
    }).reset_index()


    trend_tab1, trend_tab2 , trend_tab3 = st.tabs(['Sales Trend', 'Profit Trend', 'Order Trend'])

    with trend_tab1:
        fig_slaes = px.line(
            Mothly_Sales,
            x= 'YearMonth',
            y= "Sales_Amount",
            title = "Monthly Sales Trend",
            markers= True

        )

        fig_slaes.update_yaxes(tickprefix = '₹', title = 'Sales Amount')
        st.plotly_chart(fig_slaes,use_container_width=True)


    with trend_tab2:
        fig_profit = px.line(
            Mothly_Sales,
            x= 'YearMonth',
            y= "Profit",
            title = "Monthly Profit Trend",
            markers= True,
            line_shape= 'spline'

        )

        fig_profit.update_yaxes(tickprefix = '₹')
        st.plotly_chart(fig_profit,use_container_width=True)


    with trend_tab3:
        fig_ordered = px.line(
            Mothly_Sales,
            x= 'YearMonth',
            y= "Order_ID",
            title = "Monthly Order Counnt Trend",
            markers= True

        )

        fig_ordered.update_yaxes(title = "Number of order")
        st.plotly_chart(fig_ordered,use_container_width=True)

        


    st.markdown(">## Profit vs Sales Analysis ##")

    pv_tab1 , pv_tab2 = st.tabs(['Scatter Plot', 'Line Comparision'])


    with pv_tab1:
        # Scatter plot: Profit vs Sales by Product
        Produt_performance  = filter_df.groupby('Product_Name').agg({
            'Sales_Amount':  'sum',
            'Profit': 'sum',
            "Quantity": 'sum'
        }).reset_index()


        Produt_performance['Profit_Margin'] = (Produt_performance['Profit']/Produt_performance['Sales_Amount']*100).round(2)

        fig_Scatter = px.scatter(
            Produt_performance,
            x = "Sales_Amount",
            y = "Profit",
            color='Profit_Margin',
            hover_name= "Product_Name",
            color_continuous_scale='RdYlGn',
            size_max=60
        )

        fig_Scatter.update_xaxes(tickprefix = '₹',  title = "Total Sales")
        fig_Scatter.update_yaxes(tickprefix = '₹',  title = "Total Profit")

        st.plotly_chart(fig_Scatter, use_container_width=True)


    with pv_tab2:
        # Line plot comparing Sales vs Profit over time

        Produt_Comparision  = filter_df.groupby('Order_Date').agg({
            'Sales_Amount': 'sum',
            'Profit': 'sum',
        }).reset_index()



        fig_line = px.line(
            Produt_Comparision,
            x = "Order_Date",
            y = ["Sales_Amount", 'Profit'],
            title="Daily Sales vs Profit Comparion",
            labels= {'value' : 'Amount (₹)', 'variable': 'Metric'}
        )

        fig_line.update_yaxes(tickprefix = '₹')
        fig_line.update_xaxes(title = 'Order Date')
        fig_line.update_layout(legend_title_text = 'Metric')

        st.plotly_chart(fig_line, use_container_width=True)


    with  st.expander("View Filterd DATA "):
        st.dataframe(
            filter_df.style.format({
                'Sales_Maount'  : '₹{:,.0f}',
                "Profit" :  '₹{:,.0f}',
                "Discount" :  '{:,.0f}%',
            }),use_container_width= True,
            height= 300
        )

elif current_page  == "products":

    st.markdown('>## Products ##')

    cake = {
        'Pineapple Cake' : 'media/Cake/PineappleCake.png',
        'Red Valvet' : 'media/Cake/RedVelvet.png',
        'Black Forest' : 'media/Cake/BlackForest.png',
        'Vanilla Cake' : 'media/Cake/VanillaCake.png',
        'Chocolate Cake' : 'media/Cake/ChocolateCake.png',
        'Cheesecake' : 'media/Cake/Cheesecake.png',
        'Strawberry Cake' : 'media/Cake/StrawberryCake.png'

    }
    
    cols = st.columns(4)

    for i, (key, value) in enumerate(cake.items()):
        with cols[i % 4]:
            with st.container(border= True,width= 220):
                st.image(value, width=200)
                st.markdown(f'**{key}**')

elif current_page == "settings":
    st.title("⚙️ Settings")
    st.markdown("Basic dashboard configuration and preferences")
    
    # ===== APPEARANCE SETTINGS =====
    st.subheader("🎨 Appearance")

    if "theme" not in st.session_state:
        st.session_state.theme = "Light"

    c1,c2 = st.columns(2)
    with c1:

        with st.container(border=True):
            # Theme selection
            theme = st.selectbox(
                "Color Theme",
                ["Light", "Dark", "Blue", "Green"],
                help="Choose dashboard color theme"
            )

 
    with c2:
        st.button("Save")
        st.session_state.theme = theme
        st.success(f"Theme saved successfully! 🎉 Using **{theme}** mode.")

        def apply_theme(theme_name):
            themes = {
                "Light": """
                    <style>
                        .stApp { background-color: #ffffff; color: #000000; }
                    </style>
                """,
                "Dark": """
                    <style>
                        .stApp { background-color: #1e1e1e; color: #f5f5f5; }
                    </style>
                """,
                "Blue": """
                    <style>
                        .stApp { background: linear-gradient(to bottom right, #e3f2fd, #bbdefb); color: #0d47a1; }
                    </style>
                """,
                "Green": """
                    <style>
                        .stApp { background: linear-gradient(to bottom right, #e8f5e9, #c8e6c9); color: #1b5e20; }
                    </style>
                """,
            }
            st.markdown(themes.get(theme_name, ""), unsafe_allow_html=True)

            apply_theme(st.session_state.theme)

elif current_page == "customers":
    st.markdown(">## Customers ##")
    st.markdown("Customer channel preferences and distribution")
    
    channel_customers = df.groupby('Channel')['Customer_Name'].nunique().reset_index()
    channel_customers.columns = ['Channel', 'Customer_Count']
    
    # DONUT CHART 
    st.subheader("📊 Channel Usage by Customers")
    
    fig = px.pie(
        channel_customers,
        values='Customer_Count',
        names='Channel',
        title='',
        hole=0.6, 
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>%{value} customers<br>%{percent} of total'
    )
    
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.1
        ),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # CHANNEL STATS 
    st.subheader("📈 Channel Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_customers = channel_customers['Customer_Count'].sum()
        st.metric("Total Customers", total_customers)
    
    with col2:
        top_channel = channel_customers.loc[channel_customers['Customer_Count'].idxmax(), 'Channel']
        st.metric("Most Popular", top_channel)
    
    with col3:
        channels_used = len(channel_customers)
        st.metric("Channels", channels_used)
    
    with st.expander("📋 View Channel Data"):
        st.dataframe(
            channel_customers.style.format({
                'Customer_Count': '{:.0f}'
            }),
            use_container_width=True
        )
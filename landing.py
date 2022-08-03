import streamlit as st
import pandas as pd
from scripts import run_queries
from plots import * 
from queries import *
import datetime
#cm = sns.light_palette("green", as_cmap=True)
#   with st.expander('show list'):
#        st.dataframe(data.sort_values(by='USD',ascending=False).style.background_gradient(cmap=cm))
import seaborn as sns
pd.set_option('display.width', 1400)
cm = sns.light_palette("green", as_cmap=True)


def get_change(ser,previous,what='NEW_ADDRESS'):
    if what =='USER':
        a = ser['USERS_DOING_TRANSACTIONS']+ser['USERS_RECEIVING_TOKENS']
        b = previous['USERS_DOING_TRANSACTIONS']+previous['USERS_RECEIVING_TOKENS']
        change = f"{((a / b)-1)*100:.2f} %"
        
    else:
        change = f"{((ser[what] / previous[what])-1)*100:.2f} %"
    return change


def landing_page():

    st.sidebar.image("Quixotic-logo.jpeg",width=300)
    st.sidebar.title("Quixotic Dashboard")

                     
    
    with st.spinner(text="Fetching Data..."):
        df,df2 = run_queries()


    st.subheader("Facts")
    st.write("Today vs last week")
    ser = df.query('DATE=="today"').iloc[0]
    previous = df.query('DATE!="today"').iloc[0]
    
    r = st.columns(3)
    with r[0]:
        label = 'TOTAL_AMOUNT'
        value = float(f"{ser[label]:.2f}")
        delta = get_change(ser,previous,what=label)
        st.metric(label, value, delta=delta, delta_color="normal", help=None)
    with r[1]:
        label = 'TOTAL_AVERAGE_PRICE'
        value = float(f"{ser[label]:.3f}")
        delta = get_change(ser,previous,what=label)
        st.metric(label, value, delta=delta, delta_color="normal", help=None)
    with r[2]:
        label = 'TOTAL_SALES'
        value = ser[label]
        delta = get_change(ser,previous,what=label)
        st.metric(label, value, delta=delta, delta_color="normal", help=None)
    
    r = st.columns(3)
    with r[0]:
        label = 'DISTINCT_BUYERS'
        value = ser[label]
        delta = get_change(ser,previous,what=label)
        st.metric(label, value, delta=delta, delta_color="normal", help=None)
    with r[1]:
        label = 'DISTINCT_SELLERS'
        value = ser[label]
        delta = get_change(ser,previous,what=label)
        st.metric(label, value, delta=delta, delta_color="normal", help=None)
    with r[2]:
        label = 'DISTINCT_NFTS'
        value = ser[label]
        delta = get_change(ser,previous,what=label)
        st.metric(label, value, delta=delta, delta_color="normal", help=None)
    
    st.subheader('NFT Stats')
    for i in df2.columns[2:]:
        if i == 'TOTAL_AMOUNT':
            c = 'Total Amount Sold (ETH)'
        elif i == 'Sales':
            c = 'Number of Sales'
        elif i == 'DISTINCT_BUYERS':
            c = 'Unique Buyers'
        elif i == 'DISTINCT_SELLERS':
            c = 'Unique Sellers'
        elif i == 'TOTAL_AVERAGE_PRICE':
            c = 'Average Price (ETH)'
        else:
            st.write(i)
            
        st.write(f'{c}')
        _df2 = df2.sort_values(by=i,ascending=False).head(20)
    
        st.plotly_chart(plot_bar(_df2,x0=i), use_container_width=True)

    with st.expander("Show dataframe"):
    #df2.index = df2['NFT_ADDRESS']
    
        df2['ADDRESS'] = df2['NFT_ADDRESS']
        st.dataframe(df2.drop(['NFT_ADDRESS'],axis=1).sort_values('TOTAL_AMOUNT',ascending=False).reset_index(drop=True).style.background_gradient(cmap=cm))

    st.sidebar.write("""#### Powered by FlipsideCrypto Godmode and ShroomDK 🫡""")

    st.sidebar.markdown(f""" 
### 💻 Github
[kkpsiren/polygon_mega](https://github.com/kkpsiren/polygon_mega)  
    """)
    with st.expander("Show queries"):
        st.markdown(f"""#### Query 1 for metrics
```
{QUERY}
```""")
        st.markdown(f"""#### Query 2 for NFT specs" 
```
{QUERY2}
```""")
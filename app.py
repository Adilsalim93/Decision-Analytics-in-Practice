import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


#{df, NAlist = reduce_mem_usage(df)
#print("_________________")
#print("")
#print("Warning: the following columns have missing values filled with 'df['column_name'].min() -1': ")
#print("_________________")
#print("")
#print(NAlist)
@st.cache(suppress_st_warning=True, persist=True)
def processing():
    data = pd.read_excel('Cleandata.xlsx')
    wag = pd.read_csv('Locomotive_Wango.csv')
    print(data.head())
    data['PRODUCT_TITLE1'] = data['PRODUCT_TITLE1'].str.strip()
    data = data[data.PRODUCT_AMOUNT > 0]
    data = data.drop(['PAYMENT_PRICE'], axis=1)
    data = data.drop(['CUSTOMER_COUNTRY'], axis=1)
    data = data.drop(['ORDER_VAT'], axis=1)
    data = data.drop(['ORDER_ORIGIN'], axis=1)
    new_df = data.groupby(['PRODUCT_ID'], sort=True).sum().reset_index()
    new_df = new_df.sort_values(by = ['PRODUCT_AMOUNT'], ascending=[False])
    new_df= new_df.iloc[0:201,0]
    top_200 = data.merge(new_df, on=['PRODUCT_ID'])
    top_200['Week_Number'] = top_200['ORDER_DATE'].dt.week
    Id_list = top_200['PRODUCT_ID'].unique()
    type(Id_list)
    return top_200, Id_list, data, new_df, wag
final_200, final_list, final_df, latest_df, wagons = processing()
#for x in np.nditer(Id_list):
    #top_200.plot(x='Week_Number', y='PRODUCT_AMOUNT', kind='line')
st.title("Bagetid.dk Top 200 products and observed trends")
option = st.sidebar.selectbox(
    'Product selection',
     final_list)
name = final_200.loc[final_200['PRODUCT_ID'] == option, 'PRODUCT_TITLE1'].iloc[0]
st.write("""###""", name,""" *has an average weekly  sales as shown below*""")
selected_product = final_200.loc[final_200['PRODUCT_ID'] == option]
selected_product = selected_product.groupby(['Week_Number']).agg({'PRODUCT_AMOUNT':['sum']})
plt.plot(selected_product, color='red', marker='o')
plt.title('Sales per Week', fontsize=14)
plt.xlabel('Week', fontsize=14)
plt.ylabel('Amount of Product sold', fontsize=14)
plt.grid(True)
st.pyplot()
@st.cache
def locomotives(w, t, choice):
    w= w.loc[w['Locomotive_ID'] == choice]
    wagonids = w['Wango_ID'].unique()
    wagonsales = t[t['PRODUCT_ID'].isin(wagonids)]
    return wagonsales
wagonframe = locomotives(wagons, final_df, option)

wag_df = wagonframe.groupby(['PRODUCT_ID'], sort=True).sum().reset_index()
wag_df = wag_df.sort_values(by=['PRODUCT_AMOUNT'], ascending=[False])
st.write("""### *The Wagon Pairs for the Product is given below:*""")
st.dataframe(data=wag_df)
pwag = wagons.loc[wagons['Locomotive_ID'] == option]
st.dataframe(pwag)
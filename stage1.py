import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

df=pd.read_csv('Data_Train.csv')
df_test=pd.read_csv('Data_Test.csv')
df.head()
df.isnull().sum()
df.dropna()
df.dropna(subset=['Seats'],inplace=True)
df.dropna(subset=['Mileage'],inplace=True)

df=df.drop(['Location'],axis=1)
df=df.reset_index()
df=df.drop(['index'],axis=1)
df.isnull().sum()
df['Mileage']=df['Mileage'].astype(str)
df['Engine']=df['Engine'].astype(str)
df['Power']=df['Power'].astype(str)
df['Mileage']=df['Mileage'].str.replace('kmpl','')
df['Mileage']=df['Mileage'].str.replace('km/kg','')
df['Engine']=df['Engine'].str.replace('CC','')
df['Power']=df['Power'].str.replace('bhp','')

df['feature_mfg_date']='New'

df['feature_mfg_date']=np.where((df.Year<2011),'old',df.feature_mfg_date)
df['feature_mfg_date']=np.where((df.Year>=2011),'like new',df.feature_mfg_date)
df['feature_mfg_date']=np.where((df.Year>2015),'new',df.feature_mfg_date)

df.head(100)
# df_test['Mileage']=df_test['Mileage'].astype(str)
# df_test['Engine']=df_test['Engine'].astype(str)
# df_test['Power']=df_test['Power'].astype(str)
# df_test['Mileage']=df_test['Mileage'].str.replace('kmpl','')
# df_test['Mileage']=df_test['Mileage'].str.replace('km/kg','')
# df_test['Engine']=df_test['Engine'].str.replace('CC','')
# df_test['Power']=df_test['Power'].str.replace('bhp','')

# df_test.dropna()
# df_test.drop(['Location'],axis=1)
# df_test=df_test.reset_index()
# df_test=df_test.drop(['index'],axis=1)
df=df.drop([4446,76,4413,4864,4863])
df['Power']=df['Power'].astype(str)
drop=df.loc[df.Power.str.contains('null ')].index

df.drop(drop,inplace=True)
df=df[df['Kilometers_Driven']<150000]
df=df[df['Kilometers_Driven']>=10000]
df=df[df['Mileage']!=0]
df['Mileage']=pd.to_numeric(df['Mileage'],downcast='float')
df['Engine']=pd.to_numeric(df['Engine'],downcast='float')
df['Power']=pd.to_numeric(df['Power'],downcast='float')
null_values=df[df['Mileage']==0].index
df.drop(null_values,inplace=True)

df['Kilometers_Driven'].min()
df['condition']='Excellent'
df['condition']=np.where((df.Kilometers_Driven<20000),'excellent',df.condition)
df['condition']=np.where((df.Kilometers_Driven>=20000)&(df.feature_mfg_date=='old'),'good',df.condition)
df['condition']=np.where((df.Kilometers_Driven>60000)&(df.feature_mfg_date=='old'),'good',df.condition)
df['condition']=np.where((df.Kilometers_Driven>80000)&(df.feature_mfg_date=='old'),'salavage',df.condition)
df['condition']=np.where((df.Kilometers_Driven>=20000)&(df.feature_mfg_date=='like new'),'good',df.condition)
df['condition']=np.where((df.Kilometers_Driven>60000)&(df.feature_mfg_date=='like_new'),'fair',df.condition)

df['condition']=np.where((df.Kilometers_Driven>=20000)&(df.feature_mfg_date=='new'),'excellent',df.condition)

df['condition']=np.where((df.Kilometers_Driven>100000),'salavage',df.condition)

df['condition']=np.where((df.condition=='excellent')&(df.Owner_Type=='First'),'excellent',df.condition)
df['condition']=np.where((df.condition=='excellent')&(df.Owner_Type=='Second'),'good',df.condition)
df['condition']=np.where((df.condition=='good')&(df.Owner_Type=='First'),'good',df.condition)
df['condition']=np.where((df.condition=='good')&(df.Owner_Type=='Second'),'fair',df.condition)
df['condition']=np.where((df.condition=='fair')&(df.Owner_Type=='First'),'fair',df.condition)
df['condition']=np.where((df.condition=='fair')&(df.Owner_Type=='Second'),'fair',df.condition)
df['condition']=np.where((df.condition=='salavage')&(df.Owner_Type=='First'),'salavage',df.condition)
df['condition']=np.where((df.condition=='salavage')&(df.Owner_Type=='Second'),'salavage',df.condition)
df['condition']=np.where((df.condition=='excellent')&(df.Engine<2000),'good',df.condition)
df['condition']=np.where((df.condition=='good')&(df.Engine<1000),'fair',df.condition)
df['condition']=np.where((df.condition=='fair')&(df.Power>290),'excellent',df.condition)

warnings.filterwarnings('ignore')
sns.set_style('darkgrid')
f, axes = plt.subplots (2,1, figsize=(8,8))
x=['excellent','good','fair','salavage']
y=[df.condition[(df['condition']=='excellent')].count(),df.condition[(df['condition']=='good')].count(),\
     df.condition[(df['condition']=='fair')].count(),df.condition[(df['condition']=='salavage')].count()]
vis1= sns.barplot(x,y,palette='Accent',ax=axes[0])
vis1.set(xlabel='Condition',ylabel='Number of cars')
for p in vis1.patches:
             vis1.annotate("%.f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='center', fontsize=11, color='gray', xytext=(0, 20),
                 textcoords='offset points')
NG = [df.condition[(df['condition']=='excellent')].count(),df.condition[(df['condition']=='good')].count(),\
     df.condition[(df['condition']=='fair')].count(),df.condition[(df['condition']=='salavage')].count()]
G = ['excellent','good','fair','salavage']

plt.pie(NG, labels=G, startangle=90, autopct='%.1f%%')
plt.show()


plt.ioff()

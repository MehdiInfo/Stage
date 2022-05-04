# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 14:46:41 2022

@author: Mehdi
"""
import pandas as pd


df = pd.read_csv('combinerExcel/CO2_107.csv')
print(df)
print(df['Valeur'].dtype)
print(df['Valeur'].apply(type))
print(df['Valeur'].dtype)
if(df['Valeur'].dtype == 'object'):    
    df['Valeur'] = df['Valeur'].str.replace(' ','')
    df['Valeur'] = df['Valeur'].str.replace(',','.')
    df['Valeur'] = df['Valeur'].astype('float')
    df['Valeur'] = df['Valeur'].astype('int')
    #df['Valeur'] = df['Valeur'].astype('float')
print(df['Valeur'].apply(type))
df.plot()
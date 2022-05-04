# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 14:00:28 2022

@author: Mehdi
"""
# Ce programme permet de compiller,nettoyer et organiser les diffirents données colléctés en format .csv au sein de l'EPF

import pandas as pd
import os
from IPython.display import display
import matplotlib.pylab as plt
import matplotlib.dates as mdates
fichiers = []

# Parcours des différents fichiers qui se trouvent dans le dossier et les rajoutes dans la liste
for root, dirs, files in os.walk("combinerExcel/"):
    for file in files:
        if file.endswith(".csv"):
            #fichiers.append(file)
            inter = os.path.join(root,file)
            fichiers.append(inter)

#Assemblage des différents fichiers csv
all_data = pd.DataFrame()
for f in fichiers:
    df = pd.read_csv(f,parse_dates=True)
    all_data = all_data.append(df,ignore_index=False)

#suppression des dates qui ont une valeur null (Nat)
all_data.dropna(subset=['DateHeure'],inplace=True)

#Organisation de la data et découpage de la colonne lib en colonne type et salle
all_data[['Type','Salle']] = all_data['Lib'].str.split(None, 1,expand = True)

#Suppression de la colonne lib
all_data.drop("Lib", axis=1, inplace=True)
all_data = all_data.reindex(columns = ['DateHeure','Group1','Type','Salle','Valeur'])

#Dévision des données en deux catégorie ceux qui ont les température et ceux qui ont le taux de co2
CO2_s = all_data['Type'].str.match('CO2', na = False)
Temp_s = all_data['Type'].str.match('Temp', na = False)

CO2_data = all_data[CO2_s]
Temp_data = all_data[Temp_s]

#Rennomage des valeurs selon leurs catégories
CO2_data = CO2_data.rename(columns = {'Valeur':'Valeur_CO2'})
Temp_data = Temp_data.rename(columns = {'Valeur':'Valeur_Temp'})

#Supression d'espace et remplacement des , par des point pour faciliter la tranformation en valeur réel
Temp_data['Valeur_Temp'] = Temp_data['Valeur_Temp'].str.strip()
#CO2_data['Valeur_CO2'] = CO2_data['Valeur_CO2'].str.strip()
Temp_data['Valeur_Temp'] = Temp_data['Valeur_Temp'].str.replace(',','.')
#CO2_data['Valeur_CO2'] = CO2_data['Valeur_CO2'].str.replace(' ','')

#Transforme les strings en valeur numérique
CO2_data['Valeur_CO2'] = pd.to_numeric(CO2_data['Valeur_CO2'], errors = 'coerce',downcast= 'integer')
Temp_data['Valeur_Temp'] = pd.to_numeric(Temp_data['Valeur_Temp'],errors = 'coerce',downcast= 'float')

#Rassembler les données(temp et taux co2) qui ont la meme salle et la meme date/heure$
all_data = []
all_data = pd.merge(Temp_data,CO2_data, on =['DateHeure','Group1','Salle'], how ='outer')

#Suppression des colonnes inutilles
all_data.drop(['Type_y','Type_x','Group1'],axis = 1, inplace = True)

#Recalcul des indexs
all_data.reset_index(drop=True, inplace=True)

#tri par date
#all_data.sort_values(by='DateHeure', inplace= True)
all_data['pd.to_datetime(all_data['DateHeure'])
Salles = pd.DataFrame(all_data['Salle'].unique())

all_data = all_data.drop_duplicates()

#all_data = pd.between_time('8:00', '20:00')
#all_data = all_data.loc[all_data['DateHeure'] == '01-01-2018']
liste_salle = []

for salle in Salles[0]:
    liste_salle.append(all_data[all_data['Salle'].str.match(salle)])

#affichage des différents graphs
for salle in liste_salle:
    ax = salle.plot('DateHeure','Valeur_Temp', color = 'Green', linewidth = 1, rot = 45, ylabel = 'Température')
    ax2 = salle.plot('DateHeure','Valeur_CO2',secondary_y = True, color = 'Blue', linewidth = 1,rot = 45, ax = ax, ylabel = 'Taux CO2')
    ax.legend(loc='center left', bbox_to_anchor=(1.1, 1.0))
    ax2.legend(loc='center left', bbox_to_anchor=(1.1, 1.1))
    ax.set_ylabel('Température')
    ax2.set_ylabel('Taux de CO2')
    plt.title(f"Température et taux de CO2 de la salle : {salle.iloc[2]['Salle']}")
    plt.show()

#Sauvegarde dans un fichier csv
#all_data.to_csv('Compillation.csv',encoding="utf-8", index = False)
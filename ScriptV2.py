# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 10:27:08 2022

@author: Mehdi
"""
import pandas as pd
import os
from IPython.display import display
import matplotlib.pylab as plt
import matplotlib.patches as ptc
import datetime
import seaborn as sns
import matplotlib.patches as mpatches

def corr_gen(all_data):
    """
        calcule et affiche la corrélation entre la température et le taux de CO2 sur toutes les salles ainsi qu'un graph qui représente cetter derniére
    """
    print(f" La correllation entre la Température et le taux de CO2 est de  {all_data['Valeur_CO2'].corr(all_data['Valeur_Temp'])}")

def confort_thermique(all_data):
    """
        Température en fonction du CO2 
    """
    #plt.figure(figsize=(10,10))
    sns.set(rc={'axes.facecolor':'lightblue', 'figure.facecolor':'lightblue','axes.grid' : False})
    sns.despine()
    
    ax = sns.scatterplot(data = all_data,x= 'Valeur_Temp',y= 'Valeur_CO2',hue='Salle',markers = True,alpha = 1)
    ax.add_patch(ptc.Rectangle((20,0),5,820,alpha = 0.2,facecolor = 'green'))
    ax.set_ylabel('CO2(ppm)')
    ax.set_xlabel('Température(C°)')
    plt.legend(title = 'Salle',bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('Température en fonction du CO2 (La zone verte correspond au confort thermique)')
    plt.savefig('ConfortThermique.jpg')
    plt.show()
    
    
def weekly_graphs(all_data):
    
    """
        affiches des subplots qui contiennent les graphs 
    """
    test = all_data.groupby('Salle')
    sns.set(rc={'axes.facecolor':'lightblue', 'figure.facecolor':'lightblue','axes.grid' : False})
    sns.despine()
    for nom, data_salle in test:
        data_salle = data_salle.between_time('8:00:00','12:00:00')
        interm = data_salle[data_salle.index.dayofweek < 5]
        data_semaines = interm.groupby(interm.index.day)
        fig=plt.figure(figsize=(12,8),constrained_layout=True)
        fig.tight_layout()
        i = 1
        for nb, data_jour in data_semaines:
            fig.add_subplot(2,3,i)
            p = sns.lineplot(data = data_jour, x = data_jour.index, y = 'Valeur_Temp',color = 'blue',legend = 'auto')
            p.set_title(f'jour {nb}')
            p.set_ylabel('Température(C°)',color='blue')
            p.set_xlabel('Date et Heure')
            plt.xticks(rotation = 45)
            ax = p.twinx()
            ax2 = sns.lineplot(data = data_jour,x = data_jour.index, y = 'Valeur_CO2',color = 'red', ax = ax)
            ax2.set_ylabel('CO2(ppm)',color='red')
            i += 1
        fig.suptitle(f'Températures et taux de CO2 entre le 22 et 26 du mois dans la salle {nom} entre 7h et 18h (heures de cours)')
        plt.show()
        

fichiers = []
# Parcours des différents fichiers qui se trouvent dans le dossier et les rajoutes dans la liste
for root, dirs, files in os.walk("Salle de cours/"):
    for file in files:
        if file.endswith(".csv"):
            #fichiers.append(file)
            inter = os.path.join(root,file)
            fichiers.append(inter)

all_data = pd.DataFrame()

#Parser de dates
parser = lambda date: datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S')

#Lecture des fichiers csv et conversions des dates
for file in fichiers:
    print(f'Lecture du fichier {file} et conversion des dates...')
    df = pd.read_csv(file,parse_dates = ['DateHeure'], date_parser= parser)
    if(df['Valeur'].dtype == 'object'):    
        df['Valeur'] = df['Valeur'].str.replace(' ','')
        df['Valeur'] = df['Valeur'].str.replace(',','.')
        df['Valeur'] = df['Valeur'].astype('float')
    all_data = all_data.append(df)
print('Tri des données en fonction des dates/heures')
#
all_data.sort_values(by='DateHeure', inplace= True)

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


#Transforme les strings en valeur numérique
print('Conversion des valeurs CO2 et Températures...')
CO2_data['Valeur_CO2'] = pd.to_numeric(CO2_data['Valeur_CO2'],downcast= 'integer')
Temp_data['Valeur_Temp'] = pd.to_numeric(Temp_data['Valeur_Temp'],downcast= 'float')


#Rassembler les données(temp et taux co2) qui ont la meme salle et la meme date/heure$
all_data = []
all_data = pd.merge(Temp_data,CO2_data, on =['DateHeure','Group1','Salle'], how ='outer')

#Suppression des colonnes inutilles
all_data.drop(['Type_y','Type_x','Group1'],axis = 1, inplace = True)

#suppression des doublons
print('Suppression des doublons')
all_data = all_data.drop_duplicates()

#Recalcul des indexs
all_data.reset_index(drop=True, inplace=True);

#mask = pd.date_range('2018-01-25 08:00:00','2018-01-25 18:00:00',freq='10T')

all_data = all_data[(all_data['DateHeure'] >= '2018-01-22') & (all_data['DateHeure'] <= '2018-01-27')]
#all_data = all_data[(all_data['DateHeure' : mask])]



#display(all_data)
all_data.set_index('DateHeure', inplace = True)
#all_data.sort_index(inplace = True)

#all_data = all_data.between_time('7:00:00','19:00:00')

corr_gen(all_data)
#weekly_graphs(all_data)
confort_thermique(all_data)

#####################


# coding: utf-8

# # Carnet d'ordre sous la Blockchain

# In[1]:


import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from scipy.stats import norm
from pandas.plotting import autocorrelation_plot
import matplotlib.patches as mpatches
import datetime


# # Initialisation de la Blockchain, du carnet d'ordres et des utilisateurs

# In[5]:


Blockchain=[]  # initialisation de la Blockchain
Users=[]
address=0
index=0

dat=datetime.datetime.now()
dat=str(dat.day)+'/'+str(dat.month)+'/'+str(dat.year)+','+' '+ str(dat.hour)+'h-'+str(dat.minute)+'mn-'+str(dat.second)+'s'
event=[dat+'  '+'création de la Blockchain']
Blockchain.append(event)

# initialisation du carnet d'ordres
#Conditions initiales
N=50 #taille
Carnet_dOrdres=[]
Ordre=[]
valeur_initialisation=0
i=0
while i<=0.5*N-1:
    Carnet_dOrdres.append(-valeur_initialisation)
    i=i+1
    
while 0.5*N<=i<N:
    Carnet_dOrdres.append(valeur_initialisation)
    i=i+1 
    
Carnet_dOrdres=np.array(Carnet_dOrdres)

def generer_utilisateur(cash_balance,token_balance):
    
    utilisateur=[]
    utilisateur.append(address)
    utilisateur.append(cash_balance)
    utilisateur.append(token_balance)
    Users.append(utilisateur)
    
    dat=datetime.datetime.now()
    dat=str(dat.day)+'/'+str(dat.month)+'/'+str(dat.year)+','+' '+ str(dat.hour)+'h-'+str(dat.minute)+'mn-'+str(dat.second)+'s'
    event=[dat+'  '+'arrivée de '+str(address)+','+'cash_balance='+str(cash_balance)+','+'Token_balance='+str(token_balance)]
    Blockchain.append(event)
    increment_adress()
    
    return utilisateur

for i in range(11): 
    generer_utilisateur(100,50)
    
def increment_adress():
    global address
    address = address+1


# In[6]:


def get_carnet_dordres():
    return Carnet_dOrdres
    
def increment_index():
    global index
    index = index+1

def get_bestbid():
    ind=np.where(Carnet_dOrdres<0)[0][-1]
    return ['prix:'+str(ind), 'quantité:'+str(abs(Carnet_dOrdres[ind]))] 

def get_bestask():
    ind=np.where(Carnet_dOrdres>0)[0][0]
    return ['prix:'+str(ind), 'quantité:'+str(Carnet_dOrdres[ind])] 


# # Fonction transférer token

# In[7]:


def transferer_token(from_,to_,montant) :
    dat=datetime.datetime.now()
    dat=str(dat.day)+'/'+str(dat.month)+'/'+str(dat.year)+','+' '+ str(dat.hour)+'h-'+str(dat.minute)+'mn-'+str(dat.second)+'s'
    
    if montant<=Users[from_][2]:
        Users[from_][2]-=abs(montant)
        Users[to_][2]+=abs(montant)
        event=[dat+'  '+'Tansaction tokens: Transfert de '+ str(montant)+ ' token(s) de '+ str(from_)+ ' vers '+ str(to_) ]
        Blockchain.append(event)
        
        
    


# # Fonction transférer cash

# In[8]:


def transferer_cash(from_,to_,montant) :
    dat=datetime.datetime.now()
    dat=str(dat.day)+'/'+str(dat.month)+'/'+str(dat.year)+','+' '+ str(dat.hour)+'h-'+str(dat.minute)+'mn-'+str(dat.second)+'s'
    
    if montant<=Users[from_][1]: 
        Users[from_][1]-=abs(montant)
        Users[to_][1]+=abs(montant)
        event=[dat+'  '+'Tansaction cash: Transfert de '+ str(montant)+ ' dollars de '+ str(from_)+ ' vers '+ str(to_) ]
        Blockchain.append(event)


# # Ordre limite d'achat et de vente

# In[9]:


def ordre_limit_achat(from_,quantité, prix):
    ordre=[index,'Ordre limite d achat',from_,quantité,abs(prix)]
    increment_index()
    Carnet_dOrdres[prix] -= abs(quantité)
   
    
    dat=datetime.datetime.now()
    dat=str(dat.day)+'/'+str(dat.month)+'/'+str(dat.year)+','+' '+ str(dat.hour)+'h-'+str(dat.minute)+'mn-'+str(dat.second)+'s'
    event=[dat+'  '+'Ordre limite d achat de '+str(quantité)+' token(s), au prix de '+str(prix)+' ,adresse emetteur:'+str(from_)]
    Blockchain.append(event)
    
    Ordre.append(ordre)
    


# In[10]:


def ordre_limit_vente(from_,quantité, prix):
    ordre=[index,'Ordre limite de vente',from_,quantité,abs(prix)]
    increment_index()
    Carnet_dOrdres[prix] += quantité
    
    dat=datetime.datetime.now()
    dat=str(dat.day)+'/'+str(dat.month)+'/'+str(dat.year)+','+' '+ str(dat.hour)+'h-'+str(dat.minute)+'mn-'+str(dat.second)+'s'
    event=[dat+'  '+'Ordre limite de vente de '+str(quantité)+' token(s), au prix de '+str(prix)+' ,adresse emetteur:'+str(from_)]
    Blockchain.append(event)
    
    Ordre.append(ordre)


# # Suppression ordre

# In[11]:


def supprimer_ordre(from_,num_ordre):
    
    for i in range(len(Ordre)):
        if Ordre[i][0]==num_ordre:
            index_ordre=i
            break
        else:
            index_ordre=len(Ordre)+1

    if index_ordre<len(Ordre):
    
        if from_==Ordre[index_ordre][2]:

            if Ordre[index_ordre][1]=='Ordre limite d achat':
                Carnet_dOrdres[Ordre[index_ordre][4]]+=Ordre[index_ordre][3]
            else:
                Carnet_dOrdres[Ordre[index_ordre][4]]-=Ordre[index_ordre][3]



            dat=datetime.datetime.now()
            dat=str(dat.day)+'/'+str(dat.month)+'/'+str(dat.year)+','+' '+ str(dat.hour)+'h-'+str(dat.minute)+'mn-'+str(dat.second)+'s'
            event=[dat+'  '+'Annulation '+str(Ordre[index_ordre][1])+' de '+ str(Ordre[index_ordre][3])+' token(s), au prix de '+str(Ordre[index_ordre][4])+' ,adresse emetteur:'+str(Ordre[index_ordre][2])]
            Blockchain.append(event)

            del Ordre[index_ordre]

    
    


# # Ordre au marché achat et vente

# In[12]:


def ordre_achat_marché(from_,quantité):
    
    dat=datetime.datetime.now()
    dat=str(dat.day)+'/'+str(dat.month)+'/'+str(dat.year)+','+' '+ str(dat.hour)+'h-'+str(dat.minute)+'mn-'+str(dat.second)+'s'
    event=[dat+'  '+'Ordre au marché d achat de '+str(quantité)+' token(s)'+' ,adresse emetteur:'+str(from_)]
    Blockchain.append(event)
    
    
    ordre=[index,'Ordre d achat marché',from_,quantité]
    Ordre.append(ordre)
    increment_index()
   
   
    best_ask=np.where(Carnet_dOrdres>0)[0][0]#best ask
    
    while quantité>0 and best_ask<N and quantité*best_ask<=Users[from_][1] :
        
        beneficiaire=[]
         
            
        for i in range(len(Ordre)):
            if quantité>0 and Ordre[i][1]=='Ordre limite de vente' :
                u=Ordre[i][4]
                if u==best_ask:
                    beneficiaire.append([Ordre[i][0],Ordre[i][2],min(quantité,Ordre[i][3])])
                    quantité-=min(quantité,Ordre[i][3])

        for j in range(len(beneficiaire)):
            if Users[beneficiaire[j][1]][2]>=beneficiaire[j][2]:
                transferer_token(beneficiaire[j][1] ,from_,beneficiaire[j][2])
                transferer_cash(from_,beneficiaire[j][1],best_ask*beneficiaire[j][2])

                for k in range(len(Ordre)):
                        if Ordre[k][0]==beneficiaire[j][0]:
                            Ordr=Ordre[k]                              
                            break
                if beneficiaire[j][2]==Ordr[3]:
                    supprimer_ordre(beneficiaire[j][1],beneficiaire[j][0])
                else:   
                    Carnet_dOrdres[best_ask]-=beneficiaire[j][2]
                    Ordr[3]-=beneficiaire[j][2]

        best_ask+=1
    
    
    
   


# In[13]:


def ordre_vente_marché(from_,quantité):
    
    dat=datetime.datetime.now()
    dat=str(dat.day)+'/'+str(dat.month)+'/'+str(dat.year)+','+' '+ str(dat.hour)+'h-'+str(dat.minute)+'mn-'+str(dat.second)+'s'
    event=[dat+'  '+'Ordre au marché de vente de '+str(quantité_init)+' token(s)'+' ,adresse emetteur:'+str(from_)]
    Blockchain.append(event)
    
    ordre=[index,'Ordre de vente marché',from_,quantité]
    Ordre.append(ordre)
    increment_index()
    quantité_init=quantité

    best_bid=np.where(Carnet_dOrdres<0)[0][-1]  #best bid

    while quantité>0 and best_bid>=0 and quantité<=Users[from_][2]:
        
        acheteur=[]
    
        for i in range(len(Ordre)):
            if quantité>0 and Ordre[i][1]=='Ordre limite d achat' :
                u=Ordre[i][4]
                if u==best_bid:
                    acheteur.append([Ordre[i][0],Ordre[i][2],min(quantité,Ordre[i][3])])
                    quantité-=min(quantité,Ordre[i][3])
        
        for j in range(len(acheteur)):
            if Users[acheteur[j][1]][1]>=acheteur[j][2]*best_bid:
                transferer_token(from_,acheteur[j][1],acheteur[j][2])
                transferer_cash(acheteur[j][1],from_,best_bid*acheteur[j][2])
                
                for k in range(len(Ordre)):
                        if Ordre[k][0]==acheteur[j][0]:
                            Ordr=Ordre[k]                              
                            break
                if acheteur[j][2]==Ordr[3]:
                    supprimer_ordre(acheteur[j][1],acheteur[j][0])
                else:   
                    Carnet_dOrdres[best_bid]+=acheteur[j][2]
                    Ordr[3]-=acheteur[j][2]
        
        
        best_bid-=1

    


# # Tests

# In[14]:


Users


# In[18]:


Ordre


# In[16]:


ordre_limit_achat(5,2,23)
ordre_limit_achat(6,3,24)
ordre_limit_achat(7,4,22)
ordre_limit_achat(8,3,22)
ordre_limit_achat(9,2,21)


# In[17]:


ordre_limit_vente(1,5,25)
ordre_limit_vente(2,4,26)
#ordre_limit_vente(4,2,26)
#ordre_limit_vente(0,8,26)
#ordre_limit_vente(5,3,27)


# In[335]:


ordre_limit_vente(5,51,21)


# In[318]:


supprimer_ordre(5,12)


# In[375]:


transferer_cash(8,3,100)
transferer_cash(9,3,100)


# In[384]:


ordre_achat_marché(3,7)


# In[19]:


Blockchain


# In[20]:


figure = plt.figure(figsize=(15,10))
plt.vlines([t for t in range(0,N)],[0] ,Carnet_dOrdres)
plt.xscale('linear')
#plt.setp(axes, xticks=[0.1, 0.5, 0.9], 
#xticks=np.arange(10, 30, step=1)
#figure.xaxis.set_ticks( xticks )
axes = plt.gca()
axes.xaxis.set_ticks(range(50))
plt.show()


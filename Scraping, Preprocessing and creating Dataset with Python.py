from bs4 import BeautifulSoup
import requests
import xlsxwriter 

user_agent = {'User-agent': 'Mozilla/5.0'}
url = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?view=detailed&page="
sayfaIndex = ["0","1","2","3","4","5"]
#sayfaIndex = ["0"]
sayac = 0
workbook = xlsxwriter.Workbook('veriSeti.xlsx') 
islenmemis = workbook.add_worksheet("İşlenmemiş Veri") 
islenmis = workbook.add_worksheet("Ön işlemeden geçmiş veri")
satir = 0
sutun = 0


for index in sayfaIndex:
    r = requests.get(url+index, headers = user_agent)
    source = BeautifulSoup(r.content,"lxml")
    oyunlar = source.find_all("td",attrs={"class":"clamp-summary-wrap"})
    
    for oyun in oyunlar:
        oyunAdi = oyun.find("a",attrs={"class":"title"}).text.lstrip().rstrip()
        platform = oyun.find("span",attrs={"class":"data"}).text.lstrip().rstrip()
        metaScore = oyun.find("div", attrs={"class":"clamp-metascore"}).findChildren()[1].text.lstrip().rstrip()
        userScore = oyun.find("div", attrs={"class":"clamp-userscore"}).findChildren()[1].text.lstrip().rstrip()
        if userScore == "tbd":
            continue
        cikisTarihi = oyun.find("div", attrs={"class":"clamp-details"}).findChildren()[3].text.split(", ")[1].lstrip().rstrip()
        metaScore=float(metaScore)
        oyunUrl = oyun.find("a",attrs={"class":"title"},href=True)
        oyunUrl = "https://www.metacritic.com"+oyunUrl["href"]
        r2 = requests.get(oyunUrl, headers = user_agent)
        source2 = BeautifulSoup(r2.content,"lxml")
        developerCompany = source2.find("span",attrs={"class":"data"}).text.split(",")[0].lstrip().rstrip()
        genres = source2.find("li",attrs={"class":"product_genre"}).findChildren()
        sayac = sayac+1
        print(sayac)

        icerik = [oyunAdi,platform,metaScore,userScore,cikisTarihi,developerCompany,genres[2].text]
    
        for detay in icerik:
            islenmemis.write(satir, sutun, detay)
            sutun += 1
    
        sutun = 0
        satir += 1

print("TARAMA TAMAMLANDI!")
import numpy as np
import pandas as pd

data_xlsx = pd.read_excel('veriSeti.xlsx', 'İşlenmemiş Veri', index_col=False)
data_xlsx.to_csv('csvfile.csv', encoding='utf-8', index=True)
dataset = pd.read_csv('csvfile.csv')

X = dataset.iloc[:,[True,False,True,True,True,True,True,True]].values
encodeIndex = [1,4,5,6]
scaleIndex = [2,3]
    
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder 
from sklearn.compose import ColumnTransformer 

sc = StandardScaler()

oyunAddi = dataset.iloc[:, 1].values
platformIsleme = dataset.iloc[:, 2].values  #encoded
metascoreIsleme = sc.fit_transform(X[:, 2:3]) #scaled
userscoreIsleme = sc.fit_transform(X[:, 3:4]) #scaled
yearIsleme = dataset.iloc[:, 5].values      #encoded
developerIsleme = dataset.iloc[:, 6].values #encoded
categoryIsleme = dataset.iloc[:, 7].values  #encoded

columnTransformer = ColumnTransformer([('encoder', OneHotEncoder(), [0])], remainder='passthrough') 
platformIsleme = pd.get_dummies(platformIsleme)
platformIsleme = np.array(platformIsleme)
platformIsleme = np.array(columnTransformer.fit_transform(platformIsleme), dtype = np.str) 

yearIsleme = pd.get_dummies(yearIsleme)
yearIsleme = np.array(yearIsleme)
yearIsleme = np.array(columnTransformer.fit_transform(yearIsleme), dtype = np.str) 

developerIsleme = pd.get_dummies(developerIsleme)
developerIsleme = np.array(developerIsleme)
developerIsleme = np.array(columnTransformer.fit_transform(developerIsleme), dtype = np.str) 

categoryIsleme = pd.get_dummies(categoryIsleme)
categoryIsleme = np.array(categoryIsleme)
categoryIsleme = np.array(columnTransformer.fit_transform(categoryIsleme), dtype = np.str)
print(platformIsleme)

satir=1
sutun=0
islenenler = [oyunAddi,platformIsleme,metascoreIsleme,userscoreIsleme,yearIsleme,developerIsleme,categoryIsleme]
for islenen in islenenler:
    for detay in islenen:
        islenmis.write(satir,sutun,str(detay))
        satir = satir+1

    satir=1
    sutun = sutun+1

workbook.close()
print("YAZMA TAMAMLANDI !!")

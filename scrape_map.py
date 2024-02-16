from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver = webdriver.Chrome()  
driver.get("https://www.google.com/maps")

# Data untuk referensi nama daerah
data = pd.read_csv('ifls_cleaned_new.csv')  

latitudes = []
longitudes = []

for index, row in data.iterrows():
    search_box = driver.find_element(By.ID,"searchboxinput")
    search_box.clear()
    search_box.send_keys(row['merge_kecamatan'])
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)  # Tunggu beberapa detik untuk memuat hasil pencarian
    url = driver.current_url
    if '@' in url:
        coordinates = url.split('@')[1].split(',')[0:2]
        latitudes.append(coordinates[0])
        longitudes.append(coordinates[1])
    else:
        latitudes.append(None)
        longitudes.append(None)
    
    print(latitudes,longitudes)

# Menambahkan data latitude dan longitude ke data referensi
data['Latitude'] = latitudes
data['Longitude'] = longitudes

# Export data menjadi file csv
data.to_csv('data_with_coordinates.csv', index=False)
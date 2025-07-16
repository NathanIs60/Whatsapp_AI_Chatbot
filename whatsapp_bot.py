from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

from ai_cevap import ai_mesaj_cevapla

calisiyor = True #calışma durumu
driver_path = r"C:\\Program Files\~\chromedriver.exe" #Bilgisayarınızda kullanılan chromedriver.exe yolu
service = Service(driver_path) #driver servisi(Başlatıcağı yol)
driver = webdriver.Chrome(service=service) #Chrome'u bailat

driver.get("https://web.whatsapp.com") #Gidilecek alan
print("Qr Girişi Bekleniyorr...")
input()#Giriş Bekleniyor

def oku_mesajla(): 
    try:
        mesajlar = driver.find_elements(By.CLASS_NAME, "_21Ahp") #Mesaj kutusununn HTML obje sınıfı '_21Ahp'
        if len(mesajlar) == 0:
            print("Henüz mesaj yok.")
            return
        son_mesaj = mesajlar[-1].text.lower() #Eklenen son mesajı al
        print("Yeni Mesaj: " + son_mesaj)

        cevap = ai_mesaj_cevapla(son_mesaj) # yapay zeka kullanarak cevapla

        mesaj_veri = driver.find_element(By.CLASS_NAME, "_3Uu1_") #İnput HTML giriş kutusu
        mesaj_veri.click() # Alana Tıkla
        mesaj_veri.send_keys(cevap + Keys.ENTER) #Cevabı imput'a gir ve Enter tuşuna bas
        print("Cevap Gönderildi")

    except Exception as e:
        print("Hata Oluştu: " + str(e))

while calisiyor:
    oku_mesajla() #botu çalıştır
    time.sleep(5)

    print("Bot çalışıyor, durdurmak için 'q' yaz ve Enter'a bas.")
    komut = input()
    if komut.lower() == 'q': #girilen komut "q" ise çıkış yap
        calisiyor = False
        print("Bot kapatılıyor...")

driver.quit() #sekmeyi kapat

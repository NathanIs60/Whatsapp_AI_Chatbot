from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

from ai_answer import ai_message_answer

calisiyor = True  # working status
driver_path = r"C:\\Program Files\~\chromedriver.exe"  # Path to chromedriver.exe on your computer
service = Service(driver_path)  # Initialize ChromeDriver service
driver = webdriver.Chrome(service=service)  # Launch Chrome

driver.get("https://web.whatsapp.com")  # Open WhatsApp Web
print("Waiting for QR login...")
input()  # Wait for user to scan QR

def oku_mesajla(): 
    try:
        mesajlar = driver.find_elements(By.CLASS_NAME, "_21Ahp")  # Message HTML class name
        if len(mesajlar) == 0:
            print("No messages yet.")
            return
        son_mesaj = mesajlar[-1].text.lower()  # Get the last message
        print("New message: " + son_mesaj)

        cevap = ai_message_answer(son_mesaj)  # Generate reply using AI

        mesaj_veri = driver.find_element(By.CLASS_NAME, "_3Uu1_")  # Input field for sending message
        mesaj_veri.click()  # Click the input area
        mesaj_veri.send_keys(cevap + Keys.ENTER)  # Type the reply and press Enter
        print("Reply sent")

    except Exception as e:
        print("An error occurred: " + str(e))

while calisiyor:
    oku_mesajla()  # run the bot
    time.sleep(5)

    print("Bot is running, type 'q' and press Enter to stop.")
    komut = input()
    if komut.lower() == 'q':  # if user types 'q', stop the bot
        calisiyor = False
        print("Shutting down the bot...")

driver.quit()  # close browser tab

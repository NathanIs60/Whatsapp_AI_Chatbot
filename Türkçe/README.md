# Whatsap AI ChatBot (OpenAı + Selenium) (Turkish)

Bu proje, WhatsApp Web'e gelen mesajlara GPT-3.5-turbo veya kullandığınız herhangi bir OpenAI modelini kullanarak otomatik cevap veren bir yapay zeka botudur.

## 📚Özellikler:
-WhatsApp Web'deki sohbetlerdeki mesajları okur
-OpenAI API ile doğal ve sohbet tarzında cevaplar üretir
-Cevabı otomatik olarak WhatsApp Web içindeki giriş alanına yazar ve mesajı gönderir

## 🛠️ Kurulum:
 -Python 3.10 veya 3.11 sürümleri kurlu olmalı
  Gerekli Kütüphaneler: Selenium, OpenAI isteğe ve kullanıma göre pywhatkit:
  ```bash
  pip install openai
  pip install selenium
  pip install pywhatkit 
```

## ❗Dikkat:
    - `ai_cevap.py` içinde kendi OpenAI API anahtarını gir:
    ```python
    openai.api_key = "API_ANAHTARIN"
    ```
    -Yapay zeka modelinizin ayarlarını aşağıdaki alanda değiştirebilirsiniz(`ai_cevap.py`), içinde.
    ```python
    response = openai.chat.completions.create( #ChatBot oluşturma eski sürümlerde ".ChatCompletions" kullanılabilinir
            model="gpt-3.5-turbo",#Chatnot Modeli
            messages=[
                {"role": "system", "content": "Sen bir arkadaş gibi konuşan chatbot'sun."}, #ChatBot  Rol Alanı
                {"role": "user", "content": mesaj}
            ]
        )
    ```
## 🌐 Dil Desteği:
    -Türkçe ve İngilizce


# WhatsApp AI ChatBot (OpenAI + Selenium)(English)

This project is an AI bot that automatically replies to messages received on WhatsApp Web using GPT-3.5-turbo or any OpenAI model you choose.

## 📚 Features:
- Reads messages from chats on WhatsApp Web  
- Generates natural and conversational replies using the OpenAI API  
- Automatically writes the reply in the input field of WhatsApp Web and sends the message

## 🛠️ Installation:
- Python versions 3.10 or 3.11 should be installed  
- Required libraries: Selenium, OpenAI, and optionally pywhatkit:  
```bash
pip install openai
pip install selenium
pip install pywhatkit
```

## ❗Dikkat:
    - `ai_cevap.py` Insert your own OpenAI API key inside:
    ```python
    openai.api_key = "API_ANAHTARIN"
    ```
    -You can change your AI model settings in the following section inside(`ai_cevap.py`):
    ```python
    response = openai.chat.completions.create( #ChatBot oluşturma eski sürümlerde ".ChatCompletions" kullanılabilinir
            model="gpt-3.5-turbo",#Chatnot Modeli
            messages=[
                {"role": "system", "content": "Sen bir arkadaş gibi konuşan chatbot'sun."}, #ChatBot  Rol Alanı
                {"role": "user", "content": mesaj}
            ]
        )
    ```
## 🌐 Language Support:
    -Turkish and English
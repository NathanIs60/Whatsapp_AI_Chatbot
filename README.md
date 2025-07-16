# WhatsApp AI ChatBot - Gelişmiş Çoklu AI Desteği

## 🚀 Yeni Özellikler:
- **Çoklu AI Desteği**: OpenAI, Claude (Anthropic), DeepSeek
- **Grafik Kullanıcı Arayüzü**: Kolay kullanım için modern GUI
- **EXE Dosya Desteği**: Kurulum gerektirmeden çalışır
- **API Anahtar Yönetimi**: Güvenli anahtar saklama
- **Dinamik AI Seçimi**: Farklı AI'lar arasında anında geçiş

## 📚 Özellikler:
- WhatsApp Web'deki sohbetlerdeki mesajları okur
- **OpenAI, Claude ve DeepSeek** API'leri ile doğal cevaplar üretir
- Cevabı otomatik olarak WhatsApp Web'e yazar ve gönderir
- Kullanıcı dostu kontrol paneli
- API anahtarlarını güvenli şekilde saklar
- Gerçek zamanlı durum bildirimleri

## 🛠️ Hızlı Kurulum:
1. `setup.bat` dosyasını çalıştırın (Windows)
2. `build.bat` dosyasını çalıştırarak EXE dosyalarını oluşturun
3. `AI_Manager.exe` dosyasını çalıştırın

### Manuel Kurulum:
```bash
pip install -r requirements.txt
python ai_manager.py
```

## 🔑 API Anahtarları:
### OpenAI:
1. https://platform.openai.com/ adresine gidin
2. API anahtarınızı oluşturun
3. GUI'den "OpenAI API Key" alanına girin

### Claude (Anthropic):
1. https://console.anthropic.com/ adresine gidin
2. API anahtarınızı oluşturun
3. GUI'den "Claude API Key" alanına girin

### DeepSeek:
1. https://platform.deepseek.com/ adresine gidin
2. API anahtarınızı oluşturun
3. GUI'den "DeepSeek API Key" alanına girin

## 📱 Kullanım:
1. AI Manager'ı çalıştırın
2. İstediğiniz AI'ı seçin
3. API anahtarlarınızı girin ve kaydedin
4. Sorunuzu yazın ve "Gönder" butonuna tıklayın

## 🌐 Dil Desteği:
- Türkçe ve İngilizce
- Çoklu dil desteği AI ayarlarından yapılandırılabilir


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
  openai.api_key = "API_KEY"
  ```
  -You can change your AI model settings in the following section inside(`ai_cevap.py`):
  ```python
  response = openai.chat.completions.create( # For creating the ChatBot; in older versions, ".ChatCompletions" may be used
          model="gpt-3.5-turbo",#Chatnot Modeli
          messages=[
              {"role": "system", "content": "Sen bir arkadaş gibi konuşan chatbot'sun."}, #ChatBot Role Section
              {"role": "user", "content": mesaj}
          ]
      )
  ```
## 🌐 Language Support:
    -Turkish and English

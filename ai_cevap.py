import openai

openai.api_key = "API_ANAHTARI"

def ai_mesaj_cevapla(mesaj):
    try:
        response = openai.chat.completions.create( #ChatBot oluşturma eski sürümlerde ".ChatCompletions" kullanılabilinir
            model="gpt-3.5-turbo",#Chatnot Modeli
            messages=[
                {"role": "system", "content": "Sen bir arkadaş gibi konuşan chatbot'sun."}, #ChatBot  Rol Alanı
                {"role": "user", "content": mesaj}
            ]
        )
        return response['choices'][0]['message']['content'] #API'den gelen cevabı döndür
    except Exception as e:
        print("Hata:", e)
        return "Cevap Üretilemedi"
#API KEY alanını OpenAI'ın Resmi sayfasından uygun ücret ve plana göre alabilir yada başka bir api kullanabilirsiniz.
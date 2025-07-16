import openai
import requests
import json
import time
from datetime import datetime

# Anthropic API (Claude)
try:
    import anthropic
except ImportError:
    anthropic = None

class AIResponseManager:
    def __init__(self, config_file="ai_config.json"):
        """
        AI Yanıt Yöneticisi - Birden fazla AI servisini destekler
        """
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self):
        """Yapılandırma dosyasını yükle"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "openai_api_key": "",
                "claude_api_key": "", 
                "deepseek_api_key": "",
                "ollama_url": "http://localhost:11434",
                "ollama_model": "deepseek-coder:6.7b",
                "default_ai": "openai",
                "settings": {
                    "temperature": 0.7,
                    "max_tokens": 1000,
                    "system_message": "Sen yardımcı bir AI asistanısın. Türkçe sorulara Türkçe cevap ver."
                }
            }
    
    def save_config(self):
        """Yapılandırmayı kaydet"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def get_openai_response(self, message):
        """OpenAI API'sinden yanıt al"""
        api_key = self.config.get("openai_api_key", "")
        if not api_key:
            return "OpenAI API anahtarı yapılandırılmamış!"
        
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.config["settings"]["system_message"]},
                    {"role": "user", "content": message}
                ],
                max_tokens=self.config["settings"]["max_tokens"],
                temperature=self.config["settings"]["temperature"]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI API Hatası: {str(e)}"
    
    def get_claude_response(self, message):
        """Claude API'sinden yanıt al"""
        if not anthropic:
            return "Anthropic kütüphanesi yüklü değil. pip install anthropic komutu ile yükleyin."
            
        api_key = self.config.get("claude_api_key", "")
        if not api_key:
            return "Claude API anahtarı yapılandırılmamış!"
        
        try:
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=self.config["settings"]["max_tokens"],
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Claude API Hatası: {str(e)}"
    
    def get_deepseek_response(self, message):
        """DeepSeek API'sinden yanıt al"""
        api_key = self.config.get("deepseek_api_key", "")
        if not api_key:
            return "DeepSeek API anahtarı yapılandırılmamış!"
        
        try:
            url = "https://api.deepseek.com/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": self.config["settings"]["system_message"]},
                    {"role": "user", "content": message}
                ],
                "max_tokens": self.config["settings"]["max_tokens"],
                "temperature": self.config["settings"]["temperature"]
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"DeepSeek API Hatası: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"DeepSeek API Hatası: {str(e)}"
    
    def get_ollama_response(self, message):
        """Ollama (Local AI) API'sinden yanıt al"""
        ollama_url = self.config.get("ollama_url", "http://localhost:11434")
        ollama_model = self.config.get("ollama_model", "deepseek-coder:6.7b")
        
        if not ollama_url:
            return "Ollama URL'si yapılandırılmamış!"
            
        try:
            url = f"{ollama_url}/api/generate"
            headers = {
                "Content-Type": "application/json"
            }
            
            # Sistem mesajı ile birlikte tam prompt oluştur
            system_message = self.config["settings"]["system_message"]
            full_prompt = f"{system_message}\n\nKullanıcı: {message}\n\nAsistan:"
            
            data = {
                "model": ollama_model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": self.config["settings"]["temperature"],
                    "num_predict": self.config["settings"]["max_tokens"]
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Yanıt alınamadı")
            else:
                return f"Ollama API Hatası: {response.status_code} - {response.text}"
                
        except requests.exceptions.ConnectionError:
            return "Ollama sunucusuna bağlanılamıyor. Ollama'ın çalıştığından emin olun."
        except Exception as e:
            return f"Ollama API Hatası: {str(e)}"
    
    def get_ai_response(self, message, ai_type="auto"):
        """Belirtilen AI'dan yanıt al"""
        if ai_type == "auto":
            ai_type = self.config.get("default_ai", "openai")
        
        # Log ekle
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {ai_type.upper()} ile sorgu işleniyor...")
        
        if ai_type.lower() == "openai":
            return self.get_openai_response(message)
        elif ai_type.lower() == "claude":
            return self.get_claude_response(message)
        elif ai_type.lower() == "deepseek":
            return self.get_deepseek_response(message)
        elif ai_type.lower() == "ollama" or ai_type.lower() == "deepseek (local)":
            return self.get_ollama_response(message)
        else:
            return f"Desteklenmeyen AI türü: {ai_type}"
    
    def update_api_key(self, ai_type, api_key):
        """API anahtarını güncelle"""
        key_mapping = {
            "openai": "openai_api_key",
            "claude": "claude_api_key",
            "deepseek": "deepseek_api_key"
        }
        
        if ai_type.lower() in key_mapping:
            self.config[key_mapping[ai_type.lower()]] = api_key
            self.save_config()
            return True
        return False
    
    def set_default_ai(self, ai_type):
        """Varsayılan AI'ı ayarla"""
        self.config["default_ai"] = ai_type.lower()
        self.save_config()
    
    def get_available_ais(self):
        """Kullanılabilir AI'ları listele"""
        available = []
        if self.config.get("openai_api_key"):
            available.append("OpenAI")
        if self.config.get("claude_api_key"):
            available.append("Claude")
        if self.config.get("deepseek_api_key"):
            available.append("DeepSeek")
        return available

# Eski dosyalarla uyumluluk için
def ai_mesaj_cevapla(mesaj, ai_type="auto"):
    """Türkçe versiyonla uyumluluk"""
    manager = AIResponseManager()
    return manager.get_ai_response(mesaj, ai_type)

def ai_message_answer(message, ai_type="auto"):
    """İngilizce versiyonla uyumluluk"""
    manager = AIResponseManager()
    return manager.get_ai_response(message, ai_type)

if __name__ == "__main__":
    # Test
    manager = AIResponseManager()
    print("AI Response Manager Test")
    print("Kullanılabilir AI'lar:", manager.get_available_ais())
    
    # Test mesajı
    test_message = "Merhaba, nasılsın?"
    response = manager.get_ai_response(test_message)
    print(f"Yanıt: {response}")


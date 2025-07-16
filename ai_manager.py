import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import threading
import requests
from datetime import datetime

# OpenAI API
try:
    import openai
except ImportError:
    openai = None

# Anthropic API (Claude)
try:
    import anthropic
except ImportError:
    anthropic = None

class AIManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Manager - Multiple AI Control Panel")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Yapılandırma dosyası
        self.config_file = "ai_config.json"
        self.load_config()
        
        self.setup_ui()
        
    def load_config(self):
        """Yapılandırma dosyasını yükle"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = {
                    "openai_api_key": "",
                    "claude_api_key": "",
                    "deepseek_api_key": "",
                    "last_selected_ai": "OpenAI"
                }
        except Exception as e:
            messagebox.showerror("Hata", f"Yapılandırma dosyası yüklenemedi: {e}")
            self.config = {
                "openai_api_key": "",
                "claude_api_key": "",
                "deepseek_api_key": "",
                "last_selected_ai": "OpenAI"
            }
    
    def save_config(self):
        """Yapılandırmayı kaydet"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Hata", f"Yapılandırma kaydedilemedi: {e}")
    
    def setup_ui(self):
        """Kullanıcı arayüzünü oluştur"""
        # Ana frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid yapılandırması
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # AI Seçimi
        ttk.Label(main_frame, text="AI Seçimi:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ai_var = tk.StringVar(value=self.config.get("last_selected_ai", "OpenAI"))
        self.ai_combo = ttk.Combobox(main_frame, textvariable=self.ai_var, values=["OpenAI", "Claude", "DeepSeek (API)", "DeepSeek (Local)"], state="readonly", width=20)
        self.ai_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.ai_combo.bind('<<ComboboxSelected>>', self.on_ai_change)
        
        # API Anahtarları Frame
        api_frame = ttk.LabelFrame(main_frame, text="API Anahtarları", padding="10")
        api_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        api_frame.columnconfigure(1, weight=1)
        
        # OpenAI API Key
        ttk.Label(api_frame, text="OpenAI API Key:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.openai_key_var = tk.StringVar(value=self.config.get("openai_api_key", ""))
        self.openai_key_entry = ttk.Entry(api_frame, textvariable=self.openai_key_var, show="*", width=50)
        self.openai_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # Claude API Key
        ttk.Label(api_frame, text="Claude API Key:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.claude_key_var = tk.StringVar(value=self.config.get("claude_api_key", ""))
        self.claude_key_entry = ttk.Entry(api_frame, textvariable=self.claude_key_var, show="*", width=50)
        self.claude_key_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # DeepSeek API Key
        ttk.Label(api_frame, text="DeepSeek API Key:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.deepseek_key_var = tk.StringVar(value=self.config.get("deepseek_api_key", ""))
        self.deepseek_key_entry = ttk.Entry(api_frame, textvariable=self.deepseek_key_var, show="*", width=50)
        self.deepseek_key_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # Local AI (Ollama) Ayarları
        ttk.Label(api_frame, text="Local AI (Ollama) URL:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.ollama_url_var = tk.StringVar(value=self.config.get("ollama_url", "http://localhost:11434"))
        self.ollama_url_entry = ttk.Entry(api_frame, textvariable=self.ollama_url_var, width=50)
        self.ollama_url_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # Ollama Model Seçimi
        ttk.Label(api_frame, text="Ollama Model:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.ollama_model_var = tk.StringVar(value=self.config.get("ollama_model", "deepseek-coder:6.7b"))
        self.ollama_model_combo = ttk.Combobox(api_frame, textvariable=self.ollama_model_var, 
                                              values=["deepseek-coder:6.7b", "deepseek-coder:33b", "llama2:7b", "llama2:13b", "codellama:7b", "mistral:7b"], 
                                              width=47)
        self.ollama_model_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # Ollama Test Butonu
        ttk.Button(api_frame, text="Ollama Bağlantısını Test Et", command=self.test_ollama_connection).grid(row=5, column=0, columnspan=2, pady=5)
        
        # Kaydet butonu
        ttk.Button(api_frame, text="Anahtarları Kaydet", command=self.save_api_keys).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Sorgu Frame
        query_frame = ttk.LabelFrame(main_frame, text="Sorgu", padding="10")
        query_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        query_frame.columnconfigure(0, weight=1)
        query_frame.rowconfigure(1, weight=1)
        
        ttk.Label(query_frame, text="Sorunuzu girin:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.query_text = scrolledtext.ScrolledText(query_frame, height=5, width=80)
        self.query_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Butonlar
        button_frame = ttk.Frame(query_frame)
        button_frame.grid(row=2, column=0, sticky=tk.W)
        
        self.send_button = ttk.Button(button_frame, text="Gönder", command=self.send_query)
        self.send_button.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(button_frame, text="Temizle", command=self.clear_query).grid(row=0, column=1, padx=(0, 10))
        
        # Sonuç Frame
        result_frame = ttk.LabelFrame(main_frame, text="Sonuç", padding="10")
        result_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(1, weight=1)
        
        ttk.Label(result_frame, text="AI Yanıtı:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.result_text = scrolledtext.ScrolledText(result_frame, height=10, width=80, state=tk.DISABLED)
        self.result_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid weight ayarları
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=2)
        
        # Durum çubuğu
        self.status_var = tk.StringVar(value="Hazır")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
    def on_ai_change(self, event=None):
        """AI seçimi değiştiğinde çağrılır"""
        self.config["last_selected_ai"] = self.ai_var.get()
        self.save_config()
        self.status_var.set(f"AI değiştirildi: {self.ai_var.get()}")
        
    def save_api_keys(self):
        """API anahtarlarını kaydet"""
        self.config["openai_api_key"] = self.openai_key_var.get()
        self.config["claude_api_key"] = self.claude_key_var.get()
        self.config["deepseek_api_key"] = self.deepseek_key_var.get()
        self.config["ollama_url"] = self.ollama_url_var.get()
        self.config["ollama_model"] = self.ollama_model_var.get()
        self.save_config()
        messagebox.showinfo("Başarılı", "API anahtarları ve Ollama ayarları kaydedildi!")
        self.status_var.set("Tüm ayarlar kaydedildi")
        
    def test_ollama_connection(self):
        """Ollama bağlantısını test et"""
        try:
            ollama_url = self.ollama_url_var.get()
            if not ollama_url:
                messagebox.showwarning("Uyarı", "Ollama URL'si girilmemiş!")
                return
                
            # Ollama'nın çalışıp çalışmadığını kontrol et
            test_url = f"{ollama_url}/api/tags"
            response = requests.get(test_url, timeout=5)
            
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                
                if model_names:
                    self.ollama_model_combo['values'] = model_names
                    messagebox.showinfo("Başarılı", f"Ollama bağlantısı başarılı!\n\nKullanılabilir modeller:\n" + "\n".join(model_names[:10]))
                else:
                    messagebox.showinfo("Başarılı", "Ollama bağlantısı başarılı ancak hiç model yüklü değil.")
                    
                self.status_var.set("Ollama bağlantısı başarılı")
            else:
                messagebox.showerror("Hata", f"Ollama bağlantısı başarısız: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Bağlantı Hatası", "Ollama sunucusuna bağlanılamıyor.\nOllama'ın çalıştığından emin olun.")
        except Exception as e:
            messagebox.showerror("Hata", f"Ollama testi sırasında hata: {str(e)}")
        
    def clear_query(self):
        """Sorgu alanını temizle"""
        self.query_text.delete(1.0, tk.END)
        
    def send_query(self):
        """Sorguyu seçili AI'ya gönder"""
        query = self.query_text.get(1.0, tk.END).strip()
        if not query:
            messagebox.showwarning("Uyarı", "Lütfen bir sorgu girin!")
            return
            
        ai_type = self.ai_var.get()
        
        # Buton durumunu değiştir
        self.send_button.config(state=tk.DISABLED)
        self.status_var.set(f"{ai_type} ile iletişim kuruluyor...")
        
        # Thread ile sorguyu gönder
        thread = threading.Thread(target=self.process_query, args=(query, ai_type))
        thread.daemon = True
        thread.start()
        
    def process_query(self, query, ai_type):
        """Sorguyu işle"""
        try:
            if ai_type == "OpenAI":
                response = self.query_openai(query)
            elif ai_type == "Claude":
                response = self.query_claude(query)
            elif ai_type == "DeepSeek (API)":
                response = self.query_deepseek(query)
            elif ai_type == "DeepSeek (Local)":
                response = self.query_ollama(query)
            else:
                response = "Geçersiz AI seçimi!"
                
            # UI'yi güncelle
            self.root.after(0, self.update_result, response)
            
        except Exception as e:
            self.root.after(0, self.update_result, f"Hata: {str(e)}")
        finally:
            self.root.after(0, self.enable_send_button)
            
    def query_openai(self, query):
        """OpenAI API'sini kullan"""
        if not openai:
            return "OpenAI kütüphanesi yüklü değil. pip install openai komutu ile yükleyin."
            
        api_key = self.config.get("openai_api_key", "")
        if not api_key:
            return "OpenAI API anahtarı girilmemiş!"
            
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sen yardımcı bir AI asistanısın. Türkçe sorulara Türkçe cevap ver."},
                    {"role": "user", "content": query}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI API Hatası: {str(e)}"
            
    def query_claude(self, query):
        """Claude API'sini kullan"""
        if not anthropic:
            return "Anthropic kütüphanesi yüklü değil. pip install anthropic komutu ile yükleyin."
            
        api_key = self.config.get("claude_api_key", "")
        if not api_key:
            return "Claude API anahtarı girilmemiş!"
            
        try:
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": query}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Claude API Hatası: {str(e)}"
            
    def query_deepseek(self, query):
        """DeepSeek API'sini kullan"""
        api_key = self.config.get("deepseek_api_key", "")
        if not api_key:
            return "DeepSeek API anahtarı girilmemiş!"
            
        try:
            url = "https://api.deepseek.com/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Sen yardımcı bir AI asistanısın. Türkçe sorulara Türkçe cevap ver."},
                    {"role": "user", "content": query}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return f"DeepSeek API Hatası: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"DeepSeek API Hatası: {str(e)}"
            
    def query_ollama(self, query):
        """Ollama (Local AI) kullan"""
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
            system_message = "Sen yardımcı bir AI asistanısın. Türkçe sorulara Türkçe cevap ver."
            full_prompt = f"{system_message}\n\nKullanıcı: {query}\n\nAsistan:"
            
            data = {
                "model": ollama_model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 1000
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
            
    def update_result(self, result):
        """Sonucu güncelle"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # Zaman damgası ekle
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.result_text.insert(tk.END, f"[{timestamp}] {self.ai_var.get()} Yanıtı:\n\n")
        self.result_text.insert(tk.END, result)
        
        self.result_text.config(state=tk.DISABLED)
        self.status_var.set("Yanıt alındı")
        
    def enable_send_button(self):
        """Gönder butonunu aktif et"""
        self.send_button.config(state=tk.NORMAL)
        
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Uygulama kapatılırken çağrılır"""
        self.save_config()
        self.root.destroy()

if __name__ == "__main__":
    app = AIManager()
    app.run()


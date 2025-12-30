import unicodedata
import re
import google.generativeai as genai


MY_API_KEY = "AIzaSyBYzAp2edMFSQRncKiFwROLNEbwXEph-AY" 

try:
    genai.configure(api_key=MY_API_KEY)
except Exception as e:
    pass

def normalize_text(text):
    text = text.lower()
    text = text.replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ı', 'i').replace('ö', 'o').replace('ç', 'c')
    return text

def check_emergency(description):
    """
    Acil durum kontrolü - Geliştirilmiş Liste
    """
    description = normalize_text(description)
    
    
    critical_keywords = [
        'kalp krizi', 'nefes alamiyorum', 'boguluyorum', 'bilinc', 'bayildi', 
        'kanama', 'bicak', 'silah', 'felc', 'konusamiyor', 'gogus agrisi',
        'intihar', 'hap icti', 'zehirlenme', 'kaza', 'trafik kazasi', 'nabiz yok', 
        'koma', 'kaptirdim', 'is kazasi', 'kopma', 'parcalanma', 'ezilme', 
        'uzuv', 'makine', 'patlama', 'yanik', 'elektrik carpmasi'
    ]
    
    for word in critical_keywords:
        if word in description:
            return True
    return False


def get_ai_specialty_api(description):
    if "BURAYA" in MY_API_KEY or len(MY_API_KEY) < 10:
        return None

    system_prompt = "Sen tıbbi asistansın. Şikayete uygun branşı tek kelimeyle yaz. Liste: Kardiyoloji, Dahiliye, Ortopedi, Kulak Burun Boğaz, Göz Hastalıkları, Nöroloji, Psikiyatri, Dermatoloji, Genel Cerrahi, Fizik Tedavi, Üroloji"

    
    models_to_try = [
        'gemini-flash-latest',    
        'gemini-2.5-flash',       
        'gemini-2.0-flash',       
        'gemini-pro-latest',      
    ]

    for model_name in models_to_try:
        try:
            
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(f"{system_prompt}\nŞikayet: {description}")
            
            
            result = clean_response(response.text)
            if result:
                print(f"Başarılı Model: {model_name}") 
                return result
                
        except Exception as e:
            
            print(f"Model Hatası ({model_name}): {e}")
            continue 

    return None
def clean_response(text):
    """Gelen cevabı temizler"""
    text = text.strip()
    valid_specialties = ['Kardiyoloji', 'Dahiliye', 'Ortopedi', 'Kulak Burun Boğaz', 'Göz Hastalıkları', 'Nöroloji', 'Psikiyatri', 'Dermatoloji', 'Genel Cerrahi', 'Fizik Tedavi', 'Üroloji']
    for spec in valid_specialties:
        if spec in text:
            return spec
    return None


def get_ai_specialty_keyword(description):
    clean_desc = normalize_text(description)
    
    keywords = {
        'Kardiyoloji': {'puan': 0, 'kelimeler': ['kalp', 'kalb', 'gogus', 'damar', 'sol kol', 'tansiyon', 'nabiz', 'carpinti', 'sikisma', 'kriz', 'stent', 'anjiyo']},
        'Dahiliye': {'puan': 0, 'kelimeler': ['mide', 'midem', 'karin', 'bagirsak', 'ciger', 'halsizlik', 'kusma', 'bulanti', 'ishal', 'kabiz', 'gaz', 'reflu', 'seker', 'diyabet']},
        'Ortopedi': {'puan': 0, 'kelimeler': ['kemik', 'kirik', 'cikik', 'incinme', 'burkulma', 'meniskus', 'kopma', 'ezilme', 'kireclenme', 'platin', 'alci', 'ayak', 'bacak', 'kol', 'omuz', 'bilek', 'diz']},
        'Kulak Burun Boğaz': {'puan': 0, 'kelimeler': ['kulak', 'burun', 'burn', 'bogaz', 'geniz', 'bademcik', 'sinuzit', 'isitme', 'cinlama', 'vertigo', 'bas donmesi', 'yutkunma', 'ses', 'horlama', 'akinti']},
        'Göz Hastalıkları': {'puan': 0, 'kelimeler': ['goz', 'gorme', 'bulanik', 'arpacik', 'batma', 'kasinti', 'sulanma', 'capak', 'miyop', 'astigmat', 'gozluk', 'lens']},
        'Nöroloji': {'puan': 0, 'kelimeler': ['bas agrisi', 'migren', 'beyin', 'unutkanlik', 'titreme', 'parkinson', 'alzheimer', 'epilepsi', 'sara', 'felc', 'inme', 'uyusma', 'denge']},
        'Psikiyatri': {'puan': 0, 'kelimeler': ['uyku', 'depresyon', 'kaygi', 'sinir', 'stres', 'mutsuz', 'panik', 'takinti', 'bunalim', 'ruh', 'korku', 'halusinasyon', 'ofke', 'psikolo', 'manik', 'bipolar', 'dikkat', 'odak', 'hisset']},
        'Dermatoloji': {'puan': 0, 'kelimeler': ['cilt', 'deri', 'kasinti', 'sivilce', 'akne', 'leke', 'ben', 'kizariklik', 'egzama', 'mantar', 'dokuntu', 'sac', 'kepek', 'sigil', 'sedef', 'yanik']},
        'Genel Cerrahi': {'puan': 0, 'kelimeler': ['ameliyat', 'fitik', 'apandisit', 'safra', 'hemoroid', 'basur', 'meme', 'kitle', 'yara', 'dikis']},
        'Fizik Tedavi': {'puan': 0, 'kelimeler': ['bel fitigi', 'boyun fitigi', 'sirt', 'tutulma', 'kramp', 'romatizma', 'durus', 'egzersiz', 'fizik']},
        'Üroloji': {'puan': 0, 'kelimeler': ['idrar', 'prostat', 'bobrek', 'bobreg', 'tasi', 'kum', 'yumurtalik', 'kisirlik', 'sanci', 'mesane']}
    }
    
    for speciality, data in keywords.items():
        for word in data['kelimeler']:
            if word in clean_desc:
                if word in ['kalp', 'kalb', 'goz', 'kulak', 'burun', 'burn', 'prostat', 'fitik', 'ameliyat', 'kirik', 'cilt', 'psikolo']:
                    data['puan'] += 3
                else:
                    data['puan'] += 1
                    
    best_match = None
    highest_score = 0
    
    for speciality, data in keywords.items():
        if data['puan'] > highest_score:
            highest_score = data['puan']
            best_match = speciality
            
    return best_match


def get_ai_specialty(description):
    print(f" AI Analizi Başlıyor: '{description}'")
    
    
    api_result = get_ai_specialty_api(description)
    if api_result:
        print(f" Gemini API Tahmini: {api_result}")
        return api_result
    
    
    print(" API çalışmadı, Yedek Sisteme (Kural Tabanlı) geçiliyor...")
    keyword_result = get_ai_specialty_keyword(description)
    print(f"Yedek Sistem Tahmini: {keyword_result}")
    return keyword_result
"""
TRAIT AirportAI - Multilingual Engine
Supports English (en), Hindi (hi), Spanish (es), French (fr), German (de), Arabic (ar)
Provides zero-cost offline language detection, intent matching, and localized templates.
"""

import re
from typing import Dict, Any, Tuple

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "हिन्दी (Hindi)",
    "es": "Español (Spanish)",
    "fr": "Français (French)",
    "de": "Deutsch (German)",
    "ar": "العربية (Arabic)"
}

# Common language detection keywords and Unicode script ranges
SCRIPT_RANGES = {
    "hi": re.compile(r"[\u0900-\u097F]"),  # Devanagari
    "ar": re.compile(r"[\u0600-\u06FF\u0750-\u077F]"),  # Arabic
}

KEYWORD_MAP = {
    "en": ["where", "what", "how", "when", "is", "flight", "gate", "baggage", "luggage", "terminal", "counter", "status", "allowance", "check-in", "security", "wifi", "lounge"],
    "es": ["donde", "dónde", "vuelo", "puerta", "equipaje", "maleta", "baño", "horario", "llegada", "salida", "facturacion", "mostrador", "cuál", "cómo"],
    "fr": ["ou", "où", "vol", "porte", "bagage", "valise", "toilette", "retard", "arrivee", "depart", "enregistrement", "combien", "est-ce"],
    "de": ["wo", "flug", "flugsteig", "gepäck", "koffer", "toilette", "verspätung", "ankunft", "abflug", "abfertigung", "warten", "wie"],
    "hi": ["kahan", "kidhar", "samay", "kitna", "viman", "bag", "chal", "saman", "kya", "kaise"],
}

# Response localization dictionary

LOCALIZED_TEMPLATES = {
    "en": {
        "flight_found": "Here is the real-time operational status for flight {flight_number} ({airline}):",
        "gate_info": "Boarding Gate: {gate} in {terminal}. Estimated walking time from Security is approximately {walk_time} minutes.",
        "baggage_info": "Baggage Claim: Assigned to {carousel} in {terminal}.",
        "checkin_info": "Check-in Desks: Located at {checkin_desks}.",
        "status_notice": "Current Flight Status: {status} (Delay: {delay} mins).",
        "greeting": "Hello! I am TRAIT AirportAI, your real-time intelligent passenger assistant. How may I assist you with flights, gates, baggage, or airport facilities today?",
        "not_found": "I couldn't locate specific records for that inquiry. Please enter a valid flight number (e.g., AI-204, 6E-531, BA-142) or ask about gates, baggage, lounges, or Wi-Fi.",
        "prompts": ["Status of AI-204", "Where is Gate 24?", "Baggage claim for 6E-531", "Encalm Lounge locations", "Wi-Fi connection guide"]
    },
    "hi": {
        "flight_found": "उड़ान {flight_number} ({airline}) के लिए वर्तमान परिचालन स्थिति:",
        "gate_info": "बोर्डिंग गेट: {terminal} में {gate}। सुरक्षा जांच से पैदल दूरी लगभग {walk_time} मिनट है।",
        "baggage_info": "बैगेज बेल्ट: {terminal} में {carousel}।",
        "checkin_info": "चेक-इन काउंटर: {checkin_desks}।",
        "status_notice": "उड़ान स्थिति: {status} (विलंब: {delay} मिनट)।",
        "greeting": "नमस्ते! मैं TRAIT AirportAI हूँ, आपका वास्तविक समय हवाई अड्डा सहायक। आज मैं उड़ानों, गेटों, सामान या सुविधाओं के संबंध में आपकी क्या मदद कर सकता हूँ?",
        "not_found": "मुझे इस जानकारी का विशिष्ट रिकॉर्ड नहीं मिला। कृपया वैध उड़ान संख्या (उदा. AI-204, 6E-531) दर्ज करें या गेट, बैगेज, लाउंज अथवा वाई-फाई के बारे में पूछें।",
        "prompts": ["उड़ान AI-204 की स्थिति", "गेट 24 कहाँ है?", "सामान बेल्ट की जानकारी", "लाउंज कहाँ है?", "वाई-फाई कैसे जोड़ें?"]
    },
    "es": {
        "flight_found": "Aquí está el estado operativo en tiempo real del vuelo {flight_number} ({airline}):",
        "gate_info": "Puerta de embarque: {gate} en {terminal}. Tiempo estimado a pie desde el control de seguridad: aprox. {walk_time} minutos.",
        "baggage_info": "Recogida de equipaje: Asignada a {carousel} en {terminal}.",
        "checkin_info": "Mostradores de facturación: Ubicados en {checkin_desks}.",
        "status_notice": "Estado actual: {status} (Retraso: {delay} min).",
        "greeting": "¡Hola! Soy TRAIT AirportAI, su asistente de pasajeros en tiempo real. ¿Cómo puedo ayudarle hoy con vuelos, puertas, equipaje o instalaciones del aeropuerto?",
        "not_found": "No pude encontrar registros específicos para esa consulta. Ingrese un número de vuelo válido (ej. AI-204, 6E-531) o consulte sobre puertas, equipaje o wifi.",
        "prompts": ["Estado del vuelo AI-204", "¿Dónde está la puerta 24?", "Equipaje del vuelo BA-142", "Salas VIP disponibles", "Conexión wifi gratuita"]
    },
    "fr": {
        "flight_found": "Voici le statut opérationnel en temps réel pour le vol {flight_number} ({airline}) :",
        "gate_info": "Porte d'embarquement : {gate} au {terminal}. Temps de marche estimé depuis la sécurité : environ {walk_time} minutes.",
        "baggage_info": "Livraison des bagages : Carrousel {carousel} au {terminal}.",
        "checkin_info": "Comptoirs d'enregistrement : Situés à {checkin_desks}.",
        "status_notice": "Statut du vol : {status} (Retard : {delay} min).",
        "greeting": "Bonjour ! Je suis TRAIT AirportAI, votre assistant passagers en temps réel. En quoi puis-je vous aider aujourd'hui ?",
        "not_found": "Je n'ai pas trouvé d'informations pour cette demande. Veuillez entrer un numéro de vol valide (ex. AI-204) ou poser une question sur les portes ou bagages.",
        "prompts": ["Statut du vol AI-204", "Où est la porte 24 ?", "Livraison bagages 6E-531", "Salons d'attente", "Connexion Wi-Fi"]
    },
    "de": {
        "flight_found": "Hier ist der Echtzeit-Betriebsstatus für Flug {flight_number} ({airline}):",
        "gate_info": "Flugsteig (Gate): {gate} im {terminal}. Geschätzte Gehzeit ab Sicherheitskontrolle: ca. {walk_time} Minuten.",
        "baggage_info": "Gepäckausgabe: {carousel} im {terminal}.",
        "checkin_info": "Check-in-Schalter: {checkin_desks}.",
        "status_notice": "Flugstatus: {status} (Verspätung: {delay} Min).",
        "greeting": "Hallo! Ich bin TRAIT AirportAI, Ihr intelligenter Passagierassistent in Echtzeit. Wie kann ich Ihnen heute helfen?",
        "not_found": "Keine Datensätze gefunden. Bitte geben Sie eine gültige Flugnummer ein (z. B. AI-204) oder fragen Sie nach Gates, Gepäck oder WLAN.",
        "prompts": ["Status von Flug AI-204", "Wo ist Gate 24?", "Gepäckausgabe BA-142", "Lounge-Informationen", "Kostenloses WLAN"]
    },
    "ar": {
        "flight_found": "إليك الحالة التشغيلية المباشرة للرحلة {flight_number} ({airline}):",
        "gate_info": "بوابة الصعود: {gate} في {terminal}. الوقت التقديري للمشي من نقطة التفتيش: حوالي {walk_time} دقيقة.",
        "baggage_info": "استلام الأمتعة: سير الأمتعة {carousel} في {terminal}.",
        "checkin_info": "مكاتب إنهاء إجراءات السفر: {checkin_desks}.",
        "status_notice": "حالة الرحلة: {status} (التأخير: {delay} دقيقة).",
        "greeting": "مرحباً! أنا TRAIT AirportAI، مساعد الركاب الذكي في المطار. كيف يمكنني مساعدتك اليوم بخصوص الرحلات أو البوابات أو الأمتعة؟",
        "not_found": "لم أتمكن من العثور على سجلات مطابقة. يرجى إدخال رقم رحلة صالح (مثل AI-204) أو السؤال عن البوابات أو الأمتعة أو الواي فاي.",
        "prompts": ["حالة الرحلة AI-204", "أين تقع البوابة 24؟", "سير الأمتعة للرحلة EK-501", "صالات كبار الشخصيات", "الاتصال بالواي فاي"]
    }
}

def detect_language(text: str, default_lang: str = "en") -> str:
    """Accurately detects language from text using script matching and keyword heuristics."""
    if not text or not text.strip():
        return default_lang

    text_lower = text.lower()

    # 1. Unicode script detection
    if SCRIPT_RANGES["hi"].search(text):
        return "hi"
    if SCRIPT_RANGES["ar"].search(text):
        return "ar"

    # 2. Keyword heuristic detection
    words = set(re.findall(r"\b\w+\b", text_lower))
    score = {"en": 0, "es": 0, "fr": 0, "de": 0, "hi": 0}

    for lang, kws in KEYWORD_MAP.items():
        for kw in kws:
            if kw in words or kw in text_lower:
                score[lang] += 2

    best_lang, best_score = max(score.items(), key=lambda x: x[1])
    if best_score > 0:
        return best_lang

    return default_lang if default_lang in SUPPORTED_LANGUAGES else "en"

def get_template(lang: str, key: str) -> str:
    lang_key = lang if lang in LOCALIZED_TEMPLATES else "en"
    return LOCALIZED_TEMPLATES[lang_key].get(key, LOCALIZED_TEMPLATES["en"].get(key, ""))

def get_prompts_for_language(lang: str):
    lang_key = lang if lang in LOCALIZED_TEMPLATES else "en"
    return LOCALIZED_TEMPLATES[lang_key].get("prompts", LOCALIZED_TEMPLATES["en"]["prompts"])

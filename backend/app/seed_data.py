"""
TRAIT Aviation Intelligence - Synthetic Demonstration Data Generator
DISCLAIMER: ALL DATA GENERATED HERE IS STRICTLY SYNTHETIC DEMONSTRATION DATA
FOR TESTING AND DEMO PURPOSES ONLY.
"""

import sqlite3
import random
from datetime import datetime, timedelta
from app.database import get_db_connection, init_db

def generate_synthetic_data():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing tables to ensure a clean re-seed
    tables = [
        "flights", "terminals_facilities", "passenger_hourly_flow",
        "baggage_operations", "faqs_knowledge", "operational_anomalies"
    ]
    for table in tables:
        cursor.execute(f"DELETE FROM {table};")

    # 1. Terminals & Facilities Data
    facilities = [
        # Terminal 1 Facilities
        ("T1", "CheckIn", "T1 Domestic Check-in Counters 1-20", "T1 Departures Level 2, Row A & B", "Level 2", 3, 1, "24/7", "Self-kiosks, Baggage drop, Indigo/Akasa counters"),
        ("T1", "Security", "T1 Central Security Screening", "T1 Departures Level 2, Post-Checkin", "Level 2", 5, 1, "24/7", "Body scanners, Priority lane, Fast track"),
        ("T1", "Gate", "Gate 1A - 1F (Bus Boarding)", "T1 Ground Level, Pier A", "Level 1", 7, 1, "Operational hours", "Remote bay boarding, Charging points, Seating"),
        ("T1", "Gate", "Gate 8 - 14", "T1 Level 2, North Concourse", "Level 2", 6, 1, "Operational hours", "Aerobridge boarding, Coffee stand, Newsstand"),
        ("T1", "Lounge", "Encalm Domestic Lounge T1", "T1 Mezzanine Level, Near Gate 10", "Level 3", 8, 1, "04:00 - 23:00", "Buffet, Wi-Fi, Shower, Quiet pods"),
        ("T1", "Baggage", "T1 Baggage Claim Belts 1 - 4", "T1 Arrivals Ground Floor", "Level 1", 4, 1, "24/7", "Carousels 1-4, Lost luggage counter, Trolleys"),
        ("T1", "Medical", "T1 Emergency Medical Center", "T1 Arrivals Hall, Near Exit 2", "Level 1", 2, 1, "24/7", "First aid, Doctor on duty, Ambulance bay"),
        ("T1", "Food", "T1 Food Court & Starbucks", "T1 Security Hold Area, Level 2", "Level 2", 5, 1, "24/7", "Starbucks, Haldiram's, Subway, KFC"),
        ("T1", "Restroom", "T1 Restrooms & Baby Care Room", "T1 Near Gate 9 & Gate 12", "Level 2", 3, 1, "24/7", "Accessible washrooms, Diaper changing, Feeding area"),
        ("T1", "Transit", "Inter-Terminal Shuttle Bus Stop T1", "T1 Arrivals Curbside Pillar 4", "Level 1", 4, 1, "24/7", "Free shuttle to T2 and T3 every 10 mins"),

        # Terminal 2 Facilities
        ("T2", "CheckIn", "T2 Airline Check-in Counters 21-45", "T2 Departures Level 2, Zones C & D", "Level 2", 4, 1, "24/7", "Air India Express, SpiceJet, Vistara"),
        ("T2", "Security", "T2 South Security Checkpoint", "T2 Departures Level 2", "Level 2", 6, 1, "24/7", "X-ray lanes, Automated tray return, Women-only lane"),
        ("T2", "Gate", "Gate 20 - 26", "T2 Concourse Pier B", "Level 2", 8, 1, "Operational hours", "Contact gates, USB charging seats, Water refilling"),
        ("T2", "Gate", "Gate 27 - 35", "T2 Concourse Pier C", "Level 2", 11, 1, "Operational hours", "High-capacity gates, Restrooms nearby"),
        ("T2", "Lounge", "Plaza Premium Lounge T2", "T2 Security Hold Area, Near Gate 25", "Level 2", 7, 1, "24/7", "Bar, Gourmet dining, Workspaces, Nap rooms"),
        ("T2", "Baggage", "T2 Baggage Belts 5 - 8", "T2 Ground Floor Arrivals", "Level 1", 5, 1, "24/7", "Carousels 5-8, Baggage wrap, Porter service"),
        ("T2", "Food", "T2 Artisan Cafe & Indian Delights", "T2 Pier B Central Rotunda", "Level 2", 6, 1, "24/7", "Chai Point, Pizza Hut, Costa Coffee"),
        ("T2", "Restroom", "T2 Accessible Restroom & Prayer Room", "T2 Pier B, Opposite Gate 23", "Level 2", 3, 1, "24/7", "Multifaith prayer room, Accessible washroom"),

        # Terminal 3 Facilities (Major Hub & International)
        ("T3", "CheckIn", "T3 International & Domestic Check-in Rows A to K", "T3 Departures Level 3 Forecourt", "Level 3", 5, 1, "24/7", "Full service check-in, Self baggage drop, First/Business class"),
        ("T3", "Security", "T3 Central Security & Immigration", "T3 Departures Level 3", "Level 3", 8, 1, "24/7", "e-Gates, Biometric DigiYatra, 24 Screening lanes"),
        ("T3", "Gate", "Gate 40 - 48 (Domestic Pier)", "T3 Level 3, Domestic Wing Pier D", "Level 3", 9, 1, "Operational hours", "Aerobridge, Duty free, Boarding lounges"),
        ("T3", "Gate", "Gate 50 - 65 (International Pier)", "T3 Level 3, International Wing Pier E", "Level 3", 14, 1, "Operational hours", "Widebody gates A380/B777, Moving walkways"),
        ("T3", "Lounge", "Maharaja Lounge & Emirates Lounge", "T3 International Departures Mezzanine", "Level 4", 10, 1, "24/7", "Luxury buffet, Spa, Sleeping suites, Business center"),
        ("T3", "Lounge", "Encalm Privé T3", "T3 Departures Level 3 Near Gate 44", "Level 3", 8, 1, "24/7", "Executive dining, Cigar room, Private pods"),
        ("T3", "Baggage", "T3 International Baggage Claim Belts 9 - 16", "T3 Arrivals Level 1", "Level 1", 6, 1, "24/7", "Oversized luggage carousel 15, Customs screening"),
        ("T3", "Medical", "Medanta Airport Clinic & Pharmacy", "T3 Arrivals Forecourt, Pillar 12", "Level 1", 3, 1, "24/7", "Doctors, ICU setup, Prescription medicines"),
        ("T3", "Transit", "Airside International Transit Desk", "T3 International Arrivals Level 2", "Level 2", 5, 1, "24/7", "Connection boarding passes, Baggage retagging"),
        ("T3", "Food", "T3 International Promenade Dining", "T3 Post-Immigration Central Atrium", "Level 3", 7, 1, "24/7", "Duty free retail, Caviar house, McDonald's, Pret A Manger"),
        ("T3", "Restroom", "T3 Luxury Restrooms & Baby Care Hub", "T3 Every 80 meters along Pier D and E", "Level 3", 2, 1, "24/7", "Baby feeding suites, Accessible, Shower cubicles")
    ]

    for f in facilities:
        cursor.execute("""
            INSERT INTO terminals_facilities 
            (terminal, category, name, location_desc, level, walking_time_mins, wheelchair_accessible, opening_hours, amenities)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, f)

    # 2. Comprehensive Multilingual FAQs & Knowledge Base
    # Languages: EN (English), HI (Hindi), ES (Spanish), FR (French), DE (German), AR (Arabic)
    faqs = [
        {
            "topic": "Baggage Allowance",
            "category": "Baggage",
            "keywords": "baggage weight limit allowance cabin check-in luggage excess fee वजन सामान",
            "q_en": "What is the cabin and check-in baggage allowance?",
            "q_hi": "केबिन और चेक-इन सामान की सीमा क्या है?",
            "q_es": "¿Cuál es la franquicia de equipaje de mano y facturado?",
            "q_fr": "Quelle est la franchise de bagages en cabine et en soute ?",
            "q_de": "Wie viel Handgepäck und Freigepäck ist erlaubt?",
            "q_ar": "ما هو الوزن المسموح به للأمتعة اليدوية والمشحونة؟",
            "a_en": "Standard domestic allowance is 7kg for cabin baggage and 15kg for check-in baggage. International flights generally permit 20-30kg check-in baggage depending on your airline and ticket class. Excess baggage counters are located beside Check-in Row B (T1) and Row H (T3).",
            "a_hi": "घरेलू उड़ानों के लिए मानक सीमा 7 किग्रा केबिन बैग और 15 किग्रा चेक-इन बैग है। अंतरराष्ट्रीय उड़ानों में 20-30 किग्रा की अनुमति होती है। अतिरिक्त सामान काउंटर चेक-इन रो बी (टी1) और रो एच (टी3) के पास स्थित हैं।",
            "a_es": "El límite estándar nacional es de 7 kg de mano y 15 kg facturados. Los vuelos internacionales suelen permitir entre 20 y 30 kg. Los mostradores de exceso de equipaje están junto a la Fila B (T1) y Fila H (T3).",
            "a_fr": "La franchise intérieure standard est de 7 kg en cabine et 15 kg en soute. Les vols internationaux autorisent généralement 20 à 30 kg. Les comptoirs d'excédent de bagages se trouvent près de la rangée B (T1) et rangée H (T3).",
            "a_de": "Das Standard-Handgepäck beträgt 7 kg und das Freigepäck 15 kg auf Inlandsflügen. Internationale Flüge erlauben meist 20-30 kg. Schalter für Übergepäck befinden sich bei Reihe B (T1) und Reihe H (T3).",
            "a_ar": "الوزن المسموح به للرحلات الداخلية هو 7 كجم للأمتعة اليدوية و15 كجم للأمتعة المشحونة. الرحلات الدولية تسمح عادة بـ 20-30 كجم. مكاتب الوزن الزائد بجوار الصف B (T1) والصف H (T3)."
        },
        {
            "topic": "Security & Liquids",
            "category": "Security",
            "keywords": "liquids 100ml perfume water security check screening gel perfume पानी तरल सुरक्षा",
            "q_en": "What are the security regulations for carrying liquids and electronics?",
            "q_hi": "सुरक्षा जांच में तरल पदार्थ और इलेक्ट्रॉनिक्स ले जाने के क्या नियम हैं?",
            "q_es": "¿Cuáles son las normas de seguridad para líquidos y aparatos electrónicos?",
            "q_fr": "Quelles sont les règles de sécurité pour les liquides et les appareils électroniques ?",
            "q_de": "Welche Sicherheitsregeln gelten für Flüssigkeiten und elektronische Geräte?",
            "q_ar": "ما هي لوائح الأمان لحمل السوائل والأجهزة الإلكترونية؟",
            "a_en": "Liquids, gels, and pastes in cabin baggage must be in containers of 100ml or less, enclosed in a transparent resealable bag. Laptops, tablets, and power banks must be taken out of bags for X-ray screening at security. Power banks are forbidden in check-in luggage.",
            "a_hi": "केबिन बैग में तरल और जैल 100 मिली से कम के कंटेनर में होने चाहिए। लैपटॉप, टैबलेट और पावर बैंक को एक्स-रे स्क्रीनिंग के लिए बैग से बाहर निकालना अनिवार्य है। चेक-इन सामान में पावर बैंक ले जाना सख्त मना है।",
            "a_es": "Los líquidos en el equipaje de mano deben ir en envases de hasta 100 ml en bolsa transparente. Los portátiles y baterías externas deben sacarse para el escáner X. Las baterías externas están prohibidas en bodega.",
            "a_fr": "Les liquides en cabine doivent être dans des contenants de 100 ml max dans un sac transparent. Ordinateurs et batteries externes doivent être retirés pour le contrôle RX. Les batteries externes sont interdites en soute.",
            "a_de": "Flüssigkeiten im Handgepäck dürfen maximal 100 ml pro Behälter fassen. Laptops und Powerbanks müssen separat geröntgt werden. Powerbanks sind im aufgegebenen Gepäck streng verboten.",
            "a_ar": "يجب ألا تتجاوز السوائل في حقيبة اليد 100 مل في عبوة شفافة. يجب إخراج أجهزة الكمبيوتر المحمول وبنوك الطاقة للفحص بالأشعة. يُمنع وضع بنوك الطاقة في حقائب الشحن."
        },
        {
            "topic": "Gate Directions & Walking Times",
            "category": "Gate",
            "keywords": "gate find directions walk time how far how to reach गेट कहाँ है रास्ता",
            "q_en": "How do I find my boarding gate and how much time should I allow?",
            "q_hi": "मुझे अपना बोर्डिंग गेट कैसे मिलेगा और कितना समय लगेगा?",
            "q_es": "¿Cómo encuentro mi puerta de embarque y cuánto tiempo debo calcular?",
            "q_fr": "Comment trouver ma porte d'embarquement et combien de temps prévoir ?",
            "q_de": "Wie finde ich mein Flugsteig (Gate) und wie viel Zeit sollte ich einplanen?",
            "q_ar": "كيف أصل إلى بوابة الصعود إلى الطائرة وكم من الوقت أحتاج؟",
            "a_en": "Follow illuminated flight information screens (FIDS) after security. In T1: Gates 1-14 take 5-9 mins walking. In T2: Gates 20-35 take 8-12 mins. In T3: Gates 40-65 take 10-18 mins. Electric buggy carts are available for senior citizens and PRM passengers near security exits.",
            "a_hi": "सुरक्षा जांच के बाद इलेक्ट्रॉनिक डिस्प्ले स्क्रीन का पालन करें। टी1 में गेट 1-14 तक 5-9 मिनट लगते हैं। टी2 में 8-12 मिनट। टी3 में 10-18 मिनट लग सकते हैं। बुजुर्गों और दिव्यांगों के लिए सुरक्षा निकास के पास इलेक्ट्रिक बग्गी उपलब्ध है।",
            "a_es": "Siga las pantallas de información de vuelo tras el control de seguridad. En T1: Puertas 1-14 toman 5-9 min. En T2: 8-12 min. En T3: 10-18 min. Hay carritos eléctricos disponibles para personas con movilidad reducida.",
            "a_fr": "Suivez les écrans d'affichage après la sécurité. T1 : Portes 1-14 à 5-9 min. T2 : 8-12 min. T3 : 10-18 min. Des voiturettes électriques sont disponibles pour les personnes à mobilité réduite.",
            "a_de": "Folgen Sie den Abflugmonitoren nach der Sicherheitskontrolle. T1: Gates 1-14 dauern 5-9 Min. T2: 8-12 Min. T3: 10-18 Min. Elektro-Carts für Senioren und mobilitätseingeschränkte Reisende stehen bereit.",
            "a_ar": "اتبع شاشات معلومات الرحلات بعد الأمن. في T1: البوابات 1-14 تستغرق 5-9 دقائق مشياً. في T2: 8-12 دقيقة. في T3: 10-18 دقيقة. تتوفر عربات جولف كهربائية لكبار السن وذوي الاحتياجات الخاصة."
        },
        {
            "topic": "Lost and Found Baggage",
            "category": "Baggage",
            "keywords": "lost found baggage missing delayed carousel belt luggage खोया सामान बैग",
            "q_en": "What should I do if my baggage is lost, damaged, or delayed?",
            "q_hi": "अगर मेरा सामान खो जाए, क्षतिग्रस्त हो जाए या देर से आए तो क्या करें?",
            "q_es": "¿Qué debo hacer si mi equipaje se pierde, daña o retrasa?",
            "q_fr": "Que faire si mes bagages sont perdus, endommagés ou retardés ?",
            "q_de": "Was tun bei verlorenem, beschädigtem oder verspätetem Gepäck?",
            "q_ar": "ماذا أفعل إذا فُقدت أمتعتي أو تلفت أو تأخرت؟",
            "a_en": "Immediately visit your airline's Baggage Service Desk located inside the arrivals reclaim hall before exiting customs. File a Property Irregularity Report (PIR) with your luggage tag receipt. For general lost personal belongings at the airport, visit the Lost & Found office at T3 Ground Floor Pillar 8.",
            "a_hi": "सीमा शुल्क से बाहर निकलने से पहले आगमन हॉल में अपनी एयरलाइन के बैगेज सर्विस डेस्क पर तुरंत संपर्क करें। अपने बैगेज टैग के साथ पीआईआर (PIR) रिपोर्ट दर्ज करें। एयरपोर्ट पर खोई वस्तुओं के लिए टी3 ग्राउंड फ्लोर पिलर 8 पर लॉस्ट एंड फाउंड डेस्क पर जाएं।",
            "a_es": "Visite de inmediato el mostrador de equipajes de su aerolínea en la sala de llegadas antes de aduana y tramite el Parte de Irregularidad de Equipaje (PIR). Para objetos personales perdidos en la terminal, acuda a T3 Planta Baja Pilar 8.",
            "a_fr": "Rendez-vous immédiatement au comptoir bagages de votre compagnie en salle de livraison avant la douane pour établir un constat PIR. Pour les objets perdus dans l'aéroport, contactez le bureau des objets trouvés au T3 RDC Pilier 8.",
            "a_de": "Gehen Sie sofort vor dem Zoll zum Gepäckschalter Ihrer Fluggesellschaft im Ankunftsbereich und füllen Sie einen PIR-Bericht aus. Für im Terminal verlorene Gegenstände besuchen Sie das Fundbüro im T3 EG Pfeiler 8.",
            "a_ar": "توجه فوراً إلى مكتب خدمة الأمتعة التابع لشركة الطيران في صالة الوصول قبل الخروج واطلب تقرير فقدان الأمتعة (PIR). للمفقودات الشخصية في المطار، زر مكتب المفقودات في T3 الطابق الأرضي عند العمود 8."
        },
        {
            "topic": "Special Assistance & Wheelchair",
            "category": "Special Assistance",
            "keywords": "wheelchair disability special assistance elderly medical escort व्हीलचेयर सहायता",
            "q_en": "How can I request wheelchair and special mobility assistance?",
            "q_hi": "व्हीलचेयर और विशेष सहायता का अनुरोध कैसे करें?",
            "q_es": "¿Cómo solicito asistencia especial y silla de ruedas?",
            "q_fr": "Comment demander une assistance en fauteuil roulant ou une aide spécifique ?",
            "q_de": "Wie beantrage ich Rollstuhlservice und besondere Unterstützung?",
            "q_ar": "كيف يمكنني طلب كرسي متحرك والمساعدة الخاصة؟",
            "a_en": "Wheelchair assistance can be pre-booked with your airline or requested directly at the Special Assistance desks at Departures Entry Gate 1 (T1) and Gate 4 (T3). Dedicated prams, tactile paving for visually impaired passengers, and ambulift services are fully functional across all terminals.",
            "a_hi": "व्हीलचेयर सहायता आपकी एयरलाइन से पहले बुक की जा सकती है या सीधे प्रस्थान प्रवेश द्वार 1 (टी1) और गेट 4 (टी3) पर विशेष सहायता डेस्क से प्राप्त की जा सकती है। सभी टर्मिनलों में प्रैम, ब्रेल साइनेज और एम्बुलिफ्ट की पूरी सुविधा है।",
            "a_es": "Puede solicitar silla de ruedas con su aerolínea o en los mostradores de Asistencia Especial en la Entrada 1 (T1) y Entrada 4 (T3). Hay cochecitos y pasarelas accesibles en todas las terminales.",
            "a_fr": "L'assistance en fauteuil roulant peut être demandée auprès de votre compagnie ou aux comptoirs Départs Porte 1 (T1) et Porte 4 (T3). Poussettes et accès PMR sont disponibles dans tous les terminaux.",
            "a_de": "Rollstuhlassistenz kann bei der Airline vorgebucht oder an den Schaltern für besondere Hilfe an Eingang 1 (T1) und Eingang 4 (T3) angefordert werden. Alle Terminals sind barrierefrei.",
            "a_ar": "يمكن حجز الكرسي المتحرك مسبقاً مع شركة الطيران أو طلبه من مكاتب المساعدة الخاصة عند بوابة المغادرة 1 (T1) وبوابة 4 (T3). المطار مجهز بالكامل لخدمة أصحاب الهمم."
        },
        {
            "topic": "Inter-Terminal Transfer",
            "category": "Transit",
            "keywords": "inter terminal shuttle bus transit transfer t1 t2 t3 train शटल बस टर्मिनल ट्रांसफर",
            "q_en": "How do I transfer between Terminal 1, Terminal 2, and Terminal 3?",
            "q_hi": "टर्मिनल 1, 2 और 3 के बीच ट्रांसफर कैसे करें?",
            "q_es": "¿Cómo me traslado entre la Terminal 1, Terminal 2 y Terminal 3?",
            "q_fr": "Comment effectuer un transfert entre les terminaux 1, 2 et 3 ?",
            "q_de": "Wie wechsle ich zwischen Terminal 1, Terminal 2 und Terminal 3?",
            "q_ar": "كيف أنتقل بين مبنى الركاب 1 و 2 و 3؟",
            "a_en": "A complimentary Inter-Terminal Shuttle operates 24/7 between T1, T2, and T3 every 10 minutes. Pick-up points are located outside Arrivals Forecourt: T1 Pillar 4, T2 Gate 3, T3 Pillar 10. Present your connecting flight boarding pass or ticket for free transit.",
            "a_hi": "टी1, टी2 और टी3 के बीच हर 10 मिनट में 24/7 मुफ्त इंटर-टर्मिनल शटल बस चलती है। पिकअप पॉइंट आगमन हॉल के बाहर हैं: टी1 पिलर 4, टी2 गेट 3, टी3 पिलर 10। मुफ्त यात्रा के लिए अपनी कनेक्टिंग टिकट दिखाएं।",
            "a_es": "Un servicio gratuito de lanzadera opera 24/7 cada 10 min entre T1, T2 y T3. Puntos de recogida: T1 Pilar 4, T2 Puerta 3, T3 Pilar 10. Muestre su billete de conexión.",
            "a_fr": "Une navette gratuite relie les terminaux T1, T2 et T3 toutes les 10 min 24h/24. Arrêts : T1 Pilier 4, T2 Porte 3, T3 Pilier 10. Présentez votre billet en correspondance.",
            "a_de": "Ein kostenloser Shuttlebus verkehrt rund um die Uhr alle 10 Minuten zwischen T1, T2 und T3. Haltestellen: T1 Pfeiler 4, T2 Gate 3, T3 Pfeiler 10. Zeigen Sie Ihr Anschlussticket vor.",
            "a_ar": "تعمل حافلة نقل مجانية بين T1 و T2 و T3 على مدار الساعة كل 10 دقائق. نقاط الركوب: T1 عند العمود 4، T2 عند البوابة 3، T3 عند العمود 10. أظهر تذكرة رحلتك المتابعة."
        },
        {
            "topic": "Wi-Fi & Connectivity",
            "category": "Amenities",
            "keywords": "wifi internet connect password otp roaming free वाई-फाई इंटरनेट",
            "q_en": "How do I connect to free high-speed airport Wi-Fi?",
            "q_hi": "फ्री हाई-स्पीड एयरपोर्ट वाई-फाई से कैसे जुड़ें?",
            "q_es": "¿Cómo me conecto al wifi gratuito de alta velocidad del aeropuerto?",
            "q_fr": "Comment se connecter au Wi-Fi gratuit de l'aéroport ?",
            "q_de": "Wie verbinde ich mich mit dem kostenlosen Flughafen-WLAN?",
            "q_ar": "كيف أتصل بشبكة الواي فاي المجانية عالية السرعة بالمطار؟",
            "a_en": "Select the network '#TRAIT_Airport_Free_WiFi'. Open your browser, enter your mobile number to receive an SMS OTP. For international travelers without active roaming, scan your boarding pass or passport at the Wi-Fi Kiosks located near Information Desks in T1, T2, and T3 to receive a Wi-Fi coupon code.",
            "a_hi": "'#TRAIT_Airport_Free_WiFi' नेटवर्क चुनें। ब्राउज़र खोलें और एसएमएस ओटीपी प्राप्त करने के लिए मोबाइल नंबर दर्ज करें। बिना रोमिंग वाले यात्री टी1, टी2, टी3 के सूचना कियोस्क पर पासपोर्ट स्कैन करके कूपन कोड ले सकते हैं।",
            "a_es": "Seleccione la red '#TRAIT_Airport_Free_WiFi'. Abra el navegador e ingrese su teléfono para recibir un SMS con código. Los viajeros internacionales pueden escanear su pasaporte en los quioscos de información.",
            "a_fr": "Sélectionnez le réseau '#TRAIT_Airport_Free_WiFi'. Ouvrez le navigateur pour recevoir un code par SMS. Les voyageurs internationaux peuvent scanner leur passeport aux bornes Wi-Fi.",
            "a_de": "Wählen Sie '#TRAIT_Airport_Free_WiFi'. Geben Sie im Browser Ihre Handynummer für einen SMS-Code ein. Reisende ohne Roaming scannen ihren Pass an den Informationskiosken.",
            "a_ar": "اختر شبكة '#TRAIT_Airport_Free_WiFi'. افتح المتصفح وأدخل رقم هاتفك لتلقي رمز التحقق. للمسافرين الدوليين، امسح جواز سفرك في أكشاك الاستعلامات للحصول على رمز الدخول."
        },
        {
            "topic": "Lounge Access & Amenities",
            "category": "Lounge",
            "keywords": "lounge access priority pass debit card credit card food shower relax लाउंज सुविधा",
            "q_en": "Where are the lounges and how can I access them?",
            "q_hi": "लाउंज कहाँ हैं और मैं उनका उपयोग कैसे कर सकता हूँ?",
            "q_es": "¿Dónde están las salas VIP y cómo puedo acceder a ellas?",
            "q_fr": "Où se trouvent les salons VIP et comment y accéder ?",
            "q_de": "Wo befinden sich die Lounges und wie erhalte ich Zutritt?",
            "q_ar": "أين توجد صالات كبار الشخصيات وكيف يمكنني الدخول إليها؟",
            "a_en": "Encalm Lounge is located at T1 Mezzanine (Gate 10) and T3 Departures (Gate 44). Plaza Premium is in T2 (Gate 25). Access is available via Priority Pass, eligible premium bank credit cards, airline business class tickets, or direct walk-in purchase (₹1,400 domestic / ₹2,600 international). Facilities include hot buffet, shower cubicles, workstations, and sleeping pods.",
            "a_hi": "एनकाम लाउंज टी1 मेज़ानाइन (गेट 10) और टी3 (गेट 44) पर स्थित है। प्लाजा प्रीमियम टी2 (गेट 25) में है। प्रायोरिटी पास, पात्र क्रेडिट कार्ड, बिजनेस क्लास टिकट या सीधे शुल्क देकर प्रवेश उपलब्ध है। बुफे, शॉवर और आराम की पूरी सुविधा है।",
            "a_es": "La sala Encalm está en T1 altillo (Puerta 10) y T3 (Puerta 44). Plaza Premium en T2 (Puerta 25). Acceso mediante Priority Pass, tarjetas premium bancarias o pago directo.",
            "a_fr": "Les salons Encalm sont au T1 mezzanine (Porte 10) et T3 (Porte 44). Plaza Premium au T2 (Porte 25). Accès via Priority Pass, cartes bancaires éligibles ou achat direct.",
            "a_de": "Die Encalm Lounge befindet sich in T1 (Gate 10) und T3 (Gate 44). Plaza Premium in T2 (Gate 25). Zugang mit Priority Pass, teilnehmenden Kreditkarten oder gegen Gebühr.",
            "a_ar": "توجد صالة Encalm في T1 (بوابة 10) و T3 (بوابة 44). وتوجد Plaza Premium في T2 (بوابة 25). الدخول عبر بطاقة Priority Pass أو بطاقات الائتمان المؤهلة أو الدفع المباشر."
        }
    ]

    for faq in faqs:
        cursor.execute("""
            INSERT INTO faqs_knowledge 
            (topic, category, question_en, question_hi, question_es, question_fr, question_de, question_ar,
             answer_en, answer_hi, answer_es, answer_fr, answer_de, answer_ar, keywords)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            faq["topic"], faq["category"],
            faq["q_en"], faq["q_hi"], faq["q_es"], faq["q_fr"], faq["q_de"], faq["q_ar"],
            faq["a_en"], faq["a_hi"], faq["a_es"], faq["a_fr"], faq["a_de"], faq["a_ar"],
            faq["keywords"]
        ))

    # 3. Realistic Synthetic Flight Data (120+ flights)
    airlines = [
        {"code": "AI", "name": "Air India", "type": "Full Service"},
        {"code": "6E", "name": "IndiGo", "type": "Low Cost"},
        {"code": "UK", "name": "Vistara", "type": "Full Service"},
        {"code": "EK", "name": "Emirates", "type": "International"},
        {"code": "BA", "name": "British Airways", "type": "International"},
        {"code": "SQ", "name": "Singapore Airlines", "type": "International"},
        {"code": "LH", "name": "Lufthansa", "type": "International"},
        {"code": "QR", "name": "Qatar Airways", "type": "International"}
    ]

    destinations_domestic = ["Mumbai (BOM)", "Bengaluru (BLR)", "Hyderabad (HYD)", "Chennai (MAA)", "Kolkata (CCU)", "Goa (GOX)", "Ahmedabad (AMD)", "Pune (PNQ)"]
    destinations_intl = ["Dubai (DXB)", "London Heathrow (LHR)", "Singapore (SIN)", "Frankfurt (FRA)", "Doha (DOH)", "New York (JFK)", "Paris (CDG)", "Tokyo (HND)"]

    aircraft_types = ["Airbus A320neo", "Airbus A321neo", "Boeing 787-9 Dreamliner", "Boeing 777-300ER", "Airbus A350-900"]

    delay_causes = ["Carrier", "Weather", "NAS/ATC", "Late Aircraft", "Security"]

    base_time = datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=12)

    flights_data = []
    flight_idx = 100

    # Deterministic flight list for predictable demo lookups (e.g., AI-204, 6E-531, BA-142, EK-501)
    featured_flights = [
        ("AI-204", "Air India", "Mumbai (BOM)", "Departure", "T3", "Gate 44A", "Row E (Counters 40-48)", "Carousel 9", "Boarding", 0, "None", 45, 182),
        ("6E-531", "IndiGo", "Bengaluru (BLR)", "Departure", "T1", "Gate 12B", "Row A (Counters 1-12)", "Carousel 3", "On-Time", 0, "None", 40, 174),
        ("BA-142", "British Airways", "London Heathrow (LHR)", "Departure", "T3", "Gate 54", "Row K (Counters 90-98)", "Carousel 14", "Delayed", 65, "Late Aircraft", 125, 298),
        ("EK-501", "Emirates", "Dubai (DXB)", "Departure", "T3", "Gate 58B", "Row J (Counters 80-88)", "Carousel 12", "On-Time", 0, "None", 55, 360),
        ("UK-817", "Vistara", "Hyderabad (HYD)", "Departure", "T2", "Gate 24", "Row C (Counters 21-28)", "Carousel 6", "Gate Closed", 15, "NAS/ATC", 48, 158),
        ("AI-101", "Air India", "New York (JFK)", "Departure", "T3", "Gate 62", "Row F (Counters 50-60)", "Carousel 15", "Delayed", 90, "Weather", 140, 310),
        ("SQ-402", "Singapore Airlines", "Singapore (SIN)", "Departure", "T3", "Gate 52A", "Row H (Counters 70-78)", "Carousel 11", "On-Time", 0, "None", 50, 275),
        ("6E-2091", "IndiGo", "Kolkata (CCU)", "Departure", "T1", "Gate 6", "Row B (Counters 13-20)", "Carousel 2", "Departed", 0, "None", 38, 180),
        ("LH-760", "Lufthansa", "Frankfurt (FRA)", "Arrival", "T3", "Gate 51", "International Transit", "Carousel 10", "Landed", 20, "Carrier", 75, 285),
        ("QR-571", "Qatar Airways", "Doha (DOH)", "Arrival", "T3", "Gate 56", "International Transit", "Carousel 13", "Baggage Claim", 0, "None", 52, 312),
    ]

    for ff in featured_flights:
        f_num, airline, city, f_type, term, gate, checkin, carousel, status, delay_m, delay_r, turnaround, pax = ff
        sched = (base_time + timedelta(hours=random.randint(1, 14), minutes=random.choice([0, 15, 30, 45]))).strftime("%Y-%m-%d %H:%M")
        est = (datetime.strptime(sched, "%Y-%m-%d %H:%M") + timedelta(minutes=delay_m)).strftime("%Y-%m-%d %H:%M")
        flights_data.append((
            f_num, airline, "Delhi (DEL)" if f_type == "Departure" else city,
            city if f_type == "Departure" else "Delhi (DEL)",
            f_type, sched, est, est if status in ["Departed", "Landed"] else None,
            status, term, gate, checkin, carousel, delay_m, delay_r,
            random.choice(aircraft_types), pax, turnaround
        ))

    # Generate additional 115 synthetic flights across the schedule
    random.seed(42)  # Consistent synthetic seed for test reproducibility
    for i in range(115):
        flight_idx += 1
        al = random.choice(airlines)
        f_num = f"{al['code']}-{random.randint(100, 999)}"
        # Ensure unique flight number
        if any(f[0] == f_num for f in flights_data):
            f_num = f"{al['code']}-{random.randint(1000, 4999)}"

        f_type = random.choice(["Departure", "Arrival"])
        is_intl = al["type"] == "International"
        dest = random.choice(destinations_intl) if is_intl else random.choice(destinations_domestic)
        origin = "Delhi (DEL)" if f_type == "Departure" else dest
        destination = dest if f_type == "Departure" else "Delhi (DEL)"

        if is_intl:
            term = "T3"
            gate = f"Gate {random.randint(48, 65)}{random.choice(['A', 'B', ''])}"
            checkin = f"Row {random.choice(['G', 'H', 'J', 'K'])} (Counters {random.randint(60, 90)}-{random.randint(91, 99)})"
            carousel = f"Carousel {random.randint(10, 16)}"
        elif al["code"] == "6E":
            term = "T1"
            gate = f"Gate {random.randint(1, 14)}{random.choice(['A', 'B', ''])}"
            checkin = f"Row {random.choice(['A', 'B'])} (Counters {random.randint(1, 10)}-{random.randint(11, 20)})"
            carousel = f"Carousel {random.randint(1, 4)}"
        else:
            term = random.choice(["T2", "T3"])
            gate = f"Gate {random.randint(20, 45)}{random.choice(['A', 'B', ''])}"
            checkin = f"Row {random.choice(['C', 'D', 'E'])} (Counters {random.randint(21, 35)}-{random.randint(36, 50)})"
            carousel = f"Carousel {random.randint(5, 9)}"

        # 78% on-time, 22% delayed
        is_delayed = random.random() < 0.22
        delay_m = random.choice([15, 25, 35, 45, 60, 85, 110]) if is_delayed else 0
        delay_r = random.choice(delay_causes) if is_delayed else "None"

        # Turnaround time: standard 40-60 mins, with occasional anomaly (110-150 mins)
        is_turnaround_anomaly = random.random() < 0.05
        turnaround = random.randint(115, 145) if is_turnaround_anomaly else random.randint(35, 65)

        sched_dt = base_time + timedelta(minutes=i * 12)
        sched = sched_dt.strftime("%Y-%m-%d %H:%M")
        est_dt = sched_dt + timedelta(minutes=delay_m)
        est = est_dt.strftime("%Y-%m-%d %H:%M")

        # Determine status
        now = datetime.now()
        if sched_dt < now - timedelta(hours=2):
            status = "Departed" if f_type == "Departure" else "Landed"
        elif sched_dt < now - timedelta(minutes=30):
            status = "Gate Closed" if f_type == "Departure" else "Baggage Claim"
        elif sched_dt < now + timedelta(minutes=45):
            status = "Boarding" if f_type == "Departure" else "Landed"
        elif is_delayed:
            status = "Delayed"
        else:
            status = "On-Time"

        pax = random.randint(130, 360) if is_intl else random.randint(120, 195)
        aircraft = random.choice(aircraft_types)

        flights_data.append((
            f_num, al["name"], origin, destination, f_type,
            sched, est, est if status in ["Departed", "Landed"] else None,
            status, term, gate, checkin, carousel, delay_m, delay_r,
            aircraft, pax, turnaround
        ))

    for f in flights_data:
        cursor.execute("""
            INSERT OR IGNORE INTO flights 
            (flight_number, airline, origin, destination, flight_type, scheduled_time, estimated_time, actual_time,
             status, terminal, gate, checkin_desks, baggage_carousel, delay_minutes, delay_reason, aircraft_type,
             passengers_booked, turnaround_time_mins)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, f)

    # 4. Hourly Passenger Flow (48 hours across T1, T2, T3)
    # Peak bank hours: 06:00-09:00 and 18:00-22:00
    for h in range(48):
        flow_time = (base_time + timedelta(hours=h)).strftime("%Y-%m-%d %H:00")
        hour_val = (base_time + timedelta(hours=h)).hour

        # Calculate diurnal peak multiplier
        if 6 <= hour_val <= 9:
            mult = 1.85  # Morning peak
        elif 18 <= hour_val <= 22:
            mult = 1.70  # Evening peak
        elif 0 <= hour_val <= 4:
            mult = 0.40  # Late night lull
        else:
            mult = 1.05  # Standard daytime

        for term, cap in [("T1", 3200), ("T2", 2800), ("T3", 5800)]:
            inbound = int((random.randint(600, 1200) * mult) * (cap / 4000.0))
            outbound = int((random.randint(700, 1400) * mult) * (cap / 4000.0))
            total_passengers = inbound + outbound
            cap_pct = round(min(98.5, (total_passengers / cap) * 100), 1)

            # Security wait time correlates with outbound volume
            base_wait = 4.0
            security_wait = round(base_wait + (cap_pct / 100.0) * 22.0 + random.uniform(-1.5, 2.5), 1)
            security_wait = max(3.0, security_wait)

            cursor.execute("""
                INSERT INTO passenger_hourly_flow 
                (timestamp, terminal, inbound_passengers, outbound_passengers, security_wait_mins, capacity_pct)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (flow_time, term, inbound, outbound, security_wait, cap_pct))

    # 5. Baggage Operations Data (50 arrival records)
    for i in range(50):
        f_record = flights_data[i]
        f_num = f_record[0]
        term = f_record[9]
        carousel = f_record[12]
        pax = f_record[16]

        total_bags = int(pax * random.uniform(1.05, 1.35))
        first_bag = random.randint(11, 20)
        # Occasional baggage dwell anomaly (last bag taking >65 mins)
        is_baggage_anomaly = (i % 9 == 0)
        last_bag = random.randint(68, 88) if is_baggage_anomaly else random.randint(28, 48)
        dwell_time = last_bag - first_bag
        processed = total_bags if last_bag < 50 else int(total_bags * 0.85)
        mishandled = random.choice([0, 0, 0, 0, 1, 2]) if is_baggage_anomaly else 0
        bag_status = "Delayed Hold" if is_baggage_anomaly else random.choice(["Delivered", "Completed", "Processing"])

        cursor.execute("""
            INSERT INTO baggage_operations
            (flight_number, carousel_id, terminal, total_bags, processed_bags, first_bag_mins, last_bag_mins, dwell_time_mins, mishandled_bags, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (f_num, carousel, term, total_bags, processed, first_bag, last_bag, dwell_time, mishandled, bag_status))

    # 6. Operational Anomalies Seed (Known baseline incident logs)
    anomalies = [
        (datetime.now().strftime("%Y-%m-%d %H:15"), "Turnaround Delay", "BA-142", "Gate 54 (T3)", "Turnaround Time", 125.0, "35 - 65 mins", "HIGH", "Aircraft turnaround exceeded standard threshold by 60 mins due to fueling pump failure and late catering.", "ACTIVE"),
        (datetime.now().strftime("%Y-%m-%d %H:05"), "Baggage Carousel Jam", "AI-101", "Carousel 15 (T3)", "Last Bag Delivery", 78.0, "25 - 45 mins", "HIGH", "Mechanical conveyor blockage on Carousel 15 resulted in high dwell time for widebody flight bags.", "ACTIVE"),
        ((datetime.now() - timedelta(minutes=45)).strftime("%Y-%m-%d %H:20"), "Security Surge", None, "T1 Central Security", "Security Wait Time", 26.5, "5 - 15 mins", "MEDIUM", "Sudden bank of 4 simultaneous narrowbody departures created screening bottleneck at T1 checkpoint.", "RESOLVING"),
        ((datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:00"), "ATC Ground Hold", "UK-817", "Runway 29L / Gate 24", "Departure Delay", 48.0, "0 - 15 mins", "MEDIUM", "Dense fog morning advisory reduced runway acceptance rate to 32 movements/hr.", "RESOLVED")
    ]

    for a in anomalies:
        cursor.execute("""
            INSERT INTO operational_anomalies
            (timestamp, incident_type, flight_number, location, metric_name, observed_value, expected_range, severity, description, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, a)

    conn.commit()
    conn.close()
    print("Synthetic demonstration data seeded successfully: 125 flights, 30 facilities, 48h flow, 50 baggage ops, 8 multilingual FAQs.")

if __name__ == "__main__":
    generate_synthetic_data()

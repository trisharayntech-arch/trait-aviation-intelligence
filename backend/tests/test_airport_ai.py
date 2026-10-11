import pytest
from app.airport_ai.multilingual import detect_language, get_template, SUPPORTED_LANGUAGES
from app.airport_ai.flight_assistant import extract_flight_number, get_flight_record, generate_flight_guidance
from app.airport_ai.knowledge_engine import KnowledgeEngine

def test_language_detection():
    # Hindi
    assert detect_language("उड़ान AI-204 की स्थिति क्या है?") == "hi"
    # Spanish
    assert detect_language("dónde está la puerta de embarque") == "es"
    # French
    assert detect_language("où sont mes bagages") == "fr"
    # German
    assert detect_language("wo ist das flugsteig") == "de"
    # Arabic
    assert detect_language("أين بوابة الصعود للرحلة") == "ar"
    # English default
    assert detect_language("Where is Gate 24B?") == "en"

def test_flight_number_extraction():
    assert extract_flight_number("Status for AI-204 please") == "AI-204"
    assert extract_flight_number("Where is flight 6E 531?") == "6E-531"
    assert extract_flight_number("Flight BA142 delay") == "BA-142"
    assert extract_flight_number("Hello there") is None

def test_flight_guidance():
    record = get_flight_record("AI-204")
    assert record is not None
    assert record["flight_number"] == "AI-204"
    assert record["terminal"] == "T3"

    guidance = generate_flight_guidance(record, lang="en")
    assert len(guidance.navigation_steps) > 0
    assert guidance.flight_number == "AI-204"
    assert "Gate" in guidance.gate

def test_knowledge_engine_search():
    engine = KnowledgeEngine()
    
    # 1. Flight inquiry
    res_flight = engine.process_query("What is the gate for flight AI-204?", user_lang="en")
    assert res_flight.intent == "FLIGHT_GUIDANCE"
    assert res_flight.flight_guidance is not None
    assert "AI-204" in res_flight.flight_guidance.flight_number

    # 2. FAQ inquiry (Baggage)
    res_bag = engine.process_query("What is the baggage weight allowance for domestic flights?", user_lang="en")
    assert "Baggage" in res_bag.intent or res_bag.confidence > 0.2
    assert "7kg" in res_bag.answer or "15kg" in res_bag.answer

    # 3. Multilingual inquiry (Hindi)
    res_hi = engine.process_query("सामान की सीमा क्या है?", user_lang="hi")
    assert res_hi.detected_language == "hi"

    # 4. Facility search
    res_fac = engine.process_query("Where is the Encalm Lounge?", user_lang="en")
    assert len(res_fac.facility_matches) > 0 or "Lounge" in res_fac.answer

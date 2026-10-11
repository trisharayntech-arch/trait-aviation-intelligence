"""
TRAIT AirportAI - Local Knowledge & Semantic Retrieval Engine
Uses Scikit-Learn TF-IDF vectorization and cosine similarity over local SQLite knowledge base.
Budget: ₹0. Runs 100% offline without external AI API dependencies.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Any, List, Optional
from app.database import get_db_connection
from app.models import ChatResponse, FlightGuidance
from app.airport_ai.multilingual import (
    detect_language, get_template, get_prompts_for_language, SUPPORTED_LANGUAGES
)
from app.airport_ai.flight_assistant import (
    extract_flight_number, get_flight_record, generate_flight_guidance
)

class KnowledgeEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            token_pattern=r"[\w\u0900-\u097F\u0600-\u06FF]+",
            ngram_range=(1, 2),
            stop_words=None,
            min_df=1
        )


        self.faq_records: List[Dict[str, Any]] = []
        self.facility_records: List[Dict[str, Any]] = []
        self.faq_texts: List[str] = []
        self.faq_matrix = None
        self._load_and_index()

    def _load_and_index(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        # Load FAQs
        cursor.execute("SELECT * FROM faqs_knowledge")
        self.faq_records = [dict(row) for row in cursor.fetchall()]

        # Load Facilities
        cursor.execute("SELECT * FROM terminals_facilities")
        self.facility_records = [dict(row) for row in cursor.fetchall()]

        conn.close()

        # Build corpus for TF-IDF indexing
        self.faq_texts = []
        for f in self.faq_records:
            # Combine all multilingual questions, keywords, and topics for robust indexing
            corpus_text = f"{f['topic']} {f['category']} {f['keywords']} " \
                          f"{f['question_en']} {f['question_hi']} {f['question_es']} " \
                          f"{f['question_fr']} {f['question_de']} {f['question_ar']} " \
                          f"{f['answer_en']}"
            self.faq_texts.append(corpus_text)

        if self.faq_texts:
            self.faq_matrix = self.vectorizer.fit_transform(self.faq_texts)

    def refresh_index(self):
        self._load_and_index()

    def search_facilities(self, query: str, limit: int = 4) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        matches = []
        for fac in self.facility_records:
            score = 0
            name_low = fac["name"].lower()
            cat_low = fac["category"].lower()
            loc_low = fac["location_desc"].lower()
            amen_low = (fac.get("amenities") or "").lower()

            words = q_lower.split()
            for w in words:
                if len(w) > 2:
                    if w in name_low:
                        score += 3
                    if w in cat_low:
                        score += 3
                    if w in loc_low:
                        score += 2
                    if w in amen_low:
                        score += 2

            if score > 0:
                fac_copy = dict(fac)
                fac_copy["match_score"] = score
                matches.append(fac_copy)

        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return matches[:limit]

    def process_query(self, query: str, user_lang: Optional[str] = None) -> ChatResponse:
        # 1. Detect language
        detected_lang = detect_language(query, default_lang=user_lang or "en")
        if user_lang and user_lang in SUPPORTED_LANGUAGES and detected_lang == "en":
            detected_lang = user_lang

        clean_query = query.strip()
        if not clean_query:
            return ChatResponse(
                answer=get_template(detected_lang, "greeting"),
                detected_language=detected_lang,
                intent="GREETING",
                confidence=1.0,
                flight_guidance=None,
                facility_matches=[],
                suggested_prompts=get_prompts_for_language(detected_lang)
            )

        # 2. Check for flight number pattern
        extracted_f_num = extract_flight_number(clean_query)
        flight_record = get_flight_record(extracted_f_num) if extracted_f_num else None

        if flight_record:
            guidance = generate_flight_guidance(flight_record, lang=detected_lang)
            intro = get_template(detected_lang, "flight_found").format(
                flight_number=guidance.flight_number,
                airline=guidance.airline
            )
            calc_walk_time = sum(st.estimated_minutes for st in guidance.navigation_steps) if guidance.navigation_steps else 10
            gate_info = get_template(detected_lang, "gate_info").format(
                gate=guidance.gate,
                terminal=guidance.terminal,
                walk_time=calc_walk_time
            )

            baggage_info = get_template(detected_lang, "baggage_info").format(
                carousel=guidance.baggage_carousel,
                terminal=guidance.terminal
            )
            checkin_info = get_template(detected_lang, "checkin_info").format(
                checkin_desks=guidance.checkin_desks
            )
            status_info = get_template(detected_lang, "status_notice").format(
                status=guidance.status,
                delay=guidance.delay_minutes
            )

            full_answer = f"{intro}\n\n• {status_info}\n• {gate_info}\n• {checkin_info}\n• {baggage_info}\n\n" \
                          f"Scheduled: {guidance.scheduled_time} | Estimated: {guidance.estimated_time}"

            facility_matches = self.search_facilities(guidance.terminal)

            return ChatResponse(
                answer=full_answer,
                detected_language=detected_lang,
                intent="FLIGHT_GUIDANCE",
                confidence=0.98,
                flight_guidance=guidance,
                facility_matches=facility_matches,
                suggested_prompts=get_prompts_for_language(detected_lang)
            )

        # 3. Check for standard greetings
        greetings = ["hi", "hello", "hey", "namaste", "hola", "bonjour", "hallo", "marhaba", "salam"]
        if clean_query.lower() in greetings or len(clean_query.split()) == 1 and clean_query.lower() in greetings:
            return ChatResponse(
                answer=get_template(detected_lang, "greeting"),
                detected_language=detected_lang,
                intent="GREETING",
                confidence=1.0,
                flight_guidance=None,
                facility_matches=[],
                suggested_prompts=get_prompts_for_language(detected_lang)
            )

        # 4. Search Local FAQs using TF-IDF + Cosine Similarity
        best_faq = None
        best_similarity = 0.0

        if self.faq_matrix is not None and len(self.faq_texts) > 0:
            q_vec = self.vectorizer.transform([clean_query])
            similarities = cosine_similarity(q_vec, self.faq_matrix).flatten()
            best_idx = int(np.argmax(similarities))
            best_similarity = float(similarities[best_idx])

            if best_similarity >= 0.15:
                best_faq = self.faq_records[best_idx]

        # 5. Search facilities
        facilities = self.search_facilities(clean_query)

        if best_faq and best_similarity >= 0.15:
            # Pick localized answer
            answer_field = f"answer_{detected_lang}"
            answer_text = best_faq.get(answer_field) or best_faq.get("answer_en")

            return ChatResponse(
                answer=answer_text,
                detected_language=detected_lang,
                intent=f"FAQ_{best_faq['category'].upper()}",
                confidence=round(best_similarity, 3),
                flight_guidance=None,
                facility_matches=facilities,
                suggested_prompts=get_prompts_for_language(detected_lang)
            )

        # 6. If facilities matched without FAQ
        if facilities:
            top_fac = facilities[0]
            answer_text = f"Found airport facility: {top_fac['name']} ({top_fac['category']}) located in {top_fac['terminal']} at {top_fac['location_desc']}. Operating hours: {top_fac['opening_hours']}."
            return ChatResponse(
                answer=answer_text,
                detected_language=detected_lang,
                intent="FACILITY_LOOKUP",
                confidence=0.75,
                flight_guidance=None,
                facility_matches=facilities,
                suggested_prompts=get_prompts_for_language(detected_lang)
            )

        # 7. Fallback response
        return ChatResponse(
            answer=get_template(detected_lang, "not_found"),
            detected_language=detected_lang,
            intent="FALLBACK",
            confidence=0.2,
            flight_guidance=None,
            facility_matches=[],
            suggested_prompts=get_prompts_for_language(detected_lang)
        )

# Global singleton
_engine_instance: Optional[KnowledgeEngine] = None

def get_knowledge_engine() -> KnowledgeEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = KnowledgeEngine()
    return _engine_instance

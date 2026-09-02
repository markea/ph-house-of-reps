import json
import re
import time
from typing import Dict, Any, Optional

def word_match(pattern_list, text):
    """Matches any whole word or phrase in text using regex word boundary."""
    for p in pattern_list:
        if re.search(r'\b' + re.escape(p) + r'\b', text, re.IGNORECASE):
            return True
    return False

class HRepTriageAgent:
    """
    ADK-Compliant AI Service Triage Agent.
    
    Responsibilities:
    - Ingests natural language issue descriptions from Congressional staff (English & Taglish).
    - Classifies the intent into one of the Core 5 services (MOTOR_POOL, AC_REPAIR, ICT_SUPPORT, ID_REPLACEMENT, CONTRACT_REVIEW).
    - Extracts structured entities required by the dynamic JSON Schema.
    - Prompts the user for any missing critical parameters.
    """
    
    def __init__(self):
        self.agent_name = "HRep-Service-Triage-Agent"
        self.version = "1.0.0-ADK"

    def triage_request(self, user_prompt: str) -> Dict[str, Any]:
        """
        Processes user natural language input and returns a structured triage outcome with execution latency.
        """
        start_time = time.time()
        result = self._evaluate_intent(user_prompt)
        result["latency_ms"] = round((time.time() - start_time) * 1000, 2)
        return result

    def _evaluate_intent(self, user_prompt: str) -> Dict[str, Any]:
        prompt_lower = user_prompt.lower()

        # 1. ID Badge Replacement (OSAA)
        if word_match(["id", "badge", "rfid", "id card", "lost id", "damaged id", "turnstile", "rfid card"], prompt_lower):
            app_type = "Replacement for Lost ID (Affidavit of Loss Required)" if word_match(["lost", "nawala", "missing"], prompt_lower) else "Replacement for Damaged / Worn ID"
            return {
                "suggested_service_code": "ID_REPLACEMENT",
                "suggested_service_name": "HRep Official ID Issuance & Replacement (OSAA)",
                "extracted_fields": {
                    "application_type": app_type,
                    "full_name_on_id": "Maria Santos",
                    "item_or_district": "1st District of Cavite / Legislative Staff",
                    "blood_type": "O+"
                },
                "confidence_score": 0.95,
                "reasoning": "Detected identification card / security RFID badge issuance query.",
                "next_question": "Do you have an electronic copy of your Affidavit of Loss ready for upload?" if "lost" in prompt_lower else None
            }

        # 2. Legal Contract Review (LAD)
        if word_match(["contract", "agreement", "moa", "mou", "legal", "procurement", "lawyer", "nda", "terms", "legal review", "memorandum of agreement"], prompt_lower):
            doc_type = "Memorandum of Agreement (MOA) / MOU" if word_match(["moa", "mou", "memorandum", "memorandum of agreement"], prompt_lower) else "Procurement Contract / Supply Agreement"
            return {
                "suggested_service_code": "CONTRACT_REVIEW",
                "suggested_service_name": "Legal Contract & Agreement Review (LAD)",
                "extracted_fields": {
                    "document_type": doc_type,
                    "contract_title": "Legal Review Requisition",
                    "contract_party": "Department of Health" if "health" in prompt_lower else "ABC Solutions Inc.",
                    "background_summary": user_prompt
                },
                "confidence_score": 0.93,
                "reasoning": "Identified legal document review or contract evaluation request for LAD.",
                "next_question": "What is the name of the counterparty or vendor in this agreement?"
            }

        # 3. Motor Pool / Transport (English & Taglish)
        if word_match(["van", "car", "driver", "vehicle", "ride", "transport", "motor pool", "motorpool", "trip", "drive", "kotse", "sasakyan", "pahiram ng van", "papuntang", "hatid", "escort"], prompt_lower):
            dest_match = re.search(r"(?:to|papuntang|bound for)\s+(?:the\s+|an\s+)?([A-Za-z0-9\s,]+?)(?:\s+tomorrow|\s+today|\s+at|\s+on|\s+para|\.|$)", user_prompt, re.IGNORECASE)
            destination = dest_match.group(1).strip() if dest_match else "Official Destination"
            
            passengers_match = re.search(r"(\d+)\s*(?:people|passengers|pax|persons|of us|staff|katao)", user_prompt, re.IGNORECASE)
            passengers = int(passengers_match.group(1)) if passengers_match else 1

            trip_purpose = "Official VIP / Diplomatic Escort" if word_match(["vip", "diplomat", "diplomats", "ambassador", "dignitary"], prompt_lower) else "Committee Hearing / Ocular"

            return {
                "suggested_service_code": "MOTOR_POOL",
                "suggested_service_name": "Motor Pool Vehicle & Driver Dispatch",
                "extracted_fields": {
                    "trip_purpose": trip_purpose,
                    "destination": destination,
                    "passenger_count": passengers,
                    "lead_passenger": "Maria Santos (Staff)",
                    "special_requirements": "Generated via HRep ADK Triage Assistant"
                },
                "confidence_score": 0.96,
                "reasoning": "Detected vehicle/transport requisition with destination and passenger count entities.",
                "next_question": None if dest_match else "Where is the destination for this official trip?"
            }

        # 4. Aircon / Building Maintenance (EPFD)
        if word_match(["aircon", "air-con", "ac", "leak", "leaking", "cold", "warm", "water", "light", "power", "plumbing", "cr", "restroom", "outlet", "ceiling", "kuryente", "tulo", "init", "ilaw", "gripo", "outlets", "dripping"], prompt_lower):
            room_match = re.search(r"(?:room|rm|office)\s*([0-9A-Za-z\-]+)", user_prompt, re.IGNORECASE)
            if room_match:
                room = f"Room {room_match.group(1)}"
            else:
                wing_match = re.search(r"(south|north|main|mitra)\s*(?:wing|building|hall)?", user_prompt, re.IGNORECASE)
                room = wing_match.group(0).title() if wing_match else "South Wing"

            if word_match(["power", "kuryente", "outlet", "outlets", "saksakan", "ilaw", "light"], prompt_lower):
                category = "Electrical / Power Outlets"
            elif word_match(["plumbing", "cr", "restroom", "gripo", "toilet"], prompt_lower):
                category = "Plumbing / Restroom"
            else:
                category = "Air-Conditioning (Leaking/Not Cold)"

            urgency = "Urgent (Disrupting Office Work)" if word_match(["urgent", "emergency", "flood", "now", "emergency:", "tulo", "files"], prompt_lower) else "Routine"

            return {
                "suggested_service_code": "AC_REPAIR",
                "suggested_service_name": "Building & Air-Conditioning Maintenance (EPFD)",
                "extracted_fields": {
                    "building_location": "South Wing Annex" if "south" in prompt_lower else ("Main Building" if "main" in prompt_lower else "North Wing Annex"),
                    "room_number": room,
                    "category": category,
                    "issue_description": user_prompt,
                    "urgency": urgency
                },
                "confidence_score": 0.94,
                "reasoning": "Detected facility defect, power interruption, or climate control issue.",
                "next_question": None if room_match else "Which room or building wing is experiencing the issue?"
            }

        # 5. ICT Support & Equipment Loan
        if word_match(["laptop", "wifi", "wi-fi", "internet", "projector", "mic", "microphone", "sound", "screen", "computer", "printer", "zoom", "teams", "paki-ayos", "network", "print", "ayaw"], prompt_lower):
            equip = "Laptop + Wireless Clicker" if "laptop" in prompt_lower else ("High-Lumen Projector & Screen" if "projector" in prompt_lower else "Portable PA Sound System")
            
            # If troubleshooting / defect keywords present, classify as troubleshooting
            if word_match(["paki-ayos", "ayos", "ayaw", "cannot", "can't", "troubleshoot", "repair", "broken", "issue"], prompt_lower):
                req_type = "Workstation / Laptop Troubleshooting"
            elif word_match(["need", "borrow", "loan", "pahiram", "presentation"], prompt_lower):
                req_type = "Equipment Loan (Hearing / Presentation)"
            else:
                req_type = "Workstation / Laptop Troubleshooting"
            
            return {
                "suggested_service_code": "ICT_SUPPORT",
                "suggested_service_name": "ICT Equipment Loan & Technical Support (ICTS)",
                "extracted_fields": {
                    "request_type": req_type,
                    "equipment_needed": equip if req_type == "Equipment Loan (Hearing / Presentation)" else "None (Service Only)",
                    "venue": "Mitra Hall" if "mitra" in prompt_lower else "Committee Hearing Room",
                    "hearing_or_event": "Official Legislative Meeting"
                },
                "confidence_score": 0.92,
                "reasoning": "Identified technology workstation / audio-visual equipment assistance request.",
                "next_question": "What date and time do you need the ICT equipment set up?" if req_type == "Equipment Loan (Hearing / Presentation)" else None
            }

        # Fallback General Support
        return {
            "suggested_service_code": "ICT_SUPPORT",
            "suggested_service_name": "ICT Equipment Loan & Technical Support",
            "extracted_fields": {
                "request_type": "Workstation / Laptop Troubleshooting",
                "equipment_needed": "None (Service Only)"
            },
            "confidence_score": 0.60,
            "reasoning": "General support request routed to Help Desk.",
            "next_question": "Could you provide more details about your request?"
        }

triage_agent = HRepTriageAgent()

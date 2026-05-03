"""
data/symptoms_db.py — Disease-Symptom Knowledge Base
=====================================================
All facts are declared here as pure data — no logic lives in this file.
The Kanren `Relation` objects act as in-memory logic databases.

LOGIC PROGRAMMING CONCEPT: Facts
    A "fact" is an unconditionally true statement.
    E.g., facts(has_symptom, ("flu", "fever")) means:
          "It is a fact that flu has the symptom fever."
"""

from kanren import Relation, facts

# ── Relations (think: database tables) ─────────────────────────────────────
has_symptom      = Relation()   # (disease, symptom)
risk_factor      = Relation()   # (disease, risk_factor)
disease_category = Relation()   # (disease, category)

# ── Disease → Symptom Facts ─────────────────────────────────────────────────
_SYMPTOM_FACTS = [
    # ── Respiratory ──────────────────────────────────────────────────────────
    ("influenza",           "fever"),
    ("influenza",           "cough"),
    ("influenza",           "body_aches"),
    ("influenza",           "fatigue"),
    ("influenza",           "headache"),

    ("common_cold",         "runny_nose"),
    ("common_cold",         "sore_throat"),
    ("common_cold",         "sneezing"),
    ("common_cold",         "mild_cough"),
    ("common_cold",         "congestion"),

    ("covid19",             "fever"),
    ("covid19",             "cough"),
    ("covid19",             "loss_of_taste"),
    ("covid19",             "loss_of_smell"),
    ("covid19",             "fatigue"),
    ("covid19",             "shortness_of_breath"),

    ("pneumonia",           "high_fever"),
    ("pneumonia",           "chest_pain"),
    ("pneumonia",           "productive_cough"),
    ("pneumonia",           "shortness_of_breath"),
    ("pneumonia",           "fatigue"),

    # ── Gastrointestinal ─────────────────────────────────────────────────────
    ("gastroenteritis",     "nausea"),
    ("gastroenteritis",     "vomiting"),
    ("gastroenteritis",     "diarrhea"),
    ("gastroenteritis",     "stomach_cramps"),
    ("gastroenteritis",     "fatigue"),

    ("appendicitis",        "severe_abdominal_pain"),
    ("appendicitis",        "nausea"),
    ("appendicitis",        "fever"),
    ("appendicitis",        "loss_of_appetite"),

    # ── General ──────────────────────────────────────────────────────────────
    ("dehydration",         "dizziness"),
    ("dehydration",         "dry_mouth"),
    ("dehydration",         "fatigue"),
    ("dehydration",         "headache"),

    ("anemia",              "fatigue"),
    ("anemia",              "pallor"),
    ("anemia",              "shortness_of_breath"),
    ("anemia",              "dizziness"),
]

# ── Risk Factor Facts ────────────────────────────────────────────────────────
_RISK_FACTS = [
    ("influenza",           "elderly"),
    ("influenza",           "immunocompromised"),
    ("pneumonia",           "elderly"),
    ("pneumonia",           "smoker"),
    ("covid19",             "elderly"),
    ("covid19",             "obesity"),
    ("anemia",              "vegetarian"),
    ("anemia",              "female"),
    ("dehydration",         "athlete"),
    ("gastroenteritis",     "traveler"),
]

# ── Category Facts ───────────────────────────────────────────────────────────
_CATEGORY_FACTS = [
    ("influenza",           "respiratory"),
    ("common_cold",         "respiratory"),
    ("covid19",             "respiratory"),
    ("pneumonia",           "respiratory"),
    ("gastroenteritis",     "gastrointestinal"),
    ("appendicitis",        "gastrointestinal"),
    ("dehydration",         "general"),
    ("anemia",              "general"),
]

# ── Human-Readable Descriptions ─────────────────────────────────────────────
DISEASE_DESCRIPTIONS: dict[str, str] = {
    "influenza":        "A contagious viral infection affecting the respiratory tract.",
    "common_cold":      "A mild upper-respiratory infection caused by various viruses.",
    "covid19":          "An infectious disease caused by the SARS-CoV-2 coronavirus.",
    "pneumonia":        "Infection inflaming air sacs in one or both lungs.",
    "gastroenteritis":  "Inflammation of the stomach and intestines (stomach flu).",
    "appendicitis":     "Inflammation of the appendix — requires urgent medical care.",
    "dehydration":      "Occurs when fluid loss exceeds fluid intake.",
    "anemia":           "Insufficient healthy red blood cells to carry adequate oxygen.",
}

VALID_SYMPTOMS: list[str] = sorted({s for _, s in _SYMPTOM_FACTS})
VALID_RISK_FACTORS: list[str] = sorted({r for _, r in _RISK_FACTS})


def load_facts() -> None:
    """
    Assert all facts into their Kanren Relations.
    Must be called once before any query is run.
    """
    facts(has_symptom,      *_SYMPTOM_FACTS)
    facts(risk_factor,      *_RISK_FACTS)
    facts(disease_category, *_CATEGORY_FACTS)
    print("[MedLogic] Knowledge base loaded: "
          f"{len(_SYMPTOM_FACTS)} symptom facts, "
          f"{len(_RISK_FACTS)} risk facts.")

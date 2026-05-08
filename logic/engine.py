"""
logic/engine.py — Core Logic Engine (Kanren / miniKanren)
==========================================================
This is the most important file for understanding Logic Programming.

KEY CONCEPTS DEMONSTRATED:
    1. Logic Variables  — placeholders that Kanren fills via unification
    2. Relations        — declared facts about the world
    3. Goals            — constraints that must be satisfied
    4. run()            — asks "find all X such that all goals hold"
    5. Conjunction      — multiple goals = AND (all must be true)

Unlike imperative code ("FOR each disease, IF it has this symptom..."),
logic code DECLARES what we want: "Give me all diseases such that
they have symptom A AND symptom B." Kanren figures out HOW.
"""

from kanren import run, var
from data.symptoms_db import has_symptom, risk_factor, disease_category


# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 1: Basic Relational Queries
# ─────────────────────────────────────────────────────────────────────────────

def diseases_with_symptom(symptom: str) -> tuple:
    disease = var()
    return run(0, disease, has_symptom(disease, symptom))


def symptoms_of_disease(disease_name: str) -> tuple:
    symptom = var()
    return run(0, symptom, has_symptom(disease_name, symptom))


def diseases_in_category(category: str) -> tuple:
    disease = var()
    return run(0, disease, disease_category(disease, category))


# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 2: Multi-Symptom Conjunction (the real magic of logic programming)
# ─────────────────────────────────────────────────────────────────────────────

def diagnose_exact(symptoms: list[str]) -> tuple:
    if not symptoms:
        return ()
    disease = var()
    goals = [has_symptom(disease, s) for s in symptoms]
    return run(0, disease, *goals)


# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 3: Scored Partial Matching (reasoning over logic results)
# ─────────────────────────────────────────────────────────────────────────────

def diagnose_scored(symptoms: list[str]) -> dict[str, dict]:
    if not symptoms:
        return {}
    # Collect all candidate diseases (union of symptom lookups)
    candidates: set[str] = set()
    for s in symptoms:
        candidates.update(diseases_with_symptom(s))

    exact_matches = set(diagnose_exact(symptoms))
    input_set = set(symptoms)

    scores: dict[str, dict] = {}
    for disease in candidates:
        disease_symptoms = set(symptoms_of_disease(disease))
        matched = disease_symptoms & input_set

        coverage  = len(matched) / len(disease_symptoms) if disease_symptoms else 0
        relevance = len(matched) / len(input_set)        if input_set       else 0

        scores[disease] = {
            "matched_symptoms":   sorted(matched),
            "missing_symptoms":   sorted(disease_symptoms - input_set),
            "total_symptoms":     len(disease_symptoms),
            "match_count":        len(matched),
            "coverage":           round(coverage, 3),
            "relevance":          round(relevance, 3),
            "score":              round((coverage + relevance) / 2, 3),
            "is_exact_match":     disease in exact_matches,
        }

    return dict(sorted(scores.items(), key=lambda x: x[1]["score"], reverse=True))


# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 4: Risk Factor Reasoning
# ─────────────────────────────────────────────────────────────────────────────

def applicable_risks(disease_name: str, patient_profile: list[str]) -> list[str]:
    risk = var()
    all_risks = run(0, risk, risk_factor(disease_name, risk))
    return [r for r in all_risks if r in patient_profile]

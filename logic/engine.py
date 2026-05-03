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
    """
    LOGIC QUERY: "What diseases have this symptom?"

    disease = var()          → create a logic variable (unknown)
    has_symptom(disease, symptom)  → goal: disease must be related to symptom
    run(0, disease, goal)    → find ALL values of `disease` satisfying the goal
                               (0 means "no limit")
    """
    disease = var()
    return run(0, disease, has_symptom(disease, symptom))


def symptoms_of_disease(disease_name: str) -> tuple:
    """
    LOGIC QUERY: "What symptoms does this disease have?"
    The logic variable is now on the symptom side — same relation, reversed.
    This shows BIDIRECTIONAL querying: one relation, two query directions.
    """
    symptom = var()
    return run(0, symptom, has_symptom(disease_name, symptom))


def diseases_in_category(category: str) -> tuple:
    """LOGIC QUERY: "What diseases belong to this category?" """
    disease = var()
    return run(0, disease, disease_category(disease, category))


# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 2: Multi-Symptom Conjunction (the real magic of logic programming)
# ─────────────────────────────────────────────────────────────────────────────

def diagnose_exact(symptoms: list[str]) -> tuple:
    """
    LOGIC QUERY: "What disease has ALL of these symptoms?"

    This is CONJUNCTION — multiple goals all applied to the SAME variable.
    Kanren finds values of `disease` that satisfy EVERY goal simultaneously.

    Imperative equivalent (for comparison):
        results = []
        for disease in all_diseases:
            if all(disease_has(disease, s) for s in symptoms):
                results.append(disease)

    Logic equivalent (what we write):
        disease = var()
        goals = [has_symptom(disease, s) for s in symptoms]
        return run(0, disease, *goals)     ← Kanren does the searching
    """
    if not symptoms:
        return ()
    disease = var()
    goals = [has_symptom(disease, s) for s in symptoms]
    return run(0, disease, *goals)


# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 3: Scored Partial Matching (reasoning over logic results)
# ─────────────────────────────────────────────────────────────────────────────

def diagnose_scored(symptoms: list[str]) -> dict[str, dict]:
    """
    Ranked diagnosis using symptom overlap scoring.

    Steps:
        1. Find all diseases that have ANY of the given symptoms
        2. For each candidate disease, compute a match score
        3. Return sorted results with exact-match flag

    Score formula:
        coverage  = matched / total_disease_symptoms   (how "complete" is the match?)
        relevance = matched / total_input_symptoms     (how "specific" to the input?)
        score     = average(coverage, relevance)
    """
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
    """
    LOGIC QUERY + FILTER:
    Find which known risk factors for this disease apply to the patient.
    """
    risk = var()
    all_risks = run(0, risk, risk_factor(disease_name, risk))
    return [r for r in all_risks if r in patient_profile]

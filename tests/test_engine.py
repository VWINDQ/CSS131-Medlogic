"""
tests/test_engine.py — Unit Tests for the Logic Engine
=========================================================
Run with:  pytest tests/ -v

Each test group targets one layer of the architecture:
    TestDataLayer    → facts loading and data integrity
    TestEngineLayer  → raw Kanren query correctness
    TestReasonerLayer → reasoning pipeline + enrichment
"""

import pytest

from data.symptoms_db import (
    load_facts, VALID_SYMPTOMS, VALID_RISK_FACTORS, DISEASE_DESCRIPTIONS
)
from logic.engine import (
    diseases_with_symptom,
    symptoms_of_disease,
    diseases_in_category,
    diagnose_exact,
    diagnose_scored,
    applicable_risks,
)
from logic.reasoner import analyze, explain_query, DiagnosisResult


# ── Fixture: load facts once per test session ─────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def load_knowledge_base():
    load_facts()


# ─────────────────────────────────────────────────────────────────────────────
# Data Layer Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestDataLayer:

    def test_valid_symptoms_not_empty(self):
        assert len(VALID_SYMPTOMS) > 0

    def test_valid_risk_factors_not_empty(self):
        assert len(VALID_RISK_FACTORS) > 0

    def test_all_diseases_have_descriptions(self):
        """Every disease referenced in facts should have a description."""
        for disease in DISEASE_DESCRIPTIONS:
            syms = symptoms_of_disease(disease)
            assert len(syms) > 0, f"{disease} has no symptoms in the knowledge base"


# ─────────────────────────────────────────────────────────────────────────────
# Engine / Kanren Layer Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestEngineLayer:

    def test_diseases_with_fever(self):
        results = diseases_with_symptom("fever")
        assert "influenza"   in results
        assert "covid19"     in results
        assert "appendicitis" in results
        # common_cold does NOT have "fever" in the knowledge base
        assert "common_cold" not in results

    def test_symptoms_of_influenza(self):
        syms = symptoms_of_disease("influenza")
        assert "fever"    in syms
        assert "cough"    in syms
        assert "fatigue"  in syms
        # loss_of_taste is covid, not flu
        assert "loss_of_taste" not in syms

    def test_bidirectional_query_same_relation(self):
        """The same `has_symptom` relation works in both query directions."""
        diseases = diseases_with_symptom("cough")
        assert "influenza" in diseases

        symptoms = symptoms_of_disease("influenza")
        assert "cough" in symptoms

    def test_diseases_in_category(self):
        respiratory = diseases_in_category("respiratory")
        assert "influenza"   in respiratory
        assert "common_cold" in respiratory
        assert "anemia"      not in respiratory

    def test_diagnose_exact_flu_full_symptoms(self):
        flu_syms = ["fever", "cough", "body_aches", "fatigue", "headache"]
        result = diagnose_exact(flu_syms)
        assert "influenza" in result

    def test_diagnose_exact_no_match(self):
        result = diagnose_exact(["purple_spots", "extra_arm"])
        assert len(result) == 0

    def test_diagnose_exact_empty_input(self):
        result = diagnose_exact([])
        assert result == ()

    def test_diagnose_scored_returns_scores(self):
        scored = diagnose_scored(["fever", "cough"])
        assert isinstance(scored, dict)
        assert len(scored) > 0
        for disease, data in scored.items():
            assert 0.0 <= data["score"] <= 1.0
            assert "matched_symptoms" in data
            assert "is_exact_match"   in data

    def test_diagnose_scored_flu_highest_for_flu_symptoms(self):
        flu_syms = ["fever", "cough", "body_aches", "fatigue", "headache"]
        scored = diagnose_scored(flu_syms)
        top_disease = list(scored.keys())[0]
        assert top_disease == "influenza"

    def test_applicable_risks_match(self):
        risks = applicable_risks("influenza", ["elderly", "vegetarian"])
        assert "elderly" in risks
        assert "vegetarian" not in risks

    def test_applicable_risks_no_match(self):
        risks = applicable_risks("influenza", ["traveler"])
        assert risks == []


# ─────────────────────────────────────────────────────────────────────────────
# Reasoner Layer Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestReasonerLayer:

    def test_analyze_returns_list_of_results(self):
        results = analyze(["fever", "cough"])
        assert isinstance(results, list)
        assert all(isinstance(r, DiagnosisResult) for r in results)

    def test_analyze_top_n_respected(self):
        results = analyze(["fever", "cough", "fatigue"], top_n=2)
        assert len(results) <= 2

    def test_analyze_confidence_labels(self):
        results = analyze(["fever", "cough", "body_aches", "fatigue", "headache"])
        influenza_results = [r for r in results if r.disease == "influenza"]
        assert len(influenza_results) == 1
        assert influenza_results[0].confidence in ("HIGH", "MEDIUM", "LOW")

    def test_analyze_risk_boosting(self):
        """Score with matching risk factor should be >= score without."""
        base = analyze(["fever", "cough"], patient_profile=[])
        boosted = analyze(["fever", "cough"], patient_profile=["elderly"])
        # Find influenza in both
        base_flu = next((r for r in base if r.disease == "influenza"), None)
        boost_flu = next((r for r in boosted if r.disease == "influenza"), None)
        if base_flu and boost_flu:
            assert boost_flu.score >= base_flu.score

    def test_analyze_empty_symptoms(self):
        results = analyze([])
        assert results == []

    def test_display_name_formatting(self):
        r = DiagnosisResult(
            disease="common_cold",
            score=0.5, confidence="MEDIUM",
            matched_symptoms=[], missing_symptoms=[],
            description="test",
        )
        assert r.display_name == "Common Cold"
        assert r.score_pct == 50

    def test_explain_query_output(self):
        explanation = explain_query(["fever", "cough"])
        assert "var()" in explanation
        assert "fever" in explanation
        assert "cough" in explanation
        assert "run(0" in explanation

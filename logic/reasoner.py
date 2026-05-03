"""
logic/reasoner.py — High-Level Reasoning API
=============================================
Translates raw logic engine output into structured, enriched results.
This layer isolates the interface from Kanren internals.

DESIGN PRINCIPLE: The interface layer should never import from kanren.
    Interface → Reasoner → Engine (Kanren) → Data
"""

from dataclasses import dataclass, field
from logic.engine import diagnose_scored, applicable_risks, symptoms_of_disease
from data.symptoms_db import DISEASE_DESCRIPTIONS


# ─────────────────────────────────────────────────────────────────────────────
# Data Transfer Object
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class DiagnosisResult:
    """
    Structured result for a single disease candidate.
    Using @dataclass for clean, self-documenting field declarations.
    """
    disease:             str
    score:               float
    confidence:          str           # "HIGH" / "MEDIUM" / "LOW"
    matched_symptoms:    list[str]
    missing_symptoms:    list[str]
    description:         str
    risk_factors:        list[str] = field(default_factory=list)
    is_exact_match:      bool = False

    @property
    def display_name(self) -> str:
        return self.disease.replace("_", " ").title()

    @property
    def score_pct(self) -> int:
        return round(self.score * 100)

    def __repr__(self) -> str:
        return (
            f"DiagnosisResult({self.display_name!r}, "
            f"score={self.score_pct}%, "
            f"confidence={self.confidence!r})"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────────

def _confidence_label(score: float) -> str:
    """Map a numeric score to a human-readable confidence label."""
    if score >= 0.70:
        return "HIGH"
    if score >= 0.40:
        return "MEDIUM"
    return "LOW"


def _boost_with_risk(base_score: float, risk_count: int) -> float:
    """
    Slightly elevate a score when patient risk factors match the disease.
    Cap at 1.0 to prevent score inflation.
    """
    return min(base_score + 0.05 * risk_count, 1.0)


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def analyze(
    symptoms: list[str],
    patient_profile: list[str] | None = None,
    top_n: int = 5,
) -> list[DiagnosisResult]:
    """
    Full reasoning pipeline:
        1. Delegate to Kanren logic engine for scored candidates
        2. Enrich each candidate with risk factors and description
        3. Optionally boost scores based on patient risk profile
        4. Return top-N DiagnosisResult objects, sorted by score

    Args:
        symptoms:        List of symptom strings (must be in VALID_SYMPTOMS)
        patient_profile: List of applicable risk factors for this patient
        top_n:           Maximum number of results to return

    Returns:
        List of DiagnosisResult, highest score first
    """
    if patient_profile is None:
        patient_profile = []

    raw = diagnose_scored(symptoms)
    results: list[DiagnosisResult] = []

    for disease, data in raw.items():
        risks = applicable_risks(disease, patient_profile)
        boosted = _boost_with_risk(data["score"], len(risks))

        result = DiagnosisResult(
            disease=disease,
            score=round(boosted, 3),
            confidence=_confidence_label(boosted),
            matched_symptoms=data["matched_symptoms"],
            missing_symptoms=data["missing_symptoms"],
            description=DISEASE_DESCRIPTIONS.get(disease, "No description available."),
            risk_factors=risks,
            is_exact_match=data["is_exact_match"],
        )
        results.append(result)

    results.sort(key=lambda r: r.score, reverse=True)
    return results[:top_n]


def explain_query(symptoms: list[str]) -> str:
    """
    Generate a human-readable explanation of the logic query being executed.
    Great for the classroom: shows what Kanren is doing under the hood.
    """
    if not symptoms:
        return "No symptoms provided."

    goals = "\n    ".join([f"has_symptom(disease, '{s}')" for s in symptoms])
    return (
        f"Logic query being executed:\n\n"
        f"    disease = var()   # logic variable\n"
        f"    run(0, disease,\n"
        f"    {goals}\n"
        f"    )\n\n"
        f"Kanren searches for all values of `disease` satisfying ALL {len(symptoms)} goal(s)."
    )

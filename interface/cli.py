"""
interface/cli.py — Command-Line Interface
==========================================
Handles all user input/output. Imports only from interface layer
and reasoner. Has no direct knowledge of Kanren or data structures.
"""

from colorama import init, Fore, Style
from interface.formatter import (
    display_banner,
    display_symptoms_list,
    display_results,
    display_logic_explanation,
)
from logic.reasoner import analyze, explain_query
from data.symptoms_db import VALID_SYMPTOMS, VALID_RISK_FACTORS

init(autoreset=True)  # Enable cross-platform ANSI colour codes


def _prompt(label: str, hint: str = "") -> str:
    """Consistent input prompt with optional hint text."""
    if hint:
        print(f"{Style.DIM}  {hint}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}{label}{Style.RESET_ALL}", end="")
    return input(" ").strip().lower()


def _parse_csv_input(raw: str, valid: list[str]) -> tuple[list[str], list[str]]:
    """Parse comma-separated input, separate valid from unrecognised tokens."""
    tokens = [t.strip().replace(" ", "_") for t in raw.split(",") if t.strip()]
    valid_tokens   = [t for t in tokens if t in valid]
    invalid_tokens = [t for t in tokens if t not in valid]
    return valid_tokens, invalid_tokens


def _get_symptoms() -> list[str]:
    display_symptoms_list(VALID_SYMPTOMS)

    while True:
        raw = _prompt(
            "Enter symptoms (comma-separated):",
            hint="Example: fever, cough, fatigue"
        )
        symptoms, unknown = _parse_csv_input(raw, VALID_SYMPTOMS)

        if unknown:
            print(f"  {Fore.YELLOW}Unrecognised symptoms ignored: "
                  f"{', '.join(unknown)}{Style.RESET_ALL}")
        if symptoms:
            return symptoms

        print(f"  {Fore.RED}No valid symptoms found. Please try again.{Style.RESET_ALL}\n")


def _get_risk_profile() -> list[str]:
    raw = _prompt(
        "Risk factors (optional, press Enter to skip):",
        hint=f"Options: {', '.join(VALID_RISK_FACTORS)}"
    )
    if not raw:
        return []
    profile, _ = _parse_csv_input(raw, VALID_RISK_FACTORS)
    return profile


def _ask_show_query() -> bool:
    raw = _prompt("Show the underlying Kanren logic query? (y/n):")
    return raw.startswith("y")


def run_cli() -> None:
    """Main application loop."""
    display_banner()

    while True:
        # ── Step 1: Collect symptoms ──────────────────────────────────────
        symptoms = _get_symptoms()

        # ── Step 2: Collect optional risk profile ────────────────────────
        risk_profile = _get_risk_profile()

        # ── Step 3: Optionally show the Kanren query ──────────────────────
        if _ask_show_query():
            display_logic_explanation(explain_query(symptoms))

        # ── Step 4: Run analysis ──────────────────────────────────────────
        print(f"\n  {Fore.BLUE}Querying logic engine "
              f"({len(symptoms)} symptom(s))...{Style.RESET_ALL}")
        results = analyze(symptoms, risk_profile)

        # ── Step 5: Display results ───────────────────────────────────────
        display_results(results, symptoms)

        # ── Step 6: Loop or exit ──────────────────────────────────────────
        again = _prompt("Run another diagnosis? (y/n):")
        if not again.startswith("y"):
            print(f"\n  {Fore.GREEN}Thank you for using MedLogic. Stay healthy!{Style.RESET_ALL}\n")
            break

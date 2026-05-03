"""
interface/formatter.py — Display & Formatting Utilities
========================================================
All terminal rendering lives here. Zero logic, zero data.
If you swap CLI for a web UI, only this file changes.
"""

from colorama import Fore, Back, Style

BANNER = r"""
  __  __          _ _               _      _
 |  \/  | ___  __| | |   ___   __ _(_) ___| |
 | |\/| |/ _ \/ _` | |  / _ \ / _` | |/ __| |
 | |  | |  __/ (_| | | | (_) | (_| | | (__ |_|
 |_|  |_|\___|\__,_|_|  \___/ \__, |_|\___(_)
                                |___/
"""

_CONFIDENCE_STYLE = {
    "HIGH":   Fore.GREEN,
    "MEDIUM": Fore.YELLOW,
    "LOW":    Fore.RED,
}

_BAR_WIDTH = 20
_SEPARATOR = "─" * 60


def _score_bar(score: float) -> str:
    """Render a simple ASCII progress bar for the confidence score."""
    filled = round(score * _BAR_WIDTH)
    bar = "█" * filled + "░" * (_BAR_WIDTH - filled)
    return f"[{bar}] {round(score * 100):>3}%"


def display_banner() -> None:
    print(f"{Fore.CYAN}{BANNER}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Logic-Based Symptom Diagnosis System{Style.RESET_ALL}")
    print(f"  {Style.DIM}Powered by miniKanren — Relational Logic Programming{Style.RESET_ALL}")
    print(f"  {_SEPARATOR}\n")


def display_symptoms_list(symptoms: list[str]) -> None:
    print(f"{Fore.WHITE}Available symptoms:{Style.RESET_ALL}")
    cols = 4
    for i in range(0, len(symptoms), cols):
        row = symptoms[i : i + cols]
        print("  " + "  ".join(f"{Fore.CYAN}{s:<24}{Style.RESET_ALL}" for s in row))
    print()


def display_results(results, input_symptoms: list[str]) -> None:
    """Render top diagnosis results to the terminal."""
    print(f"\n{Fore.WHITE}{'═' * 60}")
    print(f"  DIAGNOSIS RESULTS  ·  {len(input_symptoms)} symptom(s) entered")
    print(f"{'═' * 60}{Style.RESET_ALL}\n")

    if not results:
        print(f"  {Fore.RED}No matching diagnoses found.{Style.RESET_ALL}")
        print(f"  {Style.DIM}Try entering more symptoms.{Style.RESET_ALL}\n")
        return

    for rank, result in enumerate(results, start=1):
        conf_color = _CONFIDENCE_STYLE.get(result.confidence, Fore.WHITE)
        exact_tag = (
            f"  {Back.GREEN}{Fore.BLACK} EXACT MATCH {Style.RESET_ALL}"
            if result.is_exact_match else ""
        )

        # ── Disease name + exact-match badge
        print(f"  {Fore.WHITE}#{rank}  {result.display_name.upper()}{exact_tag}")

        # ── Confidence bar
        print(f"      {conf_color}{_score_bar(result.score)}  "
              f"{result.confidence}{Style.RESET_ALL}")

        # ── Matched symptoms (what we found)
        matched_str = (
            f"{Fore.GREEN}{', '.join(result.matched_symptoms)}{Style.RESET_ALL}"
            if result.matched_symptoms else f"{Style.DIM}none{Style.RESET_ALL}"
        )
        print(f"      {Fore.WHITE}Matched:    {matched_str}")

        # ── Missing symptoms (what to watch for)
        if result.missing_symptoms:
            missing_str = f"{Fore.YELLOW}{', '.join(result.missing_symptoms[:3])}"
            if len(result.missing_symptoms) > 3:
                missing_str += f" (+{len(result.missing_symptoms) - 3} more)"
            print(f"      {Fore.WHITE}Watch for:  {missing_str}{Style.RESET_ALL}")

        # ── Risk factors
        if result.risk_factors:
            print(f"      {Fore.WHITE}Risk flags: "
                  f"{Fore.RED}{', '.join(result.risk_factors)}{Style.RESET_ALL}")

        # ── Description
        print(f"      {Style.DIM}{result.description}{Style.RESET_ALL}")
        print()

    print(f"  {Style.DIM}⚠  Educational demo only — always consult a qualified doctor.{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}{'═' * 60}{Style.RESET_ALL}\n")


def display_logic_explanation(explanation: str) -> None:
    """Show the underlying Kanren query — great for classroom demos."""
    print(f"\n  {Fore.CYAN}[ Kanren Query ]{Style.RESET_ALL}")
    print(f"  {Style.DIM}{_SEPARATOR}{Style.RESET_ALL}")
    for line in explanation.splitlines():
        print(f"  {Fore.YELLOW}{line}{Style.RESET_ALL}")
    print()

"""
tools/file_writer.py

Utility functions for writing generated agent outputs to local files.
"""

from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs"


def save_proposal(proposal_text: str, output_dir: Path | None = None) -> str:
    """
    Saves a generated freelance proposal to a timestamped text file.

    Args:
        proposal_text: The proposal content to write.
        output_dir: Optional custom output directory.

    Returns:
        The absolute path to the saved proposal file.
    """
    target_dir = output_dir or DEFAULT_OUTPUT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = target_dir / f"proposal_{timestamp}.txt"
    output_path.write_text(proposal_text.strip() + "\n", encoding="utf-8")

    return str(output_path)

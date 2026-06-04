from fastmcp import FastMCP
import json
from pathlib import Path

import fitz  # pymupdf

mcp = FastMCP("Oregon IT Policy Search")

# --- Load and index PDFs at startup ---

POLICIES = []  # list of {"id": str, "title": str, "number": str, "text": str}
PDF_DIR = Path(__file__).parent / "pdfs"

# Fallback titles for scanned-image PDFs that have no extractable text
KNOWN_TITLES = {
    "107-004-051": "Controlling Portable and Removable Storage Devices",
    "107-004-053": "Employee Security",
    "107-001-016": "Mobile Communication Device Usage While Driving",
    "107-004-015": "Internal Controls for Managing Mobile Communications Devices",
    "107-004-120": "Cyber and Information Security Incident Response",
}


def extract_policies():
    """Load all PDFs from the pdfs/ directory and extract their text."""
    global POLICIES
    POLICIES = []
    for pdf_path in sorted(PDF_DIR.glob("*.pdf")):
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

        # Extract the SUBJECT line as the title
        lines = [l.strip() for l in full_text.split("\n") if l.strip()]
        title = "Unknown"
        for i, line in enumerate(lines):
            if line.upper().startswith("SUBJECT"):
                # Subject may be on same line or next line
                after_colon = line.split(":", 1)[1].strip() if ":" in line else ""
                if after_colon:
                    # Clean up: stop at APPROVED, NUMBER, or similar headers
                    for stop_word in ["APPROVED", "NUMBER", "SIGNATURE"]:
                        if stop_word in after_colon:
                            after_colon = after_colon[:after_colon.index(stop_word)].strip()
                    title = after_colon
                elif i + 1 < len(lines):
                    title = lines[i + 1]
                break

        policy_number = pdf_path.stem  # filename without .pdf

        # Use known title if extraction failed
        if title == "Unknown" and policy_number in KNOWN_TITLES:
            title = KNOWN_TITLES[policy_number]

        searchable = len(full_text.strip()) > 0

        POLICIES.append({
            "id": policy_number,
            "number": policy_number,
            "title": title,
            "filename": pdf_path.name,
            "text": full_text,
            "searchable": searchable,
        })


# Load on import
extract_policies()


# --- MCP Tools ---

@mcp.tool()
async def list_policies() -> str:
    """List all available Oregon statewide IT policies.

    Returns a list of every policy with its number and title.
    Use this to see what policies are available before searching.
    """
    result = []
    for p in POLICIES:
        entry = {
            "number": p["number"],
            "title": p["title"],
        }
        if not p["searchable"]:
            entry["note"] = "Scanned image — not searchable"
        result.append(entry)
    return json.dumps(result, indent=2)


@mcp.tool()
async def search_policies(query: str, max_results: int = 5) -> str:
    """Search across all Oregon IT policies by keyword or phrase.

    Searches the full text of every policy document. Returns matching
    excerpts with the policy number and title so you can understand
    the context.

    Args:
        query: Word or phrase to search for (e.g., "cloud", "incident response", "acceptable use", "AI")
        max_results: Maximum number of matching excerpts to return (default 5)
    """
    query_lower = query.lower()
    matches = []

    for policy in POLICIES:
        text_lower = policy["text"].lower()
        if query_lower not in text_lower:
            continue

        # Find matching excerpts (surrounding context)
        lines = policy["text"].split("\n")
        for i, line in enumerate(lines):
            if query_lower in line.lower():
                # Grab surrounding lines for context
                start = max(0, i - 1)
                end = min(len(lines), i + 3)
                excerpt = "\n".join(lines[start:end]).strip()
                if excerpt:
                    matches.append({
                        "policy_number": policy["number"],
                        "policy_title": policy["title"],
                        "excerpt": excerpt,
                    })
                    if len(matches) >= max_results:
                        break
        if len(matches) >= max_results:
            break

    if not matches:
        return f"No results found for '{query}' across {len(POLICIES)} policies."

    return json.dumps(matches, indent=2)


@mcp.tool()
async def get_policy(policy_number: str) -> str:
    """Get the full text of a specific Oregon IT policy by its number.

    Args:
        policy_number: The policy number (e.g., "107-004-052", "107-004-110")
    """
    for policy in POLICIES:
        if policy["number"] == policy_number or policy["id"] == policy_number:
            return json.dumps({
                "number": policy["number"],
                "title": policy["title"],
                "full_text": policy["text"],
            }, indent=2)

    available = [p["number"] for p in POLICIES]
    return f"Policy '{policy_number}' not found. Available policies: {', '.join(available)}"


if __name__ == "__main__":
    mcp.run()

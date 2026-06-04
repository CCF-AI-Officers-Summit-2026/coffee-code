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


@mcp.tool()
async def compare_policies(query: str) -> str:
    """Find which Oregon IT policies mention a topic and how prominently.

    Unlike search_policies (which returns excerpts), this gives a bird's-eye
    view: every policy that mentions the query, ranked by how many times the
    topic appears. Use this to understand which policies are most relevant
    to a topic before diving into details.

    Args:
        query: Topic to search for (e.g., "encryption", "cloud", "training", "PII")
    """
    query_lower = query.lower()
    hits = []

    for policy in POLICIES:
        text_lower = policy["text"].lower()
        count = text_lower.count(query_lower)
        if count > 0:
            hits.append({
                "policy_number": policy["number"],
                "policy_title": policy["title"],
                "mentions": count,
            })

    if not hits:
        return f"No policies mention '{query}'."

    hits.sort(key=lambda h: h["mentions"], reverse=True)
    return json.dumps({
        "query": query,
        "policies_matched": len(hits),
        "results": hits,
    }, indent=2)


# Section headers commonly found in Oregon IT policies
SECTION_HEADERS = [
    "PURPOSE",
    "APPLICABILITY",
    "DEFINITIONS",
    "GENERAL INFORMATION",
    "RESPONSIBILITY",
    "REFERENCE",
    "PROCEDURE",
    "EXCLUSIONS AND SPECIAL SITUATIONS",
    "FORMS/EXHIBITS/INSTRUCTIONS",
]


def _extract_sections(text: str) -> dict:
    """Split policy text into named sections based on standard headers."""
    import re
    lines = text.split("\n")
    sections = {}
    current_section = None
    current_lines = []

    for line in lines:
        stripped = line.strip()
        # Check if this line is a section header
        matched_header = None
        for header in SECTION_HEADERS:
            if stripped.upper() == header or stripped.upper().startswith(header + " "):
                matched_header = header
                break

        if matched_header:
            # Save previous section
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = matched_header.title()
            current_lines = []
        elif current_section:
            current_lines.append(line)

    # Save the last section
    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

    return sections


@mcp.tool()
async def get_policy_section(policy_number: str, section: str = "") -> str:
    """Get a specific section from an Oregon IT policy.

    Instead of reading the full policy, pull out just the section you need.
    Common sections: Purpose, Applicability, Definitions, General Information,
    Responsibility, Reference, Procedure.

    Args:
        policy_number: The policy number (e.g., "107-004-052")
        section: Section name to extract (e.g., "Purpose", "Definitions"). Leave blank to list available sections.
    """
    for policy in POLICIES:
        if policy["number"] == policy_number or policy["id"] == policy_number:
            sections = _extract_sections(policy["text"])

            if not section:
                return json.dumps({
                    "policy_number": policy["number"],
                    "policy_title": policy["title"],
                    "available_sections": list(sections.keys()),
                }, indent=2)

            # Fuzzy match the section name
            section_lower = section.lower()
            for name, content in sections.items():
                if section_lower in name.lower():
                    return json.dumps({
                        "policy_number": policy["number"],
                        "policy_title": policy["title"],
                        "section": name,
                        "content": content,
                    }, indent=2)

            return json.dumps({
                "error": f"Section '{section}' not found in policy {policy_number}.",
                "available_sections": list(sections.keys()),
            }, indent=2)

    available = [p["number"] for p in POLICIES]
    return f"Policy '{policy_number}' not found. Available policies: {', '.join(available)}"


if __name__ == "__main__":
    mcp.run()

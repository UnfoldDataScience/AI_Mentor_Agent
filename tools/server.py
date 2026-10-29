import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from mcp.server.mcpserver import MCPServer

ARXIV_API = "https://export.arxiv.org/api/query"
GITHUB_API = "https://api.github.com/search/repositories"
ATOM = "{http://www.w3.org/2005/Atom}"
USER_AGENT = "ai-mentor-mcp"
TIMEOUT = 15

server = MCPServer("ai-mentor-research")


def _fetch(url: str, headers: dict = None) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read()


@server.tool(
    description=(
        "Search arXiv for real, published AI/ML research papers. Returns titles, authors, "
        "publication dates, summaries, and links. Use when the learner asks for papers, "
        "research, the original source of an idea, or the latest work on a topic."
    ),
    structured_output=False,
)
def search_arxiv_papers(query: str, max_results: int = 5) -> str:
    params = urllib.parse.urlencode(
        {
            "search_query": f"all:{query}",
            "max_results": max(1, min(max_results, 10)),
            "sortBy": "relevance",
        }
    )
    root = ET.fromstring(_fetch(f"{ARXIV_API}?{params}"))
    entries = root.findall(f"{ATOM}entry")
    if not entries:
        return f"No arXiv papers found for '{query}'."

    papers = []
    for i, entry in enumerate(entries, start=1):
        title = " ".join(entry.findtext(f"{ATOM}title", "").split())
        summary = " ".join(entry.findtext(f"{ATOM}summary", "").split())
        authors = [a.findtext(f"{ATOM}name", "") for a in entry.findall(f"{ATOM}author")]
        author_text = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "")
        papers.append(
            f"[{i}] {title}\n"
            f"Authors: {author_text}\n"
            f"Published: {entry.findtext(f'{ATOM}published', '')[:10]}\n"
            f"Link: {entry.findtext(f'{ATOM}id', '')}\n"
            f"Summary: {summary[:500]}"
        )
    return "\n\n".join(papers)


@server.tool(
    description=(
        "Search GitHub for real, popular open-source repositories, sorted by stars. Returns "
        "names, descriptions, star counts, main language, and links. Use when the learner "
        "asks for example code, libraries, open-source projects, or real repos to study."
    ),
    structured_output=False,
)
def search_github_repos(query: str, max_results: int = 5) -> str:
    params = urllib.parse.urlencode(
        {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": max(1, min(max_results, 10)),
        }
    )
    data = json.loads(
        _fetch(f"{GITHUB_API}?{params}", headers={"Accept": "application/vnd.github+json"})
    )
    repos = data.get("items", [])
    if not repos:
        return f"No GitHub repositories found for '{query}'."

    return "\n\n".join(
        f"[{i}] {repo['full_name']} — ⭐ {repo['stargazers_count']:,}\n"
        f"Language: {repo.get('language') or 'n/a'}\n"
        f"Link: {repo['html_url']}\n"
        f"Description: {repo.get('description') or 'No description'}"
        for i, repo in enumerate(repos, start=1)
    )


if __name__ == "__main__":
    server.run()

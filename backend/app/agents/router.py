import re


def detect_routes(message: str):
    """
    Detect which MCP capabilities are required
    from the user's natural-language request.
    """

    text = message.lower()

    routes = []

    # --------------------------------------------------
    # GOOGLE NEWS
    # --------------------------------------------------

    news_keywords = [
        "latest news",
        "latest",
        "breaking news",
        "today's news",
        "today news",
        "recent news",
        "current news",
        "news about",
        "news on",
        "headlines",
    ]

    if any(keyword in text for keyword in news_keywords):
        routes.append("google_news")

    # --------------------------------------------------
    # WEB SEARCH
    # --------------------------------------------------

    web_keywords = [
        "search the web",
        "search online",
        "search internet",
        "search for",
        "find information",
        "look up",
        "research",
        "what is",
        "who is",
        "how does",
        "explain",
    ]

    if any(keyword in text for keyword in web_keywords):
        routes.append("web_search")

    # --------------------------------------------------
    # FILE SEARCH
    # --------------------------------------------------

    file_keywords = [
        "my files",
        "my documents",
        "document",
        "documents",
        "file",
        "files",
        "search my",
        "in my documents",
        "from my files",
    ]

    if any(keyword in text for keyword in file_keywords):
        routes.append("file_search")

    # --------------------------------------------------
    # PDF
    # --------------------------------------------------

    pdf_keywords = [
        "pdf",
        "extract pdf",
        "read pdf",
        "extract text",
        ".pdf",
    ]

    if any(keyword in text for keyword in pdf_keywords):
        routes.append("pdf")

    # --------------------------------------------------
    # FACT CHECK
    # --------------------------------------------------

    fact_keywords = [
        "fact check",
        "fact-check",
        "verify this",
        "verify the claim",
        "is this true",
        "is this claim true",
        "check whether",
        "check if this is true",
        "true or false",
    ]

    if any(keyword in text for keyword in fact_keywords):
        routes.append("fact_check")

    # --------------------------------------------------
    # RESEARCH ORGANIZER
    # --------------------------------------------------

    save_keywords = [
        "save this research",
        "save the research",
        "save this",
        "save this information",
        "store this research",
        "remember this research",
    ]

    if any(keyword in text for keyword in save_keywords):
        routes.append("research_organizer")

    # --------------------------------------------------
    # TELEGRAM
    # --------------------------------------------------

    telegram_keywords = [
        "telegram",
        "send to telegram",
        "send this to telegram",
        "message telegram",
    ]

    if any(keyword in text for keyword in telegram_keywords):
        routes.append("telegram")

    return list(dict.fromkeys(routes))


def clean_query(message: str):
    """
    Remove common routing instructions so the MCP
    receives a cleaner research query.
    """

    query = message.strip()

    query = re.sub(
        r"\b(search the web|search online|search internet)\b",
        "",
        query,
        flags=re.IGNORECASE,
    )

    query = re.sub(
        r"\b(fact check|fact-check|verify this)\b",
        "",
        query,
        flags=re.IGNORECASE,
    )

    return query.strip()
import argparse
import json
from collections.abc import Collection
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_ALLOWED_DOMAINS = frozenset({"books.toscrape.com"})
MAX_TEXT_LENGTH = 10_000
REQUEST_TIMEOUT_SECONDS = 10

CONSULTAR_PAGINA_TOOL = {
    "type": "function",
    "function": {
        "name": "consultar_pagina",
        "description": (
            "Busca uma página web permitida e retorna título e texto para análise."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "URL HTTP ou HTTPS da página.",
                }
            },
            "required": ["url"],
            "additionalProperties": False,
        },
    },
}


def consultar_pagina(
    url: str,
    allowed_domains: Collection[str] = DEFAULT_ALLOWED_DOMAINS,
) -> dict[str, str | int]:
    """Busca uma página permitida e retorna os dados em formato estruturado."""
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    if parsed_url.scheme not in {"http", "https"} or not hostname:
        raise ValueError("Informe uma URL completa usando HTTP ou HTTPS.")
    if parsed_url.username or parsed_url.password:
        raise ValueError("URLs com credenciais não são permitidas.")
    if hostname.lower() not in {domain.lower() for domain in allowed_domains}:
        raise ValueError(
            f"Domínio não permitido: {hostname}. "
            "Configure allowed_domains para autorizar este site."
        )

    response = requests.get(
        url,
        timeout=REQUEST_TIMEOUT_SECONDS,
        allow_redirects=False,
        headers={"User-Agent": "WebCrawler/1.0"},
    )
    response.raise_for_status()
    if response.is_redirect:
        raise requests.HTTPError(
            "Redirecionamentos não são seguidos pelo scraper.",
            response=response,
        )

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    text = soup.get_text(" ", strip=True)[:MAX_TEXT_LENGTH]

    return {
        "url": url,
        "status_code": response.status_code,
        "title": title,
        "text": text,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrai texto de uma página web.")
    parser.add_argument(
        "url",
        nargs="?",
        default="https://books.toscrape.com/",
        help="URL permitida (padrão: Books to Scrape).",
    )
    args = parser.parse_args()
    print(json.dumps(consultar_pagina(args.url), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

# generate_paper_notes.py
# Organiza PDFs e gera notas .md com metadados automáticos via Semantic Scholar API (2-step: search + details)

import os
import re
import time
import json
import shutil
import fitz  # PyMuPDF
import requests
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv

# === CONFIGURAÇÕES ===
BASE_DIR = Path(__file__).resolve().parent
PAPERS_DIR = BASE_DIR.parent.parent / "papers" / "papers"
OUTPUT_EXTENSION = ".md"
CACHE_FILE = BASE_DIR / "metadata_cache.json"

# === TEMPLATE ===
TEMPLATE = """### {paper_title} ({authors}, {year})

**Problem Statement:**  
The paper addresses [describe the core issue] in the context of [domain].  
This problem is relevant due to [reason].

**Objectives:**  
The authors aim to [state the main objectives or research questions].

**Proposed Solution:**  
The proposed approach involves [summarize the architecture/method/technology].  
The system integrates components such as [list briefly].

**Evaluation:**  
The work was evaluated through [type of experiment or benchmark], showing [main results and metrics].

**Key Contributions:**  
- [List the most important findings or innovations]  
- [Mention any unique aspect compared to prior work]

**Limitations and Future Work:**  
The study notes that [limitations]. Future directions include [suggested work].

**Relevance to Current Project:**  
This paper provides insights applicable to the cloud infrastructure project at DI, particularly [authentication / virtualization / orchestration / etc.].

**DOI / Link:** {doi}
"""

# === FUNÇÕES AUXILIARES ===
def load_cache():
    """Carrega cache local de metadados."""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache):
    """Guarda cache local de metadados."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)

def slugify(name: str) -> str:
    """Cria nomes de pastas legíveis."""
    name = re.sub(r"[^A-Za-z0-9À-ÿ .()-]+", "", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip().title()

def extract_title_from_pdf(pdf_path):
    """Tenta extrair o título da primeira página ou dos metadados."""
    try:
        doc = fitz.open(pdf_path)
        text = doc.load_page(0).get_text("text")
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        likely_title = ""
        for line in lines[:10]:
            if len(line) > 10 and not re.search(r"[.:;!?]", line):
                likely_title = line
                break
        if not likely_title:
            meta_title = doc.metadata.get("title", "")
            if meta_title and len(meta_title) > 5:
                likely_title = meta_title
        if not likely_title:
            likely_title = Path(pdf_path).stem.replace("_", " ")
        return likely_title.strip()
    except Exception as e:
        print(f"⚠️ Erro a ler PDF: {pdf_path.name}: {e}")
        return Path(pdf_path).stem.replace("_", " ")

# === API SEMANTIC SCHOLAR (2 REQUESTS) ===
def query_semanticscholar(title, api_key):
    """1️⃣ Pesquisa paper → obtém paperId, 2️⃣ recolhe detalhes."""
    if not title:
        return None

    headers = {
        "x-api-key": api_key,
        "User-Agent": "ThesisCloudInfra/1.0 (joao.oliveira@campus.ul.pt)"
    }

    # Limpeza e codificação do título
    clean_title = re.sub(r"[^A-Za-z0-9À-ÿ.,:;!?()\- ]+", "", title).strip()
    query_url = (
        "https://api.semanticscholar.org/graph/v1/paper/search?"
        + urllib.parse.urlencode({"query": clean_title, "limit": 1})
    )

    try:
        r = requests.get(query_url, headers=headers, timeout=15)
        if r.status_code == 429:
            print("⏳ Rate limit atingido, aguardar 2s...")
            time.sleep(2)
            return query_semanticscholar(title, api_key)
        elif r.status_code >= 400:
            print(f"⚠️ Erro {r.status_code} na pesquisa por '{title}'")
            return None

        data = r.json()
        papers = data.get("data", [])
        if not papers:
            print(f"⚠️ Nenhum resultado encontrado para '{title}'")
            return None

        paper_id = papers[0]["paperId"]
        time.sleep(1)  # respeita rate limit

        # 2️⃣ Obter detalhes do paper
        fields = "url,year,authors,title,venue,fieldsOfStudy,publicationTypes"
        detail_url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields={fields}"
        r2 = requests.get(detail_url, headers=headers, timeout=15)
        if r2.status_code == 429:
            print("⏳ Rate limit atingido, aguardar 2s...")
            time.sleep(2)
            r2 = requests.get(detail_url, headers=headers, timeout=15)
        r2.raise_for_status()

        paper = r2.json()
        authors = ", ".join(a["name"] for a in paper.get("authors", [])) or "[Unknown]"

        print(f"✅ Encontrado: {paper.get('title', title)} ({paper.get('year', 'N/A')})")

        return {
            "title": paper.get("title", title),
            "authors": authors,
            "year": paper.get("year", "[Unknown]"),
            "venue": paper.get("venue", "[Unknown]"),
            "doi": f"https://doi.org/{paper['doi']}" if paper.get("doi") else "[None]",
            "url": paper.get("url", "[None]"),
        }

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erro ao contactar Semantic Scholar: {e}")
        return None

# === FUNÇÃO PRINCIPAL ===
def organize_papers():
    load_dotenv()
    api_key = os.getenv("API_KEY")

    if not api_key:
        print("❌ API key não encontrada. Cria um ficheiro .env com API_KEY=<a_tua_key>")
        return

    if not PAPERS_DIR.exists():
        raise FileNotFoundError(f"Pasta de papers não encontrada: {PAPERS_DIR.resolve()}")

    pdfs = list(PAPERS_DIR.rglob("*.pdf"))
    if not pdfs:
        print(f"⚠️ Nenhum PDF encontrado em: {PAPERS_DIR.resolve()}")
        return

    cache = load_cache()

    for pdf in pdfs:
        folder_name = slugify(pdf.stem)
        paper_dir = PAPERS_DIR / folder_name
        paper_dir.mkdir(exist_ok=True)

        new_pdf_path = paper_dir / pdf.name
        if pdf.resolve() != new_pdf_path.resolve():
            try:
                shutil.move(str(pdf), new_pdf_path)
                print(f"📂 Moveu: {pdf.name} → {paper_dir.name}/")
            except shutil.Error:
                print(f"⚠️ {pdf.name} já existe em {paper_dir.name}/")

        # Extrai título e consulta API
        extracted_title = extract_title_from_pdf(new_pdf_path)
        if extracted_title in cache:
            meta = cache[extracted_title]
            print(f"🧠 Cache: usando metadados de '{extracted_title}'")
        else:
            meta = query_semanticscholar(extracted_title, api_key)
            if meta:
                cache[extracted_title] = meta
                save_cache(cache)
            time.sleep(1)

        if meta:
            paper_title = meta["title"]
            authors = meta["authors"]
            year = meta["year"]
            doi = meta["doi"]
        else:
            paper_title = extracted_title
            authors = "[Unknown]"
            year = "[Unknown]"
            doi = "[None]"

        # Cria ficheiro .md
        notes_path = paper_dir / f"{folder_name}{OUTPUT_EXTENSION}"
        if not notes_path.exists():
            content = TEMPLATE.format(
                paper_title=paper_title,
                authors=authors,
                year=year,
                doi=doi,
            )
            notes_path.write_text(content, encoding="utf-8")
            print(f"✅ Criado: {notes_path.name} em {paper_dir.name}/")
        else:
            print(f"ℹ️ Já existe: {notes_path.name}, não foi recriado.")

    print("\n🎉 Organização e extração de metadados concluída com sucesso!")

# === EXECUÇÃO ===
if __name__ == "__main__":
    organize_papers()

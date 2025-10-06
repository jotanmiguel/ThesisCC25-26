# generate_paper_notes.py
# Organiza PDFs e gera notas .md com metadados automáticos via Semantic Scholar API (REST)

import os
import re
import time
import shutil
import fitz  # PyMuPDF
import requests
import urllib.parse
from pathlib import Path

# === CONFIGURAÇÕES ===
BASE_DIR = Path(__file__).resolve().parent
PAPERS_DIR = BASE_DIR.parent.parent / "papers" / "papers"
OUTPUT_EXTENSION = ".md"

# === TEMPLATE DO FICHEIRO ===
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

# === CONSULTA À API SEMANTIC SCHOLAR (REST) ===
def query_semanticscholar(title):
    """Pesquisa título no Semantic Scholar e devolve metadados."""
    if not title:
        return None
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": title,
        "limit": 1,
        "fields": "title,authors,year,venue,doi,abstract"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        items = data.get("data", [])
        if not items:
            print(f"⚠️ Nenhum resultado encontrado para: '{title}'")
            return None

        item = items[0]
        authors = ", ".join(a["name"] for a in item.get("authors", [])) or "[Unknown]"
        return {
            "title": item.get("title", title),
            "authors": authors,
            "year": item.get("year", "[Unknown]"),
            "venue": item.get("venue", "[Unknown]"),
            "doi": f"https://doi.org/{item['doi']}" if item.get("doi") else "[None]",
        }
    except Exception as e:
        print(f"⚠️ Erro ao contactar Semantic Scholar: {e}")
        return None

# === FUNÇÃO PRINCIPAL ===
def organize_papers():
    if not PAPERS_DIR.exists():
        raise FileNotFoundError(f"Pasta de papers não encontrada: {PAPERS_DIR.resolve()}")

    pdfs = list(PAPERS_DIR.rglob("*.pdf"))
    if not pdfs:
        print(f"⚠️ Nenhum PDF encontrado em: {PAPERS_DIR.resolve()}")
        return

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

        # Extrai título e recolhe metadados
        extracted_title = extract_title_from_pdf(new_pdf_path)
        meta = query_semanticscholar(extracted_title)

        if meta:
            paper_title = meta["title"]
            authors = meta["authors"]
            year = meta["year"]
            doi = meta["doi"]
        else:
            paper_title = extracted_title or pdf.stem.replace("_", " ").title()
            authors = "[Unknown]"
            year = "[Unknown]"
            doi = "[None]"

        # Cria ficheiro de notas
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

        # 1 request/segundo para respeitar limite
        time.sleep(1.1)

    print("\n🎉 Organização e extração de metadados concluída com sucesso!")

# === EXECUÇÃO ===
if __name__ == "__main__":
    organize_papers()

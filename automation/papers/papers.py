# organize_papers_only.py
# Move PDFs para pastas organizadas, sem chamar a API (modo offline)

import os
import re
import shutil
from pathlib import Path

# === CONFIGURAÇÕES ===
BASE_DIR = Path(__file__).resolve().parent
PAPERS_DIR = BASE_DIR.parent.parent / "papers" / "papers"

# === FUNÇÕES AUXILIARES ===
def slugify(name: str) -> str:
    """Cria nomes de pastas legíveis, sem underscores nem caracteres estranhos."""
    name = re.sub(r"[^A-Za-z0-9À-ÿ .()-]+", "", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip().title()

# === FUNÇÃO PRINCIPAL ===
def organize_papers():
    if not PAPERS_DIR.exists():
        raise FileNotFoundError(f"Pasta de papers não encontrada: {PAPERS_DIR.resolve()}")

    pdfs = list(PAPERS_DIR.glob("*.pdf"))  # só PDFs no nível direto
    if not pdfs:
        print(f"⚠️ Nenhum PDF encontrado em: {PAPERS_DIR.resolve()}")
        return

    for pdf in pdfs:
        folder_name = slugify(pdf.stem)
        paper_dir = PAPERS_DIR / folder_name

        # se a pasta já existir, saltar
        if paper_dir.exists():
            print(f"ℹ️ Pasta '{folder_name}' já existe — a saltar.")
            continue

        # criar pasta e mover ficheiro
        paper_dir.mkdir(exist_ok=True)
        new_pdf_path = paper_dir / pdf.name

        try:
            shutil.move(str(pdf), new_pdf_path)
            print(f"📂 Moveu: {pdf.name} → {paper_dir.name}/")
        except Exception as e:
            print(f"⚠️ Erro ao mover '{pdf.name}': {e}")

    print("\n✅ Organização concluída (modo offline, sem chamadas à API).")

# === EXECUÇÃO ===
if __name__ == "__main__":
    organize_papers()
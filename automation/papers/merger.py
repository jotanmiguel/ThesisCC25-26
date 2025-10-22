import os
import argparse
from PyPDF2 import PdfMerger

def merge_pdfs_in_subfolders(root_folder, output_folder, output_filename):
    merger = PdfMerger()

    # Caminha por todas as subpastas e arquivos
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in sorted(filenames):
            if filename.lower().endswith(".pdf"):
                filepath = os.path.join(dirpath, filename)
                print(f"Adicionando: {filepath}")
                merger.append(filepath)

    # Cria a pasta de saída, se não existir
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, output_filename)
    merger.write(output_path)
    merger.close()

    print(f"\n✅ PDF combinado criado em: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Compila todos os PDFs em subpastas dentro de um único arquivo PDF."
    )
    parser.add_argument(
        "-r", "--root",
        default="C:\Users\joaom\Desktop\Faculdade\Mestrado\ThesisCC25-26\papers\papers",
        help="Caminho da pasta raiz onde estão os PDFs."
    )
    parser.add_argument(
        "-o", "--output-folder",
        default="C:\Users\joaom\Desktop\Faculdade\Mestrado\ThesisCC25-26\papers\papers",
        help="Pasta onde o PDF final será salvo (padrão: pasta atual)."
    )
    parser.add_argument(
        "-n", "--name",
        default="merged.pdf",
        help="Nome do arquivo PDF final (padrão: merged.pdf)."
    )

    args = parser.parse_args()
    merge_pdfs_in_subfolders(args.root, args.output_folder, args.name)


if __name__ == "__main__":
    main()

import os
from pypdf import PdfReader, PdfWriter

BASE_DIR = r"C:/Users/SEU_NOME_USUARIO/Documents/Contracheques"

def unir_pdfs_do_ano(pasta_ano):
    writer = PdfWriter()

    arquivos = [
        f for f in os.listdir(pasta_ano)
        if f.lower().endswith(".pdf")
    ]

    # ordena pelo mês (01, 02, ..., 12)
    arquivos.sort(key=lambda x: int(x.split(".")[0]))

    for pdf in arquivos:
        caminho = os.path.join(pasta_ano, pdf)
        reader = PdfReader(caminho)

        for pagina in reader.pages:
            writer.add_page(pagina)

    ano = os.path.basename(pasta_ano)
    saida = os.path.join(BASE_DIR, f"Contracheques_{ano}.pdf")

    with open(saida, "wb") as f:
        writer.write(f)

    print(f" Gerado: {saida}")


# =============================
# EXECUÇÃO
# =============================
for nome in os.listdir(BASE_DIR):
    pasta_ano = os.path.join(BASE_DIR, nome)

    if not os.path.isdir(pasta_ano):
        continue

    if not nome.isdigit():
        continue

    unir_pdfs_do_ano(pasta_ano)

print(" Finalizado!")

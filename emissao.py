import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import shutil

# =============================
# CONFIGURAÇÕES
# =============================
BASE_DIR = r"C:/Users/SEU_NOME_USUARIO/Documents/Contracheques"
URL = "https://portaldoservidor.ma.gov.br/portal/#/servidor/contracheque"
DOWNLOADS_DIR = r"C:/Users/SEU_NOME_USUARIO/Downloads"

MESES = [
    ("01", "Jan"),
    ("02", "Fev"),
    ("03", "Mar"),
    ("04", "Abr"),
    ("05", "Mai"),
    ("06", "Jun"),
    ("07", "Jul"),
    ("08", "Ago"),
    ("09", "Set"),
    ("10", "Out"),
    ("11", "Nov"),
    ("12", "Dez"),
]

def esperar_download_pdf(inicio, timeout=60):
    """
    Espera um PDF ser baixado APÓS o momento 'inicio'
    e retorna o caminho do arquivo.
    """
    while time.time() - inicio < timeout:
        for nome in os.listdir(DOWNLOADS_DIR):
            if not nome.lower().endswith(".pdf"):
                continue

            caminho = os.path.join(DOWNLOADS_DIR, nome)

            # ignora arquivos antigos
            if os.path.getctime(caminho) < inicio:
                continue

            # ignora downloads incompletos
            if nome.lower().endswith(".crdownload"):
                continue

            return caminho

        time.sleep(0.5)

    raise TimeoutError("PDF não foi baixado dentro do tempo esperado.")


# =============================
# CHROME
# =============================
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
})

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 9999)

driver.get(URL)

print(" Faça login manualmente.")
print(" Depois clique em: Menu do Contracheque.")
print(" O script só continua quando a tela REAL carregar.")

# =============================
# ESPERA PELA TELA DE CONTRACHEQUE
# =============================

# espera os DOIS selects aparecerem
wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "//select")
    )
)

print(" Tela de contracheque detectada.")

# =============================
# LOOP
# =============================
for ano in range(2025, 2026):
    pasta_ano = os.path.join(BASE_DIR, str(ano))
    os.makedirs(pasta_ano, exist_ok=True)

    for mes_valor, mes_abrev in MESES:
        print(f" Emitindo {mes_abrev}.{ano}")
        
        time.sleep(0.5)

        # Captura dinâmica dos selects
        selects = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//select"))
        )
        
        select_ano = Select(selects[0])
        select_mes = Select(selects[1])

        # Seleciona o ano
        select_ano.select_by_value(str(ano))

        # Aguarda o Angular carregar os meses
        wait.until(
            lambda d: len(Select(
                d.find_elements(By.XPATH, "//select")[1]
            ).options) > 1
        )

        # Rebusca o select de mês (Angular recria o elemento)
        selects = driver.find_elements(By.XPATH, "//select")
        select_mes = Select(selects[1])

        # Seleciona o mês
        select_mes.select_by_value(mes_valor)


        # botão imprimir
        btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Imprimir')]")
            )
        )
        
        # MARCA O MOMENTO DO CLIQUE
        inicio_download = time.time()

        btn.click()

        # espera somente o PDF GERADO AGORA
        pdf_baixado = esperar_download_pdf(inicio_download)

        # destino final
        nome_final = f"{mes_valor}.{ano}.pdf"
        destino = os.path.join(pasta_ano, nome_final)

        # move e renomeia
        shutil.move(pdf_baixado, destino)

        print(f" Salvo: {destino}")
        time.sleep(1)
        
print(" Finalizado com sucesso!")
driver.quit() 

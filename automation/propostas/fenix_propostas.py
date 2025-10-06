from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import unicodedata
import time
import json

driver = webdriver.Firefox()
driver.get("https://fenix.ciencias.ulisboa.pt")

print("🔐 Faz login no Fénix e entra na página das propostas.")
print("➡️ Pressiona ENTER para capturar propostas visíveis.")
print("❌ Escreve 'q' + ENTER para sair e guardar.\n")

propostas_completas = {}  # agora é dict, com o título como key
capturados_set = set()

def limpar(texto):
    return texto.replace("\xa0", " ").replace("\r", "").strip()

def normalize(texto):
    texto = texto.lower().strip()
    texto = ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))
    return texto

while True:
    start = time.time()
    cmd = input("📸 ENTER para capturar propostas visíveis, ou 'q' para sair: ")
    if cmd.strip().lower() == "q":
        stop = time.time()
        print(f"⏱️ Tempo total: {stop - start:.2f}")
        break

    time.sleep(0.3)

    botoes = []
    candidatos = driver.find_elements(By.CSS_SELECTOR, "div.v-button.v-button-link")
    for botao in candidatos:
        try:
            legenda = botao.find_element(By.CLASS_NAME, "v-button-caption")
            if legenda.text.strip():
                botoes.append(botao)
        except:
            continue

    for botao in botoes:
        try:
            title = botao.text.strip()
            if not title or title in capturados_set:
                continue

            print(f"➡️ A capturar: {title[:60]}")
            driver.execute_script("arguments[0].click();", botao)

            WebDriverWait(driver, 0.8).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.v-window"))
            )
            time.sleep(0.4)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            campos = soup.select("div.v-label pre")
            textos = [limpar(pre.get_text()) for pre in campos]

            # Extrair pares consecutivos: label -> valor
            proposta_info = {}
            ignorar = False
            i = 0
            while i < len(textos) - 1:
                label = textos[i]
                valor = textos[i + 1]

                if label.lower() == "aluno pré-selecionado" and normalize(valor) == "sim":
                    print(f"⛔ Ignorada (pré-selecionado): {title[:60]}")
                    ignorar = True
                    break

                proposta_info[label] = valor
                i += 2  # avançar de 2 em 2 (label → valor)

            try:
                close_button = WebDriverWait(driver, 0.8).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.v-window-closebox"))
                )
                driver.execute_script("arguments[0].click();", close_button)
            except:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

            time.sleep(0.2)

            if ignorar:
                continue

            propostas_completas[title] = proposta_info
            capturados_set.add(title)
            print(f"✅ Capturada com sucesso: {title[:60]}")

        except Exception as e:
            print(f"⚠️ Erro ao capturar: {e}")
            try:
                driver.find_element(By.CSS_SELECTOR, "button.v-window-closebox").click()
                time.sleep(1)
            except:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(1)
            continue

# Guardar como JSON com títulos como keys
with open("propostas_fenix.json", "w", encoding="utf-8") as f:
    json.dump(propostas_completas, f, ensure_ascii=False, indent=2)

print(f"\n📦 {len(propostas_completas)} propostas exportadas para 'propostas_fenix.json'")
driver.quit()

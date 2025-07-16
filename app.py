import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

# Função para extrair eventos de alto impacto do Forex Factory
def obter_eventos_fundamentalistas():
    url = "https://www.forexfactory.com/calendar"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr", class_="calendar__row")

    eventos_hoje = []

    for row in rows:
        impacto = row.find("td", class_="calendar__impact")
        if impacto and "high" in impacto.get("class", []):  # Apenas impacto alto
            moeda = row.find("td", class_="calendar__currency").text.strip()
            if moeda != "USD":
                continue

            hora = row.find("td", class_="calendar__time").text.strip()
            evento = row.find("td", class_="calendar__event").text.strip()
            atual = row.find("td", class_="calendar__actual").text.strip()
            esperado = row.find("td", class_="calendar__forecast").text.strip()

            if atual == "" or esperado == "":
                continue

            eventos_hoje.append({
                "hora": hora,
                "evento": evento,
                "esperado": esperado,
                "real": atual,
            })

    return eventos_hoje

# Análise simples: se real > esperado, USD forte; se real < esperado, USD fraco
def analisar_sinal(evento):
    try:
        real = float(evento["real"].replace("%", "").replace(",", ""))
        esperado = float(evento["esperado"].replace("%", "").replace(",", ""))
        diferenca = real - esperado

        if abs(diferenca) < 0.2:
            direcao = "Neutro – Sem sinal claro"
            acao = "Aguardar confirmação no H1"
        elif diferenca > 0:
            direcao = "USD Forte – Comprar USD"
            acao = "Ex: Vender EUR/USD (Entrada no M15 após pullback)"
        else:
            direcao = "USD Fraco – Vender USD"
            acao = "Ex: Comprar EUR/USD (Entrada no M15 após pullback)"

        return direcao, acao
    except:
        return "Dados insuficientes", "Aguardar nova leitura"

# Interface Streamlit
st.set_page_config(page_title="Sinais Forex USD", layout="centered")
st.title("📊 Sinais Fundamentalistas – USD (Tempo Real)")
st.markdown("Filtrando eventos de **alto impacto** envolvendo USD")

# Zona horária (opcional)
fuso = pytz.timezone("America/Sao_Paulo")
agora = datetime.now(fuso).strftime("%d/%m/%Y %H:%M")
st.caption(f"📅 Atualizado em: {agora}")

eventos = obter_eventos_fundamentalistas()

if not eventos:
    st.warning("Nenhum evento de alto impacto com USD encontrado para hoje.")
else:
    for ev in eventos:
        direcao, acao = analisar_sinal(ev)
        with st.container():
            st.subheader(f"🕒 {ev['hora']} – {ev['evento']}")
            st.write(f"**Esperado:** {ev['esperado']} | **Real:** {ev['real']}")
            st.write(f"📈 **Sinal:** {direcao}")
            st.write(f"🕵️‍♂️ **Tempo gráfico sugerido:** {acao}")
            st.markdown("---")

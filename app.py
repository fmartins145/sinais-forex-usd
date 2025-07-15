import streamlit as st

st.set_page_config(page_title="Sinais Fundamentais - USD")
st.title("📊 Sinais Fundamentais - USD")

st.markdown("Ferramenta para gerar sinais com base em eventos econômicos dos EUA.")

eventos = [
    {"hora": "09:30", "evento": "Inflação (CPI)", "esperado": 3.1, "real": 3.4},
    {"hora": "11:00", "evento": "Taxa de juros (Fed)", "esperado": 5.25, "real": 5.25},
    {"hora": "15:00", "evento": "PMI de Serviços", "esperado": 52.5, "real": 49.8},
]

for ev in eventos:
    st.subheader(f"{ev['hora']} - {ev['evento']}")
    st.write(f"Esperado: {ev['esperado']} | Real: {ev['real']}")

    if ev["real"] > ev["esperado"]:
        st.success("📈 USD Forte - Comprar USD")
    elif ev["real"] < ev["esperado"]:
        st.error("📉 USD Fraco - Vender USD")
    else:
        st.info("➖ Neutro - Sem direção clara")

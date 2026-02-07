import streamlit as st
import requests
import uuid
import os
import time

st.set_page_config(page_title="Agent Empty - Debugger", page_icon="🕵️", layout="wide")

API_URL = os.getenv("API_URL", "http://localhost:8000")
DATA_DIR = "data/raw"  # Caminho local para checar arquivos

st.title("🕵️ Agent RAG Debugger")

# --- SIDEBAR: Gerenciamento e Status ---
with st.sidebar:
    st.header("🎮 Controle")
    
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    
    thread_id = st.text_input("Thread ID (Sessão)", value=st.session_state.thread_id)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset ID"):
            st.session_state.thread_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🗑️ Limpar Chat"):
            st.session_state.messages = []
            st.rerun()

    st.divider()
    
    # Lista de Arquivos Ingeridos (Visualização)
    st.header("📂 Base de Conhecimento")
    try:
        files = os.listdir(DATA_DIR)
        if files:
            for f in files:
                st.caption(f"📄 {f}")
        else:
            st.warning("Nenhum arquivo em data/raw")
    except FileNotFoundError:
        st.error(f"Pasta {DATA_DIR} não encontrada")

# --- CHAT PRINCIPAL ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Renderizar mensagens anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Se tiver fontes salvas no histórico, mostra também
        if "sources" in msg and msg["sources"]:
            with st.expander("📚 Contexto Recuperado (RAG)"):
                for idx, source in enumerate(msg["sources"]):
                    st.text(f"--- Trecho {idx+1} ---")
                    st.caption(source)

# Input do Usuário
if prompt := st.chat_input("Pergunte algo aos seus dados..."):
    # 1. Usuário
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Resposta do Bot
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⏳ *Consultando base de vetores...*")
        
        start_time = time.time()
        try:
            payload = {"message": prompt, "thread_id": st.session_state.thread_id}
            response = requests.post(f"{API_URL}/chat", json=payload)
            end_time = time.time()
            latency = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("response", "")
                sources = data.get("sources", [])
                
                # Exibe resposta final
                placeholder.markdown(content)
                
                # Exibe Contexto de RAG (Se houver)
                if sources:
                    with st.expander(f"📚 Contexto Recuperado ({len(sources)} trechos) - {latency:.2f}s"):
                        for idx, source in enumerate(sources):
                            st.markdown(f"**Trecho {idx+1}:**")
                            st.info(source)
                else:
                    st.caption(f"⏱️ Resposta gerada em {latency:.2f}s (Sem uso de ferramentas)")

                # Salva no histórico com as fontes
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": content,
                    "sources": sources
                })
                
            else:
                placeholder.error(f"Erro {response.status_code}: {response.text}")
        
        except Exception as e:
            placeholder.error(f"Erro de conexão: {e}")
import json
import pandas as pd
import asyncio
import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from app.agent.graph import create_graph # Importa o agente
from langchain_core.messages import HumanMessage
from app.core.config import settings

# Configuração do Juiz
JUDGE_MODEL = "deepseek-r1:8b" 

async def run_evaluation():
    print(f"⚖️  Iniciando Sessão do LLM Judge ({JUDGE_MODEL})...")
    
    # 1. Carregar Dataset
    dataset_path = "data/datasets/golden_dataset.jsonl"
    try:
        with open(dataset_path, "r", encoding="utf-8") as f:
            records = [json.loads(line) for line in f]
    except FileNotFoundError:
        print("❌ Dataset não encontrado. Crie o arquivo data/datasets/golden_dataset.jsonl")
        return

    # 2. Inicializar Agente e Juiz
    # O agente usa o modelo definido em settings (ex: llama3.1:8b)
    # O juiz usa o modelo definido acima (deepseek-r1:8b)
    
    print("🔹 Inicializando Agente...")
    agent = create_graph()
    
    print(f"🔹 Inicializando Juiz ({JUDGE_MODEL})...")
    judge_llm = ChatOllama(model=JUDGE_MODEL, temperature=0)
    
    results = []

    # 3. Prompt de Avaliação (O Crivo do Juiz)
    eval_prompt = ChatPromptTemplate.from_template("""
    Você é um professor rigoroso avaliando uma prova técnica.
    
    Pergunta: {question}
    Resposta Esperada (Gabarito): {ground_truth}
    Resposta do Aluno (Agente): {agent_answer}
    
    Avalie a resposta do aluno de 1 a 5, onde:
    1 = Completamente errada ou alucinação.
    2 = Errada, mas com algum conceito próximo.
    3 = Parcialmente correta, perdeu detalhes importantes.
    4 = Correta, mas com pequenos desvios de terminologia.
    5 = Correta e completa (pode usar palavras diferentes, mas o sentido deve ser o mesmo).

    IMPORTANTE: Se a resposta esperada for "Eu não sei" e o aluno inventar algo, dê nota 1.
    Se a resposta esperada for "Eu não sei" e o aluno disser que não sabe, dê nota 5.
    
    Responda APENAS no formato JSON, sem crases ou markdown:
    {{
        "score": <numero>,
        "reasoning": "<explicação breve>"
    }}
    """)

    # 4. Loop de Teste
    print(f"\n🚀 Iniciando avaliação de {len(records)} questões...\n")
    
    for i, record in enumerate(records):
        print(f"🔹 Avaliando {i+1}/{len(records)}: {record['question']}")
        
        # A. Obter resposta do Agente
        try:
            inputs = {"messages": [HumanMessage(content=record["question"])]}
            response = await agent.ainvoke(inputs)
            agent_answer = response["messages"][-1].content
        except Exception as e:
            print(f"❌ Erro ao invocar agente: {e}")
            agent_answer = "ERRO: Falha ao gerar resposta."
        
        # B. Julgar
        eval_chain = eval_prompt | judge_llm
        try:
            eval_result_str = eval_chain.invoke({
                "question": record["question"],
                "ground_truth": record["ground_truth"],
                "agent_answer": agent_answer
            })
            
            # Limpeza básica caso o LLM mande markdown ou thought process (comum no deepseek-r1)
            content = eval_result_str.content
            
            # Remover tags <think> se existirem (específico deepseek-r1)
            if "<think>" in content:
                content = content.split("</think>")[-1]
            
            content = content.replace("```json", "").replace("```", "").strip()
            
            # Tentar parsear JSON
            try:
                eval_json = json.loads(content)
            except json.JSONDecodeError:
                # Fallback simples se o JSON falhar
                print(f"⚠️ JSON inválido do juiz. Conteúdo bruto: {content[:100]}...")
                eval_json = {"score": 0, "reasoning": "Erro no parser do Juiz (JSON inválido)"}
                
        except Exception as e:
            print(f"⚠️ Erro ao julgar: {e}")
            eval_json = {"score": 0, "reasoning": "Erro na execução do Juiz"}

        # C. Salvar Resultado
        results.append({
            "question": record["question"],
            "ground_truth": record["ground_truth"],
            "agent_answer": agent_answer,
            "score": eval_json.get("score", 0),
            "reasoning": eval_json.get("reasoning", "N/A")
        })

    # 5. Gerar Relatório
    if not results:
        print("❌ Nenhum resultado gerado.")
        return

    df = pd.DataFrame(results)
    
    print("\n📊 Relatório Final:")
    print(df[["question", "score", "reasoning"]])
    
    output_csv = "data/datasets/evaluation_report.csv"
    output_md = "data/datasets/evaluation_report.md"
    
    df.to_csv(output_csv, index=False)
    
    # Gerar Markdown também para facilitar leitura
    with open(output_md, "w", encoding="utf-8") as f:
        f.write("# Relatório de Avaliação do Agente\n\n")
        f.write(f"**Data:** {pd.Timestamp.now()}\n")
        f.write(f"**Modelo Juiz:** {JUDGE_MODEL}\n")
        f.write(f"**Média de Precisão:** {df['score'].mean():.2f} / 5.0\n\n")
        f.write("## Detalhes\n\n")
        f.write(df.to_markdown(index=False))
        
    print(f"\n✅ Relatório CSV salvo em: {output_csv}")
    print(f"✅ Relatório MD salvo em: {output_md}")
    print(f"⭐ Média de Precisão: {df['score'].mean():.2f} / 5.0")

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_evaluation())
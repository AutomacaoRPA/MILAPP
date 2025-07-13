"""
Dashboards Executivos do MILAPP - Streamlit
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json
from typing import Dict, List, Any
import os
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="MILAPP - Dashboards Executivos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurações
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Cache para dados
@st.cache_data(ttl=300)
def fetch_data(endpoint: str) -> Dict[str, Any]:
    """Busca dados da API com cache"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/{endpoint}")
        return response.json()
    except Exception as e:
        st.error(f"Erro ao buscar dados: {str(e)}")
        return {}

@st.cache_data(ttl=300)
def fetch_projects() -> List[Dict[str, Any]]:
    """Busca projetos"""
    return fetch_data("projects") or []

@st.cache_data(ttl=300)
def fetch_conversations() -> List[Dict[str, Any]]:
    """Busca conversações"""
    return fetch_data("conversations") or []

def main():
    """Função principal do dashboard"""
    
    # Header
    st.title("📊 MILAPP - Dashboards Executivos")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Filtros")
        
        # Filtro de período
        st.subheader("Período")
        date_range = st.date_input(
            "Selecione o período",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            max_value=datetime.now()
        )
        
        # Filtro de status
        st.subheader("Status")
        status_filter = st.multiselect(
            "Status dos projetos",
            ["planning", "development", "testing", "deployed", "completed"],
            default=["development", "testing", "deployed"]
        )
        
        # Filtro de metodologia
        st.subheader("Metodologia")
        methodology_filter = st.multiselect(
            "Metodologia",
            ["scrum", "kanban", "hybrid"],
            default=["scrum", "kanban"]
        )
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Projetos Ativos",
            value=len([p for p in fetch_projects() if p.get("status") in ["development", "testing"]]),
            delta=5
        )
    
    with col2:
        st.metric(
            label="Conversações IA",
            value=len(fetch_conversations()),
            delta=12
        )
    
    with col3:
        total_hours = sum(p.get("estimated_hours", 0) for p in fetch_projects())
        st.metric(
            label="Horas Estimadas",
            value=f"{total_hours:,}",
            delta="+15%"
        )
    
    with col4:
        completed_projects = len([p for p in fetch_projects() if p.get("status") == "completed"])
        st.metric(
            label="Projetos Concluídos",
            value=completed_projects,
            delta=3
        )
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Status dos Projetos")
        projects_data = fetch_projects()
        if projects_data:
            status_counts = pd.DataFrame(projects_data).groupby("status").size().reset_index(name="count")
            fig = px.pie(
                status_counts,
                values="count",
                names="status",
                title="Distribuição por Status"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⏱️ Velocidade de Desenvolvimento")
        # Dados simulados para velocidade
        velocity_data = {
            "Sprint": [f"Sprint {i}" for i in range(1, 11)],
            "Story Points": [15, 18, 22, 19, 25, 21, 24, 27, 23, 26]
        }
        df_velocity = pd.DataFrame(velocity_data)
        fig = px.line(
            df_velocity,
            x="Sprint",
            y="Story Points",
            title="Velocidade por Sprint"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela de projetos
    st.subheader("📋 Projetos Recentes")
    
    if projects_data:
        df_projects = pd.DataFrame(projects_data)
        df_projects["created_at"] = pd.to_datetime(df_projects["created_at"])
        df_projects = df_projects.sort_values("created_at", ascending=False)
        
        # Filtros aplicados
        if status_filter:
            df_projects = df_projects[df_projects["status"].isin(status_filter)]
        if methodology_filter:
            df_projects = df_projects[df_projects["methodology"].isin(methodology_filter)]
        
        # Formatação da tabela
        display_columns = {
            "name": "Nome",
            "status": "Status",
            "methodology": "Metodologia",
            "estimated_hours": "Horas Estimadas",
            "quality_score": "Qualidade",
            "risk_level": "Risco",
            "created_at": "Criado em"
        }
        
        df_display = df_projects[display_columns.keys()].rename(columns=display_columns)
        df_display["Criado em"] = df_display["Criado em"].dt.strftime("%d/%m/%Y")
        
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )
    
    # Análise de IA
    st.subheader("🤖 Análise de IA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tipos de Arquivos Processados")
        # Dados simulados
        file_types = ["PDF", "Imagem", "Áudio", "BPMN", "Excel", "Word"]
        file_counts = [45, 32, 18, 12, 28, 15]
        
        fig = px.bar(
            x=file_types,
            y=file_counts,
            title="Arquivos Processados por Tipo"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Confiança da IA")
        # Dados simulados
        confidence_data = {
            "Baixa (< 50%)": 5,
            "Média (50-80%)": 25,
            "Alta (> 80%)": 70
        }
        
        fig = px.pie(
            values=list(confidence_data.values()),
            names=list(confidence_data.keys()),
            title="Distribuição de Confiança da IA"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # KPIs de Negócio
    st.subheader("💰 KPIs de Negócio")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="ROI Médio",
            value="320%",
            delta="+45%"
        )
    
    with col2:
        st.metric(
            label="Tempo Médio de Desenvolvimento",
            value="12.5 dias",
            delta="-2.3 dias"
        )
    
    with col3:
        st.metric(
            label="Taxa de Sucesso",
            value="94.2%",
            delta="+3.1%"
        )
    
    # Gráfico de tendências
    st.subheader("📊 Tendências")
    
    # Dados simulados para tendências
    dates = pd.date_range(start=datetime.now() - timedelta(days=90), end=datetime.now(), freq="D")
    trend_data = {
        "Data": dates,
        "Projetos Ativos": [10 + i * 0.1 + np.random.normal(0, 0.5) for i in range(len(dates))],
        "Conversações IA": [5 + i * 0.05 + np.random.normal(0, 0.3) for i in range(len(dates))],
        "Horas Economizadas": [100 + i * 2 + np.random.normal(0, 5) for i in range(len(dates))]
    }
    
    df_trends = pd.DataFrame(trend_data)
    
    fig = go.Figure()
    
    for col in ["Projetos Ativos", "Conversações IA", "Horas Economizadas"]:
        fig.add_trace(
            go.Scatter(
                x=df_trends["Data"],
                y=df_trends[col],
                mode="lines",
                name=col
            )
        )
    
    fig.update_layout(
        title="Tendências dos Últimos 90 Dias",
        xaxis_title="Data",
        yaxis_title="Valor"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>MILAPP v2.0.0 - Sistema Integrado de Gestão RPA e Inovação</p>
            <p>Desenvolvido para MedSênior</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
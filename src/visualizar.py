import streamlit as st
import pandas as pd
import os
import json
import numpy as np
import plotly.express as px
import random
from streamlit_extras.dataframe_explorer import dataframe_explorer

src_dir = os.path.dirname(os.path.abspath(__file__))
categorizado = pd.read_json(os.path.join(src_dir, "..", "data", "categorizado.json"))
categorizado.set_index('uid', inplace=True)

with open(os.path.join(src_dir, '..', 'metadados.json'), 'r') as file:
    metadados = json.loads(file.read())
edicoes_nomes = list(reversed(list(map(lambda edicao: { 'nome': edicao['nome'], 'nome_alt': edicao['nome_alt'] }, metadados))))
cpbr_edicoes_ordem_cronologica = [item['nome'] for item in edicoes_nomes]
cpbr_edicoes_ordem_cronologica_nomes = [item['nome_alt'] for item in edicoes_nomes]

colors = random.sample(["#cedc00", "#e10098", "#00bfff", "#ff4500", "#4e008e", "#00c000", "#a71d1d", "#1e90ff", "#d2691e", "#a020f0", "#32cd32", "#ff007f", "#6495ed", "#483d8b", "#a0522d", "#ffdb58", "#2323FF", "#00ced1", "#b8860b", "#6b8e23"], 20)
page_title = 'Análise da programação das últimas 10 edições da Campus Party Brasil'

st.set_page_config(page_title='cpbr-programacao-analise', page_icon='📊', initial_sidebar_state='expanded')

st.sidebar.subheader('Menu')
st.sidebar.markdown("[Início](#inicio)")
st.sidebar.markdown("[Eixos das atividades](#eixos)")
st.sidebar.markdown("[Formatos das atividades](#formatos)")
st.sidebar.markdown("[Objetivos das atividades](#objetivos)")
st.sidebar.markdown("[Perfis dos organizador(es)](#perfis)")
st.sidebar.markdown("[Visão geral](#visao_geral)")
st.sidebar.markdown("[GitHub :material/call_made:](https://github.com/gusalbukrk/cpbr-programacao-analise)")

# global CSS styles
st.markdown("""
    <style>
        .stMainBlockContainer {
            max-width: 800px;
        }

        .stSidebar h3 {
            margin-bottom: .75rem;
        }

        .stSidebar a {
            text-decoration: none;
            color: #ca6cf9
        }

        .stSidebar .stElementContainer:last-of-type {
            margin-top: 1rem !important;
        }

        .stSidebar .stElementContainer:last-of-type a, #projeto-descricao a {
            text-decoration: none;
            color: #62b4cf;    
        }

        h1 {
            margin-bottom: 2rem !important;
            text-align: justify;
        }

        #projeto-descricao {
            text-align: justify;    
        }

        .stSelectbox {
            margin-bottom: 2rem;
        }

        div[data-baseweb="tab-border"] {
            # display: none;
        }

        .stSelectbox p {
            margin-bottom: .5rem;
        }

        h2 {
            margin-bottom: 1rem !important;
        }

        h2:not(#eixos) {
            margin-top: 2rem !important;
        }

        .atividades_total {
            font-size: 1rem;
        }

        .stElementContainer .sep {
            height: 1px;
            background: repeating-linear-gradient(90deg,rgba(250, 250, 250, 0.1) 0 5px,#0000 0 5px)
        }
    </style>
""", unsafe_allow_html=True)

# para uma dada categoria, calcula a frequência de cada rotulo e sua proporção percentual dentro daquela categoria
def calcular_rotulos(atividades, categoria):
    if (categoria == 'eixo'):
        total = (atividades_edicao_selecionada['eixo'].explode().value_counts(dropna=False))
        porcentagem = pd.Series((atividades_edicao_selecionada['eixo'].explode().value_counts(dropna=False) * 100 / len(atividades_edicao_selecionada)).round(2).to_dict())
        eixos = pd.DataFrame({
            'Total': total,
            'Porcentagem': porcentagem,
        })

        # rename NaN index to 'Outros
        eixos = eixos.reset_index().rename(columns={'index': 'eixo'})
        eixos['eixo'] = eixos['eixo'].fillna('Outros')
        eixos.set_index('eixo', inplace=True)
        eixos.index.name = ''

        return eixos
    else:
        total = atividades[categoria].value_counts(dropna=False)
        porcentagem = (atividades[categoria].value_counts(dropna=False, normalize=True) * 100).apply(lambda n: round(n, 2))
        df = pd.DataFrame(total).merge(pd.DataFrame(porcentagem), on=categoria).rename(columns={ 'count': 'Total', 'proportion': 'Porcentagem' }, index={None: 'Outros'})
        df.index.name = ''
        return df

def desenhar_grafico(df, height=425, margin=None, font_size=14):
    fig = px.pie(df, names=df.index, values='Total', color_discrete_sequence=colors, hover_data=['Porcentagem'], height=height)
    fig.update_traces(text=[ str(p) + '%' for p in df['Porcentagem']], textinfo='label+text', textposition='outside')
    fig.update_layout(showlegend=False, font=dict(size=font_size))

    if margin is not None:
        fig.update_layout(margin=margin)

    st.plotly_chart(fig, use_container_width=False)

def mostrar_grafico_tabela(df, height=425, margin=dict(t=40,b=110,l=80,r=80), font_size=14):
    grafico, tabela = st.tabs(['Gráfico', 'Tabela'])
    with grafico:
        desenhar_grafico(df, height=height, margin=margin, font_size=font_size)
    with tabela:
        st.dataframe(df)
    st.html('<div class="sep"></div>')

st.title(page_title, anchor="inicio")

st.html('<p id="projeto-descricao">Este projeto de ciência de dados compreendeu na análise da programação das últimas dez edições da Campus Party Brasil, realizadas de 2022 a 2024. Através da metodologia ETL (Extração, Transformação e Carga) e da API de IA do Google, 5492 atividades foram coletadas, categorizadas e analisadas. Isso permitiu identificar tendências na distribuição de eixos temáticos de atividades, formatos de atividades, objetivos de atividades e perfis de organizadores. A análise dos resultados oferece insights sobre as tendencias da Campus Party Brasil como um importante evento do cenário tecnológico nacional. Para assegurar a reprodutibilidade e fomentar investigações futuras, o código-fonte e o dataset deste projeto estão publicamente disponíveis neste <a href="https://github.com/gusalbukrk/cpbr-programacao-analise" target="_blank">link</a>.</p>')

atividades_quant_por_edicao = pd.DataFrame(categorizado['edicao'].value_counts().reindex(cpbr_edicoes_ordem_cronologica)).reset_index()
atividades_quant_por_edicao['edicao_nome'] = cpbr_edicoes_ordem_cronologica_nomes
fig = px.bar(
    atividades_quant_por_edicao,
    text_auto=True,
    x="edicao_nome",
    y="count",
    labels={"edicao_nome": "", "count": ""},
    title="Total de atividades por edições",
    subtitle="soma: 5492; média: 549.2",
)
fig.update_traces(textposition='inside', textfont_color='black', textfont_weight='bold')
st.plotly_chart(fig, use_container_width=True)

edicao_selecionada = st.selectbox('Selecione a edição da Campus Party Brasil', ['Todas as edições'] + cpbr_edicoes_ordem_cronologica, accept_new_options=False)
atividades_edicao_selecionada = categorizado if edicao_selecionada == 'Todas as edições' else categorizado[categorizado['edicao'] == edicao_selecionada]

st.header('Eixos das atividades', anchor='eixos')
eixos = calcular_rotulos(atividades_edicao_selecionada, 'eixo')
mostrar_grafico_tabela(eixos, height=520, margin=dict(t=120, b=120, l=25, r=0), font_size=12)

st.header('Formatos das atividades', anchor='formatos')
formatos = calcular_rotulos(atividades_edicao_selecionada, 'formato')
mostrar_grafico_tabela(formatos, margin=dict(t=20,b=130))

st.header('Objetivos das atividades', anchor='objetivos')
objetivos = calcular_rotulos(atividades_edicao_selecionada, 'objetivo')
mostrar_grafico_tabela(objetivos)

st.header('Perfis dos organizadores', anchor='perfis')
perfis = calcular_rotulos(atividades_edicao_selecionada, 'perfil_organizador')
mostrar_grafico_tabela(perfis)

st.header('Visão geral', anchor='visao_geral')
visao_geral = atividades_edicao_selecionada.copy()
visao_geral['speakers'] = visao_geral['speakers'].apply(str)
visao_geral['eixo'] = visao_geral['eixo'].apply(lambda eixos: '; '.join(sorted(eixos)))
visao_geral.drop(columns=['open'], inplace=True)
visao_geral.rename({
    'edicao': 'Edição',
    'name': 'Nome',
    'description': 'Descrição',
    'eixo': 'Eixos',
    'formato': 'Formato',
    'objetivo': 'Objetivo',
    'perfil_organizador': 'Perfil do(s) organizador(es)',
    'speakers': 'Organizador(es)',
    'start_time': 'Início',
    'end_time': 'Término',
    'auditorium': 'Auditório',
}, axis='columns', inplace=True)
visao_geral_filtrada = dataframe_explorer(visao_geral, case=False)
#
# columns omitted in the list below will be hidden
column_order = ['Edição', 'Nome', 'Descrição', 'Eixos', 'Formato', 'Objetivo', 'Perfil do(s) organizador(es)', 'Organizador(es)', 'Início', 'Término', 'Auditório']
column_config = {
    'Eixos': st.column_config.ListColumn('Eixos', width='large'),
    'Organizador(es)': st.column_config.JsonColumn('Organizador(es)', width='large'),
    'Auditório': st.column_config.TextColumn(width='large'),
    'Início': st.column_config.DatetimeColumn(format="D MMM YYYY - HH:mm"),
    'Término': st.column_config.DatetimeColumn(format="D MMM YYYY - HH:mm"),
}

st.dataframe(visao_geral_filtrada, hide_index=True, column_config=column_config, column_order=column_order)

# Analisa a distribuição das atividades em relação às quatro categorias

import os
import json

eixos = [
    'Inteligência Artificial',
    'Cultura Maker',
    'Sustentabilidade Ambiental',
    'Astronomia e Exploração Espacial',
    'Games',
    'Saúde e Gastronomia',
    'Cibersegurança',
    'Desenvolvimento de Software e Cloud Computing',
    'Ciência de Dados e Big Data',
    'Negócios, Empreendedorismo, Gestão e Marketing',
    'Aspectos Éticos e Legais da Tecnologia',
    'Inclusão e Diversidade',
    'Arte, Design e Multimídia',
    'Entretenimento e Cultura Geek',
    'Desenvolvimento Profissional',
    'Tecnologia na Educação',
    'Web3',
    'Institutional',
]

formatos = [
    'Palestra',
    'Workshop',
    'Painel de Discussão',
    'Competição',
    'Mentoria',
    'Exposição',
    'Meetup',
]

organizador_tipos = [
    'Empresa',
    'Instituição de Ensino',
    'Comunidade ou Grupo de Interesse',
    'Influenciador',
    'Órgão Governamental',
    'Pesquisador ou Especialista',
]

objetivos = [
    'Educar sobre um tema',
    'Ensinar habilidades práticas',
    'Fomentar networking',
    'Apresentar projeto, produto ou startup',
    'Ativação de marca',
    'Entreter',
]

def inicializar_contador_categoria(categorias):
    contador = {rotulo: 0 for rotulo in categorias}
    contador['Outro/Não especificado'] = 0
    return contador

def imprimir_distribuicao(categoria, contador, total):
    print(f"\n--- Distribuição: {categoria} ---")
    for rotulo, valor in contador.items():
        porcentagem = (valor / total) * 100 if total > 0 else 0
        print(f"{rotulo}: {porcentagem:.2f}% ({valor})")

def incrementar_categoria(rotulo, categoria, contador):
    chave = rotulo if rotulo in categoria else 'Outro/Não especificado'
    contador[chave] += 1

def main():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(src_dir, "..", "data", "categorizado.json"), "r", encoding="utf-8") as f:
        atividades = json.load(f)

    atividades_quant_total = len(atividades)

    eixos_contador = inicializar_contador_categoria(eixos)
    formatos_contador = inicializar_contador_categoria(formatos)
    organizador_tipos_contador = inicializar_contador_categoria(organizador_tipos)
    objetivo_contador = inicializar_contador_categoria(objetivos)

    for atividade in atividades:
        incrementar_categoria(atividade.get('eixo'), eixos, eixos_contador)
        incrementar_categoria(atividade.get('formato'), formatos, formatos_contador)
        incrementar_categoria(atividade.get('organizador'), organizador_tipos, organizador_tipos_contador)
        incrementar_categoria(atividade.get('objetivo'), objetivos, objetivo_contador)

    imprimir_distribuicao('Eixos Temáticos', eixos_contador, atividades_quant_total)
    imprimir_distribuicao('Perfil dos Organizadores', organizador_tipos_contador, atividades_quant_total)
    imprimir_distribuicao('Objetivos das Atividades', objetivo_contador, atividades_quant_total)
    imprimir_distribuicao('Formato das Atividades', formatos_contador, atividades_quant_total)

if __name__ == "__main__":
    main()
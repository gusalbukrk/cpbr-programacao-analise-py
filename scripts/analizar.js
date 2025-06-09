import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const eixos = [
    'Inteligência Artificial',
    'Cultura Maker',
    'Tecnologias Sustentáveis',
    'Astronomia e Exploração Espacial',
    'Games',
    'Healthtech',
    'Foodtech',
    'Cibersegurança',
    'Desenvolvimento de Software e Cloud Computing',
    'Ciência de Dados e Big Data',
    'Negócios, Empreendedorismo, Gestão e Marketing',
    'Aspectos Éticos e Legais da Tecnologia',
    'Inclusão e Diversidade',
    'Arte, Design e Multimídia',
    'Entretenimento e Cultura Geek',
    'Desenvolvimento Profissional',
    'Tecnologia e Educação',
    'Web3',
    'Institutional',
];

const formatos = [
    'Palestra',
    'Workshop',
    'Painel de Discussão',
    'Competição',
    'Mentoria',
    'Exposição',
    'Meetup',
];

const organizadorTipos = [
    'Empresa',
    'Startup',
    'Instituição de Ensino',
    'Comunidade ou Grupo de Interesse',
    'Influenciador',
    'Órgão Governamental',
    'Pesquisador ou Especialista',
];

const objetivos = [
    'Educar sobre um tema',
    'Ensinar habilidades práticas',
    'Fomentar networking',
    'Apresentar projeto, produto ou startup',
    'Ativação de marca',
    'Entreter',
];

let eixosContador = inicializarContadorCategoria(eixos);
let formatosContador = inicializarContadorCategoria(formatos);
let organizadorTiposContador = inicializarContadorCategoria(organizadorTipos);
let objetivoContador = inicializarContadorCategoria(objetivos);

const atividades = JSON.parse(
    await fs.readFile(
        path.join(__dirname, '..', 'data', 'categorizado.json'),
        'utf8',
    ),
);

const atividadesQuantTotal = atividades.length;

atividades.forEach((atividade) => {
    const eixo = atividade.eixo || 'Outro/Não especificado';
    if (eixos.includes(eixo)) {
        eixosContador[eixo]++;
    } else {
        eixosContador['Outro/Não especificado']++;
    }

    const formato = atividade.formato || 'Outro/Não especificado';
    if (formatos.includes(formato)) {
        formatosContador[formato]++;
    } else {
        formatosContador['Outro/Não especificado']++;
    }

    const organizador = atividade.organizador || 'Outro/Não especificado';
    if (organizadorTipos.includes(organizador)) {
        organizadorTiposContador[organizador]++;
    } else {
        organizadorTiposContador['Outro/Não especificado']++;
    }

    const objetivo = atividade.objetivo || 'Outro/Não especificado';
    if (objetivos.includes(objetivo)) {
        objetivoContador[objetivo]++;
    } else {
        objetivoContador['Outro/Não especificado']++;
    }
});

imprimirDistribuição('Eixos Temáticos', eixosContador);
imprimirDistribuição('Perfil dos Organizadores', organizadorTiposContador);
imprimirDistribuição('Objetivos das Atividades', objetivoContador);
imprimirDistribuição('Formato das Atividades', formatosContador);

function inicializarContadorCategoria(categoria) {
    const contador = {};
    categoria.forEach((rotulo) => {
        contador[rotulo] = 0;
    });
    contador['Outro/Não especificado'] = 0;
    return contador;
}

function imprimirDistribuição(categoria, contador) {
    console.log(`\n--- Distribuição: ${categoria} ---`);
    for (const rotulo in contador) {
        const porcentagem = (contador[rotulo] / atividadesQuantTotal) * 100;
        console.log(
            `${rotulo}: ${porcentagem.toFixed(2)}% (${contador[rotulo]})`,
        );
    }
}

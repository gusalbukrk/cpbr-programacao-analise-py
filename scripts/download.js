// Faz o download dos arquivos JSON contendo a programação das últimas 10 edições da Campus Party.

import fs from 'node:fs/promises';
import path, { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import metadados from '../metadados.json' with { type: 'json' };

const __dirname = dirname(fileURLToPath(import.meta.url)) + '/';

const downloadsDir = path.join(__dirname, '..', 'data', 'downloads');

try {
    await fs.stat(downloadsDir);
} catch (error) {
    await fs.mkdir(downloadsDir, {
        recursive: true,
    });
}

for (const [index, edicao] of metadados.entries()) {
    // em `metadados.json`, os arquivos estão enumerados em ordem decrescente
    // (da edição mais recente para a mais antiga)
    const arquivoNome = `${index} - ${edicao.nome}.json`;
    const arquivoNomeBancadas = `${index} - ${edicao.nome}-bancadas.json`;

    await download(edicao.programacaoLink, arquivoNome);

    // as 3 últimas edições listam a programação principal e as atividades das bancadas separadamente
    if (edicao.programacaoBancadasLink !== null)
        download(edicao.programacaoBancadasLink, arquivoNomeBancadas);
}

async function download(url, filename) {
    console.log(`Download em progresso: "${filename}"`);

    const json = await (await fetch(url)).json();
    await fs.writeFile(
        path.join(downloadsDir, filename),
        JSON.stringify(json, null, 2),
    );

    console.log(`Download finalizado: "${filename}"`);
}

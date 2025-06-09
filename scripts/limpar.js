// Consolida os arquivos JSON baixados em um único arquivo e remove dados irrelevantes.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { stripHtml } from 'string-strip-html';
import { createHash } from 'node:crypto';

const __dirname = path.dirname(fileURLToPath(import.meta.url)) + '/';

const downloadsDir = path.join(__dirname, '../data/downloads');
const arquivosJson = fs
    .readdirSync(downloadsDir)
    .filter((file) => file.endsWith('.json'));

// programação das últimas 10 edições da Campus Party, separadas por edições
const programacao = [];

for (const arquivoJson of arquivosJson) {
    console.log(`Processando: "${arquivoJson}"`);

    const edicaoNome = /(?<=\d - ).*(?=\.json)/
        .exec(arquivoJson)[0]
        .replace('-bancadas', '');

    const json = JSON.parse(
        fs.readFileSync(path.join(downloadsDir, arquivoJson), 'utf8'),
    );

    json.result.schedule
        .map((s) => s.activity_list)
        .flat()
        .forEach((atividade) => {
            const atividadeLimpa = {
                name: atividade.name,
                auditorium: atividade.auditorium_name,
                description: stripHtml(atividade.description.trim()).result,
                open: atividade.open,
                start_time: atividade.start_time,
                end_time: atividade.end_time,
                speakers: atividade.speakers.map((speaker) => ({
                    name: speaker.name,
                    profession: speaker.profession,
                    description: stripHtml((speaker.description ?? '').trim())
                        .result,
                })),
            };

            const uid = gerarUid(atividadeLimpa);

            // descarta duplicatas
            if (programacao.some((item) => item.uid === uid)) return;

            programacao.push({
                uid,
                edicao: edicaoNome,
                ...atividadeLimpa,
            });
        });
}

escreverArquivo(path.join(__dirname, '../data/limpo.json'), programacao);

function escreverArquivo(caminho, data) {
    try {
        fs.writeFileSync(caminho, JSON.stringify(data, null, 2), 'utf8');
        console.log(`Arquivo escrito: ${caminho}`);
    } catch (error) {
        console.error('Error ao tentar escrever o arquivo:', error);
    }
}

export function gerarUid(obj) {
    const str = JSON.stringify(obj);
    const hash = createHash('sha256');
    hash.update(str, 'utf8');
    const reproducibleId = hash.digest('hex');
    return reproducibleId;
}

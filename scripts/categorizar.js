// Usa Gemini API para classificar as atividades em quatro categorias:
// eixo temático, perfil do organizador, formato da atividade e objetivo da atividade.

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import 'dotenv/config';
import { GoogleGenAI } from '@google/genai';

const __dirname = path.dirname(fileURLToPath(import.meta.url)) + '/';

import limpo from '../data/limpo.json' with { type: 'json' };
const promptTemplate = await lerArquivo('../promptTemplate.md');

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

const categorizadoCaminho = path.join(
    __dirname,
    '..',
    'data',
    'categorizado.json',
);
let categorizado = [];
try {
    categorizado = JSON.parse(await fs.readFile(categorizadoCaminho, 'utf8'));
} catch (error) {
    await atualizarArquivoCategorizado();
}

const atividadesQuantTotal = limpo.length;

for (const atividade of limpo) {
    if (categorizado.some((item) => item.uid === atividade.uid)) continue;

    console.log(
        `${obterHorarioAtual()} - ${categorizado.length + 1} de ${atividadesQuantTotal}`,
    );

    const prompt = `${promptTemplate}${JSON.stringify(omitirAtributosIrrelevantes(atividade))}`;

    const resp = await AI(prompt);
    const respJson = JSON.parse(removeMarkdownCodeBlocks(resp.text));

    categorizado.push({ ...atividade, ...respJson });
    await atualizarArquivoCategorizado();
}

async function atualizarArquivoCategorizado() {
    return await fs.writeFile(
        categorizadoCaminho,
        JSON.stringify(categorizado, null, 2),
    );
}

async function lerArquivo(filePath) {
    try {
        return await fs.readFile(path.join(__dirname, filePath), {
            encoding: 'utf8',
        });
    } catch (error) {
        console.error('Error reading file:', error);
        return null;
    }
}

function omitirAtributosIrrelevantes(atividade) {
    const { open, start_time, end_time, speakers, ...relevantProperties } =
        atividade;
    relevantProperties.organizers = speakers;
    return relevantProperties;
}

function removeMarkdownCodeBlocks(text) {
    return text
        .replace(/^\s*```(?:json\s*)?\n*/, '')
        .replace(/\s*```\s*$/, '')
        .trim();
}

async function AI(prompt) {
    const resp = await ai.models.generateContent({
        // model: "gemini-2.5-flash-preview-04-17",
        // model: 'gemini-2.0-flash',
        model: 'gemini-2.0-flash-lite',
        contents: prompt,
        // config: {
        //     includeThoughts: {
        //         includeThoughts: false,
        //     },
        // }
    });

    return resp;
}

function obterHorarioAtual() {
    const agora = new Date();

    const horas = agora.getHours();
    const minutos = agora.getMinutes();
    const segundos = agora.getSeconds();

    const horasFormatada = String(horas).padStart(2, '0');
    const minutosFormatados = String(minutos).padStart(2, '0');
    const segundosFormatado = String(segundos).padStart(2, '0');

    return `${horasFormatada}:${minutosFormatados}:${segundosFormatado}`;
}

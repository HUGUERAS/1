#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import * as fs from 'fs/promises';
import * as path from 'path';
import { XMLParser } from 'fast-xml-parser';

const server = new Server({ name: 'ativo-real-filesystem', version: '1.0.0' }, { capabilities: { tools: {} } });

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'read_file',
        description: 'Le um arquivo do disco',
        inputSchema: { type: 'object', properties: { filePath: { type: 'string' } }, required: ['filePath'] },
      },
      {
        name: 'write_file',
        description: 'Escreve um arquivo no disco',
        inputSchema: { type: 'object', properties: { filePath: { type: 'string' }, content: { type: 'string' } }, required: ['filePath', 'content'] },
      },
      {
        name: 'list_files',
        description: 'Lista arquivos em um diretorio',
        inputSchema: { type: 'object', properties: { dirPath: { type: 'string' } }, required: ['dirPath'] },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request: any) => {
  const { name, arguments: args } = request.params;
  try {
    if (name === 'read_file') {
      const content = await fs.readFile(args.filePath, 'utf-8');
      return { content: [{ type: 'text', text: content }] };
    }
    if (name === 'write_file') {
      await fs.writeFile(args.filePath, args.content);
      return { content: [{ type: 'text', text: 'OK: Arquivo salvo' }] };
    }
    if (name === 'list_files') {
      const files = await fs.readdir(args.dirPath);
      return { content: [{ type: 'text', text: JSON.stringify(files) }] };
    }
    throw new Error('Ferramenta desconhecida');
  } catch (error: any) {
    return { content: [{ type: 'text', text: 'ERRO: ' + error.message }], isError: true };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('MCP Filesystem iniciado!');
}

main().catch((error) => {
  console.error('Erro fatal:', error);
  process.exit(1);
});

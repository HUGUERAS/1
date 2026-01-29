#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { CosmosClient } from '@azure/cosmos';

let cosmosClient: any;
let projectsContainer: any;

const server = new Server({ name: 'ativo-real-cosmosdb', version: '1.0.0' }, { capabilities: { tools: {} } });

function initCosmosDB() {
  const endpoint = process.env.COSMOS_ENDPOINT || '';
  const key = process.env.COSMOS_KEY || '';
  if (!endpoint || !key) throw new Error('COSMOS_ENDPOINT e COSMOS_KEY obrigatorios!');
  cosmosClient = new CosmosClient({ endpoint, key });
  projectsContainer = cosmosClient.database('ativo-real').container('projetos');
}

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      { name: 'create_project', description: 'Cria novo projeto', inputSchema: { type: 'object', properties: { titulo: { type: 'string' }, local: { type: 'string' }, proprietario: { type: 'string' } }, required: ['titulo'] } },
      { name: 'list_projects', description: 'Lista projetos', inputSchema: { type: 'object', properties: {} } },
      { name: 'get_project', description: 'Busca projeto por ID', inputSchema: { type: 'object', properties: { id: { type: 'string' } }, required: ['id'] } },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request: any) => {
  const { name, arguments: args } = request.params;
  try {
    if (name === 'create_project') {
      const projeto = { id: `proj_${Date.now()}`, titulo: args.titulo, local: args.local || '', proprietario: args.proprietario || '', status: 'em_andamento' };
      const { resource } = await projectsContainer.items.create(projeto);
      return { content: [{ type: 'text', text: JSON.stringify({ success: true, id: resource.id, titulo: resource.titulo }) }] };
    }
    if (name === 'list_projects') {
      const { resources } = await projectsContainer.items.query('SELECT * FROM c').fetchAll();
      return { content: [{ type: 'text', text: JSON.stringify({ success: true, total: resources.length, projects: resources }) }] };
    }
    if (name === 'get_project') {
      const { resource } = await projectsContainer.item(args.id, args.id).read();
      return { content: [{ type: 'text', text: JSON.stringify({ success: true, project: resource }) }] };
    }
    throw new Error('Ferramenta desconhecida');
  } catch (error: any) {
    return { content: [{ type: 'text', text: JSON.stringify({ success: false, error: error.message }) }], isError: true };
  }
});

async function main() {
  initCosmosDB();
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('MCP Cosmos DB iniciado!');
}

main().catch((error) => {
  console.error('Erro fatal:', error);
  process.exit(1);
});

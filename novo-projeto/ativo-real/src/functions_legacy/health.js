const { app } = require('@azure/functions')

function jsonResponse(status, body) {
    return {
        status,
        headers: { 'Content-Type': 'application/json' },
        jsonBody: body,
    }
}

app.http('health', {
    methods: ['GET'],
    authLevel: 'anonymous',
    route: 'health',
    handler: async () => jsonResponse(200, { status: 'ok', service: 'ativo-real-api' }),
})

const { app } = require('@azure/functions')

function jsonResponse(status, body) {
  return {
    status,
    headers: {
      'Content-Type': 'application/json',
    },
    jsonBody: body,
  }
}

app.http('techLogin', {
  methods: ['POST'],
  authLevel: 'anonymous',
  route: 'tech/login',
  handler: async (request) => {
    let payload
    try {
      payload = await request.json()
    } catch (err) {
      return jsonResponse(400, { error: 'Invalid JSON body' })
    }

    const { username, password } = payload || {}

    if (!username || !password) {
      return jsonResponse(400, { error: 'username and password are required' })
    }

    if (password.length < 6) {
      return jsonResponse(400, { error: 'password must have at least 6 characters' })
    }

    return jsonResponse(200, {
      success: true,
      sessionId: `session-${Date.now()}`,
      message: 'Technician authenticated',
    })
  },
})

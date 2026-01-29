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

function onlyDigits(value = '') {
  return String(value).replace(/\D/g, '')
}

app.http('urbanActivate', {
  methods: ['POST'],
  authLevel: 'anonymous',
  route: 'urban/activate',
  handler: async (request) => {
    let payload
    try {
      payload = await request.json()
    } catch (err) {
      return jsonResponse(400, { error: 'Invalid JSON body' })
    }

    const { cpf, birthDate, password } = payload || {}
    const cpfDigits = onlyDigits(cpf)

    if (!cpfDigits || cpfDigits.length !== 11) {
      return jsonResponse(400, { error: 'cpf must have 11 digits' })
    }

    if (!birthDate) {
      return jsonResponse(400, { error: 'birthDate is required (YYYY-MM-DD)' })
    }

    if (!password || password.length < 6) {
      return jsonResponse(400, { error: 'password must have at least 6 characters' })
    }

    return jsonResponse(200, {
      success: true,
      userId: `urban-user-${Date.now()}`,
      message: 'Urban account activated',
    })
  },
})

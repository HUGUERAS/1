const http = require('http')

const PORT = process.env.MOCK_PORT || 4000
const JSON_TYPE = 'application/json'

function send(res, status, data) {
  const body = JSON.stringify(data)
  res.writeHead(status, {
    'Content-Type': JSON_TYPE,
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  })
  res.end(body)
}

function parseJson(req) {
  return new Promise((resolve, reject) => {
    let raw = ''
    req.on('data', chunk => { raw += chunk })
    req.on('end', () => {
      if (!raw) return resolve({})
      try {
        resolve(JSON.parse(raw))
      } catch (err) {
        reject(err)
      }
    })
    req.on('error', reject)
  })
}

function notFound(res) {
  send(res, 404, { error: 'Not found' })
}

function badRequest(res, message) {
  send(res, 400, { error: message })
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    })
    return res.end()
  }

  if (req.method !== 'POST') {
    return notFound(res)
  }

  const url = req.url || ''

  try {
    const body = await parseJson(req)

    if (url === '/api/rural/onboard') {
      const { farmName, document, area, email } = body || {}
      const areaNumber = Number(area)
      if (!farmName || !document || !area || !email) {
        return badRequest(res, 'farmName, document, area, and email are required')
      }
      if (Number.isNaN(areaNumber) || areaNumber <= 0) {
        return badRequest(res, 'area must be a positive number')
      }
      const organizationId = `org-${Date.now()}`
      const adminUserId = `user-${Date.now()}`
      return send(res, 201, {
        message: 'Rural organization created',
        organizationId,
        adminUserId,
        organization: {
          organizationId,
          adminUserId,
          name: farmName,
          document,
          area: areaNumber,
          email,
          createdAt: new Date().toISOString(),
        },
      })
    }

    if (url === '/api/urban/activate') {
      const digits = String(body.cpf || '').replace(/\D/g, '')
      if (digits.length !== 11) {
        return badRequest(res, 'cpf must have 11 digits')
      }
      if (!body.birthDate) {
        return badRequest(res, 'birthDate is required (YYYY-MM-DD)')
      }
      if (!body.password || String(body.password).length < 6) {
        return badRequest(res, 'password must have at least 6 characters')
      }
      return send(res, 200, {
        success: true,
        userId: `urban-user-${Date.now()}`,
        message: 'Urban account activated',
      })
    }

    if (url === '/api/tech/login') {
      const { username, password } = body || {}
      if (!username || !password) {
        return badRequest(res, 'username and password are required')
      }
      if (String(password).length < 6) {
        return badRequest(res, 'password must have at least 6 characters')
      }
      return send(res, 200, {
        success: true,
        sessionId: `session-${Date.now()}`,
        message: 'Technician authenticated',
      })
    }

    return notFound(res)
  } catch (err) {
    console.error('Mock server error', err)
    send(res, 500, { error: 'Internal error' })
  }
})

server.listen(PORT, () => {
  console.log(`Mock API running at http://localhost:${PORT}/api`)
})

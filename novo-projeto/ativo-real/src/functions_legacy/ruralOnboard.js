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

app.http('ruralOnboard', {
  methods: ['POST'],
  authLevel: 'anonymous',
  route: 'rural/onboard',
  handler: async (request, context) => {
    let payload
    try {
      payload = await request.json()
    } catch (err) {
      return jsonResponse(400, { error: 'Invalid JSON body' })
    }

    const { farmName, document, area, email } = payload || {}

    if (!farmName || !document || !area || !email) {
      return jsonResponse(400, {
        error: 'farmName, document, area, and email are required',
      })
    }

    const areaNumber = Number(area)
    if (Number.isNaN(areaNumber) || areaNumber <= 0) {
      return jsonResponse(400, { error: 'area must be a positive number' })
    }

    const organizationId = `org-${Date.now()}`
    const adminUserId = `user-${Date.now()}`

    context.log('Rural onboard request', { farmName, document, areaNumber, email })

    return jsonResponse(201, {
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
  },
})

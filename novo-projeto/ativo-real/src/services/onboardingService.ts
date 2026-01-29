/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */
// API client for onboarding flows (default points to Azure Functions /api; override with VITE_API_BASE)

const API_BASE = (import.meta as { env?: Record<string, string> }).env?.VITE_API_BASE || '/api'

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })

  if (!res.ok) {
    let errorMessage = `Request failed (${res.status})`
    try {
      const errorBody = await res.json()
      errorMessage = errorBody?.error || errorBody?.message || errorMessage
    } catch {
      // ignore parse errors
    }
    throw new Error(errorMessage)
  }

  return res.json() as Promise<T>
}
export interface RuralOrganizationRecord {
  organizationId: string
  adminUserId: string
  name: string
  document: string
  area: number
  email: string
  createdAt: string
  tenantId: string
  partitionKey: string
}

export interface OnboardingSnapshot {
  ruralOrganizations: RuralOrganizationRecord[]
  urbanActivations: unknown[]
  technicianSessions: any[]
}

export interface RegisterRuralFarmParams {
  farmName: string
  document: string
  area: string
  email: string
}

export interface RegisterRuralFarmResult {
  organizationId: string
  adminUserId: string
  organization: RuralOrganizationRecord
}

export interface ActivateUrbanAccountParams {
  cpf: string
  birthDate: string
  password: string
}

export interface LoginTechnicianParams {
  username: string
  password: string
}

// Mock implementations
export async function registerRuralFarm(
  params: RegisterRuralFarmParams
): Promise<RegisterRuralFarmResult> {
  return postJson<RegisterRuralFarmResult>('/rural/onboard', params)
}

export async function activateUrbanAccount(
  params: ActivateUrbanAccountParams
): Promise<{ success: boolean; userId: string }> {
  return postJson('/urban/activate', params)
}

export async function loginTechnician(
  params: LoginTechnicianParams
): Promise<{ success: boolean; sessionId: string }> {
  return postJson('/tech/login', params)
}

export function getOnboardingSnapshot(): OnboardingSnapshot {
  return {
    ruralOrganizations: [],
    urbanActivations: [],
    technicianSessions: [],
  }
}

const API_BASE = '/api'

export async function fetchHealth(): Promise<Response> {
  return fetch(API_BASE + '/')
}

export async function uploadFile(file: File): Promise<Response> {
  const form = new FormData()
  form.append('file', file)
  return fetch(API_BASE + '/upload', { method: 'POST', body: form })
}

export async function reviewFile(file: File): Promise<Response> {
  const form = new FormData()
  form.append('file', file)
  return fetch(API_BASE + '/review', { method: 'POST', body: form })
}

export async function ingestKnowledge(): Promise<Response> {
  return fetch(API_BASE + '/knowledge/ingest', { method: 'POST' })
}

export async function fetchKnowledgeStats(): Promise<Response> {
  return fetch(API_BASE + '/knowledge/stats')
}

export async function searchKnowledge(
  q: string,
  collection: string,
  limit = 5
): Promise<Response> {
  const params = new URLSearchParams({ q, collection, limit: String(limit) })
  return fetch(API_BASE + '/knowledge/search?' + params)
}

export async function addKnowledge(
  collection: string,
  text: string,
  source = ''
): Promise<Response> {
  return fetch(API_BASE + '/knowledge/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ collection, text, source }),
  })
}

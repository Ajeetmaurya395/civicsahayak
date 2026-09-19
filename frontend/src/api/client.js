/** API client for the CivicOS orchestrator. */

const API_BASE = import.meta.env.VITE_API_URL || '';

async function apiFetch(url, options) {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API Error ${response.status}: ${error}`);
  }
  return response.json();
}

export async function sendChatMessage(message, conversationId) {
  return apiFetch('/chat', {
    method: 'POST',
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  });
}

export async function searchSchemes(profile) {
  return apiFetch('/schemes/search', {
    method: 'POST',
    body: JSON.stringify({ profile, limit: 10 }),
  });
}

export async function checkEligibility(userProfile, schemeCriteria) {
  return apiFetch('/schemes/check-eligibility', {
    method: 'POST',
    body: JSON.stringify({
      user_profile: userProfile,
      scheme_criteria: schemeCriteria,
    }),
  });
}

export async function saveScheme(scheme) {
  return apiFetch('/schemes/save', {
    method: 'POST',
    body: JSON.stringify(scheme),
  });
}

export async function uploadDocument(file, documentType) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('document_type', documentType);

  const response = await fetch(`${API_BASE}/documents/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!response.ok) throw new Error(`Upload failed: ${response.statusText}`);
  return response.json();
}

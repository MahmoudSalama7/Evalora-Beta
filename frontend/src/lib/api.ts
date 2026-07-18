/**
 * API Fetch Helper
 * Handles requests to the FastAPI backend, auth header injections, and JSON parsers.
 */

const BASE_URL = '';

interface RequestOptions extends RequestInit {
  params?: Record<string, string | number | boolean>;
}

export async function apiFetch<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { params, headers, ...rest } = options;
  
  // Format URL query params if any
  let url = `${BASE_URL}${endpoint}`;
  if (params) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, val]) => {
      if (val !== undefined && val !== null) {
        query.append(key, String(val));
      }
    });
    url += `?${query.toString()}`;
  }

  // Set default headers
  const defaultHeaders: Record<string, string> = {};
  if (!(rest.body instanceof FormData)) {
    defaultHeaders['Content-Type'] = 'application/json';
  }

  // Fetch token from localStorage if logged in
  const token = localStorage.getItem('evalora_auth_token');
  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
  }

  const mergedHeaders = {
    ...defaultHeaders,
    ...headers,
  };

  const response = await fetch(url, {
    ...rest,
    headers: mergedHeaders,
  });

  if (!response.ok) {
    const errorBody = await response.text().catch(() => '');
    let errorMessage = `Request failed with status ${response.status}`;
    try {
      const parsed = JSON.parse(errorBody);
      if (parsed && parsed.detail) {
        errorMessage = typeof parsed.detail === 'string' ? parsed.detail : JSON.stringify(parsed.detail);
      }
    } catch {
      if (errorBody) {
        errorMessage = errorBody;
      }
    }
    throw new Error(errorMessage);
  }

  // Handle empty responses
  if (response.status === 204) {
    return {} as T;
  }

  return response.json() as Promise<T>;
}

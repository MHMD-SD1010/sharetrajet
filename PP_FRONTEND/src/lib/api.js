const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "http://localhost:8000";

function buildUrl(path) {
  if (path.startsWith("http://") || path.startsWith("https://")) {
    return path;
  }
  return `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;
}

export async function apiRequest(path, { method = "GET", body, token, headers = {} } = {}) {
  const response = await fetch(buildUrl(path), {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const message =
      payload?.error ||
      payload?.detail ||
      payload?.message ||
      `Request failed (${response.status})`;
    throw new Error(message);
  }

  return payload;
}

export function persistAuth(data) {
  if (!data?.tokens) return;
  localStorage.setItem("access_token", data.tokens.access || "");
  localStorage.setItem("refresh_token", data.tokens.refresh || "");
  localStorage.setItem("current_user", JSON.stringify(data.user || null));
}

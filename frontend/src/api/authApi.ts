import type { AuthSession } from "../types/review";

const AUTH_STORAGE_KEY = "code-review-auth-session";

export const loadAuthSession = (): AuthSession | null => {
  const stored = window.localStorage.getItem(AUTH_STORAGE_KEY);
  if (!stored) return null;

  try {
    return JSON.parse(stored) as AuthSession;
  } catch {
    window.localStorage.removeItem(AUTH_STORAGE_KEY);
    return null;
  }
};

export const saveAuthSession = (session: AuthSession) => {
  window.localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(session));
};

export const clearAuthSession = () => {
  window.localStorage.removeItem(AUTH_STORAGE_KEY);
};

const readErrorMessage = async (response: Response) => {
  try {
    const body = (await response.json()) as { detail?: unknown };
    if (typeof body.detail === "string") return body.detail;
    if (body.detail && typeof body.detail === "object" && "message" in body.detail) {
      return String((body.detail as { message: unknown }).message);
    }
  } catch {
    // Use the generic status message below when the body is not JSON.
  }

  return `请求失败：${response.status}`;
};

const submitAuth = async (
  apiBaseUrl: string,
  path: "/auth/login" | "/auth/register",
  email: string,
  password: string,
) => {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }

  return (await response.json()) as AuthSession;
};

export const login = (apiBaseUrl: string, email: string, password: string) =>
  submitAuth(apiBaseUrl, "/auth/login", email, password);

export const register = (apiBaseUrl: string, email: string, password: string) =>
  submitAuth(apiBaseUrl, "/auth/register", email, password);

export const logout = async (apiBaseUrl: string, accessToken: string, refreshToken: string) => {
  const response = await fetch(`${apiBaseUrl}/auth/logout`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  if (!response.ok && response.status !== 401) {
    throw new Error(await readErrorMessage(response));
  }
};

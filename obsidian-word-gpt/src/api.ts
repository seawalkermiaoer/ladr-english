/** API 客户端：基于 Token 与可配置服务器地址进行通信 */

export interface StatsResponse {
  total: number;
  reviewed: number;
  due_today: number;
}

let BASE_URL = "";
let TOKEN = "";

/** 设置基础 URL，如 http://127.0.0.1:8000 */
export function setBaseUrl(url: string): void {
  BASE_URL = url?.replace(/\/$/, "") || "";
}

/** 设置 Bearer Token */
export function setToken(token: string): void {
  TOKEN = token || "";
}

/** 统一请求封装，自动附加 Authorization 头 */
export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  if (!BASE_URL) throw new Error("服务地址未配置");
  const url = `${BASE_URL}${path.startsWith("/") ? path : "/" + path}`;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init.headers as Record<string, string> | undefined),
  };
  if (TOKEN) headers["Authorization"] = `Bearer ${TOKEN}`;

  const resp = await fetch(url, { ...init, headers });
  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(text || `HTTP ${resp.status}`);
  }
  const contentType = resp.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return (await resp.json()) as T;
  }
  // 非 JSON 返回空对象
  return {} as T;
}

/** 健康检查（无需 Token） */
export async function getHealth(): Promise<{ status: string }> {
  return request<{ status: string }>("/health", { method: "GET" });
}

/** 词库统计（需 Token） */
export async function getStats(): Promise<StatsResponse> {
  return request<StatsResponse>("/api/stats", { method: "GET" });
}

export async function verify(): Promise<{ ok: boolean; token: string }> {
  return request<{ ok: boolean; token: string }>("/api/verify", { method: "GET" });
}

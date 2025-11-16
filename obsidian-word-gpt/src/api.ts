/** API 客户端：基于 Token 与可配置服务器地址进行通信 */

export interface StatsResponse {
  total: number;
  reviewed: number;
  due_today: number;
}

export interface UserInfo {
  id: number;
  name: string;
  created_at: string;
  openid: string;
  current_level: string;
  token: string;
  updated_at: string;
}

// Article word interfaces
export interface ArticleWord {
  id: number;
  openid: string;
  word: string;
  definition: string;
  ai_memory: string;
  created_at: string;
}

export interface ArticleWordListResponse {
  openid: string;
  article_id: string;
  words: ArticleWord[];
}

// Set the base URL directly since it's fixed
const BASE_URL = "https://jrwhb5.faas.xiaoduoai.com";
let TOKEN = "";

/** 设置 Bearer Token */
export function setToken(token: string): void {
  TOKEN = token || "";
}

/** 统一请求封装，自动附加 Authorization 头 */
export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
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

/** 获取用户信息 */
export async function getUserInfo(): Promise<UserInfo> {
  return request<UserInfo>("/ladr-user-info", { method: "GET" });
}

/** 获取文章单词列表 */
export async function getArticleWordList(openid: string, article_id: string): Promise<ArticleWordListResponse> {
  return request<ArticleWordListResponse>("/ladr-article-word-list", {
    method: "POST",
    body: JSON.stringify({ openid, article_id })
  });
}

/** 插入单词到文章 */
export async function insertArticleWord(openid: string, article_id: string, word: string): Promise<any> {
  return request<any>("/ladr-article-insert-word", {
    method: "POST",
    body: JSON.stringify({ openid, article_id, word })
  });
}

/** 从文章中移除单词 */
export async function removeArticleWord(openid: string, article_id: string, word: string): Promise<any> {
  return request<any>("/ladr-article-remove-word", {
    method: "POST",
    body: JSON.stringify({ openid, article_id, word })
  });
}
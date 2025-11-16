/** Test file for the new API functions */

// Since we can't easily import the TypeScript module directly, we'll reimplement the key parts here
const BASE_URL = "https://jrwhb5.faas.xiaoduoai.com";
let TOKEN = "";

/** 设置 Bearer Token */
function setToken(token) {
  TOKEN = token || "";
}

/** 统一请求封装，自动附加 Authorization 头 */
async function request(path, init = {}) {
  const url = `${BASE_URL}${path.startsWith("/") ? path : "/" + path}`;

  const headers = {
    "Content-Type": "application/json",
    ...(init.headers || {}),
  };
  if (TOKEN) headers["Authorization"] = `Bearer ${TOKEN}`;

  const resp = await fetch(url, { ...init, headers });
  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(text || `HTTP ${resp.status}`);
  }
  const contentType = resp.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return await resp.json();
  }
  // 非 JSON 返回空对象
  return {};
}

/** 获取文章单词列表 */
async function getArticleWordList(openid, article_id) {
  return request("/ladr-article-word-list", {
    method: "POST",
    body: JSON.stringify({ openid, article_id })
  });
}

/** 插入单词到文章 */
async function insertArticleWord(openid, article_id, word) {
  return request("/ladr-article-insert-word", {
    method: "POST",
    body: JSON.stringify({ openid, article_id, word })
  });
}

/** 从文章中移除单词 */
async function removeArticleWord(openid, article_id, word) {
  return request("/ladr-article-remove-word", {
    method: "POST",
    body: JSON.stringify({ openid, article_id, word })
  });
}

function testAPIs() {
  // Set the token
  setToken("wmfOHOeRz605z3A");
  
  const openid = "okUi951rYmFM_wmfOHOeRz605z3A";
  const article_id = "Q2cSZhk8LzvRCXYw";
  const testWord = "subject";
  
  console.log("Testing getArticleWordList...");
  getArticleWordList(openid, article_id)
    .then(wordList => {
      console.log("Word list:", wordList);
      
      console.log("\nTesting insertArticleWord...");
      return insertArticleWord(openid, article_id, testWord);
    })
    .then(insertResult => {
      console.log("Insert result:", insertResult);
      
      console.log("\nTesting removeArticleWord...");
      return removeArticleWord(openid, article_id, testWord);
    })
    .then(removeResult => {
      console.log("Remove result:", removeResult);
    })
    .catch(error => {
      console.error("Error testing APIs:", error);
    });
}

// Run the tests
testAPIs();
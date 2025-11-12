import { setBaseUrl, setToken, request, getHealth, getStats, verify } from "../src/api";

describe("API client", () => {
  const fetchMock = jest.fn();
  const origFetch = global.fetch as any;

  beforeEach(() => {
    fetchMock.mockReset();
    // @ts-ignore
    global.fetch = fetchMock;
    setBaseUrl("http://127.0.0.1:8000");
    setToken("test-token");
  });

  afterAll(() => {
    // @ts-ignore
    global.fetch = origFetch;
  });

  it("attaches Authorization header", async () => {
    fetchMock.mockResolvedValue({ ok: true, headers: new Map([["content-type", "application/json"]]), json: async () => ({ ok: true }) });
    await request("/api/stats", { method: "GET" });
    const call = fetchMock.mock.calls[0];
    expect(call[0]).toBe("http://127.0.0.1:8000/api/stats");
    expect(call[1].headers["Authorization"]).toBe("Bearer test-token");
  });

  it("parses JSON and handles errors", async () => {
    fetchMock.mockResolvedValueOnce({ ok: true, headers: new Map([["content-type", "application/json"]]), json: async () => ({ status: "ok" }) });
    const h = await getHealth();
    expect(h.status).toBe("ok");

    fetchMock.mockResolvedValueOnce({ ok: false, text: async () => "Bad Request", headers: new Map() });
    await expect(getStats()).rejects.toThrow("Bad Request");
  });

  it("calls /api/verify with Authorization", async () => {
    fetchMock.mockResolvedValue({ ok: true, headers: new Map([["content-type", "application/json"]]), json: async () => ({ ok: true, token: "test-token" }) });
    const res = await verify();
    expect(res.ok).toBe(true);
    const call = fetchMock.mock.calls[0];
    expect(call[0]).toBe("http://127.0.0.1:8000/api/verify");
    expect(call[1].headers["Authorization"]).toBe("Bearer test-token");
  });
});

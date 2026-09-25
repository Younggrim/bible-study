// mcp.js — MCP (Model Context Protocol) endpoint for the esv-proxy Worker.
//
// Lets claude.ai use the ESV API as a custom connector (e.g. the Stored Up
// memorization app's "Look up" button). It lives beside the existing /?q=
// route and does not change it.
//
// Route:  POST /mcp/<MCP_PATH_KEY>
//   Claude's servers call this directly, so there is no browser Origin to
//   check. The secret path segment takes the place of the origin allowlist:
//   without the right key every request gets a plain 404.
//
// Secrets (set with `npx wrangler secret put <NAME>`):
//   ESV_API_TOKEN  – already set for the existing proxy; reused here
//   MCP_PATH_KEY   – new; a long random string (see DEPLOY.md)
//
// Transport: MCP "Streamable HTTP", stateless, JSON responses only
// (no SSE stream, no session ids). Supports initialize, ping,
// tools/list and tools/call.

const SERVER_INFO = { name: "esv", title: "ESV Bible", version: "1.0.0" };
const SUPPORTED_VERSIONS = ["2025-06-18", "2025-03-26", "2024-11-05"];
const CACHE_TTL_SECONDS = 60 * 60 * 24 * 30; // 30 days, same as the /?q= route
const MAX_REFERENCE_LENGTH = 120;

const TOOLS = [
  {
    name: "esv_passage",
    title: "Get ESV passage text",
    description:
      "Returns the plain text of a Bible passage in the English Standard Version (ESV). " +
      "Accepts a reference like 'Romans 12:2', 'Psalm 23', or 'Philippians 4:6-7'. " +
      "By default the text has no verse numbers, headings, or footnotes, which suits memorization.",
    inputSchema: {
      type: "object",
      properties: {
        reference: {
          type: "string",
          description: "Bible reference, e.g. 'John 3:16' or 'Philippians 4:6-7'.",
        },
        include_verse_numbers: {
          type: "boolean",
          description: "Include bracketed verse numbers like [6] in the text. Defaults to false.",
        },
      },
      required: ["reference"],
      additionalProperties: false,
    },
    outputSchema: {
      type: "object",
      properties: {
        reference: { type: "string", description: "Canonical reference returned by the ESV API." },
        text: { type: "string", description: "Passage text." },
        translation: { type: "string" },
        copyright: { type: "string" },
      },
      required: ["reference", "text", "translation", "copyright"],
    },
    annotations: { readOnlyHint: true, openWorldHint: true },
  },
];

const JSON_HEADERS = { "Content-Type": "application/json", "Cache-Control": "no-store" };

export function isMcpPath(url) {
  return url.pathname === "/mcp" || url.pathname.startsWith("/mcp/");
}

export async function handleMcp(request, env, ctx) {
  const url = new URL(request.url);
  const key = url.pathname.slice("/mcp/".length).replace(/\/+$/, "");
  if (!env.MCP_PATH_KEY || !key || !timingSafeEqual(key, env.MCP_PATH_KEY)) {
    return new Response("Not found", { status: 404 });
  }

  if (request.method !== "POST") {
    // Stateless server: no SSE stream (GET) and no sessions to end (DELETE).
    return new Response("Method not allowed", { status: 405, headers: { Allow: "POST" } });
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return rpcResponse(rpcError(null, -32700, "Parse error"), 400);
  }

  // Older clients may send a JSON-RPC batch.
  if (Array.isArray(body)) {
    const results = (await Promise.all(body.map((m) => handleMessage(m, env, ctx)))).filter(Boolean);
    return results.length ? rpcResponse(results) : new Response(null, { status: 202 });
  }

  const result = await handleMessage(body, env, ctx);
  return result ? rpcResponse(result) : new Response(null, { status: 202 });
}

async function handleMessage(msg, env, ctx) {
  if (!msg || msg.jsonrpc !== "2.0" || typeof msg.method !== "string") {
    // A JSON-RPC response sent by the client needs no answer; anything else is malformed.
    if (msg && msg.jsonrpc === "2.0" && ("result" in msg || "error" in msg)) return null;
    return rpcError(msg?.id ?? null, -32600, "Invalid request");
  }
  const isNotification = !("id" in msg);
  const { id, method, params } = msg;

  try {
    switch (method) {
      case "initialize": {
        const asked = params?.protocolVersion;
        const protocolVersion = SUPPORTED_VERSIONS.includes(asked) ? asked : SUPPORTED_VERSIONS[0];
        return rpcResult(id, {
          protocolVersion,
          capabilities: { tools: { listChanged: false } },
          serverInfo: SERVER_INFO,
          instructions:
            "Use esv_passage to fetch English Standard Version text for a Bible reference. " +
            "Scripture quotations are from the ESV® Bible, © 2001 by Crossway.",
        });
      }
      case "ping":
        return isNotification ? null : rpcResult(id, {});
      case "tools/list":
        return rpcResult(id, { tools: TOOLS });
      case "tools/call":
        return rpcResult(id, await callTool(params, env, ctx));
      default:
        if (isNotification) return null; // e.g. notifications/initialized
        return rpcError(id, -32601, `Method not found: ${method}`);
    }
  } catch (err) {
    if (isNotification) return null;
    if (err instanceof RpcError) return rpcError(id, err.code, err.message);
    return rpcError(id, -32603, "Internal error");
  }
}

async function callTool(params, env, ctx) {
  const name = params?.name;
  const args = params?.arguments ?? {};
  if (name !== "esv_passage") throw new RpcError(-32602, `Unknown tool: ${name}`);

  const reference = typeof args.reference === "string" ? args.reference.trim() : "";
  if (!reference) return toolError("Give a Bible reference, for example 'Romans 12:2'.");
  if (reference.length > MAX_REFERENCE_LENGTH) return toolError("That reference is too long.");
  const withNumbers = args.include_verse_numbers === true;

  let data;
  try {
    data = await fetchEsvText(reference, withNumbers, env, ctx);
  } catch (err) {
    return toolError(err.message || "The ESV service could not be reached. Try again in a moment.");
  }

  const text = (data.passages || [])
    .join("\n\n")
    .split("\n")
    .map((line) => line.replace(/[ \t]+/g, " ").trim())
    .join("\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
  if (!text) return toolError(`Couldn't find a passage for "${reference}". Check the book name and numbers.`);

  const out = {
    reference: data.canonical || reference,
    text,
    translation: "ESV",
    copyright: "Scripture quotations are from the ESV® Bible (The Holy Bible, English Standard Version®), © 2001 by Crossway.",
  };
  return {
    content: [{ type: "text", text: `${out.reference} (ESV)\n\n${out.text}` }],
    structuredContent: out,
    isError: false,
  };
}

async function fetchEsvText(reference, withNumbers, env, ctx) {
  if (!env.ESV_API_TOKEN) throw new Error("The ESV API token is not configured on the Worker.");

  const q = new URLSearchParams({
    q: reference,
    "include-passage-references": "false",
    "include-verse-numbers": String(withNumbers),
    "include-first-verse-numbers": String(withNumbers),
    "include-footnotes": "false",
    "include-footnote-body": "false",
    "include-headings": "false",
    "include-short-copyright": "false",
    "include-copyright": "false",
    "include-passage-horizontal-lines": "false",
    "include-heading-horizontal-lines": "false",
    "include-selahs": "true",
    "indent-using": "space",
    "indent-paragraphs": "0",
    "indent-poetry": "false",
    "indent-poetry-lines": "0",
    "indent-declares": "0",
    "indent-psalm-doxology": "0",
    "line-length": "0",
  });

  // Separate cache namespace from the HTML route so the two never collide.
  const cacheKey = new Request(
    `https://esv-proxy-cache.internal/text?v=${withNumbers ? 1 : 0}&q=${encodeURIComponent(reference.toLowerCase())}`
  );
  const cache = typeof caches !== "undefined" ? caches.default : null;
  if (cache) {
    const hit = await cache.match(cacheKey);
    if (hit) return hit.json();
  }

  let res;
  try {
    res = await fetch(`https://api.esv.org/v3/passage/text/?${q}`, {
      headers: { Authorization: `Token ${env.ESV_API_TOKEN}` },
    });
  } catch {
    throw new Error("The ESV service could not be reached. Try again in a moment.");
  }
  if (res.status === 429) throw new Error("The ESV API rate limit was reached. Try again later.");
  if (!res.ok) throw new Error(`The ESV API returned an error (${res.status}).`);

  const data = await res.json();
  if (cache && Array.isArray(data.passages) && data.passages.length) {
    const toStore = new Response(JSON.stringify(data), {
      headers: { "Content-Type": "application/json", "Cache-Control": `public, max-age=${CACHE_TTL_SECONDS}` },
    });
    const put = cache.put(cacheKey, toStore);
    if (ctx && ctx.waitUntil) ctx.waitUntil(put);
    else await put;
  }
  return data;
}

/* ---------- helpers ---------- */

class RpcError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}
function rpcResult(id, result) {
  return { jsonrpc: "2.0", id, result };
}
function rpcError(id, code, message) {
  return { jsonrpc: "2.0", id, error: { code, message } };
}
function rpcResponse(payload, status = 200) {
  return new Response(JSON.stringify(payload), { status, headers: JSON_HEADERS });
}
function toolError(message) {
  return { content: [{ type: "text", text: message }], isError: true };
}
function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

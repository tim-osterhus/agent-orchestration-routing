import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import net from "node:net";
import { spawn } from "node:child_process";
import { randomUUID } from "node:crypto";
import { fileURLToPath } from "node:url";
import { withAppServer, runAppServerTurn } from "../scripts/lib/codex.mjs";
import { CodexAppServerClient, BROKER_BUSY_RPC_CODE, BROKER_ENDPOINT_ENV } from "../scripts/lib/app-server.mjs";
import { createBrokerEndpoint, parseBrokerEndpoint } from "../scripts/lib/broker-endpoint.mjs";
import { runTrackedJob, serializeRelayError } from "../scripts/lib/tracked-jobs.mjs";
import { readJobFile, resolveJobFile, listJobs } from "../scripts/lib/state.mjs";

const cwd = process.cwd();
const busy = () => Object.assign(new Error("Shared Codex broker is busy."), { rpcCode: BROKER_BUSY_RPC_CODE, data: { code: BROKER_BUSY_RPC_CODE } });
const disconnected = () => Object.assign(new Error("socket lost"), { code: "ECONNRESET" });
const resumed = { thread: { id: "old-thread" }, model: "gpt-6.1-sol", reasoningEffort: "high", approvalPolicy: "never", sandbox: { type: "workspaceWrite" } };
const completed = { turn: { id: "one-turn", status: "completed", items: [] } };

function fakeClient(transport, handler) {
  let exit;
  const client = {
    transport, stderr: "", closed: 0, requests: [],
    exitPromise: new Promise(resolve => { exit = resolve; }),
    setNotificationHandler(fn) { this.notificationHandler = fn; },
    async request(method, params) { this.requests.push({ method, params }); return handler(method, params, this); },
    async close() { this.closed++; exit(); },
    disconnect(error = disconnected()) { this.exitError = error; this.exitResolved = true; exit(); }
  };
  return client;
}

function connector(...clients) {
  const calls = [];
  return { calls, connect: async (...args) => { calls.push(args); assert.ok(clients.length, "no unexpected second server"); return clients.shift(); } };
}

async function resumeThenStart(client) {
  await client.request("thread/resume", { threadId: "old-thread" });
  return client.request("turn/start", { threadId: "old-thread", input: [{ type: "text", text: "continue" }] });
}

test("busy before resume retries only that request on owning client", async () => {
  let attempts = 0, acceptedTurns = 0, callbacks = 0;
  const client = fakeClient("broker", method => {
    if (method === "thread/resume") { if (++attempts === 1) throw busy(); return resumed; }
    acceptedTurns++; return completed;
  });
  const conn = connector(client);
  await withAppServer(cwd, c => { callbacks++; return resumeThenStart(c); }, { ...conn, sleep: async () => {} });
  assert.equal(callbacks, 1); assert.equal(conn.calls.length, 1);
  assert.equal(attempts, 2); assert.equal(acceptedTurns, 1);
});

test("busy between resume and start never resumes again or uses another server", async () => {
  let turns = 0, acceptedTurns = 0;
  const client = fakeClient("broker", method => {
    if (method === "thread/resume") return resumed;
    if (++turns === 1) throw busy();
    acceptedTurns++; return completed;
  });
  const conn = connector(client);
  await withAppServer(cwd, resumeThenStart, { ...conn, sleep: async () => {}, allowFreshThreadFallback: true });
  assert.equal(client.requests.filter(r => r.method === "thread/resume").length, 1);
  assert.equal(conn.calls.length, 1); assert.equal(turns, 2); assert.equal(acceptedTurns, 1);
});

test("fresh-worker parallel dispatch survives explicit pre-creation rejection", async () => {
  const broker = fakeClient("broker", () => { throw busy(); });
  const direct = fakeClient("direct", method => method === "thread/start" ? resumed : completed);
  const conn = connector(broker, direct);
  await withAppServer(cwd, async client => {
    const response = await client.request("thread/start", {});
    return client.request("turn/start", { threadId: response.thread.id });
  }, { ...conn, allowFreshThreadFallback: true });
  assert.equal(conn.calls.length, 2); assert.deepEqual(conn.calls[1][1], { disableBroker: true });
  assert.deepEqual(broker.requests.map(r => r.method), ["thread/start"]);
  assert.deepEqual(direct.requests.map(r => r.method), ["thread/start", "turn/start"]);
});

test("indefinitely busy broker has finite total wait, no accepted turn", async () => {
  let clock = 0;
  const client = fakeClient("broker", () => { throw busy(); });
  const conn = connector(client);
  await assert.rejects(withAppServer(cwd, resumeThenStart, {
    ...conn, brokerWaitTimeoutMs: 200, now: () => clock, sleep: async ms => { clock += ms; }
  }), error => error.code === "BROKER_WAIT_TIMEOUT" && error.rpcCode === BROKER_BUSY_RPC_CODE && error.cause.rpcCode === BROKER_BUSY_RPC_CODE);
  assert.equal(clock, 200); assert.equal(conn.calls.length, 1);
  assert.equal(client.requests.filter(r => r.method === "turn/start").length, 0);
});

test("cancellation during post-resume wait sends no delayed turn", async () => {
  const abort = new AbortController();
  const reason = new Error("cancelled by owner");
  const client = fakeClient("broker", method => { if (method === "thread/resume") return resumed; throw busy(); });
  const conn = connector(client);
  await assert.rejects(withAppServer(cwd, resumeThenStart, {
    ...conn, signal: abort.signal, sleep: async (_ms, signal) => { abort.abort(reason); signal.throwIfAborted(); }
  }), error => error === reason);
  assert.equal(conn.calls.length, 1);
  assert.equal(client.requests.filter(r => r.method === "turn/start").length, 1); // rejected, never forwarded
});

test("connection exit during busy backoff sends no subsequent request", { timeout: 1000 }, async () => {
  const original = disconnected();
  const client = fakeClient("broker", method => { if (method === "thread/resume") return resumed; throw busy(); });
  const conn = connector(client);
  await assert.rejects(withAppServer(cwd, resumeThenStart, {
    ...conn, sleep: async () => client.disconnect(original)
  }), error => (error.cause === original || error.cause?.cause === original) && error.relayContext.threadId === "old-thread");
  assert.equal(conn.calls.length, 1);
  assert.deepEqual(client.requests.map(r => r.method), ["thread/resume", "turn/start"]);
});

test("busy resume then socket exit makes exactly one request and rejects promptly", { timeout: 1000 }, async () => {
  const original = disconnected();
  const client = fakeClient("broker", () => { throw busy(); });
  const conn = connector(client);
  await assert.rejects(withAppServer(cwd, resumeThenStart, {
    ...conn, sleep: async () => client.disconnect(original)
  }), error => (error.cause === original || error.cause?.cause === original) && error.relayContext.threadId === "old-thread");
  assert.equal(conn.calls.length, 1);
  assert.deepEqual(client.requests.map(r => r.method), ["thread/resume"]);
});

for (const method of ["thread/resume", "turn/start"]) {
  test(`disconnect during ${method} fails closed with identity and original cause`, async () => {
    const original = disconnected();
    const client = fakeClient("broker", requested => { if (requested === method) throw original; return resumed; });
    const conn = connector(client);
    await assert.rejects(withAppServer(cwd, resumeThenStart, conn), error => {
      assert.equal(error.cause, original); assert.equal(error.code, "ECONNRESET");
      assert.equal(error.relayContext.threadId, "old-thread");
      assert.match(error.message, /uncertain.*reconcile/i); return true;
    });
    assert.equal(conn.calls.length, 1);
    assert.equal(client.requests.filter(r => r.method === "thread/resume").length, 1);
  });
}

test("connect failure before callback does not start a direct server", async () => {
  let connections = 0, callbacks = 0;
  const original = Object.assign(new Error("missing broker socket"), { code: "ENOENT" });
  await assert.rejects(withAppServer(cwd, () => { callbacks++; }, {
    connect: async () => { connections++; throw original; }, allowFreshThreadFallback: true
  }), error => error.cause === original && error.relayContext.phase === "connecting");
  assert.equal(connections, 1); assert.equal(callbacks, 0);
});

for (const [transport, message, rpcCode] of [
  ["direct", "Shared Codex broker is busy.", BROKER_BUSY_RPC_CODE],
  ["broker", "native unrelated error", BROKER_BUSY_RPC_CODE],
  ["broker", "thread already has an active writer", -32603],
  ["broker", "authentication required", -32000],
  ["broker", "model unavailable", -32602]
]) {
  test(`${transport} ${message} passes through without replay or cleanup masking`, async () => {
    const original = Object.assign(new Error(message), { rpcCode, data: { opaque: true } });
    const client = fakeClient(transport, () => { throw original; });
    client.close = async () => { throw new Error("cleanup failed"); };
    const conn = connector(client);
    await assert.rejects(withAppServer(cwd, resumeThenStart, conn), error => error === original && error.data.opaque);
    assert.equal(conn.calls.length, 1); assert.equal(client.requests.length, 1);
  });
}

async function withConnectedFake(client, fn) {
  const original = CodexAppServerClient.connect;
  let connects = 0;
  CodexAppServerClient.connect = async (_root, options) => { connects++; assert.ok(!options?.disableBroker); return client; };
  try { return await fn(() => connects); } finally { CodexAppServerClient.connect = original; }
}

const runOptions = { resumeThreadId: "old-thread", model: "gpt-6.1-sol", effort: "high", getAvailability: () => ({ available: true }), sandbox: "workspace-write", prompt: "A harmless technical recall; use no tools." };

test("model/effort/workspace-write settings remain exact on resume and turn", async () => {
  const client = fakeClient("broker", method => method === "thread/resume" ? resumed : completed);
  await withConnectedFake(client, async () => {
    const result = await runAppServerTurn(cwd, runOptions);
    assert.equal(result.route.exact, true);
    const [resume, turn] = client.requests;
    assert.equal(resume.params.sandbox, "workspace-write");
    assert.equal(resume.params.approvalPolicy, "never");
    assert.equal(resume.params.model, "gpt-6.1-sol");
    assert.deepEqual(resume.params.config, { model_reasoning_effort: "high" });
    assert.equal(turn.params.model, "gpt-6.1-sol"); assert.equal(turn.params.effort, "high");
  });
});

test("disconnect after accepted turn rejects promptly without duplicate turn", { timeout: 2000 }, async () => {
  const client = fakeClient("broker", (method, _params, self) => {
    if (method === "thread/resume") return resumed;
    setImmediate(() => self.disconnect());
    return { turn: { id: "accepted-turn", status: "inProgress" } };
  });
  await withConnectedFake(client, async connects => {
    await assert.rejects(runAppServerTurn(cwd, runOptions), error => {
      assert.equal(error.relayContext.threadId, "old-thread"); assert.equal(error.relayContext.turnId, "accepted-turn");
      assert.match(error.message, /uncertain.*reconcile/i); return true;
    });
    assert.equal(connects(), 1); assert.deepEqual(client.requests.map(r => r.method), ["thread/resume", "turn/start"]);
  });
});

test("accepted fresh thread with busy turn start never falls back or recreates", async () => {
  let starts = 0;
  const client = fakeClient("broker", method => {
    if (method === "thread/start") return resumed;
    if (++starts === 1) throw busy();
    return completed;
  });
  const conn = connector(client);
  await withAppServer(cwd, async c => {
    const response = await c.request("thread/start", {});
    return c.request("turn/start", { threadId: response.thread.id });
  }, { ...conn, allowFreshThreadFallback: true, sleep: async () => {} });
  assert.equal(conn.calls.length, 1);
  assert.deepEqual(client.requests.map(r => r.method), ["thread/start", "turn/start", "turn/start"]);
});

test("busy budget is shared across requests, not reset after accepted resume", async () => {
  let clock = 0;
  let resumes = 0;
  const client = fakeClient("broker", method => {
    if (method === "thread/resume" && ++resumes > 1) return resumed;
    throw busy();
  });
  const conn = connector(client);
  await assert.rejects(withAppServer(cwd, resumeThenStart, {
    ...conn, now: () => clock, brokerWaitTimeoutMs: 250, sleep: async ms => { clock += ms; }
  }), error => error.code === "BROKER_WAIT_TIMEOUT" && error.relayContext.acceptedRequests === 1);
  assert.equal(clock, 250);
  assert.equal(conn.calls.length, 1);
});

test("success is retained even when cleanup rejects", async () => {
  const client = fakeClient("broker", () => completed);
  client.close = async () => { throw new Error("cleanup failed"); };
  assert.equal(await withAppServer(cwd, () => "finished", connector(client)), "finished");
});

test("read-only route stays read-only and completed turn wins over simultaneous close", async () => {
  const client = fakeClient("broker", (method, _params, self) => {
    if (method === "thread/resume") return { ...resumed, sandbox: { type: "readOnly" } };
    self.disconnect();
    return completed;
  });
  await withConnectedFake(client, async () => {
    const result = await runAppServerTurn(cwd, { ...runOptions, sandbox: "read-only" });
    assert.equal(result.status, 0);
    assert.equal(client.requests[0].params.sandbox, "read-only");
    assert.equal(result.route.observed.sandbox, "readOnly");
  });
});

test("structured identity, acceptance uncertainty and original cause persist in stored job", async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "relay-job-"));
  const prior = process.env.AGENT_ORCH_CODEX_DATA;
  process.env.AGENT_ORCH_CODEX_DATA = path.join(root, "state");
  try {
    const original = disconnected();
    const client = fakeClient("broker", method => {
      if (method === "thread/resume") return resumed;
      throw original;
    });
    const job = { id: "failure", workspaceRoot: root };
    await assert.rejects(runTrackedJob(job, () => withAppServer(root, resumeThenStart, connector(client))));
    const stored = readJobFile(resolveJobFile(root, job.id));
    assert.equal(stored.relayError.relayContext.threadId, "old-thread");
    assert.equal(stored.relayError.relayContext.acceptedRequests, 1);
    assert.equal(stored.relayError.relayContext.reconciliationRequired, true);
    assert.equal(stored.relayError.relayContext.automaticRetryAllowed, false);
    assert.equal(stored.relayError.cause.code, "ECONNRESET");
    assert.deepEqual(listJobs(root)[0].relayError, stored.relayError);
    assert.deepEqual(JSON.parse(JSON.stringify(serializeRelayError(original))).message, "socket lost");
  } finally {
    if (prior === undefined) delete process.env.AGENT_ORCH_CODEX_DATA;
    else process.env.AGENT_ORCH_CODEX_DATA = prior;
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("real CLI preserves uncertain failure in JSON, work-order result and job without a provider", { timeout: 10000 }, async () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "relay-cli-"));
  const endpoint = createBrokerEndpoint(root + randomUUID().slice(0, 8));
  const target = parseBrokerEndpoint(endpoint).path;
  const methods = [];
  const sockets = new Set();
  const server = net.createServer(socket => {
    sockets.add(socket);
    socket.on("close", () => sockets.delete(socket));
    let buffer = "";
    socket.on("data", data => {
      buffer += data;
      let newline;
      while ((newline = buffer.indexOf("\n")) >= 0) {
        const request = JSON.parse(buffer.slice(0, newline));
        buffer = buffer.slice(newline + 1);
        if (request.id === undefined) continue;
        methods.push(request.method);
        const result = request.method === "initialize" ? { userAgent: "offline-test" }
          : request.method === "thread/resume" ? resumed
          : { turn: { id: "accepted-turn", status: "inProgress" } };
        socket.write(JSON.stringify({ id: request.id, result }) + "\n");
        if (request.method === "turn/start") socket.end();
      }
    });
  });
  // Unix sockets need an existing parent; named pipes do not.
  if (process.platform !== "win32") fs.mkdirSync(path.dirname(target), { recursive: true });
  await new Promise((resolve, reject) => { server.once("error", reject); server.listen(target, resolve); });
  try {
    fs.mkdirSync(path.join(root, "bin"));
    const binary = path.join(root, "bin", process.platform === "win32" ? "codex.cmd" : "codex");
    fs.writeFileSync(binary, process.platform === "win32" ? "@echo off\r\necho offline-codex\r\nexit /b 0\r\n" : "#!/bin/sh\necho offline-codex\n");
    fs.chmodSync(binary, 0o700);
    const order = path.join(root, "order.md");
    fs.writeFileSync(order, "Do not use any tools. Offline transport regression only.");
    const companion = fileURLToPath(new URL("../scripts/codex-companion.mjs", import.meta.url));
    const env = { ...process.env, PATH: path.join(root, "bin") + path.delimiter + process.env.PATH,
      [BROKER_ENDPOINT_ENV]: endpoint, AGENT_ORCH_CODEX_DATA: path.join(root, "state") };
    const child = spawn(process.execPath, [companion, "task", "--json", "--model", "gpt-6.1-sol", "--effort", "high", "--resume-thread", "old-thread", "--prompt-file", order], { cwd: root, env });
    let stdout = "", stderr = "";
    child.stdout.on("data", b => { stdout += b; });
    child.stderr.on("data", b => { stderr += b; });
    const code = await new Promise((resolve, reject) => { child.once("error", reject); child.once("close", resolve); });
    assert.equal(code, 1, stderr);
    const payload = JSON.parse(stdout);
    const saved = JSON.parse(fs.readFileSync(order + ".result.json", "utf8"));
    assert.deepEqual(saved, payload);
    assert.equal(saved.threadId, "old-thread");
    assert.equal(saved.turnId, "accepted-turn");
    assert.equal(saved.error.relayContext.reconciliationRequired, true);
    assert.equal(saved.error.relayContext.automaticRetryAllowed, false);
    assert.equal(saved.error.relayContext.acceptedRequests, 2);
    assert.deepEqual(methods, ["initialize", "thread/resume", "turn/start"]);
    const jobFiles = fs.readdirSync(path.join(root, "state"), { recursive: true }).filter(p => String(p).endsWith(".json") && String(p).includes("jobs"));
    assert.equal(jobFiles.length, 1);
    const job = JSON.parse(fs.readFileSync(path.join(root, "state", jobFiles[0]), "utf8"));
    assert.deepEqual(job.relayError, saved.error);
  } finally {
    for (const socket of sockets) socket.destroy();
    await new Promise(resolve => server.close(resolve));
    fs.rmSync(root, { recursive: true, force: true });
    if (process.platform !== "win32") fs.rmSync(path.dirname(target), { recursive: true, force: true });
  }
});

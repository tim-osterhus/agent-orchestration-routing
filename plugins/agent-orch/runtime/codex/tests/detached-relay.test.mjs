// Offline regression for bounded relay waits: no provider, a fake broker endpoint stands in for Codex.
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import net from "node:net";
import { spawn } from "node:child_process";
import { randomUUID } from "node:crypto";
import { fileURLToPath } from "node:url";
import { BROKER_ENDPOINT_ENV } from "../scripts/lib/app-server.mjs";
import { createBrokerEndpoint, parseBrokerEndpoint } from "../scripts/lib/broker-endpoint.mjs";

const companion = fileURLToPath(new URL("../scripts/codex-companion.mjs", import.meta.url));
const usage = (total) => ({ inputTokens: total - 10, cachedInputTokens: 5, outputTokens: 10, reasoningOutputTokens: 4, totalTokens: total });

// finishAfterMs: null keeps the turn running until the test ends.
async function fakeBroker(root, { finishAfterMs }) {
  const endpoint = createBrokerEndpoint(root + randomUUID().slice(0, 8));
  const target = parseBrokerEndpoint(endpoint).path;
  const methods = [];
  const sockets = new Set();
  const timers = new Set();
  const server = net.createServer(socket => {
    sockets.add(socket);
    socket.on("close", () => sockets.delete(socket));
    socket.on("error", () => {});
    const notify = (method, params) => socket.write(JSON.stringify({ method, params }) + "\n");
    const later = (ms, fn) => { const timer = setTimeout(() => { timers.delete(timer); if (!socket.destroyed) fn(); }, ms); timers.add(timer); };
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
          : request.method === "thread/start" ? { thread: { id: "thread-1" }, model: "gpt-6.1-sol", reasoningEffort: "high", approvalPolicy: "never", sandbox: { type: "readOnly" } }
          : request.method === "turn/start" ? { turn: { id: "turn-1", status: "inProgress" } }
          : {};
        socket.write(JSON.stringify({ id: request.id, result }) + "\n");
        if (request.method !== "turn/start") continue;
        later(50, () => {
          notify("turn/started", { threadId: "thread-1", turn: { id: "turn-1", status: "inProgress" } });
          notify("thread/tokenUsage/updated", { threadId: "thread-1", turnId: "turn-1", tokenUsage: { total: usage(100), last: usage(100) } });
        });
        if (finishAfterMs === null) continue;
        later(finishAfterMs, () => {
          notify("thread/tokenUsage/updated", { threadId: "thread-1", turnId: "turn-1", tokenUsage: { total: usage(250), last: usage(150) } });
          notify("item/completed", { threadId: "thread-1", turnId: "turn-1", item: { type: "agentMessage", id: "m1", text: "Finished the bounded task.", phase: "final_answer" } });
          notify("turn/completed", { threadId: "thread-1", turn: { id: "turn-1", status: "completed", items: [] } });
        });
      }
    });
  });
  // Unix sockets need an existing parent; named pipes do not.
  if (process.platform !== "win32") fs.mkdirSync(path.dirname(target), { recursive: true });
  await new Promise((resolve, reject) => { server.once("error", reject); server.listen(target, resolve); });
  return {
    endpoint, methods,
    async close() {
      for (const timer of timers) clearTimeout(timer);
      for (const socket of sockets) socket.destroy();
      await new Promise(resolve => server.close(resolve));
      if (process.platform !== "win32") fs.rmSync(path.dirname(target), { recursive: true, force: true });
    }
  };
}

function workspace(broker) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "relay-detach-"));
  fs.mkdirSync(path.join(root, "bin"));
  const binary = path.join(root, "bin", process.platform === "win32" ? "codex.cmd" : "codex");
  fs.writeFileSync(binary, process.platform === "win32" ? "@echo off\r\necho offline-codex\r\nexit /b 0\r\n" : "#!/bin/sh\necho offline-codex\n");
  fs.chmodSync(binary, 0o700);
  const order = path.join(root, "order.md");
  fs.writeFileSync(order, "Role: research\nOffline transport regression only.");
  const env = { ...process.env, PATH: path.join(root, "bin") + path.delimiter + process.env.PATH,
    [BROKER_ENDPOINT_ENV]: broker.endpoint, AGENT_ORCH_CODEX_DATA: path.join(root, "state") };
  delete env.BASH_DEFAULT_TIMEOUT_MS;
  return { root, order, env };
}

function run(args, { root, env }) {
  const child = spawn(process.execPath, [companion, "task", ...args], { cwd: root, env });
  let stdout = "", stderr = "";
  child.stdout.on("data", b => { stdout += b; });
  child.stderr.on("data", b => { stderr += b; });
  return new Promise((resolve, reject) => {
    child.once("error", reject);
    child.once("close", code => resolve({ code, stdout, stderr, json: stdout.trim() ? JSON.parse(stdout) : null }));
  });
}

const relayArgs = order => ["--json", "--detach", "--wait-ms", "300", "--model", "gpt-6.1-sol", "--effort", "high", "--prompt-file", order];

test("detached relay returns within its wait budget, then the identical command collects one result", { timeout: 20000 }, async () => {
  const broker = await fakeBroker(os.tmpdir(), { finishAfterMs: 1500 });
  const space = workspace(broker);
  try {
    const started = Date.now();
    const first = await run(relayArgs(space.order), space);
    assert.equal(first.code, 0, first.stderr);
    assert.ok(Date.now() - started < 5000, "the first call must return near its wait budget");
    assert.equal(first.json.status, "running");
    assert.match(first.json.jobId, /^task-/);
    assert.ok(fs.existsSync(space.order + ".job.json"));

    let latest = first;
    const seen = [];
    for (let attempt = 0; attempt < 40 && latest.json?.status === "running"; attempt++) {
      latest = await run(relayArgs(space.order), space);
      seen.push(latest.json);
    }
    assert.equal(latest.code, 0, latest.stderr);
    assert.equal(latest.json.status, 0);
    assert.equal(latest.json.jobId, first.json.jobId);
    assert.equal(latest.json.rawOutput, "Finished the bounded task.");
    assert.equal(latest.json.tokenUsage.totalTokens, 250);
    assert.ok(seen.some(payload => payload.status === "running" && payload.tokenUsage?.totalTokens === 100),
      "running status reports the latest Codex token totals");
    assert.deepEqual(JSON.parse(fs.readFileSync(space.order + ".result.json", "utf8")), latest.json);

    const again = await run([...relayArgs(space.order), "--attach"], space);
    assert.deepEqual(again.json, latest.json, "attaching after completion returns the same result");
    const repeated = await run(relayArgs(space.order), space);
    assert.deepEqual(repeated.json, latest.json, "the identical command never starts a second run");
    assert.equal(broker.methods.filter(method => method === "thread/start").length, 1);
    assert.equal(broker.methods.filter(method => method === "turn/start").length, 1);
  } finally {
    await broker.close();
    fs.rmSync(space.root, { recursive: true, force: true });
  }
});

test("a changed work order starts a new job and --attach never starts one", { timeout: 20000 }, async () => {
  const broker = await fakeBroker(os.tmpdir(), { finishAfterMs: 200 });
  const space = workspace(broker);
  try {
    const orphan = path.join(space.root, "orphan.md");
    fs.writeFileSync(orphan, "Role: research\nNo job yet.");
    const refused = await run([...relayArgs(orphan), "--attach"], space);
    assert.equal(refused.code, 1);
    assert.match(refused.stderr, /No Codex job is recorded for this work order/);
    assert.equal(broker.methods.length, 0);

    let first = await run(relayArgs(space.order), space);
    while (first.json?.status === "running") first = await run(relayArgs(space.order), space);
    assert.equal(first.json.status, 0, first.stderr);
    fs.writeFileSync(space.order, "Role: research\nA different assignment in a reused file.");
    let second = await run(relayArgs(space.order), space);
    while (second.json?.status === "running") second = await run(relayArgs(space.order), space);
    assert.equal(second.json.status, 0, second.stderr);
    assert.notEqual(second.json.jobId, first.json.jobId);
    assert.equal(broker.methods.filter(method => method === "turn/start").length, 2);
  } finally {
    await broker.close();
    fs.rmSync(space.root, { recursive: true, force: true });
  }
});

test("a worker that dies mid-turn is reported as lost, with its thread, instead of waiting forever", { timeout: 20000 }, async () => {
  const broker = await fakeBroker(os.tmpdir(), { finishAfterMs: null });
  const space = workspace(broker);
  try {
    const first = await run(relayArgs(space.order), space);
    assert.equal(first.json.status, "running", first.stderr);
    const jobFile = path.join(space.root, "state");
    let job;
    for (let attempt = 0; attempt < 50; attempt++) {
      const files = fs.readdirSync(jobFile, { recursive: true }).filter(p => String(p).endsWith(`${first.json.jobId}.json`));
      job = files.length ? JSON.parse(fs.readFileSync(path.join(jobFile, files[0]), "utf8")) : null;
      if (job?.threadId) break;
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    assert.ok(job?.pid, "the running job records its worker");
    process.kill(job.pid, "SIGKILL");
    await new Promise(resolve => setTimeout(resolve, 200));
    const lost = await run(relayArgs(space.order), space);
    assert.equal(lost.code, 1);
    assert.equal(lost.json.status, 1);
    assert.equal(lost.json.threadId, "thread-1");
    assert.match(lost.json.error.message, /exited without recording a result/);
    assert.deepEqual(JSON.parse(fs.readFileSync(space.order + ".result.json", "utf8")), lost.json);
  } finally {
    await broker.close();
    fs.rmSync(space.root, { recursive: true, force: true });
  }
});

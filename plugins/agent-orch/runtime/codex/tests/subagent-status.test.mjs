// Offline regression for the plugin's subagentStatusLine command, using the transcript layout Claude Code 2.1.322 writes.
import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { displayActivity } from "../scripts/lib/relay-activity.mjs";

const script = fileURLToPath(new URL("../scripts/subagent-status.mjs", import.meta.url));

function fixture({ jobStatus = "running", tokens = 12345 } = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "relay-status-"));
  const session = "session-1";
  const transcriptPath = path.join(root, "project", `${session}.jsonl`);
  const subagents = path.join(root, "project", session, "subagents");
  fs.mkdirSync(subagents, { recursive: true });
  const order = path.join(root, "order.md");
  const jobFile = path.join(root, "job.json");
  const logFile = path.join(root, "job.log");
  fs.writeFileSync(path.join(subagents, "agent-a1.jsonl"), JSON.stringify({ type: "user",
    message: { role: "user", content: `Role: implementation\nWork order file: ${order}\n` } }) + "\n" + JSON.stringify({ type: "assistant" }) + "\n");
  fs.writeFileSync(`${order}.job.json`, JSON.stringify({ jobId: "task-1", workspaceRoot: root, fingerprint: "f", jobFile, logFile }));
  fs.writeFileSync(jobFile, JSON.stringify({ id: "task-1", status: jobStatus, tokenUsage: tokens === null ? undefined : { totalTokens: tokens } }));
  fs.writeFileSync(logFile, [
    "[2026-11-13T00:00:00.000Z] Starting Codex Task.",
    "[2026-11-13T00:00:01.000Z] Running command: npm test",
    "",
    "[2026-11-13T00:00:02.000Z] Assistant message",
    "[not a log line] body text that only looks prefixed",
    "plain body text",
    ""
  ].join("\n"));
  return { root, input: { session_id: session, transcript_path: transcriptPath, columns: 200 } };
}

function status(input) {
  const result = spawnSync(process.execPath, [script], { input: typeof input === "string" ? input : JSON.stringify(input), encoding: "utf8" });
  return { code: result.status, stderr: result.stderr, lines: result.stdout.split("\n").filter(Boolean).map(line => JSON.parse(line)) };
}

const relay = (extra = {}) => ({ id: "a1", agentType: "agent-orch:codex-sm", status: "running", description: "Fix parser", startTime: Date.now() - 65000, ...extra });

test("a running Codex relay row shows Codex activity, Codex tokens, and elapsed time", () => {
  const { root, input } = fixture();
  try {
    const result = status({ ...input, tasks: [relay(),
      { id: "a2", agentType: "agent-orch:claude-oh", status: "running" },
      { id: "a3", agentType: "agent-orch:codex-ll", status: "running" },
      { id: "a4", agentType: "agent-orch:codex-sm", status: "completed" }] });
    assert.equal(result.code, 0, result.stderr);
    assert.equal(result.lines.length, 1, "only the running Codex relay with a readable job gets a line");
    assert.equal(result.lines[0].id, "a1");
    // "[not a log line] ..." is a block body, so the last real activity is the command.
    assert.match(result.lines[0].content, /^codex-sm \(Fix parser\) · Running command: npm test · 12\.3k Codex tokens · 1m [56]s$/);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test("finished jobs, missing token totals, and narrow rows stay well formed", () => {
  const done = fixture({ jobStatus: "completed", tokens: null });
  try {
    assert.match(status({ ...done.input, tasks: [relay()] }).lines[0].content, /^codex-sm \(Fix parser\) · Codex finished · 1m [56]s$/);
    const narrow = status({ ...done.input, columns: 24, tasks: [relay()] }).lines[0].content;
    assert.equal(narrow.length, 24);
    assert.ok(narrow.endsWith("…"));
  } finally {
    fs.rmSync(done.root, { recursive: true, force: true });
  }
});

test("bad input or missing files print nothing and exit 0", () => {
  for (const input of ["not json", "{}", JSON.stringify({ session_id: "s", transcript_path: "/nonexistent/x.jsonl", tasks: [relay()] })]) {
    const result = status(input);
    assert.equal(result.code, 0);
    assert.deepEqual(result.lines, []);
  }
});

test("activity display unwraps Codex shell commands and drops turn UUIDs", () => {
  assert.equal(displayActivity("Running command: /bin/zsh -lc 'sleep 20; echo one'"), "Running command: sleep 20; echo one");
  assert.equal(displayActivity("Command completed: /bin/bash -lc 'npm test' (exit 1)"), "Command completed: npm test (exit 1)");
  assert.equal(displayActivity("Running command: /bin/zsh -lc 'python -c \"print(1)\" && ech..."), "Running command: python -c \"print(1)\" && ech...");
  assert.equal(displayActivity("Turn started (01a1d614-434b-7fb3-a0f2-41a7fceabfa8)."), "Turn started.");
  assert.equal(displayActivity("Applying 2 file change(s)."), "Applying 2 file change(s).");
});

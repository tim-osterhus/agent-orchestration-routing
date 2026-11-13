#!/usr/bin/env node
// agent-orch addition (not from openai/codex-plugin-cc). Claude Code subagentStatusLine command, supplied by the plugin's
// settings.json. It runs about every 5 seconds with the session's tasks on stdin and prints one {"id","content"} line per
// running Codex relay: Codex's latest action, its token total, and elapsed time. Rows it does not print keep Claude Code's
// default rendering, so every failure path prints nothing for that row and the script always exits 0.
import fs from "node:fs";
import path from "node:path";

import { compactTokens, formatElapsed, latestActivity, readSliceHead } from "./lib/relay-activity.mjs";

const PROMPT_HEAD_BYTES = 65536;
const WORK_ORDER = /^Work order file:[ \t]*(\S.*?)[ \t]*$/m;

// The relay's prompt is the first line of its transcript: <project>/<session>/subagents/agent-<task id>.jsonl.
function workOrderFor(input, task) {
  const transcript = path.join(path.dirname(input.transcript_path), input.session_id, "subagents", `agent-${task.id}.jsonl`);
  const head = readSliceHead(transcript, PROMPT_HEAD_BYTES);
  const newline = head.indexOf("\n");
  const content = JSON.parse(newline < 0 ? head : head.slice(0, newline)).message?.content;
  const prompt = typeof content === "string" ? content : (content ?? []).map((block) => block?.text ?? "").join("\n");
  return WORK_ORDER.exec(prompt)?.[1] ?? null;
}

function statusLine(input, task) {
  const order = workOrderFor(input, task);
  if (!order) return null;
  const marker = JSON.parse(fs.readFileSync(`${order}.job.json`, "utf8"));
  if (!marker.jobFile || !marker.logFile) return null;
  const job = JSON.parse(fs.readFileSync(marker.jobFile, "utf8"));
  const activity = job.status === "completed" ? "Codex finished"
    : job.status === "failed" || job.status === "cancelled" ? `Codex ${job.status}`
    : latestActivity(marker.logFile) ?? "Codex starting";
  const tokens = compactTokens(job.tokenUsage?.totalTokens ?? job.result?.tokenUsage?.totalTokens);
  const name = String(task.agentType).split(":").pop();
  const parts = [task.description ? `${name} (${task.description})` : name, activity,
    tokens ? `${tokens} Codex tokens` : null, Number.isFinite(task.startTime) ? formatElapsed(task.startTime) : null];
  return parts.filter(Boolean).join(" · ").replace(/\s+/g, " ");
}

function fit(text, columns) {
  if (!Number.isInteger(columns) || columns < 8 || text.length <= columns) return text;
  return `${text.slice(0, columns - 1)}…`;
}

let input;
try {
  input = JSON.parse(fs.readFileSync(0, "utf8"));
} catch {
  process.exit(0);
}
for (const task of Array.isArray(input?.tasks) ? input.tasks : []) {
  if (task?.status !== "running" || !/(^|:)codex-[a-z0-9]+$/.test(task.agentType ?? "")) continue;
  try {
    const content = statusLine(input, task);
    if (content) process.stdout.write(`${JSON.stringify({ id: task.id, content: fit(content, input.columns) })}\n`);
  } catch {
    // Missing transcript, marker, or job file: leave this row to the default rendering.
  }
}

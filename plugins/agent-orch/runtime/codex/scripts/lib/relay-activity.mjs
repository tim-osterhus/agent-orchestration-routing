// agent-orch addition (not from openai/codex-plugin-cc): what a Codex relay shows while its job runs. Kept free of heavy
// imports because the subagent status line loads it about every 5 seconds.
import fs from "node:fs";

const LOG_TAIL_BYTES = 16384;
const LOG_ENTRY = /^\[\d{4}-\d{2}-\d{2}T[\d:.]+Z\]\s*(.*)$/;
const BLOCK_TITLES = new Set(["Final output", "Assistant message", "Reasoning summary", "Review output"]);
// Display only: Codex runs commands as `/bin/zsh -lc '<command>'`, and turn and thread lines end in a UUID.
const SHELL_WRAPPED = /^(\w[\w ]*: )(?:\S*\/)?(?:ba|z)?sh -l?c '(.*?)'?( \(exit -?\d+\))?$/;
const TRAILING_UUID = / \([0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\)(?=\.?$)/;

export function displayActivity(text) {
  const wrapped = SHELL_WRAPPED.exec(text);
  return (wrapped ? `${wrapped[1]}${wrapped[2]}${wrapped[3] ?? ""}` : text).replace(TRAILING_UUID, "");
}

function readSlice(file, start, length) {
  const fd = fs.openSync(file, "r");
  try {
    const buffer = Buffer.alloc(length);
    return buffer.toString("utf8", 0, fs.readSync(fd, buffer, 0, length, start));
  } finally {
    fs.closeSync(fd);
  }
}

// Latest progress line from a job log's tail. Block bodies have no timestamp prefix, though they may start with "[".
export function latestActivity(logFile) {
  const size = fs.statSync(logFile).size;
  const start = Math.max(0, size - LOG_TAIL_BYTES);
  const lines = readSlice(logFile, start, size - start).split(/\r?\n/);
  if (start > 0) lines.shift();
  for (let index = lines.length - 1; index >= 0; index--) {
    const text = LOG_ENTRY.exec(lines[index])?.[1].trim();
    if (text && !BLOCK_TITLES.has(text) && !/^Subagent .+ (message|reasoning summary)$/.test(text)) return displayActivity(text);
  }
  return null;
}

export function compactTokens(count) {
  return Number.isFinite(count) ? (count >= 1000 ? `${(count / 1000).toFixed(1)}k` : String(count)) : null;
}

export function formatElapsed(startMs, endMs = Date.now()) {
  const seconds = Math.max(0, Math.round((endMs - startMs) / 1000));
  const [h, m, s] = [Math.floor(seconds / 3600), Math.floor(seconds / 60) % 60, seconds % 60];
  return h ? `${h}h ${m}m` : m ? `${m}m ${s}s` : `${s}s`;
}

export function readSliceHead(file, length) {
  return readSlice(file, 0, length);
}

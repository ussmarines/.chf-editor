#!/usr/bin/env node
// Narrow migration CLI for a page whose line breaks were accidentally removed.
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const value = flag => args[args.indexOf(flag) + 1];
const cli = value('--cli');
const id = value('--id');
if (!args.includes('--cli') || !args.includes('--id') || !cli || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id ?? '')) {
  throw new Error('Usage: node tools/brain-repair.mjs --cli <brain/bin/brain.mjs> --id <id> [--apply --sha256 <dry-run hash>]');
}
const lib = await import(pathToFileURL(resolve(dirname(cli), '../lib/brain.mjs')));
const raw = execFileSync(process.execPath, [cli, 'read-page', id], { encoding: 'utf8' });
const sha = createHash('sha256').update(raw).digest('hex');
if (raw.includes('\n') || raw.includes('\r')) throw new Error('Refusing: this is not a fully collapsed page');
const match = raw.match(/^---(.*?)---<!-- compiled_truth -->(.*?)## Timeline(- time: .*)$/s);
if (!match) throw new Error('Refusing: unknown legacy shape');
const keys = ['id', 'title', 'category', 'status', 'created', 'updated'];
let fm = match[1];
for (const key of keys) {
  if (fm.split(`${key}:`).length !== 2) throw new Error(`Refusing: ambiguous frontmatter key ${key}`);
  fm = fm.replace(`${key}:`, `\n${key}:`);
}
const timeline = match[3]
  .replace(/- time: (?=\d{4}-\d{2}-\d{2}T)/g, '\n- time: ')
  .replace(/  (kind|summary|source|affects): /g, '\n  $1: ');
const repaired = `---${fm}\n---\n<!-- compiled_truth -->\n${match[2]}\n## Timeline${timeline}\n`;
if (repaired.replace(/\n/g, '') !== raw) throw new Error('Refusing: migration would change existing characters');
const truth = lib.extractSection(repaired, 'compiled_truth');
const history = lib.extractSection(repaired, 'timeline');
const count = (match[3].match(/- time: \d{4}-\d{2}-\d{2}T/g) ?? []).length;
if (truth !== match[2] || lib.countTimelineEntries(history) !== count) throw new Error('Refusing: section/history verification failed');
console.log(JSON.stringify({ id, sha256: sha, preservedTimelineEntries: count, characterPreservation: true, apply: args.includes('--apply') }));
if (args.includes('--apply')) {
  if (!args.includes('--sha256') || value('--sha256') !== sha) throw new Error('Refusing: expected dry-run SHA required');
  const backupDir = resolve('outputs/brain-repair');
  mkdirSync(backupDir, { recursive: true });
  writeFileSync(resolve(backupDir, `${id}-${sha}.md`), raw, { flag: 'wx' });
  lib.writeFileAtomic(lib.pagePath(id), repaired);
  lib.reindexBrain();
  execFileSync(process.execPath, [cli, 'read-page', id], { stdio: 'ignore' });
}

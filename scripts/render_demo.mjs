#!/usr/bin/env node

import { execFileSync, spawnSync } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { createRequire } from 'node:module';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const sharp = require('sharp');

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const python = process.env.PYTHON || 'python3';
execFileSync(python, [path.join(root, 'scripts/build_standalone.py')], { stdio: 'inherit' });

const target = mkdtempSync(path.join(os.tmpdir(), 'maintainer-defense-demo-'));
const cli = path.join(root, 'dist', 'maintainer-defense-kit.py');

function run(args) {
  const result = spawnSync(python, [cli, '--target', target, ...args], { encoding: 'utf8' });
  if (result.status !== 0) throw new Error(result.stderr || `command failed: ${args.join(' ')}`);
  return result.stdout.trim();
}

const commands = [
  {
    stage: '1 / 4  DRY RUN',
    command: 'python3 maintainer-defense-kit.py --target ./demo-repo --profile observe --language en --repo acme/demo',
    output: run(['--profile', 'observe', '--language', 'en', '--repo', 'acme/demo']),
  },
  {
    stage: '2 / 4  INSTALL OBSERVE',
    command: 'python3 maintainer-defense-kit.py --target ./demo-repo --profile observe --language en --repo acme/demo --apply',
    output: run(['--profile', 'observe', '--language', 'en', '--repo', 'acme/demo', '--apply']),
  },
  {
    stage: '3 / 4  VERIFY',
    command: 'python3 maintainer-defense-kit.py --target ./demo-repo --verify',
    output: run(['--verify']),
  },
  {
    stage: '4 / 4  UNINSTALL',
    command: 'python3 maintainer-defense-kit.py --target ./demo-repo --uninstall',
    output: run(['--uninstall']),
  },
];
rmSync(target, { recursive: true, force: true });

function escapeXml(value) {
  return value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

function wrapCommand(command, width = 92) {
  const words = command.split(' ');
  const lines = [];
  let line = '$';
  for (const word of words) {
    if (`${line} ${word}`.length > width) {
      lines.push(line + ' \\');
      line = '  ' + word;
    } else {
      line += ' ' + word;
    }
  }
  lines.push(line);
  return lines;
}

function frameSvg(item, complete) {
  const commandLines = wrapCommand(item.command);
  const outputLines = complete ? item.output.split('\n') : ['Running the real standalone CLI…'];
  const lines = [...commandLines.map((text) => ({ text, color: '#F2F5F7' })), { text: '', color: '#A7B7C4' }, ...outputLines.map((text) => ({ text, color: complete ? (text.startsWith('ERROR') ? '#FF8A8A' : '#AFC2CF') : '#B8F36B' }))];
  const visible = lines.slice(0, 18);
  const rowSvg = visible.map((line, index) => `<text x="76" y="${214 + index * 25}" fill="${line.color}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="17">${escapeXml(line.text)}</text>`).join('');
  const completedStages = Number(item.stage[0]) - (complete ? 0 : 1);
  const steps = [1, 2, 3, 4].map((step) => {
    const x = 784 + (step - 1) * 100;
    const active = step <= completedStages;
    return `<circle cx="${x}" cy="94" r="10" fill="${active ? '#B8F36B' : '#263A49'}" stroke="${step === Number(item.stage[0]) ? '#B8F36B' : '#516677'}" stroke-width="2"/>`;
  }).join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
    <rect width="1280" height="720" fill="#0B1220"/>
    <rect x="38" y="34" width="1204" height="652" rx="18" fill="#101D2A" stroke="#31485A" stroke-width="2"/>
    <circle cx="72" cy="68" r="7" fill="#FF6B6B"/><circle cx="96" cy="68" r="7" fill="#F8CF5C"/><circle cx="120" cy="68" r="7" fill="#69D68A"/>
    <text x="76" y="132" fill="#B8F36B" font-family="ui-sans-serif, system-ui, sans-serif" font-size="20" font-weight="800" letter-spacing="1.5">${escapeXml(item.stage)}</text>
    <text x="76" y="164" fill="#7F96A7" font-family="ui-sans-serif, system-ui, sans-serif" font-size="15">Maintainer Defense Kit · real installer output</text>
    <path d="M784 94 H1084" stroke="#31485A" stroke-width="3"/>${steps}
    <rect x="62" y="184" width="1156" height="454" rx="12" fill="#09131D" stroke="#243847"/>
    ${rowSvg}
    <text x="76" y="666" fill="#637B8C" font-family="ui-sans-serif, system-ui, sans-serif" font-size="14">read-only default · manifest verification · safe rollback</text>
  </svg>`;
}

const frames = [];
for (const item of commands) {
  frames.push(await sharp(Buffer.from(frameSvg(item, false))).png().toBuffer());
  frames.push(await sharp(Buffer.from(frameSvg(item, true))).png().toBuffer());
}
const delay = [3000, 5500, 3000, 5500, 3000, 4500, 3000, 8000];
const output = path.join(root, 'assets', 'demo.gif');
await sharp(frames, { join: { animated: true } })
  .gif({ loop: 0, delay, colors: 96, effort: 8, dither: 0 })
  .toFile(output);

const metadata = await sharp(output, { animated: true }).metadata();
const duration = delay.reduce((sum, value) => sum + value, 0) / 1000;
if (metadata.width !== 1280 || metadata.pageHeight !== 720 || metadata.pages !== frames.length || duration < 30 || duration > 45) {
  throw new Error(`invalid demo: ${metadata.width}x${metadata.pageHeight}, ${metadata.pages} frames, ${duration}s`);
}
console.log(`RENDERED assets/demo.gif ${metadata.width}x${metadata.pageHeight}, ${metadata.pages} frames, ${duration}s`);

#!/usr/bin/env node

import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const sharp = require('sharp');

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const visuals = [
  { name: 'social-preview', width: 1280, height: 640 },
  { name: 'audit-result', width: 1280, height: 720 },
];

for (const visual of visuals) {
  const source = path.join(root, 'assets', `${visual.name}.svg`);
  const output = path.join(root, 'assets', `${visual.name}.png`);
  await sharp(source, { density: 144 })
    .resize(visual.width, visual.height)
    .png({ compressionLevel: 9, palette: true, quality: 100 })
    .toFile(output);

  const metadata = await sharp(output).metadata();
  if (metadata.width !== visual.width || metadata.height !== visual.height) {
    throw new Error(`unexpected ${visual.name} dimensions: ${metadata.width}x${metadata.height}`);
  }
  console.log(`RENDERED assets/${visual.name}.png ${metadata.width}x${metadata.height}`);
}

#!/usr/bin/env node

import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const sharp = require('sharp');

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, 'assets', 'social-preview.svg');
const output = path.join(root, 'assets', 'social-preview.png');

await sharp(source, { density: 144 })
  .resize(1280, 640)
  .png({ compressionLevel: 9, palette: true, quality: 100 })
  .toFile(output);

const metadata = await sharp(output).metadata();
if (metadata.width !== 1280 || metadata.height !== 640) {
  throw new Error(`unexpected social preview dimensions: ${metadata.width}x${metadata.height}`);
}
console.log(`RENDERED assets/social-preview.png ${metadata.width}x${metadata.height}`);

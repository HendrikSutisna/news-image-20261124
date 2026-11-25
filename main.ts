// news-image-20261124 entry v3 (Node 22, standard library only): the image
// is the entry.png beside this file, and the program copies it to
// /output/entry.png, then verifies the copy is byte-identical to the source.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const sourcePath = fileURLToPath(new URL('./entry.png', import.meta.url));
const targetPath = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');

copyFileSync(sourcePath, targetPath);

const sha256 = (path: string): string =>
  createHash('sha256').update(readFileSync(path)).digest('hex');

if (sha256(sourcePath) !== sha256(targetPath)) {
  throw new Error('entry.png copy is not byte-identical');
}

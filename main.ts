import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Copy the pre-rendered newspaper image to the harness output directory,
// then verify the copy before reporting success. A truncated or partial
// copy must fail loudly instead of silently scoring a corrupt image.
const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// Verify: the output must exist and be byte-identical to the source.
if (!existsSync(target)) {
  console.error(`error: output file missing after copy: ${target}`);
  process.exit(1);
}
const sourceBytes = readFileSync(source);
const targetBytes = readFileSync(target);
if (sourceBytes.length !== targetBytes.length || !sourceBytes.equals(targetBytes)) {
  console.error(
    `error: output verification failed: ${target} (${targetBytes.length} bytes) ` +
      `does not match ${source} (${sourceBytes.length} bytes)`,
  );
  process.exit(1);
}
console.log(`wrote ${target} (${targetBytes.length} bytes, verified)`);

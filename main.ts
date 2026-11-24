// World News — 24 November 2026 (make.fun news-image-20261124 entry).
// The front page is drawn in the repository as entry.png; this program
// copies it to the grader's output directory, deterministically.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The program runs with no network and writes exactly the bytes it
// ships: the same file on every run, so the two grading runs match.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(
  join(dirname(fileURLToPath(import.meta.url)), "entry.png"),
  join(outDir, "entry.png"),
);

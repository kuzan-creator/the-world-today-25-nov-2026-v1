// main.ts -- entrypoint for "The World in One Day" (25 Nov 2026, v1).
//
// Copies the included entry.png (1024x1024) to the output directory.
// No dependencies, no network, deterministic: the output bytes are
// always identical to the included file.
//
// Output directory, first match wins:
//   MAKEFUN_OUTPUT_DIR, OUTPUT_DIR, then /output
// Run:  node main.ts

import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function fail(message) {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function main() {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, "entry.png");
  if (!existsSync(source)) {
    fail(`entry.png not found next to main.ts (${source})`);
  }

  const bytes = readFileSync(source);
  if (bytes.length < PNG_MAGIC.length || !bytes.subarray(0, 8).equals(PNG_MAGIC)) {
    fail("entry.png does not start with the PNG magic bytes");
  }

  const outDir =
    process.env.MAKEFUN_OUTPUT_DIR || process.env.OUTPUT_DIR || "/output";
  mkdirSync(outDir, { recursive: true });
  const target = join(outDir, "entry.png");
  writeFileSync(target, bytes);

  const written = readFileSync(target);
  if (!written.equals(bytes)) {
    fail(`${target} differs from entry.png after copying`);
  }
  if (!written.subarray(0, 8).equals(PNG_MAGIC)) {
    fail(`${target} does not start with the PNG magic bytes`);
  }

  console.log(`entry.png -> ${target}`);
  console.log(`sha256 ${sha256(written)}`);
  console.log(`bytes ${written.length}`);
}

main();

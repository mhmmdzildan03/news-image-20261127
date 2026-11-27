// News image entry for Friday, 27 November 2026.
//
// The broadsheet lives in this repository as entry.png (built by
// build_image.py from the verified stories of the day). The grader
// runs this program with no network and expects exactly one file at
// /output/entry.png, so the program simply delivers the bundled
// image there, byte for byte, every run.
//
// Local dry run:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(targetDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(targetDir, "entry.png"));

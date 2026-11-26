// The World Today — Thursday 26 November 2026 (news-image-20261126).
//
// Node 22, standard library only, no network. The entry image is the
// entry.png beside this file (drawn at build time by gen_image.py); this
// program validates it — PNG signature, 1024x1024 header, at most 1 MiB —
// then copies it to /output/entry.png and verifies the copy hashes exactly
// like the source. Two runs write identical bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const SRC = new URL('./entry.png', import.meta.url);
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const DEST = join(OUT_DIR, 'entry.png');

const bytes = readFileSync(SRC);

// Whole PNG: signature + IHDR header declaring 1024x1024, every chunk
// with its CRC intact, and the IEND end marker as the last 12 bytes.
if (bytes.length < 33 || bytes.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') {
  throw new Error('entry.png is not a PNG');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}
const CRC_TABLE: number[] = Array.from({ length: 256 }, (_, n) => {
  let c = n;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  return c >>> 0;
});
const crc32 = (buf: Buffer): number => {
  let c = 0xffffffff;
  for (const b of buf) c = CRC_TABLE[(c ^ b) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
};
let off = 8;
let sawIEND = false;
while (off + 12 <= bytes.length) {
  const len = bytes.readUInt32BE(off);
  const type = bytes.toString('latin1', off + 4, off + 8);
  if (off + 12 + len > bytes.length) throw new Error(`PNG chunk ${type} is truncated`);
  const stored = bytes.readUInt32BE(off + 8 + len);
  if (crc32(bytes.subarray(off + 4, off + 8 + len)) !== stored) {
    throw new Error(`PNG chunk ${type} fails its CRC`);
  }
  off += 12 + len;
  if (type === 'IEND') { sawIEND = true; break; }
}
if (!sawIEND || off !== bytes.length) {
  throw new Error('entry.png does not end cleanly at its IEND chunk');
}

mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SRC, DEST);

// The destination must be a plain file of exactly the source's size:
// a symlink or a stale longer file would break the two-runs-same-bytes rule.
const destStat = statSync(DEST);
if (!destStat.isFile() || destStat.size !== bytes.length) {
  throw new Error('output entry.png is not an exact copy of the source');
}

// The copy must hash exactly like the source: both runs, same bytes.
const digest = (p: string) => createHash('sha256').update(readFileSync(p)).digest('hex');
if (digest(DEST) !== digest(SRC)) {
  throw new Error('copied entry.png does not match the source');
}
console.log(`The World Today — Thursday, 26 November 2026`);
console.log(`wrote ${DEST} (${destStat.size} bytes, sha256 ${digest(DEST).slice(0, 16)}…)`);

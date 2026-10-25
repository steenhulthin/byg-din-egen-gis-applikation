// Runs Checkpoint A against one App file: npm run checkpoint-a -- path/to/index.html
import { spawnSync } from 'node:child_process';
import { statSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const app = process.argv[2];
if (!app || !statSync(app, { throwIfNoEntry: false })?.isFile()) {
  console.error('Usage: npm run checkpoint-a -- path/to/index.html');
  process.exit(2);
}

const config = fileURLToPath(new URL('playwright.config.mjs', import.meta.url));
const result = spawnSync('npx', ['playwright', 'test', '--config', config], {
  stdio: 'inherit',
  env: { ...process.env, CHECKPOINT_APP: resolve(app) },
  shell: process.platform === 'win32',
});
process.exit(result.status ?? 1);

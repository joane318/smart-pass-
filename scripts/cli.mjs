import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
const cli = fileURLToPath(new URL('../node_modules/wrangler/bin/wrangler.js',import.meta.url));
export function wrangler(args, capture = false) {
  const result = spawnSync(process.execPath, [cli, ...args], {
    encoding:'utf8', stdio:capture ? ['inherit','pipe','inherit'] : 'inherit',
    env:{...process.env,WRANGLER_SEND_METRICS:'false'}
  });
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error(`O comando wrangler ${args.slice(0,2).join(' ')} falhou. Resolva o erro acima antes de continuar.`);
  return capture ? result.stdout : '';
}

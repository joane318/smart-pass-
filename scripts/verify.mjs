import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {wrangler} from './cli.mjs';
const sha=data=>createHash('sha256').update(data).digest('hex');
const manifest=JSON.parse(readFileSync('.cloudflare-migracao/conferencia.json','utf8'));
const quote=name=>{if(!/^[A-Za-z_][A-Za-z0-9_]*$/.test(name))throw new Error('Identificador inválido na conferência.');return `"${name}"`;};
export function verifyPackage() {
  if(sha(readFileSync('.cloudflare-migracao/db-original.sqlite3'))!==manifest.source_sha256)throw new Error('A cópia do banco original foi alterada.');
  if(sha(readFileSync('.cloudflare-migracao/dados-originais.sql'))!==manifest.migration_sha256)throw new Error('O arquivo da migração foi alterado.');
}
export function query(sql,remote=true) {
  const raw=wrangler(['d1','execute','smart_pass_db',remote?'--remote':'--local','--command',sql,'--json'],true);
  const response=JSON.parse(raw);
  if(!Array.isArray(response)||!response.every(r=>r.success!==false))throw new Error('Falha ao consultar o D1.');
  return response[0].results;
}
export function verifyDatabase(remote=true) {
  for(const t of manifest.tables) {
    const rows=query(`SELECT ${t.columns.map(quote).join(',')} FROM ${quote(t.name)} ORDER BY ${t.order.map(quote).join(',')}`,remote);
    const data=rows.map(row=>t.columns.map(c=>row[c]));
    if(data.length!==t.count||sha(JSON.stringify(data))!==t.sha256)throw new Error(`Divergência na tabela ${t.name}. Publicação interrompida; banco original preservado.`);
    console.log(`${t.name}: ${data.length} registros, conteúdo conferido.`);
  }
  if(query('PRAGMA foreign_key_check',remote).length)throw new Error('Foram encontradas relações inválidas.');
  console.log('Conferência concluída: todos os dados originais correspondem ao D1.');
}
if(process.argv[1]?.endsWith('verify.mjs')) {
  try{verifyPackage();verifyDatabase(!process.argv.includes('--local'));}
  catch(error){console.error(error.message);process.exitCode=1;}
}

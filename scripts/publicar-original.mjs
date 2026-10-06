import {readFileSync,writeFileSync} from 'node:fs';
import {randomBytes} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {wrangler} from './cli.mjs';
import {verifyPackage,verifyDatabase,query} from './verify.mjs';

try {
  verifyPackage();
  const config=JSON.parse(readFileSync('wrangler.jsonc','utf8'));
  if(config.name!=='smart-pass'||config.main!=='.cloudflare-build/entry.py')throw new Error('A configuração não corresponde ao Django original.');
  wrangler(['login']);wrangler(['whoami']);
  const list=()=>JSON.parse(wrangler(['d1','list','--json'],true));
  const binding=config.d1_databases[0];
  let dbs=list();
  if(binding.database_id==='00000000-0000-0000-0000-000000000000') {
    let db=dbs.find(d=>d.name===binding.database_name);
    if(!db){wrangler(['d1','create',binding.database_name]);db=list().find(d=>d.name===binding.database_name);}
    if(!db)throw new Error('D1 não identificado.');
    binding.database_id=db.uuid;
    writeFileSync('wrangler.jsonc',JSON.stringify(config,null,2)+'\n');
  }else if(!dbs.some(d=>d.uuid===binding.database_id&&d.name===binding.database_name))throw new Error('O banco configurado não pertence à conta conectada.');
  const tables=query("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_cf_%' AND name!='d1_migrations'");
  if(tables.length){
    console.log('O D1 já contém dados. Apenas verificando, sem reimportar.');
    verifyDatabase();
  }else {
    console.log('Importando os dados originais para o D1 vazio.');
    wrangler(['d1','execute','smart_pass_db','--remote','--file','.cloudflare-migracao/dados-originais.sql']);
    verifyDatabase();
  }
  const secrets=JSON.parse(wrangler(['secret','list'],true));
  if(!secrets.some(s=>s.name==='DJANGO_SECRET_KEY')) {
    console.log('Criando a chave interna do Django. Se pedir criar o Worker, responda y.');
    const cli=fileURLToPath(new URL('../node_modules/wrangler/bin/wrangler.js',import.meta.url));
    const result=spawnSync(process.execPath,[cli,'secret','put','DJANGO_SECRET_KEY'],{
      input:randomBytes(64).toString('base64url')+'\n',encoding:'utf8',stdio:['pipe','inherit','inherit'],
      env:{...process.env,WRANGLER_SEND_METRICS:'false'}
    });
    if(result.error||result.status!==0)throw new Error('Não foi possível salvar a chave interna do Django.');
  }
  const deployed=spawnSync('uv',['run','pywrangler','deploy'],{stdio:'inherit',env:{...process.env,WRANGLER_SEND_METRICS:'false'}});
  if(deployed.error||deployed.status!==0)throw new Error('Publicação Python não concluída. Envie o erro acima.');
  console.log('Django original publicado. /admin/ mantém os usuários e senhas originais.');
}catch(error){console.error('Publicação interrompida:',error.message);process.exitCode=1;}

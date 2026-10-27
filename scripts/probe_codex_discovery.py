import subprocess,json,select,time
from pathlib import Path
p=subprocess.Popen(['codex','app-server','--stdio'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=open('work/app-server.stderr','w'),text=True,bufsize=1)
def call(i,m,params):
 p.stdin.write(json.dumps({'id':i,'method':m,'params':params})+'\n'); p.stdin.flush()
 deadline=time.monotonic()+45
 while time.monotonic()<deadline:
  if not select.select([p.stdout],[],[],1)[0]: continue
  line=p.stdout.readline()
  if not line: raise RuntimeError('app-server exited')
  v=json.loads(line)
  if v.get('id')==i:
   if 'error' in v: raise RuntimeError(v['error'])
   return v['result']
 raise TimeoutError(m)
try:
 call(1,'initialize',{'clientInfo':{'name':'skill-registration-check','version':'1.0.0'},'capabilities':{'experimentalApi':True}})
 result=call(2,'skills/list',{'cwds':[str(Path.cwd())],'forceReload':True})
 Path('work/discovery.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps(result,ensure_ascii=False,indent=2))
finally:
 p.terminate()
 try: p.wait(timeout=2)
 except subprocess.TimeoutExpired:
  p.kill(); p.wait(timeout=2)

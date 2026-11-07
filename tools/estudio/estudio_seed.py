import json,sys,os
R=os.path.expanduser(sys.argv[2]) if len(sys.argv)>2 else os.path.expanduser('~/reels/2026-11-04-reel'); ids=json.load(open(os.path.expanduser('~/reels/estudio_ids.json')))
A=json.load(open(R+'/edit.json')); C=json.load(open(R+'/var_C/edit.json')) if os.path.exists(R+'/var_C/edit.json') else A
names={'p1':'paso 1','p2':'paso 2','p3':'paso 3','launch':'lanzamiento','stamp':'100% gratis','nuevo':'nuevo','mismotexto':'mismo texto','no_cosas':'no cosas','no_logo':'no logo','no_perfil':'no perfil','nobajar':'no bajar','tucriterio':'tu criterio','herobadge':'superheroína badge','heroemo':'superheroína','noapp':'no app','lupa':'lupa','ojo':'ojo','bulb':'idea','gift':'regalo','chat':'chat','sparkles':'brillos','memo':'nota','mail':'mail','eyes':'ojos','ghost':'fantasma','phone':'móvil','point':'señalar','scissors':'tijeras','film':'cine','heart':'corazón','listo':'listo','descarga':'descarga','semana':'semana','belleza':'belleza','hogar':'hogar','gratis':'gratis','claude':'claude'}
kind={'title':'Título','tag':'Rótulo','sticker':'Sticker','card':'Tarjeta','page':'Pantalla de color','cta':'Llamada a la acción'}
def key(c): return (c['type'],c.get('src') or c.get('text') or c.get('title') or c.get('bg'))
cards=[]
for i,c in enumerate(A['cards']):
    d={'id':f'c{i}','kind':kind.get(c['type'],c['type']),'start':round(c['start'],2),'end':round(c['end'],2)}
    if c['type'] in('title','tag','cta'): d['text']=c['text']; d['label']=c['text']
    elif c['type']=='sticker': n=os.path.basename(c['src'])[:-4]; d['label']='sticker «'+names.get(n,n)+'»'
    elif c['type']=='card': d['label']=c['title']+': '+' · '.join(c['rows'])
    else: d['label']='fondo de color (lanzamiento)'
    cards.append(d)
ckeys={key(c) for c in C['cards']}
cids=[f'c{i}' for i,c in enumerate(A['cards']) if key(c) in ckeys]
caps=[]
for g in A['captions']:
    for w in g['words']: caps.append({'t':round(w['t'],2),'text':w['text'],'accent':bool(w.get('accent'))})
V=json.loads(sys.argv[1])
sounds=[('pop','pop','aparición rápida'),('whoosh','whoosh','transición'),('swish','swish','transición suave'),('snap','chasquido','corte seco'),('chime','campanita','idea / acierto'),('ding','ding','notificación'),('tada','ta-dá','revelación, lanzamiento'),('riser','subida','tensión antes de revelar'),('boom','boom','golpe de impacto'),('boing','boing','momento gracioso'),('click','clic','tocar pantalla'),('camara','cámara','foto / captura'),('typing','teclado','escribir')]
META=json.loads(sys.argv[3]) if len(sys.argv)>3 else {'reelId':'2026-11-04-reel','title':'¿No sabes qué decirle a una marca?','subtitle':'Reel de lanzamiento · Evaluador de Perfiles UGC · CTA «COMUNIDAD»'}
doc={**META,
 'versions':V,'cards':cards,'captions':caps,
 'stickers':[{'id':k,'name':names.get(k,k),'img':v} for k,v in ids['st'].items()],
 'sounds':[{'id':k,'name':n,'desc':d,'audio':ids['sfx'][k]} for k,n,d in sounds]}
for v in doc['versions']:
    if v['id']=='C' and C is not A: v['cardIds']=cids
s=json.dumps(doc,ensure_ascii=False); print(len(s),'bytes; cards',len(cards),'C cards',len(cids),'caps',len(caps),file=sys.stderr)
open(os.path.expanduser('~/reels/estudio_current.json'),'w').write(s)

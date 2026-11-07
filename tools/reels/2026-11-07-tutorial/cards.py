import json,re,sys
V=sys.argv[1]
e=json.load(open('edit.json'))
cam=[(0,13.88),(27.81,37.24)]
e['punch']=[p for p in e['punch'] if any(a<=(p if not isinstance(p,list) else p[0])<b-0.4 for a,b in cam)]
acc=['ugc','sencillo','editar','termina','producto','resultado','utilizamos','instagram','sobran','complicadísima','entienda','montarlos','comentarios']
seen=set()
for c in e['captions']:
    for x in c['words']:
        k=re.sub(r'[^\wáéíóúñ]','',x['text'].lower())
        if k in acc and k not in seen: x['accent']=True; seen.add(k)
        else: x['accent']=False
S=lambda f:f"stickers/{f}.png"
cards=[
 {"type":"title","start":0.0,"end":2.72,"text":"edita tus / clips UGC","y":700},
 {"type":"sticker","start":3.9,"end":6.3,"src":S("phone"),"x":920,"y":560,"size":190,"rotate":10},
 {"type":"sticker","start":4.3,"end":6.3,"src":S("film"),"x":160,"y":600,"size":200,"rotate":-10},
 {"type":"tag","start":6.8,"end":9.4,"text":"antes de editar: el orden","y":820},
 {"type":"card","start":9.44,"end":13.88,"title":"piensa en","rows":["qué se ve primero","qué viene después","cómo termina"],"row_times":[10.16,11.68,12.8],"y":740},
 {"type":"tag","start":13.88,"end":16.36,"text":"ejemplo: demo de producto","y":170},
 {"type":"sticker","start":16.36,"end":18.55,"src":S("p1"),"x":900,"y":420,"size":210,"rotate":-8},
 {"type":"tag","start":16.36,"end":18.55,"text":"empieza por el resultado","y":170},
 {"type":"sticker","start":18.55,"end":20.07,"src":S("p2"),"x":900,"y":420,"size":210,"rotate":-8},
 {"type":"tag","start":18.55,"end":20.07,"text":"luego cómo se usa","y":170},
 {"type":"sticker","start":20.07,"end":21.73,"src":S("p3"),"x":900,"y":420,"size":210,"rotate":-8},
 {"type":"tag","start":20.07,"end":21.73,"text":"cierra con el producto","y":170},
 {"type":"tag","start":21.73,"end":23.18,"text":"abre el editor de Instagram","y":300},
 {"type":"tag","start":23.18,"end":24.70,"text":"elige tus clips","y":300},
 {"type":"sticker","start":23.5,"end":24.70,"src":S("point"),"x":930,"y":1500,"size":170,"rotate":0},
 {"type":"tag","start":24.70,"end":26.38,"text":"recorta lo que sobra","y":300},
 {"type":"sticker","start":24.9,"end":26.38,"src":S("scissors"),"x":900,"y":760,"size":220,"rotate":-14},
 {"type":"tag","start":26.38,"end":27.81,"text":"colócalos en orden","y":300},
 {"type":"sticker","start":26.5,"end":27.81,"src":S("sparkles"),"x":900,"y":760,"size":170,"rotate":10},
 {"type":"sticker","start":27.9,"end":31.9,"src":S("bulb"),"x":920,"y":560,"size":190,"rotate":8},
 {"type":"tag","start":30.94,"end":32.3,"text":"primero, que se entienda","y":820},
 {"type":"sticker","start":32.4,"end":35.8,"src":S("chat"),"x":920,"y":560,"size":180,"rotate":8},
 {"type":"tag","start":33.6,"end":35.8,"text":"¿grabar o montar?","y":820},
 {"type":"cta","start":35.82,"end":37.24,"text":"dímelo en COMENTARIOS"}]
e['cards']=cards
json.dump(e,open('edit.json','w'),ensure_ascii=False,indent=1)
print(len(e['punch']),'punches',sorted(seen))

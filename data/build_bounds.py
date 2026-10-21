import json
c=json.load(open('data/canton.json'))
def rings(rel):
    segs=[[(round(p['lon'],5),round(p['lat'],5)) for p in m['geometry']] for m in rel['members'] if m['type']=='way' and m.get('role') in ('outer','') and 'geometry' in m]
    out=[]
    while segs:
        ring=segs.pop(0)
        changed=True
        while ring[0]!=ring[-1] and changed:
            changed=False
            for i,s in enumerate(segs):
                if s[0]==ring[-1]: ring+=s[1:]
                elif s[-1]==ring[-1]: ring+=s[::-1][1:]
                elif s[-1]==ring[0]: ring=s[:-1]+ring
                elif s[0]==ring[0]: ring=s[::-1][:-1]+ring
                else: continue
                segs.pop(i); changed=True; break
        out.append(ring)
    return out
feats=[]
for e in c['elements']:
    rs=rings(e)
    # simplify: keep every point (fine size) but drop near duplicates
    feats.append({"type":"Feature","properties":{"name":e['tags']['name'],"level":e['tags']['admin_level']},
      "geometry":{"type":"MultiPolygon","coordinates":[[r] for r in rs]}})
    print(e['tags']['name'],len(rs),[len(r) for r in rs],[r[0]==r[-1] for r in rs])
json.dump({"type":"FeatureCollection","features":feats},open('data/bounds.geojson','w'),separators=(',',':'))

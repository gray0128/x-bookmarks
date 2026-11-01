#!/usr/bin/env python3
"""Build index.html from data/bookmarks.json + data/classify.json.
Unclassified posts go to type '待分类'. Run: python3 build.py"""
import json,datetime,collections,sys
JST=datetime.timezone(datetime.timedelta(hours=9))
D=json.load(open('data/bookmarks.json'));C=json.load(open('data/classify.json'))
P,inc,U=D['posts'],D['includes'],D['users']
def ft(t):
    n=t.get('note_tweet') or {}
    s=n.get('text') or t.get('text','')
    for u in (n.get('entities') or t.get('entities') or {}).get('urls',[]):
        if u.get('url') and u.get('expanded_url'): s=s.replace(u['url'],u['expanded_url'])
    return s
def dt(s): return datetime.datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(JST).strftime('%Y-%m-%d %H:%M')
cards=[];miss=0
for p in P:
    c=C.get(p['id']) or {'type':'待分类','topic':'待分类'}
    if p['id'] not in C: miss+=1
    u=U.get(p['author_id'],{});m=p.get('public_metrics',{})
    qs=[]
    for r in p.get('referenced_tweets',[]):
        t=inc.get(r['id'])
        if t:
            qu=U.get(t.get('author_id'),{})
            qs.append({'type':r['type'],'text':ft(t),'who':'@'+qu.get('username','?'),'url':f"https://x.com/i/status/{t['id']}"})
    cards.append({'ty':c['type'],'tp':c['topic'],'name':u.get('name',''),'handle':u.get('username',''),'date':dt(p['created_at']),'ts':p['created_at'],
      'text':ft(p),'quotes':qs,'likes':m.get('like_count',0),'bm':m.get('bookmark_count',0),
      'url':p.get('url') or f"https://x.com/{u.get('username','i')}/status/{p['id']}"})
now=datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M')
data=json.dumps(cards,ensure_ascii=False).replace('</','<\\/')
html=open('template.html').read().replace('__DATA__',data).replace('__UPDATED__',now)
open('index.html','w').write(html)
cnt=collections.Counter(c['ty'] for c in cards)
print('total',len(cards),'unclassified',miss)
for t,n in cnt.most_common():
    print(f'{t} {n}: '+', '.join(f'{k} {v}' for k,v in collections.Counter(c["tp"] for c in cards if c["ty"]==t).most_common()))

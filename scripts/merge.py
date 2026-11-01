"""Merge X API bookmark page files into data/bookmarks.json (dedupe by id).
Usage: python3 scripts/merge.py page1.json page2.json ...
Each page file = raw get_users_bookmarks response {data, includes:{posts,users}, meta}.
Newly seen ids get 'bookmarked_seen' = now (Asia/Tokyo) and are prepended (newest first)."""
import json,sys,os,datetime
F='data/bookmarks.json'
db=json.load(open(F)) if os.path.exists(F) else {'posts':[],'includes':{},'users':{}}
have={p['id'] for p in db['posts']}
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec='seconds')
new=[]
for f in sys.argv[1:]:
    d=json.load(open(f))
    if 'posts' in d and 'data' not in d:  # legacy raw.json format
        posts=d['posts'];inc={k:v for k,v in (d.get('inc') or {}).items()};users=d.get('users',{})
    else:
        posts=d.get('data',[]);I=d.get('includes',{})
        inc={p['id']:p for p in I.get('posts',[])};users={u['id']:u for u in I.get('users',[])}
    db['includes'].update(inc);db['users'].update(users)
    for p in posts:
        if p['id'] in have: continue
        have.add(p['id']);p['bookmarked_seen']=now;new.append(p)
db['posts']=new+db['posts']
json.dump(db,open(F,'w'),ensure_ascii=False,indent=1)
print('new',len(new),'total',len(db['posts']))
for p in new: print('NEW',p['id'])

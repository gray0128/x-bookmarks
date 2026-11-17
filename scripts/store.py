"""Load/save bookmarks, splitting into GitHub Contents API-safe part files (<600KB)."""
import json, os, glob

PART_GLOB = "data/bookmarks-part*.json"
COMBINED = "data/bookmarks.json"
MAX_PART = 600_000

def load_bookmarks():
    parts = sorted(glob.glob(PART_GLOB))
    if parts:
        db = {"posts": [], "includes": {}, "users": {}}
        for f in parts:
            d = json.load(open(f))
            db["posts"].extend(d.get("posts") or [])
            db["includes"].update(d.get("includes") or {})
            db["users"].update(d.get("users") or {})
        return db
    if os.path.exists(COMBINED):
        return json.load(open(COMBINED))
    return {"posts": [], "includes": {}, "users": {}}

def _dump(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

def save_bookmarks(db, write_combined=True):
    if write_combined:
        os.makedirs("data", exist_ok=True)
        json.dump(db, open(COMBINED, "w"), ensure_ascii=False, indent=1)
    for f in glob.glob(PART_GLOB):
        os.remove(f)
    includes = db.get("includes") or {}
    users = db.get("users") or {}
    posts = db.get("posts") or []
    meta = {"posts": [], "includes": includes, "users": users}
    meta_size = len(_dump(meta).encode())
    current, with_meta, size = [], True, meta_size
    empty_overhead = len(_dump({"posts": []}).encode())
    parts = []
    for p in posts:
        extra = len(_dump(p).encode()) + 1
        if current and size + extra > MAX_PART:
            obj = {"posts": current}
            if with_meta:
                obj["includes"] = includes
                obj["users"] = users
            parts.append(obj)
            current, with_meta, size = [p], False, empty_overhead + extra
        else:
            current.append(p)
            size += extra
    if current or not parts:
        obj = {"posts": current}
        if with_meta:
            obj["includes"] = includes
            obj["users"] = users
        parts.append(obj)
    written = []
    for i, obj in enumerate(parts, 1):
        path = f"data/bookmarks-part{i:02d}.json"
        open(path, "w").write(_dump(obj))
        print("wrote", path, "bytes", os.path.getsize(path), "posts", len(obj["posts"]))
        written.append(path)
    return written

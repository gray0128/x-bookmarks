# X 收藏导航

我的 X（@IfiflyL95010）收藏，按「内容类型 → 主题」两级整理。网站：https://gray0128.github.io/x-bookmarks/

## 文件
- `data/bookmarks.json`：收藏原始数据（`posts` 新的在前、`includes` 被引用帖、`users` 作者），按帖子 id 去重
- `data/classify.json`：帖子 id → `{type, topic}`。类型/主题是动态的，可随时新增
- `scripts/merge.py`：把 X API `get_users_bookmarks` 的分页响应合并进 bookmarks.json，打印新增 id（`NEW <id>`）
- `template.html` + `build.py`：生成单页 `index.html`（类型标签、主题分组、搜索、复制按钮、深浅色）

## 每日更新流程
1. 用 X 工具 `get_users_bookmarks`（id=1721765420464783360, max_results=100，post.fields=created_at,public_metrics,author_id,lang,conversation_id,entities,note_tweet,referenced_tweets，expansions=author_id,referenced_tweets.id，user.fields=name,username,description）拉取，把每页响应存为 JSON 文件；遇到已存在的 id 即可停止翻页
2. `python3 scripts/merge.py page1.json [page2.json ...]`
3. 为每个 `NEW` id 在 `data/classify.json` 加 `{"type": ..., "topic": ...}`（优先复用已有类型/主题；需要时新增）。未分类的会显示在「待分类」
4. `python3 build.py`（输出各类型/主题计数和未分类数）
5. `git add -A && git commit -m "update $(date +%F)" && git push`

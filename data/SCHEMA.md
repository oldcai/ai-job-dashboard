# Job Database Schema

## `data/jobs.json`

本地 JSON 数据库，追踪所有抓取过的职位。

### 结构

```json
{
  "meta": {
    "version": 1,
    "lastUpdated": "2026-02-11T10:00:00+11:00",
    "totalJobs": 25,
    "schema": "v1"
  },
  "jobs": {
    "<job_id>": {
      "id": "linkedin-3847291056",
      "title": "AI Engineer",
      "company": "Optiver",
      "location": "Sydney",
      "salaryMin": 180,
      "salaryMax": 250,
      "salaryCurrency": "AUD",
      "salaryRaw": "$180K-$250K+",
      "url": "https://www.linkedin.com/jobs/view/3847291056",
      "source": "linkedin",
      "postedDate": "2026-02-06",
      "firstSeen": "2026-02-11T10:00:00+11:00",
      "lastSeen": "2026-02-11T10:00:00+11:00",
      "status": "active",
      "scores": {
        "aiRelevance": 5,
        "sponsorship": 5,
        "companyFundamentals": 5,
        "salaryMatch": 5,
        "total": 5.0
      },
      "visaPathway": "482→186",
      "tags": ["new", "sponsor", "ai"],
      "description": "Cached job description text...",
      "descriptionFetchedAt": "2026-02-11T10:00:00+11:00",
      "notes": ""
    }
  }
}
```

### Job ID 生成规则

- LinkedIn: `linkedin-<job_view_id>` (从 URL 提取)
- Seek: `seek-<job_id>` (从 URL 提取)
- UOW: `uow-<slug>` (从 URL 路径提取)
- 其他: `other-<md5(url)>`

### Status 状态

- `active` — 最近一次抓取仍存在
- `closed` — 连续 3 次抓取未出现，标记为已关闭
- `applied` — 用户已申请（手动标记）
- `rejected` — 用户已被拒（手动标记）
- `interviewing` — 面试中（手动标记）

### 抓取逻辑

1. **每次抓取时**：
   - 对搜索结果中的每个职位，生成 `job_id`
   - 如果 `job_id` 已存在于 `jobs` 中：
     - 更新 `lastSeen`
     - 保持 `firstSeen` 不变
     - 如果状态是 `closed`，改回 `active`
     - **不重新抓取 detail 页面**（除非 `description` 为空）
   - 如果 `job_id` 不存在：
     - 新建记录
     - 设置 `firstSeen` = 当前时间
     - 抓取 detail 页面，缓存 `description`
     - 标记 `tags` 包含 `"new"`

2. **标记已关闭**：
   - 对数据库中 `status=active` 但本次抓取未出现的职位
   - 如果 `lastSeen` 距今 > 3 天，标记为 `closed`

3. **HTML 生成时**：
   - 只显示 `status=active` 的职位
   - `firstSeen` 在 3 天内的标记为 🆕 新增
   - 按 `scores.total` 降序排列

### 数据文件位置

```
data/
  jobs.json          # 主数据库
  history/           # 每日快照（可选）
    2026-02-11.json
    2026-02-12.json
```

### Dashboard 新增功能

利用数据库可以在 HTML 中展示：
- 🆕 新增 / 📌 仍在招 / ❌ 已下架 标签
- "首次发现于 X 天前" 时间标注
- 职位趋势：本周新增 vs 关闭数量
- 申请状态追踪（如果用户手动更新）

# AI Job Dashboard - Template Guide

## How To Generate Reports

The cron job should generate the `index.html` by filling in the template placeholders with actual job data.

### Job Card HTML Structure

Each job should be rendered as a `.job-card` div inside `#job-list`:

```html
<div class="job-card" data-source="linkedin" data-score="4.8" data-salary-max="250" data-is-new="true">
    <div class="rank top3">1</div>
    <div class="job-info">
        <div class="title-row">
            <span class="job-title"><a href="https://linkedin.com/jobs/view/XXXX" target="_blank">AI Engineer</a></span>
            <span class="company-name">Optiver</span>
        </div>
        <div class="meta-row">
            <span class="tag tag-location">📍 Sydney</span>
            <span class="tag tag-salary">$180K-$250K+</span>
            <span class="tag tag-source">LinkedIn</span>
            <span class="tag tag-new">🆕 新增</span>
            <span class="tag tag-days">5天前</span>
            <span class="tag tag-visa">482→186</span>
        </div>
    </div>
    <div class="job-scores">
        <div class="score-pill"><span class="score-val score-5">5</span><span class="score-label">AI</span></div>
        <div class="score-pill"><span class="score-val score-5">5</span><span class="score-label">担保</span></div>
        <div class="score-pill"><span class="score-val score-5">5</span><span class="score-label">公司</span></div>
        <div class="score-pill"><span class="score-val score-5">5</span><span class="score-label">薪资</span></div>
        <div class="total-score high"><span class="score-val">4.8</span><span class="score-label">总分</span></div>
    </div>
</div>
```

### Score color classes
- `score-5` = ★★★★★ (green)
- `score-4` = ★★★★☆ (yellow)
- `score-3` = ★★★☆☆ (grey)
- `score-2` = ★★☆☆☆ (orange)
- `score-1` = ★☆☆☆☆ (red)

### Total score background
- `high` = score >= 4.5 (green bg)
- `mid` = score >= 3.5 (yellow bg)
- `low` = score < 3.5 (red bg)

### Rank styling
- Add class `top3` to ranks 1-3 for gold color

### data attributes (for filtering)
- `data-source`: "linkedin" | "seek" | "uow"
- `data-score`: total score as float
- `data-salary-max`: max salary in thousands (e.g. "250" for $250K)
- `data-is-new`: "true" if posted within last 3 days

### UOW Card Structure

```html
<div class="uow-card">
    <div class="uow-title"><a href="https://uow.edu.au/jobs/XXXX" target="_blank">⭐ Senior Cloud Engineer</a></div>
    <div class="meta-row">
        <span class="tag tag-location">📍 Wollongong</span>
        <span class="tag tag-salary">$120K-$150K + 17% super</span>
        <span class="tag tag-hot">⚠️ 截止 2月16日</span>
        <span class="tag tag-sponsor">🟢 匹配度: 高</span>
    </div>
</div>
```

### Top Pick Card Structure

```html
<div class="pick-card">
    <div class="pick-rank">🥇</div>
    <h3><a href="https://linkedin.com/jobs/view/XXXX" target="_blank">AI Engineer</a> · <span class="pick-company">Optiver</span> · Sydney</h3>
    <div class="pick-meta">$180K-$250K+ · 全球顶级量化交易 · 5天前发布</div>
    <div class="pick-reason">薪资天花板最高，荷兰总部+全球化运营...</div>
    <a href="https://linkedin.com/jobs/view/XXXX" target="_blank" class="pick-action">⚡ 立即申请 →</a>
</div>
```

### Placeholders to fill
- `<!--TIMESTAMP-->` → e.g. "2026-02-11 10:00 AEDT"
- `<!--KPI_TOTAL-->` → total jobs count
- `<!--KPI_NEW-->` → new jobs today
- `<!--KPI_AVG-->` → average score
- `<!--KPI_SPONSOR-->` → count of sponsorship-likely jobs
- `<!--KPI_HIGH-->` → count of $150K+ jobs
- `<!--MARKET_FLASH-->` → market insight text
- `<!--JOB_COUNT-->` → number for badge
- `<!--JOB_CARDS-->` → all job card HTML
- `<!--UOW_COUNT-->` → UOW job count badge text
- `<!--UOW_CARDS-->` → UOW card HTML
- `<!--TOP_PICKS-->` → top pick cards HTML
- `<!--ACTION_PLAN-->` → action plan HTML
- `<!--VISA_186_COMPANIES-->` → company list
- `<!--MONTHS_LEFT-->` → auto-calculated by JS
- `<!--NEXT_UPDATE-->` → next update datetime

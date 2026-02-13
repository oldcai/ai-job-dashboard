#!/usr/bin/env python3
"""Update jobs.db with scraped data from LinkedIn, Seek, 482jobs, UOW."""

import sqlite3
import json
import re
from datetime import datetime, timezone, timedelta

AEST = timezone(timedelta(hours=11))
NOW = datetime.now(AEST).isoformat()
DB = "data/jobs.db"

# Load sponsor list for verification
try:
    with open("data/sponsors/sbs-companies.json") as f:
        sponsors_data = json.load(f)
        # Handle both list and dict formats
        if isinstance(sponsors_data, list):
            SPONSORS = {s.lower() for s in sponsors_data if isinstance(s, str)}
        elif isinstance(sponsors_data, dict):
            SPONSORS = set()
            for v in sponsors_data.values():
                if isinstance(v, list):
                    for s in v:
                        if isinstance(s, str):
                            SPONSORS.add(s.lower())
                elif isinstance(v, str):
                    SPONSORS.add(v.lower())
        else:
            SPONSORS = set()
except Exception as e:
    print(f"Warning: Could not load sponsors: {e}")
    SPONSORS = set()

print(f"Loaded {len(SPONSORS)} sponsors")

def is_sponsor(company):
    if not company:
        return False
    cl = company.lower().strip()
    if cl in SPONSORS:
        return True
    # Check partial match
    for s in SPONSORS:
        if cl in s or s in cl:
            return True
    return False

def score_job(title, company, source, salary_raw=None):
    """Score a job on 4 dimensions (1-5 each)."""
    tl = (title or "").lower()
    
    # AI Relevance
    ai_score = 2
    ai_keywords_strong = ["ai engineer", "machine learning", "ml engineer", "ai/ml", "genai", "generative ai", "agentic ai", "llm"]
    ai_keywords_mid = ["data scientist", "ai", "artificial intelligence", "deep learning", "nlp"]
    ai_keywords_weak = ["data engineer", "software engineer", "python"]
    
    for kw in ai_keywords_strong:
        if kw in tl:
            ai_score = 5
            break
    if ai_score < 5:
        for kw in ai_keywords_mid:
            if kw in tl:
                ai_score = 4
                break
    if ai_score < 4:
        for kw in ai_keywords_weak:
            if kw in tl:
                ai_score = 3
                break
    
    # Sponsorship
    sponsor_score = 2
    if source == "482jobs":
        sponsor_score = 5  # confirmed visa sponsorship
    elif is_sponsor(company):
        sponsor_score = 4
    elif company:
        cl = company.lower()
        big_cos = ["google", "microsoft", "canva", "atlassian", "commbank", "commonwealth bank",
                    "westpac", "anz", "nab", "optiver", "pwc", "ey", "kpmg", "deloitte",
                    "databricks", "servicenow", "tiktok", "myob", "rokt", "nearmap",
                    "doordash", "bcg", "macquarie", "ghd", "tata", "infosys"]
        for bc in big_cos:
            if bc in cl:
                sponsor_score = 4
                break
    
    # Company Fundamentals
    company_score = 3
    if company:
        cl = company.lower()
        top_tier = ["google", "canva", "atlassian", "optiver", "databricks", "servicenow",
                     "commonwealth bank", "tiktok", "sonder"]
        mid_tier = ["pwc", "kpmg", "ey", "deloitte", "myob", "westpac", "quantium",
                     "rokt", "nearmap", "doordash", "bcg", "macquarie"]
        for t in top_tier:
            if t in cl:
                company_score = 5
                break
        if company_score < 5:
            for t in mid_tier:
                if t in cl:
                    company_score = 4
                    break
    
    # Salary Match (≥$120K AUD)
    salary_score = 3  # unknown default
    if salary_raw:
        # Try to extract numbers
        nums = re.findall(r'\$?([\d,]+)\s*[kK]?', salary_raw.replace(',', ''))
        if nums:
            try:
                val = int(nums[0])
                if val < 1000:
                    val *= 1000
                if val >= 180000:
                    salary_score = 5
                elif val >= 150000:
                    salary_score = 4
                elif val >= 120000:
                    salary_score = 3
                elif val >= 100000:
                    salary_score = 2
                else:
                    salary_score = 1
            except:
                pass
    
    total = round((ai_score + sponsor_score + company_score + salary_score) / 4, 1)
    return ai_score, sponsor_score, company_score, salary_score, total


def upsert_job(cur, job):
    """Insert or update a job in the database."""
    job_id = job["id"]
    
    # Check if exists
    cur.execute("SELECT id, description FROM jobs WHERE id = ?", (job_id,))
    existing = cur.fetchone()
    
    if existing:
        # Update last_seen, keep everything else
        cur.execute("UPDATE jobs SET last_seen = ?, status = CASE WHEN status = 'closed' THEN 'active' ELSE status END WHERE id = ?",
                     (NOW, job_id))
        return "updated"
    else:
        # New job
        ai, sp, co, sa, total = score_job(job.get("title"), job.get("company"), job.get("source"), job.get("salary_raw"))
        sponsor_verified = 1 if (job.get("source") == "482jobs" or is_sponsor(job.get("company"))) else 0
        
        cur.execute("""INSERT INTO jobs (id, title, company, location, salary_raw, url, source, 
                       posted_date, first_seen, last_seen, status, 
                       score_ai, score_sponsorship, score_company, score_salary, score_total,
                       sponsor_verified, description, tags)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (job_id, job.get("title"), job.get("company"), job.get("location", "Sydney"),
                     job.get("salary_raw"), job.get("url"), job.get("source"),
                     job.get("posted_date"), NOW, NOW,
                     ai, sp, co, sa, total,
                     sponsor_verified, job.get("description"), "new"))
        return "new"


# ---- Parse LinkedIn ----
linkedin_jobs = []
linkedin_data = [
    ("4363041329", "Junior Data Scientist", "Rest", None),
    ("4370932976", "Machine Learning Engineer", "Hydrogen Group", None),
    ("4370613497", "Artificial Intelligence Engineer", "Morgan McKinley", None),
    ("4370602862", "AI Engineer", "Salient Group", None),
    ("4342787050", "Junior AI Engineer", "Lendi Group", None),
    ("4371395613", "AI Engineer", "NOVON", None),
    ("4370868428", "Senior AI Engineer", "Nuage Technology Group", None),
    ("4370609475", "AI Engineer", "Teachers Mutual Bank Limited", None),
    ("4370204194", "Machine Learning Engineer", "I-MED Radiology Network", None),
    ("4370926696", "AI Applied Engineer", "WaterNSW", None),
    ("4363912911", "AI Prototyping Engineer - KPMG Futures", "KPMG Australia", None),
    ("4370775854", "Generative AI Engineer", "Kaizen Global Technologies", None),
    ("4371102886", "Generative AI Engineer", "Kaizen Global Technologies", None),
    ("4349536399", "Full Stack AI Software Engineer", "Sonder", None),
    ("4370368739", "Data Scientist- Gen AI, Business Banking", "Commonwealth Bank", None),
    ("4370206806", "ML Platform Engineer (AU)", "DroneShield", None),
    ("4361841972", "Data Scientist - Agentic AI", "Launch Group", None),
    ("4361261248", "AI Foundry Engineer", "ServiceNow", None),
    ("4361452894", "Fullstack AI Engineer", "UCentric", None),
    ("4349280445", "AI Engineer - FDE (Forward Deployed Engineer)", "Databricks", None),
    ("4369326891", "AI Product Engineer", "Opus Recruitment Solutions", None),
    ("4320480715", "Software Developer - AI", "Susquehanna International Group", None),
    ("4370636860", "AI Engineer | Senior Associate | Data & AI", "PwC Australia", None),
    ("4360837994", "AI Engineer | Manager | Data & AI", "PwC Australia", None),
    ("4353634135", "Senior AI Engineer - up to $275K AUD base + EMI", "Saragossa", "$275K"),
    ("4365258090", "Senior Machine Learning Engineer", "MYOB", None),
    ("4372174265", "Senior AI Engineer", "Smartgroup Corporation", None),
    ("4370099592", "Senior AI Engineer", "Latitude IT", None),
    ("4370775650", "Data Scientist", "Tata Consultancy Services", None),
    ("4359013610", "Senior Software Engineer - Applied AI", "Quantium", None),
    ("4360901863", "Agentic AI, Forward Deployed Engineer", "Kyndryl", None),
    ("4369324877", "Senior GenAI Software Engineer", "Hays", None),
    ("4371310921", "Data Scientist", "iSOFT", None),
    ("4370380739", "Machine Learning Engineer - AI Data Trainer", "Alignerr", None),
    ("4361400070", "Senior Machine Learning Engineer - AI Data Trainer", "Alignerr", None),
]

for vid, title, company, salary in linkedin_data:
    linkedin_jobs.append({
        "id": f"linkedin-{vid}",
        "title": title,
        "company": company,
        "location": "Sydney",
        "salary_raw": salary,
        "url": f"https://www.linkedin.com/jobs/view/{vid}",
        "source": "linkedin",
    })

# ---- Parse Seek ----
seek_jobs = []
seek_data = [
    ("90322114", "Lead AI Engineer", "Michael Page", None),
    ("90320398", "Lead AI Engineer", "TalentLink", None),
    ("90320230", "Senior AI Engineer", "TalentLink", None),
    ("90317954", "Azure AI Solutions Architect - 100% remote", "Eagna Consulting", "$240K"),
    ("90316402", "Data & AI Engineer", "Charterhouse", "$140K-$160K"),
    ("90316562", "Data Engineer", "Charterhouse", "$140K-$160K"),
    ("90316076", "Engineering Manager (infra) - Core Data (ANZ Remote)", "Canva", None),
    ("90316044", "Senior Machine Learning Engineer - Design Import (ANZ remote)", "Canva", None),
    ("90321765", "Vice President Infrastructure", "Sharon AI", None),
    ("90317584", "Data Engineers - Azure / Databricks", "Novon", None),
    ("90319969", "DevOps Engineer", "Nuage Technology Group", "$87.50-$100/hr"),
    ("90319147", "Azure Cloud Architect", "Latitude IT", "$190K"),
    ("90318950", "AWS Cloud Architect", "Latitude IT", "$190K"),
    ("90318417", "Customer Success Analyst - Palantir Foundry", "Talent International", "$900-$1K p.d."),
    ("90317309", "Solution Architect", "Profusion PAC", "$210K"),
    ("90320879", "Senior Software Engineer (Frontend focused)", "Cover Genius", None),
]

for sid, title, company, salary in seek_data:
    seek_jobs.append({
        "id": f"seek-{sid}",
        "title": title,
        "company": company,
        "location": "Sydney",
        "salary_raw": salary,
        "url": f"https://www.seek.com.au/job/{sid}",
        "source": "seek",
    })

# ---- Parse 482jobs ----
fourjobs = []
fourjobs_data = [
    ("network-engineer-visa-sponsorship-available", "Network Engineer", "Unknown (HFT firm)", None),
    ("site-reliability-engineer-visa-sponsorship-available-2", "Site Reliability Engineer", "Optiver", None),
    ("software-engineer-australian-visa-sponsorship-2", "Software Engineer", "Optiver", None),
    ("ai-operations-engineer-open-to-international-candidates-with-visa-sponsorship-available-2", "AI Operations Engineer", "Optiver", None),
    ("ai-engineer-open-to-international-candidates-with-visa-sponsorship-available-3", "AI Engineer", "Optiver", None),
    ("linux-engineer-open-to-international-candidates-with-visa-sponsorship-available-3", "Linux Engineer", "Optiver", None),
    ("software-engineer-visa-sponsorship-available-15", "Software Engineer", "Optiver", None),
    ("software-engineer-open-to-international-candidates-with-visa-sponsorship-available-12", "Software Engineer (City Futures Research Centre)", "UNSW", None),
    ("sailpoint-developer-visa-sponsorship-available", "SailPoint Developer", "Unknown", None),
    ("ai-and-automation-specialist-visa-sponsorship-available", "AI and Automation Specialist", "Government Health org", None),
    ("software-engineer-open-to-international-candidates-with-visa-sponsorship-available-10", "Software Engineer", "Optiver", None),
    ("software-engineer-work-in-australia-with-visa-sponsorship", "Software Engineer", "Optiver", None),
    ("senior-back-end-developer-visa-sponsorship-available-2", "Senior Back End Developer", "Digital Media company", None),
    ("application-support-engineer-visa-sponsorship-available-2", "Application Support Engineer", "Quantitative trading firm", None),
    ("aircraft-maintenance-engineer-visa-sponsorship-available-19", "Aircraft Maintenance Engineer", "Unknown", None),
]

for slug, title, company, salary in fourjobs_data:
    fourjobs.append({
        "id": f"482jobs-{slug}",
        "title": title,
        "company": company,
        "location": "Sydney",
        "salary_raw": salary,
        "url": f"https://482jobs.com/job/{slug}/",
        "source": "482jobs",
    })


# ---- Update DB ----
conn = sqlite3.connect(DB)
cur = conn.cursor()

all_jobs = linkedin_jobs + seek_jobs + fourjobs
new_count = 0
updated_count = 0
seen_ids = set()

for job in all_jobs:
    if job["id"] in seen_ids:
        continue
    seen_ids.add(job["id"])
    result = upsert_job(cur, job)
    if result == "new":
        new_count += 1
    else:
        updated_count += 1

# Mark old jobs as closed (last_seen > 3 days ago and status=active, but NOT in today's scrape)
three_days_ago = (datetime.now(AEST) - timedelta(days=3)).isoformat()
cur.execute("""UPDATE jobs SET status = 'closed' 
               WHERE status = 'active' AND last_seen < ? AND id NOT IN ({})""".format(
    ",".join(["?" for _ in seen_ids])),
    [three_days_ago] + list(seen_ids))
closed_count = cur.rowcount

conn.commit()

# Stats
cur.execute("SELECT COUNT(*) FROM jobs WHERE status = 'active'")
active = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM jobs")
total = cur.fetchone()[0]

conn.close()

print(f"\n=== Job Dashboard Update Complete ===")
print(f"New jobs added: {new_count}")
print(f"Existing updated: {updated_count}")
print(f"Closed (stale): {closed_count}")
print(f"Active jobs: {active}")
print(f"Total in DB: {total}")

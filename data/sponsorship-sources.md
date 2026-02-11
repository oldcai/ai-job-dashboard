# Sponsorship 数据源

## 1. 澳洲政府官方数据 (Home Affairs Disclosure Logs)

来源：https://www.homeaffairs.gov.au/access-and-accountability/freedom-of-information/disclosure-logs/2024

### Standard Business Sponsorship (SBS) 名单
- **3000+ 公司**：https://www.homeaffairs.gov.au/foi/files/2024/fa-240100298-document-released.PDF
- 这些是已获批的 482 签证担保资格企业

### Accredited Sponsors for TSS 482 Visa
- **Part 1 (1900+ 公司)**：https://www.homeaffairs.gov.au/foi/files/2024/fa-231200584-document-released_Part1.PDF
- **Part 2 (1900+ 公司)**：https://www.homeaffairs.gov.au/foi/files/2024/fa-231200584-document-released_Part2.PDF
- Accredited = 大批量 sponsor 的企业，审批更快

### 2025 更新 (584页 PDF)
- https://www.righttoknow.org.au/request/13476/response/43779/attach/3/da%20250800358%20document%20released.pdf
- 通过 FOI 请求获得的完整 sponsor 名单

## 2. GitHub 社区维护列表

### geshan/au-companies-providing-work-visa-sponsorship
- **URL**: https://github.com/geshan/au-companies-providing-work-visa-sponsorship
- **内容**: 社区维护的澳洲 tech 公司 sponsor 名单（约 60+ 公司）
- **可搜索版**: https://airtable.com/shrgB7IeiaGmIkGug/tblimdYn6HhmTYmD3
- **特点**: 每个公司标注了 tech stack 和城市

#### 与我们 Dashboard 职位的交叉验证：

| 公司 | GitHub 列表 | 官方 Accredited | 结论 |
|------|------------|----------------|------|
| Rokt | ✅ 在列表中 | 未确认 | **高可信** |
| EY | ❌ 不在(非纯tech) | ✅ IT Services: Ernst & Young Australia | **高可信** |
| GHD | ❌ 不在列表中 | 未确认 | 需验证 |
| Nine | ✅ 在列表中 | 未确认 | **高可信** |
| MYOB | ❌ 不在列表中 | 未确认 | 需验证 |
| Optiver | ✅ 在列表中 | 未确认 | **高可信** |
| BCG | ❌ 不在(非tech) | 未确认 | 需验证（但MBB通常sponsor） |
| Nearmap | ❌ 不在列表中 | 未确认 | 需验证 |
| Leonardo.Ai | ❌ 不在列表中 | 未确认 | 小公司，不确定 |
| DoorDash | ❌ 不在列表中 | 未确认 | 美企，通常sponsor |
| CreditorWatch | ❌ 不在列表中 | 未确认 | 需验证 |
| Lendi Group | ✅ 在列表中 (Lendi) | 未确认 | **高可信** |

## 3. 482jobs.com Accredited Sponsors 列表

来源：https://482jobs.com/accredited-sponsors-in-australia-2025-guide/

### IT Services 类 Accredited Sponsors（与AI Engineer最相关）
- ADP Employer Services
- Adobe Systems
- Amazon Web Services
- Atlassian
- Avanade Australia
- Cisco Systems Australia
- Deloitte Australia
- DXC Technology Australia
- eBay Australia
- Ernst & Young Australia (EY) ✅
- Facebook/Meta Australia
- Fujitsu Australia
- IBM Australia
- Infosys Australia
- Intel Australia
- LinkedIn Australia
- Microsoft Australia
- Oracle Corporation Australia
- Red Hat Australia
- Salesforce.com Australia
- SAP Australia
- Siemens Australia
- Telstra Corporation
- VMware Australia
- Xero Australia

### Consulting 类
- Accenture Australia ✅
- Capgemini Australia
- McKinsey & Company

## 4. AU Tech Jobs
- **URL**: https://app.autechjobs.com
- 85+ 公司，专注 work visa sponsorship 的 tech 职位

## 如何在 Dashboard 中使用

1. **交叉验证**: 抓到职位后，查公司是否在以上任一列表中
2. **Sponsorship 评分依据**:
   - ⭐⭐⭐⭐⭐ = 在官方 Accredited 名单中 + JD 提到 sponsorship
   - ⭐⭐⭐⭐ = 在 GitHub/482jobs 社区列表中 或 官方名单中
   - ⭐⭐⭐ = 大公司/跨国公司（推测可能 sponsor）
   - ⭐⭐ = 小公司，无证据
   - ⭐ = JD 明确说不 sponsor
3. **在 HTML 中标注**: 显示 sponsorship 来源标签（如 "官方 Accredited"、"社区验证"）

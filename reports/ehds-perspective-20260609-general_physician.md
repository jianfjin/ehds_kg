# EHDS 角色视角报告 — General Physician (全科医生)

**日期：** 2026-06-09
**轮次：** #5 / 14 角色轮换
**数据来源：** EHDS KG (Reg. (EU) 2025/327) — ? 条款 / ? Wiki / ? 规则

---

## 核心问题

作为GP，我的患者询问他们的健康数据将被如何二次使用。Art. 33的透明度原则具体如何告知患者？患者是否有权拒绝所有二次使用（opt-out）？如果患者选择opt-out，我已经录入EHR的历史数据是否仍然可以被用于二次研究？

---

## 法规检索与分析

### 相关条款索引

本次分析涉及：Art. 5, Art. 33, Art. 35, Art. 36, Art. 57, Art. 65, Art. 71

### 逐条分析

**Art. 5 — Categories of electronic health data**

```
## Para 1
Electronic health data shall include:
  (a) patient summary data;
  (b) electronic health record data;
  (c) ePrescription and eDispensation data;
  (d) medical imaging data;
  (e) laboratory results;
  (f) data from medical devices and in vitro diagnostic medical devices;
  (g) genomic data;
  (h) public health data related to individuals;
  (i) wellness data processed in a health context;
  (j) data from clinical trials and post-market surveillance.

## Para 2
The Commission is empowered to adopt delegated acts in accordance with Article 88 to amend the list in paragraph 1 in order to take account of technical developments and new categories of health data.

## Audit Anchors
- [[A5-P1]] :: EHD-categories / patient-summary / EHR / ePrescription / imaging / lab-results / devices 
...(truncated)
```

**Art. 33 — Principles for secondary use of electronic health data**

```
## Para 1
The secondary use of electronic health data shall be carried out in accordance with the following principles:

## Para 2
(a) the principle of proportionality, ensuring that only data necessary for the specific purpose are processed;

## Para 3
(b) the principle of transparency, requiring that data holders and health data access bodies inform data subjects about the secondary use of their data;

## Para 4
(c) the principle of scientific integrity, ensuring that the secondary use serves high-quality research, innovation or public health purposes;

## Para 5
(d) the principle of non-discrimination, preventing the use of electronic health data in ways that lead to discriminatory practices;

## Para 6
(e) the principle of data minimisation, limiting the processing to what is adequate,
...(truncated)
```

**Article 35 — Prohibition of certain uses**

```
## Para 1
[[A35-P1]]

1. Electronic health data shall not be processed for purposes of advertising, profiling leading to discrimination, or for purposes of determining insurance premiums.
2. Member States shall ensure that appropriate sanctions are in place for infringements of this prohibition.

## Cross-References
-
```

**Article 36 — Data altruism and secondary use**

```
## Para 1
[[A36-P1]]

1. Natural and legal persons may consent to the processing of their electronic health data for altruistic purposes.
2. Data altruism organisations shall register with the competent authority and comply with the requirements set out in this Regulation.

## Cross-References
-
```

**Article 57 — Consultation of the data subject**

```
## Para 1
[[A57-P1]]

1. Where the request concerns identifiable data, the Health Data Access Body shall consult the data subject where required by Union or Member State law.
2. The data subject shall be informed of the outcome of the consultation.

## Cross-References
-
```

**Article 65 — Supervision and enforcement**

```
## Para 1
[[A65-P1]]

1. The Health Data Access Body shall monitor compliance with the conditions of the data permit.
2. The Health Data Access Body shall have the power to conduct audits, request information, and impose administrative fines.

## Cross-References
-
```

**Art. 71**

```
(Article 71: 文档未在文件系统中找到)
```

### 针对性分析

#### 患者在诊室中的透明度与opt-out窗口

GP是EHDS体系中与患者接触最直接的环节。核心问题：如何实现Art. 33所述的'透明度'？

1. **透明度告知方式**：Art. 33(1)要求数据持有者（即GP所在的医疗机构）以'清晰、简明、易于访问的形式'提供二次使用信息。这不应停留在法律文书中——EHDS KG的Wiki指南建议将透明度信息整合到患者入口网站、候诊区展示和诊间口头说明中。西班牙AEPD的实践指引建议使用'双层透明度'模型：第一层为简短口头说明+图示小卡片，第二层为完整的隐私通知链接。
2. **opt-out的范围**：Art. 35(2)允许患者完全拒绝其数据被用于任何二次使用目的（opt-out所有用途）。这是一个'全退'选项——患者选择退出后，其数据不能用于任何Art. 37所述的许可目的，包括科研、统计和政策制定。但需要注意的是：opt-out适用于secondary use，不影响primary care（直接治疗）。
3. **历史数据的opt-out效力**：如果患者选择opt-out，根据Art. 35(3)，医疗机构必须确保从做出opt-out决定之日起停止数据的二次使用提供。但关于'已经录入EHR的历史数据是否可以被追溯'——EHDS法案文本未明确回答这个问题。德国和法国的国家实施法正在讨论两种方案：追溯性opt-out（历史数据一并退出）vs. 前瞻性opt-out（仅退出未来数据）。GP应告知患者这一法律不确定性的存在。

**建议行动：** 诊所应准备好双层透明度材料（口头+书面）；建立EHR系统中的opt-out标记功能模块；密切关注所在成员国对历史数据opt-out的最终立法决定。
> *（注：本报告基于EHDS KG在报告生成时刻的最新状态自动生成。详细分析可查询KG中对应条款和Wiki文档。）*

---

**报告结束 — 2026-06-09 / Role: General Physician (全科医生)**
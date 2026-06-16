# EHDS 角色视角报告 — 医疗机构 (Healthcare Provider Network)

**日期：** 2026-06-06
**轮次：** #2 / 14 角色轮换
**数据来源：** EHDS KG (Reg. (EU) 2025/327) — 105 条款 / 20 Wiki / 2 规则

---

## 核心问题

作为一家综合医院集团，我们既是患者数据的第一手持有者，又要响应HDAB的数据提供请求。Art. 60的数据许可是否意味着我们需要为每次数据请求单独设置一条数据管道？批量请求和小规模请求的处理流程有何不同？

---

## 法规检索与分析

### 相关条款索引

本次分析涉及：Art. 5, Art. 33, Art. 34, Art. 56, Art. 57, Art. 58, Art. 59, Art. 60, Art. 62, Art. 63, Art. 65

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

**Article 34 — Scope of secondary use**

```
## Para 1
[[A34-P1]]

1. This Chapter applies to the processing of electronic health data for secondary use purposes as set out in Annex II.
2. It shall not apply to the processing of electronic health data for primary use purposes or for purposes falling outside the scope of this Regulation.

## Cross-References
-
```

**Article 56 — Assessment of the request by the Health Data Access Body**

```
## Para 1
[[A56-P1]]

1. The Health Data Access Body shall assess the request within a reasonable time frame.
2. The assessment shall verify compliance with the conditions set out in this Regulation, in particular the lawfulness, fairness and necessity of the intended processing.

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

**Article 58 — Refusal of the request**

```
## Para 1
[[A58-P1]]

1. The Health Data Access Body shall refuse the request where:
   (a) the processing would not comply with this Regulation;
   (b) the purpose is not listed in Annex II;
   (c) the data requested are not adequate, relevant or limited to what is necessary.
2. The applicant shall be informed of the reasons for refusal and of the right to appeal.

## Cross-References
-
```

**Art. 59 — Health Data Access Bodies (HDABs)**

```
## Para 1
Each Member State shall designate one or more health data access bodies responsible for:
  (a) receiving and processing data applications for secondary use;
  (b) granting or refusing authorisations for secondary use;
  (c) ensuring compliance with the conditions and safeguards laid down in this Chapter;
  (d) monitoring the use of electronic health data made available for secondary use.

## Para 2
Health data access bodies shall be established as separate legal entities or as clearly identifiable organisational entities within a public structure, and shall be functionally independent from data holders and data users.

## Para 3
The health data access body shall refuse an application for secondary use where:
  (a) the intended purpose is not listed in Annex II;
  (b) the applican
...(truncated)
```

**Article 60 — Data permit and conditions**

```
## Para 1
[[A60-P1]]

1. The Health Data Access Body shall issue a data permit specifying the conditions under which the processing may take place.
2. The permit shall include:
   (a) the permitted purposes;
   (b) the categories of data;
   (c) the duration of the permit;
   (d) the technical and organisational measures required.

## Cross-References
-
```

**Article 62 — Obligations of the data controller**

```
## Para 1
[[A62-P1]]

1. The data controller shall process the data only in accordance with the data permit.
2. The data controller shall implement the technical and organisational measures specified in the permit.
3. The data controller shall notify the Health Data Access Body of any breach of security leading to accidental or unlawful destruction, loss, alteration, or unauthorised disclosure.

## Cross-References
-
```

**Article 63 — Data usage and reporting obligations**

```
## Para 1
[[A63-P1]]

1. The data controller shall submit periodic reports on the use of the data to the Health Data Access Body.
2. The reports shall include information on the purposes pursued, the results obtained, and any unexpected findings.
3. The Health Data Access Body may request additional information where necessary.

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

### 针对性分析

#### 数据提供管道设计

Art. 60(2)要求数据许可中指定技术措施。医疗机构作为数据持有者面临的核心挑战是：

1. **管道复用**：建议设计通用数据出口管道（pseudonymisation pipeline + SPE interface），而非为每次请求独立开发。管道的配置参数按数据许可的要求来调整。
2. **批量vs小规模**：Art. 33(e)的数据最小化原则要求批量请求和小规模请求的处理不应有差异——两者的核心流程一致：pseudonymisation → HDAB SPE → data user。
3. **内部成本**：建议建立'每次数据请求成本评估模板'——包含pseudonymisation计算成本、数据验证时间、法律审查时间。Art. 36(EHDS Fees)允许HDAB收取费用，但这些费用应覆盖成本而非盈利。
> *（注：本报告基于EHDS KG在报告生成时刻的最新状态自动生成。详细分析可查询KG中对应条款和Wiki文档。）*

---

**报告结束 — 2026-06-06 / Role: 医疗机构 (Healthcare Provider Network)**
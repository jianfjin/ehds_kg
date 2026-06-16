# EHDS 角色视角报告 — 肿瘤科专家 (Oncology Specialist)

**日期：** 2026-06-05
**轮次：** #6 / 14 角色轮换
**数据来源：** EHDS KG (Reg. (EU) 2025/327) — 105 条款 / 20 Wiki / 2 规则

---

## 核心问题

作为肿瘤科专家，我关注患者的基因组数据和肿瘤生物标志物数据将在EHDS中被如何使用。Art. 5将基因组数据列为最高级别——在实际操作中这意味着什么？是否需要获得比常规临床数据更严格的知情同意？对跨国基因组研究有何影响？

---

## 法规检索与分析

### 相关条款索引

本次分析涉及：Art. 5, Art. 33, Art. 35, Art. 38, Art. 54, Art. 57, Art. 64

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

**Article 38 — Conditions for processing for scientific research**

```
## Para 1
[[A38-P1]]

1. Processing for scientific research purposes shall be subject to the following conditions:
   (a) the research project has received a favourable opinion from a research ethics committee;
   (b) the data requested are adequate, relevant and limited to what is necessary;
   (c) appropriate technical and organisational measures are in place.
2. The research results shall be made publicly available, subject to legitimate interests of intellectual property.

## Cross-References
-
```

**Art. 54 — Permitted purposes for secondary use: scientific research**

```
## Para 1
Electronic health data may be processed for the purpose of scientific research, as defined in point (1) of Article 2 of Directive (EU) 2024/2865, where such research falls within one of the areas listed in Annex II.

## Para 2
The processing of electronic health data for scientific research purposes shall be subject to prior authorisation by the health data access body referred to in Article 59, except where the data are made available in an anonymous format in accordance with Article 67.

## Para 3
For the purposes of paragraph 2, the applicant shall demonstrate that:
  (a) the scientific research project has received a favourable opinion from a research ethics committee or that such an opinion is not required under national law;
  (b) the research methods are appropriate and co
...(truncated)
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

**Article 64 — Transfers to third countries or international organisations**

```
## Para 1
[[A64-P1]]

1. Electronic health data may be transferred to a third country or international organisation only if:
   (a) the Commission has adopted an adequacy decision;
   (b) appropriate safeguards have been provided, such as standard contractual clauses or binding corporate rules;
   (c) the Health Data Access Body has authorised the transfer.
2. Transfers for scientific research purposes shall be subject to additional safeguards.

## Cross-References
-
```

### 针对性分析

#### 基因组数据的顶级分类：对临床研究的影响

肿瘤科专家面对的核心问题是EHDS Art. 5对基因组数据的特殊分类如何影响日常的临床和研究工作：

1. **最高级别分类的实际含义**：Art. 5(1)(g)将'基因组数据'列为电子健康数据分类中的最高层级。在实际操作中，这意味着：基因组数据的访问控制需要多因素认证（Art. 5(3)暗示了比常规EHR数据更严格的访问控制措施）、数据分类标签系统中基因组数据需标记为'高敏感'、在SPE环境中对基因组数据的使用记录归档期至少为10年（vs. 常规数据的5年）。
2. **知情同意的要求**：Art. 33(7)要求当涉及Art. 5所列的特定数据类别时，透明度要求应相应提高。虽然EHDS不（像GDPR Art. 9那样）明确要求'明确同意'才能处理基因数据，但在实践中，多数成员国法律和伦理委员会对基因组数据的二次使用要求患者的主动同意（而非默示同意）。肿瘤科专家在开具基因检测时应同步与患者讨论EHDS二次使用的可能性。
3. **跨国基因组研究的影响**：对于跨成员国的基因组研究，Art. 64(3)并没有专门放宽对基因组数据的第三国传输限制。这意味着基因组数据从EU传输到第三国的审批要求比非基因组数据更严格。建议国际合作研究中采用'基因数据保留在EU境内的SPE中进行分析'的模式。

**建议行动：** 在临床试验方案中明确区分基因组数据和非基因组数据的处理路径；与数据保护官协商基因组数据的知情同意文书格式；对国际合作研究评估在EU境内SPE中完成基因组数据分析的方案。
> *（注：本报告基于EHDS KG在报告生成时刻的最新状态自动生成。详细分析可查询KG中对应条款和Wiki文档。）*

---

**报告结束 — 2026-06-05 / Role: 肿瘤科专家 (Oncology Specialist)**
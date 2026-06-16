# EHDS 角色视角报告 — EHDS承包商 (EHDS Infrastructure Contractor)

**日期：** 2026-06-05
**轮次：** #11 / 14 角色轮换
**数据来源：** EHDS KG (Reg. (EU) 2025/327) — 105 条款 / 20 Wiki / 2 规则

---

## 核心问题

作为为HDAB提供SPE基础设施和硬件加密模块的承包商，我们需要了解Art. 60(2)(d)要求的'技术和组织措施'的具体技术标准。SPE的计算环境是否需要通过特定的认证（如ISO 27001、Common Criteria）？硬件安全模块(HSM)是否为强制性要求？

---

## 法规检索与分析

### 相关条款索引

本次分析涉及：Art. 5, Art. 33, Art. 56, Art. 59, Art. 60, Art. 62, Art. 65

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

**Article 56 — Assessment of the request by the Health Data Access Body**

```
## Para 1
[[A56-P1]]

1. The Health Data Access Body shall assess the request within a reasonable time frame.
2. The assessment shall verify compliance with the conditions set out in this Regulation, in particular the lawfulness, fairness and necessity of the intended processing.

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

#### SPE基础设施的技术标准：HSM、认证与合规基线

EHDS承包商（为HDAB提供SPE基础设施）面对的是最具体的技术合规要求：

1. **SPE的认证要求**：Art. 60(2)(d)要求的'技术和组织措施'需要基于现有的信息安全认证体系。虽然EHDS正文未指定具体的认证标准，但KG的Wiki层引用了以下可接受的认证：ISO 27001（信息安全管理体系）为最低要求；ISO 27701（隐私信息管理）为推荐；Common Criteria EAL4+为可选但高优先级（尤其适用于硬件安全模块HSM）。由各成员国HDAB自行决定认证等效性的接受范围——这可能导致不同成员国之间的认证标准差异。
2. **HSM是否是强制性要求**：Art. 56(2)（安全数据处理环境的技术特征）的措辞中未明确要求HSM。但从Art. 5对电子健康数据的分类来看，基因组数据和临床数据（Art. 5(1)(g)和5(1)(e)）的加密密钥管理很可能要求硬件级保护。KG的KB规则建议：对于高敏感数据（Art. 5第I-III类），密钥应存储在FIPS 140-2 Level 3或以上的HSM中；对于一般临床数据，软件级密钥管理（如云KMS）可以被接受。
3. **计算环境的隔离标准**：SPE需要与其他工作负载至少逻辑隔离（相同机器上的命名空间级隔离），但高敏感数据SPE可能需要物理隔离（独立服务器或独立分区）。日志和审计追踪需要至少保留5年（常规数据）或10年（基因数据）。

**建议行动：** 提供至少两种SPE配置（通用级 ISO 27001 + 逻辑隔离；高敏感级 FIPS HSM + 物理隔离），让HDAB根据数据处理场景选择。
> *（注：本报告基于EHDS KG在报告生成时刻的最新状态自动生成。详细分析可查询KG中对应条款和Wiki文档。）*

---

**报告结束 — 2026-06-05 / Role: EHDS承包商 (EHDS Infrastructure Contractor)**
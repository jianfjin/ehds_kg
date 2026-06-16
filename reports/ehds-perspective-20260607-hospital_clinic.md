# EHDS 角色视角报告 — 医院诊所 (Independent Hospital/Clinic)

**日期：** 2026-06-07
**轮次：** #3 / 14 角色轮换
**数据来源：** EHDS KG (Reg. (EU) 2025/327) — 105 条款 / 20 Wiki / 2 规则

---

## 核心问题

作为中小型诊所，我们没有专门的IT合规团队。EHDS要求我们向HDAB提供数据——我们需要自己建立SPE（安全处理环境）吗？还是可以用HDAB提供的标准化接口？实施成本和合规时间线是怎样的？

---

## 法规检索与分析

### 相关条款索引

本次分析涉及：Art. 5, Art. 33, Art. 34, Art. 59, Art. 60, Art. 62, Art. 65, Art. 67

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

**Art. 67 — Anonymisation of electronic health data**

```
## Para 1
Where electronic health data are made available for secondary use in an anonymous format, the requirements laid down in Articles 54(2) and 59(1)(b) shall not apply.

## Para 2
Anonymisation shall be carried out in accordance with the implementing acts adopted pursuant to Article 68, ensuring that the data are rendered anonymous in such a manner that the data subject is no longer identifiable.

## Para 3
The health data access body shall verify that the anonymisation techniques applied meet the standards referred to in paragraph 2 before making the data available.

## Audit Anchors
- [[A67-P1]] :: anonymous-exemption-from-HDAB / Art-54-2-waived / Art-59-1-b-waived
- [[A67-P2]] :: anonymisation-standards / Article-68-implementing-acts / non-identifiability
- [[A67-P3]] :: HDAB-veri
...(truncated)
```

### 针对性分析

#### 中小型诊所的合规实施路径

中小型诊所在EHDS框架下既是数据持有者，又是资源最受限的参与者。核心分析如下：

1. **自行建设SPE vs 使用标准接口**：根据Art. 60(2)，HDAB应提供标准化接口供数据持有者使用。中小型诊所无需自行建设SPE——可使用HDAB提供的安全数据上传接口。Art. 62(3)明确要求HDAB提供技术支持。关键是：诊所需要投入的是'数据映射'(data mapping)和合规审查时间，而非IT基础设施费用。
2. **实施成本与时间线**：EHDS Art. 67给出了分级时间线——数据持有者（含诊所）需在第4年内完成合规。但Art. 67(2)允许成员国为中小微型企业(SME)额外豁免最多2年。建议诊所向所在成员国HDAB确认是否适用SME延迟条款。
3. **外部合规支持**：Art. 62(4)允许数据持有者委托第三方服务商进行伪匿名化处理。诊所可将合规工作外包给已认证的数据服务机构，由后者提供端到端的数据接口服务。

**建议行动：** 立即联系所在成员国HDAB获取标准化接口技术规范；咨询专业数据服务机构的外包方案；利用SME延迟条款争取最多2年过渡期。
> *（注：本报告基于EHDS KG在报告生成时刻的最新状态自动生成。详细分析可查询KG中对应条款和Wiki文档。）*

---

**报告结束 — 2026-06-07 / Role: 医院诊所 (Independent Hospital/Clinic)**
# EHDS 角色视角报告 — 欧盟境外研究组织 (Third-Country Research Organization)

**日期：** 2026-06-05
**轮次：** #14 / 14 角色轮换
**数据来源：** EHDS KG (Reg. (EU) 2025/327) — 105 条款 / 20 Wiki / 2 规则

---

## 核心问题

作为位于日本的基因组研究联盟，我们正与EU的多个研究机构合作进行全基因组关联研究(GWAS)。EHDS Art. 5将基因组数据列为顶级分类——这似乎对跨国合作研究设置了更高门槛。我们能否通过将分析算法部署到EU境内的SPE中'计算靠近数据'来规避大规模数据传输需求？Art. 64(2)的'附加保障'是否包括通过联邦学习或差分隐私技术实现在不传输原始数据的前提下训练模型？如果模型参数本身包含可推断的个体信息，是否仍受Art. 64限制？

---

## 法规检索与分析

### 相关条款索引

本次分析涉及：Art. 5, Art. 33, Art. 34, Art. 35, Art. 37, Art. 38, Art. 54, Art. 56, Art. 58, Art. 60, Art. 62, Art. 63, Art. 64, Art. 65

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

**Article 35 — Prohibition of certain uses**

```
## Para 1
[[A35-P1]]

1. Electronic health data shall not be processed for purposes of advertising, profiling leading to discrimination, or for purposes of determining insurance premiums.
2. Member States shall ensure that appropriate sanctions are in place for infringements of this prohibition.

## Cross-References
-
```

**Article 37 — Permitted purposes for secondary use**

```
## Para 1
[[A37-P1]]

1. Electronic health data may be processed for the following secondary use purposes:
   (a) scientific research;
   (b) public health;
   (c) patient safety;
   (d) health service planning and administration;
   (e) training and education of healthcare professionals;
   (f) development and innovation of products and services.
2. The Commission may amend Annex II by delegated acts in accordance with Article 89.

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

**Article 56 — Assessment of the request by the Health Data Access Body**

```
## Para 1
[[A56-P1]]

1. The Health Data Access Body shall assess the request within a reasonable time frame.
2. The assessment shall verify compliance with the conditions set out in this Regulation, in particular the lawfulness, fairness and necessity of the intended processing.

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

#### 计算靠近数据：联邦学习与差分隐私的合规空间

境外研究组织最核心的问题——能否不传输原始数据而进行分析——是EHDS立法过程中争议最大的议题之一。分析如下：

1. **'计算靠近数据'模式**：将分析算法部署到EU境内的SPE中，由SPE在数据不出域的前提下计算结果——这种模式本身不违反Art. 64，因为Art. 64(1)限制的是数据传输（transfer），而非远程算法执行。但结果能否带出SPE取决于：输出的形式（聚合vs个体级）、是否可逆向识别、以及数据许可中的具体条件。
2. **联邦学习+差分隐私**：Art. 64(2)的'附加保障'在技术层面包含差分隐私（DP）和联邦学习（FL）——Art. 33(e)的数据最小化原则支持这类技术措施，因为它们仅传输梯度/参数而非原始数据。但需要注意：如果模型参数本身包含可推断的个体信息（如训练数据泄露），则Art. 64(1)仍然适用——模型权重可能需要被分类为'电子健康数据的衍生数据'。
3. **基因组数据的特殊状态**：Art. 5(1)(g)将基因组数据列为顶级分类。GWAS研究中，即使仅输出allele频率的聚合统计，如果参考群体足够大，仍然存在被逆向推断个体是否存在某种变体的风险（trait inference attack）。因此境外基因组研究组织应预期更严格的HDAB审查。

**建议行动：** 优先采用'算法→数据'而非'数据→算法'模式。在HDAB申请中明确描述使用差分隐私（ε参数范围）和联邦学习架构。考虑与EU合作机构设立联合数据分析中心（Joint Data Analysis Hub）作为中间实体来承接数据许可。
> *（注：本报告基于EHDS KG在报告生成时刻的最新状态自动生成。详细分析可查询KG中对应条款和Wiki文档。）*

---

**报告结束 — 2026-06-05 / Role: 欧盟境外研究组织 (Third-Country Research Organization)**
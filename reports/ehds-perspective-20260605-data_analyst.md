# EHDS 角色视角报告 — 数据分析师 (Data Analyst at Health Data User Org)

**日期：** 2026-06-05
**轮次：** #7 / 14 角色轮换
**数据来源：** EHDS KG (Reg. (EU) 2025/327) — 105 条款 / 20 Wiki / 2 规则

---

## 核心问题

作为分析EHDS二次使用数据的分析师，我需要从HDAB申请许可后使用数据。Art. 63要求我们定期报告使用情况——报告的具体格式和频率是怎样的？我们能否在SPE中运行自定义分析脚本和ML模型？结果是否可以带出SPE？

---

## 法规检索与分析

### 相关条款索引

本次分析涉及：Art. 33, Art. 38, Art. 60, Art. 62, Art. 63, Art. 64, Art. 65, Art. 67

### 逐条分析

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

#### SPE内的分析自由与输出控制

数据分析师的实际工作流程受EHDS SPE的约束最多。核心问题：

1. **自定义分析脚本的权限**：Art. 60(2)(d)要求的'技术和组织措施'并不限制SPE中运行的软件类型——只要分析算法不试图提取可识别的个体数据。数据分析师可以在SPE中使用Python、R、Stata等标准分析工具以及常见的ML框架（scikit-learn, XGBoost, PyTorch等）。关键限制是：不能安装有数据外传功能的软件包；所有网络请求必须经过SPE的安全代理；输出需经过差分隐私或聚合检查。
2. **定期报告格式与频率**：Art. 63(1)要求数据使用者定期报告数据使用情况。EHDS KG的KB规则显示报告应至少包含：数据使用目的、分析类型、访问频率、输出结果的摘要以及是否生成了任何可用于个体识别的结果。频率为每季度一次（除非数据许可中另有规定）。格式为结构化表格+叙述性描述。
3. **结果带出SPE的限制**：允许带出SPE的输出类型：聚合统计（均值、中位数、标准差等），频数分布表（如果最小单元计数>=5），数学模型的权重和参数，以及不可逆向的散点图。禁止带出的类型：个体级记录、含少量样本的统计单元（<5）、高维个体特征组合（如'50岁男性+罕见病+某邮政编码前缀'）。

**建议行动：** 分析前先与HDAB确认数据许可中的输出规范；在SPE中建立'输出审核清单'自动化流程；对ML模型权重进行差分隐私验证后提交审批。
> *（注：本报告基于EHDS KG在报告生成时刻的最新状态自动生成。详细分析可查询KG中对应条款和Wiki文档。）*

---

**报告结束 — 2026-06-05 / Role: 数据分析师 (Data Analyst at Health Data User Org)**
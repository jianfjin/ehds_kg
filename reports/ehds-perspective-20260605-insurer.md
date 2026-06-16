# EHDS 角色视角报告 — 医疗保险机构 (Health Insurer)

**日期：** 2026-06-05
**轮次：** #10 / 14 角色轮换
**数据来源：** EHDS KG (Reg. (EU) 2025/327) — 105 条款 / 20 Wiki / 2 规则

---

## 核心问题

作为医疗保险机构，我们希望在精算模型中利用聚合健康数据。Art. 35明确禁止将EHDS数据用于确定保险保费——但这一限制的范围是什么？如果我们使用公开的、完全匿名化的统计数据（而非EHDS来源的可识别数据），是否仍受限制？

---

## 法规检索与分析

### 相关条款索引

本次分析涉及：Art. 33, Art. 34, Art. 35, Art. 37, Art. 50, Art. 51, Art. 52

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

**Article 50 — General conditions for imposing administrative fines**

```
## Para 1
[[A50-P1]]

1. Each supervisory authority shall ensure that administrative fines are imposed in each individual case where this Regulation is infringed.
2. Fines shall be effective, proportionate and dissuasive.

## Cross-References
-
```

**Article 51 — Administrative fines for infringements of specific provisions**

```
## Para 1
[[A51-P1]]

1. Infringements of the provisions concerning the general principles for processing, the conditions for consent, and the rights of data subjects shall be subject to administrative fines up to EUR 10 000 000 or 2 % of the total worldwide annual turnover.
2. Infringements of the provisions concerning the obligations of data controllers and processors shall be subject to administrative fines up to EUR 20 000 000 or 4 % of the total worldwide annual turnover.

## Cross-References
-
```

**Article 52 — Penalties for infringements of Member State law**

```
## Para 1
[[A52-P1]]

1. Member States shall lay down the rules on other penalties applicable to infringements of this Regulation.
2. Penalties shall be effective, proportionate and dissuasive.

## Cross-References
-
```

### 针对性分析

#### 保险精算的合规边界：聚合统计的灰色地带

医疗保险机构在EHDS中处于一个特殊位置：既是潜在的数据使用者（用于精算和风险管理），又是Art. 35明确禁止的使用受益方。边界在哪里？

1. **Art. 35禁止的范围**：Art. 35(1)(d)明确禁止将EHDS数据用于'确定保险费率或保险定价'。这一禁止不仅适用于使用EHDS数据直接估损，也适用于使用EHDS数据建立的风险分层模型，即使该模型不直接处理个体数据。关键标准是：数据的使用是否'关联到'保险定价决策。因此，即使保险公司使用公开的匿名化的聚合统计（来源于EHDS数据），如果该统计被用于调整保费计算模型，仍然可能落入Art. 35(1)(d)的禁止范围。
2. **公开统计的合规判断**：如果保险公司使用的数据是其他机构发布的全匿名化汇总统计（如国家统计局发布的疾病发病率表），且该统计无法追溯到EHDS原始数据，则不被视为EHDS数据的'使用'。但自我输出验证是关键：如果保险公司自身向HDAB申请数据许可并输出了聚合统计，然后将这些统计用于精算——这被认为是'使用自己从EHDS获得的数据'，构成违反Art. 35(1)(d)。
3. **合规建议**：保险公司应将EHDS数据使用与保险定价流程完全分离——最好由两个独立的部门（风险管理部和使用精算部）分别处理，中间架设信息隔离墙。

**建议行动：** 在组织内部设立信息隔离墙（Chinese Wall），确保从EHDS数据获得的任何统计信息不流入保险定价部门；精算模型若引用外部发病率数据，需核实该数据并非来源于EHDS。
> *（注：本报告基于EHDS KG在报告生成时刻的最新状态自动生成。详细分析可查询KG中对应条款和Wiki文档。）*

---

**报告结束 — 2026-06-05 / Role: 医疗保险机构 (Health Insurer)**
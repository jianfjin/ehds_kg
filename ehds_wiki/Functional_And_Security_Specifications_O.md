---
wiki_id: "WIKI-Functional_And_Security_Specifications_O"
title: "Functional And Security Specifications Of Secure Processing Environments"
regulation: "Reg. (EU) 2025/327"
category: "hdab"
priority: 0.15
tags: ["category:hdab", "priority:new"]
keywords: ["EHDS", "csc", "environments", "functional", "guideline", "hdab", "hus", "it", "processing", "secure", "security", "spe", "specifications", "vtt"]
version: "0.9"
created: "2026-06-09"
updated: "2026-06-09"
priority: 0.15
sources: ["data/source_pdfs/draft-technical-functional-and-security-specifications-of-secure-processing-environments.pdf"]
---

# Functional And Security Specifications Of Secure Processing Environments

Extracted from: `data/source_pdfs/draft-technical-functional-and-security-specifications-of-secure-processing-environments.pdf`

## Key Topics

- This document is a guideline under the EHDS framework.
- Category: hdab
- Tags: category:hdab, priority:new

## Extracted Content

 
 
  
 
 
 
 
 
 
M7.4 Draft technical, functional and security 
specifications of Secure Processing 
Environments 
 
TEHDAS2 – Second Joint Action Towards the European Health Data 
Space 
 
 
12 September 2025  
 
 
 
 
 
 
 
 
Co-funded by 
the European Union 
 
 
 

 
 
 
 
 
 
 
                               M7.4 Draft technical, functional and security specifications of Secure Processing Environments 
 1  
 
 
 
0 Document info 
 
0.1 Authors 
 
Lead Author(s) 
Lead organisation  
Heikki Lehväslaiho 
CSC – IT Center for Science, Finland 
Helena Lodenius 
CSC – IT Center for Science, Finland 
Beatriz Barros 
Sciensano, Belgium 
Alexandre Berna 
Health Data Hub, France 
Lucas Bréchot 
Health Data Hub, France 
Zdenek Gütter 
Ministry of Health of the Czech Republic  
Hans Aage Huru 
Norwegian Institute of Public Health, 
Norway 
Yohan Jarosz 
Luxembourg National Data Service, 
Luxembourg 
Todor Kondić 
Luxembourg National Data Service, 
Luxembourg 
Jaakko Lähteenmäki 
VTT Technical Research Centre of 
Finland Ltd, Finland 
Max Martens 
BfArM - Federal Institute for Drugs and 
Medical Devices, Germany 
Minerva Alvarez 
Spanish Ministry of Health 
Juha Pajula 
VTT Technical Research Centre of 
Finland Ltd, Finland 
Thomas Sondag 
Luxembourg National Data Service, 
Luxembourg 
Christophe Trefois 
Luxembourg National Data Service, 
Luxembourg 
Emmi Turunen 
HUS Group, the joint authority for 
Helsinki and Uusimaa, Finland 
 
 
0.2 Keywords 
 
Keywords 
TEHDAS2, Joint Action, Health Data, Health Data Space, Secure 
Processing Environments, SPE Federation, Federated computing 
 
 

 
 
 
 
 
 
 
                               M7.4 Draft technical, functional and security specifications of Secure Processing Environments 
 2  
 
 
 
0.3 Document history 
 
Date 
Version 
Editor 
Change 
Status 
11/10/2024 
0.1 
Helena Lodenius, Heikki 
Lehväslaiho 
Table of Contents 
Draft 
27/06/2025 
0.2 
Heikki Lehväslaiho, Helena 
Lodenius, Beatriz Barros, 
Alexandre Berna, Todor 
Kondić, Jaakko Lähteenmäki, 
Juha Pajula 
Draft to be 
reviewed by the 
Consortium 
Draft 
12/09/2025 
1.0 
Heikki Lehväslaiho, Helena 
Lodenius, Beatriz Barros, 
Jaakko Lähteenmäki 
Document to be 
submitted for 
public 
consultation 
Final 
 
Accepted in Project Steering Group on 12 September 2025.  
 
 
Disclaimer  
Views and opinions expressed in this deliverable represent those of the author(s) only and 
do not necessarily reflect those of the European Union or HaDEA. Neither the European 
Union nor the granting authority can be held responsible for them. 
 
Copyright Notice 
Copyright © 2024 TEHDAS2 Consortium Partners. All rights reserved. For more information 
on the project, please see www.tehdas.eu. 
 
 
 
 

 
 
 
 
 
 
 
                               M7.4 Draft technical, functional and security specifications of Secure Processing Environments 
 3  
 
 
 
Table of contents 
 
 
1 Executive summary ............................................................................................................................. 6 
2 Introduction ........................................................................................................................................ 7 
3 Scope .................................................................................................................................................. 9 
3.1 Legal requirements for EHDS SPE................................................................................................... 9 
3.2 Preliminary life cycle components of SPE ....................................................................................... 9 
4 Core SPE requirements....................................................................................................................... 11 
4.1 Principles .................................................................................................................................... 11 
4.2 User stories ................................................................................................................................ 12 
4.3 Functional requirements ............................................................................................................. 13 
4.3.1 Sensitive data ................................................................................................................................................... 14 
4.3.2 Scientific research ............................................................................................................................................ 15 
4.3.3 Minimum SPE requirements ............................................................................................................................ 17 
4.4 EHDS SPE requirements .............................................................................................................. 19 
4.5 Operational requirements ................................................................................................

---
*Auto-generated from draft-technical-functional-and-security-specifications-of-secure-processing-environments.pdf on 2026-06-09*

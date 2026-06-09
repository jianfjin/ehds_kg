---
wiki_id: "WIKI-For_Health_Data_Access_Bodies_On_The_Imp"
title: "For Health Data Access Bodies On The Implementation Of Secure Processing Environments"
regulation: "Reg. (EU) 2025/327"
category: "hdab"
priority: 0.15
tags: ["category:hdab", "priority:new"]
keywords: ["EHDS", "access", "bodies", "csc", "data", "environments", "guideline", "hdab", "health", "hus", "implementation", "it", "processing", "secure", "spe"]
version: "7.4"
created: "2026-06-09"
updated: "2026-06-09"
priority: 0.15
sources: ["data/source_pdfs/d7.4-technical-specification-for-health-data-access-bodies-on-the-implementation-of-secure-processing-environments.pdf"]
---

# For Health Data Access Bodies On The Implementation Of Secure Processing Environments

Extracted from: `data/source_pdfs/d7.4-technical-specification-for-health-data-access-bodies-on-the-implementation-of-secure-processing-environments.pdf`

## Key Topics

- This document is a guideline under the EHDS framework.
- Category: hdab
- Tags: category:hdab, priority:new

## Extracted Content

 
 
  
 
 
 
 
 
 
 
D7.4 Technical specification for Health Data  
Access Bodies on the implementation of secure 
processing environments 
Technical, functional and security specifications of secure  
processing environments 
 
TEHDAS2 – Second Joint Action Towards the European Health Data 
Space 
 
 
24 February 2026  
 
 
 
 
 
 
Co-funded by 
the European Union 
 

 
 
 
 
 
 
 
                               D7.4 Technical, functional and security specifications of Secure Processing Environments 
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
Krisztina Fekete-Molnar 
Sciensano, Belgium 
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

 
 
 
 
 
 
 
                               D7.4 Technical, functional and security specifications of Secure Processing Environments 
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
02/02/2026 
1.1 
Heikki Lehväslaiho, Helena 
Lodenius, Beatriz Barros, 
Krisztina Fekete-Molnar, 
Jaakko Lähteenmäki, Juha 
Pajula, Anne Heidi Skogholt 
 
Draft D7.4 
Draft 
24/02/2026 
1.2 
Heikki Lehväslaiho, Helena 
Lodenius, Beatriz Barros, 
Krisztina Fekete-Molnar 
D7.4 
Final 
 
Accepted in Project Steering Group on 24 February 2026.  
 
 
Disclaimer  
Views and opinions expressed in this deliverable represent those of the author(s) only and 
do not necessarily reflect those of the European Union or HaDEA. Neither the European 
Union nor the granting authority can be held responsible for them. 
 
Copyright Notice 
Copyright © 2024 TEHDAS2 Consortium Partners. All rights reserved. For more information 
on the project, please see www.tehdas.eu. 
 
 
 
 

 
 
 
 
 
 
 
                               D7.4 Technical, functional and security specifications of Secure Processing Environments 
 3  
 
 
 
Table of contents 
1 Executive summary ............................................................................................................................. 6 
2 Introduction ........................................................................................................................................ 7 
3 Scope .................................................................................................................................................. 9 
4 Generic SPE ....................................................................................................................................... 11 
4.1 SPE as service ............................................................................................................................. 11 
4.1.1 Principles .......................................................................................................................................................... 11 
4.1.2 Sensitive data protection requirements .......................................................................................................... 13 
4.1.3 Enabling needs of scientific research ............................................................................................................... 14 
4.1.4 Stand-alone SPE ................................................................................................................................................ 16 
4.2 SPE federation ............................................................................................................................ 20 
4.2.1 SPE federation requirements ................................................................................

---
*Auto-generated from d7.4-technical-specification-for-health-data-access-bodies-on-the-implementation-of-secure-processing-environments.pdf on 2026-06-09*

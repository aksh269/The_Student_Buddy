# 🚀 Project Context: Student Buddy

This repository contains the current data preparation work for **Student Buddy**, a chatbot for DAIICT students.

### 📋 Project Details
- **Institution:** DAIICT
- **Chatbot Name:** Student Buddy
- **Faculty Mentor:** Dr. Amit Mankodi (Amit Mankodi Sir)
---

## 🛠️ Scraper Scripts

The workspace contains scripts used to harvest and update the raw data from the intranet and official portal:
- [`scraper.py`](./scraper.py): A multi-threaded web crawler that scans the DA-IICT intranet portal, builds an `inventory.csv` list of academic documents, and downloads them.
- [`scrape_programs_of_study.py`](./scrape_programs_of_study.py): A web scraper that fetches curricula details, descriptions, downloadable PDFs/DOCs, and links from the official DA-IICT Programs of Study site, compiling them into organized category folders.

---

## 📂 Detailed Knowledge Base Directory Structure

All crawled files are normalized into Markdown format and organized under the main directory: [`daiict_document processed`](./daiict_document%20processed).

### 📋 Knowledge Base Dashboard

| Directory Category | Path (Relative Link) | Files / Sub-folders | Summary of Covered Knowledge |
| :--- | :--- | :--- | :--- |
| **Academic** | [`/daiict_document processed/Academic`](./daiict_document%20processed/Academic) | 6 root files, 3 folders | Course booklets (Autumn/Winter), academic requirements, and internship policies. |
| **Academic Rules & Guidelines** | [`/daiict_document processed/Academic Rules-Guidelines`](./daiict_document%20processed/Academic%20Rules-Guidelines) | 8 root files, 3 folders | Conduct codes, vehicle policies, exam regulations, and project/thesis guidelines. |
| **Administration** | [`/daiict_document processed/administration`](./daiict_document%20processed/administration) | 22 files | Governance policies, TA/TF guidelines, employee terms, and holiday schedules. |
| **Admissions** | [`/daiict_document processed/Admissions`](./daiict_document%20processed/Admissions) | 4 major folders | Eligibility, FAQs, seat criteria for UG, PG, Dual Degrees, and PhD. |
| **Announcements** | [`/daiict_document processed/Announcement`](./daiict_document%20processed/Announcement) | 4 root files, 6 folders | Payment manuals, Moodle settings, ID cards, and medical insurance processes. |
| **Faculty Profiles** | [`/daiict_document processed/faculty`](./daiict_document%20processed/faculty) | 9 root files, 5 folders | Detailed profile directories for Regular, Adjunct, Practice, and Int'l faculty. |
| **Placements** | [`/daiict_document processed/placements`](./daiict_document%20processed/placements) | 12 files | Recruitment procedures, company rules (Dream categories), and placement stats. |
| **Programs of Study** | [`/daiict_document processed/programs_of_study`](./daiict_document%20processed/programs_of_study) | 4 folders | Detailed course lists and curricula for all degrees offered. |
| **Scholarships** | [`/daiict_document processed/scholarships DAIICT 2026`](./daiict_document%20processed/scholarships%20DAIICT%202026) | 15 files | Financial aid guidelines (DAFS, Cybage, Government, and Merit-cum-Means). |
| **Student Services** | [`/daiict_document processed/student_services`](./daiict_document%20processed/student_services) | 13 root files, 5 folders | Hostel rules, committees (IEEE, Grievances), contacts, and social media links. |

---

### 1. 🎓 Academic
- **Path:** [`daiict_document processed/Academic`](./daiict_document%20processed/Academic)
- **Overview:** Houses registration guides, official notices, graduation rules, and comprehensive curriculum details.
- **Detailed Structure:**
  - **Core Policies:** Handles registration notices, Student Document Services, and committee guidelines like [`Committees_T&R_2024-25 updated.md`](./daiict_document%20processed/Academic/Committees_T%26R_2024-25%20updated.md) and [`Minor_RAS_Policy_Document.md`](./daiict_document%20processed/Academic/Minor_RAS_Policy_Document.md).
  - [`academic requirement`](./daiict_document%20processed/Academic/academic%20requirement): Contains 17 files detailing course structures and academic requirements for B.Tech (ICT, ICT-CS, MnC, EVD), M.Sc (IT, DS, AA), M.Tech (EC, ICT, CS&ML), M.Des (CD, IUxD), and PhD (HSS & Design, Engineering Science) streams.
  - [`Course`](./daiict_document%20processed/Academic/Course):
    - [`Course_Files_Autumn_2025_26`](./daiict_document%20processed/Academic/Course/Course_Files_Autumn_2025_26): Includes the Autumn semester course booklet and a subfolder of **109 individual course files** (e.g. CS374, CT204, DS603) detailing syllabus, instructors, and evaluation criteria.
    - [`Course_Files_Winter_2025_26`](./daiict_document%20processed/Academic/Course/Course_Files_Winter_2025_26): Includes the Winter semester course booklet and a subfolder of **94 individual course files** (e.g. CS301, CT216, IT549).
  - [`UG Internships`](./daiict_document%20processed/Academic/UG%20Internships): Contains materials for Summer Research, Industrial, and Rural internships, detailing safety guidelines, host organization reports (e.g., Seva Mandir, Prayas), FAQ packets, and student evaluation rubrics.

### 2. 📜 Academic Rules & Guidelines
- **Path:** [`daiict_document processed/Academic Rules-Guidelines`](./daiict_document%20processed/Academic%20Rules-Guidelines)
- **Overview:** General code of conduct, medical benefits, and project workflows.
- **Detailed Structure:**
  - **General Guidelines:** Policies on late registration fines, student code of conduct, vehicle rules, and program transfers.
  - [`Examinations Related`](./daiict_document%20processed/Academic%20Rules-Guidelines/Examinations%20Related): Exam rules, malpractice guidelines, and written exam guidelines for candidates with benchmark disabilities.
  - [`Honours-Minor Policy`](./daiict_document%20processed/Academic%20Rules-Guidelines/Honours-Minor%20Policy%28Minor_Robotic%20and%20Autonomous%29): Policies for the Robotic and Autonomous Systems minor.
  - [`Project-Thesis Guidelines`](./daiict_document%20processed/Academic%20Rules-Guidelines/Project-Thesis%20Guidelines): Deliverable rules for B.Tech Projects/Mini-Projects, M.Sc DS projects, and M.Tech Project/Thesis.

### 3. 🏢 Administration
- **Path:** [`daiict_document processed/administration`](./daiict_document%20processed/administration)
- **Overview:** Comprises 22 documentation files handling general institutional governance and policies.
- **Detailed Structure:**
  - Alumni privacy rules, employee service conditions, e-governance policies, travel policy, and TA/TF (Teaching Assistant/Fellow) policy frameworks.
  - Plagiarism prevention rules, public self-disclosures (2025), and GSIRF accreditation status details.
  - Grievance Redressal Authorities lists for students, faculty, and staff.

### 4. 📝 Admissions
- **Path:** [`daiict_document processed/Admissions`](./daiict_document%20processed/Admissions)
- **Overview:** Contains admission handbooks, eligibility rules, and admission FAQs.
- **Detailed Structure:**
  - **Undergraduate:** Admissions guidelines for B.Tech CS-AI, ECE, EVD, Honours ICT, ICT, and MnC (broken down by Gujarat Category, All India Category, NRI/Foreign, and BTech FAQs).
  - **Postgraduate:** All India and Gujarat category details for M.Tech ICT, and overview documents for M.Sc IT, M.Sc DS, M.Sc AA, and M.Des IUxD.
  - **Dual Degrees & PhDs:** Admission rules for BS-MS (IT, DS-AI) and Ph.D (Regular, Part-Time, Visvesvaraya Scheme).

### 5. 📢 Announcements & Resources
- **Path:** [`daiict_document processed/Announcement`](./daiict_document%20processed/Announcement)
- **Overview:** Student announcements, payment procedures, and welfare forms.
- **Detailed Structure:**
  - **General Guidelines:** Charges for documents, emergency procedures, student ID card workflows, and leave policies.
  - [`Fees-Payment`](./daiict_document%20processed/Announcement/Fees-Payment): Step-by-step instructions on paying fee adjustments through UniRP.
  - [`ICT Policy`](./daiict_document%20processed/Announcement/ICT%20Policy): Guidelines on printing quotas and computer use on campus.
  - [`IT Resouce Guide`](./daiict_document%20processed/Announcement/IT%20Resouce%20Guide): Registration guidelines for Moodle and remote network access.
  - [`Medical Insurance_Students`](./daiict_document%20processed/Announcement/Medical%20Insurance_Students): Group mediclaim policy, claim form, standard procedures, and accident coverage details.
  - [`Semester_Registration`](./daiict_document%20processed/Announcement/Semester_Registration): UniRP portal registration guides.

### 6. 🧑‍🏫 Faculty Profiles
- **Path:** [`daiict_document processed/faculty`](./daiict_document%20processed/faculty)
- **Overview:** Profiles, Boards of Studies, dean details, tenure regulations, and lists of teaching fellows.
- **Detailed Structure:**
  - [`regular`](./daiict_document%20processed/faculty/regular): **76 files** representing profiles and research domains of all full-time regular faculty (e.g. Dr. Amit Mankodi, Dr. Aditya Tatu, Dr. Maniklal Das).
  - [`adjunct`](./daiict_document%20processed/faculty/adjunct): **29 profiles** of visiting/adjunct faculty.
  - [`international_adjunct`](./daiict_document%20processed/faculty/international_adjunct): **22 profiles** of international professors affiliated with DA-IICT.
  - [`professor_of_practice`](./daiict_document%20processed/faculty/professor_of_practice): **11 profiles** of active industry leaders instructing specialized classes.
  - [`distinguished`](./daiict_document%20processed/faculty/distinguished): Profiles of distinguished faculty.

### 7. 💼 Placements
- **Path:** [`daiict_document processed/placements`](./daiict_document%20processed/placements)
- **Overview:** Job placement cell organization, rules, and statistics.
- **Detailed Structure:**
  - Includes placement cell guidelines (v1 & v2), placement brochures (2025-26), recruitment steps, and salary placement statistics (2025-26).
  - Company categorization policies (classification of Dream, Super Dream, and exceptions), candidate offer rejection terms, and job switching rules.
  - IPRS Placement Report (2023-24).

### 8. 📖 Programs of Study (Curricula)
- **Path:** [`daiict_document processed/programs_of_study`](./daiict_document%20processed/programs_of_study)
- **Overview:** Explicit program structure and curriculum layouts.
- **Detailed Structure:**
  - [`undergraduate_programs`](./daiict_document%20processed/programs_of_study/undergraduate_programs): Curriculum rules for B.Tech CS-AI, B.Tech ECE-AI, B.Tech EVD, B.Tech Honours ICT with Computational Science, B.Tech ICT, and B.Tech MnC.
  - [`postgraduate_programs`](./daiict_document%20processed/programs_of_study/postgraduate_programs): Layouts for M.Des (CD, IUxD), M.Sc (AA, DS, IT), and M.Tech ICT.
  - [`dual_degree_programs`](./daiict_document%20processed/programs_of_study/dual_degree_programs): Structuring of the BS-MS in IT and BS-MS in DS & AI.
  - [`doctoral_program`](./daiict_document%20processed/programs_of_study/doctoral_program): PhD program details and parameters.

### 9. 💰 Scholarships
- **Path:** [`daiict_document processed/scholarships DAIICT 2026`](./daiict_document%20processed/scholarships%20DAIICT%202026)
- **Overview:** Comprehensive financial assistance details.
- **Detailed Structure:**
  - Includes 15 files covering B.Tech DAFS (Dhirubhai Ambani Foundation Scholarship), Institute fellowships, Merit-cum-Means terms, and program-wise fellowships (M.Des, M.Sc AA/DS/IT).
  - Outlines Gujarat Government financial aid programs, Cybage Khushboo, HEST, Jai Jhulelal, and Satnaam WaheGuruji scholarships.

### 10. 🏫 Student Services & Campus Life
- **Path:** [`daiict_document processed/student_services`](./daiict_document%20processed/student_services)
- **Overview:** Activities, medical systems, contact info, rules, and student organizations.
- **Detailed Structure:**
  - Dean of Students rules, holiday lists (2026), first-year onboarding guidelines, and campus events.
  - [`alumni`](./daiict_document%20processed/student_services/alumni): Association rules, document requests, ID card processes, and alumni drives.
  - [`committees`](./daiict_document%20processed/student_services/committees): Charters for E-Cell (Entrepreneurship Cell), Grievance Redressal Cells, IEEE Student Branch, and the Internal Complaints Committee (ICC).
  - [`contact`](./daiict_document%20processed/student_services/contact): Administrative contact information, emergency phone lines, and directions/location contacts.
  - [`rules`](./daiict_document%20processed/student_services/rules): Student leave policy, hostel rules and regulations, exam rules, disciplinary codes, vehicle guidelines, and UGC anti-ragging regulations.
  - [`social_media`](./daiict_document%20processed/student_services/social_media): Integration details for Facebook, Instagram, LinkedIn, Twitter, and YouTube channels.

---

## 🤖 Data Ingestion Guidelines for Student Buddy
1. **Clean Markdown Format:** All documentation files have been cleaned to minimize noise (script codes, styling elements, forms, and buttons are removed).
2. **Strict Hierarchy:** Section titles (`#`, `##`, etc.) match structural divisions, ensuring splitters (e.g., recursive character text splitters) can partition files cleanly.
3. **Cross-Linking:** Files contain relative links and references for RAG context verification.

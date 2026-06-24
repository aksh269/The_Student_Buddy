# Student Buddy - DAIICT (Data Preparation Status)

This repository contains the current data preparation work for **Student Buddy**, a chatbot for DAIICT students.

Current project context:
- Institution: DAIICT
- Chatbot name: Student Buddy
- Faculty mentor: Amit Mankodi Sir

## What has been done so far

1. Collected institutional documents into a raw archive.
2. Created a processed markdown dataset for chatbot-friendly ingestion.
3. Preserved directory structure in processed data for traceability.
4. Kept both raw and processed datasets available in this workspace.

## Data Description (Exact Coverage)

### Academic
- Course data includes both Autumn 2025-26 and Winter 2025-26 content.
- For each semester, data includes the semester course booklet and individual course files.
- Academic requirement documents include program-wise regulations for UG and PG tracks such as BTech (ICT, ICT-CS, EVD, MnC), MSc (AA, IT, DS), MTech (ICT, EC, CS&ML), MDes (CD, IUxD), and PhD streams.
- Academic section also contains institute-level academic notices and references such as registration notices, student document service information, committee circulars, and policy references.
- UG internship data is present in three major blocks: guidelines, industrial internship material, and rural internship material.

### Academic Rules-Guidelines
- This section covers institute policies and rules including student conduct, vehicle rules, international student guidelines, medical facilities, and late registration policy.
- It includes examination-related rules and malpractice guidelines, including provisions related to benchmark disabilities.
- It includes project and thesis related policy documents.
- It includes honours/minor policy references, including the Minor in Robotic and Autonomous Systems.
- It includes operational student governance documents such as leave and transfer-related rules.

### Announcement
- This section includes student-facing operational announcements.
- It covers e-campus orientation materials, semester registration instructions, fee payment guides, ICT policy notes, and IT resource usage guides.
- It includes student welfare and compliance documents such as medical insurance process documents, emergency procedure documents, and ID card related instructions.

### Scholarships
- This section includes scholarship and fellowship information across UG and PG programs.
- It includes BTech, BS-MS, MDes, and MSc scholarship documents.
- It also includes institute and external support options such as government assistance and program-specific sponsorship/fellowship notices.

### Raw and Processed Relationship
- Raw data contains source files collected from institutional documents.
- Processed data mirrors this structure in markdown format for downstream chatbot ingestion.
- The processed directory is intended to be the primary knowledge base input for retrieval, chunking, and indexing in Student Buddy.

## Current gap to close

A small set of legacy office-format files still needs full and uniform conversion handling in the pipeline.

## Immediate next step

Use the processed markdown folder (daiict_document processed) as the primary ingestion source for retrieval, chunking, and indexing in Student Buddy.

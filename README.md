# EngiVerify

> AI-assisted document-to-database building, reconciliation, and human validation.

## Overview

EngiVerify is a configurable platform that extracts structured information from engineering documents, compares it with existing records, and directs reviewers to discrepancies and uncertain results.

The platform is designed for workflows involving PDF datasheets, P&IDs, scanned documents, Excel workbooks, CSV files, and structured databases. It supports engineers and document reviewers by reducing repetitive extraction and comparison work while preserving source traceability and human technical authority.

EngiVerify is not an autonomous engineering approval system. Automated extraction, mapping recommendations, normalization, comparison results, confidence scores, and color coding are decision-support tools. The human reviewer remains the final authority.

## Product Category

EngiVerify can be described as an:

- AI-assisted engineering document-to-database builder
- Document intelligence and data reconciliation platform
- Human-in-the-loop technical document validation system
- Intelligent data capture and exception review application

A concise product statement is:

> EngiVerify converts engineering documents into structured, traceable project data, compares that data with existing records, and routes uncertain or inconsistent results to reviewers for validation.

## Core Principles

1. **Source documents remain authoritative.**
2. **Human validation is the final authority.**
3. **AI provides recommendations, not approvals.**
4. **Original files and original values are never overwritten.**
5. **Every accepted result must be traceable to its source.**
6. **The latest verified source version is the only development baseline.**
7. **A representative test record must pass before a full run.**
8. **Document profiles and rules must be versioned and validated.**
9. **Uncertainty must be visible, not hidden.**
10. **New functionality must not regress protected behavior.**

## Why EngiVerify Exists

Vendor-document review can involve hundreds of equipment tags and thousands of PDF pages, images, records, and technical fields. Reviewers may need to compare PDF datasheets and P&IDs with Excel registers or other structured records.

Typical fields include:

- Tag number
- Model number
- Manufacturer
- Line size
- Body size
- Valve type
- Valve rating
- Pressure rating
- CV
- Materials
- Design conditions
- Other equipment-specific technical specifications

Small datasets can be reviewed manually. Larger datasets are slow, repetitive, difficult to validate consistently, and vulnerable to transcription and mapping errors.

EngiVerify shifts reviewer effort from repetitive copying toward discrepancy verification and technical decision-making.

## What the Platform Does

The target workflow is:

1. Create a review project.
2. Upload or select source documents.
3. Analyze PDF and workbook structures.
4. Select a validated document profile or create a draft profile.
5. Detect equipment tags and associated pages.
6. Extract candidate fields with source coordinates.
7. Import existing Excel, CSV, or database records.
8. Recommend source-to-target field mappings.
9. Require the user to review and correct mappings.
10. Normalize values using approved rules.
11. Run one representative test tag or record.
12. Require approval of the test result.
13. Process the full dataset.
14. Prioritize mismatches, missing values, ambiguous mappings, and low-confidence results.
15. Record reviewer decisions and comments.
16. Export controlled reports without modifying the original files.

## Universal Platform Scope

EngiVerify is intended to be universal at the platform level, not universal in automatic interpretation.

The same application can support many document families through validated profiles, including:

- Block-valve datasheets
- Control-valve datasheets
- Instrument datasheets
- Pump and motor datasheets
- P&IDs
- Equipment schedules
- Line lists
- Cable schedules
- Vendor document registers
- Inspection records
- Punch lists

Each materially different document family may require its own:

- Document profile
- Field definitions
- Coordinate regions
- Tag-detection rules
- Page-grouping rules
- Mapping configuration
- Normalization rules
- Comparison settings
- Validation dataset
- Approval record

The platform must never claim guaranteed zero-configuration support for every document.

## Supported Data Flows

The architecture should support:

- PDF to database
- PDF to Excel
- PDF to database comparison
- PDF to Excel comparison
- Excel to Excel comparison
- PDF revision to PDF revision comparison
- Vendor document to project specification comparison
- Structured data import and export

The browser interface is the primary review workspace. Excel remains a supported input and output format.

## Result Categories

The user-facing result categories are:

- **Match:** Source and target values are technically equivalent under approved rules.
- **Mismatch:** Source and target values materially differ.
- **Not Found:** A required source or target value cannot be located.
- **Not Analyzed:** The field was imported but intentionally excluded from comparison.
- **Manual Selection Required:** The mapping is unresolved or insufficiently confident.
- **Extraction Review Required:** The value was extracted with insufficient confidence or conflicting evidence.
- **Error:** The record could not be processed successfully.

Recommended color convention:

- Green: Match
- Yellow: Mismatch
- Pink: Unmapped, unrecognized, or unsuccessfully extracted
- Red: Not Found

Colors guide attention. They do not represent engineering approval.

## Recommended Architecture

```text
Browser Application
    |
    +-- Project and Review Interface
    +-- PDF Viewer and Source Highlighting
    +-- Mapping and Profile Editors
    +-- Exception Review Workspace
    |
Web API
    |
    +-- Authentication and Authorization
    +-- Project Management
    +-- File and Job Management
    +-- Review and Approval Workflow
    |
Processing Services
    |
    +-- Native PDF Text Extraction
    +-- OCR
    +-- Layout and Coordinate Extraction
    +-- Tag Detection and Multi-page Grouping
    +-- Excel and Structured-data Ingestion
    +-- Mapping Recommendation
    +-- Normalization
    +-- Deterministic Comparison
    +-- Reporting
    |
Persistence
    |
    +-- PostgreSQL
    +-- Controlled File or Object Storage
    +-- Audit Log
```

## Recommended Technology Stack

### Frontend

- React
- TypeScript
- PDF.js
- Accessible enterprise data grid
- HTML and CSS component system

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Worker queue for long-running jobs

### Document Processing

- PyMuPDF for native PDF text, coordinates, rendering, and annotations
- pdfplumber as a secondary diagnostic or table extraction engine
- openpyxl for Excel preservation and export
- pandas only for controlled data analysis
- Local OCR such as PaddleOCR or Tesseract
- Optional approved cloud document intelligence provider

### Persistence

- PostgreSQL for shared or production deployments
- SQLite only for a local prototype
- Controlled file server, object storage, or approved enterprise content storage

### Quality and Delivery

- pytest
- Golden-file and regression tests
- Git
- Tagged verified releases
- Continuous integration checks
- Dependency and security scanning

## Repository Structure

```text
.
├── README.md
├── agent.md
├── implementation.md
├── pyproject.toml
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── domain/
│   ├── extraction/
│   ├── ingestion/
│   ├── mapping/
│   ├── normalization/
│   ├── comparison/
│   ├── reporting/
│   ├── review/
│   └── workers/
├── frontend/
│   ├── src/
│   └── tests/
├── profiles/
│   ├── draft/
│   ├── approved/
│   └── retired/
├── rules/
│   ├── draft/
│   ├── approved/
│   └── retired/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── regression/
│   ├── fixtures/
│   └── golden/
├── scripts/
├── docs/
├── migrations/
└── sample_data/
```

Production source documents, confidential vendor files, credentials, generated reports, and local databases must not be committed to the repository.

## Data and Traceability Requirements

For every extracted or compared field, preserve where applicable:

- Project ID
- Document ID and version
- Source file hash
- Tag or record identifier
- Field name
- Original extracted value
- Original target value
- Normalized source value
- Normalized target value
- PDF page
- Source bounding box
- Extraction method
- OCR confidence
- Extraction confidence
- Mapping confidence
- Applied rule IDs and versions
- Comparison status
- Reason for the result
- Reviewer decision
- Reviewer comment
- Review timestamp
- Application version
- Profile version
- Mapping version
- Rule-set version

Identification fields such as tag numbers, model numbers, and equipment IDs must be stored as strings unless an approved schema explicitly states otherwise. Leading zeros must be preserved.

## Security and Privacy

Before cloud OCR or AI services are enabled, confirm:

- Information-security approval
- Data-residency requirements
- Vendor confidentiality restrictions
- Retention and deletion policies
- Access-control requirements
- Encryption requirements
- Logging and audit requirements
- Applicable contracts and regulations

Secrets must be provided through environment variables or an approved secret manager. Never commit credentials, tokens, production connection strings, or confidential source documents.

## Human-in-the-Loop Requirements

The application must require human review for:

- Unresolved mappings
- Low-confidence tag detection
- Low-confidence extraction
- Mismatches
- Not Found results
- New or changed normalization rules
- New document profiles
- Unexpected values
- Final technical acceptance

The system should block a full run when required mappings are unresolved. A full-run result is a review candidate, not an approved engineering record.

## Versioning and Single Source of Truth

Every accepted change must identify:

- Source version
- New version
- Exact requested change
- Modified components
- Protected components
- Test evidence
- Regression result
- Remaining local validation requirements

Use explicit version names and Git tags. Avoid ambiguous names such as `final.py`, `final_new.py`, or `latest2.py`.

A generated or modified version becomes the new master only after local validation and formal acceptance.

## Development Status

The repository now includes a first executable ingestion foundation in addition to the product architecture. Implemented scope is deliberately narrow: immutable source identity/hashing, native-PDF text and coordinate extraction, structured workbook inspection, draft coordinate profiles, and a versioned telecom interchange bundle.

OCR, semantic AI extraction, database persistence, FastAPI services, React review UI, authentication, and production deployment are still roadmap items.

Use the implementation status labels below in issues and pull requests:

- `proposed`
- `in-development`
- `implemented`
- `locally-validated`
- `approved`
- `retired`

## Getting Started

Until the initial project skeleton is implemented, the recommended first actions are:

1. Place the latest verified legacy source in a protected baseline branch or archive.
2. Record its exact version and validation evidence.
3. Add representative, sanitized PDF and workbook fixtures.
4. Convert the completed manual review into golden regression expectations.
5. Create the backend and frontend skeletons.
6. Implement source-file hashing and immutable file handling first.
7. Migrate one validated document profile without changing its expected results.
8. Implement the test-tag gate before full batch processing.
9. Add AI recommendations only after deterministic processing is stable.

See [implementation.md](implementation.md) for the phased delivery plan and [agent.md](agent.md) for coding-agent constraints.

## Contributing

All contributions must:

- Use the latest verified branch or commit as the baseline.
- Make the minimum necessary change.
- Preserve protected functionality.
- Include tests for changed behavior.
- Include regression evidence.
- Avoid unsupported technical equivalence rules.
- Avoid claims of successful execution without evidence.
- Update relevant documentation and version metadata.

## License

No license has been selected in this initial repository specification. Add an approved license before external distribution or third-party reuse.


## Implemented Ingestion Foundation

The first executable release adds:

- SHA-256 source identity and immutable-copy storage behavior.
- Safe source filenames and source-document manifests.
- Native PDF analysis, text-block extraction, and coordinate-region extraction using PyMuPDF.
- Excel/workbook structure and cell ingestion using openpyxl while retaining raw values, formulas, cached values, cell types, and number formats.
- Versioned document-profile validation and deterministic coordinate-based field extraction.
- A stable `engiverify.telecom.v1` interchange bundle for downstream engineering systems.
- JSON Schemas, synthetic tests, and GitHub Actions CI.

The telecom integration boundary is documented in [docs/TELECOM_INTEGRATION.md](docs/TELECOM_INTEGRATION.md).

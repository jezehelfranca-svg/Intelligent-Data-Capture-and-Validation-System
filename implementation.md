# Implementation Plan

## 1. Objective

Build EngiVerify as a configurable, browser-based document-to-database, reconciliation, and human-validation platform.

The first production scope should preserve and formalize the behavior of the latest verified PDF-to-Excel comparison program. The architecture should then support additional document and equipment profiles without rewriting the platform core.

This plan distinguishes between:

- **Platform core:** Shared project, ingestion, extraction, mapping, comparison, review, audit, and reporting capabilities
- **Document profile:** Versioned configuration for a particular document family or layout
- **Rule set:** Approved field-specific normalization and comparison rules
- **Review workflow:** Human checkpoints that prevent uncertain automation from becoming accepted technical data

## 2. Product Outcomes

The implementation should enable users to:

1. Create a controlled review project.
2. Add immutable source PDF and structured-data files.
3. Identify or select a document profile.
4. Extract fields with page and coordinate traceability.
5. Detect tags and group associated pages.
6. Import Excel, CSV, or approved database records.
7. Review top mapping candidates and confirm mappings.
8. Run and approve a representative test tag.
9. Process a complete dataset in controlled jobs or batches.
10. Review discrepancies and low-confidence results beside source evidence.
11. Record corrections, comments, and final human decisions.
12. Export a separate Excel or other approved report.
13. Reproduce a run using recorded versions of files, profiles, mappings, rules, and application code.

## 3. Scope Strategy

### Initial validated scope

Start with one known document family and one known workbook structure from the currently verified process.

The initial release should not attempt to support every equipment type or vendor layout. It should prove that the new architecture reproduces the validated baseline while improving traceability and maintainability.

### Expansion strategy

Add one approved profile at a time. A new profile must include:

- Representative documents
- Expected tags and page groups
- Expected extracted fields
- Mapping expectations
- Approved normalization examples
- Expected comparison results
- Test evidence
- Profile owner and approval status

## 4. Proposed Technology Stack

### Frontend

- React
- TypeScript
- PDF.js
- Accessible component library
- Enterprise data grid with virtual scrolling

### Backend

- Python 3.12 or an organization-approved supported version
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic database migrations
- Background worker system for resource-intensive jobs

### Processing

- PyMuPDF as the primary native PDF engine
- pdfplumber for secondary diagnostics or table cases
- openpyxl for workbook preservation and export
- pandas for controlled analysis only
- Pluggable OCR provider interface
- Local OCR provider as the default where confidentiality requires it
- Optional approved enterprise cloud document-intelligence provider

### Persistence

- PostgreSQL for production
- Approved object or file storage for source and generated files
- SQLite for isolated development only

### Testing and delivery

- pytest
- Frontend unit and component test framework
- Browser end-to-end tests
- Golden-file regression tests
- GitHub Actions or approved CI service
- Dependency, secret, and static-analysis scanning

## 5. Logical Components

### 5.1 Project Service

Responsibilities:

- Project creation and status
- User and role assignment
- Profile and rule-set selection
- Processing-run history
- Review completion status

### 5.2 File Service

Responsibilities:

- Safe upload and storage
- File-type validation
- Strong hashing
- Immutable source handling
- Download and controlled export
- Antivirus or malware scanning integration where available

### 5.3 Document Classification Service

Responsibilities:

- Detect native text availability
- Recommend document type and profile
- Detect unknown or incompatible layouts
- Prevent silent use of an unvalidated profile

### 5.4 PDF Extraction Service

Responsibilities:

- Native text extraction
- Word, line, and block coordinates
- Page rendering
- Coordinate transformations
- Field-region extraction
- Source evidence storage

### 5.5 OCR Service

Responsibilities:

- OCR provider abstraction
- Page-image generation
- OCR result and confidence capture
- Coordinate alignment
- Provider metadata and version recording

### 5.6 Tag and Page Grouping Service

Responsibilities:

- Tag-pattern detection
- Header and coordinate-zone detection
- Multi-page continuation rules
- Multiple-tag-per-page handling
- Manual correction of page groups

### 5.7 Structured Data Ingestion Service

Responsibilities:

- Workbook and worksheet discovery
- Header selection
- Formula and displayed-value handling
- Cell value and type preservation
- Leading-zero preservation
- Selected-column import
- CSV and future database adapters

### 5.8 Mapping Service

Responsibilities:

- Top candidate generation
- Header similarity
- Approved synonyms
- Data-pattern compatibility
- Historical verified mapping signals
- Confidence and rationale
- Manual confirmation and `None of the Above`

### 5.9 Normalization Service

Responsibilities:

- Deterministic approved rules
- Field-specific rule application
- Rule versioning
- Original-value preservation
- Unit conversions only when approved
- Explicit null, blank, formula, and display-value handling

### 5.10 Comparison Service

Responsibilities:

- Exact comparisons
- Approved-equivalence comparisons
- Mismatch classification
- Missing-value classification
- Not-analyzed handling
- Explicit reasons and applied rule IDs

### 5.11 Confidence and Review Service

Responsibilities:

- Separate confidence dimensions
- Threshold configuration
- Review queue generation
- Blocking conditions
- Reviewer decisions and comments
- Reopen and correction history

### 5.12 Reporting Service

Responsibilities:

- Excel output
- Exception-only output
- HTML review summaries
- Audit and run manifests
- Original, normalized, and final values
- Source-page references
- Version information

### 5.13 Audit Service

Responsibilities:

- Append-only activity records
- User action history
- Profile, mapping, and rule changes
- Run creation and completion events
- Review decisions
- Export events

## 6. Data Model

The initial relational model should include the following entities.

### Project

- `id`
- `name`
- `description`
- `status`
- `created_by`
- `created_at`
- `updated_at`

### SourceDocument

- `id`
- `project_id`
- `original_filename`
- `storage_key`
- `sha256`
- `media_type`
- `document_type`
- `document_revision`
- `page_count`
- `is_native_text`
- `created_at`

### StructuredSource

- `id`
- `project_id`
- `original_filename`
- `storage_key`
- `sha256`
- `source_type`
- `workbook_metadata`
- `created_at`

### DocumentProfile

- `id`
- `name`
- `version`
- `equipment_type`
- `vendor`
- `template_revision`
- `configuration`
- `status`
- `approved_by`
- `approved_at`

### FieldDefinition

- `id`
- `canonical_name`
- `display_name`
- `data_type`
- `unit_family`
- `identifier_flag`
- `validation_pattern`

### TagRecord

- `id`
- `project_id`
- `tag_value`
- `normalized_tag_value`
- `page_group`
- `detection_confidence`
- `review_status`

### ExtractedValue

- `id`
- `tag_record_id`
- `field_definition_id`
- `original_value`
- `page_number`
- `bounding_box`
- `extraction_method`
- `ocr_confidence`
- `extraction_confidence`
- `profile_id`
- `profile_version`

### ImportedRecord

- `id`
- `structured_source_id`
- `sheet_name`
- `row_number`
- `record_key`
- `original_values`

### MappingConfiguration

- `id`
- `project_id`
- `name`
- `version`
- `status`
- `configuration`
- `confirmed_by`
- `confirmed_at`

### MappingCandidate

- `id`
- `mapping_configuration_id`
- `source_field_id`
- `target_field`
- `rank`
- `confidence`
- `matched_keywords`
- `reason`

### NormalizationRule

- `id`
- `rule_id`
- `version`
- `applicable_fields`
- `configuration`
- `status`
- `approved_by`
- `approved_at`

### ComparisonResult

- `id`
- `processing_run_id`
- `tag_record_id`
- `field_definition_id`
- `pdf_original_value`
- `target_original_value`
- `pdf_normalized_value`
- `target_normalized_value`
- `status`
- `comparison_confidence`
- `reason`
- `applied_rule_ids`
- `requires_review`

### ReviewDecision

- `id`
- `comparison_result_id`
- `reviewer_id`
- `decision`
- `corrected_value`
- `comment`
- `created_at`

### ProcessingRun

- `id`
- `project_id`
- `run_type`
- `status`
- `application_version`
- `source_commit`
- `profile_version`
- `mapping_version`
- `rule_set_version`
- `started_at`
- `completed_at`
- `error_summary`

### AuditEvent

- `id`
- `project_id`
- `actor_id`
- `event_type`
- `entity_type`
- `entity_id`
- `event_data`
- `created_at`

## 7. Internal Status Model

Use explicit machine-readable statuses. Initial values may include:

```text
MATCH
MISMATCH
NOT_FOUND_SOURCE
NOT_FOUND_TARGET
NOT_ANALYZED
MAPPING_REQUIRED
EXTRACTION_REVIEW_REQUIRED
PROCESSING_ERROR
```

Review states may include:

```text
UNREVIEWED
REVIEW_REQUIRED
APPROVED
CORRECTED
REJECTED
REOPENED
```

Profile and rule states may include:

```text
DRAFT
UNDER_VALIDATION
APPROVED
RETIRED
```

Do not infer approval from a green color or high confidence.

## 8. API Outline

A first API may expose:

```text
POST   /projects
GET    /projects/{project_id}
POST   /projects/{project_id}/documents
POST   /projects/{project_id}/structured-sources
POST   /projects/{project_id}/analyze
GET    /projects/{project_id}/profiles
POST   /projects/{project_id}/profile-selection
GET    /projects/{project_id}/fields
GET    /projects/{project_id}/mapping-candidates
POST   /projects/{project_id}/mappings
POST   /projects/{project_id}/test-runs
GET    /runs/{run_id}
POST   /projects/{project_id}/full-runs
GET    /projects/{project_id}/results
POST   /results/{result_id}/review-decisions
POST   /projects/{project_id}/exports
GET    /exports/{export_id}
```

Long operations should create persistent jobs. The interface should show current status and must not report a job as successful until completion is recorded.

## 9. User Interface Workspaces

### Project Dashboard

- Project metadata
- Exact source files and hashes
- Selected profile and versions
- Mapping and rule versions
- Test-run status
- Full-run status
- Review progress

### Source Analysis

- PDF document list
- Workbook and sheet list
- Header and column analysis
- Native text or OCR indication
- Detected tags and page groups

### Profile Studio

- Page preview
- Draw and edit coordinate regions
- Define labels and patterns
- Configure page and grouping rules
- Validate against representative files
- Save as draft or submit for approval

### Mapping Workspace

- Extracted PDF fields
- Top three target candidates
- Confidence
- Matched keywords
- Recommendation reason
- Manual dropdown
- `None of the Above`
- Import and analyze selections

### Test Tag Workspace

- Representative tag selection
- PDF source highlighting
- Original and normalized values
- Status and color validation
- Mapping and extraction corrections
- Approval gate for the full run

### Comparison Workspace

- Filterable result grid
- Source and target values
- Normalized values
- Result and reason
- Separate confidence indicators
- PDF viewer with source highlighting
- Reviewer correction and comment controls

### Report Center

- Full Excel export
- Exception-only export
- Run manifest
- Profile and rule report
- Audit export subject to permissions

## 10. Delivery Phases

### Phase 0: Baseline and Governance

Deliverables:

- Exact latest verified source identified
- Protected copy or release tag
- Application version recorded
- Representative sanitized inputs
- Completed manual review converted into expected outputs
- Protected-feature inventory
- Initial risk register

Exit criteria:

- The verified baseline is reproducible.
- Inputs and expected results are available for regression testing.
- No implementation begins from an assumed or conversationally remembered version.

### Phase 1: Repository and Test Foundation

Deliverables:

- Backend and frontend skeletons
- Development configuration
- CI checks
- Unit-test structure
- Regression fixture structure
- Secret and dependency scanning
- Version endpoint and UI version display

Exit criteria:

- The project builds in the approved development environment.
- Automated checks run on pull requests.
- Version identity is visible and testable.

### Phase 2: Immutable Source Ingestion

Deliverables:

- Project creation
- PDF and workbook upload
- Safe filename handling
- Strong file hashing
- Immutable storage behavior
- Source metadata display

Exit criteria:

- Original files are never overwritten.
- Duplicate or changed inputs can be detected through hashes.
- Unauthorized file access is blocked.

### Phase 3: Baseline Extraction and Excel Ingestion

Deliverables:

- Native PDF extraction
- Coordinate capture
- Initial OCR routing
- Workbook and sheet detection
- Header analysis
- String-preserving identifier import
- Leading-zero tests

Exit criteria:

- Baseline source documents reproduce expected raw values.
- Workbook integrity tests pass.
- Identifiers preserve original representation.

### Phase 4: Profile and Tag Grouping

Deliverables:

- Versioned document profiles
- Coordinate-region configuration
- Tag patterns
- Multi-page grouping
- Manual page-group correction
- Profile validation status

Exit criteria:

- Baseline tags and page groups match golden expectations.
- An unapproved profile cannot be silently used as trusted configuration.

### Phase 5: Mapping Workflow

Deliverables:

- Target column listing
- Top-three candidate recommendation
- Keyword and synonym scoring
- Data-pattern compatibility
- Confidence and rationale
- Manual selection
- `None of the Above`
- Blocking unresolved mapping state
- Save and load configuration

Exit criteria:

- Baseline mapping behavior is reproduced.
- Unresolved mandatory mappings block full processing.
- Saved valid mappings reload without loss.

### Phase 6: Rules and Deterministic Comparison

Deliverables:

- Versioned normalization engine
- Original-value preservation
- Approved equivalence rules
- Null and formula handling
- Explicit result statuses
- Reason and applied-rule capture

Exit criteria:

- Golden comparison results match the validated manual review.
- Unsupported AI-generated equivalence cannot enter production automatically.

### Phase 7: Test Tag and Full Processing

Deliverables:

- Test-tag selection and run
- Test result approval gate
- Full-run job creation
- Batch processing
- Progress and error logging
- Safe retry behavior

Exit criteria:

- Full processing cannot start without required configuration and test approval.
- Batch size does not change final results.
- Interrupted jobs do not corrupt accepted results.

### Phase 8: Review Interface and Source Evidence

Deliverables:

- Side-by-side PDF and result view
- Page navigation
- Coordinate highlighting
- Exception queue
- Reviewer decisions and corrections
- Comments and history
- Non-color status labels

Exit criteria:

- Every reviewable result links to available source evidence.
- Reviewer actions are auditable.
- Low-confidence and exception states are clearly visible.

### Phase 9: Reporting and Export

Deliverables:

- Separate Excel output
- Original and normalized values
- Result, reason, confidence, and source location
- Version and run metadata
- Exception-only report
- Export audit event

Exit criteria:

- Original input workbook remains unchanged.
- Reports match approved layout and color conventions.
- A report can be traced back to exact inputs and configuration versions.

### Phase 10: AI-Assisted Recommendations

Deliverables:

- Pluggable recommendation provider
- Semantic mapping support
- Profile and rule suggestions
- Model/provider metadata capture
- Human acceptance and rejection controls
- Evaluation dataset and threshold testing

Exit criteria:

- AI can be disabled without breaking deterministic processing.
- AI output is stored as a candidate, not final truth.
- Recommendation quality is measured on approved validation data.

### Phase 11: Additional Document Profiles

Deliverables:

- Second equipment or document type
- Profile-specific validation dataset
- Cross-profile regression suite
- Profile approval workflow

Exit criteria:

- The same platform core supports materially different profiles.
- The original profile remains regression-safe.

## 11. Acceptance Criteria

The initial production release is acceptable when:

- The explicitly identified verified baseline was used.
- Original PDF and structured-data files remain unchanged.
- The platform reproduces the validated baseline results.
- PDF extraction is operational.
- Excel ingestion and preservation are operational for the approved workbook scope.
- Tag extraction and multi-page grouping are operational.
- Mapping candidates and manual selection are operational.
- Mappings can be saved and loaded.
- Test-tag processing is operational and gates the full run.
- Full comparison is operational.
- Approved equivalent values are handled deterministically.
- Defined statuses and colors are retained.
- Low-confidence and unresolved results enter manual review.
- HTML controls call the correct backend functions.
- Reports are saved separately.
- Application, profile, mapping, and rule versions are visible.
- The complete regression suite passes.
- Local validation is completed before release promotion.

## 12. Performance Strategy

Performance work must preserve result quality.

Recommended techniques:

- Extract each source page once per run.
- Cache immutable extraction artifacts by file hash and engine version.
- Reuse confirmed profile coordinates.
- Process records in deterministic batches.
- Use database indexes for project, tag, field, status, and review state.
- Use virtual scrolling for large review grids.
- Separate interactive API requests from heavy processing jobs.
- Record timing by pipeline stage.
- Add cancellation and safe retry controls.

Performance examples from previous work must be described as observations, not guarantees. Establish benchmarks with representative local datasets.

## 13. Security Controls

Minimum controls:

- Authentication
- Role-based authorization
- Project-level access control
- Encrypted transport
- Approved encryption at rest
- Secret management
- File-type, size, and content validation
- Malware scanning where available
- Audit logging
- Dependency scanning
- Secure error handling
- Backup and restore procedure
- Data-retention and deletion procedure

Potential roles:

```text
Administrator
Profile Maintainer
Technical Reviewer
Project Reviewer
Read-only Auditor
```

Profile approval and final technical acceptance should require explicitly authorized roles.

## 14. Risks and Mitigations

### Incorrect field mapping

Mitigation:

- Top candidate display
- Confidence and rationale
- Mandatory human confirmation
- Test-tag gate

### PDF layout change

Mitigation:

- File and template checks
- Profile compatibility rules
- Layout fingerprinting
- Draft profile workflow

### Adjacent-field over-extraction

Mitigation:

- Field-specific bounding boxes
- Label-value validation
- Source highlighting
- Representative profile tests

### OCR error

Mitigation:

- OCR confidence
- Native text preference
- Alternative provider option
- Human review for weak results

### Unsupported normalization

Mitigation:

- Approved, versioned deterministic rules
- Draft state for suggestions
- Rule-level tests

### Version regression

Mitigation:

- Explicit baseline
- Git release tags
- Protected branches
- Golden regression suite
- Minimal-change policy

### Confidential data leakage

Mitigation:

- Local provider option
- Cloud-provider approval process
- Access control
- No production files in Git
- Data-retention controls

### False impression of autonomous approval

Mitigation:

- Clear user-interface wording
- Separate review state
- Mandatory human decision
- Audit trail
- No approval inferred from color or confidence

## 15. Definition of a Verified Release

A release is verified only when:

1. It is built from an identified commit.
2. Its application version is visible.
3. Database migrations are recorded.
4. Unit, integration, security, and regression checks pass for the approved scope.
5. Golden outputs are reviewed.
6. Representative local source files are processed successfully.
7. Original files are confirmed unchanged.
8. Required technical reviewers accept the results.
9. Known limitations are documented.
10. The release is tagged and archived for rollback.

A generated build, pull request, or AI-produced source file is not a verified release by itself.

## 16. Immediate Repository Backlog

Create issues for:

1. Record the latest verified baseline commit and application version.
2. Add confidentiality-safe validation fixtures.
3. Define golden expected results from the completed manual review.
4. Create the backend package structure.
5. Create the frontend application structure.
6. Add CI, test, lint, dependency, and secret checks.
7. Implement source file hashing and immutable storage.
8. Define the initial database schema and migrations.
9. Implement native PDF text and coordinate extraction.
10. Implement workbook structure analysis with identifier preservation.
11. Define the first versioned document profile format.
12. Implement tag detection and multi-page grouping.
13. Implement mapping candidate and manual selection workflows.
14. Implement deterministic normalization and comparison.
15. Implement the test-tag approval gate.
16. Implement PDF source highlighting.
17. Implement separate Excel export.
18. Add regression tests for every protected feature.
19. Document security and deployment decisions.
20. Validate the first end-to-end release locally before promotion.

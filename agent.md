# Agent Instructions

## Purpose

This file defines mandatory instructions for AI coding agents and automated contributors working in this repository.

The product is a human-in-the-loop engineering document-to-database and validation platform. Changes may affect technical document interpretation, traceability, file integrity, and reviewer decisions. Agents must prioritize correctness, minimal change, explainability, and regression prevention over speed or code simplification.

## Authority Order

Use the following authority order when sources conflict:

1. The exact latest verified source commit or release explicitly identified for the task
2. Approved acceptance criteria for the requested change
3. Existing regression tests and golden expected outputs
4. Approved document profiles and normalization rules
5. Current repository documentation
6. Conversation context and informal notes

Conversation history, cached snippets, older branches, and remembered code are never valid substitutes for the explicitly identified baseline.

## Mandatory Task Header

Every change request should identify:

```text
Latest verified baseline: [COMMIT, TAG, OR RELEASE]
Source application version: [VERSION]
New application version: [VERSION]
Requested change: [PRECISE CHANGE]
Protected behavior: [LIST]
Acceptance criteria: [LIST]
Validation fixtures: [LIST]
```

If the baseline is not explicitly identifiable, do not guess. Limit work to documentation, analysis, or a proposed patch plan and clearly state that executable changes cannot be treated as release-ready.

## Non-Negotiable Product Rules

Agents must preserve these rules:

- Human validation is the final authority.
- AI recommendations must never become automatic engineering approvals.
- Original source files must never be overwritten.
- Original extracted and imported values must be preserved.
- Normalized values must be separate from original values.
- Full processing must not begin when mandatory mappings remain unresolved.
- A representative test tag or record must be supported before a full run.
- Low-confidence, mismatched, missing, ambiguous, and unexpected results must be reviewable.
- Every result must remain traceable to its source document and location when available.
- Identification values must preserve leading zeros and string semantics.
- Unsupported technical equivalence rules must not be invented.
- Colors and confidence scores must not be presented as technical approval.
- New profiles and rules must remain draft until validated and approved.

## Protected Features

Unless the task explicitly and narrowly changes one of these features, preserve it unchanged:

- PDF file selection and controlled storage
- Excel file selection and loading
- Workbook and worksheet detection
- Header and column analysis
- PDF structure analysis
- Native PDF text extraction
- OCR routing
- Tag-number extraction
- Multi-page tag grouping
- Coordinate-based field extraction
- Source page and bounding-box traceability
- PDF-to-target mapping
- Multiple mapping candidates
- Confidence scoring
- Manual mapping selection
- Test-tag processing
- Full-tag processing
- Original-value preservation
- Equivalent-value normalization
- Match classification
- Mismatch classification
- Not Found classification
- Not Analyzed classification
- Manual Selection Required classification
- Extraction Review Required classification
- Status color convention
- Mapping-configuration save and load
- Document-profile save and load
- HTML interface
- Frontend-to-backend integration
- Report generation
- Separate output-file saving
- Audit logging
- Version display

## Change Procedure

Before editing:

1. Read the complete files relevant to the change.
2. Confirm the baseline commit, tag, or source version.
3. Identify the smallest set of functions and files requiring change.
4. Identify protected functions and workflows that must remain unchanged.
5. Locate existing tests, fixtures, profiles, migrations, and API contracts.
6. Record assumptions and known validation gaps.

During editing:

1. Change only the minimum code required.
2. Prefer existing abstractions and libraries.
3. Do not rewrite working modules without explicit authorization.
4. Do not rename, delete, move, simplify, or reorganize unrelated functions.
5. Do not alter result semantics or colors as a side effect.
6. Do not silently change schemas, APIs, profile formats, or mapping files.
7. Add a migration and compatibility plan for intentional schema changes.
8. Preserve backward compatibility with valid saved configurations whenever practical.
9. Mark significant changed sections in the change log, not with excessive inline comments.
10. Keep domain rules outside presentation code.

After editing:

1. Run focused unit tests.
2. Run relevant integration tests.
3. Run the protected regression suite.
4. Compare golden outputs where applicable.
5. Verify that input files remain unchanged.
6. Verify that outputs are written separately.
7. Verify frontend controls still call the intended API operations.
8. Verify saved profiles and mappings still load.
9. Review the diff for unrelated changes.
10. Update application version and documentation when required.
11. Report tests actually executed and their results.
12. State anything that still requires local or technical validation.

Never claim execution, test success, accuracy, or release readiness without evidence.

## AI Usage Boundaries

AI may assist with:

- Mapping candidate generation
- Header and label similarity
- Document-profile suggestions
- Field-location suggestions
- Extraction-failure explanations
- Candidate normalization rules
- Discrepancy summaries
- Code generation and test generation

AI must not independently finalize:

- Engineering acceptance
- Source-to-target mapping
- Technical equivalence rules
- Profile approval
- Rule activation
- Release promotion
- Source baseline selection
- Final database values

Any generative model output that affects technical data must be stored as a candidate with model/provider metadata, confidence or rationale where available, and a human review state.

## Normalization Rules

Normalization must be deterministic in production.

Each rule must have:

- Stable rule ID
- Version
- Applicable field types
- Input examples
- Expected canonical value
- Technical rationale
- Approver or approval reference
- Effective date
- Status

Agents must not add equivalence rules based only on intuition or language-model output. A suggested rule may be added in draft status with tests, but it must not become active without technical approval.

## Confidence Rules

Keep confidence dimensions separate when possible:

- Document-type confidence
- Tag-detection confidence
- OCR confidence
- Extraction confidence
- Mapping confidence
- Comparison confidence

Do not combine these into a misleading single score without a documented and validated method. An exact string comparison does not override weak extraction confidence.

## File Integrity

Required controls:

- Treat uploaded source files as immutable.
- Calculate and store a strong hash for each source file.
- Write generated artifacts to separate output locations.
- Prevent path traversal and unsafe filenames.
- Never commit production or confidential documents.
- Sanitize or synthesize repository fixtures.
- Preserve macro-enabled files when supported, and clearly report unsupported workbook features.

## Database and Schema Changes

For database changes:

- Use versioned migrations.
- Do not edit applied migrations.
- Include downgrade behavior when safe and practical.
- Preserve original values and provenance.
- Avoid destructive changes unless explicitly approved and backed up.
- Represent tags, model numbers, and similar identifiers as strings.
- Use explicit enumerations or controlled values for statuses.
- Record application, profile, mapping, and rule versions with each processing run.

## API Changes

For API changes:

- Maintain typed request and response models.
- Validate all inputs.
- Return explicit error codes and actionable messages.
- Avoid exposing internal stack traces or secrets.
- Preserve compatible endpoints unless a breaking change is approved.
- Update API tests and frontend clients together.
- Make long-running processing asynchronous at the application level through jobs, without presenting an incomplete job as a completed result.

## Frontend Changes

The browser interface must preserve:

- File selection
- Structure analysis
- Profile selection
- Mapping controls
- Import and analyze selections
- Test-tag controls
- Full-run controls
- Progress and status messages
- Error messages
- PDF source highlighting
- Original and normalized values
- Confidence visibility
- Review and correction controls
- Separate export controls

Follow accessible interaction patterns. Do not rely on color alone to communicate status.

## Testing Requirements

Every behavior change should include the applicable tests:

### Unit tests

- Parsing
- Normalization
- Mapping scoring
- Comparison status
- Confidence thresholds
- Coordinate transformations

### Integration tests

- PDF extraction to stored fields
- Workbook ingestion to stored records
- Mapping confirmation to test-tag processing
- Full run to report export
- Profile and mapping save/load
- Frontend API contracts

### Regression tests

- Previously validated manual-review dataset
- Golden extracted values
- Golden statuses and status colors
- Preserved leading zeros
- Multi-page tag grouping
- Original workbook integrity
- Saved-configuration compatibility

### Security tests

- File-name and path handling
- Upload type and size validation
- Authentication and authorization
- Tenant or project isolation where applicable
- Secret handling
- Dependency scanning

## Required Pull Request Summary

Every pull request should include:

```text
Base version:
New version:
Requested change:
Files changed:
Functions or components changed:
Protected behavior reviewed:
Tests executed:
Test results:
Golden-output differences:
Schema or API compatibility impact:
New dependencies:
Security considerations:
Known limitations:
Local validation still required:
Rollback method:
```

## Prohibited Actions

Agents must not:

- Choose an older or remembered baseline.
- Rewrite the entire application for a narrow change.
- Remove working features to simplify implementation.
- Change unrelated behavior.
- Overwrite original PDF, Excel, or database input.
- Mutate original source values during normalization.
- Auto-approve low-confidence results.
- Hide unresolved mappings.
- Invent unsupported equivalence rules.
- Add confidential files or secrets to Git.
- Claim universal accuracy.
- Claim tests were run when they were not.
- Promote a generated version as verified without local evidence.

## Definition of Done

A change is complete only when:

- The explicitly identified baseline was used.
- The requested behavior is implemented.
- Acceptance criteria are satisfied.
- Protected features remain available.
- Required tests pass.
- Regression output is reviewed.
- Source files remain unchanged.
- Output remains separately saved.
- Version and change log are updated where required.
- Remaining validation needs are stated.
- A human reviewer accepts the change for the intended environment.

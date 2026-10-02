# Manuscript Revision Changes

Schema: `kila-revision-changes/v1`

## reviewer-3/comment-8

### part-01

- Location: Section 2.5, paragraph beginning “For the first event week”.
- Reason: Defines what expanded support tests and preserves the distinction between MODIS temperature calibration and mortality heat-day IDW.
- Kila decisions: KILA-D-20261002-014
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T01:35:46Z
- Author: Kila
- Markup SHA-256 before: `3fe1ae2bc421ca84b758db7e5baecd621e33c500bffca53e7dc74e2bd7b60319`
- Markup SHA-256 after: `b9fa2588491ac6677acd15e80a852f7ccfe6fd0882e6474ab1a8efe03d9ca035`
- Revision IDs: `1`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T103546987164.reviewer-3-comment-8.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Prediction uncertainty combines cross-validated error with surface sensitivity and remains distinct from missing satellite coverage.
~~~~

- After:

~~~~text
Prediction uncertainty combines cross-validated error with surface sensitivity and remains distinct from missing satellite coverage. To assess peripheral representativeness, we quantify displayed pixels outside the station convex hull and outside the station-sampled land-surface-temperature range. A sensitivity test adds eligible neighboring stations within 30 and 50 km of the prefectural boundary while retaining the original daytime and nighttime model specifications and MODIS quality rules. New stations require complete temperature pairs for the 150 matching-period days in 2021–2025 and an eligible MODIS pixel within 5 km. Prediction errors are evaluated by holding out each original Kumamoto station in turn; these temperature-calibration tests do not alter the separate high-heat-day interpolation.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " To assess peripheral representativeness, we quantify displayed pixels outside the station convex hull and outside the station-sampled land-surface-temperature range. A sensitivity test adds eligible neighboring stations within 30 and 50 km of the prefectural boundary while retaining the original daytime and nighttime model specifications and MODIS quality rules. New stations require complete temperature pairs for the 150 matching-period days in 2021–2025 and an eligible MODIS pixel within 5 km. Prediction errors are evaluated by holding out each original Kumamoto station in turn; these temperature-calibration tests do not alter the separate high-heat-day interpolation."

### part-02

- Location: Section 3.2, paragraph beginning “Observed event-week temperatures”.
- Reason: Directly answers the reviewer with quantitative peripheral diagnostics and honestly reports mixed rather than uniformly improved performance.
- Kila decisions: KILA-D-20261002-014
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T01:36:02Z
- Author: Kila
- Markup SHA-256 before: `b9fa2588491ac6677acd15e80a852f7ccfe6fd0882e6474ab1a8efe03d9ca035`
- Markup SHA-256 after: `2d0a0e6d17a3546f0168a572425f467c682dcbdb5fbdbe149fb0f058a8b2269e`
- Revision IDs: `2`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T103602241330.reviewer-3-comment-8.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Cross-validation errors of 0.696 °C for daytime and 0.615 °C for nighttime are lower than their mean-only benchmarks, supporting spatial calibration while retaining explicit uncertainty.
~~~~

- After:

~~~~text
Cross-validation errors of 0.696 °C for daytime and 0.615 °C for nighttime are lower than their mean-only benchmarks, supporting spatial calibration while retaining explicit uncertainty. Nevertheless, 33.4% of displayed pixels lie outside the station convex hull, and 61.1% of daytime and 31.3% of nighttime pixels lie outside the station-sampled land-surface-temperature range. Adding 23 eligible stations within 30 km changes daytime/nighttime RMSE to 0.763/0.571 °C; adding 44 within 50 km changes it to 0.716/0.563 °C. The 50 km extension removes geographic hull extrapolation for displayed pixels but does not uniformly improve prediction error. We therefore retain the original calibration as the main specification and report the extension as a sensitivity test.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Nevertheless, 33.4% of displayed pixels lie outside the station convex hull, and 61.1% of daytime and 31.3% of nighttime pixels lie outside the station-sampled land-surface-temperature range. Adding 23 eligible stations within 30 km changes daytime/nighttime RMSE to 0.763/0.571 °C; adding 44 within 50 km changes it to 0.716/0.563 °C. The 50 km extension removes geographic hull extrapolation for displayed pixels but does not uniformly improve prediction error. We therefore retain the original calibration as the main specification and report the extension as a sensitivity test."

### part-03

- Location: Section 4.5, paragraph beginning “Housing-loss geography remains”.
- Reason: States the remaining representativeness and validation limits without changing the model or making claims unsupported by the station data.
- Kila decisions: KILA-D-20261002-014
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T01:36:14Z
- Author: Kila
- Markup SHA-256 before: `2d0a0e6d17a3546f0168a572425f467c682dcbdb5fbdbe149fb0f058a8b2269e`
- Markup SHA-256 after: `1ea47c4023b98db9cb7e607e4d9f1f4065ed70364d63f923df1aed19e63bd14a`
- Revision IDs: `3`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T103614236430.reviewer-3-comment-8.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
These surfaces do not estimate indoor temperature or forecast realized event-month weather.
~~~~

- After:

~~~~text
These surfaces do not estimate indoor temperature or forecast realized event-month weather. Improved station coverage does not by itself establish accuracy at unobserved peripheral locations, and geographic coverage does not eliminate extrapolation beyond sampled land-surface temperatures. Cross-validation scores are conditional on model selection using the same station sample, rather than independent validation, and the uncertainty surface is not a calibrated prediction interval.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Improved station coverage does not by itself establish accuracy at unobserved peripheral locations, and geographic coverage does not eliminate extrapolation beyond sampled land-surface temperatures. Cross-validation scores are conditional on model selection using the same station sample, rather than independent validation, and the uncertainty surface is not a calibrated prediction interval."


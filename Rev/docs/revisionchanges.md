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

## reviewer-3/comment-10

### part-01

- Location: Section 2.1, paragraph beginning “The study covers Kumamoto Prefecture”.
- Reason: Explain why the main cutoff remains fixed without claiming every input was available on the event date.
- Kila decisions: KILA-D-20261002-016
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T03:53:22Z
- Author: Kila
- Markup SHA-256 before: `1ea47c4023b98db9cb7e607e4d9f1f4065ed70364d63f923df1aed19e63bd14a`
- Markup SHA-256 after: `e95b7395587d7b6814a7202a1490fe55862eb5a50b189d5c4415c49a6a679e05`
- Revision IDs: `4`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T125322918651.reviewer-3-comment-10.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Housing damage is constrained by the official snapshot available at 17:00 JST on August 1, and observed event heat extends through August 3.
~~~~

- After:

~~~~text
Housing damage is constrained by the official snapshot available at 17:00 JST on August 1, and observed event heat extends through August 3. We retain this early housing-damage cutoff for the main analysis and use later reported totals only in a separate retrospective sensitivity test; they are not treated as information available at the early cutoff.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " We retain this early housing-damage cutoff for the main analysis and use later reported totals only in a separate retrospective sensitivity test; they are not treated as information available at the early cutoff."

### part-02

- Location: Section 2.2, paragraph beginning “The baseline combines”.
- Reason: Identify the newer official evidence and avoid presenting early counts as the latest available.
- Kila decisions: KILA-D-20261002-016
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T04:30:27Z
- Author: Kila
- Markup SHA-256 before: `e95b7395587d7b6814a7202a1490fe55862eb5a50b189d5c4415c49a6a679e05`
- Markup SHA-256 after: `c43d52f112becdaad84e9f85c7a4fe40a09143da38cb2e7b4b80a004bccdf9a9`
- Revision IDs: `5, 6, 7, 8, 9, 10, 11`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T133028009540.reviewer-3-comment-10.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The latest usable prefecture snapshot reports 181 fully collapsed and 245 half-collapsed residences, which constrain rather than locate the modeled loss.
~~~~

- After:

~~~~text
The August 1 prefecture snapshot reports 181 fully collapsed and 245 half-collapsed residential buildings, which constrain rather than locate the modeled loss. FDMA Report 65, dated September 24, 2026, at 17:00 JST, reports 2,270 fully collapsed and 6,357 half-collapsed residential buildings in Kumamoto Prefecture (https://www.fdma.go.jp/disaster/info/items/20260728kumamotojishin65.pdf). Both snapshots count buildings rather than households or people, and the later figures remain provisional.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "latest"
     - After: "August"
  2. `replace`
     - Before: "usable"
     - After: "1"
  3. `replace`
     - Before: "residences"
     - After: "residential buildings"
  4. `insert`
     - Before: ""
     - After: " FDMA Report 65, dated September 24, 2026, at 17:00 JST, reports 2,270 fully collapsed and 6,357 half-collapsed residential buildings in Kumamoto Prefecture (https://www.fdma.go.jp/disaster/info/items/20260728kumamotojishin65.pdf). Both snapshots count buildings rather than households or people, and the later figures remain provisional."

### part-03

- Location: Section 2.8, paragraph beginning “The framework contains four distinct sensitivity classes”.
- Reason: Specify exactly what the later-snapshot comparison changes and holds fixed.
- Kila decisions: KILA-D-20261002-016
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T04:30:39Z
- Author: Kila
- Markup SHA-256 before: `c43d52f112becdaad84e9f85c7a4fe40a09143da38cb2e7b4b80a004bccdf9a9`
- Markup SHA-256 after: `03515e1f75abdd64e0210ab09342a4e1d3adfa43dbdff57f13508f66d154ecee`
- Revision IDs: `12`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T133039134316.reviewer-3-comment-10.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Keeping them separate makes each planning range traceable to its assumption.
~~~~

- After:

~~~~text
Keeping them separate makes each planning range traceable to its assumption. A separate retrospective snapshot test substitutes the September 24 full- and half-collapse totals while retaining the main spatial weights, population inputs, half-collapse weight of 0.5, and downstream assumptions. It tests sensitivity to the reported prefecture total, not changes in the observed geography of damage.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " A separate retrospective snapshot test substitutes the September 24 full- and half-collapse totals while retaining the main spatial weights, population inputs, half-collapse weight of 0.5, and downstream assumptions. It tests sensitivity to the reported prefecture total, not changes in the observed geography of damage."

### part-04

- Location: Section 3.3, paragraph beginning “The total-constrained allocation”.
- Reason: Quantify substantial magnitude sensitivity and qualify the mechanically unchanged ranking.
- Kila decisions: KILA-D-20261002-016
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T04:30:50Z
- Author: Kila
- Markup SHA-256 before: `03515e1f75abdd64e0210ab09342a4e1d3adfa43dbdff57f13508f66d154ecee`
- Markup SHA-256 after: `e7f59d7aeaec0ca1544ea810b5fd035499a19ed4e708e05c29ada304c1bf03ed`
- Revision IDs: `13`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T133050223731.reviewer-3-comment-10.part-04.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 5 connects geographically bounded official evidence to a central total of 303.5 functionally lost residences and the associated older-person exposure.
~~~~

- After:

~~~~text
Figure 5 connects geographically bounded official evidence to a central total of 303.5 functionally lost residences and the associated older-person exposure. In the total-only retrospective test, the later snapshot raises this constraint to 5,448.5, or 17.95 times the early value. Municipal rankings remain unchanged under fixed spatial weights and nonbinding household caps; this is a consequence of the test design, not evidence that actual territorial damage priorities remain unchanged.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " In the total-only retrospective test, the later snapshot raises this constraint to 5,448.5, or 17.95 times the early value. Municipal rankings remain unchanged under fixed spatial weights and nonbinding household caps; this is a consequence of the test design, not evidence that actual territorial damage priorities remain unchanged."

### part-05

- Location: Section 4.5, paragraph beginning “Housing-loss geography remains”.
- Reason: Explain temporal information limits without attributing the full increase to new damage or claiming geographic validation.
- Kila decisions: KILA-D-20261002-016
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T04:31:00Z
- Author: Kila
- Markup SHA-256 before: `e7f59d7aeaec0ca1544ea810b5fd035499a19ed4e708e05c29ada304c1bf03ed`
- Markup SHA-256 after: `3ea7fbe58f85c8f666f0ee8051d3e45a87f2b49153a946f68d5503386d7b76e6`
- Revision IDs: `14`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T133100481088.reviewer-3-comment-10.part-05.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Housing-loss geography remains the largest structural uncertainty.
~~~~

- After:

~~~~text
Housing-loss geography remains the largest structural uncertainty. The early damage snapshot also limits the magnitude of estimated need. Later reported totals can reflect delayed assessment and classification changes as well as additional damage, so their increase cannot be interpreted solely as new physical losses after August 1. Operational priorities require updated local damage and displacement evidence rather than proportional rescaling of prefecture totals alone.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The early damage snapshot also limits the magnitude of estimated need. Later reported totals can reflect delayed assessment and classification changes as well as additional damage, so their increase cannot be interpreted solely as new physical losses after August 1. Operational priorities require updated local damage and displacement evidence rather than proportional rescaling of prefecture totals alone."

## reviewer-3/comment-1

### part-01

- Location: Abstract, paragraph beginning “Earthquake damage can deprive older residents”.
- Reason: Make the restricted target visible in the Abstract as explicitly requested.
- Kila decisions: KILA-D-20261002-019
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T04:52:13Z
- Author: Kila
- Markup SHA-256 before: `3ea7fbe58f85c8f666f0ee8051d3e45a87f2b49153a946f68d5503386d7b76e6`
- Markup SHA-256 after: `be39ddc7ac6a083e4241691f46ac4a19e696d45a64b8e519b647dde66e0191de`
- Revision IDs: `15`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T135214016994.reviewer-3-comment-1.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
We develop an evidence-constrained spatial framework for Kumamoto Prefecture that allocates official residence-damage totals across census disclosure groups, estimates the older population associated with functional housing loss, and links this population to cooling placement, electricity demand, and a fixed-weather mortality-risk contrast.
~~~~

- After:

~~~~text
We develop an evidence-constrained spatial framework for Kumamoto Prefecture that allocates official residence-damage totals across census disclosure groups, estimates the older population associated with functional housing loss, and links this population to cooling placement, electricity demand, and a fixed-weather mortality-risk contrast. The target is the housing-loss-related older population, not all displaced residents or everyone potentially requiring cooling after service disruptions.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The target is the housing-loss-related older population, not all displaced residents or everyone potentially requiring cooling after service disruptions."

### part-02

- Location: Section 1, paragraph beginning “This study asks”.
- Reason: Avoid describing a housing-loss model as covering all post-earthquake cooling needs.
- Kila decisions: KILA-D-20261002-019
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T04:52:23Z
- Author: Kila
- Markup SHA-256 before: `be39ddc7ac6a083e4241691f46ac4a19e696d45a64b8e519b647dde66e0191de`
- Markup SHA-256 after: `6263f72ee391e88b52cb95126a94f56d0ae5fd99834af62f5d8296e78cf41b6c`
- Revision IDs: `16, 17`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T135223306362.reviewer-3-comment-1.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
This study asks where older-person cooling protection is most needed after the Kumamoto earthquake, how much peak power and daily electricity that protection would require, and how the modeled mortality burden differs if effective cooling is not restored during the next 30 days.
~~~~

- After:

~~~~text
This study asks where cooling protection for older residents associated with functional housing loss is most needed after the Kumamoto earthquake, how much peak power and daily electricity that protection would require, and how the modeled mortality burden differs if effective cooling is not restored during the next 30 days.
~~~~

- Minimal tracked fragments:
  1. `delete`
     - Before: "older-person "
     - After: ""
  2. `insert`
     - Before: ""
     - After: " for older residents associated with functional housing loss"

### part-03

- Location: Section 2.3, paragraph beginning “Baseline variables retain”.
- Reason: Justify the scope from the evidence available and distinguish a modeled association from observed individual cooling loss.
- Kila decisions: KILA-D-20261002-019
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T04:52:38Z
- Author: Kila
- Markup SHA-256 before: `6263f72ee391e88b52cb95126a94f56d0ae5fd99834af62f5d8296e78cf41b6c`
- Markup SHA-256 after: `ea406d74f898384dd253208f55cd6510b218b8c2a5d13a4e634d56d477104a67`
- Revision IDs: `18`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T135239033599.reviewer-3-comment-1.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Modeled exposure variables comprise expected functionally lost residences, the associated population aged 65 or older, and no-verified-placement older-person-days.
~~~~

- After:

~~~~text
Modeled exposure variables comprise expected functionally lost residences, the associated population aged 65 or older, and no-verified-placement older-person-days. We restrict this population to the housing-loss pathway because reported building-damage totals constrain that pathway, whereas the available operational reports do not identify the older individuals displaced by each cause. Residents requiring protection solely because of service outages or precautionary evacuation are outside this modeled population. Association with housing loss does not establish actual displacement or loss of effective cooling for each individual.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " We restrict this population to the housing-loss pathway because reported building-damage totals constrain that pathway, whereas the available operational reports do not identify the older individuals displaced by each cause. Residents requiring protection solely because of service outages or precautionary evacuation are outside this modeled population. Association with housing loss does not establish actual displacement or loss of effective cooling for each individual."

### part-04

- Location: Section 3.1, paragraph beginning “Population concentration and older-age vulnerability”.
- Reason: Explain why the shelter observations and model do not measure the same population, without asserting that housing-loss residents are all present in shelters.
- Kila decisions: KILA-D-20261002-019
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T04:52:51Z
- Author: Kila
- Markup SHA-256 before: `ea406d74f898384dd253208f55cd6510b218b8c2a5d13a4e634d56d477104a67`
- Markup SHA-256 after: `5ee25230c8358a0c371e34ba9ae83e1ede20e0ddda0db986a88cead6e487b86d`
- Revision IDs: `19`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T135252028670.reviewer-3-comment-1.part-04.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Reported Kumamoto City shelter occupancy peaked at 2,487 people, and the latest Minami Ward observation recorded 430 occupants.
~~~~

- After:

~~~~text
Reported Kumamoto City shelter occupancy peaked at 2,487 people, and the latest Minami Ward observation recorded 430 occupants. These occupancy counts describe a broader, differently timed and geographically bounded population; they are not age-specific counts of residents associated with functional housing loss. Service disruptions and precautionary needs can also prompt shelter use. We therefore use occupancy as operational context, not as a calibration or validation total for modeled older-person exposure.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " These occupancy counts describe a broader, differently timed and geographically bounded population; they are not age-specific counts of residents associated with functional housing loss. Service disruptions and precautionary needs can also prompt shelter use. We therefore use occupancy as operational context, not as a calibration or validation total for modeled older-person exposure."

## reviewer-3/comment-5

### part-01

- Location: 2.4: provenance and eligibility; approved bundle P01/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 2.4: provenance and eligibility
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:34Z
- Author: Kila
- Markup SHA-256 before: `5ee25230c8358a0c371e34ba9ae83e1ede20e0ddda0db986a88cead6e487b86d`
- Markup SHA-256 after: `0db734f5a6908fc5fbca7d6a570cbdfeddd3b990ba67e03bc51a3f8173350ca2`
- Revision IDs: `20`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155234522943.reviewer-3-comment-5.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
We construct disclosure-group allocation weights from an exposure proxy and exponential distance decay from the official epicenter.
~~~~

- After:

~~~~text
We construct disclosure-group allocation weights from an exposure proxy and exponential distance decay from the official epicenter. This is a study-defined total-constrained screening allocation, not a fitted damage-prediction model. Groups without general households receive zero allocation; the remaining weights are renormalized to conserve the scenario total.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " This is a study-defined total-constrained screening allocation, not a fitted damage-prediction model. Groups without general households receive zero allocation; the remaining weights are renormalized to conserve the scenario total."

### part-02

- Location: 2.4: structural ensemble; approved bundle P02/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 2.4: structural ensemble
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:35Z
- Author: Kila
- Markup SHA-256 before: `0db734f5a6908fc5fbca7d6a570cbdfeddd3b990ba67e03bc51a3f8173350ca2`
- Markup SHA-256 after: `119cedaeec74284231acd9d16ff33312c187bc88b0deb91fe30c665183aa60b1`
- Revision IDs: `21, 22, 23, 24, 25, 26, 27, 28, 29, 30`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155235337973.reviewer-3-comment-5.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Housing-loss scenarios cross three exposure proxies, three distance-decay scales, and three half-collapse weights, producing 27 allocations.
~~~~

- After:

~~~~text
Housing-loss scenarios cross general households, mapped-building count and mapped footprint area with three distance-decay scales and half-collapse weights of 0, 0.5 and 1, producing 27 allocations. Building proxies are weighting variables, not counts of residences.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "three"
     - After: "general"
  2. `replace`
     - Before: "exposure"
     - After: "households,"
  3. `replace`
     - Before: "proxies,"
     - After: "mapped-building count and mapped footprint area with"
  4. `delete`
     - Before: ","
     - After: ""
  5. `delete`
     - Before: " three"
     - After: ""
  6. `insert`
     - Before: ""
     - After: " of 0, 0.5 and 1"
  7. `insert`
     - Before: ""
     - After: " Building proxies are weighting variables, not counts of residences."

### part-03

- Location: 2.4: replace hybrid primary; approved bundle P03/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 2.4: replace hybrid primary
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:35Z
- Author: Kila
- Markup SHA-256 before: `119cedaeec74284231acd9d16ff33312c187bc88b0deb91fe30c665183aa60b1`
- Markup SHA-256 after: `e8fe575c91adbe1b6b553610cdaf48e3c274c82be601f216ac0d5d7c84041482`
- Revision IDs: `31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155236197687.reviewer-3-comment-5.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The central surface is the normalized pointwise median of the allocation scenarios constrained to the approved central functional-loss total.
~~~~

- After:

~~~~text
The central surface is one coherent scenario using general households, a 20-km decay scale and a half-collapse weight of 0.5, giving 303.5 functional-loss units. Household counts align the allocation denominator with the target population; 20 km and 0.5 are transparent planning assumptions, not empirically optimized parameters or a calibrated loss fraction. The normalized pointwise-median surface, rebuilt after the zero-household correction, is retained only as a separate sensitivity.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "the"
     - After: "one"
  2. `replace`
     - Before: "normalized"
     - After: "coherent"
  3. `replace`
     - Before: "pointwise"
     - After: "scenario"
  4. `replace`
     - Before: "median"
     - After: "using general households, a 20-km decay scale and a half-collapse weight"
  5. `insert`
     - Before: ""
     - After: " 0.5, giving 303.5 functional-loss units. Household counts align"
  6. `replace`
     - Before: "scenarios"
     - After: "denominator"
  7. `replace`
     - Before: "constrained to"
     - After: "with"
  8. `replace`
     - Before: "approved"
     - After: "target"
  9. `replace`
     - Before: "central"
     - After: "population;"
  10. `replace`
     - Before: "functional-loss"
     - After: "20"
  11. `replace`
     - Before: "total"
     - After: "km and 0"
  12. `insert`
     - Before: ""
     - After: "5 are transparent planning assumptions, not empirically optimized parameters or a calibrated loss fraction. The normalized pointwise-median surface, rebuilt after the zero-household correction, is retained only as a separate sensitivity."

### part-04

- Location: 2.4: bounded demographic allocation and Eq. 3 assumption; approved bundle P04/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 2.4: bounded demographic allocation and Eq. 3 assumption
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:36Z
- Author: Kila
- Markup SHA-256 before: `e8fe575c91adbe1b6b553610cdaf48e3c274c82be601f216ac0d5d7c84041482`
- Markup SHA-256 after: `187b74f68ef184a75f1fceabef2894824595cfb242dc71c24340cc3395fd5b46`
- Revision IDs: `53, 54`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155236963129.reviewer-3-comment-5.part-04.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
We associate structural housing loss with older residents by scaling each group's population aged 65 or older by its modeled share of general households lost.
~~~~

- After:

~~~~text
We associate structural housing loss with older residents by scaling each group's estimated general-household population aged 65 or older by its modeled share of general households lost. For each group, the lower bound is the number of households containing an older member; the upper bound is the all-resident older population where that lower bound is positive, and zero otherwise. Starting from the lower bound, we distribute the municipal remainder in proportion to older-household counts, subject to the upper bounds, to match official municipal general-household older-population controls. Groups are assigned to municipalities by representative points. Residual-capacity weighting is a separate demographic sensitivity. These allocations reproduce municipal controls but do not validate within-municipality residence patterns. Equation 3 assumes that housing loss is not systematically associated with age composition within a group; exposure is defined as zero where general households are zero.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " estimated general-household"
  2. `insert`
     - Before: ""
     - After: " For each group, the lower bound is the number of households containing an older member; the upper bound is the all-resident older population where that lower bound is positive, and zero otherwise. Starting from the lower bound, we distribute the municipal remainder in proportion to older-household counts, subject to the upper bounds, to match official municipal general-household older-population controls. Groups are assigned to municipalities by representative points. Residual-capacity weighting is a separate demographic sensitivity. These allocations reproduce municipal controls but do not validate within-municipality residence patterns. Equation 3 assumes that housing loss is not systematically associated with age composition within a group; exposure is defined as zero where general households are zero."

### part-05

- Location: 2.4: Eq. 3 symbol definition; preserve OMML; approved bundle P05/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 2.4: Eq. 3 symbol definition; preserve OMML
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:37Z
- Author: Kila
- Markup SHA-256 before: `187b74f68ef184a75f1fceabef2894824595cfb242dc71c24340cc3395fd5b46`
- Markup SHA-256 after: `4d7afce46071c7058b7d71db339e73f6e23652ad491424efb4de8ef9be219f2c`
- Revision IDs: `55, 56`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155237601002.reviewer-3-comment-5.part-05.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
is the resident older population
~~~~

- After:

~~~~text
is the estimated general-household older population
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "resident"
     - After: "estimated general-household"

### part-06

- Location: 2.8: consistent municipality geography; approved bundle P06/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 2.8: consistent municipality geography
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:38Z
- Author: Kila
- Markup SHA-256 before: `4d7afce46071c7058b7d71db339e73f6e23652ad491424efb4de8ef9be219f2c`
- Markup SHA-256 after: `c40e7daeaa7533ba610ff5e327e85325ad6262486d4c14161d8da7b225722ae3`
- Revision IDs: `57, 58, 59, 60`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155238231300.reviewer-3-comment-5.part-06.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Additive disclosure-group outcomes are summed within municipality boundaries after the central scenario is selected at its defined analytical scale.
~~~~

- After:

~~~~text
Additive disclosure-group outcomes are summed using representative-point municipality assignments after the central scenario is selected at its defined analytical scale.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "within"
     - After: "using representative-point"
  2. `replace`
     - Before: "boundaries"
     - After: "assignments"

### part-07

- Location: 2.8: shaking and report-comparison design; approved bundle P07/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 2.8: shaking and report-comparison design
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:38Z
- Author: Kila
- Markup SHA-256 before: `c40e7daeaa7533ba610ff5e327e85325ad6262486d4c14161d8da7b225722ae3`
- Markup SHA-256 after: `8c4ac3c5901d7e0f7779173f54b5107d43e3ba493660e4baa2e482211a65d7ed`
- Revision IDs: `61`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155238836509.reviewer-3-comment-5.part-07.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Keeping them separate makes each planning range traceable to its assumption.
~~~~

- After:

~~~~text
Keeping them separate makes each planning range traceable to its assumption. We additionally compare the selected primary with the corrected hybrid, bounded demographic alternative and 54 hypothetical shaking allocations. For the latter, nearest-station JMA intensity categories are assigned in projected coordinates, including neighbouring-prefecture stations and excluding the withdrawn Tomiai observation. Three full-collapse vulnerability shapes from Suto et al. (2019, Equation 2 and Table 4; https://www.jstage.jst.go.jp/article/jaee/19/4/19_4_13/_pdf) are crossed with two category-endpoint evaluations, three exposure proxies and three half-collapse weights. The wooden, steel and light-steel normal-CDF shapes use location/scale pairs (6.87, 0.73), (7.25, 0.63) and (7.24, 0.60), respectively. The open upper endpoint of intensity 7 uses the limiting value of one, not an observed intensity. Relative weights are normalized with household-capacity constraints; no caps bind. These are hypothetical weighting shapes, not local material shares or validated functional-loss probabilities. We assess municipality rank correlations, rank shifts and top-five overlap. Separate comparisons with July 31 and September 29 prefectural reports use full collapse, large-scale-half plus half collapse, and their combined counts. Share total-variation distance is half the sum of absolute municipal share differences. Report dates and categories are kept distinct from the planning snapshot. These comparisons are descriptive rather than independent validation: outcomes and assessment completeness differ, report zeros are not verified negatives, and report geography was examined before developing the alternatives.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " We additionally compare the selected primary with the corrected hybrid, bounded demographic alternative and 54 hypothetical shaking allocations. For the latter, nearest-station JMA intensity categories are assigned in projected coordinates, including neighbouring-prefecture stations and excluding the withdrawn Tomiai observation. Three full-collapse vulnerability shapes from Suto et al. (2019, Equation 2 and Table 4; https://www.jstage.jst.go.jp/article/jaee/19/4/19_4_13/_pdf) are crossed with two category-endpoint evaluations, three exposure proxies and three half-collapse weights. The wooden, steel and light-steel normal-CDF shapes use location/scale pairs (6.87, 0.73), (7.25, 0.63) and (7.24, 0.60), respectively. The open upper endpoint of intensity 7 uses the limiting value of one, not an observed intensity. Relative weights are normalized with household-capacity constraints; no caps bind. These are hypothetical weighting shapes, not local material shares or validated functional-loss probabilities. We assess municipality rank correlations, rank shifts and top-five overlap. Separate comparisons with July 31 and September 29 prefectural reports use full collapse, large-scale-half plus half collapse, and their combined counts. Share total-variation distance is half the sum of absolute municipal share differences. Report dates and categories are kept distinct from the planning snapshot. These comparisons are descriptive rather than independent validation: outcomes and assessment completeness differ, report zeros are not verified negatives, and report geography was examined before developing the alternatives."

### part-08

- Location: 3.3: prefecture exposure; approved bundle P08/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 3.3: prefecture exposure
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:39Z
- Author: Kila
- Markup SHA-256 before: `8c4ac3c5901d7e0f7779173f54b5107d43e3ba493660e4baa2e482211a65d7ed`
- Markup SHA-256 after: `165e50486e9ae1ff023fc5ee7319a1da5ee1ed67aab615a445ea24a307f7226b`
- Revision IDs: `62, 63, 64, 65`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155239444072.reviewer-3-comment-5.part-08.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The central exposure totals 245.794 residents aged 65 or older across Kumamoto.
~~~~

- After:

~~~~text
The central exposure totals 202.042 residents aged 65 or older across Kumamoto.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "245"
     - After: "202"
  2. `replace`
     - Before: "794"
     - After: "042"

### part-09

- Location: 3.3: municipality and person-day totals; approved bundle P09/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 3.3: municipality and person-day totals
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:39Z
- Author: Kila
- Markup SHA-256 before: `165e50486e9ae1ff023fc5ee7319a1da5ee1ed67aab615a445ea24a307f7226b`
- Markup SHA-256 after: `5a89e52a968f7363c19c77c1064dec1519d468126cec2661c99a17d3b12ea7e2`
- Revision IDs: `66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155240084397.reviewer-3-comment-5.part-09.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Table 1 reports 134.030 central functionally lost residences and 90.383 affected older residents in Kumamoto City, followed by 54.839 residences and 48.287 older residents in Yatsushiro City. Across all municipalities, the central totals are 303.5 residences, 245.794 older residents, and 7,373.815 no-placement older-person-days.
~~~~

- After:

~~~~text
Table 1 reports 156.259 central functionally lost residences and 84.543 affected older residents in Kumamoto City, followed by 38.188 residences and 29.708 older residents in Yatsushiro City. Across all municipalities, the central totals are 303.5 residences, 202.042 older residents, and 6,061.258 no-placement older-person-days.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "134"
     - After: "156"
  2. `replace`
     - Before: "030"
     - After: "259"
  3. `replace`
     - Before: "90"
     - After: "84"
  4. `replace`
     - Before: "383"
     - After: "543"
  5. `replace`
     - Before: "54"
     - After: "38"
  6. `replace`
     - Before: "839"
     - After: "188"
  7. `replace`
     - Before: "48"
     - After: "29"
  8. `replace`
     - Before: "287"
     - After: "708"
  9. `replace`
     - Before: "245"
     - After: "202"
  10. `replace`
     - Before: "794"
     - After: "042"
  11. `replace`
     - Before: "7"
     - After: "6"
  12. `replace`
     - Before: "373"
     - After: "061"
  13. `replace`
     - Before: "815"
     - After: "258"

### part-10

- Location: 3.3: validated sensitivity and limited agreement; approved bundle P10/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 3.3: validated sensitivity and limited agreement
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:40Z
- Author: Kila
- Markup SHA-256 before: `5a89e52a968f7363c19c77c1064dec1519d468126cec2661c99a17d3b12ea7e2`
- Markup SHA-256 after: `0cf007ab16017f7b4894b743de1c13fbde107ec9e2401ba41abe54f0839b18ff`
- Revision IDs: `92`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155240775319.reviewer-3-comment-5.part-10.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The table's scenario ranges remain structural sensitivity summaries rather than inspection intervals.
~~~~

- After:

~~~~text
The table's scenario ranges remain structural sensitivity summaries rather than inspection intervals. The corrected hybrid yields 216.546 exposed older residents, 7.18% above the selected primary; municipal exposure rank correlation is 0.9818, with a maximum rank shift of six and the same top-five set. Residual-capacity demographic weighting yields 202.185 exposed older residents, with a maximum rank shift of one. Across the 54 shaking scenarios, exposure ranges from 133.49 to 363.43 and rank correlations from 0.8163 to 0.8978; maximum rank shifts are 16–24. All retain the exposure top-five set, but incremental-death top-five overlap is four of five. These ranges combine hazard, proxy and half-collapse assumptions and are not confidence intervals. Against September 29 full-or-half reports, the primary has rank correlation 0.7252, share total-variation distance 0.5845 and top-five overlap 3/5; the corresponding shaking ranges are 0.7732–0.8127, 0.2374–0.3855 and 4/5. The July 31 combined report has only five municipalities with positive counts; primary correlation is 0.3108 and share distance 0.9674. Thus stable high-exposure membership does not establish accurate reported-damage geography.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The corrected hybrid yields 216.546 exposed older residents, 7.18% above the selected primary; municipal exposure rank correlation is 0.9818, with a maximum rank shift of six and the same top-five set. Residual-capacity demographic weighting yields 202.185 exposed older residents, with a maximum rank shift of one. Across the 54 shaking scenarios, exposure ranges from 133.49 to 363.43 and rank correlations from 0.8163 to 0.8978; maximum rank shifts are 16–24. All retain the exposure top-five set, but incremental-death top-five overlap is four of five. These ranges combine hazard, proxy and half-collapse assumptions and are not confidence intervals. Against September 29 full-or-half reports, the primary has rank correlation 0.7252, share total-variation distance 0.5845 and top-five overlap 3/5; the corresponding shaking ranges are 0.7732–0.8127, 0.2374–0.3855 and 4/5. The July 31 combined report has only five municipalities with positive counts; primary correlation is 0.3108 and share distance 0.9674. Thus stable high-exposure membership does not establish accurate reported-damage geography."

### part-11

- Location: 3.4: engineering totals; approved bundle P11/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 3.4: engineering totals
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:41Z
- Author: Kila
- Markup SHA-256 before: `0cf007ab16017f7b4894b743de1c13fbde107ec9e2401ba41abe54f0839b18ff`
- Markup SHA-256 after: `1c47808dab965ecd8afacce1bb5e474cd9d0e3a5a00200426c65bff95353321f`
- Revision IDs: `93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155241395887.reviewer-3-comment-5.part-11.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Peak power rises from 21.85 kW in the Low bundle to 34.583 kW in the Central bundle and 48.52 kW in the High bundle; corresponding daily electricity rises from 262.21 to 622.497 and 1,164.47 kWh.
~~~~

- After:

~~~~text
Peak power rises from 17.96 kW in the Low bundle to 28.427 kW in the Central bundle and 39.88 kW in the High bundle; corresponding daily electricity rises from 215.54 to 511.691 and 957.19 kWh.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "21"
     - After: "17"
  2. `replace`
     - Before: "85"
     - After: "96"
  3. `replace`
     - Before: "34"
     - After: "28"
  4. `replace`
     - Before: "583"
     - After: "427"
  5. `replace`
     - Before: "48"
     - After: "39"
  6. `replace`
     - Before: "52"
     - After: "88"
  7. `replace`
     - Before: "262"
     - After: "215"
  8. `replace`
     - Before: "21"
     - After: "54"
  9. `replace`
     - Before: "622"
     - After: "511"
  10. `replace`
     - Before: "497"
     - After: "691"
  11. `replace`
     - Before: "1,164"
     - After: "957"
  12. `replace`
     - Before: "47"
     - After: "19"

### part-12

- Location: 3.4: municipality engineering values; approved bundle P12/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 3.4: municipality engineering values
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:41Z
- Author: Kila
- Markup SHA-256 before: `1c47808dab965ecd8afacce1bb5e474cd9d0e3a5a00200426c65bff95353321f`
- Markup SHA-256 after: `63614c9dc2ed24229956626c16d62d55c0cc20087a08f430d414d3e1266fffec`
- Revision IDs: `117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155242023321.reviewer-3-comment-5.part-12.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Table 2 gives Kumamoto City a Central requirement of 12.717 kW and 228.903 kWh per day, followed by Yatsushiro City at 6.794 kW and 122.292 kWh per day.
~~~~

- After:

~~~~text
Table 2 gives Kumamoto City a Central requirement of 11.895 kW and 214.114 kWh per day, followed by Yatsushiro City at 4.180 kW and 75.238 kWh per day.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "12"
     - After: "11"
  2. `replace`
     - Before: "717"
     - After: "895"
  3. `replace`
     - Before: "228"
     - After: "214"
  4. `replace`
     - Before: "903"
     - After: "114"
  5. `replace`
     - Before: "6"
     - After: "4"
  6. `replace`
     - Before: "794"
     - After: "180"
  7. `replace`
     - Before: "122"
     - After: "75"
  8. `replace`
     - Before: "292"
     - After: "238"

### part-13

- Location: 3.5: aggregate effect and uncertainty label; approved bundle P13/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 3.5: aggregate effect and uncertainty label
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:42Z
- Author: Kila
- Markup SHA-256 before: `63614c9dc2ed24229956626c16d62d55c0cc20087a08f430d414d3e1266fffec`
- Markup SHA-256 after: `c23233d5d8fcd7f0e7e5a84b7fcf4a76c69e5918fea69a92b8c48e243fee6099`
- Revision IDs: `133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155242656182.reviewer-3-comment-5.part-13.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The prefecture-weighted central 30-day mortality-burden increase without effective cooling is 5.34%, with a transferred-effect interval from 0.67% to 10.01%.
~~~~

- After:

~~~~text
The prefecture-weighted central 30-day mortality-burden increase without effective cooling is 5.31%, with source-effect endpoint scenarios of 0.66% and 9.96%; these endpoints are not whole-model confidence limits.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "34"
     - After: "31"
  2. `replace`
     - Before: "a"
     - After: "source-effect"
  3. `replace`
     - Before: "transferred-effect"
     - After: "endpoint"
  4. `replace`
     - Before: "interval"
     - After: "scenarios"
  5. `replace`
     - Before: "from"
     - After: "of"
  6. `replace`
     - Before: "67"
     - After: "66"
  7. `replace`
     - Before: "to"
     - After: "and"
  8. `replace`
     - Before: "10"
     - After: "9"
  9. `replace`
     - Before: "01"
     - After: "96"
  10. `insert`
     - Before: ""
     - After: "; these endpoints are not whole-model confidence limits"

### part-14

- Location: 3.5: Kumamoto incremental expected deaths; approved bundle P14/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 3.5: Kumamoto incremental expected deaths
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:43Z
- Author: Kila
- Markup SHA-256 before: `c23233d5d8fcd7f0e7e5a84b7fcf4a76c69e5918fea69a92b8c48e243fee6099`
- Markup SHA-256 after: `3dba3f197a0fac13d49cffc3c466fdecead1af4b56bd8884c9eab4e1776143e3`
- Revision IDs: `152, 153`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155243270338.reviewer-3-comment-5.part-14.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
0.01797
~~~~

- After:

~~~~text
0.01681
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "01797"
     - After: "01681"

### part-15

- Location: 3.5: prefecture incremental expected deaths; approved bundle P15/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 3.5: prefecture incremental expected deaths
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:43Z
- Author: Kila
- Markup SHA-256 before: `3dba3f197a0fac13d49cffc3c466fdecead1af4b56bd8884c9eab4e1776143e3`
- Markup SHA-256 after: `5cbba9e4b47cb1f9a39c55de28ece81971267b5a232aa2d4ceb7e882c9b4be35`
- Revision IDs: `154, 155`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155243882300.reviewer-3-comment-5.part-15.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
0.04380
~~~~

- After:

~~~~text
0.03565
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "04380"
     - After: "03565"

### part-16

- Location: 4.5: explicit residual validity limits; approved bundle P16/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: 4.5: explicit residual validity limits
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:44Z
- Author: Kila
- Markup SHA-256 before: `5cbba9e4b47cb1f9a39c55de28ece81971267b5a232aa2d4ceb7e882c9b4be35`
- Markup SHA-256 after: `b383bb6c97363eaea33dcceb7e814aa7147fce380a29d0e134d43a59ff7ba61d`
- Revision IDs: `156`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155244511481.reviewer-3-comment-5.part-16.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
In this study, epicentral distance remains an incomplete hazard representation, and the functional contribution of half-collapse varies across scenarios.
~~~~

- After:

~~~~text
In this study, epicentral distance remains an incomplete hazard representation, and the functional contribution of half-collapse varies across scenarios. The selected allocation is retained as transparent early demand screening, not validated municipal or building-level damage prediction. Report-share disagreement remains substantial; the closer descriptive agreement of shaking alternatives does not establish independent validity or justify post hoc selection. Nearest-station categories omit local site effects, source vulnerability curves are transferred beyond their original setting, and full-collapse shapes are used only as hypothetical functional-loss weights. Municipal calibration and demographic rank stability cannot verify within-group residence patterns or the assumed absence of systematic age-related loss differences.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The selected allocation is retained as transparent early demand screening, not validated municipal or building-level damage prediction. Report-share disagreement remains substantial; the closer descriptive agreement of shaking alternatives does not establish independent validity or justify post hoc selection. Nearest-station categories omit local site effects, source vulnerability curves are transferred beyond their original setting, and full-collapse shapes are used only as hypothetical functional-loss weights. Municipal calibration and demographic rank stability cannot verify within-group residence patterns or the assumed absence of systematic age-related loss differences."

### part-17

- Location: Abstract: exposure; approved bundle P17/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: Abstract: exposure
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:44Z
- Author: Kila
- Markup SHA-256 before: `b383bb6c97363eaea33dcceb7e814aa7147fce380a29d0e134d43a59ff7ba61d`
- Markup SHA-256 after: `c6f2e20105f9b03dceb9560f67b6753b66aaf514d4760c5dbbf162f547a51c41`
- Revision IDs: `157, 158`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155245118071.reviewer-3-comment-5.part-17.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
approximately 246
~~~~

- After:

~~~~text
approximately 202
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "246"
     - After: "202"

### part-18

- Location: Abstract: engineering; approved bundle P18/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: Abstract: engineering
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:45Z
- Author: Kila
- Markup SHA-256 before: `c6f2e20105f9b03dceb9560f67b6753b66aaf514d4760c5dbbf162f547a51c41`
- Markup SHA-256 after: `fdd09681622d0d06d6e0d35b5f5999df0e77ccd4c5df1c09acd6af7b7f080cf3`
- Revision IDs: `159, 160, 161, 162, 163, 164, 165, 166`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155245704063.reviewer-3-comment-5.part-18.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
34.583 kW of peak cooling power and 622.497 kWh
~~~~

- After:

~~~~text
28.427 kW of peak cooling power and 511.691 kWh
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "34"
     - After: "28"
  2. `replace`
     - Before: "583"
     - After: "427"
  3. `replace`
     - Before: "622"
     - After: "511"
  4. `replace`
     - Before: "497"
     - After: "691"

### part-19

- Location: Abstract: health; approved bundle P19/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: Abstract: health
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:46Z
- Author: Kila
- Markup SHA-256 before: `fdd09681622d0d06d6e0d35b5f5999df0e77ccd4c5df1c09acd6af7b7f080cf3`
- Markup SHA-256 after: `b2be73245c0c96ec1236eeb0289c3d9a8cebe269fbedb0b67634d84dceecffb0`
- Revision IDs: `167, 168`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155246288818.reviewer-3-comment-5.part-19.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
5.34%
~~~~

- After:

~~~~text
5.31%
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "34"
     - After: "31"

### part-20

- Location: Figure 5 note; approved bundle P20/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: Figure 5 note
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:46Z
- Author: Kila
- Markup SHA-256 before: `b2be73245c0c96ec1236eeb0289c3d9a8cebe269fbedb0b67634d84dceecffb0`
- Markup SHA-256 after: `c545abf37ad474c97edcd00037e805a5bb88f984d3f151eaef1c8fd0df34c441`
- Revision IDs: `169`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155246883880.reviewer-3-comment-5.part-20.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `c21d00426c037a67b0fba1fabff610e453e3a2a5424274c5287e40c65ce00d46`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Note: Panel a maps geographically bounded official residence-loss evidence and the prefecture snapshot used to constrain scenario totals. Panel b maps central expected structural residence loss across disclosure groups with epicentral distance guides. Panel c maps the associated central exposure of residents aged 65 or older.
~~~~

- After:

~~~~text
Note: Panel a maps geographically bounded official residence-loss evidence and the prefecture snapshot used to constrain scenario totals. Panel b maps central expected structural residence loss across disclosure groups with epicentral distance guides. Panel c maps the associated central exposure of residents aged 65 or older. Panels b and c use the household/20-km/0.5 primary and bounded general-household older-population allocation; panel a is contextual evidence, not independent validation.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Panels b and c use the household/20-km/0.5 primary and bounded general-household older-population allocation; panel a is contextual evidence, not independent validation."

### part-21

- Location: Figure 6 note: envelope; approved bundle P21/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: Figure 6 note: envelope
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:47Z
- Author: Kila
- Markup SHA-256 before: `c545abf37ad474c97edcd00037e805a5bb88f984d3f151eaef1c8fd0df34c441`
- Markup SHA-256 after: `a00de4d5bfc98fe83b2c7fc5c2a9cf8339458659914fb2956ea61c86bf546381`
- Revision IDs: `170, 171, 172, 173, 174, 175, 176, 177`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155247629876.reviewer-3-comment-5.part-21.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `c21d00426c037a67b0fba1fabff610e453e3a2a5424274c5287e40c65ce00d46`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
whose values are not additive
~~~~

- After:

~~~~text
derived from pointwise maxima across the 27 distance/proxy/half-collapse scenarios and not representing a jointly realized aggregate scenario
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "whose"
     - After: "derived"
  2. `replace`
     - Before: "values"
     - After: "from"
  3. `replace`
     - Before: "are"
     - After: "pointwise maxima across the 27 distance/proxy/half-collapse scenarios and"
  4. `replace`
     - Before: "additive"
     - After: "representing a jointly realized aggregate scenario"

### part-22

- Location: Figure 7 note; approved bundle P22/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: Figure 7 note
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:48Z
- Author: Kila
- Markup SHA-256 before: `a00de4d5bfc98fe83b2c7fc5c2a9cf8339458659914fb2956ea61c86bf546381`
- Markup SHA-256 after: `4817619e08894e38ea7e23e334738ff99cbd55b50b970f8b75400a587b1ad078`
- Revision IDs: `178`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155248262936.reviewer-3-comment-5.part-22.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `c21d00426c037a67b0fba1fabff610e453e3a2a5424274c5287e40c65ce00d46`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Note: Panel a maps Central-scenario required peak cooling electric power by municipality. Panel b maps Central-scenario required daily cooling electricity by municipality. Panel c compares prefecture-wide peak power and daily energy requirements under the Low, Central, and High engineering bundles.
~~~~

- After:

~~~~text
Note: Panel a maps Central-scenario required peak cooling electric power by municipality. Panel b maps Central-scenario required daily cooling electricity by municipality. Panel c compares prefecture-wide peak power and daily energy requirements under the Low, Central, and High engineering bundles. All bundles use the same selected primary population; daily energy assumes constant scenario power over the specified operating hours, not measured consumption or a verified supply shortfall.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " All bundles use the same selected primary population; daily energy assumes constant scenario power over the specified operating hours, not measured consumption or a verified supply shortfall."

### part-23

- Location: Figure 8 note; approved bundle P23/23
- Reason: Execute the approved linked R3/C5 primary-allocation reconciliation: Figure 8 note
- Kila decisions: KILA-D-20261002-022
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T06:52:48Z
- Author: Kila
- Markup SHA-256 before: `4817619e08894e38ea7e23e334738ff99cbd55b50b970f8b75400a587b1ad078`
- Markup SHA-256 after: `07fe9213daa6647013e21e1a09e222d5cbc11818c7dfbaf12aa4d27803c9e6f5`
- Revision IDs: `179, 180, 181, 182, 183, 184`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T155248884212.reviewer-3-comment-5.part-23.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `c21d00426c037a67b0fba1fabff610e453e3a2a5424274c5287e40c65ce00d46`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
transferred effect interval
~~~~

- After:

~~~~text
source-effect endpoint range, which excludes structural, engineering, baseline and transfer uncertainty
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "transferred"
     - After: "source-effect"
  2. `replace`
     - Before: "effect"
     - After: "endpoint"
  3. `replace`
     - Before: "interval"
     - After: "range, which excludes structural, engineering, baseline and transfer uncertainty"

### object-bundle-01 — explicitly approved execution exception

- Date: 2026-10-02; author: Codex; comment: reviewer-3/comment-5.
- Reason: implement figures and displayed table results approved by KILA-D-20261002-022; user separately authorizes agent object replacement in this turn.
- Mode: scoped object-edit exception, not a normal one-paragraph edit invocation.
- Location: Figures 5–8 and Tables 1–3; three continuous tables retained.
- Exact changes: 369 cells; the complete before/after strings, coordinates and paired revision IDs for every cell are retained in `data/exp/revision_object_replacement/validation.json` under `changes`. Four image targets, replacement paths and SHA-256 values are in its `images` field.
- Before hash: `f1e3c1af7f82876885bdc28045b293e7579326058b559654f97dc8b0a5d9abfd`.
- After hash: `6ad3214ab2394e3f2f58bdaf8095b8d8b7b40d12b00f44f35bf0358ca3c90202`.
- Backup: `data/exp/revision_object_replacement/before_objects.markup.docx`.
- Existing revisions preserved exactly; 369 new insertion/deletion pairs; 472 insertions and 450 deletions total with unique IDs. Changed table cells preserve paragraph/run properties; no prior insertion is re-edited.
- Image swaps are not tracked textual changes; old images are recoverable from backup. Same widths, corrected heights to preserve source aspect ratios.
- All non-document/non-target-image package parts unchanged, including endnote XML and relationship bytes. Existing equations and non-table prose untouched.
- Fresh clean and scoped visual checks: `Rev/docs/r3-c5-object-review.md`. No response completion or submission approval inferred.

## reviewer-3/comment-6

### part-01

- Location: Section 2.2, final stages paragraph.
- Reason: the code fixes area at 3.5 m²/person in all bundles.
- Kila decisions: KILA-D-20261002-029, KILA-D-20261002-030
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T12:25:13Z
- Author: Kila
- Markup SHA-256 before: `6ad3214ab2394e3f2f58bdaf8095b8d8b7b40d12b00f44f35bf0358ca3c90202`
- Markup SHA-256 after: `92e1c3f6626c84308a2b43ec0971913c746a96606a7e662f34beb47424ffe180`
- Revision IDs: `923, 924, 925, 926`
- Backup: `/Users/lichao/Research/KE01/Rev/revision/.kila-backups/KE01.rev.markup.20261002T212513802647.reviewer-3-comment-6.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Low, Central, and High engineering bundles vary shelter space, cooling load, system efficiency, peak diversity, and operating duration.
~~~~

- After:

~~~~text
Low, Central, and High engineering bundles hold shelter area per person fixed and vary cooling load, system efficiency, peak diversity, and operating duration.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "vary"
     - After: "hold"
  2. `replace`
     - Before: "space,"
     - After: "area per person fixed and vary"

### part-02

- Location: Section 2.4, paragraph beginning Housing-loss scenarios.
- Reason: make the full ensemble reproducible without implying that mapped polygons are dwellings.
- Kila decisions: KILA-D-20261002-029, KILA-D-20261002-030
- Mode: `replace`
- Revises prior parts: reviewer-3/comment-5#part-02
- Timestamp: 2026-10-02T12:25:14Z
- Author: Kila
- Markup SHA-256 before: `92e1c3f6626c84308a2b43ec0971913c746a96606a7e662f34beb47424ffe180`
- Markup SHA-256 after: `9fa1782d23b120f8e8a65291db8e1adfb7c8d872ba6da273f2162a37dca3cca0`
- Revision IDs: `927, 928, 929`
- Backup: `/Users/lichao/Research/KE01/Rev/revision/.kila-backups/KE01.rev.markup.20261002T212514571133.reviewer-3-comment-6.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Housing-loss scenarios cross general households, mapped-building count and mapped footprint area with three distance-decay scales and half-collapse weights of 0, 0.5 and 1, producing 27 allocations. Building proxies are weighting variables, not counts of residences.
~~~~

- After:

~~~~text
Housing-loss scenarios cross general households, mapped-building count and mapped footprint area with distance-decay scales of 10, 20 and 40 km and half-collapse weights of 0, 0.5 and 1, producing 27 allocations. The proxies are the census general-household count, mapped-building polygon count and summed mapped-building footprint area within each disclosure group. Building proxies are weighting variables, not counts of residences.
~~~~

- Minimal tracked fragments:
  1. `delete`
     - Before: "three "
     - After: ""
  2. `insert`
     - Before: ""
     - After: " of 10, 20 and 40 km"
  3. `insert`
     - Before: ""
     - After: "The proxies are the census general-household count, mapped-building polygon count and summed mapped-building footprint area within each disclosure group. "

### part-03

- Location: Section 2.6, final sentence of the Low/Central/High bundle paragraph.
- Reason: explain heterogeneous range provenance, address the requested consideration of area variation without inventing a new empirical range, and distinguish demand assumptions from standards and observations.
- Kila decisions: KILA-D-20261002-029, KILA-D-20261002-030
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T12:25:15Z
- Author: Kila
- Markup SHA-256 before: `9fa1782d23b120f8e8a65291db8e1adfb7c8d872ba6da273f2162a37dca3cca0`
- Markup SHA-256 after: `f68ba4f317a3a61c4cbefd0469459cc181cca9f338d6c8dc28604363516aa11d`
- Revision IDs: `930`
- Backup: `/Users/lichao/Research/KE01/Rev/revision/.kila-backups/KE01.rev.markup.20261002T212515338414.reviewer-3-comment-6.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
These bundles bound engineering assumptions on the demand side.
~~~~

- After:

~~~~text
These bundles bound engineering assumptions on the demand side. Table S1 reports all parameter values, units and sources. Area remains fixed at 3.5 m²/person as a minimum living-space proxy, not an elderly-specific cooled-floor-area standard. The load-density endpoints are insulation-dependent benchmarks from one gymnasium case, and 134 W/m² is their arithmetic midpoint. That case assumes 0.15 persons/m², whereas the adopted area implies approximately 0.286 persons/m²; the case also contains inconsistent gymnasium/office labeling. These differences limit transfer to emergency shelters. COP, diversity and operating hours are study-defined scenarios rather than government-prescribed values. The narrow load-density range reflects the two case benchmarks, while the broader efficiency and duration ranges explore equipment and operating choices; their widths are not comparable measures of uncertainty. Area is not varied in these bundles because a larger cooled-space requirement is not established for the target facilities. At fixed load density and other inputs, thermal load, electric demand and daily energy scale directly with area, so site-specific area can be substituted without treating this algebraic relationship as a validated facility design. Daily energy assumes constant scenario electric demand over the stated operating hours, not a measured load profile.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Table S1 reports all parameter values, units and sources. Area remains fixed at 3.5 m²/person as a minimum living-space proxy, not an elderly-specific cooled-floor-area standard. The load-density endpoints are insulation-dependent benchmarks from one gymnasium case, and 134 W/m² is their arithmetic midpoint. That case assumes 0.15 persons/m², whereas the adopted area implies approximately 0.286 persons/m²; the case also contains inconsistent gymnasium/office labeling. These differences limit transfer to emergency shelters. COP, diversity and operating hours are study-defined scenarios rather than government-prescribed values. The narrow load-density range reflects the two case benchmarks, while the broader efficiency and duration ranges explore equipment and operating choices; their widths are not comparable measures of uncertainty. Area is not varied in these bundles because a larger cooled-space requirement is not established for the target facilities. At fixed load density and other inputs, thermal load, electric demand and daily energy scale directly with area, so site-specific area can be substituted without treating this algebraic relationship as a validated facility design. Daily energy assumes constant scenario electric demand over the stated operating hours, not a measured load profile."

### reviewer-3/comment-6 — part-04 supplementary asset

- Decision: KILA-D-20261002-029; implementation exception KILA-D-20261002-030.
- Operation: create independent supplementary Table S1; no manuscript table replacement.
- Before: no supplementary Table S1 artifact.
- After: `Rev/revision/KE01.supplementary-table-S1.docx`, containing the complete approved P4 table, notes and source entries in `Rev/docs/proposal-r3-c6.md`.
- Source: reproducible builder `src/analyses/build_r3c6_supplement.py`; exact five-row/six-column and note checks pass.
- Asset SHA-256: b331e95a1742c9a4fa9417bc80d793e251603549636de6579f64bbf4c58d6f03.
- Markup remains f68ba4f317a3a61c4cbefd0469459cc181cca9f338d6c8dc28604363516aa11d during this external asset operation; no revision IDs added by P4.
- Visual review: final single-page render checked, including Japanese source titles; detailed receipt in `Rev/docs/r3-c6-implementation-verification.md`.

## reviewer-1/comment-4

### part-01

- Location: Section 2.5, paragraph beginning “Municipality heat heterogeneity”.
- Reason: distinguish a historical planning exposure from an observed sequence or a meteorological prediction.
- Kila decisions: KILA-D-20261002-033
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T12:58:28Z
- Author: Kila
- Markup SHA-256 before: `f68ba4f317a3a61c4cbefd0469459cc181cca9f338d6c8dc28604363516aa11d`
- Markup SHA-256 after: `1e6a509fcebb45024edc27564c5b5741b52faac5063330aed96418631ed76590`
- Revision IDs: `931`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T215828495820.reviewer-1-comment-4.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The resulting expected high-heat days preserve spatial differences during the relevant season.
~~~~

- After:

~~~~text
The resulting expected high-heat days preserve spatial differences during the relevant season. Fractional values arise from averaging calendar-matched counts over 2021–2025 and spatially weighting station values; they represent an expected exposure duration, not an observed sequence of partial days. The historical scenario supplies a common seasonal outdoor exposure for the two cooling states, not a forecast of the weather during the post-earthquake month.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Fractional values arise from averaging calendar-matched counts over 2021–2025 and spatially weighting station values; they represent an expected exposure duration, not an observed sequence of partial days. The historical scenario supplies a common seasonal outdoor exposure for the two cooling states, not a forecast of the weather during the post-earthquake month."

### part-02

- Location: Section 2.7, paragraph introducing Equation 10.
- Reason: explain fractional powers and explicitly avoid claiming equivalence to a predictive expectation over weather realizations.
- Kila decisions: KILA-D-20261002-033
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T12:58:43Z
- Author: Kila
- Markup SHA-256 before: `1e6a509fcebb45024edc27564c5b5741b52faac5063330aed96418631ed76590`
- Markup SHA-256 after: `1e1b994d33fa4eca153b3ef332e67e7f7c63e78f09cd1c6d0aae0ff9d43afe99`
- Revision IDs: `932`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T215843953321.reviewer-1-comment-4.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
This protected state maintains effective cooling while retaining the same modeled outdoor sequence used by the unprotected state.
~~~~

- After:

~~~~text
This protected state maintains effective cooling while retaining the same modeled outdoor sequence used by the unprotected state. In Equations 10 and 11, the expected high-heat duration and its complement to 30 days enter directly as real-valued exponents of the corresponding daily survival probabilities, without rounding. This weights log survival by the expected duration in each heat state. It is a plug-in scenario approximation: risk evaluated at the mean duration need not equal mean risk across historical years because compounding is nonlinear.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " In Equations 10 and 11, the expected high-heat duration and its complement to 30 days enter directly as real-valued exponents of the corresponding daily survival probabilities, without rounding. This weights log survival by the expected duration in each heat state. It is a plug-in scenario approximation: risk evaluated at the mean duration need not equal mean risk across historical years because compounding is nonlinear."

### part-03

- Location: Section 3.5, final sentence of the paragraph beginning “The fixed-weather health scenario”.
- Reason: provide evidence for retaining the selected approximation without confusing population-weighted death counts, municipal risk rankings, or uncertainty sources.
- Kila decisions: KILA-D-20261002-033
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T13:02:01Z
- Author: Kila
- Markup SHA-256 before: `1e1b994d33fa4eca153b3ef332e67e7f7c63e78f09cd1c6d0aae0ff9d43afe99`
- Markup SHA-256 after: `1b0926453462d1c3f94470362cd5369ae327599125ade72221d159309ea99f32`
- Revision IDs: `933`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T220201164384.reviewer-1-comment-4.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The small absolute magnitude and the larger relative contrast are compatible because the modeled exposed population and time horizon are limited.
~~~~

- After:

~~~~text
The small absolute magnitude and the larger relative contrast are compatible because the modeled exposed population and time horizon are limited. As an aggregation check, we calculate both cooling-state risks separately for each of the five annual interpolated heat-day scenarios and then average the risks. Compared with using mean heat days, the maximum municipal difference in incremental risk is 0.001059 per 100,000, with no change in municipal incremental-risk rankings. This supports the mean-day approximation under the specified baseline, effect parameters and missing-day treatment, but does not validate weather prediction or the transferred health effect.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " As an aggregation check, we calculate both cooling-state risks separately for each of the five annual interpolated heat-day scenarios and then average the risks. Compared with using mean heat days, the maximum municipal difference in incremental risk is 0.001059 per 100,000, with no change in municipal incremental-risk rankings. This supports the mean-day approximation under the specified baseline, effect parameters and missing-day treatment, but does not validate weather prediction or the transferred health effect."

## reviewer-3/comment-9

### part-01

- Location: Section 2.2, body paragraph 19 beginning “The final stages combine”.
- Reason: distinguish official numerator data from the study-constructed rate and make its temporal denominator explicit.
- Kila decisions: KILA-D-20261002-011, KILA-D-20261002-035
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T13:16:37Z
- Author: Kila
- Markup SHA-256 before: `1b0926453462d1c3f94470362cd5369ae327599125ade72221d159309ea99f32`
- Markup SHA-256 after: `3bdfaad30194025ccb8637d46584f5d75115466a905e1e2c6871fdf710b19ab4`
- Revision IDs: `934, 935, 936, 937, 938, 939, 940, 941`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T221637451504.reviewer-3-comment-9.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The final stages combine official municipality mortality baselines, transparent engineering bundles, and a transferred cooling-effect estimate. The mortality baseline pools age-65-or-older all-cause deaths over five years against a fixed census denominator.
~~~~

- After:

~~~~text
The final stages combine municipality mortality references constructed from official death counts, transparent engineering bundles, and a transferred cooling-effect estimate. The mortality baseline pools age-65-or-older all-cause deaths over 2020–2024 and divides them by the fixed 2020 census population aged 65 or older multiplied by five years. This denominator approximates person-time rather than tracking annual population change.
~~~~

- Minimal tracked fragments:
  1. `delete`
     - Before: "official "
     - After: ""
  2. `replace`
     - Before: "baselines"
     - After: "references constructed from official death counts"
  3. `insert`
     - Before: ""
     - After: "2020–2024 and divides them by the fixed 2020 census population aged 65 or older multiplied by "
  4. `insert`
     - Before: ""
     - After: "."
  5. `replace`
     - Before: "against a fixed census"
     - After: "This"
  6. `insert`
     - Before: ""
     - After: " approximates person-time rather than tracking annual population change"

### part-02

- Location: Section 2.7, body paragraph 49 immediately before Equation 8.
- Reason: explain what conversion does and does not establish; a common baseline does not itself provide seasonal calibration.
- Kila decisions: KILA-D-20261002-011, KILA-D-20261002-035
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T13:16:56Z
- Author: Kila
- Markup SHA-256 before: `3bdfaad30194025ccb8637d46584f5d75115466a905e1e2c6871fdf710b19ab4`
- Markup SHA-256 after: `83554b1589e2402390b02ab6f0b62c9795b16e5225bbabfeea0a7a989f0f80de`
- Revision IDs: `942`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T221656882140.reviewer-3-comment-9.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
This baseline anchors both cooling states, so differences arise only on high-heat days.
~~~~

- After:

~~~~text
This baseline anchors both cooling states, so differences arise only on high-heat days. Dividing the annual rate by 100,000 and 365.25 supplies a small-probability approximation to an average daily risk, not an observed summer or non-heat-day probability. We use it as a common reference for the fixed-weather cooling contrast; assigning it to ordinary days is a modeling assumption because the annual rate already averages across seasons and weather conditions.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Dividing the annual rate by 100,000 and 365.25 supplies a small-probability approximation to an average daily risk, not an observed summer or non-heat-day probability. We use it as a common reference for the fixed-weather cooling contrast; assigning it to ordinary days is a modeling assumption because the annual rate already averages across seasons and weather conditions."

### part-03

- Location: Section 4.5, body paragraph 99, transition from housing uncertainty to heat and health uncertainty.
- Reason: explain adequacy only for the stated scenario purpose, identify unresolved population and seasonal mismatches, and avoid claiming robustness that has not been tested.
- Kila decisions: KILA-D-20261002-011, KILA-D-20261002-035, KILA-D-20261002-036
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T13:27:38Z
- Author: Kila
- Markup SHA-256 before: `83554b1589e2402390b02ab6f0b62c9795b16e5225bbabfeea0a7a989f0f80de`
- Markup SHA-256 after: `a83981f6df2fe159bff676aba52f2d582b1e235519ce314b7a115ebd409d6e80`
- Revision IDs: `943`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261002T222738217560.reviewer-3-comment-9.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Heat and health components add separate transfer uncertainties.
~~~~

- After:

~~~~text
Heat and health components add separate transfer uncertainties. The annual mortality reference supports an illustrative common-baseline comparison but does not establish the absolute mortality level for the summer window. The source death counts concern Japanese nationals, whereas the census denominator includes all residents, and both include institutional residents rather than isolating the target general-household population. Holding the 2020 population fixed also omits subsequent demographic change. These mismatches can affect absolute incremental risks and expected-death magnitudes; sharing a baseline across cooling states does not remove them or guarantee unchanged spatial rankings. A matched seasonal baseline by age, municipality and residence setting would be needed to calibrate those quantities more directly; no empirical seasonal correction is applied here.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The annual mortality reference supports an illustrative common-baseline comparison but does not establish the absolute mortality level for the summer window. The source death counts concern Japanese nationals, whereas the census denominator includes all residents, and both include institutional residents rather than isolating the target general-household population. Holding the 2020 population fixed also omits subsequent demographic change. These mismatches can affect absolute incremental risks and expected-death magnitudes; sharing a baseline across cooling states does not remove them or guarantee unchanged spatial rankings. A matched seasonal baseline by age, municipality and residence setting would be needed to calibrate those quantities more directly; no empirical seasonal correction is applied here."

## reviewer-3/comment-3

### part-01

- Location: Section 2.7, body paragraph 51, final sentence after the existing Katz citation.
- Reason: clarify what is transferred and the additional common-baseline assumption without changing Equation 9.
- Kila decisions: KILA-D-20261002-011, KILA-D-20261002-038, KILA-D-20261003-001
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T22:55:29Z
- Author: Kila
- Markup SHA-256 before: `a83981f6df2fe159bff676aba52f2d582b1e235519ce314b7a115ebd409d6e80`
- Markup SHA-256 after: `a9aa53ddd871b8ba8794203fb8b86b2a1d1f871d467b3fdf4bb312f3bc9e7175`
- Revision IDs: `944`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261003T075529909217.reviewer-3-comment-3.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Outdoor heat and the municipality baseline remain fixed across these states.
~~~~

- After:

~~~~text
Outdoor heat and the municipality baseline remain fixed across these states. In the source study, the relative odds ratio compares heat-associated mortality odds ratios between nursing homes without and with air conditioning, rather than directly comparing mortality between displaced community residents with and without cooling. Applying this interaction to our two states assumes a shared reference baseline and transfers the source heat-effect contrast as a planning scenario, not a locally estimated effect.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " In the source study, the relative odds ratio compares heat-associated mortality odds ratios between nursing homes without and with air conditioning, rather than directly comparing mortality between displaced community residents with and without cooling. Applying this interaction to our two states assumes a shared reference baseline and transfers the source heat-effect contrast as a planning scenario, not a locally estimated effect."

### part-02

- Location: Section 4.4, body paragraph 96, after the interpretation of lost indoor protection.
- Reason: supply relevant Japanese comparative evidence without selectively presenting only supportive findings or substituting morbidity estimates for mortality effects.
- Kila decisions: KILA-D-20261002-011, KILA-D-20261002-038, KILA-D-20261003-001
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T22:55:45Z
- Author: Kila
- Markup SHA-256 before: `a9aa53ddd871b8ba8794203fb8b86b2a1d1f871d467b3fdf4bb312f3bc9e7175`
- Markup SHA-256 after: `a214947a86c2b5149a6a050ec8cc3c844bb078db65558603e64dbbee1e41f5c8`
- Revision IDs: `945`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261003T075545364150.reviewer-3-comment-3.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
It represents the additional modeled burden that may accompany loss of indoor protection if suitable placement is not restored.
~~~~

- After:

~~~~text
It represents the additional modeled burden that may accompany loss of indoor protection if suitable placement is not restored. Comparative evidence supports attention to cooling but does not establish a transferable effect size: a multicountry longitudinal analysis including Japan associates greater residential air-conditioning prevalence with lower heat-related mortality, while measuring availability rather than actual use (Sera et al., 2020). After the 2011 earthquake, Japanese prefectures with larger electricity reductions showed lower rather than higher heat-related mortality, and daily electricity reduction did not significantly modify the heat–mortality association in Tokyo (Kim et al., 2017). Following the 2019 typhoon-related outage, an event study reports a short-lived increase in all-cause mortality and a longer increase in heat-related ambulance transport; a separate analysis finds stronger temperature-related ambulance risk under electricity reduction but no clear amplification of the temperature–mortality association (Yamasaki et al., 2024). These population-level studies concern air-conditioning prevalence, electricity conservation or outages, not verified loss of cooling among housing-displaced older residents, and therefore provide context rather than validation of our numerical contrast.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Comparative evidence supports attention to cooling but does not establish a transferable effect size: a multicountry longitudinal analysis including Japan associates greater residential air-conditioning prevalence with lower heat-related mortality, while measuring availability rather than actual use (Sera et al., 2020). After the 2011 earthquake, Japanese prefectures with larger electricity reductions showed lower rather than higher heat-related mortality, and daily electricity reduction did not significantly modify the heat–mortality association in Tokyo (Kim et al., 2017). Following the 2019 typhoon-related outage, an event study reports a short-lived increase in all-cause mortality and a longer increase in heat-related ambulance transport; a separate analysis finds stronger temperature-related ambulance risk under electricity reduction but no clear amplification of the temperature–mortality association (Yamasaki et al., 2024). These population-level studies concern air-conditioning prevalence, electricity conservation or outages, not verified loss of cooling among housing-displaced older residents, and therefore provide context rather than validation of our numerical contrast."

### part-03

- Location: Section 4.5, body paragraph 99, immediately after the existing Ontario nursing-home source sentence.
- Reason: make specific transfer limitations explicit rather than treating the source interval as Japanese-population uncertainty.
- Kila decisions: KILA-D-20261002-011, KILA-D-20261002-038, KILA-D-20261003-001
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T22:56:21Z
- Author: Kila
- Markup SHA-256 before: `a214947a86c2b5149a6a050ec8cc3c844bb078db65558603e64dbbee1e41f5c8`
- Markup SHA-256 after: `3f30b9c4643d5e656a1464ad1c0a13ba89337217ed3c183402c73df7238e8375`
- Revision IDs: `946`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261003T075622018582.reviewer-3-comment-3.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
That interval represents effect-parameter uncertainty, not total model uncertainty.
~~~~

- After:

~~~~text
That interval represents effect-parameter uncertainty, not total model uncertainty. Transfer from institutional nursing-home residents to community-dwelling older residents may be affected by differences in frailty, care provision, housing, cooling access and climatic acclimatization. The source uses a local heat-index threshold, whereas this study uses station-calibrated air-temperature scenarios; housing-related cooling loss and repeated exposure over a 30-day displacement period are not directly observed in the source study. The direction and magnitude of transfer bias remain unquantified, and the reported confidence interval does not cover these population, exposure or duration mismatches.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Transfer from institutional nursing-home residents to community-dwelling older residents may be affected by differences in frailty, care provision, housing, cooling access and climatic acclimatization. The source uses a local heat-index threshold, whereas this study uses station-calibrated air-temperature scenarios; housing-related cooling loss and repeated exposure over a 30-day displacement period are not directly observed in the source study. The direction and magnitude of transfer bias remain unquantified, and the reported confidence interval does not cover these population, exposure or duration mismatches."

## reviewer-1/comment-6

### part-01

- Location: Section 2.8, body paragraph 61, final sentence of health-effect sensitivity.
- Reason: define the requested alternative scenario distinctly from source confidence endpoints.
- Kila decisions: KILA-D-20261003-003, KILA-D-20261003-004
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T23:28:38Z
- Author: Kila
- Markup SHA-256 before: `89011af551143121ca6fcda9c3b94f701c2424120105843bea74f659375527c7`
- Markup SHA-256 after: `83700fbf9cc53996f9e46ab48aab40d7ebc03f36569a1075b018e6413bb84638`
- Revision IDs: `1014`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261003T082838833243.reviewer-1-comment-6.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The resulting lower and upper burden values therefore capture effect-parameter uncertainty alone.
~~~~

- After:

~~~~text
The resulting lower and upper burden values therefore capture effect-parameter uncertainty alone. Separately, we evaluate a hypothetical no-increment benchmark by setting the no-cooling relative odds ratio to 1 while retaining the effective-cooling heat multiplier of 1.03 and all other inputs. This benchmark tests the algebraic boundary of the transferred contrast, not a locally estimated effect or a confidence bound.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Separately, we evaluate a hypothetical no-increment benchmark by setting the no-cooling relative odds ratio to 1 while retaining the effective-cooling heat multiplier of 1.03 and all other inputs. This benchmark tests the algebraic boundary of the transferred contrast, not a locally estimated effect or a confidence bound."

### part-02

- Location: Section 3.5, body paragraph 83, immediately after the primary and source-endpoint relative results.
- Reason: report the alternative result without equating zero excess with zero mortality or presenting a tautology as validation.
- Kila decisions: KILA-D-20261003-003, KILA-D-20261003-004
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T23:28:57Z
- Author: Kila
- Markup SHA-256 before: `83700fbf9cc53996f9e46ab48aab40d7ebc03f36569a1075b018e6413bb84638`
- Markup SHA-256 after: `7426e68fd5dc1839ef709a6e67cd9379ff01dffba5db883332c414b418155205`
- Revision IDs: `1015`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261003T082857156343.reviewer-1-comment-6.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
These contrasts compare cooling states under the same outdoor conditions.
~~~~

- After:

~~~~text
These contrasts compare cooling states under the same outdoor conditions. In the hypothetical no-increment benchmark, both cooling states have identical modeled risks in every municipality, yielding a 0% relative increase and zero incremental expected deaths, while total expected mortality remains positive. This algebraic result shows dependence on the assumed cooling contrast; it does not validate the transferred effect or establish robustness to its absence.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " In the hypothetical no-increment benchmark, both cooling states have identical modeled risks in every municipality, yielding a 0% relative increase and zero incremental expected deaths, while total expected mortality remains positive. This algebraic result shows dependence on the assumed cooling contrast; it does not validate the transferred effect or establish robustness to its absence."

## reviewer-1/comment-5

### part-01

- Location: Section 2.7, paragraph beginning “We apply effect estimates on the odds scale”.
- Reason: identify the empirical source and distinguish the two effect parameters without altering Equation 9 or implying local calibration.
- Kila decisions: KILA-D-20261003-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T23:40:37Z
- Author: Kila
- Markup SHA-256 before: `7426e68fd5dc1839ef709a6e67cd9379ff01dffba5db883332c414b418155205`
- Markup SHA-256 after: `3860095a88787c0cf09e08f8b596d9c99ef3d3dd2f81247530ef7a9fa7057367`
- Revision IDs: `1016`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261003T084037315375.reviewer-1-comment-5.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Outdoor heat and the municipality baseline remain fixed across these states.
~~~~

- After:

~~~~text
The effective-cooling multiplier of 1.03 is the heat-associated mortality odds ratio among air-conditioned nursing homes in the same study (95% confidence interval, 0.98–1.07), not an estimated cooling-loss effect. Multiplying it by the relative odds ratio of 1.08 gives a no-cooling heat multiplier of 1.1124, consistent with the study's rounded estimate of 1.11. Outdoor heat and the municipality baseline remain fixed across these states.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: "The effective-cooling multiplier of 1.03 is the heat-associated mortality odds ratio among air-conditioned nursing homes in the same study (95% confidence interval, 0.98–1.07), not an estimated cooling-loss effect. Multiplying it by the relative odds ratio of 1.08 gives a no-cooling heat multiplier of 1.1124, consistent with the study's rounded estimate of 1.11. "

### part-02

- Location: Section 2.7, final paragraph.
- Reason: disclose the completed diagnostic without mislabeling it as joint uncertainty or changing the existing primary sensitivity.
- Kila decisions: KILA-D-20261003-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T23:40:49Z
- Author: Kila
- Markup SHA-256 before: `3860095a88787c0cf09e08f8b596d9c99ef3d3dd2f81247530ef7a9fa7057367`
- Markup SHA-256 after: `dcae9f3797c4b4def0a0b61f634ef263ba21d60045584147363f62076e4d8cc6`
- Revision IDs: `1017, 1018`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261003T084049815545.reviewer-1-comment-5.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Health-effect sensitivity varies only the transferred no-cooling effect across its reported interval.
~~~~

- After:

~~~~text
In an additional one-factor diagnostic, we set the effective-cooling heat multiplier to 0.98, 1.00, 1.03 and 1.07 while fixing the relative odds ratio at 1.08 and all other inputs. The endpoints are the source interval for the effective-cooling multiplier, not joint confidence limits; covariance between effect estimates is not modeled. This diagnostic changes both cooling-state heat multipliers while retaining their odds-ratio contrast. The primary health-effect sensitivity varies only the transferred no-cooling effect across its reported interval.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "Health-effect"
     - After: "In an additional one-factor diagnostic, we set the effective-cooling heat multiplier to 0.98, 1.00, 1.03 and 1.07 while fixing the relative odds ratio at 1.08 and all other inputs. The endpoints are the source interval for the effective-cooling multiplier, not joint confidence limits; covariance between effect estimates is not modeled. This diagnostic changes both cooling-state heat multipliers while retaining their odds-ratio contrast. The primary health-effect"

### part-03

- Location: Section 3.5, paragraph beginning “The fixed-weather health scenario varies geographically”.
- Reason: answer sensitivity of the central estimate using current rather than superseded 5.34% results.
- Kila decisions: KILA-D-20261003-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T23:41:01Z
- Author: Kila
- Markup SHA-256 before: `dcae9f3797c4b4def0a0b61f634ef263ba21d60045584147363f62076e4d8cc6`
- Markup SHA-256 after: `b9c1a82d2dd84d017244a3c03f98e5c623ffcdb50a54e4d705773cfae1f3d00e`
- Revision IDs: `1019`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261003T084102106086.reviewer-1-comment-5.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Summed across municipalities, the central expected-death planning magnitude is 0.03565.
~~~~

- After:

~~~~text
Summed across municipalities, the central expected-death planning magnitude is 0.03565. Across effective-cooling multipliers of 0.98, 1.00, 1.03 and 1.07, the aggregate relative burden increases are 5.22%, 5.26%, 5.31% and 5.38%, respectively, and incremental expected deaths range from 0.03392 to 0.03703. The central contrast is therefore only modestly sensitive to this multiplier over the tested range, conditional on the fixed relative odds ratio and other model inputs; this does not establish transferability to displaced older residents.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Across effective-cooling multipliers of 0.98, 1.00, 1.03 and 1.07, the aggregate relative burden increases are 5.22%, 5.26%, 5.31% and 5.38%, respectively, and incremental expected deaths range from 0.03392 to 0.03703. The central contrast is therefore only modestly sensitive to this multiplier over the tested range, conditional on the fixed relative odds ratio and other model inputs; this does not establish transferability to displaced older residents."

## reviewer-3/comment-4

### part-01

- Location: Section 4.4, paragraph beginning The health comparison isolates the protective function of cooling.
- Reason: Clarify the modeled estimate and conditional spatial drivers without changing results.
- Kila decisions: KILA-D-20261003-009
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-02T23:53:30Z
- Author: Kila
- Markup SHA-256 before: `b9c1a82d2dd84d017244a3c03f98e5c623ffcdb50a54e4d705773cfae1f3d00e`
- Markup SHA-256 after: `168a6b94aa1f14918162108c3826de3f18094b7ae439e953bb1154d108009d17`
- Revision IDs: `1020`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261003T085330379546.reviewer-3-comment-4.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
It represents the additional modeled burden that may accompany loss of indoor protection if suitable placement is not restored.
~~~~

- After:

~~~~text
It represents the additional modeled burden that may accompany loss of indoor protection if suitable placement is not restored. The prefecture-wide 5.31% increase is a model output obtained by applying transferred health parameters to local historical high-heat-day estimates and municipality mortality baselines, not evidence of an observed health effect in Kumamoto. Conditional on fixed effect parameters and a fixed baseline, differences in expected high-heat days determine the spatial variation in the relative contrast; expected-death magnitudes additionally depend on the modeled affected population.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The prefecture-wide 5.31% increase is a model output obtained by applying transferred health parameters to local historical high-heat-day estimates and municipality mortality baselines, not evidence of an observed health effect in Kumamoto. Conditional on fixed effect parameters and a fixed baseline, differences in expected high-heat days determine the spatial variation in the relative contrast; expected-death magnitudes additionally depend on the modeled affected population."

## reviewer-1/comment-8

### part-01

- Location: Section4.2, final sentence of paragraph beginning “Spatial prioritization should consider older-person exposure”.
- Reason: explicitly connect existing sensitivities to stable conclusions and unstable or unverified operational priorities without treating mechanical rank invariance as validation.
- Kila decisions: KILA-D-20261003-011
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-03T00:03:46Z
- Author: Kila
- Markup SHA-256 before: `168a6b94aa1f14918162108c3826de3f18094b7ae439e953bb1154d108009d17`
- Markup SHA-256 after: `0e22d02b590126bd1257a06dfcd9b0897d253752baffb76fb5a74bff73a4343b`
- Revision IDs: `1021`
- Backup: `Rev/revision/.kila-backups/KE01.rev.markup.20261003T090347009652.reviewer-1-comment-8.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The no-placement person-day bound should consequently trigger field verification and placement tracking rather than be interpreted as a measured deficit.
~~~~

- After:

~~~~text
The no-placement person-day bound should consequently trigger field verification and placement tracking rather than be interpreted as a measured deficit. Across the tested structural alternatives, the exposure top-five set is retained, but shaking scenarios shift individual exposure ranks by up to 24 places and retain only four of the five highest incremental-death municipalities. Broad high-demand screening is therefore more stable than detailed municipal sequencing or health-burden priorities. Engineering bundles preserve demand rankings because common per-person factors scale all municipalities, while changing resource quantities; this does not establish supply adequacy. Calibration tests do not establish stable priorities in unobserved areas: extending the MODIS station domain does not uniformly improve errors, and this temperature calibration is distinct from the threshold-day interpolation used in the mortality model. The latter's spatial error remains a limitation despite the small tested annual-aggregation difference. Health-effect sensitivities likewise support only conditional conclusions: the protected multiplier has a modest influence over its tested range, whereas the no-cooling effect endpoints materially change burden magnitude and the null-increment benchmark removes the modeled contrast. These separate tests support staged verification of high-demand areas, not a validated ordering of local deficits or a jointly quantified uncertainty range.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Across the tested structural alternatives, the exposure top-five set is retained, but shaking scenarios shift individual exposure ranks by up to 24 places and retain only four of the five highest incremental-death municipalities. Broad high-demand screening is therefore more stable than detailed municipal sequencing or health-burden priorities. Engineering bundles preserve demand rankings because common per-person factors scale all municipalities, while changing resource quantities; this does not establish supply adequacy. Calibration tests do not establish stable priorities in unobserved areas: extending the MODIS station domain does not uniformly improve errors, and this temperature calibration is distinct from the threshold-day interpolation used in the mortality model. The latter's spatial error remains a limitation despite the small tested annual-aggregation difference. Health-effect sensitivities likewise support only conditional conclusions: the protected multiplier has a modest influence over its tested range, whereas the no-cooling effect endpoints materially change burden magnitude and the null-increment benchmark removes the modeled contrast. These separate tests support staged verification of high-demand areas, not a validated ordering of local deficits or a jointly quantified uncertainty range."


## reviewer-3/comment-12 — supplementary artifact

### part-01

- Decision: KILA-D-20261003-014
- Action: Create complete supplementary Tables S2–S4; existing S1 unchanged.
- Before: No S2–S4 document.
- After: Rev/revision/KE01.supplementary-tables-S2-S4.docx; three continuous tables, each with 45 municipalities and one header.
- Source: Fresh pre-bundle clean 07e84e9ec1e017ac6f47587bb1e91d079cb4f6d1a0cff632a240bb399f435064. All cell values and row order match source-cells.json exactly.
- Artifact SHA256: 69b34730f3a41db2465c70ddea07a4a398534741bb70de711c62c50b5042c104
- Visual review: All nine rendered supplementary pages verified before copy; copied artifact identical.

## reviewer-3/comment-12

### part-02

- Location: Table 1, data rows11–45
- Reason: Retain ten-row main excerpt and preserve full table in supplement
- Kila decisions: KILA-D-20261003-013, KILA-D-20261003-014
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-03T00:34:31Z
- Author: Kila
- Markup SHA-256 before: `0e22d02b590126bd1257a06dfcd9b0897d253752baffb76fb5a74bff73a4343b`
- Markup SHA-256 after: `4f5c0e760f0b14403a8023c70c2a77904759e20424fc5953a2d4524dca010ec5`
- Revision IDs: `1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056`
- Backup: `/Users/lichao/Research/KE01/Rev/revision/.kila-backups/KE01.rev.markup.20261003T093431698035.reviewer-3-comment-12.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `all original row/cell formatting preserved`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
[["Municipality", "Functionally Lost Residences (Primary)", "Functionally Lost Residences (Scenario Range)", "Affected Population Age 65+ (Primary)", "Affected Population Age 65+ (Scenario Range)", "No-Placement Older-Person-Days"], ["Kumamoto City", "156.3", "35.8–304.9", "84.5", "20.6–180.1", "2,536.3"], ["Yatsushiro City", "38.2", "11.1–154.9", "29.7", "8.5–124.9", "891.2"], ["Uki City", "23.2", "5.2–117.9", "18.8", "4.1–96.0", "563.2"], ["Uto City", "11.5", "2.6–38.5", "8.3", "1.8–27.2", "247.7"], ["Hikawa Town", "4.5", "0.9–24.4", "4.6", "0.9–25.4", "138.0"], ["Tamana City", "5.6", "0.8–24.7", "4.6", "0.7–21.4", "137.1"], ["Koshi City", "7.1", "1.3–19.5", "4.3", "0.8–12.4", "127.7"], ["Mashiki Town", "5.4", "1.4–11.3", "4.1", "1.0–8.9", "122.7"], ["Mifune Town", "3.9", "0.9–10.6", "3.3", "0.7–8.8", "99.9"], ["Kamiamakusa City", "3.6", "0.7–9.8", "3.4", "0.6–9.4", "103.2"], ["Kikuchi City", "3.3", "0.3–16.0", "2.7", "0.3–13.8", "81.5"], ["Arao City", "2.8", "0.2–14.3", "2.3", "0.2–12.3", "67.6"], ["Kosa Town", "2.8", "0.5–7.9", "2.8", "0.6–8.1", "83.7"], ["Misato Town", "2.5", "0.5–6.8", "2.8", "0.5–7.4", "82.9"], ["Yamaga City", "2.7", "0.2–11.8", "2.5", "0.2–10.8", "73.7"], ["Kikuyo Town", "5.7", "0.8–13.4", "2.6", "0.4–6.8", "78.9"], ["Hitoyoshi City", "2.2", "0.2–9.8", "1.7", "0.2–8.0", "51.7"], ["Amakusa City", "3.4", "0.2–14.0", "3.0", "0.2–12.4", "90.0"], ["Kashima Town", "2.2", "0.6–5.0", "1.5", "0.4–3.7", "43.9"], ["Ozu Town", "3.5", "0.4–10.6", "1.8", "0.2–6.3", "54.0"], ["Asagiri Town", "0.8", "0.1–5.4", "0.8", "0.1–5.4", "24.3"], ["Aso City", "1.0", "0.1–6.1", "0.9", "0.1–5.8", "27.8"], ["Nagasu Town", "1.1", "0.1–5.0", "0.9", "0.1–4.4", "27.1"], ["Yamato Town", "1.5", "0.2–3.6", "1.8", "0.2–4.1", "53.9"], ["Minamata City", "1.1", "0.1–6.3", "0.9", "0.1–5.4", "27.5"], ["Ashikita Town", "1.4", "0.1–4.0", "1.5", "0.1–4.2", "44.6"], ["Taragi Town", "0.6", "0.1–3.3", "0.6", "0.1–3.5", "18.3"], ["Nishiki Town", "0.6", "0.1–3.3", "0.5", "0.05–3.1", "14.7"], ["Minamiaso Village", "0.7", "0.1–2.3", "0.7", "0.05–2.2", "21.4"], ["Nankan Town", "0.4", "0.03–2.5", "0.4", "0.03–2.5", "11.8"], ["Nishihara Village", "0.7", "0.1–2.0", "0.6", "0.1–1.6", "16.9"], ["Yunomae Town", "0.2", "0.03–1.5", "0.2", "0.03–1.6", "7.0"], ["Gyokuto Town", "0.5", "0.1–1.3", "0.4", "0.1–1.3", "13.4"], ["Nagomi Town", "0.5", "0.03–1.7", "0.5", "0.03–1.9", "15.2"], ["Sagara Village", "0.3", "0.03–1.2", "0.3", "0.03–1.4", "9.6"], ["Takamori Town", "0.3", "0.02–1.2", "0.3", "0.02–1.2", "8.8"], ["Yamae Village", "0.2", "0.03–0.9", "0.2", "0.03–0.9", "6.9"], ["Tsunagi Town", "0.2", "0.01–0.8", "0.2", "0.01–0.8", "7.3"], ["Mizukami Village", "0.1", "0.01–0.4", "0.1", "0.01–0.5", "4.3"], ["Kuma Village", "0.2", "0.01–0.6", "0.2", "0.01–0.6", "6.7"], ["Reihoku Town", "0.2", "0.003–0.9", "0.2", "0.003–0.8", "5.4"], ["Itsuki Village", "0.2", "0.02–0.3", "0.2", "0.02–0.3", "6.1"], ["Oguni Town", "0.1", "0.002–0.7", "0.1", "0.002–0.7", "3.7"], ["Minamioguni Town", "0.1", "0.002–0.4", "0.1", "0.002–0.4", "2.5"], ["Ubuyama Village", "0.03", "0.0004–0.1", "0.03", "0.0004–0.1", "0.9"]]
~~~~

- After:

~~~~text
[["Municipality", "Functionally Lost Residences (Primary)", "Functionally Lost Residences (Scenario Range)", "Affected Population Age 65+ (Primary)", "Affected Population Age 65+ (Scenario Range)", "No-Placement Older-Person-Days"], ["Kumamoto City", "156.3", "35.8–304.9", "84.5", "20.6–180.1", "2,536.3"], ["Yatsushiro City", "38.2", "11.1–154.9", "29.7", "8.5–124.9", "891.2"], ["Uki City", "23.2", "5.2–117.9", "18.8", "4.1–96.0", "563.2"], ["Uto City", "11.5", "2.6–38.5", "8.3", "1.8–27.2", "247.7"], ["Hikawa Town", "4.5", "0.9–24.4", "4.6", "0.9–25.4", "138.0"], ["Tamana City", "5.6", "0.8–24.7", "4.6", "0.7–21.4", "137.1"], ["Koshi City", "7.1", "1.3–19.5", "4.3", "0.8–12.4", "127.7"], ["Mashiki Town", "5.4", "1.4–11.3", "4.1", "1.0–8.9", "122.7"], ["Mifune Town", "3.9", "0.9–10.6", "3.3", "0.7–8.8", "99.9"], ["Kamiamakusa City", "3.6", "0.7–9.8", "3.4", "0.6–9.4", "103.2"]]
~~~~

- Minimal tracked fragments:
  1. `delete-rows`
     - Before: "[[\"Municipality\", \"Functionally Lost Residences (Primary)\", \"Functionally Lost Residences (Scenario Range)\", \"Affected Population Age 65+ (Primary)\", \"Affected Population Age 65+ (Scenario Range)\", \"No-Placement Older-Person-Days\"], [\"Kumamoto City\", \"156.3\", \"35.8–304.9\", \"84.5\", \"20.6–180.1\", \"2,536.3\"], [\"Yatsushiro City\", \"38.2\", \"11.1–154.9\", \"29.7\", \"8.5–124.9\", \"891.2\"], [\"Uki City\", \"23.2\", \"5.2–117.9\", \"18.8\", \"4.1–96.0\", \"563.2\"], [\"Uto City\", \"11.5\", \"2.6–38.5\", \"8.3\", \"1.8–27.2\", \"247.7\"], [\"Hikawa Town\", \"4.5\", \"0.9–24.4\", \"4.6\", \"0.9–25.4\", \"138.0\"], [\"Tamana City\", \"5.6\", \"0.8–24.7\", \"4.6\", \"0.7–21.4\", \"137.1\"], [\"Koshi City\", \"7.1\", \"1.3–19.5\", \"4.3\", \"0.8–12.4\", \"127.7\"], [\"Mashiki Town\", \"5.4\", \"1.4–11.3\", \"4.1\", \"1.0–8.9\", \"122.7\"], [\"Mifune Town\", \"3.9\", \"0.9–10.6\", \"3.3\", \"0.7–8.8\", \"99.9\"], [\"Kamiamakusa City\", \"3.6\", \"0.7–9.8\", \"3.4\", \"0.6–9.4\", \"103.2\"], [\"Kikuchi City\", \"3.3\", \"0.3–16.0\", \"2.7\", \"0.3–13.8\", \"81.5\"], [\"Arao City\", \"2.8\", \"0.2–14.3\", \"2.3\", \"0.2–12.3\", \"67.6\"], [\"Kosa Town\", \"2.8\", \"0.5–7.9\", \"2.8\", \"0.6–8.1\", \"83.7\"], [\"Misato Town\", \"2.5\", \"0.5–6.8\", \"2.8\", \"0.5–7.4\", \"82.9\"], [\"Yamaga City\", \"2.7\", \"0.2–11.8\", \"2.5\", \"0.2–10.8\", \"73.7\"], [\"Kikuyo Town\", \"5.7\", \"0.8–13.4\", \"2.6\", \"0.4–6.8\", \"78.9\"], [\"Hitoyoshi City\", \"2.2\", \"0.2–9.8\", \"1.7\", \"0.2–8.0\", \"51.7\"], [\"Amakusa City\", \"3.4\", \"0.2–14.0\", \"3.0\", \"0.2–12.4\", \"90.0\"], [\"Kashima Town\", \"2.2\", \"0.6–5.0\", \"1.5\", \"0.4–3.7\", \"43.9\"], [\"Ozu Town\", \"3.5\", \"0.4–10.6\", \"1.8\", \"0.2–6.3\", \"54.0\"], [\"Asagiri Town\", \"0.8\", \"0.1–5.4\", \"0.8\", \"0.1–5.4\", \"24.3\"], [\"Aso City\", \"1.0\", \"0.1–6.1\", \"0.9\", \"0.1–5.8\", \"27.8\"], [\"Nagasu Town\", \"1.1\", \"0.1–5.0\", \"0.9\", \"0.1–4.4\", \"27.1\"], [\"Yamato Town\", \"1.5\", \"0.2–3.6\", \"1.8\", \"0.2–4.1\", \"53.9\"], [\"Minamata City\", \"1.1\", \"0.1–6.3\", \"0.9\", \"0.1–5.4\", \"27.5\"], [\"Ashikita Town\", \"1.4\", \"0.1–4.0\", \"1.5\", \"0.1–4.2\", \"44.6\"], [\"Taragi Town\", \"0.6\", \"0.1–3.3\", \"0.6\", \"0.1–3.5\", \"18.3\"], [\"Nishiki Town\", \"0.6\", \"0.1–3.3\", \"0.5\", \"0.05–3.1\", \"14.7\"], [\"Minamiaso Village\", \"0.7\", \"0.1–2.3\", \"0.7\", \"0.05–2.2\", \"21.4\"], [\"Nankan Town\", \"0.4\", \"0.03–2.5\", \"0.4\", \"0.03–2.5\", \"11.8\"], [\"Nishihara Village\", \"0.7\", \"0.1–2.0\", \"0.6\", \"0.1–1.6\", \"16.9\"], [\"Yunomae Town\", \"0.2\", \"0.03–1.5\", \"0.2\", \"0.03–1.6\", \"7.0\"], [\"Gyokuto Town\", \"0.5\", \"0.1–1.3\", \"0.4\", \"0.1–1.3\", \"13.4\"], [\"Nagomi Town\", \"0.5\", \"0.03–1.7\", \"0.5\", \"0.03–1.9\", \"15.2\"], [\"Sagara Village\", \"0.3\", \"0.03–1.2\", \"0.3\", \"0.03–1.4\", \"9.6\"], [\"Takamori Town\", \"0.3\", \"0.02–1.2\", \"0.3\", \"0.02–1.2\", \"8.8\"], [\"Yamae Village\", \"0.2\", \"0.03–0.9\", \"0.2\", \"0.03–0.9\", \"6.9\"], [\"Tsunagi Town\", \"0.2\", \"0.01–0.8\", \"0.2\", \"0.01–0.8\", \"7.3\"], [\"Mizukami Village\", \"0.1\", \"0.01–0.4\", \"0.1\", \"0.01–0.5\", \"4.3\"], [\"Kuma Village\", \"0.2\", \"0.01–0.6\", \"0.2\", \"0.01–0.6\", \"6.7\"], [\"Reihoku Town\", \"0.2\", \"0.003–0.9\", \"0.2\", \"0.003–0.8\", \"5.4\"], [\"Itsuki Village\", \"0.2\", \"0.02–0.3\", \"0.2\", \"0.02–0.3\", \"6.1\"], [\"Oguni Town\", \"0.1\", \"0.002–0.7\", \"0.1\", \"0.002–0.7\", \"3.7\"], [\"Minamioguni Town\", \"0.1\", \"0.002–0.4\", \"0.1\", \"0.002–0.4\", \"2.5\"], [\"Ubuyama Village\", \"0.03\", \"0.0004–0.1\", \"0.03\", \"0.0004–0.1\", \"0.9\"]]"
     - After: "[[\"Municipality\", \"Functionally Lost Residences (Primary)\", \"Functionally Lost Residences (Scenario Range)\", \"Affected Population Age 65+ (Primary)\", \"Affected Population Age 65+ (Scenario Range)\", \"No-Placement Older-Person-Days\"], [\"Kumamoto City\", \"156.3\", \"35.8–304.9\", \"84.5\", \"20.6–180.1\", \"2,536.3\"], [\"Yatsushiro City\", \"38.2\", \"11.1–154.9\", \"29.7\", \"8.5–124.9\", \"891.2\"], [\"Uki City\", \"23.2\", \"5.2–117.9\", \"18.8\", \"4.1–96.0\", \"563.2\"], [\"Uto City\", \"11.5\", \"2.6–38.5\", \"8.3\", \"1.8–27.2\", \"247.7\"], [\"Hikawa Town\", \"4.5\", \"0.9–24.4\", \"4.6\", \"0.9–25.4\", \"138.0\"], [\"Tamana City\", \"5.6\", \"0.8–24.7\", \"4.6\", \"0.7–21.4\", \"137.1\"], [\"Koshi City\", \"7.1\", \"1.3–19.5\", \"4.3\", \"0.8–12.4\", \"127.7\"], [\"Mashiki Town\", \"5.4\", \"1.4–11.3\", \"4.1\", \"1.0–8.9\", \"122.7\"], [\"Mifune Town\", \"3.9\", \"0.9–10.6\", \"3.3\", \"0.7–8.8\", \"99.9\"], [\"Kamiamakusa City\", \"3.6\", \"0.7–9.8\", \"3.4\", \"0.6–9.4\", \"103.2\"]]"

### part-03

- Location: Table 2, data rows11–45
- Reason: Retain ten-row main excerpt and preserve full table in supplement
- Kila decisions: KILA-D-20261003-013, KILA-D-20261003-014
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-03T00:34:31Z
- Author: Kila
- Markup SHA-256 before: `4f5c0e760f0b14403a8023c70c2a77904759e20424fc5953a2d4524dca010ec5`
- Markup SHA-256 after: `65359974be4132901ca91a7326407ea4af641a0c3b5b7c439491a4e8cfc7ea5c`
- Revision IDs: `1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091`
- Backup: `/Users/lichao/Research/KE01/Rev/revision/.kila-backups/KE01.rev.markup.20261003T093431987943.reviewer-3-comment-12.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `all original row/cell formatting preserved`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
[["Municipality", "Affected Population Age 65+ (Central)", "No-Placement Older-Person-Days", "Expected High-Heat Days", "Peak Cooling Power kW (Central)", "Daily Cooling Electricity kWh (Central)"], ["Kumamoto City", "84.5", "2,536.3", "23.4", "11.90", "214.1"], ["Yatsushiro City", "29.7", "891.2", "19.0", "4.18", "75.2"], ["Uki City", "18.8", "563.2", "20.0", "2.64", "47.5"], ["Uto City", "8.3", "247.7", "20.8", "1.16", "20.9"], ["Hikawa Town", "4.6", "138.0", "19.0", "0.65", "11.7"], ["Tamana City", "4.6", "137.1", "23.4", "0.64", "11.6"], ["Koshi City", "4.3", "127.7", "17.7", "0.60", "10.8"], ["Mashiki Town", "4.1", "122.7", "12.0", "0.58", "10.4"], ["Mifune Town", "3.3", "99.9", "14.2", "0.47", "8.4"], ["Kamiamakusa City", "3.4", "103.2", "18.2", "0.48", "8.7"], ["Kikuchi City", "2.7", "81.5", "13.6", "0.38", "6.9"], ["Arao City", "2.3", "67.6", "22.7", "0.32", "5.7"], ["Kosa Town", "2.8", "83.7", "14.4", "0.39", "7.1"], ["Misato Town", "2.8", "82.9", "14.9", "0.39", "7.0"], ["Yamaga City", "2.5", "73.7", "13.7", "0.35", "6.2"], ["Kikuyo Town", "2.6", "78.9", "10.8", "0.37", "6.7"], ["Hitoyoshi City", "1.7", "51.7", "11.1", "0.24", "4.4"], ["Amakusa City", "3.0", "90.0", "17.9", "0.42", "7.6"], ["Kashima Town", "1.5", "43.9", "17.6", "0.21", "3.7"], ["Ozu Town", "1.8", "54.0", "10.1", "0.25", "4.6"], ["Asagiri Town", "0.8", "24.3", "10.6", "0.11", "2.1"], ["Aso City", "0.9", "27.8", "0.4", "0.13", "2.4"], ["Nagasu Town", "0.9", "27.1", "23.6", "0.13", "2.3"], ["Yamato Town", "1.8", "53.9", "4.8", "0.25", "4.6"], ["Minamata City", "0.9", "27.5", "15.9", "0.13", "2.3"], ["Ashikita Town", "1.5", "44.6", "16.2", "0.21", "3.8"], ["Taragi Town", "0.6", "18.3", "11.0", "0.09", "1.5"], ["Nishiki Town", "0.5", "14.7", "11.0", "0.07", "1.2"], ["Minamiaso Village", "0.7", "21.4", "2.2", "0.10", "1.8"], ["Nankan Town", "0.4", "11.8", "18.9", "0.06", "1.0"], ["Nishihara Village", "0.6", "16.9", "7.3", "0.08", "1.4"], ["Yunomae Town", "0.2", "7.0", "11.3", "0.03", "0.6"], ["Gyokuto Town", "0.4", "13.4", "21.3", "0.06", "1.1"], ["Nagomi Town", "0.5", "15.2", "16.1", "0.07", "1.3"], ["Sagara Village", "0.3", "9.6", "11.5", "0.05", "0.8"], ["Takamori Town", "0.3", "8.8", "0.6", "0.04", "0.7"], ["Yamae Village", "0.2", "6.9", "12.3", "0.03", "0.6"], ["Tsunagi Town", "0.2", "7.3", "16.0", "0.03", "0.6"], ["Mizukami Village", "0.1", "4.3", "12.3", "0.02", "0.4"], ["Kuma Village", "0.2", "6.7", "12.7", "0.03", "0.6"], ["Reihoku Town", "0.2", "5.4", "17.9", "0.03", "0.5"], ["Itsuki Village", "0.2", "6.1", "14.1", "0.03", "0.5"], ["Oguni Town", "0.1", "3.7", "1.4", "0.02", "0.3"], ["Minamioguni Town", "0.1", "2.5", "1.2", "0.01", "0.2"], ["Ubuyama Village", "0.03", "0.9", "1.0", "0.004", "0.1"]]
~~~~

- After:

~~~~text
[["Municipality", "Affected Population Age 65+ (Central)", "No-Placement Older-Person-Days", "Expected High-Heat Days", "Peak Cooling Power kW (Central)", "Daily Cooling Electricity kWh (Central)"], ["Kumamoto City", "84.5", "2,536.3", "23.4", "11.90", "214.1"], ["Yatsushiro City", "29.7", "891.2", "19.0", "4.18", "75.2"], ["Uki City", "18.8", "563.2", "20.0", "2.64", "47.5"], ["Uto City", "8.3", "247.7", "20.8", "1.16", "20.9"], ["Hikawa Town", "4.6", "138.0", "19.0", "0.65", "11.7"], ["Tamana City", "4.6", "137.1", "23.4", "0.64", "11.6"], ["Koshi City", "4.3", "127.7", "17.7", "0.60", "10.8"], ["Mashiki Town", "4.1", "122.7", "12.0", "0.58", "10.4"], ["Mifune Town", "3.3", "99.9", "14.2", "0.47", "8.4"], ["Kamiamakusa City", "3.4", "103.2", "18.2", "0.48", "8.7"]]
~~~~

- Minimal tracked fragments:
  1. `delete-rows`
     - Before: "[[\"Municipality\", \"Affected Population Age 65+ (Central)\", \"No-Placement Older-Person-Days\", \"Expected High-Heat Days\", \"Peak Cooling Power kW (Central)\", \"Daily Cooling Electricity kWh (Central)\"], [\"Kumamoto City\", \"84.5\", \"2,536.3\", \"23.4\", \"11.90\", \"214.1\"], [\"Yatsushiro City\", \"29.7\", \"891.2\", \"19.0\", \"4.18\", \"75.2\"], [\"Uki City\", \"18.8\", \"563.2\", \"20.0\", \"2.64\", \"47.5\"], [\"Uto City\", \"8.3\", \"247.7\", \"20.8\", \"1.16\", \"20.9\"], [\"Hikawa Town\", \"4.6\", \"138.0\", \"19.0\", \"0.65\", \"11.7\"], [\"Tamana City\", \"4.6\", \"137.1\", \"23.4\", \"0.64\", \"11.6\"], [\"Koshi City\", \"4.3\", \"127.7\", \"17.7\", \"0.60\", \"10.8\"], [\"Mashiki Town\", \"4.1\", \"122.7\", \"12.0\", \"0.58\", \"10.4\"], [\"Mifune Town\", \"3.3\", \"99.9\", \"14.2\", \"0.47\", \"8.4\"], [\"Kamiamakusa City\", \"3.4\", \"103.2\", \"18.2\", \"0.48\", \"8.7\"], [\"Kikuchi City\", \"2.7\", \"81.5\", \"13.6\", \"0.38\", \"6.9\"], [\"Arao City\", \"2.3\", \"67.6\", \"22.7\", \"0.32\", \"5.7\"], [\"Kosa Town\", \"2.8\", \"83.7\", \"14.4\", \"0.39\", \"7.1\"], [\"Misato Town\", \"2.8\", \"82.9\", \"14.9\", \"0.39\", \"7.0\"], [\"Yamaga City\", \"2.5\", \"73.7\", \"13.7\", \"0.35\", \"6.2\"], [\"Kikuyo Town\", \"2.6\", \"78.9\", \"10.8\", \"0.37\", \"6.7\"], [\"Hitoyoshi City\", \"1.7\", \"51.7\", \"11.1\", \"0.24\", \"4.4\"], [\"Amakusa City\", \"3.0\", \"90.0\", \"17.9\", \"0.42\", \"7.6\"], [\"Kashima Town\", \"1.5\", \"43.9\", \"17.6\", \"0.21\", \"3.7\"], [\"Ozu Town\", \"1.8\", \"54.0\", \"10.1\", \"0.25\", \"4.6\"], [\"Asagiri Town\", \"0.8\", \"24.3\", \"10.6\", \"0.11\", \"2.1\"], [\"Aso City\", \"0.9\", \"27.8\", \"0.4\", \"0.13\", \"2.4\"], [\"Nagasu Town\", \"0.9\", \"27.1\", \"23.6\", \"0.13\", \"2.3\"], [\"Yamato Town\", \"1.8\", \"53.9\", \"4.8\", \"0.25\", \"4.6\"], [\"Minamata City\", \"0.9\", \"27.5\", \"15.9\", \"0.13\", \"2.3\"], [\"Ashikita Town\", \"1.5\", \"44.6\", \"16.2\", \"0.21\", \"3.8\"], [\"Taragi Town\", \"0.6\", \"18.3\", \"11.0\", \"0.09\", \"1.5\"], [\"Nishiki Town\", \"0.5\", \"14.7\", \"11.0\", \"0.07\", \"1.2\"], [\"Minamiaso Village\", \"0.7\", \"21.4\", \"2.2\", \"0.10\", \"1.8\"], [\"Nankan Town\", \"0.4\", \"11.8\", \"18.9\", \"0.06\", \"1.0\"], [\"Nishihara Village\", \"0.6\", \"16.9\", \"7.3\", \"0.08\", \"1.4\"], [\"Yunomae Town\", \"0.2\", \"7.0\", \"11.3\", \"0.03\", \"0.6\"], [\"Gyokuto Town\", \"0.4\", \"13.4\", \"21.3\", \"0.06\", \"1.1\"], [\"Nagomi Town\", \"0.5\", \"15.2\", \"16.1\", \"0.07\", \"1.3\"], [\"Sagara Village\", \"0.3\", \"9.6\", \"11.5\", \"0.05\", \"0.8\"], [\"Takamori Town\", \"0.3\", \"8.8\", \"0.6\", \"0.04\", \"0.7\"], [\"Yamae Village\", \"0.2\", \"6.9\", \"12.3\", \"0.03\", \"0.6\"], [\"Tsunagi Town\", \"0.2\", \"7.3\", \"16.0\", \"0.03\", \"0.6\"], [\"Mizukami Village\", \"0.1\", \"4.3\", \"12.3\", \"0.02\", \"0.4\"], [\"Kuma Village\", \"0.2\", \"6.7\", \"12.7\", \"0.03\", \"0.6\"], [\"Reihoku Town\", \"0.2\", \"5.4\", \"17.9\", \"0.03\", \"0.5\"], [\"Itsuki Village\", \"0.2\", \"6.1\", \"14.1\", \"0.03\", \"0.5\"], [\"Oguni Town\", \"0.1\", \"3.7\", \"1.4\", \"0.02\", \"0.3\"], [\"Minamioguni Town\", \"0.1\", \"2.5\", \"1.2\", \"0.01\", \"0.2\"], [\"Ubuyama Village\", \"0.03\", \"0.9\", \"1.0\", \"0.004\", \"0.1\"]]"
     - After: "[[\"Municipality\", \"Affected Population Age 65+ (Central)\", \"No-Placement Older-Person-Days\", \"Expected High-Heat Days\", \"Peak Cooling Power kW (Central)\", \"Daily Cooling Electricity kWh (Central)\"], [\"Kumamoto City\", \"84.5\", \"2,536.3\", \"23.4\", \"11.90\", \"214.1\"], [\"Yatsushiro City\", \"29.7\", \"891.2\", \"19.0\", \"4.18\", \"75.2\"], [\"Uki City\", \"18.8\", \"563.2\", \"20.0\", \"2.64\", \"47.5\"], [\"Uto City\", \"8.3\", \"247.7\", \"20.8\", \"1.16\", \"20.9\"], [\"Hikawa Town\", \"4.6\", \"138.0\", \"19.0\", \"0.65\", \"11.7\"], [\"Tamana City\", \"4.6\", \"137.1\", \"23.4\", \"0.64\", \"11.6\"], [\"Koshi City\", \"4.3\", \"127.7\", \"17.7\", \"0.60\", \"10.8\"], [\"Mashiki Town\", \"4.1\", \"122.7\", \"12.0\", \"0.58\", \"10.4\"], [\"Mifune Town\", \"3.3\", \"99.9\", \"14.2\", \"0.47\", \"8.4\"], [\"Kamiamakusa City\", \"3.4\", \"103.2\", \"18.2\", \"0.48\", \"8.7\"]]"

### part-04

- Location: Table 3, data rows11–45
- Reason: Retain ten-row main excerpt and preserve full table in supplement
- Kila decisions: KILA-D-20261003-013, KILA-D-20261003-014
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-03T00:34:32Z
- Author: Kila
- Markup SHA-256 before: `65359974be4132901ca91a7326407ea4af641a0c3b5b7c439491a4e8cfc7ea5c`
- Markup SHA-256 after: `cb864ee87e5998616d64cdca3d2cd5a829ecce4e6beaf04eebe7cb5244150ebb`
- Revision IDs: `1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126`
- Backup: `/Users/lichao/Research/KE01/Rev/revision/.kila-backups/KE01.rev.markup.20261003T093432300637.reviewer-3-comment-12.part-04.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `all original row/cell formatting preserved`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
[["Municipality", "Expected High-Heat Days", "Incremental Excess Deaths (30 Days)", "Relative Mortality Burden Increase %", "Relative Mortality Burden Increase % Lower Effect Scenario", "Relative Mortality Burden Increase % Upper Effect Scenario"], ["Nagasu Town", "23.6", "0.00017", "6.32", "0.79", "11.86"], ["Kumamoto City", "23.4", "0.01681", "6.26", "0.78", "11.74"], ["Tamana City", "23.4", "0.00098", "6.26", "0.78", "11.74"], ["Arao City", "22.7", "0.00046", "6.09", "0.76", "11.42"], ["Gyokuto Town", "21.3", "0.00008", "5.71", "0.71", "10.71"], ["Uto City", "20.8", "0.00154", "5.60", "0.70", "10.49"], ["Uki City", "20.0", "0.00345", "5.39", "0.67", "10.10"], ["Yatsushiro City", "19.0", "0.00531", "5.12", "0.64", "9.60"], ["Hikawa Town", "19.0", "0.00089", "5.12", "0.64", "9.60"], ["Nankan Town", "18.9", "0.00008", "5.08", "0.64", "9.53"], ["Kamiamakusa City", "18.2", "0.00062", "4.91", "0.61", "9.21"], ["Reihoku Town", "17.9", "0.00003", "4.83", "0.60", "9.05"], ["Amakusa City", "17.9", "0.00055", "4.82", "0.60", "9.03"], ["Koshi City", "17.7", "0.00060", "4.76", "0.59", "8.92"], ["Kashima Town", "17.6", "0.00026", "4.73", "0.59", "8.86"], ["Ashikita Town", "16.2", "0.00025", "4.36", "0.54", "8.17"], ["Nagomi Town", "16.1", "0.00008", "4.35", "0.54", "8.16"], ["Tsunagi Town", "16.0", "0.00004", "4.32", "0.54", "8.10"], ["Minamata City", "15.9", "0.00013", "4.30", "0.54", "8.06"], ["Misato Town", "14.9", "0.00045", "4.02", "0.50", "7.54"], ["Kosa Town", "14.4", "0.00037", "3.89", "0.49", "7.30"], ["Mifune Town", "14.2", "0.00041", "3.84", "0.48", "7.20"], ["Itsuki Village", "14.1", "0.00003", "3.81", "0.48", "7.14"], ["Yamaga City", "13.7", "0.00032", "3.71", "0.46", "6.96"], ["Kikuchi City", "13.6", "0.00034", "3.69", "0.46", "6.92"], ["Kuma Village", "12.7", "0.00004", "3.43", "0.43", "6.43"], ["Yamae Village", "12.3", "0.00002", "3.34", "0.42", "6.26"], ["Mizukami Village", "12.3", "0.00002", "3.32", "0.42", "6.23"], ["Mashiki Town", "12.0", "0.00038", "3.24", "0.41", "6.08"], ["Sagara Village", "11.5", "0.00003", "3.13", "0.39", "5.87"], ["Yunomae Town", "11.3", "0.00003", "3.05", "0.38", "5.73"], ["Hitoyoshi City", "11.1", "0.00018", "3.02", "0.38", "5.66"], ["Taragi Town", "11.0", "0.00006", "2.99", "0.37", "5.60"], ["Nishiki Town", "11.0", "0.00005", "2.97", "0.37", "5.57"], ["Kikuyo Town", "10.8", "0.00019", "2.92", "0.37", "5.48"], ["Asagiri Town", "10.6", "0.00008", "2.89", "0.36", "5.41"], ["Ozu Town", "10.1", "0.00015", "2.74", "0.34", "5.14"], ["Nishihara Village", "7.3", "0.00004", "1.99", "0.25", "3.73"], ["Yamato Town", "4.8", "0.00009", "1.31", "0.16", "2.45"], ["Minamiaso Village", "2.2", "0.00001", "0.59", "0.07", "1.11"], ["Oguni Town", "1.4", "0.000002", "0.37", "0.05", "0.70"], ["Minamioguni Town", "1.2", "0.000001", "0.33", "0.04", "0.62"], ["Ubuyama Village", "1.0", "0.0000003", "0.27", "0.03", "0.51"], ["Takamori Town", "0.6", "0.000001", "0.15", "0.02", "0.28"], ["Aso City", "0.4", "0.000003", "0.10", "0.01", "0.18"]]
~~~~

- After:

~~~~text
[["Municipality", "Expected High-Heat Days", "Incremental Excess Deaths (30 Days)", "Relative Mortality Burden Increase %", "Relative Mortality Burden Increase % Lower Effect Scenario", "Relative Mortality Burden Increase % Upper Effect Scenario"], ["Nagasu Town", "23.6", "0.00017", "6.32", "0.79", "11.86"], ["Kumamoto City", "23.4", "0.01681", "6.26", "0.78", "11.74"], ["Tamana City", "23.4", "0.00098", "6.26", "0.78", "11.74"], ["Arao City", "22.7", "0.00046", "6.09", "0.76", "11.42"], ["Gyokuto Town", "21.3", "0.00008", "5.71", "0.71", "10.71"], ["Uto City", "20.8", "0.00154", "5.60", "0.70", "10.49"], ["Uki City", "20.0", "0.00345", "5.39", "0.67", "10.10"], ["Yatsushiro City", "19.0", "0.00531", "5.12", "0.64", "9.60"], ["Hikawa Town", "19.0", "0.00089", "5.12", "0.64", "9.60"], ["Nankan Town", "18.9", "0.00008", "5.08", "0.64", "9.53"]]
~~~~

- Minimal tracked fragments:
  1. `delete-rows`
     - Before: "[[\"Municipality\", \"Expected High-Heat Days\", \"Incremental Excess Deaths (30 Days)\", \"Relative Mortality Burden Increase %\", \"Relative Mortality Burden Increase % Lower Effect Scenario\", \"Relative Mortality Burden Increase % Upper Effect Scenario\"], [\"Nagasu Town\", \"23.6\", \"0.00017\", \"6.32\", \"0.79\", \"11.86\"], [\"Kumamoto City\", \"23.4\", \"0.01681\", \"6.26\", \"0.78\", \"11.74\"], [\"Tamana City\", \"23.4\", \"0.00098\", \"6.26\", \"0.78\", \"11.74\"], [\"Arao City\", \"22.7\", \"0.00046\", \"6.09\", \"0.76\", \"11.42\"], [\"Gyokuto Town\", \"21.3\", \"0.00008\", \"5.71\", \"0.71\", \"10.71\"], [\"Uto City\", \"20.8\", \"0.00154\", \"5.60\", \"0.70\", \"10.49\"], [\"Uki City\", \"20.0\", \"0.00345\", \"5.39\", \"0.67\", \"10.10\"], [\"Yatsushiro City\", \"19.0\", \"0.00531\", \"5.12\", \"0.64\", \"9.60\"], [\"Hikawa Town\", \"19.0\", \"0.00089\", \"5.12\", \"0.64\", \"9.60\"], [\"Nankan Town\", \"18.9\", \"0.00008\", \"5.08\", \"0.64\", \"9.53\"], [\"Kamiamakusa City\", \"18.2\", \"0.00062\", \"4.91\", \"0.61\", \"9.21\"], [\"Reihoku Town\", \"17.9\", \"0.00003\", \"4.83\", \"0.60\", \"9.05\"], [\"Amakusa City\", \"17.9\", \"0.00055\", \"4.82\", \"0.60\", \"9.03\"], [\"Koshi City\", \"17.7\", \"0.00060\", \"4.76\", \"0.59\", \"8.92\"], [\"Kashima Town\", \"17.6\", \"0.00026\", \"4.73\", \"0.59\", \"8.86\"], [\"Ashikita Town\", \"16.2\", \"0.00025\", \"4.36\", \"0.54\", \"8.17\"], [\"Nagomi Town\", \"16.1\", \"0.00008\", \"4.35\", \"0.54\", \"8.16\"], [\"Tsunagi Town\", \"16.0\", \"0.00004\", \"4.32\", \"0.54\", \"8.10\"], [\"Minamata City\", \"15.9\", \"0.00013\", \"4.30\", \"0.54\", \"8.06\"], [\"Misato Town\", \"14.9\", \"0.00045\", \"4.02\", \"0.50\", \"7.54\"], [\"Kosa Town\", \"14.4\", \"0.00037\", \"3.89\", \"0.49\", \"7.30\"], [\"Mifune Town\", \"14.2\", \"0.00041\", \"3.84\", \"0.48\", \"7.20\"], [\"Itsuki Village\", \"14.1\", \"0.00003\", \"3.81\", \"0.48\", \"7.14\"], [\"Yamaga City\", \"13.7\", \"0.00032\", \"3.71\", \"0.46\", \"6.96\"], [\"Kikuchi City\", \"13.6\", \"0.00034\", \"3.69\", \"0.46\", \"6.92\"], [\"Kuma Village\", \"12.7\", \"0.00004\", \"3.43\", \"0.43\", \"6.43\"], [\"Yamae Village\", \"12.3\", \"0.00002\", \"3.34\", \"0.42\", \"6.26\"], [\"Mizukami Village\", \"12.3\", \"0.00002\", \"3.32\", \"0.42\", \"6.23\"], [\"Mashiki Town\", \"12.0\", \"0.00038\", \"3.24\", \"0.41\", \"6.08\"], [\"Sagara Village\", \"11.5\", \"0.00003\", \"3.13\", \"0.39\", \"5.87\"], [\"Yunomae Town\", \"11.3\", \"0.00003\", \"3.05\", \"0.38\", \"5.73\"], [\"Hitoyoshi City\", \"11.1\", \"0.00018\", \"3.02\", \"0.38\", \"5.66\"], [\"Taragi Town\", \"11.0\", \"0.00006\", \"2.99\", \"0.37\", \"5.60\"], [\"Nishiki Town\", \"11.0\", \"0.00005\", \"2.97\", \"0.37\", \"5.57\"], [\"Kikuyo Town\", \"10.8\", \"0.00019\", \"2.92\", \"0.37\", \"5.48\"], [\"Asagiri Town\", \"10.6\", \"0.00008\", \"2.89\", \"0.36\", \"5.41\"], [\"Ozu Town\", \"10.1\", \"0.00015\", \"2.74\", \"0.34\", \"5.14\"], [\"Nishihara Village\", \"7.3\", \"0.00004\", \"1.99\", \"0.25\", \"3.73\"], [\"Yamato Town\", \"4.8\", \"0.00009\", \"1.31\", \"0.16\", \"2.45\"], [\"Minamiaso Village\", \"2.2\", \"0.00001\", \"0.59\", \"0.07\", \"1.11\"], [\"Oguni Town\", \"1.4\", \"0.000002\", \"0.37\", \"0.05\", \"0.70\"], [\"Minamioguni Town\", \"1.2\", \"0.000001\", \"0.33\", \"0.04\", \"0.62\"], [\"Ubuyama Village\", \"1.0\", \"0.0000003\", \"0.27\", \"0.03\", \"0.51\"], [\"Takamori Town\", \"0.6\", \"0.000001\", \"0.15\", \"0.02\", \"0.28\"], [\"Aso City\", \"0.4\", \"0.000003\", \"0.10\", \"0.01\", \"0.18\"]]"
     - After: "[[\"Municipality\", \"Expected High-Heat Days\", \"Incremental Excess Deaths (30 Days)\", \"Relative Mortality Burden Increase %\", \"Relative Mortality Burden Increase % Lower Effect Scenario\", \"Relative Mortality Burden Increase % Upper Effect Scenario\"], [\"Nagasu Town\", \"23.6\", \"0.00017\", \"6.32\", \"0.79\", \"11.86\"], [\"Kumamoto City\", \"23.4\", \"0.01681\", \"6.26\", \"0.78\", \"11.74\"], [\"Tamana City\", \"23.4\", \"0.00098\", \"6.26\", \"0.78\", \"11.74\"], [\"Arao City\", \"22.7\", \"0.00046\", \"6.09\", \"0.76\", \"11.42\"], [\"Gyokuto Town\", \"21.3\", \"0.00008\", \"5.71\", \"0.71\", \"10.71\"], [\"Uto City\", \"20.8\", \"0.00154\", \"5.60\", \"0.70\", \"10.49\"], [\"Uki City\", \"20.0\", \"0.00345\", \"5.39\", \"0.67\", \"10.10\"], [\"Yatsushiro City\", \"19.0\", \"0.00531\", \"5.12\", \"0.64\", \"9.60\"], [\"Hikawa Town\", \"19.0\", \"0.00089\", \"5.12\", \"0.64\", \"9.60\"], [\"Nankan Town\", \"18.9\", \"0.00008\", \"5.08\", \"0.64\", \"9.53\"]]"

### part-05

- Location: Table 1 caption
- Reason: Explain excerpt and point to complete supplement
- Kila decisions: KILA-D-20261003-014
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-03T00:34:32Z
- Author: Kila
- Markup SHA-256 before: `cb864ee87e5998616d64cdca3d2cd5a829ecce4e6beaf04eebe7cb5244150ebb`
- Markup SHA-256 after: `9c2c2a695d5df9b35149d29f70616584428e84c0af9a234079762b6594d13fff`
- Revision IDs: `1127`
- Backup: `/Users/lichao/Research/KE01/Rev/revision/.kila-backups/KE01.rev.markup.20261003T093432720087.reviewer-3-comment-12.part-05.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `5017784f5cca96911d02c75702284e2458f97a555bee88c1cf2aa939b54390c5`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Table 1. Municipality Housing Loss and Cooling Need
~~~~

- After:

~~~~text
Table 1. Municipality Housing Loss and Cooling Need. Ten municipalities are shown in the existing table order; Table S2 provides all 45 municipalities. This excerpt is not a validated intervention ranking.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: ". Ten municipalities are shown in the existing table order; Table S2 provides all 45 municipalities. This excerpt is not a validated intervention ranking."

### part-06

- Location: Table 2 caption
- Reason: Explain excerpt and point to complete supplement
- Kila decisions: KILA-D-20261003-014
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-03T00:34:32Z
- Author: Kila
- Markup SHA-256 before: `9c2c2a695d5df9b35149d29f70616584428e84c0af9a234079762b6594d13fff`
- Markup SHA-256 after: `640a635266ea9fe20b905a52d2fdbfe34c7d071f47a622e75d10152ba51eb4c4`
- Revision IDs: `1128`
- Backup: `/Users/lichao/Research/KE01/Rev/revision/.kila-backups/KE01.rev.markup.20261003T093433152683.reviewer-3-comment-12.part-06.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `5017784f5cca96911d02c75702284e2458f97a555bee88c1cf2aa939b54390c5`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Table 2. Municipality Cooling Electricity Planning Summary
~~~~

- After:

~~~~text
Table 2. Municipality Cooling Electricity Planning Summary. Ten municipalities are shown in the existing table order; Table S3 provides all 45 municipalities. This excerpt is not a validated intervention ranking.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: ". Ten municipalities are shown in the existing table order; Table S3 provides all 45 municipalities. This excerpt is not a validated intervention ranking."

### part-07

- Location: Table 3 caption
- Reason: Explain excerpt and point to complete supplement
- Kila decisions: KILA-D-20261003-014
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-10-03T00:34:33Z
- Author: Kila
- Markup SHA-256 before: `640a635266ea9fe20b905a52d2fdbfe34c7d071f47a622e75d10152ba51eb4c4`
- Markup SHA-256 after: `fcf9c721c8776d947fa257e4e62c6d399fe721fd235b0bb02531c40a4eb4bb66`
- Revision IDs: `1129`
- Backup: `/Users/lichao/Research/KE01/Rev/revision/.kila-backups/KE01.rev.markup.20261003T093433530097.reviewer-3-comment-12.part-07.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `5017784f5cca96911d02c75702284e2458f97a555bee88c1cf2aa939b54390c5`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Table 3. Municipality Cooling-Loss Health-Risk Summary
~~~~

- After:

~~~~text
Table 3. Municipality Cooling-Loss Health-Risk Summary. Ten municipalities are shown in the existing table order; Table S4 provides all 45 municipalities. This excerpt is not a validated intervention ranking.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: ". Ten municipalities are shown in the existing table order; Table S4 provides all 45 municipalities. This excerpt is not a validated intervention ranking."


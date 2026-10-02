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


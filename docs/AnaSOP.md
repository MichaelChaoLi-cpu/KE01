# AnaSOP
Analysis Standard Operating Procedure

## 1. Research Objective

### Central Research Question

- Research question: During the first 30 days after the 2026 Kumamoto earthquake, where are older residents likely to lose effective protection from heat, and which shelters face a deficit in accessible cooling capacity under uncertainty about housing damage?
- Why it matters: Emergency decisions concern whether vulnerable residents can remain safe, not only whether a roof is visibly collapsed. A house may cease to provide heat protection because it is structurally unsafe, inaccessible, without power or water, or abandoned after nearby ground failure. Reframing the endpoint as loss of effective heat-protective shelter links early damage evidence directly to cooling allocation.
- Data support currently visible: Government aerial photographs and official incident reports provide early damage evidence; deformation and secondary-hazard products can localize high-risk zones; processed small-area population data provide counts of older residents and vulnerable older households. Post-event heat, building footprints, shelter attributes, outages, and registered damage outcomes remain incomplete or pending.
- Key readable variables or data scope: Building-level probability of functional housing loss; confirmed damage lower bound; older residents and older households exposed by grid; observed and scenario-based heat stress; shelter accessibility, occupancy, air-conditioning, backup power, and effective cooled capacity.
- What would verify it: Later official building inspections should be spatially concentrated in high-probability loss grids; observed shelter demand or displacement should rise with estimated loss of heat-protective housing; and shelters classified as cooling-deficit locations should show demand exceeding verified cooled capacity during hot periods.
- What would falsify or weaken it: Image and hazard proxies fail to predict later inspected damage; high-risk grids show little displacement; temperatures remain below hazardous levels; or nearby shelters retain sufficient accessible cooled capacity throughout the event window.
- Required next feasibility check: Acquire building footprints, gridded shaking or hazard measures, shelter facility attributes, outage information, and a defensible post-event weather source; determine whether later official damage records can be spatially linked for validation.

### Supporting Research Questions

#### Supporting Point 1

- Role relative to central point: measurement
- Research question: How many buildings were confirmed, probable, or at elevated probability of becoming uninhabitable, and how uncertain is the expected loss count in each analysis grid?
- Why it matters: A single deep-learning label would overstate precision. A layered estimate preserves immediate operational value while distinguishing observed damage from modeled risk.
- Data support currently visible: Government post-event photographs cover the focal municipalities; official reports provide a small confirmed lower bound; image-screening experiments show that generic zero-shot recognition can rank scenes but cannot independently identify or count collapsed houses.
- Key readable variables or data scope: Confirmed incident indicator, building footprint, image visibility and quality, pre/post change evidence, roof or debris anomaly, shaking intensity, distance to mapped displacement boundary, secondary-hazard exposure, building vulnerability proxy, and validation status.
- What would verify it: A damage-specific model calibrated against geolocated manual or official labels should recover later inspected damage with acceptable precision, recall, spatial calibration, and count error.
- What would falsify or weaken it: Pre/post registration remains unavailable, official cases cannot be geolocated, roof-intact structural failures dominate, or probability estimates are poorly calibrated against later inspection records.
- Required next feasibility check: Confirm building-footprint coverage and registration-quality imagery; construct damage-specific validation labels; compare an image-only baseline against a multimodal model using hazard and building context.

For grid (g), report an expected count rather than an unqualified destroyed-building count:

\[
E[D_g] = \sum_{i \in g} p_i,
\]

where \(p_i\) is the calibrated probability that building \(i\) has lost safe habitability. Report confirmed cases separately as a lower bound and retain uncertainty intervals around \(E[D_g]\).

#### Supporting Point 2

- Role relative to central point: exposure heterogeneity
- Research question: How many residents, especially residents aged 65+, 75+, and 85+ and older people living alone, are expected to live in grids with functional housing loss?
- Why it matters: The affected population cannot be inferred by assigning all residents of a municipality or grid to the damaged category. Expected exposure should vary with the estimated share of housing rendered unsafe.
- Data support currently visible: Population and vulnerable-household counts are available at fine grid or official disclosure-group geography, with explicit suppression handling.
- Key readable variables or data scope: Total population, older-population counts and shares, older single-person and older-couple households, expected functionally lost dwellings, residential building stock, and grid-level exposure uncertainty.
- What would verify it: Estimated affected populations should be consistent with later displacement, shelter-registration, welfare-check, or damage-certificate counts after accounting for residents who relocate privately.
- What would falsify or weaken it: Population baselines are too outdated, disclosure aggregation prevents meaningful spatial linkage, or housing-loss probability has no measurable relationship with subsequent displacement.
- Required next feasibility check: Build common grid geometry, link residential building footprints to population disclosure groups, and test alternative allocation rules instead of assuming uniform population within a grid.

#### Supporting Point 3

- Role relative to central point: heat mechanism
- Research question: What daytime and nighttime heat-stress conditions are plausible during days 0-30, and how do they differ from the same calendar period in 2021-2025?
- Why it matters: Satellite land-surface temperature alone does not measure the air temperature experienced by people and cannot provide a reliable one-month forecast. A combined observed, forecast, and historical-scenario design is needed.
- Data support currently visible: Event-window station observations and historical weather records are partially available; gridded satellite surface temperature and operational heat-stress or forecast data remain to be acquired.
- Key readable variables or data scope: Maximum air temperature, minimum air temperature, humidity or heat-stress index, hot-day and hot-night duration, land-surface temperature anomaly, forecast scenario, and uncertainty band.
- What would verify it: Independent stations and gridded products should show consistent spatial and temporal heat rankings, and realized temperatures should fall within the pre-specified scenario intervals.
- What would falsify or weaken it: Persistent cloud prevents useful satellite retrievals, historical years poorly represent current conditions, or land-surface temperature does not agree with near-surface heat stress in populated grids.
- Required next feasibility check: Compare station observations, operational forecasts, and satellite products; choose explicit daytime and nighttime thresholds before calculating exposure.

#### Supporting Point 4

- Role relative to central point: policy decision
- Research question: Which shelters have insufficient effective cooled capacity for the expected number of heat-vulnerable displaced residents within an accessible catchment?
- Why it matters: Shelter location alone does not establish protection. Air-conditioning, backup electricity, usable cooled floor area, current occupancy, operating hours, transport access, and the needs of residents with limited mobility determine effective capacity.
- Data support currently visible: Public shelter locations can support an initial accessibility layer, but verified cooling equipment, power resilience, occupancy, and usable capacity are not yet present in the analytical data.
- Key readable variables or data scope: Expected older displaced residents, travel time or distance, shelter occupancy, accessible cooled spaces, air-conditioning status, backup power, outage duration, medical support, and effective cooled capacity.
- What would verify it: Facility checks or operational records confirm that predicted deficit shelters have demand exceeding functioning cooled capacity during hazardous heat periods.
- What would falsify or weaken it: Most exposed residents remain in safe cooled housing, relocate outside public shelters, or shelters have larger functioning capacity than public records imply.
- Required next feasibility check: Obtain or rapidly survey shelter HVAC, backup-power, occupancy, accessibility, and usable-capacity attributes; define a transparent catchment-allocation rule.

For shelter (s) and day (t), define a decision-facing deficit:

\[
Gap_s(t) = Demand_{65+,s}(t) - Capacity_{cool,s}(t).
\]

A positive value indicates that expected older-person demand exceeds verified effective cooled capacity. Both terms must be reported with uncertainty rather than as exact counts.

### Scope of Analysis

- Event: The 2026 Kumamoto earthquake beginning on 2026-07-28.
- Geographic frame: Kumamoto Prefecture for consistent mapping, with primary implementation in Uki City, Hikawa Town, and Yatsushiro City.
- Units of analysis: Buildings for loss probability; harmonized small-area grids for population and heat exposure; shelter catchments for cooling-capacity decisions.
- Population: All residents, with primary strata for ages 65+, 75+, and 85+, older single-person households, and older-couple households.
- Immediate period: Days 0-14 for rapid response.
- Extended period: Days 0-30 for heat-exposure and shelter planning.
- Historical heat reference: Matching calendar periods in 2021-2025.
- Damage reporting layers: Confirmed observed cases, probable image-supported cases, and modeled elevated-risk buildings must remain separate.

### Study Design Declaration

- Research type: applied
- Study design: Two-stage applied rapid-assessment study. Stage 1 produces an uncertainty-aware nowcast of functional housing loss, older-person exposure, heat stress, and shelter cooling deficits. Stage 2 validates and recalibrates the nowcast when official building inspections, displacement records, or shelter operations data become available.
- Interpretation limit: The initial products estimate where loss and unmet cooling demand are likely; they do not establish an exact destroyed-building count, identify earthquake-attributable deaths, or prove that every resident assigned to a high-risk grid was displaced.

## 2. Theoretical Background  /  Conceptual Framework  /  Problem Formulation

Research type: applied
Section focus: Early decision support under delayed damage statistics and measurement uncertainty.

### Research Gap

- Rapid disaster mapping often treats visible structural destruction as the endpoint, while heat-health planning treats population, weather, and shelters separately. This separation cannot answer whether older residents have lost access to a safe cooled environment.
- Post-event-only aerial images can detect some large debris fields but miss roof-intact buckling and internal damage. Generic image-recognition scores are therefore unsuitable as direct destroyed-building counts.
- Official damage statistics arrive later, but delayed labels create an opportunity for retrospective validation of an early nowcasting model rather than a reason to postpone all analysis.

### Conceptual Framework

- The policy-relevant construct is functional loss of heat-protective shelter, defined as collapse, unsafe occupancy, inaccessible housing, or loss of essential cooling-enabling services. It is broader than visually confirmed roof collapse and narrower than general earthquake exposure.
- The pathway is: earthquake shaking and ground failure -> probability of functional housing loss -> displacement or reduced household cooling -> heat exposure interacting with older-age vulnerability -> demand for accessible cooled shelter.
- Deep learning contributes evidence to the housing-loss probability but does not determine the final label alone. Official incident reports, deformation and secondary-hazard layers, building context, image visibility, and later inspection records provide complementary evidence.
- Older residents may remain at home, move to public shelters, stay with relatives, sleep in vehicles, or relocate elsewhere. Shelter-demand estimates must therefore use scenarios rather than equate housing loss with public-shelter occupancy.
- Scope boundary: The study prioritizes early spatial decision support and validation. It does not initially claim causal health effects or complete building-level loss enumeration.

### Problem Formulation

- Stage 1 estimates a calibrated probability of functional housing loss for each building where evidence permits and aggregates expected counts to a common grid. It reports confirmed, probable, and modeled-risk layers separately.
- Stage 1 combines grid-level expected housing loss with older-population and household vulnerability, then overlays observed and scenario-based daytime and nighttime heat stress.
- Expected vulnerable demand is allocated to reachable shelters under explicit mobility and relocation scenarios. Effective cooled capacity is measured from functioning equipment, power resilience, usable space, and current occupancy.
- The primary decision output is a map and table of cooling-protection deficits with uncertainty intervals and evidence grades, supported by separate housing-loss, population, heat, and shelter-capacity components.
- Stage 2 compares early predictions with later official inspection, displacement, and shelter-use data. Prediction error, calibration, and missed-case analysis are research outcomes in their own right.
- Interpretation limit: A building-loss probability is not an inspection result; expected affected population is not observed displacement; satellite land-surface temperature is not indoor heat; nominal shelter capacity is not effective cooled capacity; and a risk nowcast is not a causal estimate of mortality.

## 3. Data Overview

### Data Scope

- Data sources reviewed: 37
- Variables summarized: 521
- Distribution plots generated: 80
- Files skipped during briefing: 2

| Data source | Rows | Columns |
| --- | ---: | ---: |
| Data source 1 | 9 | 26 |
| Data source 2 | 1315 | 11 |
| Data source 3 | 1315 | 10 |
| Data source 4 | 1713 | 17 |
| Data source 5 | 1713 | 16 |
| Data source 6 | 36657 | 26 |
| Data source 7 | 1036590 | 9 |
| Data source 8 | 5 | 17 |
| Data source 9 | 35 | 19 |
| Data source 10 | 300 | 16 |
| Data source 11 | 2550 | 18 |
| Data source 12 | 2561 | 14 |
| Data source 13 | 1660 | 8 |
| Data source 14 | 917 | 13 |
| Data source 15 | 4470 | 15 |
| Data source 16 | 8661 | 15 |
| Data source 17 | 36657 | 19 |
| Data source 18 | 62945 | 10 |
| Data source 19 | 14 | 24 |
| Data source 20 | 62945 | 24 |
| Data source 21 | 36657 | 33 |
| Data source 22 | 9608 | 6 |
| Data source 23 | 316 | 8 |
| Data source 24 | 12 | 9 |
| Data source 25 | 170 | 12 |
| Data source 26 | 4 | 13 |
| Data source 27 | 80 | 11 |
| Data source 28 | 2045 | 9 |
| Data source 29 | 7671 | 9 |
| Data source 30 | 2910 | 13 |
| Data source 31 | 11 | 8 |
| Data source 32 | 2910 | 9 |
| Data source 33 | 18 | 11 |
| Data source 34 | 2910 | 13 |
| Data source 35 | 1315 | 10 |
| Data source 36 | 1713 | 16 |
| Data source 37 | 46 | 4 |

### Time-Series Candidates

Potential time-series structure was detected in 17 data source(s).
Specific source files and original column names remain in the data-briefing artifacts, not in AnaSOP.

### Data Limitations

- 2 file(s) were skipped during briefing; see the data-briefing artifacts for technical details.
- Treat this section as exploratory; final variable decisions belong to Section 4.
- AnaSOP intentionally avoids raw dataset names, source file paths, and original column names.
## 4. Variable Construction  /  Key Variables

### Evidence Architecture and Construction Rules

The rapid assessment uses four linked analytical tables rather than forcing official totals, incident reports, service interruptions, and modeled grid exposure into a single building-level dataset.

1. **Housing Damage Snapshots** preserve each official report time as a separate prefecture- or municipality-level claim.
2. **Damage Evidence Registry** stores one evidence claim at one observation time and spatial resolution. A row may describe one asset, multiple assets reported together, or an updated claim about an earlier event.
3. **Service Disruption Snapshots** distinguish policy coverage, such as an evacuation instruction, from observed evacuation, power loss, water loss, or cooling loss.
4. **Grid Exposure Estimates** contain the population and mapped-building denominators needed for estimation, but housing-loss and affected-population fields remain missing until spatial damage evidence supports allocation.

Construction follows these non-negotiable rules:

- Blank official-report cells are unknown, not zero.
- Every record retains observation time, source organization, source URL, report number, and source page.
- Prefecture totals are never spread uniformly across buildings or population grids.
- Evacuation-instruction coverage is not observed evacuation and is not confirmed loss of cooling.
- Municipality-only incident descriptions retain missing coordinates; coordinates are never inferred from a municipality centroid and presented as an event location.
- Later evidence is linked through a supersession field rather than overwriting earlier claims.
- Official housing totals, image-supported evidence, and modeled loss estimates remain analytically separate.

The initial official time series records an early report in which the Kumamoto housing total was not yet reported and subsequent preliminary prefecture snapshots. The latest acquired prefecture snapshot reports 181 fully collapsed, 245 half-collapsed, and 1,419 partially damaged residences, totaling 1,845 reported affected residences. A Kumamoto City snapshot provides the first sub-prefecture split: Minami Ward reported four fully collapsed residences and approximately 35 additional residences ranging from partial damage to half collapse. City pre-assessment further identifies Tomiai and Jonan as the principal housing-damage cluster, but the remaining prefecture total is not yet spatially allocated.

### Housing Damage Snapshot Variables

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Snapshot ID | Official Housing-Damage Snapshot ID | linkage | Unique identifier for one geographic claim in one official report snapshot. | Constructed from reporting organization, report number, and geographic unit. | yes |
| Observation Time | Official Report Observation Time | time index | Time at which the official situation report was issued. | Parsed as a timezone-aware timestamp and normalized internally to UTC. | yes |
| Geographic Level | Housing-Damage Reporting Geography | spatial scale | Spatial resolution represented by the reported counts. | Coded as prefecture, municipality, or another explicitly reported aggregate; it is never assumed to be building-level. | yes |
| Municipality | Reported Municipality | spatial linkage | Municipality to which the claim applies, when reported separately. | Missing for prefecture-level totals. | yes |
| Full Collapse Buildings | Officially Reported Fully Collapsed Residences | observed outcome | Number of residences classified as fully collapsed in the report snapshot. | Retained as a nullable integer; blank source cells remain missing. | yes |
| Half Collapse Buildings | Officially Reported Half-Collapsed Residences | observed outcome | Number of residences classified as half-collapsed in the report snapshot. | Retained as a nullable integer; blank source cells remain missing. | yes |
| Partial Damage Buildings | Officially Reported Partially Damaged Residences | observed outcome | Number of residences classified as partially damaged in the report snapshot. | Retained as a nullable integer; blank source cells remain missing. | yes |
| Reported Affected Buildings | Officially Reported Affected Residences | observed outcome | Sum of the reported residential damage categories included in the source table. | Validated against the component total when all relevant components are present. | yes |
| Data Status | Official Housing-Damage Data Status | quality control | Whether the value is reported, preliminary, revised, or absent from the official table. | Explicit categorical field; an absent early total is coded as not reported, not zero. | yes |

### Damage Evidence Registry Variables

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Evidence ID | Damage Evidence Claim ID | linkage | Unique identifier for one claim at one observation time and spatial resolution. | Constructed from source report, place code, asset or event type, and sequence number. | yes |
| Event ID | Persistent Damage Event ID | longitudinal linkage | Identifier joining multiple reports or evidence claims about the same event. | Remains stable when a later claim updates an earlier claim. | yes |
| Observation Time | Damage Evidence Observation Time | time index | Time associated with the evidence claim. | Parsed as a timezone-aware timestamp; it refers to report availability unless a more precise acquisition time is documented. | yes |
| Municipality | Damage Evidence Municipality | spatial linkage | Municipality in which the reported event occurred. | Retained from the source; it does not imply a precise point. | yes |
| Place Description | Reported Place or Asset Description | reference | Source-supported description of the damaged place or asset. | Transcribed conservatively without adding an unreported facility identity. | yes |
| Latitude | Damage Evidence Latitude | spatial linkage | North-south coordinate of the evidence location in decimal degrees. | Missing until a source supports geolocation. | yes |
| Longitude | Damage Evidence Longitude | spatial linkage | East-west coordinate of the evidence location in decimal degrees. | Missing until a source supports geolocation. | yes |
| Coordinate Precision | Damage Evidence Coordinate Precision | uncertainty | Spatial precision of the evidence location. | Coded as exact, approximate, municipality only, or unknown. | yes |
| Coordinate Uncertainty m | Estimated Coordinate Uncertainty | uncertainty | Approximate radial uncertainty of a geolocated point in metres. | Missing for municipality-only claims; it is not calculated from a municipality centroid. | yes |
| Asset Type | Damaged Asset Category | stratification | Functional category of the reported asset. | Coded as residential, commercial, industrial, infrastructure, or other supported category. | yes |
| Observed Damage Type | Source-Observed Damage Mechanism | damage evidence | Reported physical damage, such as buckling, floor collapse, debris, or access obstruction. | Retains the source-supported mechanism without converting it directly to a dwelling-loss count. | yes |
| Structural Damage Class | Evidence-Based Structural Damage Class | observed outcome | Structural severity supported by the current evidence. | Coded as confirmed collapse, confirmed severe damage, probable severe damage, observed non-collapse damage, or not assessable. | yes |
| Functional Housing Loss Status | Functional Loss of Heat-Protective Housing | main outcome | Whether the evidence supports loss of safe, accessible, cooling-capable residential shelter. | Coded as confirmed loss, probable loss, uncertain, no supported loss, or not applicable for nonresidential assets. | yes |
| Habitability Status | Evidence-Based Habitability Status | intermediate outcome | Whether a residence can safely be occupied based on available evidence. | Coded separately from structural damage and remains pending until inspection where necessary. | yes |
| Heat Protection Loss Mechanism | Mechanism of Lost Household Heat Protection | mechanism | Pathway through which a residence may cease to protect occupants from heat. | Structural unsafety, evacuation, power outage, water outage, access obstruction, or unknown; multiple claims may later be linked to one event. | yes |
| Reported Affected Asset Count | Number of Assets Represented by the Claim | aggregation weight | Count of assets explicitly represented by one evidence claim. | May exceed one for an aggregate incident; it must not be treated as one row per building. | yes |
| Evidence Tier | Damage Evidence Strength Tier | uncertainty | Ordered category reflecting source authority, geolocation, and directness. | Tier A is an official inspected or clearly geolocated claim; Tier B is an official approximate incident; lower tiers may hold geolocated ground imagery or supporting aerial signals. | yes |
| Verification Status | Damage Evidence Verification Status | quality control | Current verification state of the claim. | Distinguishes official reported, geolocated, manually reviewed, image supported, contradicted, and pending states. | yes |
| Supersedes Evidence ID | Prior Damage Evidence Claim ID | longitudinal linkage | Earlier claim updated by the current evidence record. | Missing for the first claim; later records link backward without deleting history. | yes |

### Service Disruption Snapshot Variables

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Disruption Snapshot ID | Service or Occupancy Disruption Snapshot ID | linkage | Unique identifier for one type of disruption at one observation time and geography. | Constructed from source report, geography, and disruption type. | yes |
| Disruption Type | Service or Occupancy Disruption Type | mechanism | Type of disruption that may reduce access to heat protection. | Includes evacuation instruction, power outage, water outage, road isolation, shelter closure, or another explicitly observed disruption. | yes |
| Service Status | Disruption Operational Status | time-varying state | Current state of the reported disruption. | Coded as in effect, resolved, partially restored, or unknown. | yes |
| Reported Affected Households | Official Disruption-Coverage Households | exposure scope | Households covered by the official disruption or instruction. | Nullable integer; interpretation follows Disruption Type and does not imply observed displacement. | yes |
| Reported Affected People | Official Disruption-Coverage Population | exposure scope | People covered by the official disruption or instruction. | Nullable integer; an evacuation-instruction count is a policy-coverage denominator. | yes |
| Observed Evacuee Count | Observed Number of Evacuees | observed outcome | People documented as having evacuated or entered shelters. | Remains missing when only an instruction-coverage count is available. | yes |
| Observed Power Outage Customers | Observed Electricity Outage Customers | mechanism | Customer connections reported without electricity. | Retained separately from population and household counts. | yes |
| Observed Water Outage Households | Observed Water-Service Outage Households | mechanism | Households reported without water service. | Nullable integer with observation time and source. | yes |
| Cooling Loss Confirmed | Confirmed Loss of Effective Cooling | main explanatory | Indicator that available evidence confirms loss of usable cooling. | False for evacuation instruction alone; it becomes true only with direct facility, household, or service evidence. | yes |
| Evidence Tier | Service Disruption Evidence Strength Tier | uncertainty | Strength and spatial specificity of the disruption claim. | Official aggregate and verified facility-level observations remain distinguishable. | yes |

### Grid Exposure Estimate Variables

The grid table uses the finest official population disclosure geography. A disclosure group can contain one mesh or multiple officially linked meshes. Population totals are never duplicated across member cells.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Disclosure Group Code | Official Population Disclosure Group ID | linkage | Identifier for the finest geography at which all selected population variables are disclosed. | Retained from the population preprocessing workflow. | yes |
| Functional Housing Loss Status | Grid Functional Housing-Loss Estimation Status | main outcome status | Whether functional housing loss has been estimated for the grid. | Initially not yet estimated; updated only when damage evidence can be spatially linked. | yes |
| Expected Functionally Lost Buildings | Expected Number of Functionally Lost Buildings | main outcome | Sum of calibrated building-level functional-loss probabilities in the grid. | (E[D_g]=\sum_{i\in g}p_i); remains missing until probabilities are estimated. | yes |
| Confirmed Functionally Lost Buildings | Confirmed Functionally Lost Buildings in Grid | lower-bound outcome | Count of buildings with sufficiently strong confirmed functional-loss evidence. | Reported separately from expected loss and remains missing until confirmed evidence is geolocated. | yes |
| Estimated Affected Population | Expected Population Associated with Functional Housing Loss | exposure outcome | Population expected to occupy functionally lost housing under an explicit allocation model. | Not calculated by multiplying the whole grid population by an unlocalized prefecture damage share. | yes |
| Estimated Affected Population Age 65+ | Expected Affected Population Age 65 or Older | primary exposure outcome | Expected number of residents age 65 or older associated with functional housing loss. | Estimated only after housing loss is localized and an allocation rule is specified. | yes |
| Estimated Affected Population Age 75+ | Expected Affected Population Age 75 or Older | exposure outcome | Expected number of residents age 75 or older associated with functional housing loss. | Uses the same uncertainty-aware allocation as the age-65-or-older measure. | yes |
| Estimated Affected Population Age 85+ | Expected Affected Population Age 85 or Older | exposure outcome | Expected number of residents age 85 or older associated with functional housing loss. | Uses the same uncertainty-aware allocation as the age-65-or-older measure. | yes |
| Heat Exposure Status | Grid Heat-Exposure Input Status | quality control | Whether event-window heat exposure has been constructed for the grid. | Initially pending heat input; satellite surface temperature alone cannot finalize this status. | yes |
| Estimation Status | Grid Exposure Estimation Status | quality control | Readiness of the grid for affected-population estimation. | Initially pending damage localization; later states must identify the completed evidence and model stage. | yes |
| Damage Evidence Cutoff | Latest Damage Evidence Time Used | time index | Most recent evidence time included in the grid estimate. | Stored as a timezone-aware timestamp and updated when the grid estimates are rerun. | yes |

### Designated Shelter Variables

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Common ID | GSI Common Facility ID | linkage | Stable facility identifier within the official shelter snapshot. | Retained as trimmed text and used for joins, verification tracking, and deduplication. | yes |
| Facility Name | Designated Shelter Facility Name | reference | Official name of the designated shelter facility or place. | Retained as trimmed text; it does not establish current opening or cooling availability. | yes |
| Address | Facility Address | spatial linkage | Official street address associated with the designated shelter. | Retained as trimmed text for administrative cross-checks and facility verification. | yes |
| Municipal Conditions | Other Conditions Required by the Municipal Mayor | eligibility constraint | Municipality-specific conditions attached to shelter use. | Retained as text; missing values remain unknown and are not coded as no restriction. | yes |
| Accepted Persons | Persons Eligible for Admission | vulnerability linkage | Officially stated category of persons eligible for admission where provided. | Retained as text for identifying facilities intended for people requiring special consideration; missing values remain unknown. | yes |
| Latitude | Facility Latitude | spatial linkage | North-south coordinate of the designated shelter in decimal degrees. | Converted to numeric and validated as non-missing within the Kumamoto Prefecture extent. | yes |
| Longitude | Facility Longitude | spatial linkage | East-west coordinate of the designated shelter in decimal degrees. | Converted to numeric and validated as non-missing within the Kumamoto Prefecture extent. | yes |
| Notes | Official Facility Notes | eligibility constraint | Additional official remarks associated with the designated shelter. | Retained as text; notes may qualify vehicle use, admission, or other facility conditions but do not verify post-event operation. | yes |

### Population and Vulnerable-Household Variables

The three overall totals are retained at the populated 125 m mesh. Age and vulnerable-household variables are represented at the finest geography permitted by the official disclosure system. A disclosure group is either one unsuppressed mesh or an aggregation-destination mesh dissolved together with every suppressed source mesh assigned to it. Suppressed values are treated as missing and are never set to zero or imputed.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Total Population | Total Population | control | Number of usual residents. | Exact at 125 m; summed across member meshes for each disclosure group. | yes |
| Population Age 65+ | Population Age 65 or Older | main explanatory | Number of residents age 65 or older. | Official count at the disclosure-group geography. | yes |
| Population Age 75+ | Population Age 75 or Older | main explanatory | Number of residents age 75 or older. | Official count at the disclosure-group geography. | yes |
| Population Age 85+ | Population Age 85 or Older | main explanatory | Number of residents age 85 or older. | Official count at the disclosure-group geography. | yes |
| Total Households | Total Households | control | Number of all households. | Exact at 125 m; summed across member meshes for each disclosure group. | yes |
| General Households | General Households | control | Number of general households. | Exact at 125 m; summed across member meshes for each disclosure group. | yes |
| One-Person Households | One-Person General Households | main explanatory | Number of general households containing one person. | Official count at the disclosure-group geography. | yes |
| Households with Member Age 65+ | General Households with a Member Age 65 or Older | main explanatory | Number of general households containing at least one member age 65 or older. | Official count at the disclosure-group geography. | yes |
| Older Single-Person Households | Older Single-Person General Households | main explanatory | Number of older single-person general households under the census definition. | Official count at the disclosure-group geography. | yes |
| Older Couple Households | Older Couple General Households | main explanatory | Number of older-couple general households under the census definition. | Official count at the disclosure-group geography. | yes |
| Population Age 65+ Share | Share of Population Age 65 or Older | main explanatory | \(s_{65+} = N_{65+} / N\). | Computed within each disclosure group; bounded from 0 to 1. | yes |
| Population Age 75+ Share | Share of Population Age 75 or Older | main explanatory | \(s_{75+} = N_{75+} / N\). | Computed within each disclosure group; bounded from 0 to 1. | yes |
| Population Age 85+ Share | Share of Population Age 85 or Older | main explanatory | \(s_{85+} = N_{85+} / N\). | Computed within each disclosure group; bounded from 0 to 1. | yes |
| Older Single-Person Household Share | Share of General Households That Are Older Single-Person Households | main explanatory | \(s_{single} = H_{older,single} / H_{general}\). | Computed within each disclosure group; missing when General Households is zero. | yes |
| Older Couple Household Share | Share of General Households That Are Older Couple Households | main explanatory | \(s_{couple} = H_{older,couple} / H_{general}\). | Computed within each disclosure group; missing when General Households is zero. | yes |

### Mapped Building Variables

The building layer is a pre-event spatial denominator derived from GSI vector tiles. Only polygonal building features are retained. Buffered-tile duplicates are removed by assigning each polygon to the nominal tile containing its representative point, exact geometry duplicates are removed by stable hash, and the representative point must fall inside Kumamoto Prefecture. These variables describe mapped building stock; they are not destroyed-building labels, dwelling counts, or occupancy observations.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Building ID | Stable Mapped-Building Geometry ID | linkage | Stable identifier for one unique mapped building polygon. | BLAKE2b hash of normalized polygon geometry after tile-ownership, prefecture-boundary, and exact-duplicate filtering. | yes |
| Building Area m2 | Mapped Building Footprint Area | exposure denominator | Planar area of one mapped building footprint in square metres. | Calculated from polygon geometry in JGD2011 / Japan Plane Rectangular CS II (EPSG:6670). | yes |
| Crosses Nominal Tile Boundary | Building Polygon Crosses Source Tile Boundary | quality control | Indicator that a retained polygon extends beyond the bounds of its owner tile. | One when polygon bounds cross any nominal source-tile edge; it does not mean that the geometry is incomplete. | yes |
| Mapped Building Count | Number of Mapped Building Polygons | exposure denominator | Count of unique building representative points within a populated 125 m cell or disclosure group. | Counted by representative-point spatial join and summed across disclosure-group member cells. It is not a count of damaged buildings. | yes |
| Mapped Building Footprint Area m2 | Total Mapped Building Footprint Area | exposure denominator | Sum of mapped building footprint area within a populated 125 m cell or disclosure group. | Aggregated using the same representative-point assignment as Mapped Building Count. | yes |

### Shelter and Support-Facility Accessibility Variables

Facility distances are straight-line distances from the centre of each populated 125 m cell, calculated in EPSG:6670. Disclosure-group distance is the minimum member-cell distance. Facility presence does not establish post-earthquake operation, road access, available beds, shelter opening, cooling equipment, or cooling capacity.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Support Facility ID | Stable Support-Facility Point ID | linkage | Stable identifier for a standardized MLIT support-facility point. | Hash of source type, facility name, address, and rounded coordinates. | yes |
| Support Facility Type | Support-Facility Category | stratification | One of Medical Institution, Welfare Facility, Public Office or Hall, or School. | Assigned from the official MLIT source dataset; the source reference year is retained separately. | yes |
| Nearest Designated Shelter Distance m | Straight-Line Distance to Nearest Designated Shelter | accessibility | Euclidean distance from the mesh centre to the nearest designated shelter point. | Calculated in metres; disclosure-group value is the minimum among member meshes. | yes |
| Nearest Earthquake-Compatible Emergency Site Distance m | Straight-Line Distance to Nearest Earthquake-Compatible Emergency Evacuation Site | accessibility | Euclidean distance to the nearest emergency site officially coded for earthquake use. | Emergency-site records are filtered to Earthquake = 1 before nearest-neighbour calculation. | yes |
| Nearest Medical Institution Distance m | Straight-Line Distance to Nearest Medical Institution | accessibility | Euclidean distance to the nearest MLIT medical-institution point. | Uses the 2020 reference layer and does not verify current operation. | yes |
| Nearest Welfare Facility Distance m | Straight-Line Distance to Nearest Welfare Facility | accessibility | Euclidean distance to the nearest MLIT welfare-facility point. | Uses the 2023 reference layer and does not verify current operation or admission capacity. | yes |
| Nearest Public Office or Hall Distance m | Straight-Line Distance to Nearest Public Office or Public Hall | accessibility | Euclidean distance to the nearest MLIT public-office or public-hall point. | Uses the 2022 reference layer; presence does not imply shelter designation or cooling availability. | yes |
| Nearest School Distance m | Straight-Line Distance to Nearest School | accessibility | Euclidean distance to the nearest MLIT school point. | Uses the 2023 reference layer; presence does not imply shelter designation or cooling availability. | yes |

### Station Heat and Historical Scenario Variables

Event-window heat is constructed from quality-checked ten-minute observations at five
stations. The line-figure historical scenario uses matching calendar dates from 2021-2025
at Kumamoto and Yatsushiro, while the prefecture-wide spatial baseline uses the same dates
at 17 temperature-reporting stations. Missing observations remain missing; no temperature
or humidity values are imputed or clipped. Station air temperature is not interpreted as
indoor temperature or, before the spatial model is evaluated, as a complete prefecture-wide
heat surface.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Station Name | JMA AMeDAS Station Name | stratification | Official English name of the observation station. | Retained from the station metadata snapshot. | yes |
| Observation Date | JMA Observation Date | time index | Local calendar date of the event-window observation in Japan Standard Time. | Ten-minute timestamps are parsed in Asia/Tokyo and aggregated by calendar day. | yes |
| Historical Year | Historical Heat Scenario Year | scenario index | Source year for one matched historical daily observation. | Restricted to 2021-2025. | yes |
| Scenario Date | Matched 2026 Heat Scenario Calendar Date | scenario time index | Calendar date obtained by anchoring a historical month and day to the 2026 event window. | Restricted to 2026-07-28 through 2026-08-26. | yes |
| Event Day | Days Since the 2026 Kumamoto Earthquake | time index | Number of local calendar days since 2026-07-28. | The earthquake date is day 0; the historical scenario covers days 0-29. | yes |
| Daily Maximum Air Temperature C | Daily Maximum Near-Surface Air Temperature in Degrees Celsius | main explanatory | Maximum station air temperature observed during the local calendar day. | Calculated from quality-checked ten-minute event observations or retained from the official historical daily table. | yes |
| Daily Minimum Air Temperature C | Daily Minimum Near-Surface Air Temperature in Degrees Celsius | main explanatory | Minimum station air temperature observed during the local calendar day. | Calculated from quality-checked ten-minute event observations or retained from the official historical daily table. | yes |
| Daily Mean Relative Humidity % | Daily Mean Relative Humidity Percentage | main explanatory | Arithmetic mean of available relative-humidity observations during the local calendar day. | Calculated from quality-checked ten-minute event observations or retained when reported in the official historical daily table; missing values are not imputed. | yes |
| Hot Day Indicator | Daily Maximum Air Temperature at Least 35 C | heat threshold | Indicator that daily maximum air temperature is at least 35 C. | A partial event day above the threshold can be confirmed true; a partial day below the threshold remains missing. | yes |
| Hot Night Indicator | Daily Minimum Air Temperature at Least 25 C | heat threshold | Indicator that daily minimum air temperature is at least 25 C. | Evaluated only for a complete event day or a reported historical day; incomplete event days remain missing. | yes |
| Daily Observation Completeness % | Share of Expected Ten-Minute Temperature Observations Available | quality control | Percentage of the expected 144 ten-minute temperature records available for a station-day. | Observation count divided by 144 and multiplied by 100; capped at 100. | yes |
| Daily Record Status | Daily Station Heat Record Completeness Status | quality control | Whether the event station-day contains all expected ten-minute temperature observations. | Coded as complete for 144 observations and partial otherwise. | yes |
| Temperature Record Complete | Historical Daily Temperature-Record Completeness Indicator | quality control | Whether mean, maximum, and minimum air temperature are all reported for one historical station-day. | True only when all three official temperature fields are non-missing; 2,546 of 2,550 spatial-baseline station-days are complete. | yes |

### Historical MODIS Spatial Heat Variables

The satellite grid summarizes matching calendar periods from 2021-2025 using Terra and Aqua
eight-day land-surface-temperature products at approximately 1 km resolution. Only pixels
with mandatory quality assurance marked good, data quality marked good, and reported land-
surface-temperature error no greater than 1 K are retained. Terra and Aqua product means
receive equal weight. Cloud-affected and lower-quality values remain missing; no spatial or
temporal gap filling is used. Land-surface temperature is a spatial covariate and is not
interpreted as near-surface air temperature, indoor temperature, or a forecast.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| MODIS Pixel ID | Stable MODIS Sinusoidal Grid-Cell ID | linkage | Identifier combining source tile, row, and column for one approximately 1 km satellite cell. | Retained for each pixel whose centre lies inside Kumamoto Prefecture. | yes |
| Historical Daytime Land Surface Temperature C | Strict-Quality Historical Daytime Land Surface Temperature in Degrees Celsius | spatial heat covariate | Mean daytime satellite land-surface temperature for the matched July 28-August 26 periods in 2021-2025. | Calculated separately within Terra and Aqua from valid eight-day composites, then averaged across available product means with equal product weight. | yes |
| Historical Nighttime Land Surface Temperature C | Strict-Quality Historical Nighttime Land Surface Temperature in Degrees Celsius | spatial heat covariate | Mean nighttime satellite land-surface temperature for the matched July 28-August 26 periods in 2021-2025. | Uses the same strict quality rule and equal-product construction as the daytime measure. | yes |
| MODIS Valid Observation Count | Number of Strict-Quality MODIS Land-Surface-Temperature Observations | quality control | Number of valid Terra and Aqua eight-day observations contributing to the relevant daytime or nighttime pixel estimate. | Stored separately for daytime and nighttime; a zero count remains missing in the corresponding temperature field. | yes |
| Historical Land Surface Temperature SD C | Historical Within-Pixel Land-Surface-Temperature Standard Deviation in Degrees Celsius | sensitivity | Sample standard deviation of all strict-quality Terra and Aqua observations for the relevant daytime or nighttime pixel. | Stored separately for daytime and nighttime and used to identify temporally unstable satellite estimates. | yes |
| Station-Calibrated Historical Air Temperature C | Station-Calibrated Historical Near-Surface Air Temperature in Degrees Celsius | modeled heat outcome | Historical maximum air temperature for the daytime model or minimum air temperature for the nighttime model predicted at a MODIS pixel. | Estimated from the 17-station historical baseline using the matched daytime or nighttime satellite covariate and a cross-validated spatial residual model; produced only when out-of-station validation supports the model. | yes |
| Spatial Heat Anomaly C | Station-Calibrated Spatial Heat Anomaly in Degrees Celsius | heterogeneity outcome | Difference between a pixel's station-calibrated historical air temperature and the prefecture-wide population-relevant reference temperature for the same period. | Calculated separately for daytime and nighttime after calibration; positive values indicate a historically warmer location, not an event forecast. | yes |
| Interpolation Uncertainty C | Out-of-Station Spatial Prediction Uncertainty in Degrees Celsius | uncertainty | Estimated prediction uncertainty for the station-calibrated air-temperature surface. | Derived from leave-one-station-out prediction errors and local distance or support of the residual spatial model; reported separately for daytime and nighttime. | yes |

## 5. Identification Strategy

### Design Principle

The current phase uses descriptive evidence triangulation rather than causal identification.
Official observations are preserved at their reported time and geography, then linked only
when coordinates or explicit place descriptions permit. The screening combines three
independent dimensions: the spatial baseline of Population Age 65+, the reported
Tomiai/Jonan housing-damage concentration, and direct evidence of shelter, water, power, or
cooling disruption. Agreement across dimensions raises operational priority but does not
convert a location into a confirmed housing-loss or heat-injury case.

### Screening Specification

- Population Age 65+ is mapped at its official disclosure-group geography without assigning
  residents to damaged buildings.
- Facility Name, Latitude, and Longitude locate designated shelters. Designation alone is
  not interpreted as current operation or available cooling.
- Cooling Loss Confirmed and Heat Protection Loss Mechanism identify direct evidence of
  lost cooling protection. Evidence Tier and Verification Status remain visible in the
  supporting table.
- Observed Evacuee Count and Observed Water Outage Households are plotted as separate
  time-stamped series. They are not added, multiplied, or interpreted as the same population.
- Reported housing-damage concentrations are contextual areas, while point symbols are
  reserved for facilities with explicit coordinates.

This strategy directly produces Minami Ward Shelter and Cooling Risk Screening in Section 8.
The time-stamped evidence ledger remains an internal analytical input rather than a result.
The current phase cannot identify a causal effect of earthquake exposure on heat outcomes,
estimate indoor temperature, infer that all older residents in a highlighted area were
displaced, or calculate the shelter cooling-capacity gap defined in Section 1.

### Station Heat Scenario Design

The heat component is a descriptive event-window comparison. Daily Maximum Air Temperature
C and Daily Minimum Air Temperature C from five event-period stations are compared with the
same calendar dates observed at Kumamoto and Yatsushiro in 2021-2025. The historical
distribution supplies a calendar-matched scenario envelope; it is not a meteorological
forecast, confidence interval, or counterfactual estimate of temperatures without the
earthquake.

Daytime and nighttime heat are analyzed separately because a high daily maximum and a warm
overnight minimum represent different recovery conditions. Hot Day Indicator uses the
pre-specified threshold of 35 C and Hot Night Indicator uses 25 C. Daily Record Status is
retained visually: partial-day observations may confirm that the daytime threshold has
already been crossed, but cannot establish a below-threshold day or classify a hot night.
Station observations are not spatially interpolated to population grids in this phase.

### Historical Spatial Heat Design

The spatial component estimates historical heat heterogeneity, not event-period weather.
Historical Daytime Land Surface Temperature C is paired with the 2021-2025 station mean of
Daily Maximum Air Temperature C, and Historical Nighttime Land Surface Temperature C is
paired with the station mean of Daily Minimum Air Temperature C. Temperature Record
Complete restricts the station target to complete historical days. MODIS Valid Observation
Count determines pixel eligibility before calibration.

The calibration is evaluated out of station. A prefecture-wide mean-only model, a satellite-
only linear calibration, and a satellite calibration with inverse-distance residual
interpolation are compared by leave-one-station-out prediction. The model with the lowest
cross-validated root-mean-square error is retained separately for daytime and nighttime. If
neither satellite-based candidate improves on the mean-only model, Station-Calibrated
Historical Air Temperature C is not interpreted as a supported spatial air-temperature
surface; the figure is restricted to land-surface-temperature patterns and the failed
validation result. This design is descriptive and cannot establish earthquake effects,
indoor temperature, individual heat dose, or a future forecast.

## 6. Main Estimation Framework

### Primary Framework: Evidence-Constrained Operational Screening

The map is a layered descriptive screen. For a mapped area \(A\), the older-population
baseline is summarized as

\[
N_{65+,A} = \sum_{g \in A} N_{65+,g}.
\]

\(N_{65+,A}\) is the number of residents age 65 or older in area \(A\), \(g\) indexes an
official population disclosure group intersecting that area, and \(N_{65+,g}\) is Population
Age 65+ in group \(g\). This total is a residential baseline, not an estimate of affected or
displaced older residents.

For each observed time \(t\), the operational panel retains

\[
Y_t \in \{E_t, W_t\}.
\]

\(Y_t\) denotes the displayed operational observation, \(E_t\) is Observed Evacuee Count,
and \(W_t\) is Observed Water Outage Households. The two series use separate axes and are
never combined into a composite outcome.

A facility receives a confirmed cooling-interruption marker only when Cooling Loss
Confirmed is true and its location is supported by Latitude and Longitude. This is a
classification rule, not a fitted probability model. Facilities without a confirmed marker
remain unknown with respect to post-earthquake cooling unless direct operational evidence
states otherwise.

### Secondary Framework: Calendar-Matched Heat Scenario

Let \(Z^{k}_{syd}\) denote the observed daily station temperature for outcome
\(k \in \{\max,\min\}\), station \(s\), historical year
\(y \in \{2021,\ldots,2025\}\), and event day \(d \in \{0,\ldots,29\}\).
For each outcome and event day, the historical center is

\[
M^{k}_{d} = \operatorname{median}_{s,y}\left(Z^{k}_{syd}\right),
\]

and the descriptive historical envelope is

\[
B^{k}_{d} = \left[
\min_{s,y}\left(Z^{k}_{syd}\right),
\max_{s,y}\left(Z^{k}_{syd}\right)
\right].
\]

The envelope contains the ten calendar-matched station-year observations available for
each event day: two stations across five historical years. It describes observed historical
range and is not an uncertainty interval. Current 2026 values \(O^{k}_{sd}\) from the five
event stations are overlaid through the latest available observation date. Hot-day and
hot-night classifications are

\[
H^{\max}_{sd}=\mathbb{1}\left(O^{\max}_{sd}\geq 35\right),
\qquad
H^{\min}_{sd}=\mathbb{1}\left(O^{\min}_{sd}\geq 25\right).
\]

For a partial station-day, \(H^{\max}_{sd}=1\) is allowed once 35 C has been observed;
otherwise it remains missing. \(H^{\min}_{sd}\) remains missing until the station-day is
complete. This prevents incomplete observations from being treated as safe days or nights.

### Tertiary Framework: Cross-Validated Spatial Heat Calibration

For heat period \(k \in \{day,night\}\), define the station climatological target as

\[
\bar{T}^{k}_{s} = \frac{1}{n_s}\sum_{j=1}^{n_s} T^{k}_{sj}.
\]

\(\bar{T}^{k}_{s}\) is the mean historical station air temperature at station \(s\),
\(T^{day}_{sj}\) is Daily Maximum Air Temperature C on complete historical station-day
\(j\), \(T^{night}_{sj}\) is Daily Minimum Air Temperature C, and \(n_s\) is the number of
complete historical station-days at station \(s\).

The satellite-only calibration is

\[
\bar{T}^{k}_{s} = \beta^{k}_{0} + \beta^{k}_{1} L^{k}_{s} + r^{k}_{s}.
\]

\(\beta^{k}_{0}\) is the period-specific intercept, \(\beta^{k}_{1}\) is the period-specific
satellite calibration coefficient, \(L^{k}_{s}\) is Historical Daytime Land Surface
Temperature C or Historical Nighttime Land Surface Temperature C sampled at station \(s\),
and \(r^{k}_{s}\) is the station residual.

For candidate inverse-distance power \(p\) and neighbor count \(q\), the spatial residual at
pixel \(g\) is

\[
\hat{r}^{k}_{g}(p,q) =
\frac{\sum_{s \in N_q(g)}(d_{gs}+\delta)^{-p}r^{k}_{s}}
{\sum_{s \in N_q(g)}(d_{gs}+\delta)^{-p}}.
\]

\(N_q(g)\) is the set of the \(q\) nearest eligible stations to pixel \(g\), \(d_{gs}\) is
their projected distance, and \(\delta\) is a small fixed distance constant that prevents
division by zero. Candidate values of \(p\) and \(q\) are selected only through leave-one-
station-out prediction. The combined prediction is

\[
\hat{T}^{k}_{g} = \hat{\beta}^{k}_{0} + \hat{\beta}^{k}_{1}L^{k}_{g}
+ \hat{r}^{k}_{g}.
\]

\(\hat{T}^{k}_{g}\) is Station-Calibrated Historical Air Temperature C at pixel \(g\),
\(L^{k}_{g}\) is the corresponding historical land-surface temperature, and the hatted
terms are fitted values from the selected candidate. The mean-only, satellite-only, and
combined candidates are compared using

\[
RMSE^{k}_{LOO} =
\sqrt{\frac{1}{S}\sum_{s=1}^{S}
\left(\bar{T}^{k}_{s}-\hat{T}^{k}_{s,-s}\right)^2}.
\]

\(RMSE^{k}_{LOO}\) is the leave-one-station-out root-mean-square error, \(S\) is the number
of eligible stations, and \(\hat{T}^{k}_{s,-s}\) is the prediction for station \(s\) from a
model fitted without that station. Mean absolute error and mean signed error are reported as
supporting diagnostics, but model selection uses \(RMSE^{k}_{LOO}\).

For a supported surface, the population-referenced spatial anomaly is

\[
A^{k}_{g} = \hat{T}^{k}_{g} -
\frac{\sum_g P_g\hat{T}^{k}_{g}}{\sum_g P_g}.
\]

\(A^{k}_{g}\) is Spatial Heat Anomaly C and \(P_g\) is Total Population assigned to pixel
\(g\) from the populated small-area grid. This centers the map on where residents live
rather than on unpopulated mountain area. Prediction uncertainty is

\[
U^{k}_{g} = \sqrt{\left(RMSE^{k}_{LOO}\right)^2
+ \operatorname{SD}_{s}\left(\hat{T}^{k}_{g,-s}\right)^2}.
\]

\(U^{k}_{g}\) is Interpolation Uncertainty C and
\(\operatorname{SD}_{s}(\hat{T}^{k}_{g,-s})\) is the pixel-level standard deviation among
the leave-one-station-out fitted surfaces. It combines observed out-of-station error with
sensitivity to omission of any one station; it is not a probabilistic confidence interval.

### Sensitivity and Failure-Mode Plan

- Population disclosure groups that cross the Minami Ward boundary are clipped only for
  display; their official counts are not area-weighted into new population estimates.
- The figure distinguishes designated shelters from facilities with confirmed cooling or
  water failure so that nominal availability is not mistaken for operational availability.
- Official observations at different times are retained separately to reveal changing
  occupancy and outage conditions.
- Missing cooling, power, water, or housing fields remain unknown rather than zero.
- The Tomiai/Jonan concentration is shown as an officially reported contextual zone, not a
  count or probability surface.
- The historical heat band uses the observed minimum and maximum rather than a model-based
  interval because only ten station-year observations are available per event day.
- Event-period station values are shown individually, and partial station-days are marked
  separately rather than completed through imputation.
- The heat scenario does not estimate indoor temperature, heat illness, mortality, or a
  prefecture-wide temperature surface.
- The spatial heat model uses only strict-quality satellite observations. A pixel is eligible
  for primary calibration only when both Terra and Aqua contribute and at least five valid
  observations are available for the relevant daytime or nighttime period.
- Relaxed satellite quality criteria are reserved for a sensitivity comparison and never
  overwrite the strict-quality primary surface.
- Mean-only, satellite-only, and satellite-plus-residual candidates are compared by leave-
  one-station-out error; residual interpolation is not retained merely because it appears
  spatially smoother.
- Pixels outside the land-surface-temperature range represented by eligible stations are
  flagged as extrapolation and are not used for precise local temperature claims.
- Historical Land Surface Temperature SD C and MODIS Valid Observation Count remain visible
  as support diagnostics so that cloud-limited or temporally unstable pixels are not treated
  as equally reliable.
- Spatial Heat Anomaly C describes a 2021-2025 matching-season pattern. It is not a forecast
  for the next month and does not substitute for event-period station or forecast data.
- Results remain inconclusive for the full deficit \(Gap_s(t)\) until effective cooled
  capacity and expected older-person demand are observed or estimated.

## 7. Analytical Workflow

| step | variables used | formula/model used | generated figure/table title | theory or claim evaluated | support status |
|---|---|---|---|---|---|
| 1. Define the Minami Ward screening frame and older-population baseline | Population Age 65+, Latitude, Longitude | \(N_{65+,A} = \sum_{g \in A} N_{65+,g}\), used only as a residential baseline | Minami Ward Shelter and Cooling Risk Screening | Older residents are spatially heterogeneous within the affected ward | Descriptively supported; affected status remains unknown |
| 2. Overlay nominal shelter access and confirmed facility interruption | Facility Name, Latitude, Longitude, Cooling Loss Confirmed, Heat Protection Loss Mechanism | Evidence-constrained facility classification rule | Minami Ward Shelter and Cooling Risk Screening | Shelter designation does not guarantee usable cooling after the earthquake | Partially supported by confirmed facility failures; unreported facilities remain unknown |
| 3. Add reported damage-concentration context | Geographic Level, Municipality, Evidence Tier, Verification Status | Contextual overlay without building-level allocation | Minami Ward Shelter and Cooling Risk Screening | Tomiai and Jonan require prioritized verification because official pre-assessment reports concentrated housing damage | Supported only at the reported contextual geography |
| 4. Plot changing evacuation and water-outage observations | Observation Time, Observed Evacuee Count, Observed Water Outage Households | \(Y_t \in \{E_t, W_t\}\) | Minami Ward Shelter and Cooling Risk Screening | Cooling-protection conditions change over time and should not be represented by one static snapshot | Supported for the observed municipal and Jonan series |
| 5. Preserve the internal evidence ledger | Observation Time, Geographic Level, Municipality, Full Collapse Buildings, Half Collapse Buildings, Partial Damage Buildings, Observed Evacuee Count, Observed Power Outage Customers, Observed Water Outage Households, Heat Protection Loss Mechanism, Cooling Loss Confirmed, Evidence Tier, Verification Status | No cross-domain aggregation; one reported observation per row | Internal analytical input; excluded from results | Early decisions can use official observations while retaining uncertainty and spatial limits | Supported as documentation; not a standalone research result or affected-population estimate |
| 6. Construct the calendar-matched daytime heat scenario | Station Name, Historical Year, Scenario Date, Event Day, Daily Maximum Air Temperature C, Hot Day Indicator, Daily Record Status | Historical daily median and observed minimum-maximum envelope; overlay 2026 station values and the 35 C threshold | Event-Window Daytime and Nighttime Heat Scenario | Recovery-period daytime heat may reach levels requiring active cooling even while damage assessment remains incomplete | Descriptively supported for station locations; the historical envelope is not a forecast |
| 7. Construct the calendar-matched nighttime heat scenario | Station Name, Historical Year, Scenario Date, Event Day, Daily Minimum Air Temperature C, Hot Night Indicator, Daily Record Status | Historical daily median and observed minimum-maximum envelope; overlay 2026 station values and the 25 C threshold | Event-Window Daytime and Nighttime Heat Scenario | Warm nights may limit overnight physiological recovery and extend cooling needs beyond daytime hours | Descriptively supported for complete station-days; partial nights remain unclassified |
| 8. Construct the strict-quality historical satellite grid | MODIS Pixel ID, Historical Daytime Land Surface Temperature C, Historical Nighttime Land Surface Temperature C, MODIS Valid Observation Count, Historical Land Surface Temperature SD C | Strict quality screening, equal Terra-Aqua product weighting, and no gap filling | Historical MODIS and Station-Calibrated Heat Spatial Heterogeneity | Matching-season surface heat is spatially heterogeneous across Kumamoto Prefecture | Descriptively supported where both products and at least five strict-quality observations are available |
| 9. Calibrate satellite heat against historical station air temperature | Station Name, Temperature Record Complete, Daily Maximum Air Temperature C, Daily Minimum Air Temperature C, Historical Daytime Land Surface Temperature C, Historical Nighttime Land Surface Temperature C | Mean-only, linear satellite, and satellite-plus-residual candidates compared by \(RMSE^{k}_{LOO}\) | Historical MODIS and Station-Calibrated Heat Spatial Heterogeneity | Satellite surface temperature can provide spatial information about near-surface daytime and nighttime heat rankings | Supported only if a satellite-based candidate outperforms the mean-only model out of station; otherwise rejected |
| 10. Map population-referenced heat heterogeneity and prediction support | Station-Calibrated Historical Air Temperature C, Spatial Heat Anomaly C, Interpolation Uncertainty C, Total Population, MODIS Valid Observation Count | \(A^{k}_{g}\) and \(U^{k}_{g}\), with extrapolation and low-support pixels flagged | Historical MODIS and Station-Calibrated Heat Spatial Heterogeneity | Historically warmer populated locations may require stronger heat-protection planning after loss of housing function | Provides a historical vulnerability layer only; event risk still requires current observations or forecasts |
| 11. Test readiness for the central cooling-deficit question | Functional Housing Loss Status, Estimated Affected Population Age 65+, Heat Exposure Status, Observed Evacuee Count, Cooling Loss Confirmed | Compare required inputs with the deficit definition in Section 1 | Deferred outputs in Section 8 | Verified effective cooled capacity must be compared with expected heat-vulnerable demand | Inconclusive until capacity and localized housing-loss inputs are available; historical spatial heat does not establish current displaced demand |

The checkpoint for this phase remains partial. Minami Ward Shelter and Cooling Risk
Screening supports spatial priority screening, Event-Window Daytime and Nighttime Heat
Scenario tests the station-based 30-day heat component, and Historical MODIS and Station-
Calibrated Heat Spatial Heterogeneity can add a validated historical spatial pattern. The
historical spatial output does not establish event-period grid temperature and none of the
current outputs quantifies a shelter-level cooling deficit.

## 8. Figure and Table Plan

The planned output set links the existing population, early operational screening, and
station-heat figures to the next spatial-estimation stages. Existing figures are retained
as working outputs but return to pending while the critique findings are corrected. The
MODIS-based output is intended to characterize historical spatial heat heterogeneity; it is
not a weather forecast, indoor-temperature estimate, or substitute for station air
temperature.

### Figures

| title | what it expresses | figure type | subpanels | key variables | status |
|---|---|---|---:|---|---|
| Kumamoto Population and Older-Age Vulnerability Baseline | Establishes the prefecture-wide population baseline and spatial concentration of older residents before linking earthquake loss and heat exposure. | map | 2 | Total Population, Population Age 65+ Share, Population Age 65+, Municipality | pending |
| Minami Ward Shelter and Cooling Risk Screening | Locates older residents, designated shelters, the reported Tomiai/Jonan damage concentration, verified unavailable facilities, and changing evacuation and water-outage observations without estimating a numerical cooling-capacity deficit. | map and line | 2 | Population Age 65+, Latitude, Longitude, Facility Name, Observation Time, Observed Evacuee Count, Observed Water Outage Households, Cooling Loss Confirmed, Habitability Status, Heat Protection Loss Mechanism, Evidence Tier, Verification Status | pending |
| Event-Window Daytime and Nighttime Heat Scenario | Compares observed 2026 daytime and nighttime station temperatures with the matching 2021-2025 historical scenario while distinguishing complete and partial event days; the historical continuation is a scenario, not a weather forecast. | line | 2 | Station Name, Observation Date, Historical Year, Scenario Date, Event Day, Daily Maximum Air Temperature C, Daily Minimum Air Temperature C, Hot Day Indicator, Hot Night Indicator, Daily Observation Completeness %, Daily Record Status | pending |
| Historical MODIS and Station-Calibrated Heat Spatial Heterogeneity | Uses matching-period historical MODIS daytime and nighttime land-surface temperature together with historical station air temperature to estimate a station-calibrated spatial heat pattern for Kumamoto Prefecture. | map | 3 | Historical Daytime Land Surface Temperature C, Historical Nighttime Land Surface Temperature C, MODIS Valid Observation Count, Station-Calibrated Historical Air Temperature C, Spatial Heat Anomaly C, Interpolation Uncertainty C | pending |
| Functional Housing Loss and Older-Person Exposure | Separates the confirmed building-loss lower bound, expected functional housing loss, and estimated older population associated with localized housing loss. | map | 3 | Functional Housing Loss Status, Confirmed Functionally Lost Buildings, Expected Functionally Lost Buildings, Estimated Affected Population Age 65+, Estimation Status, Damage Evidence Cutoff | pending |

### Tables

| title | what it expresses | rows | columns | row meaning | column meaning | status |
|---|---|---:|---:|---|---|---|

No table is currently included in the research results. The time-stamped evidence ledger
is retained only as an internal analytical input.

### Deferred Outputs Required for the Full Research Objective

- A shelter-level effective cooled-capacity deficit table remains deferred until verified
  cooling equipment, backup power, usable cooled space, occupancy, and accessibility inputs
  are acquired and confirmed in Section 4.
- A building-loss calibration and validation output remains deferred until geolocated
  official inspection or damage-certificate labels become available.

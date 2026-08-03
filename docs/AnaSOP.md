# AnaSOP
Analysis Standard Operating Procedure

## 1. Research Objective

### Central Research Question

- Research question: During the first 30 days after the 2026 Kumamoto earthquake, where are older residents likely to lose effective protection from heat, and which shelters face a deficit in accessible cooling capacity under uncertainty about housing damage?
- Why it matters: Emergency decisions concern whether vulnerable residents can remain safe, not only whether a roof is visibly collapsed. A house may cease to provide heat protection because it is structurally unsafe, inaccessible, without power or water, or abandoned after nearby ground failure. Reframing the endpoint as loss of effective heat-protective shelter links early damage evidence directly to cooling allocation.
- Data support currently visible: Official residence-damage snapshots constrain a prefecture total; epicentral distance, mapped exposure, and processed small-area population data support a transparent grid allocation with explicit bounds. Event-period station observations and historical spatial heat describe the common outdoor hazard. Designated shelters and selected facility interruptions are mapped, but verified occupancy, usable cooled space, operating air-conditioning, backup power, and resident placement remain incomplete.
- Key readable variables or data scope: Expected functionally lost residences and scenario bounds; older residents and older households associated with housing loss; common outdoor heat conditions; current residence or placement status; effective cooled capacity; unprotected older-person cooling demand; required electric power; and cooling-loss-related incremental health risk.
- What would verify it: Later official residence inspections should be spatially concentrated in grids with larger expected loss; observed placement or displacement should rise with estimated loss of heat-protective housing; and locations classified as cooling deficits should show demand exceeding verified cooled capacity.
- What would falsify or weaken it: The residence-loss allocation fails against later inspections; most affected older residents retain functioning home cooling or relocate privately to cooled environments; or verified cooled capacity is sufficient for all people requiring protection throughout the event window.
- Required next feasibility check: Acquire time-stamped resident-placement, shelter occupancy, usable cooled-space, air-conditioning, backup-power, and indoor-temperature evidence; determine whether later official damage and displacement records can be spatially linked for validation.

### Supporting Research Questions

#### Supporting Point 1

- Role relative to central point: measurement
- Research question: How many residences are expected to lose safe function, where are they plausibly concentrated, and how sensitive is the allocation to distance decay, exposure proxy, and treatment of half-collapse residences?
- Why it matters: Early official totals are operationally useful but not geolocated. A transparent total-constrained scenario can support planning without claiming that mapped building polygons reveal individual residential damage.
- Data support currently visible: Official full- and half-collapse residence totals, an official epicenter, general-household counts, mapped building exposure, and populated disclosure groups support twenty-seven allocation scenarios.
- Key readable variables or data scope: Epicentral Distance km, General Households, Mapped Building Count, Mapped Building Footprint Area m2, Expected Functionally Lost Residences, pointwise scenario bounds, and confirmed evidence retained at its reported geography.
- What would verify it: Later geolocated inspections or damage certificates should concentrate in grids with larger expected loss, and municipality totals should show acceptable calibration and rank agreement.
- What would falsify or weaken it: Later inspections have little spatial agreement with the allocation, the official total changes materially, or the selected exposure proxies allocate loss to nonresidential or unoccupied areas.
- Required next feasibility check: Update official totals as assessments mature and acquire geolocated inspection labels for calibration and validation.

For grid \(g\), report the total-constrained scenario allocation \(L_{g,s}\), its ensemble central value, and its pointwise scenario range. Confirmed evidence remains separate and is never filled by the modeled allocation.

#### Supporting Point 2

- Role relative to central point: exposure heterogeneity
- Research question: How many residents, especially residents aged 65+, 75+, and 85+ and older people living alone, are expected to live in grids with functional housing loss?
- Why it matters: The affected population cannot be inferred by assigning all residents of a municipality or grid to the damaged category. Expected exposure should vary with the estimated share of housing rendered unsafe.
- Data support currently visible: Population and vulnerable-household counts are available at fine grid or official disclosure-group geography, with explicit suppression handling.
- Key readable variables or data scope: Total population, older-population counts and shares, older single-person and older-couple households, expected functionally lost dwellings, residential building stock, and grid-level exposure uncertainty.
- What would verify it: Estimated affected populations should be consistent with later displacement, shelter-registration, welfare-check, or damage-certificate counts after accounting for residents who relocate privately.
- What would falsify or weaken it: Population baselines are too outdated, disclosure aggregation prevents meaningful spatial linkage, or scenario-estimated housing loss has no measurable relationship with subsequent displacement or placement need.
- Required next feasibility check: Compare the completed disclosure-group scenario with later displacement, placement, welfare-check, and damage-certificate records; test alternative occupancy assumptions as those observations become available.

#### Supporting Point 3

- Role relative to central point: cooling-protection mechanism
- Research question: Under the same outdoor weather, how many affected older residents lose the effective indoor cooling previously supplied by a usable home, and for how many person-days would that protection remain unavailable without correct placement?
- Why it matters: The earthquake does not cause the outdoor temperature scenario. It changes whether an older resident can remain in a safe cooled indoor environment. Ambient heat therefore modifies the consequence of cooling loss but is not the treatment contrast.
- Data support currently visible: Event-window station observations and historical spatial heat describe the common outdoor hazard; modeled residence loss identifies an upper-bound population requiring cooling assessment. Direct indoor temperature, functioning household cooling, resident destination, and duration without effective cooling remain unavailable.
- Key readable variables or data scope: Estimated Affected Population Age 65+, Heat Protection Loss Mechanism, Cooling Loss Confirmed, Effective Cooled Capacity, Cooling Capacity Gap, outdoor air temperature, indoor temperature under cooled and uncooled states, and unprotected older-person-days.
- What would verify it: Time-stamped placement, household or shelter cooling status, and indoor-temperature measurements show that residents classified as protected occupy functioning cooled spaces while deficit locations experience longer or hotter indoor exposure.
- What would falsify or weaken it: Most affected older residents retain functioning home cooling, relocate promptly to private cooled environments, or measured indoor conditions do not differ meaningfully between classified protection states.
- Required next feasibility check: Collect resident-placement and cooling-status observations, verify effective cooled capacity, and obtain indoor-temperature evidence or a defensible building-thermal scenario before estimating a health effect.

#### Supporting Point 4

- Role relative to central point: policy decision
- Research question: Which placements, shelter capacities, and emergency power allocations can close the cooling-protection deficit, and how much one-month incremental mortality risk could be avoided under the same outdoor weather?
- Why it matters: Shelter location alone does not establish protection. Air-conditioning, backup electricity, usable cooled floor area, current occupancy, operating hours, transport access, and the needs of residents with limited mobility determine whether correct placement actually restores cooling protection.
- Data support currently visible: Public shelter locations can support an initial accessibility layer, but verified cooling equipment, power resilience, occupancy, and usable capacity are not yet present in the analytical data.
- Key readable variables or data scope: Expected older residents requiring cooling assessment, travel time or distance, shelter occupancy, accessible cooled spaces, air-conditioning status, backup power, outage duration, Effective Cooled Capacity, Cooling Capacity Gap, required peak electric power, required daily electricity, and cooling-loss-related incremental mortality risk.
- What would verify it: Facility checks and placement records confirm demand and functioning cooled capacity; follow-up health evidence is consistent with lower risk among residents who receive effective cooling after accounting for the common outdoor weather.
- What would falsify or weaken it: Most exposed residents remain in safe cooled housing, relocate outside public shelters, or shelters have larger functioning capacity than public records imply.
- Required next feasibility check: Obtain or rapidly survey shelter HVAC, backup-power, occupancy, accessibility, usable-capacity, and resident-placement attributes; define a transparent catchment-allocation rule and a defensible cooled-versus-uncooled health-risk contrast.

For shelter (s) and day (t), define a decision-facing deficit:

\[
Gap_s(t) = Demand_{65+,s}(t) - Capacity_{cool,s}(t).
\]

A positive value indicates that expected older-person demand exceeds verified effective cooled capacity. Both terms must be reported with uncertainty rather than as exact counts.

### Scope of Analysis

- Event: The 2026 Kumamoto earthquake beginning on 2026-07-28.
- Geographic frame: Kumamoto Prefecture for consistent mapping, with primary implementation in Uki City, Hikawa Town, and Yatsushiro City.
- Units of analysis: Residences for structural functional loss; harmonized small-area grids for population and cooling-protection need; resident-days for duration without effective cooling; and shelter catchments for placement and power decisions.
- Population: All residents, with primary strata for ages 65+, 75+, and 85+, older single-person households, and older-couple households.
- Immediate period: Days 0-14 for rapid response.
- Extended period: Days 0-30 for cooling-protection, placement, power, and health-risk planning.
- Historical heat reference: Matching calendar periods in 2021-2025.
- Damage reporting layers: Confirmed or probable reported residence evidence and modeled scenario allocations must remain separate.

### Study Design Declaration

- Research type: applied
- Study design: Two-stage applied rapid-assessment study. Stage 1 produces an uncertainty-aware nowcast of structural residence loss, older residents requiring cooling assessment, placement deficits, and the power needed to restore protection under a common outdoor-weather scenario. Stage 2 validates and recalibrates the nowcast when official inspections, displacement, placement, indoor-temperature, shelter-operation, or health records become available.
- Interpretation limit: The initial products estimate where loss and unmet cooling demand are plausible. They do not establish an exact destroyed-residence count, prove displacement, infer indoor temperature from satellite data, or identify earthquake-attributable deaths. Mortality is reported only as a cooled-versus-uncooled scenario contrast when a compatible effect estimate is available.

## 2. Theoretical Background  /  Conceptual Framework  /  Problem Formulation

Research type: applied
Section focus: Early decision support under delayed damage statistics and measurement uncertainty.

### Research Gap

- Rapid disaster mapping often treats visible structural destruction as the endpoint, while heat-health planning treats population, weather, indoor protection, and shelters separately. This separation cannot answer whether older residents have lost access to the cooling adaptation that protected them before the earthquake.
- Post-event-only aerial images can detect some large debris fields but miss roof-intact buckling and internal damage. Generic image-recognition scores are therefore unsuitable as direct destroyed-building counts.
- Official damage statistics arrive later, but delayed labels create an opportunity for retrospective validation of an early nowcasting model rather than a reason to postpone all analysis.

### Conceptual Framework

- The policy-relevant construct is functional loss of heat-protective shelter, defined as collapse, unsafe occupancy, inaccessible housing, or loss of essential cooling-enabling services. It is broader than visually confirmed roof collapse and narrower than general earthquake exposure.
- The pathway is: earthquake shaking and ground failure -> structural residence loss -> loss of usable home cooling -> unprotected older-person-days under the same outdoor weather -> increased health risk unless effective cooled placement is restored.
- Outdoor temperature is a common background condition in both protection states. The analytical contrast is effective cooling versus no effective cooling, not earthquake weather versus non-earthquake weather.
- Aerial imagery and deep-learning screens remain contextual evidence because current image quality cannot validate individual residence loss. Official totals, mapped exposure, explicit scenario assumptions, and later inspection records determine the auditable allocation and validation path.
- Older residents may remain at home, move to public shelters, stay with relatives, sleep in vehicles, or relocate elsewhere. Shelter-demand estimates must therefore use scenarios rather than equate housing loss with public-shelter occupancy.
- Scope boundary: The study prioritizes early spatial decision support and validation. It does not initially claim a causal mortality effect, infer indoor exposure without measurement or a documented thermal model, or enumerate individual damaged residences.

### Problem Formulation

- Stage 1 allocates official structural residence-loss totals to grids under explicit distance-decay, exposure-proxy, and half-collapse scenarios while retaining confirmed evidence at its reported geography.
- Stage 1 combines grid-level expected residence loss with older-population vulnerability to identify residents requiring cooling assessment. It does not equate this population with observed displacement or confirmed cooling loss.
- Cooling demand is allocated to reachable effective cooled placements under explicit mobility and relocation scenarios. Effective Cooled Capacity is constrained by functioning equipment, power resilience, usable cooled space, accessibility, and current occupancy.
- The primary decision outputs are cooling-protection need, unprotected older-person-days, and the peak power and daily electricity needed to close the deficit. The common outdoor heat scenario determines how urgent cooling is but does not define the earthquake exposure.
- A later mortality output compares otherwise identical outdoor-weather states with and without effective cooling. It is deferred until a compatible indoor-temperature or cooling-effect response and duration assumptions are documented.
- Stage 2 compares early predictions with later official inspection, displacement, and shelter-use data. Prediction error, calibration, and missed-case analysis are research outcomes in their own right.
- Interpretation limit: A modeled residence-loss allocation is not an inspection result; expected affected population is not observed displacement or confirmed cooling loss; satellite land-surface temperature is not indoor heat; nominal shelter capacity is not Effective Cooled Capacity; and a cooled-versus-uncooled risk scenario is not a causal estimate of earthquake-attributable mortality.

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
| Epicentral Distance km | Grid Distance from the Official Epicenter in Kilometres | hazard proxy | Straight-line distance from the disclosure-group representative point to the official epicenter at 32.6 degrees north and 130.7 degrees east. | Calculated in JGD2011 / Japan Plane Rectangular CS II; distance is a proxy for shaking exposure rather than an observed intensity measure. | yes |
| Housing Loss Allocation Weight | Central Structural Housing-Loss Allocation Weight | modeled allocation | Nonnegative central ensemble weight assigned to one disclosure group, normalized to sum to one across Kumamoto Prefecture. | Derived from the median spatial pattern across distance-decay and exposure-proxy specifications, then renormalized to the central residence-loss total. | yes |
| Housing Loss Scenario Count | Number of Structural Housing-Loss Scenarios | sensitivity | Number of specifications in the housing-loss ensemble. | Twenty-seven scenarios combine three distance-decay scales, three exposure proxies, and three half-collapse functional-loss weights. | yes |
| Distance Decay Scenario Set km | Epicentral-Distance Decay Scale Set in Kilometres | sensitivity | Candidate values of \(\lambda\) in the distance-decay term \(\exp(-d_g/\lambda)\). | Fixed at 10, 20, and 40 km; no value is interpreted as an estimated physical attenuation coefficient. | yes |
| Half-Collapse Functional Loss Weight Set | Half-Collapse Functional-Loss Scenario Weight Set | sensitivity | Candidate values of \(\theta\) in \(T_s=F+\theta_s H\). | Fixed at 0, 0.5, and 1; partial damage is excluded from structural functional loss. | yes |
| Housing Exposure Proxy Set | Residential Exposure Allocation Proxy Set | sensitivity | Alternative grid denominators used to distribute each scenario total. | General Households, Mapped Building Count, and Mapped Building Footprint Area m2 are evaluated separately; building variables remain exposure proxies rather than observed residential use or structural vulnerability. | yes |
| Structural Housing Loss Central Total Residences | Central Scenario Total of Structurally Functionally Lost Residences | scenario total | Official full-collapse residences plus one-half of official half-collapse residences at the damage evidence cutoff. | Used only to constrain the central spatial allocation; it is not a newly observed total. | yes |
| Functional Housing Loss Status | Grid Functional Housing-Loss Estimation Status | main outcome status | Whether the grid has a structural residence-loss scenario estimate and an eligible exposure denominator. | Coded as structural scenario estimated or no residential exposure denominator. | yes |
| Expected Functionally Lost Residences | Central Expected Number of Structurally Functionally Lost Residences | main outcome | Central residence-loss estimate allocated to the grid under the normalized ensemble-median spatial pattern. | Sums to the central scenario total across Kumamoto Prefecture; it is a scenario allocation, not an inspection count. | yes |
| Expected Functionally Lost Residences Lower Bound | Pointwise Lower Structural Residence-Loss Scenario Bound | uncertainty | Minimum grid estimate across the twenty-seven housing-loss scenarios. | A pointwise scenario bound; values must not be summed and interpreted as one jointly realized prefecture scenario. | yes |
| Expected Functionally Lost Residences Upper Bound | Pointwise Upper Structural Residence-Loss Scenario Bound | uncertainty | Maximum grid estimate across the twenty-seven housing-loss scenarios. | A pointwise scenario bound; values must not be summed and interpreted as one jointly realized prefecture scenario. | yes |
| Confirmed Functionally Lost Residences | Confirmed Functionally Lost Residences at Supported Geography | lower-bound outcome | Residence count supported by confirmed functional-loss evidence at the geography reported by the source. | Remains missing at grid level because current confirmed residence totals are not geolocated to disclosure groups. | yes |
| Estimated Affected Population | Population Associated with Central Structural Residence-Loss Scenario | exposure outcome | \(E[N_g]=N_g\min(1,E[L_g]/G_g)\), where \(G_g\) is General Households. | Estimates residents associated with modeled structural residence loss; it is not observed displacement. | yes |
| Estimated Affected Population Lower Bound | Pointwise Lower Affected-Population Scenario Bound | uncertainty | Total population multiplied by the pointwise lower modeled residence-loss share. | Retains the same proportional occupancy assumption as the central estimate. | yes |
| Estimated Affected Population Upper Bound | Pointwise Upper Affected-Population Scenario Bound | uncertainty | Total population multiplied by the pointwise upper modeled residence-loss share. | Retains the same proportional occupancy assumption as the central estimate. | yes |
| Estimated Affected Population Age 65+ | Population Age 65 or Older Associated with Central Structural Residence-Loss Scenario | primary exposure outcome | \(E[N_{65+,g}]=N_{65+,g}\min(1,E[L_g]/G_g)\). | Scenario estimate of older residents associated with structural residence loss; not observed displacement. | yes |
| Estimated Affected Population Age 65+ Lower Bound | Pointwise Lower Affected Population Age 65 or Older Scenario Bound | uncertainty | Population Age 65+ multiplied by the pointwise lower modeled residence-loss share. | Used to express model-specification sensitivity. | yes |
| Estimated Affected Population Age 65+ Upper Bound | Pointwise Upper Affected Population Age 65 or Older Scenario Bound | uncertainty | Population Age 65+ multiplied by the pointwise upper modeled residence-loss share. | Used to express model-specification sensitivity. | yes |
| Estimated Affected Population Age 75+ | Population Age 75 or Older Associated with Central Structural Residence-Loss Scenario | exposure outcome | Uses the same central residence-loss share as the age-65-or-older estimate. | Scenario estimate; not observed displacement. | yes |
| Estimated Affected Population Age 75+ Lower Bound | Pointwise Lower Affected Population Age 75 or Older Scenario Bound | uncertainty | Population Age 75+ multiplied by the pointwise lower modeled residence-loss share. | Used to express model-specification sensitivity. | yes |
| Estimated Affected Population Age 75+ Upper Bound | Pointwise Upper Affected Population Age 75 or Older Scenario Bound | uncertainty | Population Age 75+ multiplied by the pointwise upper modeled residence-loss share. | Used to express model-specification sensitivity. | yes |
| Estimated Affected Population Age 85+ | Population Age 85 or Older Associated with Central Structural Residence-Loss Scenario | exposure outcome | Uses the same central residence-loss share as the age-65-or-older estimate. | Scenario estimate; not observed displacement. | yes |
| Estimated Affected Population Age 85+ Lower Bound | Pointwise Lower Affected Population Age 85 or Older Scenario Bound | uncertainty | Population Age 85+ multiplied by the pointwise lower modeled residence-loss share. | Used to express model-specification sensitivity. | yes |
| Estimated Affected Population Age 85+ Upper Bound | Pointwise Upper Affected Population Age 85 or Older Scenario Bound | uncertainty | Population Age 85+ multiplied by the pointwise upper modeled residence-loss share. | Used to express model-specification sensitivity. | yes |
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

### Confirmed Preprocessing and Evidence Rules

The following rules apply to the selected analysis variables. Numeric fields are coerced
to numeric values, date and time fields are parsed as datetimes, text identifiers are
trimmed, and status fields may be stored as categorical values. Geometry is preserved in
the geospatial outputs. Missing values are not imputed or recoded as zero, rows are not
deleted because one selected field is missing, and counts are not clipped, winsorized, or
log-transformed. Quality, evidence-tier, verification, and data-status fields remain in the
analysis inputs. Variables for which no defensible source has been acquired remain pending
and must not be populated with invented observations.

### Mortality Reference Variables

Official municipality-level age-65-or-older all-cause deaths for 2020-2024 and the 2020
population denominator are available for all 45 Kumamoto Prefecture municipalities. The
denominator is held fixed across five years, so the resulting rate is a planning baseline
rather than a period-specific person-year rate. Outdoor temperature-mortality candidates
remain non-final because they do not identify the cooling-loss contrast.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Municipality Code | Official Municipality Code | linkage | Stable code for a Kumamoto Prefecture municipality. | Retained as five-character text; the five Kumamoto City wards are aggregated to city code 43100 to match the mortality baseline. | yes |
| Municipality | Municipality Name | spatial linkage | Municipality represented by the mortality reference record. | Harmonized to the 45-municipality boundary and summary-table naming system. | yes |
| Age Group | Mortality Reference Age Group | stratification | Age band to which the population, deaths, and response estimate apply. | The main mortality scenario selects the 65+ record. | yes |
| Baseline Period Start | Mortality Baseline Period Start Date | time index | First date included in the baseline mortality estimate. | Parsed as 2020-01-01. | yes |
| Baseline Period End | Mortality Baseline Period End Date | time index | Last date included in the baseline mortality estimate. | Parsed as 2024-12-31. | yes |
| Population at Risk | Mortality Baseline Population at Risk | denominator | 2020 Census population in the selected municipality and age group. | Retained as a nonnegative count without imputation and held fixed across the five baseline years. | yes |
| All-Cause Deaths | Baseline All-Cause Death Count | mortality numerator | Pooled 2020-2024 all-cause deaths in the selected municipality and age group. | Final vital-statistics counts are summed across the five years. | yes |
| Baseline Mortality Rate per 100,000 | Age-Specific Baseline Mortality Rate per 100,000 Population | baseline risk | (B_m=100000 D_m/(5N_m)). | (D_m) is pooled 2020-2024 age-65-or-older all-cause deaths and (N_m) is the fixed 2020 age-65-or-older population. | yes |
| Mortality Data Status | Mortality Reference Data Status | quality control | Availability and denominator status of the mortality input. | Coded as final pooled deaths with an approximate fixed-2020-population denominator. | yes |
| Estimate ID | Temperature-Mortality Response Estimate ID | linkage | Unique identifier for one candidate exposure-response estimate. | Constructed from study, region, age group, exposure metric, and model specification. | no |
| Study Region | Temperature-Mortality Study Region | applicability | Geographic population from which the response estimate was obtained. | Retained from the source and evaluated for transferability to Kumamoto. | no |
| Exposure Metric | Temperature-Mortality Exposure Metric | model input definition | Temperature variable used by the response estimate. | Must distinguish maximum, minimum, mean, apparent, or another explicitly defined temperature metric. | no |
| Reference Temperature C | Temperature-Mortality Reference Temperature in Degrees Celsius | model reference | Temperature relative to which heat-related risk is evaluated. | Retained from the selected model or estimated only under a documented estimation framework. | no |
| Relative Risk per 1 C Increase | Temperature-Mortality Relative Risk per 1 Degree Celsius Increase | exposure-response parameter | Multiplicative mortality risk change associated with a 1 C increase under the source model. | Used only when the source specification is compatible with the selected exposure metric, threshold, age group, and lag structure. | no |
| Relative Risk Lower 95% Confidence Interval | Lower 95% Confidence Limit for Temperature-Mortality Relative Risk | uncertainty | Lower confidence limit for Relative Risk per 1 C Increase. | Retained with the point estimate and propagated through scenario uncertainty. | no |
| Relative Risk Upper 95% Confidence Interval | Upper 95% Confidence Limit for Temperature-Mortality Relative Risk | uncertainty | Upper confidence limit for Relative Risk per 1 C Increase. | Retained with the point estimate and propagated through scenario uncertainty. | no |
| Minimum Lag Days | Minimum Temperature-Mortality Lag | model specification | Earliest lag day included in the response estimate. | Retained as a nonnegative integer. | no |
| Maximum Lag Days | Maximum Temperature-Mortality Lag | model specification | Latest lag day included in the response estimate. | Retained as a nonnegative integer no smaller than Minimum Lag Days. | no |
| Estimate Applicability Status | Kumamoto Applicability Status of the Temperature-Mortality Estimate | quality control | Assessment of whether an estimate is suitable for the study population and exposure definition. | Coded as pending review, applicable, sensitivity only, or rejected with a documented reason. | no |

### Cooling-Loss Mortality Planning Scenario Variables

The mortality scenario uses a direct cooled-versus-uncooled effect estimate for older
institutional residents during extreme heat. It is transferred to Kumamoto only as a
planning parameter. Outdoor weather is identical in both cooling states, and the current
calculation uses the no-verified-placement demand-side bound rather than observed exposure.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Expected High-Heat Scenario Days | Expected High-Heat Days in the 30-Day Planning Window | background heat scenario | \(H^{heat}_m=IDW_4(5^{-1}\sum_y\sum_t I^{heat}_{s,y,t})\). | A high-heat day has either JMA Hot Day Indicator or Hot Night Indicator equal to one; station five-year means are interpolated to municipality centroids with four-neighbor inverse-distance weighting. | yes |
| Baseline Daily Mortality Probability | Municipality Age-65-or-Older Daily Baseline Mortality Probability | baseline risk | \(p_m=B_m/(100000\times365.25)\). | Converts the annualized municipality baseline rate to a daily probability. | yes |
| Effective-Cooling High-Heat Daily Mortality Probability | Modeled Daily Mortality Probability During High Heat with Effective Cooling | protected state | \(p^{cool}_m=OR^{cool}o_m/(1+OR^{cool}o_m)\). | \(o_m=p_m/(1-p_m)\) and \(OR^{cool}=1.03\), the published high-heat odds ratio in older institutional residents with air conditioning. | yes |
| No-Effective-Cooling Relative Odds Ratio | Relative Odds of Death During High Heat without versus with Effective Cooling | cooling-loss effect | \(ROR=1.08\). | Primary published lag-0 interaction estimate; transferred from older institutional residents outside Japan. | yes |
| No-Effective-Cooling Relative Odds Ratio Lower 95% CI | Lower 95% Confidence Limit for the Cooling-Loss Relative Odds Ratio | effect uncertainty | \(ROR^L=1.01\). | Published lower confidence limit; transfer uncertainty is not included. | yes |
| No-Effective-Cooling Relative Odds Ratio Upper 95% CI | Upper 95% Confidence Limit for the Cooling-Loss Relative Odds Ratio | effect uncertainty | \(ROR^U=1.15\). | Published upper confidence limit; transfer uncertainty is not included. | yes |
| Cooling-Loss Daily Mortality Risk Contrast | Daily Mortality Probability Difference without versus with Effective Cooling | modeled contrast | \(\delta_m=ROR\,o^{cool}_m/(1+ROR\,o^{cool}_m)-p^{cool}_m\). | Holds outdoor high-heat conditions fixed and changes only the cooling state. | yes |
| Effective-Cooling 30-Day Mortality Risk | 30-Day Mortality Risk with Effective Cooling | protected-state outcome | \(r^{cool}_m=1-(1-p_m)^{H-H^{heat}_m}(1-p^{cool}_m)^{H^{heat}_m}\). | Accumulates daily risk across the 30-day window without adding an unestimated duration-response multiplier. | yes |
| No-Effective-Cooling 30-Day Mortality Risk | 30-Day Mortality Risk without Effective Cooling | unprotected-state outcome | \(r^{no\ cool}_m=1-(1-p_m)^{H-H^{heat}_m}(1-p^{no\ cool}_m)^{H^{heat}_m}\). | Uses the same outdoor high-heat days as the protected state and changes only cooling status. | yes |
| Cooling-Loss Relative 30-Day Mortality Burden Increase % | Relative Increase in 30-Day Mortality Burden without Effective Cooling | modeled relative outcome | \(M_m=100(r^{no\ cool}_m/r^{cool}_m-1)\). | Main Panel C metric; expresses relative rather than absolute burden. | yes |
| Cooling-Loss Relative 30-Day Mortality Burden Increase % Lower 95% CI | Lower Effect-Estimate Limit for the Relative 30-Day Mortality Burden Increase | effect uncertainty | \(M^L_m=100(r^{no\ cool,L}_m/r^{cool}_m-1)\). | Varies only the published cooling-loss relative-odds parameter. | yes |
| Cooling-Loss Relative 30-Day Mortality Burden Increase % Upper 95% CI | Upper Effect-Estimate Limit for the Relative 30-Day Mortality Burden Increase | effect uncertainty | \(M^U_m=100(r^{no\ cool,U}_m/r^{cool}_m-1)\). | Varies only the published cooling-loss relative-odds parameter. | yes |
| Cooling-Loss Incremental Mortality Risk per 100,000 | 30-Day Cooling-Loss Incremental Mortality Risk per 100,000 Affected Older Persons | modeled risk | \(R_m=100000(r^{no\ cool}_m-r^{cool}_m)\). | Central absolute risk difference under the five-year matching-period high-heat scenario. | yes |
| Cooling-Loss Incremental Mortality Risk per 100,000 Lower 95% CI | Lower Effect-Estimate Limit for Incremental Mortality Risk per 100,000 | effect uncertainty | \(R^L_m=100000(r^{no\ cool,L}_m-r^{cool}_m)\). | Varies only the published cooling-loss relative-odds parameter. | yes |
| Cooling-Loss Incremental Mortality Risk per 100,000 Upper 95% CI | Upper Effect-Estimate Limit for Incremental Mortality Risk per 100,000 | effect uncertainty | \(R^U_m=100000(r^{no\ cool,U}_m-r^{cool}_m)\). | Varies only the published cooling-loss relative-odds parameter. | yes |
| Incremental Cooling-Loss-Related Excess Deaths | Expected Incremental Deaths under the No-Verified-Placement Scenario | modeled outcome | \(\Delta D_m=(PD^{NP}_m/H)(r^{no\ cool}_m-r^{cool}_m)\). | Retained for the municipality table but not used as the main Panel C metric; does not represent observed deaths. | yes |
| Incremental Cooling-Loss-Related Excess Deaths Lower 95% CI | Lower Effect-Estimate Limit for Incremental Cooling-Loss-Related Excess Deaths | effect uncertainty | \(\Delta D^L_m=(PD^{NP}_m/H)(r^{no\ cool,L}_m-r^{cool}_m)\). | Varies only the published cooling-effect parameter; housing, heat-scenario, baseline-rate, and transfer uncertainty are not included. | yes |
| Incremental Cooling-Loss-Related Excess Deaths Upper 95% CI | Upper Effect-Estimate Limit for Incremental Cooling-Loss-Related Excess Deaths | effect uncertainty | \(\Delta D^U_m=(PD^{NP}_m/H)(r^{no\ cool,U}_m-r^{cool}_m)\). | Varies only the published cooling-effect parameter; housing, heat-scenario, baseline-rate, and transfer uncertainty are not included. | yes |
| Cooling-Loss Mortality Scenario Status | Cooling-Loss Mortality Scenario Evidence Status | quality control | Categorical evidence status. | Coded as a literature-anchored, no-verified-placement planning scenario; not observed or earthquake-attributable mortality. | yes |

### Cooling-Protection Planning Scenario Variables

The early planning scenario uses the modeled older-person cooling-assessment population
over a fixed 30-day horizon. It assumes no **verified** effective cooled placement only to
construct a demand-side upper bound. It does not assume that physical shelter capacity is
zero, and it does not identify the actual cooling-capacity gap.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Cooling Protection Planning Horizon Days | Cooling-Protection Planning Horizon in Days | scenario parameter | \(H=30\). | Fixed to the one-month post-earthquake planning window. | yes |
| No-Placement Unprotected Older-Person-Days | Central No-Verified-Placement Older-Person-Days Planning Bound | demand-side planning bound | \(PD^{NP}_g=H E[N_{65+,g}]\). | Central structural residence-loss scenario multiplied by 30 days; not observed exposure or an actual placement deficit. | yes |
| No-Placement Unprotected Older-Person-Days Lower Bound | Lower No-Verified-Placement Older-Person-Days Scenario Bound | uncertainty | \(PD^{NP,L}_g=H E[N^L_{65+,g}]\). | Uses the pointwise lower housing-loss scenario; values are not a jointly realized prefecture-wide lower scenario. | yes |
| No-Placement Unprotected Older-Person-Days Upper Bound | Upper No-Verified-Placement Older-Person-Days Scenario Bound | uncertainty | \(PD^{NP,U}_g=H E[N^U_{65+,g}]\). | Uses the pointwise upper housing-loss scenario; values are not a jointly realized prefecture-wide upper scenario. | yes |
| Cooling Protection Scenario Status | Cooling-Protection Scenario Evidence Status | quality control | Categorical scenario status. | Coded as no verified placement demand-side bound; prevents interpretation as observed cooling loss or zero physical capacity. | yes |

### Pending Shelter Cooling and Power Variables

These fields require facility-level operational verification. A designated-shelter record
alone does not establish current opening, occupancy, cooling availability, electric supply,
or backup-power capacity.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Current Shelter Occupancy | Current Number of Shelter Occupants | demand driver | People currently occupying the facility at Observation Time. | Time-stamped verified count; a designated capacity or evacuation-instruction population is not substituted. | no |
| Available Cooled Floor Area m2 | Operational Cooled Floor Area in Square Metres | cooling capacity input | Floor area that can currently maintain protective indoor conditions. | Verified facility value; nominal building area is not assumed to be cooled area. | no |
| HVAC Cooling Capacity kW Thermal | Heating, Ventilation, and Air Conditioning Cooling Capacity in Thermal Kilowatts | cooling capacity input | Available thermal cooling output of operational equipment. | Sum of verified operational equipment capacities at Observation Time. | no |
| Cooling System COP | Cooling System Coefficient of Performance | conversion parameter | Ratio of delivered thermal cooling power to electric input power. | Facility-specific verified value where available; otherwise a clearly labelled scenario parameter. | no |
| Cooling Operating Hours per Day | Daily Cooling Operating Hours | energy parameter | Number of hours per day for which protective cooling is expected to operate. | Facility-specific schedule where verified; otherwise a labelled scenario value. | no |
| Verified Available Grid Power kW | Verified Grid Electric Power Available to the Facility | available supply | Grid electric power available for cooling and other critical loads at Observation Time. | Time-stamped facility verification; nominal connection capacity is retained separately if operational availability is unknown. | no |
| Backup Generator Capacity kW | Operational Backup Generator Electric Capacity | available supply | Electric output capacity of operational backup generation. | Verified nameplate and operational status; unavailable or untested equipment is not counted as available. | no |
| Backup Power Duration Hours | Expected Backup Power Duration | resilience | Hours for which verified backup generation can operate under available fuel and load. | Estimated from verified fuel, consumption, and usable capacity or retained from a documented facility assessment. | no |
| Non-Cooling Critical Load kW | Facility Non-Cooling Critical Electric Load | competing demand | Electric load required for lighting, communications, medical devices, water, and other non-cooling functions. | Verified or explicitly scenario-based; subtracted before power is assigned to cooling. | no |
| Facility Power Data Status | Facility Cooling and Power Data Status | quality control | Completeness and operational validity of the facility audit. | Coded as verified, partial, scenario only, unavailable, or outdated. | no |
| Evidence Tier | Facility Cooling and Power Evidence Strength Tier | uncertainty | Strength and directness of the facility-level evidence. | Direct operational measurement remains distinct from administrative records or assumptions. | no |
| Verification Status | Facility Cooling and Power Verification Status | quality control | Current verification state of one facility record. | Time-stamped categorical field linked by Common ID. | no |

### Cooling Electricity Demand Scenario Parameters

The demand-side power calculation uses three internally consistent engineering scenarios.
All three hold Estimated Affected Population Age 65+ at its central structural residence-
loss scenario value so that prefecture totals can be compared and summed. The parameters
do not describe installed equipment at any specific shelter.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Power Demand Scenario | Emergency Cooling Electricity Demand Scenario | scenario linkage | One of Low, Central, or High. | Defines one complete parameter bundle; parameters from different bundles are never mixed. | yes |
| Minimum Shelter Living Area m2 per Person | Minimum Planned Shelter Living Area per Person | demand parameter | \(a=3.5\) square metres per person. | Anchored to the Cabinet Office shelter guidance; used as cooled-area demand, not observed occupied floor area. | yes |
| Cooling Load Density W per m2 | Scenario Cooling Thermal Load Density | demand parameter | \(r_z \in \{127,134,141\}\) watts per square metre for scenario \(z\). | Low and High use the MLIT gymnasium cooling-load case bounds; Central is their midpoint. | yes |
| Cooling Thermal Load W per Person | Protective Cooling Thermal Load per Person in Watts | derived demand parameter | \(q_z=a r_z\). | Equals 444.5, 469.0, and 493.5 watts per person in Low, Central, and High. | yes |
| Scenario Cooling System COP | Scenario Cooling-System Coefficient of Performance | conversion parameter | \(COP_z \in \{4.0,3.0,2.5\}\). | Research scenarios ordered from more efficient to less efficient cooling; COP is thermal cooling delivered divided by electric input. | yes |
| Scenario Peak Load Diversity Factor | Scenario Cooling Peak Load Diversity Factor | demand parameter | \(f_z \in \{0.8,0.9,1.0\}\). | Research scenarios for the fraction of individual peak loads occurring simultaneously. | yes |
| Scenario Cooling Operating Hours per Day | Scenario Daily Cooling Operating Hours | energy parameter | \(h_z \in \{12,18,24\}\) hours per day. | Research scenarios reflecting daytime-only through continuous protective cooling. | yes |
| Cooling Power Scenario Status | Cooling-Power Scenario Evidence Status | quality control | Categorical evidence status. | Coded as demand side only with no verified supply; the output is not an observed facility load or power gap. | yes |

### Cooling-Power Result Variables

These variables distinguish finalized demand-side power scenarios from supply-side
outcomes that still require operational inputs. The finalized health-planning variables
are defined in the preceding cooling-loss mortality scenario subsection.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Cooling Thermal Load kW | Required Protective Cooling Thermal Load in Kilowatts | modeled demand | \(Q_{g,z}=N^{need}_g q_z/1000\). | Central cooling-assessment population multiplied by the scenario per-person thermal load. | yes |
| Required Peak Cooling Electric Power kW | Required Peak Electric Power for Protective Cooling | modeled demand | \(P^{req}_{g,z}=Q_{g,z}f_z/COP_z\). | Thermal load multiplied by the scenario diversity factor and divided by scenario COP. | yes |
| Required Daily Cooling Electricity kWh | Required Daily Electricity for Protective Cooling | modeled energy demand | \(E^{req}_{g,z}=P^{req}_{g,z}h_z\). | Required peak power multiplied by scenario daily operating hours; reported separately from peak power. | yes |
| Verified Available Electric Power kW | Verified Electric Power Available for Cooling | available supply | \(A_g = max(0, G_g + B_g - L_g)\). | Available grid power plus operational backup generation minus non-cooling critical load, with all components evaluated at the same observation time. | no |
| Emergency Cooling Power Gap kW | Unmet Peak Electric Power for Protective Cooling | operational outcome | \(Gap_g = max(0, P_g - A_g)\). | Positive values indicate additional peak electric power required under the specified scenario. | no |
| Effective Cooled Capacity | Effective Number of People Receiving Protective Cooling | intermediate outcome | TBD | Limited by verified occupancy, cooled space, operational thermal capacity, and available electric power. | no |
| Cooling Capacity Gap | Number of Heat-Vulnerable People Without Effective Cooling Capacity | operational outcome | TBD | Difference between the population requiring protective cooling and Effective Cooled Capacity, bounded below by zero. | no |

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

### Structural Residence-Loss Scenario Design

The housing-loss component is a total-constrained spatial scenario rather than a fitted
fragility model. Epicentral Distance km represents relative proximity to the earthquake,
while General Households, Mapped Building Count, and Mapped Building Footprint Area m2
provide alternative exposure denominators. Building polygons do not identify residential
use, construction material, age, occupancy, or structural condition. They therefore enter
as alternative allocation proxies and are never assigned an unvalidated vulnerability
coefficient.

Official full-collapse and half-collapse residence totals determine the scenario totals.
Full collapse receives weight one, half collapse receives alternative functional-loss
weights of 0, 0.5, and 1, and partial damage is excluded. Distance-decay scales of 10, 20,
and 40 km are crossed with the three exposure denominators and the three half-collapse
weights to form twenty-seven scenarios. The central grid estimate uses the ensemble-median
spatial pattern, renormalized to the official full-collapse total plus one-half of the
half-collapse total. Current confirmed residence losses are not assigned to disclosure
groups because the official counts are not geolocated at that resolution.

This design produces Functional Housing Loss and Older-Person Exposure and supplies the
housing-loss input for later mortality and cooling analyses. It estimates where reported
structural residence loss is more plausibly concentrated under explicit assumptions. It
does not identify an individual damaged residence, estimate a causal distance effect,
represent observed displacement, or include service-related cooling loss within the
structural residence-loss count.

### Cooling-Protection Contrast and Output Order

The downstream estimand is loss of effective cooling protection under a common outdoor-
weather scenario. Estimated Affected Population Age 65+ identifies residents requiring a
cooling assessment after modeled structural residence loss; it is not yet the number who
are displaced or uncooled. A resident is counted as effectively protected only when a
usable home, private placement, or accessible shelter has verified functioning cooling,
power, usable cooled space, and available capacity for that resident at the relevant time.

The output order follows the mechanism. Older-Person Cooling Protection Need and Placement
Deficit first maps cooling-assessment need and the no-verified-placement planning bound.
Emergency Cooling Electricity Requirement Distribution next estimates demand-side peak
power and daily energy under approved Low, Central, and High engineering bundles. It does
not estimate actual supply or the power gap until facility power is verified. Cooling-Loss-
Related Incremental Mortality Risk Distribution is last because it requires both duration
without cooling and a compatible comparison of health risk with and without effective
cooling at the same outdoor temperature.

Municipality-Level Housing Loss, Cooling Demand, and Health-Risk Summary then consolidates
the completed scenario chain at the 45-municipality level. It includes only finalized
demand-side and literature-anchored variables. It does not add empty columns for effective
placement, verified supply, or a power gap, and it does not convert missing operational
evidence to zero.

This is a planning scenario rather than causal identification. Ambient heat data determine
the background conditions under which cooling is needed, but the earthquake exposure is
loss of cooling protection. A general outdoor temperature-mortality association cannot by
itself identify the incremental effect of cooling loss. The numerical planning scenario
therefore uses the accepted direct comparison of mortality during extreme heat among older
institutional residents without versus with air conditioning. Its transfer from a non-Japan
institutional population, the no-verified-placement demand bound, and the historical heat
scenario preclude causal or predictive interpretation. Actual mortality impact remains
unidentified until placement, individual cooling status, and event-period exposure are
observed.

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

### Quaternary Framework: Total-Constrained Structural Residence-Loss Scenarios

For disclosure group \(g\) and distance-decay scale \(\lambda\), the epicentral-distance
term is

\[
h_{g,\lambda}=\exp\left(-\frac{d_g}{\lambda}\right).
\]

\(h_{g,\lambda}\) is the distance-decay weight, \(d_g\) is Epicentral Distance km, and
\(\lambda\) is one of 10, 20, or 40 km. These values describe scenario decay and are not
estimated ground-motion attenuation coefficients.

For scenario \(s=(\lambda,m,\theta)\), the normalized spatial allocation weight is

\[
q_{g,s}=\frac{X_{g,m}h_{g,\lambda}}
{\sum_j X_{j,m}h_{j,\lambda}}.
\]

\(q_{g,s}\) is the scenario-specific allocation weight, \(m\) indexes the selected exposure
proxy, and \(X_{g,m}\) is General Households, Mapped Building Count, or Mapped Building
Footprint Area m2 for group \(g\). The index \(j\) runs over all eligible disclosure groups
in Kumamoto Prefecture.

The structural functional-loss total for scenario \(s\) is

\[
T_s=F+\theta_s H.
\]

\(T_s\) is the scenario total of functionally lost residences, \(F\) is the latest official
full-collapse residence total, \(H\) is the latest official half-collapse residence total,
and \(\theta_s\) is 0, 0.5, or 1. Partial Damage Buildings is not included in \(T_s\).
The scenario allocation is

\[
L_{g,s}=T_s q_{g,s}.
\]

\(L_{g,s}\) is the expected residence loss in group \(g\) under scenario \(s\). Let
\(\widetilde{L}_g=\operatorname{median}_s(L_{g,s})\). The central estimate is constrained to
\(T_0=F+0.5H\) through

\[
E[L_g]=T_0\frac{\widetilde{L}_g}{\sum_j\widetilde{L}_j}.
\]

\(E[L_g]\) is Expected Functionally Lost Residences and \(T_0\) is Structural Housing Loss
Central Total Residences. The pointwise scenario range is

\[
L_g^{lo}=\min_s L_{g,s},
\qquad
L_g^{hi}=\max_s L_{g,s}.
\]

\(L_g^{lo}\) is Expected Functionally Lost Residences Lower Bound and \(L_g^{hi}\) is
Expected Functionally Lost Residences Upper Bound. They are specification bounds at one
grid, not confidence limits, and their sums do not represent one jointly realized
prefecture scenario.

For population stratum \(a\), affected population associated with structural residence loss
is

\[
E[N_{a,g}]=N_{a,g}\min\left(1,\frac{E[L_g]}{G_g}\right).
\]

\(E[N_{a,g}]\) is the estimated affected population in stratum \(a\), \(N_{a,g}\) is the
corresponding population count, and \(G_g\) is General Households. The same transformation
is applied to \(L_g^{lo}\) and \(L_g^{hi}\) to construct the pointwise affected-population
bounds. This proportional occupancy rule does not identify which residents were displaced.

### Quinary Framework: Cooling Protection, Power, and Incremental Health Risk

For disclosure group \(g\) and day \(t\), the initial population requiring cooling
assessment is

\[
N^{need}_{g,t}=E[N_{65+,g}].
\]

\(N^{need}_{g,t}\) is the planning need associated with the central structural residence-
loss scenario and \(E[N_{65+,g}]\) is Estimated Affected Population Age 65+. This is a
conservative demand-side screening population, not observed displacement or confirmed loss
of cooling. Its lower and upper versions use the corresponding affected-population scenario
bounds.

Let \(x_{g,s,t}\) be the number of residents from group \(g\) assigned to effective cooled
placement \(s\) on day \(t\). Valid assignments must satisfy accessibility and capacity:

\[
\sum_g x_{g,s,t} \leq C^{eff}_{s,t}.
\]

\(C^{eff}_{s,t}\) is Effective Cooled Capacity at placement \(s\), constrained by Current
Shelter Occupancy, Available Cooled Floor Area m2, HVAC Cooling Capacity kW Thermal,
Verified Available Grid Power kW, backup power, accessibility, and contemporaneous
operational status. Nominal shelter acceptance or floor area alone does not determine
\(C^{eff}_{s,t}\).

The remaining cooling-protection deficit is

\[
U_{g,t}=\max\left(0,N^{need}_{g,t}-\sum_s x_{g,s,t}\right),
\]

and cumulative unprotected exposure over the 30-day planning window is

\[
PD_g=\sum_{t=0}^{29}U_{g,t}.
\]

\(U_{g,t}\) is Cooling Capacity Gap assigned back to origin group \(g\), and \(PD_g\) is
Unprotected Older-Person-Days. When placement or effective capacity is unverified, these
variables remain missing. A separate demand-side upper-bound scenario may set verified
placement to zero, but it must be labelled as a no-placement planning bound rather than an
observed deficit.

For the demand-side planning figure, the cooling-protection population is fixed to the
central assessment population, \(N^{cool}_g=N^{need}_g=E[N_{65+,g}]\), in every engineering
scenario \(z\). Per-person thermal load is

\[
q_z=a r_z,
\]

where \(a\) is Minimum Shelter Living Area m2 per Person and \(r_z\) is Cooling Load Density
W per m2. The approved Low, Central, and High bundles use \(a=3.5\),
\(r_z=(127,134,141)\), Scenario Cooling System COP \((4.0,3.0,2.5)\), Scenario Peak Load
Diversity Factor \((0.8,0.9,1.0)\), and Scenario Cooling Operating Hours per Day
\((12,18,24)\), respectively. These are planning scenarios rather than facility observations.
Required thermal load is

\[
Q_{g,z}=\frac{N^{cool}_g q_z}{1000},
\]

where \(Q_{g,z}\) is Cooling Thermal Load kW. Required peak electric power and daily
electricity are

\[
P^{req}_{g,z}=\frac{Q_{g,z}f_z}{COP_z},
\qquad
E^{req}_{g,z}=P^{req}_{g,z}h_z.
\]

\(P^{req}_{g,z}\) is Required Peak Cooling Electric Power kW, \(f_z\) is Scenario Peak Load
Diversity Factor, \(COP_z\) is Scenario Cooling System COP, \(E^{req}_{g,z}\) is Required
Daily Cooling Electricity kWh, and \(h_z\) is Scenario Cooling Operating Hours per Day.
Peak power and daily energy are never interchanged. Municipality values sum disclosure
groups assigned by representative point; the prefecture sensitivity panel sums the same
central assessment population under each complete engineering bundle.

Verified electric power available for cooling is

\[
A_{s,t}=\max\left(0,G_{s,t}+B_{s,t}-L^{critical}_{s,t}\right),
\]

where \(A_{s,t}\) is the verified available electric power, \(G_{s,t}\) is Verified
Available Grid Power kW, \(B_{s,t}\) is Backup Generator Capacity kW, and
\(L^{critical}_{s,t}\) is Non-Cooling Critical Load kW. The emergency power gap is

\[
Gap^{power}_{s,t}=\max\left(0,P^{req}_{s,t}-A_{s,t}\right).
\]

\(Gap^{power}_{s,t}\) is Emergency Cooling Power Gap kW. Missing supply components do not
equal zero. The current demand-side figure therefore reports \(P^{req}\) and \(E^{req}\)
only; Verified Available Electric Power kW and Emergency Cooling Power Gap kW remain missing.

For the mortality planning scenario, municipality \(m\)'s daily baseline probability is

\[
p_m=\frac{B_m}{100000\times365.25},
\]

where \(p_m\) is Baseline Daily Mortality Probability and \(B_m\) is Baseline Mortality
Rate per 100,000. Let \(o_m=p_m/(1-p_m)\) be the corresponding baseline odds. The
effective-cooling high-heat probability is

\[
p^{cool}_m=\frac{OR^{cool}o_m}{1+OR^{cool}o_m},
\]

where \(p^{cool}_m\) is Effective-Cooling High-Heat Daily Mortality Probability and
\(OR^{cool}=1.03\) is the published high-heat odds ratio in institutions with air
conditioning. The no-effective-cooling probability is

\[
p^{no\ cool}_m=\frac{ROR\,o^{cool}_m}{1+ROR\,o^{cool}_m},
\]

where \(p^{no\ cool}_m\) is the daily high-heat mortality probability without effective
cooling, \(o^{cool}_m=p^{cool}_m/(1-p^{cool}_m)\), and \(ROR=1.08\) is the accepted
relative odds ratio comparing institutions without versus with air conditioning. The
published 95% confidence limits are \(ROR^L=1.01\) and \(ROR^U=1.15\).

The effective-cooling and no-effective-cooling 30-day risks are

\[
r^{cool}_m=1-(1-p_m)^{H-H^{heat}_m}
(1-p^{cool}_m)^{H^{heat}_m},
\]

\[
r^{no\ cool}_m=1-(1-p_m)^{H-H^{heat}_m}
(1-p^{no\ cool}_m)^{H^{heat}_m},
\]

where \(r^{cool}_m\) is Effective-Cooling 30-Day Mortality Risk,
\(r^{no\ cool}_m\) is No-Effective-Cooling 30-Day Mortality Risk,
\(H^{heat}_m\) is Expected High-Heat Scenario Days, and \(H=30\). Daily survival is
accumulated across the planning window; no additional nonlinear duration-response
multiplier is imposed.

The relative and absolute cooling-loss contrasts are

\[
M_m=100\left(\frac{r^{no\ cool}_m}{r^{cool}_m}-1\right),
\]

\[
R_m=100000\left(r^{no\ cool}_m-r^{cool}_m\right),
\]

\[
\Delta D_m=\frac{PD^{NP}_m}{H}
\left(r^{no\ cool}_m-r^{cool}_m\right),
\]

where \(M_m\) is Cooling-Loss Relative 30-Day Mortality Burden Increase %,
\(R_m\) is Cooling-Loss Incremental Mortality Risk per 100,000,
\(PD^{NP}_m\) is No-Placement Unprotected Older-Person-Days, and \(\Delta D_m\) is
Incremental Cooling-Loss-Related Excess Deaths. Outdoor weather is identical in both
cooling states. Panel C reports \(M_m\); \(\Delta D_m\) is retained for the municipality
table. The lower and upper results vary only \(ROR\); they are effect-estimate confidence
limits, not complete uncertainty intervals. The estimate is a transferable planning
scenario and not observed, forecast, causal, or earthquake-attributable mortality.

### Municipality Summary Aggregation

For an additive grid-level result, the municipality summary uses

\[
X_m=\sum_{g\in\mathcal{G}_m}X_g,
\]

where \(X_m\) is the municipality total, \(X_g\) is the corresponding disclosure-group
value, and \(\mathcal{G}_m\) is the set of disclosure groups assigned to municipality
\(m\) by representative point. This aggregation is used for Expected Functionally Lost
Residences, Estimated Affected Population Age 65+, and No-Placement Unprotected
Older-Person-Days. Lower and upper columns sum pointwise bounds and are not interpreted as
joint municipality confidence intervals.

Required Peak Cooling Electric Power kW and Required Daily Cooling Electricity kWh select
the Central Power Demand Scenario before municipality summation. Expected High-Heat
Scenario Days, Incremental Cooling-Loss-Related Excess Deaths, and Cooling-Loss Relative
30-Day Mortality Burden Increase % are retained from the municipality mortality scenario.
The 45 rows are ordered by central Estimated Affected Population Age 65+ from highest to
lowest. No prefecture total row is added because pointwise lower and upper housing bounds
are not jointly additive.

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
- A strict-first historical satellite mean is retained. Relaxed-quality observations fill
  only pixels with no strict-quality mean and never overwrite an available strict value.
- Mean-only, satellite-only, and satellite-plus-residual candidates are compared by leave-
  one-station-out error; residual interpolation is not retained merely because it appears
  spatially smoother.
- Pixels outside the land-surface-temperature range represented by eligible stations are
  flagged as extrapolation and are not used for precise local temperature claims.
- Historical Land Surface Temperature SD C, MODIS Valid Observation Count, and quality
  support tier remain in the analytical data even when quality hatching is omitted from the
  result figure.
- The residence-loss main estimate is repeated across 10, 20, and 40 km distance-decay
  scales, three exposure proxies, and three half-collapse functional-loss weights.
- General Households is the official-population occupancy denominator; mapped building count
  and footprint area are alternative allocation proxies, not residence counts or fragility
  measurements.
- Confirmed Functionally Lost Residences remains missing at disclosure-group level until
  confirmed residence evidence is geolocated; the scenario allocation never fills that
  lower-bound field.
- Pointwise lower and upper residence-loss bounds are not summed as a prefecture uncertainty
  interval because they can originate from different scenarios in different grids.
- Spatial Heat Anomaly C describes a 2021-2025 matching-season pattern. It is not a forecast
  for the next month and does not substitute for event-period station or forecast data.
- Outdoor temperature is held common across effective-cooling and no-effective-cooling
  states; it is a background modifier and not the earthquake treatment contrast.
- Estimated Affected Population Age 65+ is a cooling-assessment population, not confirmed
  loss of cooling. Effective placement is subtracted only with time-compatible verified or
  explicitly scenario-based capacity.
- When Effective Cooled Capacity or placement is missing, Cooling Capacity Gap and
  Unprotected Older-Person-Days remain missing. The no-placement case is reported only as a
  conservative demand-side bound.
- Cooling Load Density W per m2, Scenario Cooling System COP, Scenario Peak Load Diversity
  Factor, and Scenario Cooling Operating Hours per Day vary jointly in the approved Low,
  Central, and High bundles. All use the same central assessment population. Grid power,
  backup power, and non-cooling critical load remain missing rather than being set to zero.
- Cooling-Loss-Related Incremental Mortality Risk Distribution uses a direct published
  cooled-versus-uncooled high-heat contrast, not a general outdoor temperature-mortality
  coefficient. Expected High-Heat Scenario Days are a five-year matching-period background,
  not a forecast. The 95% limits vary only the published relative-odds parameter and omit
  housing-loss, baseline-rate, heat-scenario, placement, and cross-population transfer
  uncertainty.

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
| 11. Construct epicentral-distance and exposure weights | Epicentral Distance km, General Households, Mapped Building Count, Mapped Building Footprint Area m2 | \(h_{g,\lambda}\) and \(q_{g,s}\) across three decay scales and three exposure proxies | Functional Housing Loss and Older-Person Exposure | Structural residence loss is more plausibly concentrated near the epicenter and where residential exposure is present | Supported only as a transparent scenario assumption; no causal distance coefficient or building fragility is identified |
| 12. Construct structural residence-loss totals | Full Collapse Buildings, Half Collapse Buildings, Structural Housing Loss Central Total Residences, Half-Collapse Functional Loss Weight Set | \(T_s=F+\theta_sH\), with partial damage excluded | Functional Housing Loss and Older-Person Exposure | Official structural damage totals can constrain an early functional-loss nowcast without treating all damage categories as uninhabitable | Partially supported; functional loss among half-collapse residences remains scenario-dependent |
| 13. Allocate expected structural residence loss | Housing Loss Allocation Weight, Expected Functionally Lost Residences, Expected Functionally Lost Residences Lower Bound, Expected Functionally Lost Residences Upper Bound, Functional Housing Loss Status, Damage Evidence Cutoff | \(L_{g,s}=T_sq_{g,s}\), ensemble-median central allocation, and pointwise scenario range | Functional Housing Loss and Older-Person Exposure | Expected structural residence loss is spatially heterogeneous within Kumamoto Prefecture | Supported as a model-based scenario allocation, not as observed grid damage |
| 14. Preserve confirmed evidence at reported geography | Confirmed Functionally Lost Residences, Municipality, Functional Housing Loss Status, Evidence Tier, Verification Status | No grid allocation without geolocation; contextual geography and evidence class retained | Functional Housing Loss and Older-Person Exposure | Confirmed or reported lower-bound evidence must remain separate from modeled expected loss | Supported at reported geography; current disclosure-group confirmed count remains unavailable |
| 15. Estimate older-person exposure associated with structural residence loss | General Households, Population Age 65+, Estimated Affected Population Age 65+, Estimated Affected Population Age 65+ Lower Bound, Estimated Affected Population Age 65+ Upper Bound | \(E[N_{a,g}]=N_{a,g}\min(1,E[L_g]/G_g)\) and pointwise scenario bounds | Functional Housing Loss and Older-Person Exposure | Older residents associated with modeled structural residence loss are spatially heterogeneous | Supported only as proportional occupancy exposure; not observed displacement or shelter demand |
| 16. Construct the cooling-protection assessment population | Estimated Affected Population Age 65+, Estimated Affected Population Age 65+ Lower Bound, Estimated Affected Population Age 65+ Upper Bound, Cooling Loss Confirmed | \(N^{need}_{g,t}=E[N_{65+,g}]\), with housing-scenario bounds and no claim of observed displacement | Older-Person Cooling Protection Need and Placement Deficit | Structural residence loss identifies older residents who require a cooling assessment, not everyone already proven uncooled | Supported as a conservative demand-side screening population; cooling-loss status remains partly unknown |
| 17. Allocate effective cooled placement and calculate the residual deficit | Current Shelter Occupancy, Available Cooled Floor Area m2, HVAC Cooling Capacity kW Thermal, Effective Cooled Capacity, Cooling Capacity Gap, Unprotected Older-Person-Days, Verification Status | Capacity-constrained assignment \(x_{g,s,t}\), \(U_{g,t}=\max(0,N^{need}_{g,t}-\sum_sx_{g,s,t})\), and \(PD_g=\sum_tU_{g,t}\) | Older-Person Cooling Protection Need and Placement Deficit | Correct placement can restore the cooling protection lost with housing function | Inconclusive until time-stamped effective capacity and placement are verified; a no-placement upper bound may be shown separately |
| 18. Estimate demand-side electricity required for protective cooling | Estimated Affected Population Age 65+, Power Demand Scenario, Minimum Shelter Living Area m2 per Person, Cooling Load Density W per m2, Cooling Thermal Load W per Person, Scenario Cooling System COP, Scenario Peak Load Diversity Factor, Scenario Cooling Operating Hours per Day, Cooling Thermal Load kW, Required Peak Cooling Electric Power kW, Required Daily Cooling Electricity kWh, Cooling Power Scenario Status, Municipality | \(q_z=a r_z\), \(Q_{g,z}=N^{need}_gq_z/1000\), \(P^{req}_{g,z}=Q_{g,z}f_z/COP_z\), and \(E^{req}_{g,z}=P^{req}_{g,z}h_z\) | Emergency Cooling Electricity Requirement Distribution | Emergency cooling-energy planning should be tied to the spatial distribution of older residents requiring cooling assessment | Supported as a Low/Central/High demand-side planning scenario; actual available power and the emergency power gap remain unidentified |
| 19. Estimate the cooled-versus-uncooled one-month health-risk contrast | No-Placement Unprotected Older-Person-Days, Expected High-Heat Scenario Days, Baseline Mortality Rate per 100,000, Baseline Daily Mortality Probability, Effective-Cooling High-Heat Daily Mortality Probability, No-Effective-Cooling Relative Odds Ratio, Effective-Cooling 30-Day Mortality Risk, No-Effective-Cooling 30-Day Mortality Risk, Cooling-Loss Relative 30-Day Mortality Burden Increase %, Cooling-Loss Incremental Mortality Risk per 100,000, Incremental Cooling-Loss-Related Excess Deaths | \(M_m=100(r^{no\ cool}_m/r^{cool}_m-1)\), \(R_m=100000(r^{no\ cool}_m-r^{cool}_m)\), and \(\Delta D_m=(PD^{NP}_m/H)(r^{no\ cool}_m-r^{cool}_m)\), holding outdoor weather fixed | Cooling-Loss-Related Incremental Mortality Risk Distribution | Failure to restore cooling may increase mortality risk even when the outdoor weather itself is unchanged by the earthquake | Supported only as a literature-anchored, no-verified-placement planning scenario; daily risk accumulates across high-heat days, but no unestimated nonlinear duration-response multiplier is imposed |
| 20. Aggregate completed planning results by municipality | Municipality, Expected Functionally Lost Residences, Expected Functionally Lost Residences Lower Bound, Expected Functionally Lost Residences Upper Bound, Estimated Affected Population Age 65+, Estimated Affected Population Age 65+ Lower Bound, Estimated Affected Population Age 65+ Upper Bound, No-Placement Unprotected Older-Person-Days, Expected High-Heat Scenario Days, Power Demand Scenario, Required Peak Cooling Electric Power kW, Required Daily Cooling Electricity kWh, Incremental Cooling-Loss-Related Excess Deaths, Cooling-Loss Relative 30-Day Mortality Burden Increase %, Cooling-Loss Relative 30-Day Mortality Burden Increase % Lower 95% CI, Cooling-Loss Relative 30-Day Mortality Burden Increase % Upper 95% CI | Municipality sum \(X_m=\sum_{g\in\mathcal{G}_m}X_g\), Central power-scenario selection, and descending ordering by central Estimated Affected Population Age 65+ | Municipality-Level Housing Loss, Cooling Demand, and Health-Risk Summary | Operational prioritization should jointly consider modeled structural loss, older-person cooling demand, electricity requirements, and relative health burden | Supported as an evidence-constrained municipality planning comparison; no actual placement, verified supply, or power gap is claimed |

The checkpoint closes the demand-side cooling-power chain and adds a literature-anchored
health-planning scenario, but it does not identify operational supply or actual mortality
effects. The completed screening, ambient-heat, and structural residence-loss outputs
identify where older residents may require cooling assessment. Approved engineering bundles
support peak-power and daily-energy planning scenarios. Effective cooled capacity, actual
placement, observed unprotected person-days, and verified power supply remain non-final.
Mortality is evaluated last as a no-verified-placement cooled-versus-uncooled scenario under
identical historical-background outdoor weather.

## 8. Figure and Table Plan

The planned output set links the completed population, operational screening, ambient-heat,
and structural residence-loss figures to a cooling-protection decision chain. Outdoor heat
is held as a common background condition: the earthquake-related contrast is effective
cooling versus loss of effective cooling. The MODIS-based output characterizes historical
spatial heat heterogeneity; it is not a weather forecast or indoor-temperature estimate.

### Figures

| title | what it expresses | figure type | subpanels | key variables | status |
|---|---|---|---:|---|---|
| Kumamoto Population and Older-Age Vulnerability Baseline | Establishes the prefecture-wide population baseline and spatial concentration of older residents before linking earthquake loss and heat exposure. | map | 2 | Total Population, Population Age 65+ Share, Population Age 65+, Municipality | done |
| Minami Ward Shelter and Cooling Risk Screening | Locates older residents, designated shelters, the reported Tomiai/Jonan damage concentration, verified unavailable facilities, and changing evacuation and water-outage observations without estimating a numerical cooling-capacity deficit. | map and line | 2 | Population Age 65+, Latitude, Longitude, Facility Name, Observation Time, Observed Evacuee Count, Observed Water Outage Households, Cooling Loss Confirmed, Habitability Status, Heat Protection Loss Mechanism, Evidence Tier, Verification Status | done |
| Event-Window Daytime and Nighttime Heat Scenario | Compares observed 2026 daytime and nighttime station temperatures with the matching 2021-2025 historical scenario while distinguishing complete and partial event days; the historical continuation is a scenario, not a weather forecast. | line | 2 | Station Name, Observation Date, Historical Year, Scenario Date, Event Day, Daily Maximum Air Temperature C, Daily Minimum Air Temperature C, Hot Day Indicator, Hot Night Indicator, Daily Observation Completeness %, Daily Record Status | done |
| Historical MODIS and Station-Calibrated Heat Spatial Heterogeneity | Uses matching-period historical MODIS daytime and nighttime land-surface temperature together with historical station air temperature to estimate a station-calibrated spatial heat pattern for Kumamoto Prefecture. | map | 6 | Historical Daytime Land Surface Temperature C, Historical Nighttime Land Surface Temperature C, MODIS Valid Observation Count, Station-Calibrated Historical Air Temperature C, Spatial Heat Anomaly C, Interpolation Uncertainty C | done |
| Functional Housing Loss and Older-Person Exposure | Separates confirmed residence-loss evidence at its reported geography from the epicentral-distance structural residence-loss scenario and the associated older-person exposure estimate; modeled values are not observed damage or displacement. | map | 3 | Epicentral Distance km, Functional Housing Loss Status, Confirmed Functionally Lost Residences, Expected Functionally Lost Residences, Expected Functionally Lost Residences Lower Bound, Expected Functionally Lost Residences Upper Bound, Estimated Affected Population Age 65+, Estimated Affected Population Age 65+ Lower Bound, Estimated Affected Population Age 65+ Upper Bound, Estimation Status, Damage Evidence Cutoff | done |
| Older-Person Cooling Protection Need and Placement Deficit | Maps the modeled older-person cooling-assessment population, a 30-day no-verified-placement demand-side bound, and nominal designated-shelter access. The early planning version does not treat unverified capacity as zero and does not claim an observed placement deficit. | map | 3 | Estimated Affected Population Age 65+, Estimated Affected Population Age 65+ Lower Bound, Estimated Affected Population Age 65+ Upper Bound, No-Placement Unprotected Older-Person-Days, No-Placement Unprotected Older-Person-Days Lower Bound, No-Placement Unprotected Older-Person-Days Upper Bound, Nearest Designated Shelter Distance m, Cooling Protection Scenario Status, Damage Evidence Cutoff | done |
| Emergency Cooling Electricity Requirement Distribution | Maps Central-scenario municipality peak cooling power and daily cooling electricity using distinct unit-specific color scales, then compares prefecture totals across approved Low, Central, and High demand-side scenarios. It does not estimate available supply or an actual power gap. | map and bar | 3 | Estimated Affected Population Age 65+, Municipality, Power Demand Scenario, Minimum Shelter Living Area m2 per Person, Cooling Load Density W per m2, Cooling Thermal Load W per Person, Scenario Cooling System COP, Scenario Peak Load Diversity Factor, Scenario Cooling Operating Hours per Day, Cooling Thermal Load kW, Required Peak Cooling Electric Power kW, Required Daily Cooling Electricity kWh, Cooling Power Scenario Status | done |
| Cooling-Loss-Related Incremental Mortality Risk Distribution | Maps five-year matching-period high-heat days, the literature-anchored absolute risk difference from losing effective cooling, and the relative increase in 30-day mortality burden under the no-verified-placement demand-side bound. Outdoor weather is fixed across cooling states; absolute expected deaths remain available for the municipality table rather than the figure. | map | 3 | Expected High-Heat Scenario Days, No-Placement Unprotected Older-Person-Days, Baseline Mortality Rate per 100,000, Baseline Daily Mortality Probability, Effective-Cooling High-Heat Daily Mortality Probability, No-Effective-Cooling Relative Odds Ratio, No-Effective-Cooling Relative Odds Ratio Lower 95% CI, No-Effective-Cooling Relative Odds Ratio Upper 95% CI, Effective-Cooling 30-Day Mortality Risk, No-Effective-Cooling 30-Day Mortality Risk, Cooling-Loss Relative 30-Day Mortality Burden Increase %, Cooling-Loss Relative 30-Day Mortality Burden Increase % Lower 95% CI, Cooling-Loss Relative 30-Day Mortality Burden Increase % Upper 95% CI, Cooling-Loss Incremental Mortality Risk per 100,000, Cooling-Loss Incremental Mortality Risk per 100,000 Lower 95% CI, Cooling-Loss Incremental Mortality Risk per 100,000 Upper 95% CI, Cooling-Loss Mortality Scenario Status | done |

### Tables

| title | what it expresses | rows | columns | row meaning | column meaning | status |
|---|---|---:|---:|---|---|---|
| Municipality Housing Loss and Older-Person Cooling Need Summary | Compares modeled structural residence loss and the associated older population requiring cooling assessment while retaining compact scenario ranges. | 45 | 6 | one municipality, sorted by central Estimated Affected Population Age 65+ in descending order | Municipality; central Expected Functionally Lost Residences; compact lower-to-upper Expected Functionally Lost Residences scenario range; central Estimated Affected Population Age 65+; compact lower-to-upper Estimated Affected Population Age 65+ scenario range; No-Placement Unprotected Older-Person-Days | done |
| Municipality Cooling Electricity Planning Summary | Translates the older-person cooling-assessment population into Central-scenario peak power and daily electricity requirements under the common historical heat scenario. | 45 | 6 | one municipality, sorted by central Estimated Affected Population Age 65+ in descending order | Municipality; Estimated Affected Population Age 65+; No-Placement Unprotected Older-Person-Days; Expected High-Heat Scenario Days; Central Required Peak Cooling Electric Power kW; Central Required Daily Cooling Electricity kWh | done |
| Municipality Cooling-Loss Health-Risk Summary | Compares the literature-anchored 30-day health-risk contrast across municipalities without treating the scenario as observed or earthquake-attributable mortality. | 45 | 6 | one municipality, sorted by central Cooling-Loss Relative 30-Day Mortality Burden Increase % in descending order | Municipality; Expected High-Heat Scenario Days; Incremental Cooling-Loss-Related Excess Deaths; central, lower, and upper Cooling-Loss Relative 30-Day Mortality Burden Increase % | done |

The three compact municipality tables use final scenario variables only and replace the
previous 15-column combined workbook. Each table contains exactly six columns and serves a
single decision stage. Housing-loss and affected-older-person lower and upper values are
combined into readable scenario-range fields; the underlying endpoints are sums of
pointwise grid bounds and are not jointly realized municipality confidence intervals.
No-Placement Unprotected Older-Person-Days remains a demand-side planning bound rather than
observed exposure. Electricity columns report Central demand only. The health-effect limits
vary only the published cooling-effect parameter. Unverified placement, effective cooled
capacity, available electric supply, and power gaps remain deferred and are not represented
by blank or zero-valued columns.

### Deferred Outputs Required for the Full Research Objective

- A shelter-level effective cooled-capacity deficit table remains deferred until verified
  cooling equipment, backup power, usable cooled space, occupancy, and accessibility inputs
  are acquired and confirmed in Section 4.
- A building-loss calibration and validation output remains deferred until geolocated
  official inspection or damage-certificate labels become available.
- The mortality map is a completed analytical draft only after user review. It uses the
  no-verified-placement demand-side bound and a transferred cooled-versus-uncooled effect;
  actual mortality impact remains deferred until event-period placement, cooling status,
  and individual exposure are verified.
- Electricity recommendations remain demand-side scenarios until cooling equipment,
  coefficient of performance, operating hours, existing grid availability, and backup-
  power capacity are verified. Required peak power in kW and daily energy in kWh must remain
  separate quantities.

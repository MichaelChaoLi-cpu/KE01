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

- Data sources reviewed: 17
- Variables summarized: 187
- Distribution plots generated: 80
- Files skipped during briefing: 2

| Data source | Rows | Columns |
| --- | ---: | ---: |
| Data source 1 | 1315 | 10 |
| Data source 2 | 1713 | 16 |
| Data source 3 | 36657 | 19 |
| Data source 4 | 62945 | 10 |
| Data source 5 | 66 | 8 |
| Data source 6 | 7 | 9 |
| Data source 7 | 4 | 13 |
| Data source 8 | 2045 | 9 |
| Data source 9 | 7671 | 9 |
| Data source 10 | 2910 | 13 |
| Data source 11 | 11 | 8 |
| Data source 12 | 2910 | 9 |
| Data source 13 | 18 | 11 |
| Data source 14 | 2910 | 13 |
| Data source 15 | 1315 | 10 |
| Data source 16 | 1713 | 16 |
| Data source 17 | 46 | 4 |

### Time-Series Candidates

Potential time-series structure was detected in 2 data source(s).
Specific source files and original column names remain in the data-briefing artifacts, not in AnaSOP.

### Data Limitations

- 2 file(s) were skipped during briefing; see the data-briefing artifacts for technical details.
- Treat this section as exploratory; final variable decisions belong to Section 4.
- AnaSOP intentionally avoids raw dataset names, source file paths, and original column names.
## 4. Variable Construction  /  Key Variables

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

# AnaSOP

Analysis Standard Operating Procedure

## 1. Research Objective

### Central Research Question

During the first 30 days after the 2026 Kumamoto earthquake, where are older
residents most likely to lose effective home cooling because of structural
housing loss, how much emergency cooling electricity would be required to
protect them, and how large is the planning-level mortality-risk contrast if
effective cooling is not restored?

The earthquake is not assumed to change outdoor weather. The analytical
contrast is effective cooling versus loss of effective cooling under the same
outdoor heat scenario.

### Operational Questions

1. Where are population and residents age 65 or older concentrated across
   Kumamoto Prefecture, and what early shelter or service interruptions are
   documented?
2. How can official prefecture residence-damage totals be allocated to small
   areas without claiming that individual buildings were identified as
   collapsed?
3. How many residents age 65 or older are associated with the modeled housing
   loss, and what is the 30-day demand-side bound if no effective cooled
   placement is verified?
4. How spatially heterogeneous is matching-season heat, and how much peak
   power, daily electricity, and incremental mortality risk are implied by the
   approved planning scenarios?

### Scope

- Event: Kumamoto earthquake beginning 2026-07-28.
- Geography: Kumamoto Prefecture; operational detail is additionally shown for
  Kumamoto City Minami Ward.
- Small-area unit: 36,657 official population disclosure groups derived from
  populated 125 m census meshes.
- Reporting unit: 45 municipalities after consolidating the five Kumamoto City
  wards for mortality and summary tables.
- Population: residents age 65 or older are the primary protection group.
- Planning horizon: 30 days.
- Historical heat reference: matching 30-day calendar periods in 2021-2025.
- Damage cutoff used by the modeled allocation: 2026-08-01 17:00 JST.
- Event heat observations currently used: 2026-07-28 through 2026-08-03.

### Study Design Declaration

- Research type: applied

This is an applied, evidence-constrained scenario study. It combines observed
official context with transparent model-based allocations. It does not identify
individual destroyed buildings, observe displacement, verify shelter cooling
capacity, estimate available electricity supply, or identify
earthquake-attributable deaths.

## 2. Theoretical Background  /  Conceptual Framework  /  Problem Formulation

### Mechanism

The implemented mechanism is:

earthquake and ground effects -> structural housing loss -> loss of usable home
cooling -> older-person-days without verified cooled placement -> emergency
cooling and electricity demand -> higher mortality risk if cooling is not
restored.

Outdoor temperature is common to the protected and unprotected states. Heat
modifies the consequence of cooling loss; it is not the earthquake treatment.

### Evidence Architecture

The study separates three evidence classes:

1. **Observed context:** census population, official damage reports, shelter
   locations, service interruptions, JMA temperatures, and historical mortality.
2. **Modeled spatial allocation:** structural residence loss and associated older
   population distributed across disclosure groups using explicit assumptions.
3. **Planning scenarios:** no-verified-placement person-days, cooling electricity
   demand, and a literature-anchored cooled-versus-uncooled mortality contrast.

Modeled values never replace confirmed observations. Aerial photographs are not
used to label collapsed houses because the available vertical imagery cannot
reliably distinguish damage for typical Japanese buildings at the available
resolution.

### Decision Use

The outputs identify places that should receive priority assessment and cooling
resources. They do not establish actual shelter deficits. A verified operational
deficit would additionally require current placement, usable cooled floor area,
functioning HVAC, backup power, and available grid supply, none of which is in the
final analytical dataset.

## 3. Data Overview

The final data sources and their analytical scope are restricted to components
actually consumed by a completed figure, table, or estimation stage.

### Data Actually Used

| data component | source and coverage | analysis unit | records used | final role |
|---|---|---|---:|---|
| Population and boundaries | 2020 Population Census and e-Stat small-area geography | populated 125 m mesh / disclosure group | 62,945 meshes; 36,657 groups | population baseline, older-person exposure, municipality assignment |
| Mapped buildings | GSI vector-map building polygons, 2026-04-01 release | building polygon | 1,036,590 | building-count and footprint exposure proxies for housing-loss allocation |
| Designated shelters | GSI designated-shelter release available during the response | facility point | 1,315 | nominal shelter access and Minami Ward screening |
| Official housing damage | time-stamped government reports through 2026-08-01 | prefecture or reported subarea | 5 snapshots | constrains structural residence-loss totals |
| Damage evidence | official geolocated or geographically bounded claims through 2026-08-02 | evidence claim | 9 | contextual confirmed/probable evidence only |
| Service disruption | official shelter occupancy, water, and cooling-related reports through 2026-08-02 | time-stamped observation | 14 | Minami Ward operational screening |
| Event heat | JMA daily summaries for five stations, 2026-07-28 to 2026-08-03 | station-day | 35 | observed event-window daytime and nighttime heat |
| Historical event-window heat | JMA matching dates for the same five event stations, 2021-2025 | station-year-day | 750 | 30-day pooled historical median and observed envelope |
| Historical spatial heat | JMA matching dates for 17 stations, 2021-2025 | station-year-day | 2,550 | spatial calibration and municipality high-heat days |
| MODIS surface heat | Terra MOD11A2 and Aqua MYD11A2 eight-day LST, matching periods in 2021-2025 | approximately 1 km pixel | 8,661 pixels from 80 source files | historical daytime/nighttime heat heterogeneity |
| Mortality baseline | official all-cause deaths for 2020-2024 and 2020 population | municipality-age group | 135; the 45 age-65-plus rows are used | baseline mortality probability |
| Cooling engineering parameters | Japanese shelter-space, HVAC-load, and efficiency guidance | scenario bundle | Low, Central, High | peak power and daily electricity demand |
| Cooling effect | Katz et al. (2025), JAMA Internal Medicine | published effect estimate | one central estimate and 95% CI | no-cooling versus cooling mortality contrast |

### Analysis Products Used by the Results

| analytical product | rows | role |
|---|---:|---|
| Population disclosure-group exposure grid | 36,657 | housing-loss allocation and older-person exposure |
| No-verified-placement cooling-need grid | 36,657 | 30-day demand-side person-day bound |
| Cooling-electricity scenario grid | 109,971 | three parameter bundles for every disclosure group |
| Municipality cooling-loss mortality scenario | 45 | high-heat days and 30-day risk contrast |

### Reconciliation Anchors

- The 2020 population baseline contains 1,738,301 residents, including 540,538
  residents age 65 or older.
- The latest usable prefecture snapshot reports 181 full-collapse and 245
  half-collapse residences. The central functional-loss total is therefore
  303.5 residences.
- The central modeled population age 65 or older associated with structural
  housing loss is 245.79 people, equivalent to 7,373.81 person-days over 30 days
  under the no-verified-placement bound.
- Prefecture cooling demand totals are 21.85, 34.58, and 48.52 kW peak power and
  262.21, 622.50, and 1,164.47 kWh per day for the Low, Central, and High
  scenarios, respectively.
- Municipality expected high-heat days range from 0.36 to 23.61. The central
  cooling-loss relative 30-day mortality-burden increase ranges from 0.10% to
  6.32%; the summed central incremental-death scenario is 0.04380.

These values are reproducibility checks, not observed impact totals. Grid lower
and upper bounds are pointwise scenario bounds and must not be summed and
interpreted as one jointly realized prefecture interval.

### Data Limitations

- The 2020 census predates the event and does not capture 2026 population change.
- Official damage totals are not geolocated to disclosure groups.
- Shelter presence does not verify opening, occupancy, cooled capacity, or power.
- MODIS land-surface temperature is not air or indoor temperature.
- The mortality effect is transferred from older institutional residents outside
  Japan; its reported interval covers only effect-parameter uncertainty.

## 4. Variable Construction  /  Key Variables

All variables below are final variables used in at least one completed figure or
table.

### Population, Geography, and Observed Context

| readable variable | role | construction and interpretation | is_final_variable |
|---|---|---|---|
| Municipality | linkage | 45-unit reporting geography; Kumamoto City wards are consolidated where required | yes |
| Total Population | denominator | 2020 Census population in a populated mesh or disclosure group | yes |
| Population Age 65+ | vulnerability | official age-65-or-older count at the disclosure geography | yes |
| Population Age 65+ Share | vulnerability | Population Age 65+ divided by Total Population | yes |
| General Households | exposure denominator | official general-household count | yes |
| Mapped Building Count | exposure proxy | unique mapped building polygons assigned by representative point; not dwelling or damage counts | yes |
| Mapped Building Footprint Area m2 | exposure proxy | summed mapped building footprint area | yes |
| Nearest Designated Shelter Distance m | access context | straight-line distance to the nearest designated shelter | yes |
| Observation Time | time index | timestamp of an official damage, occupancy, or service observation | yes |
| Observed Evacuee Count | observed context | reported public-shelter occupants at the stated geography and time | yes |
| Observed Water Outage Households | observed context | reported households without water service | yes |
| Cooling Loss Confirmed | observed context | direct evidence that cooling was unavailable at a reported facility or location | yes |

### Housing Loss and Older-Person Exposure

| readable variable | role | construction and interpretation | is_final_variable |
|---|---|---|---|
| Full Collapse Buildings | scenario total input | latest official prefecture full-collapse count | yes |
| Half Collapse Buildings | scenario total input | latest official prefecture half-collapse count | yes |
| Epicentral Distance km | hazard proxy | straight-line distance from disclosure-group representative point to 32.6 N, 130.7 E | yes |
| Expected Functionally Lost Residences | primary modeled outcome | central total-constrained structural residence-loss allocation | yes |
| Expected Functionally Lost Residences Lower Bound | sensitivity | pointwise minimum across 27 allocation scenarios | yes |
| Expected Functionally Lost Residences Upper Bound | sensitivity | pointwise maximum across 27 allocation scenarios | yes |
| Estimated Affected Population Age 65+ | primary exposure | age-65-or-older population multiplied by the central modeled housing-loss share | yes |
| Estimated Affected Population Age 65+ Lower Bound | sensitivity | exposure calculated from the pointwise lower housing-loss share | yes |
| Estimated Affected Population Age 65+ Upper Bound | sensitivity | exposure calculated from the pointwise upper housing-loss share | yes |
| Damage Evidence Cutoff | time index | latest official damage snapshot used by the allocation | yes |

### Heat

| readable variable | role | construction and interpretation | is_final_variable |
|---|---|---|---|
| Daily Maximum Air Temperature C | observed heat | JMA station daily maximum | yes |
| Daily Minimum Air Temperature C | observed heat | JMA station daily minimum | yes |
| Hot Day Indicator | threshold | one when daily maximum is at least 35 C | yes |
| Hot Night Indicator | threshold | one when daily minimum is at least 25 C | yes |
| Historical Daytime Land Surface Temperature C | spatial covariate | strict-QA equal-weight Terra/Aqua daytime LST mean | yes |
| Historical Nighttime Land Surface Temperature C | spatial covariate | strict-QA equal-weight Terra/Aqua nighttime LST mean | yes |
| Coverage-Optimized Historical Daytime Land Surface Temperature C | display covariate | strict-QA daytime value when available, otherwise relaxed-QA value; no spatial gap filling | yes |
| Coverage-Optimized Historical Nighttime Land Surface Temperature C | display covariate | strict-QA nighttime value when available, otherwise relaxed-QA value; no spatial gap filling | yes |
| Station-Calibrated Historical Air Temperature C | modeled heat | cross-validated station-calibrated surface retained only when it improves on the mean-only benchmark | yes |
| Interpolation Uncertainty C | uncertainty | selected leave-one-station-out RMSE combined with surface sensitivity | yes |
| Expected High-Heat Scenario Days | heat modifier | five-year mean days meeting either hot-day or hot-night threshold, interpolated to municipality centroids | yes |

### Cooling and Electricity

| readable variable | role | construction and interpretation | is_final_variable |
|---|---|---|---|
| No-Placement Unprotected Older-Person-Days | demand bound | Estimated Affected Population Age 65+ multiplied by 30 days | yes |
| Power Demand Scenario | sensitivity | Low, Central, or High engineering parameter bundle | yes |
| Minimum Shelter Living Area m2 per Person | parameter | fixed at 3.5 m2 per person | yes |
| Cooling Load Density W per m2 | parameter | 127, 134, or 141 W/m2 | yes |
| Scenario Cooling System COP | parameter | 4.0, 3.0, or 2.5 | yes |
| Scenario Peak Load Diversity Factor | parameter | 0.8, 0.9, or 1.0 | yes |
| Scenario Cooling Operating Hours per Day | parameter | 12, 18, or 24 hours | yes |
| Required Peak Cooling Electric Power kW | planning outcome | demand-side peak electricity required for cooling | yes |
| Required Daily Cooling Electricity kWh | planning outcome | peak power multiplied by operating hours | yes |

### Mortality Scenario

| readable variable | role | construction and interpretation | is_final_variable |
|---|---|---|---|
| Baseline Mortality Rate per 100,000 | baseline | pooled 2020-2024 age-65-plus deaths divided by five times the fixed 2020 population | yes |
| Baseline Daily Mortality Probability | baseline | annualized baseline rate converted to a daily probability | yes |
| Effective-Cooling High-Heat Daily Mortality Probability | protected state | baseline odds multiplied by the published with-cooling extreme-heat odds ratio | yes |
| No-Effective-Cooling Relative Odds Ratio | effect | 1.08, with 95% CI 1.01 to 1.15, comparing no cooling with cooling | yes |
| No-Effective-Cooling Relative Odds Ratio Lower 95% CI | effect uncertainty | lower published no-cooling versus cooling effect limit | yes |
| No-Effective-Cooling Relative Odds Ratio Upper 95% CI | effect uncertainty | upper published no-cooling versus cooling effect limit | yes |
| Effective-Cooling 30-Day Mortality Risk | protected outcome | cumulative 30-day risk with cooling on expected high-heat days | yes |
| No-Effective-Cooling 30-Day Mortality Risk | unprotected outcome | cumulative 30-day risk without cooling on expected high-heat days | yes |
| Cooling-Loss Incremental Mortality Risk per 100,000 | absolute contrast | difference between unprotected and protected 30-day risks per 100,000 | yes |
| Cooling-Loss Relative 30-Day Mortality Burden Increase % | relative contrast | relative increase in unprotected versus protected 30-day risk | yes |
| Cooling-Loss Relative 30-Day Mortality Burden Increase % Lower 95% CI | effect uncertainty | relative burden using the lower cooling-effect limit | yes |
| Cooling-Loss Relative 30-Day Mortality Burden Increase % Upper 95% CI | effect uncertainty | relative burden using the upper cooling-effect limit | yes |
| Incremental Cooling-Loss-Related Excess Deaths | planning magnitude | absolute risk difference multiplied by the no-placement population equivalent | yes |

Variables intentionally excluded from final estimation are actual placement,
effective cooled capacity, indoor temperature, verified available electricity,
emergency power gap, and individual health outcomes.

## 5. Identification Strategy

### Design Principle

The study identifies no causal earthquake mortality effect. It produces an
auditable planning chain in which every modeled output is constrained by an
observed total or an explicit scenario parameter. Observed evidence, spatial
allocation, engineering demand, and health-risk transfer are reported as
separate stages.

The Section 4 variables and inputs provide the readable, final quantities used
at every stage below; variables excluded in Section 4 are not introduced into
the identification strategy.

### Stage-Specific Strategy

1. **Baseline and operational context:** census population, shelter locations,
   damage claims, shelter occupancy, and service interruptions are described
   without imputation.
2. **Heat context:** event JMA measurements are compared with matching 2021-2025
   observations. MODIS supplies historical spatial heterogeneity only.
3. **Housing-loss allocation:** official full- and half-collapse totals are
   distributed across disclosure groups using 27 combinations of exposure proxy,
   distance decay, and half-collapse weight.
4. **Cooling demand:** the affected age-65-plus population is treated as a
   cooling-assessment population. The 30-day no-placement value is a demand-side
   bound, not an observed deficit.
5. **Electricity demand:** Low, Central, and High parameter bundles estimate
   required power; available supply is not estimated.
6. **Health contrast:** identical outdoor heat is applied to effective-cooling
   and no-effective-cooling states. A published relative odds ratio supplies the
   only between-state effect.

### Interpretation Limits

The housing allocation is a nowcast, not building classification. Population
exposure is not displacement. Nominal shelter access is not effective placement.
Power estimates are demand, not shortages. Mortality estimates are transferable
planning scenarios, not observed or earthquake-attributable deaths.

## 6. Main Estimation Framework

### Structural Housing-Loss Allocation

For disclosure group \(g\), exposure proxy \(k\), and decay scale \(\lambda\), the
unnormalized and normalized spatial weights are:

\[
w_{g,k,\lambda}=E_{g,k}\exp(-d_g/\lambda), \qquad
q_{g,k,\lambda}=\frac{w_{g,k,\lambda}}{\sum_j w_{j,k,\lambda}}.
\]

\(w_{g,k,\lambda}\) is the unnormalized spatial weight and
\(q_{g,k,\lambda}\) is the corresponding normalized allocation share.
\(E_{g,k}\) is General Households, Mapped Building Count, or Mapped Building
Footprint Area \(\mathrm{m}^2\); \(d_g\) is Epicentral Distance \(\mathrm{km}\);
\(\lambda\) is the decay scale; and \(j\) indexes disclosure groups in the
normalizing sum. The evaluated values of \(\lambda\) are \(10\), \(20\), and
\(40\,\mathrm{km}\).

For half-collapse weight \(\theta\), scenario total and group allocation are:

\[
T_{\theta}=F+\theta H, \qquad
L_{g,k,\lambda,\theta}=T_{\theta}q_{g,k,\lambda}.
\]

\(T_{\theta}\) is the scenario-wide structural residence-loss total and
\(L_{g,k,\lambda,\theta}\) is the amount allocated to disclosure group \(g\).
\(F\) is Full Collapse Buildings, \(H\) is Half Collapse Buildings, and
\(\theta\) is \(0\), \(0.5\), or \(1\). The 27 scenarios are the Cartesian
product of three exposure proxies, three decay scales, and three values of
\(\theta\). The central
surface is the normalized pointwise median constrained to
\(F+0.5H=303.5\). Pointwise minima and maxima form the displayed sensitivity
bounds.

The central affected older population is:

\[
N^{\mathrm{need}}_{65{+},g}
=N_{65{+},g}\min\left(1,\frac{L_g}{G_g}\right).
\]

\(N^{\mathrm{need}}_{65{+},g}\) is Estimated Affected Population Age 65+;
\(N_{65{+},g}\) is Population Age 65+; \(L_g\) is Expected Functionally Lost
Residences; and \(G_g\) is General Households. Lower and upper values substitute
the corresponding pointwise housing-loss bounds.

### Heat Scenario and Spatial Calibration

A high-heat day is defined as:

\[
I_{s,y,t}
=\mathbf{1}\!\left\{
T^{\max}_{s,y,t}\geq 35\ \text{or}\ T^{\min}_{s,y,t}\geq 25
\right\}.
\]

\(I_{s,y,t}\) is the high-heat indicator for station \(s\), historical year \(y\),
and event-window day \(t\); \(T^{\max}_{s,y,t}\) and \(T^{\min}_{s,y,t}\) are JMA
daily maximum and minimum air temperatures. Municipality Expected High-Heat
Scenario Days are the five-year mean station counts interpolated from the four
nearest stations using inverse-distance-squared weights.

MODIS calibration candidates are compared by leave-one-station-out RMSE. The
daytime selected model combines a linear satellite term with five-neighbor
inverse-distance-squared residual interpolation (RMSE
\(0.696\,^\circ\mathrm{C}\) versus \(1.325\,^\circ\mathrm{C}\) for the
mean-only benchmark). The nighttime selected model is satellite-only (RMSE
\(0.615\,^\circ\mathrm{C}\) versus \(1.502\,^\circ\mathrm{C}\)). Both therefore
pass the pre-specified improvement rule.

### Cooling Protection and Electricity Demand

The no-verified-placement person-day bound is:

\[
PD^{\mathrm{NP}}_g=30\,N^{\mathrm{need}}_{65{+},g}.
\]

\(PD^{\mathrm{NP}}_g\) is No-Placement Unprotected Older-Person-Days and
\(N^{\mathrm{need}}_{65{+},g}\) is the cooling-assessment population defined
above.

For engineering scenario \(z\):

\[
q_z=a\,r_z, \qquad
Q_{g,z}=\frac{N^{\mathrm{need}}_{65{+},g}q_z}{1000}.
\]

\(q_z\) is cooling thermal load in \(\mathrm{W}\) per person; \(a\) is
\(3.5\,\mathrm{m}^2\) per person; \(r_z\) is Cooling Load Density in
\(\mathrm{W}/\mathrm{m}^2\); and \(Q_{g,z}\) is cooling thermal load in
\(\mathrm{kW}\).

\[
P^{\mathrm{req}}_{g,z}
=\frac{Q_{g,z}f_z}{\mathrm{COP}_z}, \qquad
E^{\mathrm{req}}_{g,z}=P^{\mathrm{req}}_{g,z}h_z.
\]

\(P^{\mathrm{req}}_{g,z}\) is Required Peak Cooling Electric Power in
\(\mathrm{kW}\); \(f_z\) is the peak diversity factor; \(\mathrm{COP}_z\) is
Scenario Cooling System COP; \(E^{\mathrm{req}}_{g,z}\) is Required Daily
Cooling Electricity in \(\mathrm{kWh}\); and \(h_z\) is daily operating hours.

The parameter bundles are:

| scenario | load density \(\mathrm{W}/\mathrm{m}^2\) | \(\mathrm{COP}\) | diversity | hours/day |
|---|---:|---:|---:|---:|
| Low | 127 | 4.0 | 0.8 | 12 |
| Central | 134 | 3.0 | 0.9 | 18 |
| High | 141 | 2.5 | 1.0 | 24 |

### Cooling-Loss Mortality Contrast

The baseline daily probability is:

\[
p_{0,m}=\frac{B_m}{100{,}000\times365.25}.
\]

\(p_{0,m}\) is Baseline Daily Mortality Probability for municipality \(m\), and
\(B_m\) is Baseline Mortality Rate per \(100{,}000\).

Define the odds transform and its inverse as
\(\operatorname{odds}(p)=p/(1-p)\) and
\(\operatorname{prob}(o)=o/(1+o)\). Protected and unprotected
high-heat daily probabilities are:

\[
p^{\mathrm{cool}}_m
=\operatorname{prob}\!\left(
1.03\,\operatorname{odds}(p_{0,m})
\right), \qquad
p^{\mathrm{no}}_m
=\operatorname{prob}\!\left[
\rho\,\operatorname{odds}\!\left(p^{\mathrm{cool}}_m\right)
\right].
\]

\(p^{\mathrm{cool}}_m\) is Effective-Cooling High-Heat Daily Mortality
Probability; \(p^{\mathrm{no}}_m\) is the no-effective-cooling probability;
\(1.03\) is the published
with-cooling extreme-heat odds ratio; and \(\rho\) is the no-cooling versus
cooling relative odds ratio, \(1.08\) with 95% CI \(1.01\) to \(1.15\).

For \(H_m\) expected high-heat days in the 30-day window:

\[
r^{\mathrm{cool}}_m
=1-(1-p_{0,m})^{30-H_m}
\left(1-p^{\mathrm{cool}}_m\right)^{H_m},
\]

\[
r^{\mathrm{no}}_m
=1-(1-p_{0,m})^{30-H_m}
\left(1-p^{\mathrm{no}}_m\right)^{H_m}.
\]

\(H_m\) is Expected High-Heat Scenario Days; \(r^{\mathrm{cool}}_m\) is
Effective-Cooling 30-Day Mortality Risk; and \(r^{\mathrm{no}}_m\) is
No-Effective-Cooling 30-Day Mortality Risk.

The reported contrasts are:

\[
M_m
=100\left(\frac{r^{\mathrm{no}}_m}{r^{\mathrm{cool}}_m}-1\right), \qquad
R_m
=100{,}000\left(r^{\mathrm{no}}_m-r^{\mathrm{cool}}_m\right).
\]

\[
\Delta D_m
=\frac{PD^{\mathrm{NP}}_m}{30}
\left(r^{\mathrm{no}}_m-r^{\mathrm{cool}}_m\right).
\]

\(M_m\) is Cooling-Loss Relative 30-Day Mortality Burden Increase %; \(R_m\) is
Cooling-Loss Incremental Mortality Risk per \(100{,}000\); \(\Delta D_m\) is
Incremental Cooling-Loss-Related Excess Deaths; and \(PD^{\mathrm{NP}}_m\) is municipality
No-Placement Unprotected Older-Person-Days. The lower and upper health scenarios
vary only \(\rho\).

### Municipality Aggregation

For additive grid outcome \(X_g\):

\[
X_m=\sum_{g\in\mathcal{G}_m}X_g.
\]

\(X_m\) is the municipality value, \(X_g\) is the disclosure-group value, and
\(\mathcal{G}_m\) is the set of groups assigned to municipality \(m\). Central
power values are selected before aggregation. Pointwise bounds remain
sensitivity endpoints rather than joint confidence intervals.

### Symbol Consistency and Interpretation Limits

The equations reuse the same symbols across stages; each new symbol is defined
when it first appears. The resulting surfaces are planning scenarios rather than
building inspections, observed displacement, verified cooling placement, power
shortages, causal earthquake effects, or observed deaths. Pointwise sensitivity
bounds and transferred effect intervals must retain their stated interpretations.

## 7. Analytical Workflow

| step | variables used | method | completed output | claim status |
|---|---|---|---|---|
| 1. Establish the vulnerability baseline | Total Population; Population Age 65+; Population Age 65+ Share; Municipality | census aggregation and mapping | Kumamoto Population and Older-Age Vulnerability Baseline | observed baseline supported |
| 2. Screen early operational conditions | Population Age 65+; Observation Time; Observed Evacuee Count; Observed Water Outage Households; Cooling Loss Confirmed | spatial overlay and time-series description | Minami Ward Shelter and Cooling Risk Screening | observed context supported; capacity deficit not identified |
| 3. Describe event-window heat | Daily Maximum Air Temperature C; Daily Minimum Air Temperature C; Hot Day Indicator; Hot Night Indicator | 2026 observations over 2021-2025 matching-date envelope | Event-Window Daytime and Nighttime Heat Scenario | station-level heat context supported; continuation is not a forecast |
| 4. Estimate historical heat heterogeneity | Historical Daytime Land Surface Temperature C; Historical Nighttime Land Surface Temperature C; Station-Calibrated Historical Air Temperature C; Interpolation Uncertainty C; Total Population | QA screening, leave-one-station-out model selection, calibrated surface and uncertainty | Historical MODIS and Station-Calibrated Heat Spatial Heterogeneity | historical spatial ranking supported; indoor heat not identified |
| 5. Allocate structural housing loss | Full Collapse Buildings; Half Collapse Buildings; Epicentral Distance km; General Households; Mapped Building Count; Mapped Building Footprint Area m2 | 27 total-constrained allocation scenarios | Functional Housing Loss and Older-Person Exposure; Municipality Housing Loss and Older-Person Cooling Need Summary | scenario nowcast supported; individual damage not identified |
| 6. Estimate older-person cooling need | Estimated Affected Population Age 65+; Nearest Designated Shelter Distance m | proportional occupancy and 30-day no-placement bound | Older-Person Cooling Protection Need and Placement Deficit; Municipality Housing Loss and Older-Person Cooling Need Summary | demand-side screening supported; actual placement deficit not identified |
| 7. Estimate electricity demand | Estimated Affected Population Age 65+; Power Demand Scenario; Minimum Shelter Living Area m2 per Person; Cooling Load Density W per m2; Scenario Cooling System COP; Scenario Peak Load Diversity Factor; Scenario Cooling Operating Hours per Day | cooling-load, COP, diversity, and operating-hour equations | Emergency Cooling Electricity Requirement Distribution; Municipality Cooling Electricity Planning Summary | demand scenarios supported; available supply and power gap not identified |
| 8. Estimate health-risk contrast | Expected High-Heat Scenario Days; Baseline Mortality Rate per 100,000; No-Effective-Cooling Relative Odds Ratio; No-Placement Unprotected Older-Person-Days | cumulative 30-day cooled-versus-uncooled risk | Cooling-Loss-Related Incremental Mortality Risk Distribution; Municipality Cooling-Loss Health-Risk Summary | literature-anchored planning contrast supported; causal event mortality not identified |

The completed evidence chain supports spatial prioritization for assessment,
cooling placement, and demand-side electricity planning. It does not close the
operational capacity or causal mortality questions because the required
placement, facility, supply, and individual-health observations are absent.
These are the workflow interpretation limits: completed outputs support
prioritization and demand planning, but not verified operational sufficiency or
causal mortality attribution.

## 8. Figure and Table Plan

### Figures

| title | what it expresses | figure type | subpanels | key variables | status |
|---|---|---|---:|---|---|
| Kumamoto Population and Older-Age Vulnerability Baseline | Population and older-age spatial baseline across Kumamoto Prefecture. | map | 2 | Total Population, Population Age 65+, Population Age 65+ Share, Municipality | done |
| Minami Ward Shelter and Cooling Risk Screening | Operational shelter, occupancy, water, and cooling context in Minami Ward. | map and line | 2 | Population Age 65+, Observation Time, Observed Evacuee Count, Observed Water Outage Households, Cooling Loss Confirmed | done |
| Event-Window Daytime and Nighttime Heat Scenario | Observed 2026 station heat against the matching 2021-2025 historical envelope. | line | 2 | Daily Maximum Air Temperature C, Daily Minimum Air Temperature C, Hot Day Indicator, Hot Night Indicator | done |
| Historical MODIS and Station-Calibrated Heat Spatial Heterogeneity | Daytime and nighttime LST, station-calibrated air temperature, and prediction uncertainty. | map | 6 | Coverage-Optimized Historical Daytime Land Surface Temperature C, Coverage-Optimized Historical Nighttime Land Surface Temperature C, Station-Calibrated Historical Air Temperature C, Interpolation Uncertainty C | done |
| Functional Housing Loss and Older-Person Exposure | Total-constrained structural housing loss and associated older-person exposure. | map | 3 | Epicentral Distance km, Expected Functionally Lost Residences, Expected Functionally Lost Residences Lower Bound, Expected Functionally Lost Residences Upper Bound, Estimated Affected Population Age 65+ | done |
| Older-Person Cooling Protection Need and Placement Deficit | Cooling-assessment population, 30-day no-placement bound, and nominal shelter access. | map | 3 | Estimated Affected Population Age 65+, No-Placement Unprotected Older-Person-Days, Nearest Designated Shelter Distance m | done |
| Emergency Cooling Electricity Requirement Distribution | Central municipality cooling demand and Low/Central/High prefecture totals. | map and bar | 3 | Municipality, Power Demand Scenario, Required Peak Cooling Electric Power kW, Required Daily Cooling Electricity kWh | done |
| Cooling-Loss-Related Incremental Mortality Risk Distribution | Expected high-heat days, absolute cooling-loss risk, and relative mortality-burden increase. | map | 3 | Expected High-Heat Scenario Days, Cooling-Loss Incremental Mortality Risk per 100,000, Cooling-Loss Relative 30-Day Mortality Burden Increase % | done |

### Tables

| title | what it expresses | rows | columns | row meaning | column meaning | status |
|---|---|---:|---:|---|---|---|
| Municipality Housing Loss and Older-Person Cooling Need Summary | Compact municipality comparison of modeled housing loss, affected older residents, and the no-placement demand bound. | 45 | 6 | one municipality, ordered by central Estimated Affected Population Age 65+ | Municipality; central and compact scenario-range housing loss; central and compact scenario-range affected population age 65+; No-Placement Unprotected Older-Person-Days | done |
| Municipality Cooling Electricity Planning Summary | Municipality Central-scenario cooling electricity requirements under the common heat scenario. | 45 | 6 | one municipality, ordered by central Estimated Affected Population Age 65+ | Municipality; Estimated Affected Population Age 65+; No-Placement Unprotected Older-Person-Days; Expected High-Heat Scenario Days; Required Peak Cooling Electric Power kW; Required Daily Cooling Electricity kWh | done |
| Municipality Cooling-Loss Health-Risk Summary | Municipality literature-anchored 30-day cooled-versus-uncooled health-risk contrast. | 45 | 6 | one municipality, ordered by Cooling-Loss Relative 30-Day Mortality Burden Increase % | Municipality; Expected High-Heat Scenario Days; Incremental Cooling-Loss-Related Excess Deaths; central, lower, and upper Cooling-Loss Relative 30-Day Mortality Burden Increase % | done |

No additional result is claimed for individual collapsed buildings, verified
effective cooled capacity, actual resident placement, available power, power
gap, indoor temperature, or observed excess mortality.

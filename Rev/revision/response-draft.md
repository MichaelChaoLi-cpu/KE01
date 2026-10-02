# Response to reviewers and editors of manuscript number SCSI-D-26-09591

# Revision Summary

Thank you to the editor and reviewers for their careful review.

[Revision summary to be completed after the manuscript revisions.]

- [Major manuscript-level change.]
- [Theoretical or conceptual change.]
- [Methodological or robustness-check change.]
- [Results, discussion, table, or figure change.]
- [Language, consistency, or formatting change.]

# Editor

EDITOR: Thank you for submitting your manuscript to our journal. Following careful evaluation, the reviewers acknowledge the potential contribution of your work but have identified several substantive issues that require major revision, particularly concerning the clarity of the theoretical framing, the rigour of the methodology, and the depth of engagement with existing literature. We therefore invite you to revise and resubmit your manuscript, ensuring that you consolidate the calibre of your work by carefully following the reviewers’ suggestions. Please provide a comprehensive, point-by-point response to each comment, clearly indicating how you have addressed or justified the issues raised. This will be essential in demonstrating the strengthened quality and coherence of your manuscript for further consideration.

Importantly, it is also critical that the revised manuscript substantially expands the discussion section by more thoroughly articulating the theoretical, scholarly, policy, planning, and practical contributions and implications of the findings. The manuscript should clearly demonstrate how the results advance existing theory and academic knowledge, inform policy development and urban/planning decision-making, and contribute to professional practice. In addition, the revision should more explicitly and convincingly address the broader significance of the study by thoroughly answering the “so-what” question—namely, why these findings matter, to whom they matter, and how they can shape future research, governance, planning, and implementation processes.

Read your reviewers’ comments in our peer review platform.
Before you can submit your revision, you must respond to reviews in our peer review platform.

**Response:**
[Response to be completed.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

# Reviewer 1
Review Report for Sustainable Cities and Society
Manuscript Number: SCSI-D-26-09591
## Overall Comment
1. General Assessment
This manuscript presents a timely and potentially useful spatial planning framework that links postearthquake functional housing loss, older-person cooling needs, emergency electricity demand, and
a fixed-weather mortality-risk contrast. The manuscript is generally well organized and is careful to
distinguish modeled planning quantities from observed losses or causal health outcomes. However,
several core results depend on proxy-based spatial allocation and transferred health-effect parameters.
These assumptions require stronger justification, validation, and sensitivity interpretation before the
framework can support the operational conclusions claimed.
2. Comments


**Response:**
[Response to be completed.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 1
(1) Section 2.4 (Structural Housing-Loss Allocation): The spatial allocation is driven by exposure
proxies, epicentral-distance decay, and half-collapse weights. Because the manuscript itself
identifies housing-loss geography as the largest structural uncertainty, the authors should provide
a quantitative validation against the geographically bounded official damage evidence, or at
minimum show how well alternative allocations reproduce the observed spatial pattern.


**Response:**
Thank you for this comment. Sections 2.8 and 3.3 now quantify how the selected allocation and shaking-based alternatives agree with geographically bounded official damage reports. The comparisons keep report dates and damage categories separate and use municipal rank correlation, share total-variation distance and top-five overlap. They address the requested comparison of spatial patterns, rather than establishing independent predictive validation.

For the September 29 full-or-half reports, the primary allocation has a rank correlation of 0.7252, a share total-variation distance of 0.5845 and top-five overlap of 3/5. The shaking alternatives show closer descriptive agreement: correlations of 0.7732–0.8127, share distances of 0.2374–0.3855 and overlap of 4/5. Nevertheless, report-share disagreement remains substantial. The early July 31 comparison is particularly limited by incomplete reporting. We therefore retain the primary as transparent early demand screening, not a validated municipal or building-level damage prediction. Section 4.5 explains why reported zeros, differing outcomes and prior examination of report geography prevent an independent-validation claim; Figure 5a is explicitly identified as contextual evidence.

Section 2.4 defines the primary allocation:

"The central surface is one coherent scenario using general households, a 20-km decay scale and a half-collapse weight of 0.5, giving 303.5 functional-loss units. Household counts align the allocation denominator with the target population; 20 km and 0.5 are transparent planning assumptions, not empirically optimized parameters or a calibrated loss fraction."
(Page 9, Lines 170–174)

Section 2.8 specifies the comparison and its limitations:

"We assess municipality rank correlations, rank shifts and top-five overlap. Separate comparisons with July 31 and September 29 prefectural reports use full collapse, large-scale-half plus half collapse, and their combined counts. Share total-variation distance is half the sum of absolute municipal share differences. Report dates and categories are kept distinct from the planning snapshot. These comparisons are descriptive rather than independent validation: outcomes and assessment completeness differ, report zeros are not verified negatives, and report geography was examined before developing the alternatives."
(Page 16, Lines 321–328)

Section 3.3 reports the quantitative findings:

"Against September 29 full-or-half reports, the primary has rank correlation 0.7252, share total-variation distance 0.5845 and top-five overlap 3/5; the corresponding shaking ranges are 0.7732–0.8127, 0.2374–0.3855 and 4/5. The July 31 combined report has only five municipalities with positive counts; primary correlation is 0.3108 and share distance 0.9674. Thus stable high-exposure membership does not establish accurate reported-damage geography."
(Page 20, Lines 411–416)

Section 4.5 states the remaining evidence boundary:

"The selected allocation is retained as transparent early demand screening, not validated municipal or building-level damage prediction. Report-share disagreement remains substantial; the closer descriptive agreement of shaking alternatives does not establish independent validity or justify post hoc selection. Nearest-station categories omit local site effects, source vulnerability curves are transferred beyond their original setting, and full-collapse shapes are used only as hypothetical functional-loss weights."
(Page 25, Lines 523–529)

The Figure 5 note clarifies the role of the mapped official evidence:

"Panels b and c use the household/20-km/0.5 primary and bounded general-household older-population allocation; panel a is contextual evidence, not independent validation."
(Page 32, Lines 595–596)

## Comment 2
(2) Section 2.4, Equations (1)–(3): The “central surface” is constructed from a normalized pointwise
median across 27 allocation scenarios. Please clarify why this hybrid surface is preferable to
selecting a coherent central scenario and demonstrate that normalization after the pointwise
median does not distort municipality-level rankings or uncertainty interpretation.


**Response:**
Thank you for raising this issue. We no longer treat the normalized pointwise median as the primary surface. Section 2.4 now selects one coherent scenario using general households, a 20-km decay scale and a half-collapse weight of 0.5. The corrected hybrid is retained only as a sensitivity analysis. This choice makes the primary correspond to an actual scenario; it does not imply empirical optimization of its parameters.

We also checked normalization separately using the corrected scenario ensemble and the current bounded demographic allocation. The raw median sums to 234.940182 functional-loss units; multiplying all groups by the same positive factor, 1.291818187, restores the total to 303.5. All 45 municipal housing-loss and older-exposure rankings remain unchanged, and subsequent clipping affects no groups. Under fixed demographic weights, linear aggregation and nonbinding caps, a common positive multiplier preserves these rankings. This result concerns normalization within the hybrid, not equivalence between the hybrid and the coherent primary.

The latter comparison is reported in Section 3.3: the corrected hybrid yields 216.546 exposed older residents, 7.18% more than the primary, with municipal exposure rank correlation 0.9818, a maximum rank shift of six and the same top-five set. Section 2.4 explicitly distinguishes pointwise sensitivity bounds from jointly realized scenario totals. The Abstract, downstream results and Figures 5–8 and Tables 1–3 now consistently use the coherent primary; neither normalization nor ranking stability is presented as external validation.

The revised Abstract states:

"The central allocation contains 303.5 functionally lost residences and approximately 202 affected residents aged 65 or older. Under the Central engineering scenario, their protection requires 28.427 kW of peak cooling power and 511.691 kWh of electricity per day across the prefecture."
(Page 1, Lines 14–17)

Section 2.4 defines the primary and the interpretation of sensitivity bounds:

"The central surface is one coherent scenario using general households, a 20-km decay scale and a half-collapse weight of 0.5, giving 303.5 functional-loss units. Household counts align the allocation denominator with the target population; 20 km and 0.5 are transparent planning assumptions, not empirically optimized parameters or a calibrated loss fraction. The normalized pointwise-median surface, rebuilt after the zero-household correction, is retained only as a separate sensitivity. Pointwise minima and maxima form lower and upper sensitivity surfaces. Because each endpoint can arise from a different scenario at a different location, these surfaces are local sensitivity bounds rather than a jointly realized prefecture interval. Their sums must therefore retain that interpretation."
(Page 9, Lines 170–178)

Section 2.8 specifies aggregation:

"Additive disclosure-group outcomes are summed using representative-point municipality assignments after the central scenario is selected at its defined analytical scale."
(Page 15, Lines 297–298)

The same section describes the comparison:

"We additionally compare the selected primary with the corrected hybrid, bounded demographic alternative and 54 hypothetical shaking allocations. For the latter, nearest-station JMA intensity categories are assigned in projected coordinates, including neighbouring-prefecture stations and excluding the withdrawn Tomiai observation."
(Page 15, Lines 310–313)

Section 3.3 reports the difference between the primary and hybrid:

"The corrected hybrid yields 216.546 exposed older residents, 7.18% above the selected primary; municipal exposure rank correlation is 0.9818, with a maximum rank shift of six and the same top-five set."
(Pages 19–20, Lines 403–405)

Section 3.4 updates electricity requirements:

"Peak power rises from 17.96 kW in the Low bundle to 28.427 kW in the Central bundle and 39.88 kW in the High bundle; corresponding daily electricity rises from 215.54 to 511.691 and 957.19 kWh."
(Page 20, Lines 421–423)

Section 3.5 updates the health contrast:

"The prefecture-weighted central 30-day mortality-burden increase without effective cooling is 5.31%, with source-effect endpoint scenarios of 0.66% and 9.96%; these endpoints are not whole-model confidence limits."
(Page 21, Lines 436–438)

Section 4.5 retains the limits on predictive interpretation:

"The selected allocation is retained as transparent early demand screening, not validated municipal or building-level damage prediction. Report-share disagreement remains substantial; the closer descriptive agreement of shaking alternatives does not establish independent validity or justify post hoc selection. Nearest-station categories omit local site effects, source vulnerability curves are transferred beyond their original setting, and full-collapse shapes are used only as hypothetical functional-loss weights."
(Page 25, Lines 523–529)

The Figure 5 note identifies the primary specification:

"Panels b and c use the household/20-km/0.5 primary and bounded general-household older-population allocation; panel a is contextual evidence, not independent validation."
(Page 32, Lines 595–596)

The Figure 6 note distinguishes the pointwise upper bound from a jointly realized scenario:

"Panel b maps the pointwise high 30-day no-placement older-person-day planning bound, derived from pointwise maxima across the 27 distance/proxy/half-collapse scenarios and not representing a jointly realized aggregate scenario."
(Page 33, Lines 600–602)

## Comment 3
(3) Section 2.4, Equation (3): Older-person exposure assumes that the modeled household-loss share
applies proportionally to the resident population aged 65+. This ecological allocation is
important to the final cooling and mortality estimates. Please justify this assumption and add a
sensitivity test or alternative allocation based on available household/age structure.


**Response:**
Thank you for this comment. Section 2.4 now replaces the all-resident older-population input with a bounded estimate of residents aged 65 or older in general households. This aligns the population universe with the general-household denominator used in Equation 3. The estimate uses households containing an older member, all-resident older-population bounds and official municipal general-household older-population controls. Older-household weighting is the primary allocation; residual-capacity weighting provides a separate sensitivity.

The proportional housing-loss rule remains an explicit working assumption: within each disclosure group, housing loss is assumed not to be systematically associated with age composition. It produces an expected exposure count when household-specific residence and damage links are unavailable, rather than identifying affected individuals. The demographic alternative tests sensitivity to the spatial allocation of older residents; it does not test or establish equality of damage probabilities across age groups.

Under the same household/20-km/0.5 structural scenario, the two feasible demographic allocations yield 202.041936 and 202.185459 expected exposed older residents, a difference of approximately 0.071%. Their municipal rank correlation is 0.999868, with the same top five in the same order and a maximum rank shift of one. Both match the same official municipal population controls. These close municipal results can coexist with different within-municipality allocations and are not validation of grid-level residence patterns. Section 4.5 explicitly retains this limitation. The revised Abstract, Results and associated figures and tables use the selected bounded allocation.

The revised Abstract reports the selected population and associated demand:

"The central allocation contains 303.5 functionally lost residences and approximately 202 affected residents aged 65 or older. Under the Central engineering scenario, their protection requires 28.427 kW of peak cooling power and 511.691 kWh of electricity per day across the prefecture."
(Page 1, Lines 14–17)

Section 2.4 defines the household-based population allocation and working assumption:

"We associate structural housing loss with older residents by scaling each group's estimated general-household population aged 65 or older by its modeled share of general households lost. For each group, the lower bound is the number of households containing an older member; the upper bound is the all-resident older population where that lower bound is positive, and zero otherwise. Starting from the lower bound, we distribute the municipal remainder in proportion to older-household counts, subject to the upper bounds, to match official municipal general-household older-population controls. Groups are assigned to municipalities by representative points. Residual-capacity weighting is a separate demographic sensitivity. These allocations reproduce municipal controls but do not validate within-municipality residence patterns. Equation 3 assumes that housing loss is not systematically associated with age composition within a group; exposure is defined as zero where general households are zero."
(Pages 9–10, Lines 179–190)

Section 2.8 explains municipality aggregation:

"Additive disclosure-group outcomes are summed using representative-point municipality assignments after the central scenario is selected at its defined analytical scale."
(Page 15, Lines 297–298)

The same section includes the demographic alternative among the sensitivity comparisons:

"We additionally compare the selected primary with the corrected hybrid, bounded demographic alternative and 54 hypothetical shaking allocations. For the latter, nearest-station JMA intensity categories are assigned in projected coordinates, including neighbouring-prefecture stations and excluding the withdrawn Tomiai observation."
(Page 15, Lines 310–313)

Section 3.3 reports the alternative-allocation result:

"Residual-capacity demographic weighting yields 202.185 exposed older residents, with a maximum rank shift of one."
(Page 20, Lines 405–407)

Section 3.4 reports electricity demand based on the updated population:

"Peak power rises from 17.96 kW in the Low bundle to 28.427 kW in the Central bundle and 39.88 kW in the High bundle; corresponding daily electricity rises from 215.54 to 511.691 and 957.19 kWh."
(Page 20, Lines 421–423)

Section 3.5 reports the corresponding health contrast:

"The prefecture-weighted central 30-day mortality-burden increase without effective cooling is 5.31%, with source-effect endpoint scenarios of 0.66% and 9.96%; these endpoints are not whole-model confidence limits."
(Page 21, Lines 436–438)

Section 4.5 states the unresolved ecological limitation:

"Municipal calibration and demographic rank stability cannot verify within-group residence patterns or the assumed absence of systematic age-related loss differences."
(Page 25, Lines 529–531)

The Figure 5 note identifies the bounded older-population allocation:

"Panels b and c use the household/20-km/0.5 primary and bounded general-household older-population allocation; panel a is contextual evidence, not independent validation."
(Page 32, Lines 595–596)

The Figure 6 note retains the distinction between a pointwise planning bound and a realized scenario:

"Panel b maps the pointwise high 30-day no-placement older-person-day planning bound, derived from pointwise maxima across the 27 distance/proxy/half-collapse scenarios and not representing a jointly realized aggregate scenario."
(Page 33, Lines 600–602)

## Comment 4
(4) The manuscript uses the five-year mean number of matching-period high-heat station-days and
interpolates these values to municipality centroids. Please explain more clearly how the resulting
fractional expected high-heat days (e.g., 0.357–23.609 days) are used in the 30-day
compounding equations and why this is an appropriate representation of the event-period
counterfactual rather than a forecast.


**Response:**
[Response to be completed.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 5
(5) Section 2.7, Equation (9): The origin and interpretation of the 1.03 multiplier used to define the
effective-cooling high-heat probability are not sufficiently explained in the text. Please identify
its empirical source, explain how it relates to the transferred no-cooling odds ratio (ρ = 1.08),
and provide sensitivity results showing whether the 5.34% central burden increase materially
depends on this parameterization.


**Response:**
[Response to be completed.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 6
(6) Sections 2.7 and 4.5: The health-effect estimate is transferred from Ontario nursing homes to the
general population aged 65+ in Kumamoto. This is a substantial external-validity limitation
because institutional residents, building conditions, health status, and cooling exposure may
differ. The authors should strengthen the transferability argument and present the mortality
analysis more explicitly as an illustrative planning scenario; an alternative effect range or
scenario would improve robustness.


**Response:**
[Response to be completed.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 7
(7) The Low/Central/High engineering bundles are central to the reported 21.85–48.52 kW and
262.21–1,164.47 kWh/day requirements. Please provide a compact parameter table with the
numerical values, units, sources, and rationale for shelter area per person, cooling-load density,
COP, diversity factor, and operating hours. This is necessary for reproducibility and operational
interpretation.


**Response:**
Thank you for this comment. Supplementary Table S1 now provides a compact parameter table with numerical values, units, sources and rationale for all five inputs. In Low/Central/High order, these are area 3.5/3.5/3.5 m²/person, cooling-load density 127/134/141 W/m², COP 4/3/2.5, diversity factor 0.8/0.9/1.0, and operating duration 12/18/24 h/day. Section 2.6 distinguishes the official minimum living-space proxy, case-derived load-density endpoints, the analyst midpoint and study-defined efficiency and operating assumptions. It also explains the limits of transferring the case benchmarks to emergency shelters.

The engineering parameters remain unchanged. The revised population allocation updates the demand estimates to 17.96–39.88 kW and 215.54–957.19 kWh/day, replacing the earlier values quoted in the comment. Section 3.4 and Figure 7 retain the distinction between modeled demand and verified supply shortages. Daily electricity is a constant-scenario-power calculation, not measured consumption.

Section 2.6 states:

"Table S1 reports all parameter values, units and sources. Area remains fixed at 3.5 m²/person as a minimum living-space proxy, not an elderly-specific cooled-floor-area standard. The load-density endpoints are insulation-dependent benchmarks from one gymnasium case, and 134 W/m² is their arithmetic midpoint. That case assumes 0.15 persons/m², whereas the adopted area implies approximately 0.286 persons/m²; the case also contains inconsistent gymnasium/office labeling. These differences limit transfer to emergency shelters. COP, diversity and operating hours are study-defined scenarios rather than government-prescribed values."
(Page 13, Lines 255–262)

Section 3.4 reports the updated requirements:

"Peak power rises from 17.96 kW in the Low bundle to 28.427 kW in the Central bundle and 39.88 kW in the High bundle; corresponding daily electricity rises from 215.54 to 511.691 and 957.19 kWh."
(Page 21, Lines 439–441)

The Figure 7 note clarifies their interpretation:

"All bundles use the same selected primary population; daily energy assumes constant scenario power over the specified operating hours, not measured consumption or a verified supply shortfall."
(Page 34, Lines 627–629)

## Comment 8
(8) The manuscript repeatedly and appropriately states that the outputs are planning quantities rather
than observed damage, displacement, supply shortages, or deaths. The discussion should go one
step further and specify which conclusions remain robust across structural, engineering,
calibration, and health-effect sensitivities, and which municipality rankings or policy
implications are unstable.



**Response:**
[Response to be completed.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

# Reviewer 3
Major Comments
## Comment 1
M1 | Definition of exposure and distributional assumption regarding the 65+ population
References: Sec. 1; Sec. 2.3; Sec. 2.4, Eq. 3; Sec. 3.1; Figure 2, panel b; Table 1.
(M1.1)
The framework identifies the older population in need of cooling exclusively through functional housing loss. However,
Sec. 3.1 documents a shelter population also shaped by conditions, such as service disruptions and other precautionary
needs, that fall outside the adopted definition of exposure. Although the two populations are not directly comparable,
the operational data reported in the manuscript itself show that the framework identifies a specific subset of the
population potentially in need of heat protection, rather than the population affected by displacement as a whole.
SUGGESTED REVISION: explicitly clarify the relationship between the modelled population and the broader population affected
by displacement; justify the choice to restrict exposure to functional housing loss; specify, in particular in the Abstract and in Sec.
2.3, the population boundary to which the framework's outputs refer.


**Response:**
Thank you for this comment. The Abstract and Sections 1, 2.3 and 3.1 now explicitly restrict the target population to older residents associated with functional housing loss, explain the evidence-based reason for this boundary, and distinguish modeled exposure from broader shelter occupancy and observed displacement. The revised text states:

"The target is the housing-loss-related older population, not all displaced residents or everyone potentially requiring cooling after service disruptions."
(Page 1, Lines 12–14)

"This study asks where cooling protection for older residents associated with functional housing loss is most needed after the Kumamoto earthquake, how much peak power and daily electricity that protection would require, and how the modeled mortality burden differs if effective cooling is not restored during the next 30 days."
(Page 4, Lines 64–67)

"We restrict this population to the housing-loss pathway because reported building-damage totals constrain that pathway, whereas the available operational reports do not identify the older individuals displaced by each cause. Residents requiring protection solely because of service outages or precautionary evacuation are outside this modeled population. Association with housing loss does not establish actual displacement or loss of effective cooling for each individual."
(Page 7, Lines 135–140)

"These occupancy counts describe a broader, differently timed and geographically bounded population; they are not age-specific counts of residents associated with functional housing loss. Service disruptions and precautionary needs can also prompt shelter use. We therefore use occupancy as operational context, not as a calibration or validation total for modeled older-person exposure."
(Page 16, Lines 317–322)

## Comment 2
(M1.2)
Eq. 3 assumes that, within each disclosure group, the share of older residents associated with functional housing loss is
proportional to the modelled share of general households lost, and thus that housing loss is not systematically related to
age composition, an assumption acceptable as a screening proxy, but one that should be stated and discussed.
SUGGESTED REVISION: make explicit and discuss the distributional assumption in Eq. 3, assessing its impact on the estimate of
the 65+ population associated with housing loss.


**Response:**
Thank you for this comment. Section 2.4 now explicitly states that Equation 3 assumes no systematic association between housing loss and age composition within a disclosure group. This is a screening assumption, not an empirically established independence relationship. The older-population input is now restricted to an estimated general-household population, with municipal controls and household-based bounds.

To assess sensitivity to the demographic distribution, we compare older-household weighting with residual-capacity weighting under the same structural loss scenario. They yield 202.042 and 202.185 expected exposed older residents, respectively, with a maximum municipal rank shift of one. This tests the spatial allocation of the older population, not whether older households actually experience the same loss probability as other households. Section 4.5 explicitly retains that unverified assumption and cautions that municipal calibration and rank stability do not validate within-group residence patterns.

Section 2.4 states:

"These allocations reproduce municipal controls but do not validate within-municipality residence patterns. Equation 3 assumes that housing loss is not systematically associated with age composition within a group; exposure is defined as zero where general households are zero."
(Page 10, Lines 187–190)

Section 3.3 reports the demographic sensitivity:

"Residual-capacity demographic weighting yields 202.185 exposed older residents, with a maximum rank shift of one."
(Page 20, Lines 405–407)

Section 4.5 discusses the remaining limitation:

"Municipal calibration and demographic rank stability cannot verify within-group residence patterns or the assumed absence of systematic age-related loss differences."
(Page 25, Lines 529–531)

## Comment 3
M2 | Transferability of the parameters used in the mortality-risk contrast
References: Sec. 2.7, Eq. 8-12; Sec. 3.5; Sec. 4.4; Sec. 4.5; Table 3; Figure 8.
(M2.1)
The factor applied to the state with effective cooling (1.03) and the odds ratio associated with the absence of effective
cooling (ρ = 1.08, with a 95% confidence interval from 1.01 to 1.15) both derive from Katz et al. (2026), a study
conducted among nursing-home residents in Ontario. Sec. 4.5 addresses the statistical uncertainty associated with the
effect parameter, but does not substantially address the transferability of these estimates to a community-dwelling older
population in Japan, in a markedly different climatic, housing, and care context.
SUGGESTED REVISION: explicitly discuss the transferability of the parameters used, supporting the discussion with comparative
literature referring, where available, to community-dwelling older populations and to comparable climatic contexts.


**Response:**
[Response to be completed.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 4
(M2.2)
Once the transferred health parameters and the municipal mortality baseline are fixed, the territorial variation in the
relative burden (Eq. 12) is substantially driven by the number of expected high-heat days, as shown by the monotonic
relationship reported in Table 3. The prefecture-wide value of 5.34% should therefore be interpreted as a modelled
output obtained by applying a transferred health effect to the local climate profile, and not as empirical evidence of an
observed health effect in Kumamoto.
SUGGESTED REVISION: explicitly clarify this modelled nature and the dependence on the transferred parameters and on the
number of expected high-heat days.


**Response:**
[Response to be completed.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 5
M3 | Seismic hazard, local verification, and robustness of the central surface
References: Sec. 2.4, Eq. 1-3; Sec. 2.8; Sec. 3.3; Sec. 4.5; Figure 5; Table 1.
The allocation uses decay with respect to epicentral distance as the sole spatial proxy for hazard (Eq. 1), while the manuscript
does not justify the exclusion of observed seismic-intensity information that could be more representative of the spatial
distribution of shaking. In addition, the half-collapse weight θ = 0.5 contributes substantially to the central total but is not
explicitly justified; the official georeferenced evidence reported in Fig. 5a is not used for a local verification of the allocation;
and finally, the central surface, obtained as the normalized pointwise median of the scenarios, does not necessarily correspond
to any actually simulated scenario. Since this surface feeds into the subsequent outputs, it would be useful to demonstrate that
the main territorial priorities remain stable across the different structural specifications. It also remains unclear whether the
allocation approach employed was developed specifically for this study or constitutes the application of a method already
proposed and tested elsewhere: this information would make it possible to situate the adopted methodological choices more
clearly and to understand whether they have already been validated in other contexts, given the only partial availability of
independent georeferenced evidence in the present case.
SUGGESTED REVISION: justify the choice of epicentral distance relative to other available indicators, including seismic-intensity
data; state and justify the value of θ; compare, where possible, the allocation with the georeferenced evidence reported in Fig. 5a; 
verify the robustness of the main territorial priorities across the structural scenarios, for example through rank comparison or another
stability measure, and clarify the operational meaning of the central surface. The authors should also specify whether the allocation
framework was developed specifically for this study or derives from the adaptation of an approach previously proposed or tested
elsewhere.


**Response:**
Thank you for this detailed comment. Sections 2.4 and 2.8 now distinguish our study-defined, total-constrained screening allocation from a fitted or previously validated damage model. The primary surface is a single coherent household-proxy scenario with a 20-km decay scale and a half-collapse weight of 0.5, rather than a normalized pointwise median. These parameter values are transparent planning assumptions, not calibrated physical relationships. The corrected median surface remains a separate sensitivity analysis.

Observed shaking is now examined through 54 alternative allocations based on JMA intensity categories and transferred vulnerability shapes. Section 3.3 reports rank correlations, maximum rank shifts and top-five overlap, together with descriptive comparisons against dated municipal damage reports. The exposure top-five set remains stable across these alternatives, but lower-ranked municipalities and incremental-death priorities are less stable. Report-share disagreement remains substantial. Accordingly, Section 4.5 retains epicentral-distance allocation only as early demand screening: neither ranking stability nor closer agreement after examining report geography establishes independent validation. Figure 5a remains contextual evidence, not a validation sample. Figures 5–8, Tables 1–3 and the associated Abstract and Results now use the selected primary consistently.

The revised Abstract states:

"The central allocation contains 303.5 functionally lost residences and approximately 202 affected residents aged 65 or older. Under the Central engineering scenario, their protection requires 28.427 kW of peak cooling power and 511.691 kWh of electricity per day across the prefecture."
(Page 1, Lines 14–17)

Section 2.4 clarifies the allocation's provenance, assumptions and population definition:

"This is a study-defined total-constrained screening allocation, not a fitted damage-prediction model. Groups without general households receive zero allocation; the remaining weights are renormalized to conserve the scenario total."
(Page 8, Lines 155–158)

"Housing-loss scenarios cross general households, mapped-building count and mapped footprint area with three distance-decay scales and half-collapse weights of 0, 0.5 and 1, producing 27 allocations. Building proxies are weighting variables, not counts of residences."
(Pages 8–9, Lines 162–165)

"The central surface is one coherent scenario using general households, a 20-km decay scale and a half-collapse weight of 0.5, giving 303.5 functional-loss units. Household counts align the allocation denominator with the target population; 20 km and 0.5 are transparent planning assumptions, not empirically optimized parameters or a calibrated loss fraction. The normalized pointwise-median surface, rebuilt after the zero-household correction, is retained only as a separate sensitivity."
(Page 9, Lines 170–175)

"Starting from the lower bound, we distribute the municipal remainder in proportion to older-household counts, subject to the upper bounds, to match official municipal general-household older-population controls."
(Page 9, Lines 183–185)

Section 2.8 describes consistent aggregation and the shaking alternatives:

"Additive disclosure-group outcomes are summed using representative-point municipality assignments after the central scenario is selected at its defined analytical scale."
(Page 15, Lines 297–298)

"We additionally compare the selected primary with the corrected hybrid, bounded demographic alternative and 54 hypothetical shaking allocations. For the latter, nearest-station JMA intensity categories are assigned in projected coordinates, including neighbouring-prefecture stations and excluding the withdrawn Tomiai observation."
(Page 15, Lines 310–313)

Section 3.3 reports the structural sensitivity and geographic comparisons:

"The corrected hybrid yields 216.546 exposed older residents, 7.18% above the selected primary; municipal exposure rank correlation is 0.9818, with a maximum rank shift of six and the same top-five set. Residual-capacity demographic weighting yields 202.185 exposed older residents, with a maximum rank shift of one. Across the 54 shaking scenarios, exposure ranges from 133.49 to 363.43 and rank correlations from 0.8163 to 0.8978; maximum rank shifts are 16–24. All retain the exposure top-five set, but incremental-death top-five overlap is four of five. These ranges combine hazard, proxy and half-collapse assumptions and are not confidence intervals. Against September 29 full-or-half reports, the primary has rank correlation 0.7252, share total-variation distance 0.5845 and top-five overlap 3/5; the corresponding shaking ranges are 0.7732–0.8127, 0.2374–0.3855 and 4/5. The July 31 combined report has only five municipalities with positive counts; primary correlation is 0.3108 and share distance 0.9674. Thus stable high-exposure membership does not establish accurate reported-damage geography."
(Pages 19–20, Lines 403–416)

Sections 3.4 and 3.5 update the downstream estimates:

"Peak power rises from 17.96 kW in the Low bundle to 28.427 kW in the Central bundle and 39.88 kW in the High bundle; corresponding daily electricity rises from 215.54 to 511.691 and 957.19 kWh."
(Page 20, Lines 421–423)

"The prefecture-weighted central 30-day mortality-burden increase without effective cooling is 5.31%, with source-effect endpoint scenarios of 0.66% and 9.96%; these endpoints are not whole-model confidence limits."
(Page 21, Lines 436–438)

Section 4.5 states the remaining limitations:

"The selected allocation is retained as transparent early demand screening, not validated municipal or building-level damage prediction. Report-share disagreement remains substantial; the closer descriptive agreement of shaking alternatives does not establish independent validity or justify post hoc selection. Nearest-station categories omit local site effects, source vulnerability curves are transferred beyond their original setting, and full-collapse shapes are used only as hypothetical functional-loss weights."
(Page 25, Lines 523–529)

The revised figure notes explain the interpretation of the updated outputs. Figure 5 states:

"Panels b and c use the household/20-km/0.5 primary and bounded general-household older-population allocation; panel a is contextual evidence, not independent validation."
(Page 32, Lines 595–596)

Figure 6 states:

"Panel b maps the pointwise high 30-day no-placement older-person-day planning bound, derived from pointwise maxima across the 27 distance/proxy/half-collapse scenarios and not representing a jointly realized aggregate scenario."
(Page 33, Lines 600–602)

Figure 7 states:

"All bundles use the same selected primary population; daily energy assumes constant scenario power over the specified operating hours, not measured consumption or a verified supply shortfall."
(Page 34, Lines 609–611)

Figure 8 states:

"Panel c maps the relative increase in 30-day mortality burden and reports the prefecture-weighted central contrast and source-effect endpoint range, which excludes structural, engineering, baseline and transfer uncertainty."
(Page 35, Lines 616–618)

## Comment 6
M4 | Transparency of parameters and sensitivity analysis
References: Sec. 2.4, Sec. 2.6, Eq. 6-7; Sec. 2.8; Sec. 3.4; Figure 7, panel c.
Some parameters necessary for the reproducibility of the calculation chain are not explicitly reported in the manuscript. In
particular, the shelter area per person used in Eq. 6 can only be reconstructed indirectly from the outputs; similarly, Sec. 2.4
does not clearly report the values of the decay scales λ or the full specification of the exposure proxies used across the
scenarios. In addition, the engineering sensitivity analysis varies the different parameters over markedly different ranges:
cooling-load density changes relatively little, while COP and operating hours span much wider ranges. Shelter area per person,
despite entering as a direct multiplier in the load calculation, remains fixed across the three bundles.
SUGGESTED REVISION: report, in tabular form, all parameters used in the three bundles, with units, values, and their respective
sources, including shelter area per person; explicitly report the values of λ and the definition of the exposure proxies used in the
allocation; justify the choice of the ranges adopted in the sensitivity analysis and consider including shelter area per person among
the parameters varied.
Minor Comments


**Response:**
Thank you for this comment. Sections 2.2, 2.4 and 2.6 now explicitly report the fixed area assumption, the distance-decay scales and exposure-proxy definitions, and the provenance and interpretation of the engineering bundles. Supplementary Table S1 lists all five engineering parameters with units, Low/Central/High values, sources and rationale. It distinguishes Cabinet Office living-space guidance from the MLIT case-derived load benchmarks and from study-defined equipment and operating assumptions.

The differing range widths reflect these different bases: load-density endpoints come from two insulation conditions in one case, whereas COP, diversity and operating duration explore assumed equipment and operating choices. They are not comparable uncertainty intervals. We retain 3.5 m²/person in the reported bundles because a larger cooled-space requirement is not established for the target facilities. Section 2.6 explains the direct proportional scaling with area at fixed other inputs, rather than presenting an unsupported area range as an empirical sensitivity. It also discloses the source case's occupancy and labeling limitations and the constant-power assumption behind daily electricity. These clarifications do not change the reported engineering results.

Section 2.2 corrects the description of the fixed area:

"Low, Central, and High engineering bundles hold shelter area per person fixed and vary cooling load, system efficiency, peak diversity, and operating duration."
(Page 7, Lines 122–123)

Section 2.4 specifies the structural scenarios:

"Housing-loss scenarios cross general households, mapped-building count and mapped footprint area with distance-decay scales of 10, 20 and 40 km and half-collapse weights of 0, 0.5 and 1, producing 27 allocations. The proxies are the census general-household count, mapped-building polygon count and summed mapped-building footprint area within each disclosure group. Building proxies are weighting variables, not counts of residences."
(Page 9, Lines 163–168)

Section 2.6 explains the parameter table and assumptions:

"Table S1 reports all parameter values, units and sources. Area remains fixed at 3.5 m²/person as a minimum living-space proxy, not an elderly-specific cooled-floor-area standard. The load-density endpoints are insulation-dependent benchmarks from one gymnasium case, and 134 W/m² is their arithmetic midpoint. That case assumes 0.15 persons/m², whereas the adopted area implies approximately 0.286 persons/m²; the case also contains inconsistent gymnasium/office labeling. These differences limit transfer to emergency shelters. COP, diversity and operating hours are study-defined scenarios rather than government-prescribed values. The narrow load-density range reflects the two case benchmarks, while the broader efficiency and duration ranges explore equipment and operating choices; their widths are not comparable measures of uncertainty. Area is not varied in these bundles because a larger cooled-space requirement is not established for the target facilities. At fixed load density and other inputs, thermal load, electric demand and daily energy scale directly with area, so site-specific area can be substituted without treating this algebraic relationship as a validated facility design. Daily energy assumes constant scenario electric demand over the stated operating hours, not a measured load profile."
(Page 13, Lines 255–270)

## Comment 7
m1 – The 1.03 constant in Eq. 9 is not attributed in the text, although it corresponds to the odds ratio reported by Katz et al.
(2026) for air-conditioning-equipped facilities. This attribution should be made explicit. (Sec. 2.7, Eq. 9)


**Response:**
[Response to be completed.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 8
m2 – The spatial calibration relies on relatively limited instrumental coverage, subsequently interpolated. It is suggested that
the representativeness of the estimates in peripheral areas be discussed more explicitly, beyond the overall cross-validation
error alone. (Sec. 2.5; Sec. 3.2)


**Response:**
Thank you for this comment. Sections 2.5, 3.2 and 4.5 now distinguish geographic support from predictor-range extrapolation, report a neighboring-station sensitivity test, and explain why expanded coverage does not by itself validate peripheral estimates. The original calibration remains the main specification because the extension does not uniformly improve prediction error. The revised text states:

"To assess peripheral representativeness, we quantify displayed pixels outside the station convex hull and outside the station-sampled land-surface-temperature range. A sensitivity test adds eligible neighboring stations within 30 and 50 km of the prefectural boundary while retaining the original daytime and nighttime model specifications and MODIS quality rules. New stations require complete temperature pairs for the 150 matching-period days in 2021–2025 and an eligible MODIS pixel within 5 km. Prediction errors are evaluated by holding out each original Kumamoto station in turn; these temperature-calibration tests do not alter the separate high-heat-day interpolation."
(Page 10, Lines 183–191)

"Nevertheless, 33.4% of displayed pixels lie outside the station convex hull, and 61.1% of daytime and 31.3% of nighttime pixels lie outside the station-sampled land-surface-temperature range. Adding 23 eligible stations within 30 km changes daytime/nighttime RMSE to 0.763/0.571 °C; adding 44 within 50 km changes it to 0.716/0.563 °C. The 50 km extension removes geographic hull extrapolation for displayed pixels but does not uniformly improve prediction error. We therefore retain the original calibration as the main specification and report the extension as a sensitivity test."
(Pages 15–16, Lines 314–320)

"Improved station coverage does not by itself establish accuracy at unobserved peripheral locations, and geographic coverage does not eliminate extrapolation beyond sampled land-surface temperatures. Cross-validation scores are conditional on model selection using the same station sample, rather than independent validation, and the uncertainty surface is not a calibrated prediction interval."
(Pages 21–22, Lines 449–453)

## Comment 9
m3 – The mortality baseline used in Eq. 8 derives from the all-cause mortality of the population aged ≥65, aggregated over
five years, whereas the subsequent contrast concerns heat exposure within a specific seasonal window. It is suggested that the
implications of this step and the adequacy of the baseline be discussed. (Sec. 2.7, Eq. 8)


**Response:**
[Response to be completed.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 10
m4 – The analysis is constrained to the official snapshot available as of August 1, 2026. Given the progressively updated
nature of post-event damage estimates, the Authors should verify whether more recent data are available and, where they are,
clarify whether their use could substantially change the results or the territorial priorities identified. (Sec. 2.1-2.2; Sec. 4.5)


**Response:**
Thank you for this comment. Sections 2.1–2.2, 2.8, 3.3 and 4.5 now identify the later FDMA report and distinguish the early planning snapshot from a retrospective total-only sensitivity test. The later counts substantially increase the functional-loss constraint, while unchanged rankings under fixed spatial weights are a mechanical result rather than validation of territorial priorities. The revised text states:

"We retain this early housing-damage cutoff for the main analysis and use later reported totals only in a separate retrospective sensitivity test; they are not treated as information available at the early cutoff."
(Page 5, Lines 79–82)

"The August 1 prefecture snapshot reports 181 fully collapsed and 245 half-collapsed residential buildings, which constrain rather than locate the modeled loss. FDMA Report 65, dated September 24, 2026, at 17:00 JST, reports 2,270 fully collapsed and 6,357 half-collapsed residential buildings in Kumamoto Prefecture (https://www.fdma.go.jp/disaster/info/items/20260728kumamotojishin65.pdf). Both snapshots count buildings rather than households or people, and the later figures remain provisional."
(Page 6, Lines 101–108)

"A separate retrospective snapshot test substitutes the September 24 full- and half-collapse totals while retaining the main spatial weights, population inputs, half-collapse weight of 0.5, and downstream assumptions. It tests sensitivity to the reported prefecture total, not changes in the observed geography of damage."
(Page 14, Lines 286–289)

"In the total-only retrospective test, the later snapshot raises this constraint to 5,448.5, or 17.95 times the early value. Municipal rankings remain unchanged under fixed spatial weights and nonbinding household caps; this is a consequence of the test design, not evidence that actual territorial damage priorities remain unchanged."
(Pages 16–17, Lines 337–340)

"The early damage snapshot also limits the magnitude of estimated need. Later reported totals can reflect delayed assessment and classification changes as well as additional damage, so their increase cannot be interpreted solely as new physical losses after August 1. Operational priorities require updated local damage and displacement evidence rather than proportional rescaling of prefecture totals alone."
(Page 22, Lines 454–459)

## Comment 11
m5 – The Title and Abstract characterize the method as a spatial planning framework, whereas the outputs actually
demonstrated mainly concern: spatial screening, territorial prioritization, and sizing of cooling demand. Sec. 4.3 further
excludes verification of the adequacy of available resources, and the Conclusion refers to "bounded priorities" rather than to
allocation or sequencing decisions. It is therefore suggested that the decision-making level actually supported by the
framework be clarified, and that a more consistent formulation be considered. (Title; Abstract; Sec. 4.3; Sec. 5)
Optional Comments


**Response:**
[Response to be completed.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 12
o1 – Tables 1-3 (three panels each, high decimal precision) may be cumbersome for operational users. It is suggested that
concise versions be produced in the main text, with complete versions provided as supplementary material. (Tables 1-3)


**Response:**
[Response to be completed.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

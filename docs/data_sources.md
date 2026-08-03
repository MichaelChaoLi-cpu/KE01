# KE01 Initial Data Sources

## Event scope

The current working assumption is the Kumamoto earthquake that began on 2026-07-28.
The event date must remain explicit because the 2016 Kumamoto earthquake has a distinct
damage footprint, population baseline, and temperature window.

## Working evidence chain

1. Earthquake-related housing damage or loss of habitable housing.
2. Exposure of older residents, including possible displacement or shelter residence.
3. Post-event heat exposure relative to the same-season historical baseline.
4. Heat-related ambulance transport, mortality, or another health outcome.

The first three layers can support a near-real-time vulnerability map. They do not, by
themselves, establish that the earthquake caused additional deaths.

## Source plan

| Layer | Initial source | Spatial/temporal unit | Use | Main limitation |
|---|---|---|---|---|
| Damage snapshot | FDMA earthquake situation reports | Prefecture/event updates | Official evolving damage totals | Preliminary and not building-level |
| Detailed damage evidence | Official incident reports, municipal inspection updates, geolocated ground evidence, and GSI post-event aerial photographs | Event, municipality, site, or image footprint | Build a versioned evidence registry for functional housing loss | Official totals may lack locations; overhead imagery misses roof-intact and internal failures |
| Older population | e-Stat 2020 Census mesh table `T001231` | Statistical mesh | Population aged 65+ and related household measures | Six years before the event; requires sensitivity analysis or newer municipal controls |
| Air temperature | JMA AMeDAS | Station, 10-minute/daily | Observed post-event heat and historical same-season baseline | Point observations; interpolation uncertainty |
| Surface temperature | MODIS `MOD11A2.061` | 1 km, 8-day | Spatial surface-heat heterogeneity and climatological anomaly | Land-surface temperature, not 2 m air temperature; cloud/QA filtering required |
| Immediate health outcome | FDMA heatstroke ambulance transport | Prefecture/day or week, age group | Timely elderly heat-health outcome proxy | Not mortality and not generally released at small-area level |
| Mortality | Vital Statistics or approved microdata | Depends on access | Final health outcome | Release lag, privacy restrictions, and likely insufficient daily small-area detail |

## Recommended study scope

- Event: the Kumamoto earthquake beginning on 2026-07-28.
- Common data and map extent: all of Kumamoto Prefecture.
- Primary focal area: Uki City, Hikawa Town, and Yatsushiro City, with additional focal
  locations added from official damage evidence.
- Comparison area: lower-damage locations within Kumamoto Prefecture selected using
  pre-event population, heat, urban form, and healthcare-access characteristics.
- Acute follow-up: event day through day 14 (2026-07-28 to 2026-08-11).
- Extended follow-up: event day through day 30 (2026-07-28 to 2026-08-27).
- Historical heat comparison: the same calendar windows in 2021-2025.
- Spatial design: preserve official damage totals as time-stamped lower-bound snapshots;
  geolocate official incidents, inspections, and ground evidence where possible; use
  aerial imagery as supporting evidence for visible damage concentration rather than as
  an exhaustive collapse detector; then aggregate supported functional-housing-loss
  evidence, population, heat, and accessibility to a common small-area grid. Use
  municipality or prefecture outcomes only when finer data cannot be obtained.

## Download plan

### Tier A: minimum viable study

| Data | Geographic and temporal subset | Status | Purpose |
|---|---|---|---|
| Evolving FDMA, prefecture, and municipal damage reports | Event reports for the core and extended areas through day 30 | FDMA reports 15 and 26-28 plus Kumamoto City meetings 1-9 acquired; other municipalities pending | Official damage, evacuation, utility, shelter, and health context |
| GSI post-event aerial imagery and metadata | Acquire all available event-photo coverage across the prefecture while retaining explicit coverage limits | All official catalogues, 2,910 thumbnails, all 2,910 full-resolution photos, and 9 rapid-orthophoto sample tiles acquired | Visible-damage screening and coverage assessment |
| Seismic intensity and ground-motion evidence | Kumamoto Prefecture event observations and any official gridded estimate | Pending | Separate earthquake hazard from observed damage |
| Building footprints and administrative boundaries | All of Kumamoto Prefecture | 2020 small-area boundary and GSI vector-map building tiles at zooms 14 and 15 acquired | Prefecture-wide base map, building candidates, and spatial joins |
| Small-area older-population statistics and mesh geometry | Kumamoto Prefecture; retain 65+, 75+, very old, older-alone, and older-couple categories | Statistical table, matching 125 m mesh boundaries, and two analysis-ready GeoParquet layers completed | Population vulnerability and exposed counts |
| JMA air temperature and humidity | Event window through day 30 for nearby stations; same dates in 2021-2025 | Initial five-station window and monthly history acquired; continuation pending | Primary heat exposure and historical anomaly |
| Official heat-stress or WBGT observations | All available prefecture stations for the acute and extended windows and historical comparison | Pending | Humidity-sensitive physiological heat exposure |
| Shelter, evacuation, power, water, and cooling-access records | All prefecture municipalities where available, event day through day 30 | 1,315 designated shelters and 1,713 emergency evacuation sites acquired; operational and cooling attributes pending | Test the housing-loss and reduced-protection mechanism |
| Heatstroke ambulance and other acute health reports | Pre-event comparison and post-event weeks, by age and smallest available geography | Pre-event FDMA week acquired; post-event reports pending | Immediate health outcome or context indicator |

### Tier B: spatial refinement and robustness

| Data | Subset | Purpose |
|---|---|---|
| Sentinel-1 SAR | A small set of matched pre/post acquisitions over the study area | Neighborhood-level change or coherence proxy under cloud |
| Sentinel-2 or Landsat optical imagery | Nearest usable pre/post scenes | Context, debris or land-cover change; not primary single-building labels |
| MODIS Terra/Aqua land-surface temperature | July-August 2021-2026, clipped to the study area | Surface-heat pattern and anomaly; sensitivity at 1 km |
| Land cover, vegetation, imperviousness, and elevation | All of Kumamoto Prefecture | Explain spatial heat differences and interpolation error |
| Hospitals, clinics, care facilities, public halls, schools, shelters, and roads | All of Kumamoto Prefecture | Four MLIT point layers acquired for medical, care, public-facility, and school accessibility; roads pending |
| 2026 municipal resident-register totals | All prefecture municipalities | Scale or sensitivity-check the 2020 census baseline |

### Tier C: access-dependent outcome and validation data

Request rather than bulk-download these data:

- geocoded or mesh-level official building-damage inspection records;
- daily ambulance dispatch or emergency-department records with age and location;
- shelter entry and exit counts by age or care need;
- daily municipality or geocoded mortality, including cause and disaster-related status;
- power interruption, indoor temperature, cooling availability, and care-continuity records.

### Explicit exclusions for the first pass

Do not initially download nationwide imagery, all Landsat scenes, five years of full-resolution
10-minute weather for all Japanese stations, or national mortality microdata. These additions
would greatly increase storage and processing without improving the core event comparison.

## Temperature window

For the 2026 event, use 2021-2025 observations for the same calendar days as the primary
five-year climatological baseline. Compare the post-event period beginning 2026-07-28
against that baseline. Do not use a generic annual mean. Keep daytime maximum, nighttime
minimum, humidity or WBGT, and consecutive hot nights as separate candidate exposures.

## Building-damage recommendation

Landsat's 30 m optical pixels are too coarse for reliable individual-house collapse
classification. GSI 2026 post-event aerial photographs can support geolocation, coverage
assessment, and visible-damage hotspot screening, but they cannot exhaustively classify
Japanese residential habitability from overhead appearance. Sentinel-1 coherence or
other SAR change measures can be added as neighborhood-level damage proxies. Official
inspections, incident reports, utility or access disruptions, and geolocated ground
evidence remain the primary basis for functional housing-loss labels.
Use the GSI vector-map zoom-15 building layer as the pre-event candidate geometry. Because
the experimental layer contains both polygons and outline lines, includes buffered copies
across adjacent tiles, and does not provide stable building identifiers, its raw decoded
feature count is not a defensible building or dwelling count. Polygon filtering, unique
tile ownership, prefecture-boundary filtering, and exact-geometry deduplication must
precede any reported mapped-building count.

## Acquisition status

The reproducible acquisition script is `src/exp/acquire_kumamoto_2026.py`. It downloads
the credential-free first-pass bundle and writes checksums to
`data/raw/_manifests/kumamoto_2026_initial.csv`.

The rapid-assessment extension is reproducible with
`src/data/acquire_rapid_assessment_inputs.py`; its checksums and source limitations are in
`data/raw/_manifests/kumamoto_2026_rapid_assessment.csv`. The 2026-08-02 snapshot added:

- FDMA reports 26-28, providing intraday updates to prefecture housing-damage and
  evacuation-instruction totals through 2026-08-01 at 17:00;
- the Kumamoto City disaster-headquarters webpage through meeting 9 and the detailed
  96-page meeting-9 packet, providing municipal and ward-level housing, shelter,
  evacuation, outage, water-service, cooling, and heat-response evidence;
- 1,315 official designated shelters and 1,713 designated emergency evacuation sites for
  Kumamoto Prefecture, in both CSV and GeoJSON;
- the GSI 2026-07-31 interpreted surface-displacement-boundary PDF;
- 2,045 zoom-14 overview tiles and 7,671 zoom-15 building-analysis tiles from the GSI
  vector map current on 2026-04-01; and
- per-tile URLs, byte sizes, SHA-256 checksums, and building-fragment diagnostics.

The zoom-15 source files total 248,035,887 bytes and contain 2,460,144 decoded building
fragments. This is a coverage diagnostic only. It must not be interpreted as the number
of buildings, dwellings, damaged buildings, or collapsed houses.

The reproducible building preprocessing script is
`src/preprocessing/preprocess_gsi_kumamoto_buildings.py`. It excludes 1,280,001 non-polygon
features, 113,446 polygons owned by adjacent buffered tiles, 30,106 polygons whose
representative points are outside Kumamoto Prefecture, and one exact geometry duplicate.
The resulting layer contains 1,036,590 unique mapped building polygons. This is a pre-event
spatial stock layer and still must not be interpreted as dwellings, occupied homes, or
destroyed buildings.

The MLIT National Land Numerical Information point-data extension is reproducible with
`src/data/acquire_mlit_ksj_points.py`; checksums and source limitations are in
`data/raw/_manifests/kumamoto_mlit_ksj_points_2026-08-02.csv`. It added four Kumamoto
Prefecture facility layers:

- 2,561 medical institutions from the 2020 reference year;
- 4,470 welfare facilities from the 2023 reference year;
- 1,660 municipal offices and public assembly facilities from the 2022 reference year;
  and
- 917 schools from the 2023 reference year.

All four are point layers in JGD2011. They support accessibility and facility cross-checks,
but their reference years precede the earthquake and they do not verify current opening,
post-event functionality, cooling equipment, or willingness to accept evacuees.

The initial 2026-08-02 acquisition manifest contains 66 available source files and no
unavailable records. A separate event-imagery acquisition subsequently added:

- the complete official GSI event-layer definition and 10 GeoJSON catalogues;
- 2,910 unique aerial-photo records and all 2,910 thumbnails (approximately 106 MB);
- all 2,910 full-resolution photographs from the 9 photo layers, totaling
  14,969,606,506 bytes (approximately 14.97 GB), with zero failed records;
- nine zoom-level-18 rapid-orthophoto sample tiles; and
- camera-centre coverage in 20 of the 49 city/ward units represented by the administrative
  boundary layer, noting that image footprints extend beyond the camera points.

The initial manifest includes:

- one FDMA earthquake report and one GSI event-page snapshot;
- one e-Stat archive plus its extracted `T001231` table (62,947 lines including two
  header rows and 50 statistical fields);
- five official e-Stat 125 m mesh-boundary packages covering the first-order mesh blocks
  M4829, M4830, M4831, M4930, and M4931, plus one 2020 Census small-area boundary package
  for all of Kumamoto Prefecture;
- 30 event-window AMeDAS files for Kumamoto, Misumi, Kosa, Matsushima, and Yatsushiro
  from 2026-07-28 through 2026-08-02;
- 24 JMA historical monthly pages for Kumamoto and Yatsushiro, July and August of
  2021-2026;
- one FDMA pre-event heatstroke ambulance report for 2026-07-20 through 2026-07-26.

FDMA report 15 is explicitly preliminary. Its housing-damage columns are still blank,
although it identifies specific structural failures. Report 28 supplies the latest
acquired prefecture-level preliminary snapshot of 181 fully collapsed, 245 half-collapsed,
and 1,419 partially damaged residences, for a total of 1,845. Kumamoto City reports four
fully collapsed residences and approximately 35 additional residences ranging from partial
damage to half collapse in Minami Ward; its pre-assessment identifies Tomiai and Jonan as
the main damage cluster. The remaining prefecture total still lacks municipality or
building locations needed for grid allocation. The
pre-event FDMA heatstroke report records 220 transports in Kumamoto Prefecture, of which
134 were people aged 65 or older. The Kumamoto AMeDAS event-day file records a daily
maximum of 38.5 degrees C and minimum of 27.8 degrees C on 2026-07-28.

Boundary validation found 1,574,400 standard 125 m cells across the five first-order mesh
packages. All 62,945 population-table `KEY_CODE` values matched a boundary `KEY_CODE`, with
zero unmatched rows. The prefecture-wide 2020 small-area layer contains 3,101 polygons.
The raw and extracted boundary bundle occupies approximately 328 MB. Analytical processing
should join population first and retain the 62,945 populated/statistically reported cells
rather than carrying every empty standard cell into later maps.

MODIS and the complete rapid-orthophoto tile pyramid remain deferred. Cooling equipment,
backup power, current shelter occupancy, usable cooled floor area, and current opening
status also remain unavailable from the national shelter layer and require municipal or
facility verification. The complete
thumbnail set should be used to prioritize cloudy, offshore, agricultural, and otherwise
low-value frames for exclusion from detailed review; the corresponding full-resolution
archive is now locally available. The FDMA heatstroke report for 2026-07-27 through
2026-08-02 should be added when released.

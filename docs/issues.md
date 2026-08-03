# Research Output Issues

## Issues

| # | item | type | severity | description |
|---:|---|---|---|---|
| 1 | Figure_03_event_window_daytime_nighttime_heat_scenario.png | figure | major | The connected 2026 daytime series includes 2026-08-03 values observed only through 07:40 JST (32.6% daily completeness). Although open markers identify partial station-days, connecting these provisional maxima to prior complete days creates a visually prominent but non-comparable temperature drop and can be read as evidence that daytime heat has subsided. |
| 2 | Figure_02_minami_ward_shelter_cooling_risk_screening.png | figure/script | major | The script labels every geolocated record with `Asset Type == shelter` as a confirmed unavailable shelter without explicitly requiring the planned verification, availability, or cooling-loss conditions. It also does not use `Cooling Loss Confirmed`, `Evidence Tier`, or `Verification Status` as specified in the plan, so future shelter evidence rows could be misclassified. |
| 3 | figure_01_kumamoto_population_vulnerability_map.png | figure | major | This figure is stored in the research-results directory but has no corresponding entry in AnaSOP Section 8. It supports the population-baseline question, but its purpose, variables, and status have not been formally mapped to Sections 5-7 and the figure plan. |
| 4 | figure_01_kumamoto_population_vulnerability_map.py; figure_minami_ward_shelter_and_cooling_risk_screening.py | script | major | Both analysis scripts read the administrative boundary shapefile directly from `data/raw/`. This bypasses the processed-data contract used by the other analytical inputs and leaves boundary selection and municipal-area construction outside the documented preprocessing pipeline. |
| 5 | figure_01_kumamoto_population_vulnerability_map.png | figure | minor | The image contains a visible figure title, subtitle, and uppercase panel headings (`A.` and `B.`), conflicting with the no-title rule and lowercase standalone panel-label convention. |
| 6 | Figure_02_minami_ward_shelter_cooling_risk_screening.png | figure | minor | Both panels use `set_title()` to combine lowercase panel labels with descriptive panel titles. The panel labels are readable, but the embedded panel titles do not conform to the no-title output rule. |
| 7 | Figure_02_minami_ward_shelter_cooling_risk_screening.png; Figure_03_event_window_daytime_nighttime_heat_scenario.png | output naming | minor | The numeric filename prefixes and shortened slugs prevent the output-inventory tool from matching these files to their completed AnaSOP titles. The figures exist and visually match the planned items, but automated checks report them as both unplanned and missing. |
| 8 | Figure_03_event_window_daytime_nighttime_heat_scenario.png | figure | minor | The historical-band legend does not state that the reference range contains only Kumamoto and Yatsushiro observations, whereas the 2026 overlay contains five stations. The underlying AnaSOP is explicit, but the standalone figure can be misread as using historical records from all five stations. |

## Severity Summary

| severity | count |
|---|---:|
| critical | 0 |
| major | 4 |
| minor | 4 |

## Recommended Next Steps

- 返回 `figure-table-generation` 修改图 3：不要把未达到白天阈值的部分日最高温连接为完整日序列；可只显示不连线的空心点，并标注最新观测截止时间。历史图例同时注明历史范围仅来自 Kumamoto 与 Yatsushiro 两站。
- 返回 `data-preprocessing` 明确定义避难所“确认不可用”和“确认失去制冷”的可分析字段，并把行政边界转换为受控的 processed parquet；随后重新运行 `estimation-framework-planning`，确保图 2 的筛选条件与 Section 4 变量一致。
- 返回 `figure-table-generation` 重写图 2 的证据筛选：显式检查可用状态、热保护损失机制、Evidence Tier 和 Verification Status，不再仅凭 `Asset Type` 与坐标分类。
- 使用 `figure-table-planning` 决定是否正式保留全县人口脆弱性图。若保留，将其加入 Section 8 并映射到 Sections 5-7；若不保留，应移出研究结果目录。
- 修订图 1、图 2 的可见标题和面板标签，并统一文件名与 AnaSOP 标题 slug，之后重新运行 `critique-research-outputs` 验证问题是否关闭。

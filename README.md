# Cancer Screening Rates Across US Demographics

## Overview
Cancer screening is one of the most effective tools for early detection and improved 
survival outcomes. However, screening rates vary significantly across demographic 
groups in the United States — by race, income, education, age, and geography — 
contributing to persistent health disparities.

This project analyzes real cancer screening data from the National Cancer Institute 
(NCI) and CDC to identify which population groups are underserved, and quantifies 
the magnitude of screening disparities across the United States.

## Public Health Significance
- Disparities in screening rates directly translate to disparities in survival outcomes
- Identifying underserved groups helps US public health agencies target interventions
- Breast, cervical, and colorectal cancer screenings are proven to save lives when 
  adopted broadly across all demographic groups
- This analysis supports evidence-based policymaking for the US National Cancer Program

## Methods
- **Data wrangling** — cleaning and restructuring NCI SEER and CDC BRFSS screening data
- **Descriptive statistics** — screening rates by race, income, education, and state
- **Disparity quantification** — gap analysis between highest and lowest screening groups
- **Visualization** — bar charts, heatmaps, and choropleth maps of screening rates by state
- **Statistical testing** — chi-square tests to confirm significance of observed disparities

## Data Source
Data sourced from the [NCI State Cancer Profiles](https://statecancerprofiles.cancer.gov)

## Requirements
## How to Run
```bash
pip install -r requirements.txt
python src/screening_analysis.py
```

## Results
Key outputs include:
- Screening rate comparison across racial and ethnic groups
- State-by-state heatmap of cancer screening coverage
- Statistical confirmation of demographic disparities in screening uptake
- Identification of the most underserved population groups in the US

## Author
**Oreoluwa Oyetubo**

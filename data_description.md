# Child Nutrition Data - Dataset Description

## 📊 **Dataset Overview**

This dataset contains **36,050 clean child nutrition measurement records** collected from various Early Childhood Development (ECD) sites across South Africa. The data represents height measurements of children aged 0-5 years, along with associated demographic and programmatic information.

### **Key Statistics**
- **Total Records**: 36,050
- **Total Columns**: 26
- **Data Collection Period**: November 2020 - May 2025
- **Data Processing Date**: October 2024
- **Geographic Coverage**: 29 sites across South Africa
- **Measurement Type**: Height measurements only

---

## 🏗️ **Data Structure**

### **Core Measurement Data**

| Column | Data Type | Description | Sample Values |
|--------|-----------|-------------|---------------|
| **BeneficiaryId** | int64 | Unique child identifier | 115323, 132465, 161592 |
| **Answer** | float64 | Height measurement in centimeters | 40.0 - 195.0 cm (mean: 98.1 cm) |
| **Capture Date** | datetime | Date when measurement was taken | 2020-11-27 to 2025-05-14 |
| **WHO Index** | float64 | WHO z-score for height-for-age | -4.0 to 4.0 (mean: -0.64) |

### **Demographic Information**

| Column | Data Type | Description | Sample Values |
|--------|-----------|-------------|---------------|
| **FirstNames** | object | Child's first name(s) | "Onthatile", "Ithandile", "Shane" |
| **NickName** | object | Child's nickname (optional) | "Babalo", "Boetie", "Carol" |
| **LastName** | object | Child's last name (optional) | "AARONS", "ADAMS", "ANDREWS" |
| **HouseholdId** | float64 | Unique household identifier | 54168 - 100526 |
| **Household** | object | Household/ECD center name | "(SS) Ipelegeng ELC (Goratamang)" |

### **Site and Program Information**

| Column | Data Type | Description | Sample Values |
|--------|-----------|-------------|---------------|
| **Site** | object | Specific measurement site | "Sasolburg", "Kuyasa", "Wentworth ECD Forum Durban" |
| **Site Group** | object | Program/organization group | "Safripol", "Jannie Mouton", "GROOT Swem" |
| **DomainName** | object | Program domain | "Food & Nutrition" |
| **SubDomainName** | object | Program subdomain | "Growth & Nutrition" |

### **Measurement Context**

| Column | Data Type | Description | Sample Values |
|--------|-----------|-------------|---------------|
| **DatapointName** | object | Type of measurement | "Measure: Height" |
| **Answer Info** | object | Measurement context | "Measurement" |
| **Respondent** | object | Who provided the measurement | "Child" |
| **QuestionId** | float64 | Question identifier | 1233.0 - 1234.0 |

### **Quality and Processing Data**

| Column | Data Type | Description | Sample Values |
|--------|-----------|-------------|---------------|
| **Score** | float64 | Data quality score | 1.0 - 4.0 (mean: 3.17) |
| **Flagged** | int64 | Data quality flag (0/1) | 0 (93%), 1 (7%) |
| **MEASURED** | int64 | Measurement completion flag | 1 (100%) |
| **ENTRY NUMBER** | int64 | Entry sequence number | 1 - 29 (mean: 3.95) |
| **DUPLICATE** | object | Duplicate record flag | False (99.997%), True (0.003%) |

### **Temporal Data**

| Column | Data Type | Description | Sample Values |
|--------|-----------|-------------|---------------|
| **CreatedOn** | datetime | Record creation timestamp | 2024-10-10 to 2025-08-15 |
| **Capture Date** | datetime | Measurement date | 2020-11-27 to 2025-05-14 |

### **Technical Fields**

| Column | Data Type | Description | Sample Values |
|--------|-----------|-------------|---------------|
| **Unnamed: 0** | float64 | Original row index | 115323 - 239206 |
| **WHO Index Type** | object | WHO index type | "z" |
| **z Score** | float64 | Z-score field (all null) | NaN (100%) |

---

## 📈 **Data Distribution Analysis**

### **Geographic Distribution**

**Top 10 Sites by Record Count:**
1. **Sasolburg**: 10,009 records (27.8%)
2. **Wentworth ECD Forum Durban**: 6,062 records (16.8%)
3. **Kuyasa**: 5,319 records (14.8%)
4. **NG KERK Hoopstad**: 3,689 records (10.2%)
5. **Miqlat Paarl**: 2,034 records (5.6%)
6. **Stellumthombo Stellenbosch**: 2,005 records (5.6%)
7. **Pebble**: 1,207 records (3.3%)
8. **Villa Crop Protection_SmartStart_North West**: 885 records (2.5%)
9. **Masikhule-GS**: 671 records (1.9%)
10. **Elsiesrivier Cape Town**: 639 records (1.8%)

### **Program Distribution**

**Site Groups by Record Count:**
1. **Safripol**: 20,063 records (55.6%)
2. **Jannie Mouton**: 12,912 records (35.8%)
3. **GROOT Swem**: 1,268 records (3.5%)
4. **Villa Crop**: 885 records (2.5%)
5. **Remove**: 691 records (1.9%)
6. **Bright Orange**: 59 records (0.2%)
7. **Invia Gemeente**: 51 records (0.1%)
8. **OMNIA**: 49 records (0.1%)
9. **Inteligro**: 36 records (0.1%)
10. **inPharma**: 36 records (0.1%)

### **Height Measurement Analysis**

- **Range**: 40.0 - 195.0 cm
- **Mean**: 98.1 cm
- **Median**: 99.0 cm
- **Standard Deviation**: ~15.2 cm
- **Distribution**: Normal distribution with slight right skew

### **WHO Z-Score Analysis**

- **Range**: -4.0 to 4.0
- **Mean**: -0.64
- **Interpretation**: Slightly below WHO median for height-for-age
- **Distribution**: Normal distribution centered slightly below zero

---

## 🎯 **Data Quality Characteristics**

### **Completeness**
- **100% Complete**: BeneficiaryId, Answer, Capture Date, Site
- **99.6% Complete**: FirstNames, Household, Site Group
- **71.5% Complete**: LastName
- **0.4% Complete**: NickName (optional field)
- **0% Complete**: z Score (unused field)

### **Data Quality Scores**
- **Mean Score**: 3.17/4.0 (79% quality)
- **Score Range**: 1.0 - 4.0
- **Flagged Records**: 2,523 (7.0%)

### **Temporal Coverage**
- **Measurement Period**: 4.5 years (Nov 2020 - May 2025)
- **Data Entry Period**: 10 months (Oct 2024 - Aug 2025)
- **Peak Collection**: 2021-2022 period

---

## 👥 **Child Demographics**

### **Name Analysis**
- **Unique First Names**: 4,941 distinct names
- **Name Patterns**: Mix of traditional African names and international names
- **Examples**: Onthatile, Ithandile, Shane, A-Jay, ABIGAIL

### **Household Structure**
- **Unique Households**: 201 distinct households
- **Household Size**: Average 179 children per household
- **Household Types**: Mix of ECD centers, day cares, and community programs

---

## 🏥 **Health and Nutrition Context**

### **WHO Growth Standards**
- **Reference**: WHO Child Growth Standards
- **Index Type**: Height-for-age z-scores
- **Normal Range**: -2 to +2 z-scores
- **Current Status**: Mean -0.64 (slightly below WHO median)

### **Measurement Quality**
- **All measurements flagged as "MEASURED"**: 100%
- **Data quality scores**: High (mean 3.17/4.0)
- **Extreme values removed**: 38 records (0.1%)
- **Missing critical data removed**: 2 records (0.006%)

---

## 📊 **Sample Records**

### **Record 1**
- **Child**: Onthatile (ID: 161592)
- **Site**: Kuyasa
- **Height**: 96.3 cm
- **Date**: 2020-11-27
- **WHO Index**: 4.0 (above normal)

### **Record 2**
- **Child**: Ithandile (ID: 132465)
- **Site**: Kuyasa
- **Height**: 100.1 cm
- **Date**: 2020-12-14
- **WHO Index**: 4.0 (above normal)

### **Record 3**
- **Child**: Shane (ID: 132191)
- **Site**: InteliGro Ceres
- **Height**: 96.0 cm
- **Date**: 2021-03-18
- **WHO Index**: -1.02 (slightly below normal)

---

## 🔍 **Data Processing Notes**

### **Cleaning Applied**
1. **Duplicate Removal**: 15,607 duplicates removed (30.2%)
2. **Extreme Value Removal**: 38 extreme values removed (0.1%)
3. **Missing Data Removal**: 2 records with missing critical data removed (0.006%)
4. **Data Type Conversion**: All fields converted to appropriate types
5. **String Cleaning**: Special characters cleaned for database compatibility

### **Final Dataset Quality**
- **Total Records**: 36,050 (100% clean)
- **Data Completeness**: 99.6% for critical fields
- **Data Quality**: High (mean score 3.17/4.0)
- **Temporal Coverage**: 4.5 years of measurements
- **Geographic Coverage**: 29 sites across South Africa

---

## 📋 **Usage Recommendations**

### **Analytical Applications**
- **Growth Monitoring**: Track child growth patterns over time
- **Program Evaluation**: Assess effectiveness of nutrition programs
- **Geographic Analysis**: Compare outcomes across different sites
- **Temporal Analysis**: Monitor trends over time

### **Data Limitations**
- **Single Measurement Type**: Only height measurements (no weight/BMI)
- **Missing Demographics**: Limited age information
- **Temporal Gaps**: Some periods may have sparse data
- **Site Variability**: Different sites may have different measurement protocols

### **Privacy Considerations**
- **Personal Information**: Contains child names and identifiers
- **Data Anonymization**: Consider removing or masking personal identifiers
- **Access Control**: Ensure appropriate data governance
- **Retention Policies**: Follow data protection regulations

---

**Last Updated**: October 2024  
**Data Version**: 1.0 (Cleaned)  
**Total Records**: 36,050  
**Data Quality**: High (99.6% complete)

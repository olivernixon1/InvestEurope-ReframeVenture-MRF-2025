from .options_fund import OPTIONS_FUND

SCHEMA_FUND = {

    #0.1.1
    #String
    "fund_name": {
        "type": "string",
    },
    
    #0.2.1
    #STRING from yes_no_best_efforts
    "legal_esg_commitment": {
        "type": "string",
        "allowed": list(OPTIONS_FUND["yes_no_best_efforts"].keys()),
    },
    
    #0.2.2
    #STRING from yes_no_asset_scope
    "esg_investment_policy": {
        "type": "string",
        "allowed": list(OPTIONS_FUND["yes_no_asset_scope"].keys()),
    },
    
    #0.2.3
    #STRING from yes_no_asset_scope
    "climate_change_investment_policy": {
        "type": "string",
        "allowed": list(OPTIONS_FUND["yes_no_asset_scope"].keys()),
    },
    
    #0.2.4
    #STRING from yes_no_best_efforts
    "diversity_in_term_sheets_shareholder_agreements": {
        "type": "string",
        "allowed": list(OPTIONS_FUND["yes_no_best_efforts"].keys()),
    },
    
    #NEW in 2025
    #0.2.5
    #STRING from yes_no_best_efforts
    "adhere_to_ungc": {
        "type": "string",
        "allowed": list(OPTIONS_FUND["yes_no_best_efforts"].keys()),
    },
    
    #NEW in 2025
    #0.2.5.1
    #STRING from yes_no_best_efforts
    "no_ungc_explanation": {
        "type": "string",
    },
    
    #0.3.1
    #STRING from yes_no_asset_scope
    "esg_engagement_process": {
        "type": "string",
        "allowed": list(OPTIONS_FUND["yes_no_asset_scope"].keys()),
    },
    
    #0.3.2
    #STRING from yes_no_asset_scope
    "esg_monitoring_processes": {
        "type": "string",
        "allowed": list(OPTIONS_FUND["yes_no_asset_scope"].keys()),
    },
    
    #0.3.3
    #STRING from yes_no_incident_process
    "esg_incident_report_process": {
        "type": "string",
        "allowed": list(OPTIONS_FUND["yes_no_incident_process"].keys()),
    },
    
    #0.3.4
    #STRING from yes_no
    "good_governance_due_diligence": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #Updated validation options in 2025
    #0.3.5
    #STRING from yes_no
    "good_governance_post_investment": {
        "type": "string",
        "allowed": list(OPTIONS_FUND["yes_no_periods"].keys()),
    },
    
    #NEW in 2025
    #0.3.6
    #STRING from yes_no
    "responsible_ai_dd": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    
    #1.1.1
    #STRING from yes_no_incident_process
    "fund_marketing_under_sfdr": {
        "type": "string",
        "allowed": list(OPTIONS_FUND["sfdr_classification"].keys()),
    },
    
    #1.2.1
    #STRING from yes_no
    "article_8_sustainable_investment_commitment": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.2.1.1
    #Float between 0 and 100
    "article_8_sustainable_investment_commitment_minimum_share_percentage": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #1.2.2
    #STRING from yes_no
    "article_8_eu_taxonomy_alignment": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.2.2.1
    #Float between 0 and 100
    "article_8_eu_taxonomy_alignment_minimum_share_percentage": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #1.2.3
    #STRING from yes_no
    "article_8_non_eu_taxonomy_environmental_objective": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.2.3.1
    #Float between 0 and 100
    "article_8_non_eu_taxonomy_environmental_objective_minimum_share_percentage": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #1.2.4
    #STRING from yes_no
    "article_8_social_objective_investment": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.2.4.1
    #Float between 0 and 100
    "article_8_social_objective_investment_minimum_share_percentage": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #1.2.5
    #STRING from yes_no
    "article_8_considers_significant_negative_impacts": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.2.6
    #STRING from yes_no
    "article_8_ghg_reduction_target": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.2.6.1
    #STRING from ghg_reduction_strategies
    "article_8_ghg_reduction_target_main_strategy": {
        "type": "string",
        "allowed": list(OPTIONS_FUND["ghg_reduction_strategies"].keys()),
    },
    
    #1.2.6.2
    #Float between 0 and 100
    "article_8_ghg_reduction_target_ambition": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #1.2.6.3
    #Float (positive)
    "article_8_ghg_reduction_target_financed_emissions_baseline":  {"type": "float", 'min': 0},
    
    #1.2.6.4
    #Float between 1900 and 2030
    "article_8_ghg_reduction_target_base_year": {
        "type": "integer",
        "min": 1900,
        "max": 2030,
    },
    
    #1.2.6.5
    #Float between 2000 and 2200
    "article_8_ghg_reduction_target_target_year": {
        "type": "integer",
        "min": 2000,
        "max": 2200,
    },
    
    #1.2.6.6
    #Float (positive)
    "article_8_ghg_reduction_target_financed_emissions_reporting":  {"type": "float", 'min': 0},
    
    #1.2.7
    #STRING from yes_no
    "article_8_uses_index_as_reference_benchmark": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.3.1
    #STRING from yes_no
    "article_9_sustainable_investment_commitment": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.3.1.1
    #Float between 0 and 100
    "article_9_sustainable_investment_commitment_minimum_share_percentage": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #1.3.2
    #STRING from yes_no
    "article_9_eu_taxonomy_alignment": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.3.2.1
    #Float between 0 and 100
    "article_9_eu_taxonomy_alignment_minimum_share_percentage": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #1.3.3
    #STRING from yes_no
    "article_9_non_eu_taxonomy_environmental_objective": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.3.3.1
    #Float between 0 and 100
    "article_9_non_eu_taxonomy_environmental_objective_minimum_share_percentage": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #1.3.4
    #STRING from yes_no
    "article_9_social_objective_investment": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.3.4.1
    #Float between 0 and 100
    "article_9_social_objective_investment_minimum_share_percentage": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #1.3.5
    #STRING from yes_no
    "article_9_considers_significant_negative_impacts": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.3.6
    #STRING from yes_no
    "article_9_ghg_reduction_target": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.3.6.1
    #STRING from ghg_reduction_strategies
    "article_9_ghg_reduction_target_main_strategy": {
        "type": "string",
        "allowed": list(OPTIONS_FUND["ghg_reduction_strategies"].keys()),
    },
    
    #1.3.6.2
    #Float between 0 and 100
    "article_9_ghg_reduction_target_ambition": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #1.3.6.3
    #Float (positive)
    "article_9_ghg_reduction_target_financed_emissions_baseline":  {"type": "float", 'min': 0},
    
    #1.3.6.4
    #Float between 1900 and 2030
    "article_9_ghg_reduction_target_base_year": {
        "type": "integer",
        "min": 1900,
        "max": 2030,
    },
    
    #1.3.6.5
    #Float between 2000 and 2200
    "article_9_ghg_reduction_target_target_year": {
        "type": "integer",
        "min": 2000,
        "max": 2200,
    },
    
    #1.3.6.6
    #Float (positive)
    "article_9_ghg_reduction_target_financed_emissions_reporting":  {"type": "float", 'min': 0},
    
    #1.3.6.7
    #STRING from ghg_reduction_strategies
    "article_9_ghg_reduction_target_1_5_c_aligned": {
        "type": "string",
        "allowed": list(OPTIONS_FUND["yes_no_not_assessed"].keys()),
    },
    
    #1.3.7
    #STRING from yes_no
    "article_9_uses_index_as_reference_benchmark": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #2.1.1
    #Integer (positive)
    "total_number_of_partners": {"type": "integer", 'min': 0},
    
    #2.1.2
    #Integer (positive)
    "number_of_partners_female": {"type": "integer", 'min': 0},
    
    #2.1.3
    #Integer (positive)
    "number_of_partners_non_binary": {"type": "integer", 'min': 0},
    
    #2.1.4
    #Integer (positive)
    "number_of_partners_non_disclosed": {"type": "integer", 'min': 0},
    
    #2.1.5
    #Integer (positive)
    "number_of_partners_male": {"type": "integer", 'min': 0},
    
    #2.1.6
    #STRING from yes_no
    "gender_diversity_pipeline_tracked": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #2.1.6.1
    #Float between 0 and 100
    "gender_diversity_pipeline_strategy_fit": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #2.1.6.2
    #Float between 0 and 100
    "gender_diversity_pipeline_dd_undertaken": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #2.1.6.3
    #Float between 0 and 100
    "gender_diversity_pipeline_term_sheet_issued": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
}

# Dictionary mapping compound IDs to their units
FUND_COMPOUND_ID_UNITS = {
    "article_8_sustainable_investment_commitment_minimum_share_percentage": "%",
    "article_8_eu_taxonomy_alignment_minimum_share_percentage": "%",
    "article_8_non_eu_taxonomy_environmental_objective_minimum_share_percentage": "%",
    "article_8_social_objective_investment_minimum_share_percentage": "%",
    "article_8_ghg_reduction_target_ambition": "%",
    "article_8_ghg_reduction_target_financed_emissions_baseline": "tCO2e/M€",
    "article_8_ghg_reduction_target_financed_emissions_reporting": "tCO2e/M€",
    
    "article_9_sustainable_investment_commitment_minimum_share_percentage": "%",
    "article_9_eu_taxonomy_alignment_minimum_share_percentage": "%",
    "article_9_non_eu_taxonomy_environmental_objective_minimum_share_percentage": "%",
    "article_9_social_objective_investment_minimum_share_percentage": "%",
    "article_9_ghg_reduction_target_ambition": "%",
    "article_9_ghg_reduction_target_financed_emissions_baseline": "tCO2e/M€",
    "article_9_ghg_reduction_target_financed_emissions_reporting": "tCO2e/M€",
    
    "total_number_of_partners": "people",
    "number_of_partners_female": "people",
    "number_of_partners_non_binary": "people",
    "number_of_partners_non_disclosed": "people",
    "number_of_partners_male": "people",
    
    "gender_diversity_pipeline_strategy_fit": "%",
    "gender_diversity_pipeline_dd_undertaken": "%",
    "gender_diversity_pipeline_term_sheet_issued": "%",
}

ALL_FUND_METRICS = [
  "fund_name",
  "legal_esg_commitment",
  "esg_investment_policy",
  "climate_change_investment_policy",
  "diversity_in_term_sheets_shareholder_agreements",
  "adhere_to_ungc",
  "no_ungc_explanation",
  "esg_engagement_process",
  "esg_monitoring_processes",
  "esg_incident_report_process",
  "good_governance_due_diligence",
  "good_governance_post_investment",
  "responsible_ai_dd",
  "fund_marketing_under_sfdr",
  "article_8_sustainable_investment_commitment",
  "article_8_sustainable_investment_commitment_minimum_share_percentage",
  "article_8_eu_taxonomy_alignment",
  "article_8_eu_taxonomy_alignment_minimum_share_percentage",
  "article_8_non_eu_taxonomy_environmental_objective",
  "article_8_non_eu_taxonomy_environmental_objective_minimum_share_percentage",
  "article_8_social_objective_investment",
  "article_8_social_objective_investment_minimum_share_percentage",
  "article_8_considers_significant_negative_impacts",
  "article_8_ghg_reduction_target",
  "article_8_ghg_reduction_target_main_strategy",
  "article_8_ghg_reduction_target_ambition",
  "article_8_ghg_reduction_target_financed_emissions_baseline",
  "article_8_ghg_reduction_target_base_year",
  "article_8_ghg_reduction_target_target_year",
  "article_8_ghg_reduction_target_financed_emissions_reporting",
  "article_8_uses_index_as_reference_benchmark",
  "article_9_sustainable_investment_commitment",
  "article_9_sustainable_investment_commitment_minimum_share_percentage",
  "article_9_eu_taxonomy_alignment",
  "article_9_eu_taxonomy_alignment_minimum_share_percentage",
  "article_9_non_eu_taxonomy_environmental_objective",
  "article_9_non_eu_taxonomy_environmental_objective_minimum_share_percentage",
  "article_9_social_objective_investment",
  "article_9_social_objective_investment_minimum_share_percentage",
  "article_9_considers_significant_negative_impacts",
  "article_9_ghg_reduction_target",
  "article_9_ghg_reduction_target_main_strategy",
  "article_9_ghg_reduction_target_ambition",
  "article_9_ghg_reduction_target_financed_emissions_baseline",
  "article_9_ghg_reduction_target_base_year",
  "article_9_ghg_reduction_target_target_year",
  "article_9_ghg_reduction_target_financed_emissions_reporting",
  "article_9_ghg_reduction_target_1_5_c_aligned",
  "article_9_uses_index_as_reference_benchmark",
  "total_number_of_partners",
  "number_of_partners_female",
  "number_of_partners_non_binary",
  "number_of_partners_non_disclosed",
  "number_of_partners_male",
  "gender_diversity_pipeline_tracked",
  "gender_diversity_pipeline_strategy_fit",
  "gender_diversity_pipeline_dd_undertaken",
  "gender_diversity_pipeline_term_sheet_issued"
]


REQUIRED_FUND_METRICS = [
    "fund_name",
    "legal_esg_commitment",
    "esg_investment_policy",
    "climate_change_investment_policy",
    "diversity_in_term_sheets_shareholder_agreements",
    "esg_engagement_process",
    "esg_monitoring_processes",
    "esg_incident_report_process",
    "good_governance_due_diligence",
    "good_governance_post_investment",
    "responsible_ai_dd",
    "fund_marketing_under_sfdr",
    "total_number_of_partners",
    "number_of_partners_female",
    "number_of_partners_non_binary",
    "number_of_partners_non_disclosed",
    "number_of_partners_male",
    "gender_diversity_pipeline_tracked",
]
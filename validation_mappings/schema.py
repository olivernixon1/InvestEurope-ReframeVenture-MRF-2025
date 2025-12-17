from .options import OPTIONS

SCHEMA_PORTCO = {

    #0.1.1
    #String
    "company_name": {
        "type": "string",
    },

    #0.1.2
    #String
    "business_identification_number": {
        "type": "string",
    },

    #0.1.2.1
    #String
    #Updated in 2025
    "business_identification_number_system": {
        "type": "string",
         "allowed": list(OPTIONS["business_identification_system"].keys()),
    },

    #0.1.3
    #STRING from country_list
    "country_of_domicile": {
        "type": "string",
        "allowed": list(OPTIONS["country_list"].keys()),
    },

    #0.1.4
    #STRING from country_list
    "primary_country_of_operations": {
        "type": "string",
        "allowed": list(OPTIONS["country_list"].keys()),
    },

    #0.1.5
    #STRING from country_list
    "other_EU_country_of_operation_1": {
        "type": "string",
        "allowed": list(OPTIONS["eu_country_list"].keys()),
    },
    
    #0.1.5.1
    #STRING from country_list
    "other_EU_country_of_operation_2": {
        "type": "string",
        "allowed": list(OPTIONS["eu_country_list"].keys()),
    },
    
    #0.1.6
    #STRING from nace_divisions
    "main_industry_classification": {
        "type": "string",
        "allowed": list(OPTIONS["nace_divisions"].keys()),
    },
    
    #0.1.7
    #Float (positive)
    "total_ftes_end_of_report_year": {"type": "float", 'min': 0},

    #0.1.8
    #Float (positive)
    "total_ftes_end_of_previous_report_year": {"type": "float", 'min': 0},

    #0.1.9
    #Float (positive)
    "gross_revenue": {"type": "float", 'min': 0},
    
    #0.1.9.1
    #Float (positive)
    "gross_revenue_inside_eu": {"type": "float", 'min': 0},
    
    #0.1.9.2
    #Float (positive)
    "gross_revenue_outside_eu": {"type": "float", 'min': 0},
    
    #0.1.10
    #Float (positive)
    "annual_balance_sheet_assets_total": {"type": "float", 'min': 0},
    
    #0.1.10.1
    #Float (positive)
    "annual_balance_sheet_assets_total_inside_eu": {"type": "float", 'min': 0},
    
    #0.1.10.2
    #Float (positive)
    "annual_balance_sheet_assets_total_outside_eu": {"type": "float", 'min': 0},

    #0.1.11
    #Float (positive)
    "turnover": {"type": "float", 'min': 0},
    
    #0.1.11.1
    #Float (positive)
    "turnover_inside_eu": {"type": "float", 'min': 0},
    
    #0.1.11.2
    #Float (positive)
    "turnover_outside_eu": {"type": "float", 'min': 0},

    #0.1.12
    #STRING from iso_currency_code
    "currency": {
        "type": "string",
        "allowed": list(OPTIONS["iso_currency_code"].keys()),
    },

    #0.1.13
    #STRING from yes_no
    "listed": {
        "type": "string",
        "allowed": ["yes", "no"],
    },

    #0.1.13.1
    #String
    "listed_ticker": {
        "type": "string",
    },
    
    #0.2.1.1
    #STRING from yes_no
    "code_of_conduct": {
       "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #0.2.1.2
    #STRING from yes_no
    "overall_sustainability_policy": {
        "type": "string",
        "allowed": ["yes", "no"],
    },

    #0.2.1.3
    #STRING from yes_no
    "environmental_policy": {
       "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #0.2.1.4
    #STRING from yes_no
    "anti_discrimination_and_equal_opportunities_policy": {
       "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #0.2.1.5
    #STRING from yes_no
    "diversity_inclusion_policy": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #0.2.1.6
    #STRING from yes_no
    "salary_remuneration_policy": {
       "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #0.2.1.7
    #STRING from yes_no
    "health_and_safety_policy": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #0.2.1.8
    #STRING from yes_no
    "human_rights_policy": {
       "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #0.2.1.9
    #STRING from yes_no
    "anti_corruption_bribery_policy": {
       "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #0.2.1.10
    #STRING from yes_no
    "data_privacy_security_policy": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    
    #0.2.1.11
    #STRING from yes_no
    "supply_chain_policy": {
       "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #
    # 0.2.1.12
    #STRING from yes_no_expanded
    "cybersecurity_data_management_policy": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # NEW in 2025
    # 0.2.1.13
    #STRING from yes_no_expanded
    "responsible_ai_policy": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # ALL 0.2.2 METRICS REMOVED IN 2025 UPDATE
    # #0.2.2
    # #STRING from yes_no
    # "dedicated_sustainability_staff": {
    #     "type": "string",
    #     "allowed": list(OPTIONS["yes_no_expanded"].keys()),
    # },

    # #0.2.2.1
    # #STRING from yes_no
    # "sustainability_staff_ceo": {
    #    "type": "string",
    #     "allowed": ["yes", "no"],
    # },
    
    # #0.2.2.2
    # #STRING from yes_no
    # "sustainability_staff_cso": {
    #     "type": "string",
    #     "allowed": ["yes", "no"],
    # },
    
    # #0.2.2.3
    # #STRING from yes_no
    # "sustainability_staff_cfo": {
    #    "type": "string",
    #     "allowed": ["yes", "no"],
    # },
    
    # #0.2.2.4
    # #STRING from yes_no
    # "sustainability_staff_board": {
    #     "type": "string",
    #     "allowed": ["yes", "no"],
    # },
    
    # #0.2.2.5
    # #STRING from yes_no
    # "sustainability_staff_management": {
    #    "type": "string",
    #     "allowed": ["yes", "no"],
    # },
    
    # #0.2.2.6
    # #STRING from yes_no
    # "sustainability_staff_none_of_above": {
    #     "type": "string",
    #     "allowed": ["yes", "no"],
    # },
    
    # NEW in 2025
    #0.2.3.1
    #STRING from yes_no
    "sustainability_responsibility_officer": {
       "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # NEW in 2025
    #0.2.3.2
    #STRING from yes_no
    "sustainability_responsibility_team": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # NEW in 2025
    #0.2.3.3
    #STRING from yes_no
    "sustainability_responsibility_referent": {
       "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # NEW in 2025
    #0.2.3.4
    #STRING from yes_no
    "sustainability_responsibility_cfo": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # NEW in 2025
    #0.2.3.5
    #STRING from yes_no
    "sustainability_responsibility_ceo": {
       "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # NEW in 2025
    #0.2.3.6
    #STRING from yes_no
    "sustainability_responsibility_cso": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # NEW in 2025
    #0.2.3.7
    #STRING from yes_no
    "sustainability_responsibility_management": {
       "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # NEW in 2025
    #0.2.3.8
    #STRING from yes_no
    "sustainability_responsibility_none": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # Removed in 2025 update
    # #0.3.1
    # #STRING from yes_no
    # "occurrence_of_esg_incidents": {
    #     "type": "string",
    #     "allowed": ["yes", "no"],
    # },

    #0.3.1.1
    #Integer (positive)
    "number_of_esg_incidents": {"type": "integer", 'min': 0},
    
    #0.3.1.2
    #String
    "qualitative_info_esg_incidents": {
        "type": "string",
    },

    #1.1.1
    #STRING from yes_no
    "eu_taxonomy_assessment": {
        "type": "string",
        "allowed": ["yes", "no"],
    },

    #1.1.1.1
    #Float between 0 and 100
    "percentage_turnover_eu_taxonomy": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },

    #1.1.1.2
    #Float between 0 and 100
    "percentage_capex_eu_taxonomy": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },

    #1.1.1.3
    #Float between 0 and 100
    "percentage_opex_eu_taxonomy": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #1.2.1
    #STRING from yes_no
    "tobacco_activities": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.2.1.1
    #Float between 0 and 100
    "percentage_turnover_tobacco_activities": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },

    #1.2.2
    #STRING from yes_no
    "hard_coal_and_lignite_activities": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.2.2.1
    #Float between 0 and 100
    "percentage_turnover_hard_coal_and_lignite_activities": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },

    #1.2.3
    #STRING from yes_no
    "oil_fuels_activities": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.2.3.1
    #Float between 0 and 100
    "percentage_turnover_oil_fuels_activities": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },

    #1.2.4
    #STRING from yes_no
    "gaseous_fuels_activities": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.2.4.1
    #Float between 0 and 100
    "percentage_turnover_gaseous_fuels_activities": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #1.2.5
    #STRING from yes_no
    "high_ghg_intensity_electricity_generation": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #1.2.5.1
    #Float between 0 and 100
    "percentage_turnover_high_ghg_intensity_electricity_generation": {
        "type": "float",
        "min": 0.0,
        "max": 100.0,
    },
    
    #1.3.1
    #STRING from yes_no
    "subject_to_csrd_reporting": {
        "type": "string",
        "allowed": ["yes", "no"],
    },

    #2.1.1
    #STRING from ems_presence_select
    "ems_implemented": {
        "type": "string",
        "allowed": list(OPTIONS["ems_presence_select"].keys()),
    },

    # MetriC ID Updated
    # 2.1.1.1
    #String
    "environmental_risk_tools": {
        "type": "string",
    },

    #2.2.1
    #STRING from ghg_scope_list
    "ghg_scope_measured_calculated": {
        "type": "string",
        "allowed": list(OPTIONS["ghg_scope_list"].keys()),
    },

    #2.2.2
    #Float (positive)
    "total_ghg_emissions": {"type": "float", 'min': 0},
    
    #2.2.3
    #Float (positive)
    "total_scope_1_emissions":  {"type": "float", 'min': 0},

    #2.2.3.1
    #STRING from ghg_scope_1_methodology
    "total_scope_1_emissions_methodology": {
        "type": "string",
        "allowed": list(OPTIONS["ghg_scope_1_methodology"].keys()),
    },

    #2.2.4
    #Float (positive)
    "total_scope_2_emissions":  {"type": "float", 'min': 0},

    #2.2.4.1
    #STRING from ghg_scope_2_methodology
    "total_scope_2_emissions_methodology": {
        "type": "string",
        "allowed": list(OPTIONS["ghg_scope_2_methodology"].keys()),
    },

    #2.2.5
    #Float (positive)
    "total_scope_3_emissions":  {"type": "float", 'min': 0},

    #2.2.5.1
    #STRING from ghg_scope_3_methodology
    "total_scope_3_emissions_methodology": {
        "type": "string",
        "allowed": list(OPTIONS["ghg_scope_3_methodology"].keys()),
    },

    # ALL METRICS FROM 2.2.5.2 - 2.2.5.16 REMOVED IN 2025
    # #2.2.5.2
    # #Float (positive)
    # "scope_3_emissions_purchased_goods_and_services": {"type": "float", 'min': 0},

    # #2.2.5.3
    # #Float (positive)
    # "scope_3_emissions_capital_goods": {"type": "float", 'min': 0},

    # #2.2.5.4
    # #Float (positive)
    # "scope_3_emissions_fuel_and_energy_related_not_in_scopes_1_2": {"type": "float", 'min': 0},

    # #2.2.5.5
    # #Float (positive)
    # "scope_3_emissions_upstream_transportation_distribution": {"type": "float", 'min': 0},

    # #2.2.5.6
    # #Float (positive)
    # "scope_3_emissions_waste_generated_in_operations": {"type": "float", 'min': 0},

    # #2.2.5.7
    # #Float (positive)
    # "scope_3_emissions_business_travel": {"type": "float", 'min': 0},

    # #2.2.5.8
    # #Float (positive)
    # "scope_3_emissions_employee_commuting": {"type": "float", 'min': 0},

    # #2.2.5.9
    # #Float (positive)
    # "scope_3_emissions_upstream_leased_assets": {"type": "float", 'min': 0},

    # #2.2.5.10
    # #Float (positive)
    # "scope_3_emissions_downstream_transportation_distribution": {"type": "float", 'min': 0},

    # #2.2.5.11
    # #Float (positive)
    # "scope_3_emissions_processing_of_sold_products": {"type": "float", 'min': 0},

    # #2.2.5.12
    # #Float (positive)
    # "scope_3_emissions_use_of_sold_products": {"type": "float", 'min': 0},

    # #2.2.5.13
    # #Float (positive)
    # "scope_3_emissions_endoflife_treatment_of_sold_products": {"type": "float", 'min': 0},

    # #2.2.5.14
    # #Float (positive)
    # "scope_3_emissions_downstream_leased_assets": {"type": "float", 'min': 0},

    # #2.2.5.15
    # #Float (positive)
    # "scope_3_emissions_franchises": {"type": "float", 'min': 0},
    
    # #2.2.5.16
    # #Float (positive)
    # "scope_3_emissions_investments": {"type": "float", 'min': 0},
    
    # New in 2025
    # 2.2.5.17
    # STRING from ghg_scope_3_sources
    "scope_3_primary_source": {
        "type": "string",
        "allowed": list(OPTIONS["ghg_scope_3_sources"].keys()),
    },
    
    # New in 2025
    # 2.2.5.18
    #Float (positive)
    "scope_3_primary_source_emissions": {"type": "float", 'min': 0},
    
    # New in 2025
    # 2.2.5.19
    # STRING from ghg_scope_3_sources
    "scope_3_secondary_source": {
        "type": "string",
        "allowed": list(OPTIONS["ghg_scope_3_sources"].keys()),
    },
    
    # New in 2025
    # 2.2.5.20
    #Float (positive)
    "scope_3_secondary_source_emissions": {"type": "float", 'min': 0},

    #2.3.1
    #STRING from decarbonisation_strategy
    "decarbonisation_strategy_set": {
        "type": "string",
        "allowed": list(OPTIONS["decarbonisation_strategy"].keys()),
    },

    # Updated option set in 2025
    # 2.3.2
    #STRING from ghg_reduction_target
    "ghg_reduction_target_set": {
        "type": "string",
        "allowed": list(OPTIONS["ghg_reduction_target"].keys()),
    },

    #2.3.3
    #STRING from long_term_net_zero_goal
    "long_term_net_zero_goal_set": {
        "type": "string",
        "allowed": list(OPTIONS["long_term_net_zero_goal"].keys()),
    },
    
    # New in 2025
    #2.3.4
    #STRING from yes_no_expanded
    "year_on_year_emissions_profile": {
        "type": "string",
        "allowed": list(OPTIONS["yes_no_expanded"].keys()),
    },
    
    # New in 2025
    # 2.3.4.1
    #String
    "year_on_year_emissions_profile_qualitative": {
        "type": "string",
    },
    
    # New in 2025
    #2.3.6
    #STRING from climate_solution_category
    "contribution_to_climate_solutions": {
        "type": "string",
        "allowed": list(OPTIONS["climate_solution_category"].keys()),
    },

    #2.4.1
    #Float (positive)
    "total_energy_consumption": {"type": "float", 'min': 0},

    #2.4.2
    #Float (positive)
    "energy_consumption_renewable": {"type": "float", 'min': 0},
    
    #2.5.1
    #Float (positive)
    "total_emissions_to_water": {"type": "float", 'min': 0},

    #2.5.2
    #Float (positive)
    "quantity_hazardous_radioactive_waste_generated": {"type": "float", 'min': 0},
    
    #2.5.3
    #STRING from yes_no
    "circular_economy_principles": {
        "type": "string",
        "allowed": ["yes", "no"],
    },

    #2.6.1
    #STRING from yes_no
    "sites_affecting_biodiversity_areas": {
        "type": "string",
        "allowed": ["yes", "no"],
    },

    #3.1.1, 3.1.2, 3.1.3, 3.1.4
    #Float (positive) — note: number of FTEs can be non-integer
    "number_of_ftes_end_of_report_year_female": {"type": "float", 'min': 0},
    "number_of_ftes_end_of_report_year_non_binary": {"type": "float", 'min': 0},
    "number_of_ftes_end_of_report_year_non_disclosed": {"type": "float", 'min': 0},
    "number_of_ftes_end_of_report_year_male": {"type": "float", 'min': 0},

    #3.1.5, 3.1.6, 3.1.7, 3.1.8, 3.1.9
    #Integer (positive)
    "total_csuite_employees": {"type": "integer", 'min': 0},
    "number_of_csuite_female": {"type": "integer", 'min': 0},
    "number_of_csuite_non_binary": {"type": "integer", 'min': 0},
    "number_of_csuite_non_disclosed": {"type": "integer", 'min': 0},
    "number_of_csuite_male": {"type": "integer", 'min': 0},

    #3.1.10, 3.1.11, 3.1.12, 3.1.13, 3.1.14
    #Integer (positive)
    "total_founders_still_employed": {"type": "integer", 'min': 0},
    "number_of_founders_still_employed_female": {"type": "integer", 'min': 0},
    "number_of_founders_still_employed_non_binary": {"type": "integer", 'min': 0},
    "number_of_founders_still_employed_non_disclosed": {"type": "integer", 'min': 0},
    "number_of_founders_still_employed_male": {"type": "integer", 'min': 0},

    #3.2.1
    #Float between 0 and 100
    "unadjusted_gender_pay_gap": {"type": "float", "min": -100.0, "max": 100.0},

    #3.3.1
    #Float (positive) — note: number of FTEs can be non-integer
    "number_of_new_hires_inside_eu_fte": {"type": "float", 'min': 0},

    #3.3.2
    #Float (positive) — note: number of FTEs can be non-integer
    "number_of_new_hires_outside_eu_fte": {"type": "float", 'min': 0},

    #3.3.3
    #Float (positive) — note: number of FTEs can be non-integer
    "number_of_leavers_inside_eu_fte": {"type": "float", 'min': 0},

    #3.3.4
    #Float (positive) — note: number of FTEs can be non-integer
    "number_of_leavers_outside_eu_fte": {"type": "float", 'min': 0},

    #3.3.5
    #Float (positive) — note: number of FTEs can be non-integer
    "number_of_new_hires_ma_fte": {"type": "float", 'min': 0},
    
    #3.3.6
    #Float (positive) — note: number of FTEs can be non-integer
    "number_of_leavers_ma_fte": {"type": "float", 'min': 0},

    #3.3.7
    #Float (positive or negative) — note: number of FTEs can be non-integer
    "number_of_organic_net_new_hires_fte": {"type": "float"},
    
    #3.3.8
    #Float (positive or negative) — note: number of FTEs can be non-integer
    "number_of_total_net_new_hires_fte": {"type": "float"},
    
    #3.3.9
    #Float (positive) — note: number of FTEs can be non-integer
    "turnover_fte": {"type": "float", 'min': 0},

    #3.4.1
    #STRING from yes_no_expanded
    "implements_employee_survey_questionnaires": {
        "type": "string",
        "allowed": list(OPTIONS["yes_no_expanded"].keys()),
    },

    #3.4.2
    #Float between 0 and 100
    "percentage_employees_responding_employee_survey": {"type": "float", "min": 0.0, "max": 100.0},

    #3.4.3
    #STRING from whistleblower_procedure
    "implemented_whistleblower_procedure": {
        "type": "string",
        "allowed": list(OPTIONS["whistleblower_procedure"].keys()),
    },

    #3.5.1
    #Float (positive)
    "average_hours_training_employees_taken_during_reporting_period": {"type": "float", 'min': 0},

    #3.6.1
    #Integer (positive)
    "number_of_workrelated_injuries": {"type": "integer", 'min': 0},
    
    # New in 2025
    # 3.6.1.1
    #String
    "workrelated_injuries_qualitative": {
        "type": "string",
    },
    
    #3.6.2
    #Integer (positive)
    "number_of_workrelated_fatalities": {"type": "integer", 'min': 0},

    #3.6.3
    #Float (positive)
    "days_lost_due_to_injury": {"type": "float", 'min': 0},

    #3.7.1
    #STRING from yes_no_expanded
    "human_rights_due_diligence_process": {
        "type": "string",
        "allowed": list(OPTIONS["yes_no_expanded"].keys()),
    },

    #4.1.1, 4.1.2, 4.1.3, 4.1.4, 4.1.5
    #Integer (positive)
    "total_number_of_board_members": {"type": "integer", 'min': 0},
    "number_of_board_members_female": {"type": "integer", 'min': 0},
    "number_of_board_members_non_binary": {"type": "integer", 'min': 0},
    "number_of_board_members_non_disclosed": {"type": "integer", 'min': 0},
    "number_of_board_members_male": {"type": "integer", 'min': 0},

    #4.1.6
    #Integer (positive)
    "number_of_board_members_underrepresented_groups": {"type": "integer", 'min': 0},

    #4.1.7
    #Integer (positive)
    "number_of_independent_board_members": {"type": "integer", 'min': 0},

    #4.2.1
    #Integer (positive)
    "number_of_data_breaches": {"type": "integer", 'min': 0},
    
    # New in 2025
    # 4.2.1.1
    #String
    "data_breaches_qualitative": {
        "type": "string",
    },
    
    # NEW in 2025
    #4.2.2.1
    #STRING from yes_no
    "cyber_scheduled_scans": {
       "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # NEW in 2025
    #4.2.2.2
    #STRING from yes_no
    "cyber_penetration_testing": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # NEW in 2025
    #4.2.2.3
    #STRING from yes_no
    "cyber_lifecycle_security_testing": {
       "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # NEW in 2025
    #4.2.2.4
    #STRING from yes_no
    "cyber_other": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    # New in 2025
    # 4.2.2.4.1
    #String
    "cyber_other_specify": {
        "type": "string",
    },
    
    # NEW in 2025
    #4.2.2.5
    #STRING from yes_no
    "cyber_no_programme": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #PAI 1.2
    #Float (positive)
    "total_scope_2_emissions_location_based": {"type": "float", 'min': 0},
    
    #PAI 1.3
    #Float (positive)
    "total_scope_2_emissions_market_based": {"type": "float", 'min': 0},
    
    #PAI 1.5
    #Float (positive)
    "total_ghg_emissions_location_based": {"type": "float", 'min': 0},
    
    #PAI 1.6
    #Float (positive)
    "total_ghg_emissions_market_based": {"type": "float", 'min': 0},
    
    #PAI 4.1
    #STRING from yes_no
    "active_in_fossil_sector": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #PAI 5.2
    #Float (positive)
    "non_renewable_energy_consumption": {"type": "float", 'min': 0},
    
    #PAI 5.4
    #Float (positive)
    "total_energy_production": {"type": "float", 'min': 0},
    
    #PAI 5.5
    #Float (positive)
    "non_renewable_energy_production": {"type": "float", 'min': 0},
    
    #PAI 5.6
    #Float (positive)
    "renewable_energy_production": {"type": "float", 'min': 0},
    
    #PAI 6.1
    #STRING from yes_no
    "high_impact_climate_section_a_agriculture_forestry_fishing": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #PAI 6.1.1
    #Float (positive)
    "high_impact_climate_section_a_agriculture_forestry_fishing_energy_consumption_gwh": {"type": "float", 'min': 0},
    
    #PAI 6.1.2
    #Float (positive)
    "high_impact_climate_section_a_agriculture_forestry_fishing_gross_revenue": {"type": "float", 'min': 0},
    
    #PAI 6.2
    #STRING from yes_no
    "high_impact_climate_section_b_mining_quarrying": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #PAI 6.2.1
    #Float (positive)
    "high_impact_climate_section_b_mining_quarrying_energy_consumption_gwh": {"type": "float", 'min': 0},
    
    #PAI 6.2.2
    #Float (positive)
    "high_impact_climate_section_b_mining_quarrying_gross_revenue": {"type": "float", 'min': 0},
    
    #PAI 6.3
    #STRING from yes_no
    "high_impact_climate_section_c_manufacturing": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #PAI 6.3.1
    #Float (positive)
    "high_impact_climate_section_c_manufacturing_energy_consumption_gwh": {"type": "float", 'min': 0},
    
    #PAI 6.3.2
    #Float (positive)
    "high_impact_climate_section_c_manufacturing_gross_revenue": {"type": "float", 'min': 0},
    
    #PAI 6.4
    #STRING from yes_no
    "high_impact_climate_section_d_electricity_gas_steam_air_conditioning_supply": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #PAI 6.4.1
    #Float (positive)
    "high_impact_climate_section_d_electricity_gas_steam_air_conditioning_supply_energy_consumption_gwh": {"type": "float", 'min': 0},
    
    #PAI 6.4.2
    #Float (positive)
    "high_impact_climate_section_d_electricity_gas_steam_air_conditioning_supply_gross_revenue": {"type": "float", 'min': 0},
    
    #PAI 6.5
    #STRING from yes_no
    "high_impact_climate_section_e_water_supply_sewerage_waste_management_remediation_activities": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #PAI 6.5.1
    #Float (positive)
    "high_impact_climate_section_e_water_supply_sewerage_waste_management_remediation_activities_energy_consumption_gwh": {"type": "float", 'min': 0},
    
    #PAI 6.5.2
    #Float (positive)
    "high_impact_climate_section_e_water_supply_sewerage_waste_management_remediation_activities_gross_revenue": {"type": "float", 'min': 0},
    
    #PAI 6.6
    #STRING from yes_no
    "high_impact_climate_section_f_construction": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #PAI 6.6.1
    #Float (positive)
    "high_impact_climate_section_f_construction_energy_consumption_gwh": {"type": "float", 'min': 0},
    
    #PAI 6.6.2
    #Float (positive)
    "high_impact_climate_section_f_construction_gross_revenue": {"type": "float", 'min': 0},
    
    #PAI 6.7
    #STRING from yes_no
    "high_impact_climate_section_g_wholesale_retail_trade_repair_motor_vehicles_motorcycles": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #PAI 6.7.1
    #Float (positive)
    "high_impact_climate_section_g_wholesale_retail_trade_repair_motor_vehicles_motorcycles_energy_consumption_gwh": {"type": "float", 'min': 0},
    
    #PAI 6.7.2
    #Float (positive)
    "high_impact_climate_section_g_wholesale_retail_trade_repair_motor_vehicles_motorcycles_gross_revenue": {"type": "float", 'min': 0},
    
    #PAI 6.8
    #STRING from yes_no
    "high_impact_climate_section_h_transportation_storage": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #PAI 6.8.1
    #Float (positive)
    "high_impact_climate_section_h_transportation_storage_energy_consumption_gwh": {"type": "float", 'min': 0},
    
    #PAI 6.8.2
    #Float (positive)
    "high_impact_climate_section_h_transportation_storage_gross_revenue": {"type": "float", 'min': 0},
    
    #PAI 6.9
    #STRING from yes_no
    "high_impact_climate_section_l_real_estate_activities": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #PAI 6.9.1
    #Float (positive)
    "high_impact_climate_section_l_real_estate_activities_energy_consumption_gwh": {"type": "float", 'min': 0},
    
    #PAI 6.9.2
    #Float (positive)
    "high_impact_climate_section_l_real_estate_activities_gross_revenue": {"type": "float", 'min': 0},
    
    #PAI 10.1
    #STRING from yes_no
    "violating_ungp_oecd": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #PAI 10.1.1
    #STRING from yes_no
    "type_of_violations_ungc_oecd_guidelines": {
        "type": "string",
        "allowed": list(OPTIONS["violations_ungc_oecd_guidelines"].keys()),
    },
    
    #PAI 11.1
    #STRING from yes_no
    "has_processes_monitor_ungp_oecd": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
    
    #PAI 14.1
    #STRING from yes_no
    "involved_in_controversial_weapons": {
        "type": "string",
        "allowed": ["yes", "no"],
    },
}

# Dictionary mapping compound IDs to their units
COMPOUND_ID_UNITS = {
    "percentage_turnover_eu_taxonomy": "%",
    "percentage_capex_eu_taxonomy": "%",
    "percentage_opex_eu_taxonomy": "%",
    "percentage_turnover_tobacco_activities": "%",
    "percentage_turnover_hard_coal_and_lignite_activities": "%",
    "percentage_turnover_oil_fuels_activities": "%",
    "percentage_turnover_gaseous_fuels_activities": "%",
    "percentage_turnover_high_ghg_intensity_electricity_generation": "%",
    "unadjusted_gender_pay_gap": "%",
    "percentage_employees_responding_employee_survey": "%",
    "number_of_data_breaches": "breaches",
    "days_lost_due_to_injury": "days",
    "number_of_workrelated_fatalities": "fatalities",
    "total_ftes_end_of_report_year": "FTEs",
    "total_ftes_end_of_previous_report_year": "FTEs",
    "number_of_ftes_end_of_report_year_female": "FTEs",
    "number_of_ftes_end_of_report_year_non_binary": "FTEs",
    "number_of_ftes_end_of_report_year_non_disclosed": "FTEs",
    "number_of_ftes_end_of_report_year_male": "FTEs",
    "number_of_new_hires_inside_eu_fte": "FTEs",
    "number_of_new_hires_outside_eu_fte": "FTEs",
    "number_of_leavers_inside_eu_fte": "FTEs",
    "number_of_leavers_outside_eu_fte": "FTEs",
    "number_of_new_hires_ma_fte": "FTEs",
    "number_of_leavers_ma_fte": "FTEs",
    "number_of_organic_net_new_hires_fte": "FTEs",
    "number_of_total_net_new_hires_fte": "FTEs",
    "turnover_fte": "FTEs",
    "gross_revenue": "currency",
    "gross_revenue_inside_eu": "currency",
    "gross_revenue_outside_eu": "currency",
    "annual_balance_sheet_assets_total": "currency",
    "annual_balance_sheet_assets_total_inside_eu": "currency",
    "annual_balance_sheet_assets_total_outside_eu": "currency",
    "turnover": "currency",
    "turnover_inside_eu": "currency",
    "turnover_outside_eu": "currency",
    "high_impact_climate_section_a_agriculture_forestry_fishing_gross_revenue": "currency",
    "high_impact_climate_section_b_mining_quarrying_gross_revenue": "currency",
    "high_impact_climate_section_c_manufacturing_gross_revenue": "currency",
    "high_impact_climate_section_d_electricity_gas_steam_air_conditioning_supply_gross_revenue": "currency",
    "high_impact_climate_section_e_water_supply_sewerage_waste_management_remediation_activities_gross_revenue": "currency",
    "high_impact_climate_section_f_construction_gross_revenue": "currency",
    "high_impact_climate_section_g_wholesale_retail_trade_repair_motor_vehicles_motorcycles_gross_revenue": "currency",
    "high_impact_climate_section_h_transportation_storage_gross_revenue": "currency",
    "high_impact_climate_section_l_real_estate_activities_gross_revenue": "currency",
    "high_impact_climate_section_a_agriculture_forestry_fishing_energy_consumption_gwh": "GWh",
    "high_impact_climate_section_b_mining_quarrying_energy_consumption_gwh": "GWh",
    "high_impact_climate_section_c_manufacturing_energy_consumption_gwh": "GWh",
    "high_impact_climate_section_d_electricity_gas_steam_air_conditioning_supply_energy_consumption_gwh": "GWh",
    "high_impact_climate_section_e_water_supply_sewerage_waste_management_remediation_activities_energy_consumption_gwh": "GWh",
    "high_impact_climate_section_f_construction_energy_consumption_gwh": "GWh",
    "high_impact_climate_section_g_wholesale_retail_trade_repair_motor_vehicles_motorcycles_energy_consumption_gwh": "GWh",
    "high_impact_climate_section_h_transportation_storage_energy_consumption_gwh": "GWh",
    "high_impact_climate_section_l_real_estate_activities_energy_consumption_gwh": "GWh",
    "average_hours_training_employees_taken_during_reporting_period": "hours",
    "number_of_esg_incidents": "incidents",
    "number_of_workrelated_injuries": "injuries",
    "total_energy_consumption": "kWh",
    "energy_consumption_renewable": "kWh",
    "non_renewable_energy_consumption": "kWh",
    "total_energy_production": "kWh",
    "non_renewable_energy_production": "kWh",
    "renewable_energy_production": "kWh",
    "total_csuite_employees": "people",
    "number_of_csuite_female": "people",
    "number_of_csuite_non_binary": "people",
    "number_of_csuite_non_disclosed": "people",
    "number_of_csuite_male": "people",
    "total_founders_still_employed": "people",
    "number_of_founders_still_employed_female": "people",
    "number_of_founders_still_employed_non_binary": "people",
    "number_of_founders_still_employed_non_disclosed": "people",
    "number_of_founders_still_employed_male": "people",
    "total_number_of_board_members": "people",
    "number_of_board_members_female": "people",
    "number_of_board_members_non_binary": "people",
    "number_of_board_members_non_disclosed": "people",
    "number_of_board_members_male": "people",
    "number_of_board_members_underrepresented_groups": "people",
    "number_of_independent_board_members": "people",
    "total_ghg_emissions": "tCO2e",
    "total_scope_1_emissions": "tCO2e",
    "total_scope_2_emissions": "tCO2e",
    "total_scope_3_emissions": "tCO2e",
    "scope_3_primary_source_emissions": "tCO2e",
    "scope_3_secondary_source_emissions": "tCO2e",
    "total_scope_2_emissions_location_based": "tCO2e",
    "total_scope_2_emissions_market_based": "tCO2e",
    "total_ghg_emissions_location_based": "tCO2e",
    "total_ghg_emissions_market_based": "tCO2e",
    "total_emissions_to_water": "tonnes (metric)",
    "quantity_hazardous_radioactive_waste_generated": "tonnes (metric)",
}
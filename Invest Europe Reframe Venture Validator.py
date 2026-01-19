import csv
import os
import uuid
from cerberus import Validator
from flask import Flask, request, render_template, jsonify, send_file, after_this_request
import openpyxl
from collections import defaultdict

from validation_mappings.minimum_intermediate import MINIMUM_METRICS, INTERMEDIATE_METRICS, FULL_METRICS, OPTIONAL_METRICS, ALL_METRICS
from validation_mappings.schema import SCHEMA_PORTCO, COMPOUND_ID_UNITS
from validation_mappings.schema_fund import SCHEMA_FUND, FUND_COMPOUND_ID_UNITS, ALL_FUND_METRICS, REQUIRED_FUND_METRICS
from validation_mappings.schema_gp import SCHEMA_GP, GP_COMPOUND_ID_UNITS, ALL_GP_METRICS, REQUIRED_GP_METRICS
from validation_mappings.options import OPTIONS
from validation_mappings.options_fund import OPTIONS_FUND
from validation_mappings.options_gp import OPTIONS_GP


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

def is_float(value: str):
    try:
        float(value)
        return True
    except ValueError:
        return False

def get_typed_value(schema: dict, value: str, compound_id: str):
    if schema.get(compound_id, {}).get("type") == "integer" and value.isnumeric():
        value = int(value)
    elif schema.get(compound_id, {}).get("type") == "float" and is_float(value):
        value = float(value)
    else:
        value = str(value)
    return value

def read_and_organize_csv(csv_path: str, company_id: str):
    """
    Reads a CSV file for company, fund, or GP and organizes the data into a dictionary.
    
    Args:
        csv_path (str): Path to the CSV file.
        company_id (str): UUID of the company (generated in the /upload function)
    
    Returns:
        dict: A dictionary with 'metrics' and 'status' organized for the company.
    """
    expected_headers = ["COMPOUND_ID", "REPORTING_PERIOD", "UNIT", "VALUE", "STATUS", "COMMENTS"]

    company_data = {"metrics": {}, "status": {}, "currency": ""}
    with open(csv_path, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        headers = next(csv_reader, None)

        if not headers:
            raise ValueError("The CSV file is empty or missing headers.")
        
        # Check if headers match the expected format
        if headers != expected_headers:
            raise ValueError(f"Invalid CSV headers. Expected: {expected_headers}, Found: {headers}")

        for idx, row in enumerate(csv_reader, start=2):  # Start at the second row
            if len(row) < len(expected_headers):
                print(f"ERROR: Skipping row at .csv line {idx} due to insufficient columns: {row}")
                continue

            key = row[0].strip()
            value = row[3].strip()
            status = row[4].strip()
            
            # Populate company data
            company_data["metrics"][key] = value
            company_data["status"][key] = status

    return {company_id: company_data}

### PORTCO VALIDATION LOGIC ###

def validate_metrics_by_company(company_data: dict, schema: dict):
    """
    Validates the data for a single portfolio company based on the provided schema.
    
    Args:
        company_data (dict): Data for a single company, containing metrics and statuses.
        schema (dict): Validation schema for the metrics.
    
    Returns:
        dict: A summary of validation results for the company.
    """
    company_metrics = company_data["metrics"]
    company_statuses = company_data["status"]
    valid_lines = []
    error_lines = []
    unknown_lines = []
    blank_lines = []
    recommended_but_missing_lines = []
    missing_metrics = []
    warning_lines = []

    # Collect metrics for each level
    required_metrics = {
        "minimum": MINIMUM_METRICS,
        "intermediate": INTERMEDIATE_METRICS,
        "full": FULL_METRICS,
        "optional": OPTIONAL_METRICS
    }
    
    for compound_id in ALL_METRICS:
        # Determine if metric is missing or invalid
        
        if compound_id not in company_metrics:
            level = (
                    "Minimum" if compound_id in MINIMUM_METRICS
                    else "Intermediate" if compound_id in INTERMEDIATE_METRICS
                    else "Full" if compound_id in FULL_METRICS
                    else "Value not required (optional)"
                )
            
            missing_metrics.append({
                "compound_id": compound_id,
                "requirement_level": level,
                "reason": "Not in import file at all",
            })
        else:
            raw_value = company_metrics[compound_id]
            status = company_statuses.get(compound_id, "")

            # Handle not_applicable or not_available
            if status in ["not_applicable", "not_available"]:
                reason = (
                    "Marked as not applicable in import file"
                    if status == "not_applicable"
                    else "Marked as not available in import file"
                )
                level = (
                    "Minimum" if compound_id in MINIMUM_METRICS
                    else "Intermediate" if compound_id in INTERMEDIATE_METRICS
                    else "Full" if compound_id in FULL_METRICS
                    else "Value not required"
                )
                
                if raw_fte_value := company_metrics["total_ftes_end_of_report_year"]:
                    total_fte_number = get_typed_value(schema=SCHEMA_PORTCO, value=raw_fte_value, compound_id="total_ftes_end_of_report_year")

                    if level == "Minimum":
                        recommended_but_missing_lines.append({
                            "compound_id": compound_id,
                            "requirement_level": level,
                            "reason": "Status is 'not_applicable' or 'not_available', but this is a 'minimum' metric.",
                        })
                    elif level == "Intermediate":
                        if total_fte_number >= 15:
                            recommended_but_missing_lines.append({
                                "compound_id": compound_id,
                                "requirement_level": level,
                                "reason": "Status is 'not_applicable' or 'not_available', but this is an 'intermediate' metric for companies with FTE higher than 15.",
                            })
                        else:
                            blank_lines.append({
                                "compound_id": compound_id,
                                "requirement_level": level,
                                "reason": reason,
                            })
                    elif level == "Full":
                        if total_fte_number >= 250:
                            recommended_but_missing_lines.append({
                                "compound_id": compound_id,
                                "requirement_level": level,
                                "reason": "Status is 'not_applicable' or 'not_available', but all metrics are strongly recommended for companies with FTE higher than 250.",
                            })
                        else:
                            blank_lines.append({
                                "compound_id": compound_id,
                                "requirement_level": level,
                                "reason": reason,
                            })
                else:
                    if level == "Minimum":
                        recommended_but_missing_lines.append({
                            "compound_id": compound_id,
                            "requirement_level": level,
                            "reason": "Status is 'not_applicable' or 'not_available', but this is a 'minimum' metric.",
                        })
                    else:
                        recommended_but_missing_lines.append({
                            "compound_id": compound_id,
                            "requirement_level": level,
                            "reason": "Status is 'not_applicable' or 'not_available'. Unknown level of requirement for this company since total_ftes_end_of_report_year is not provided.",
                        })
                continue  # Skip schema validation for these metrics

            # Handle blank values
            if raw_value == "" and status == "provided":
                error_lines.append({
                    "compound_id": compound_id,
                    "raw_value": raw_value,
                    "error_notes": "Value is blank but marked as 'provided'.",
                })
            elif status == "provided":
                # Validate value if not blank or excluded
                typed_value = get_typed_value(schema=SCHEMA_PORTCO, value=raw_value, compound_id=compound_id)
                interpreted_value = get_interpreted_value_portco_with_units(value=raw_value, compound_id=compound_id, currency_unit=company_metrics["currency"])

                validator = Validator({compound_id: schema.get(compound_id, {})})
                validation_data = {compound_id: typed_value}
                level = (
                    "Minimum" if compound_id in MINIMUM_METRICS
                    else "Intermediate" if compound_id in INTERMEDIATE_METRICS
                    else "Full" if compound_id in FULL_METRICS
                    else "Value not required"
                )

                if validator.validate(validation_data):
                    valid_lines.append({
                        "compound_id": compound_id,
                        "raw_value": typed_value,
                        "interpreted_value": interpreted_value,
                        "requirement_level": level,
                    })
                else:
                    error_lines.append({
                        "compound_id": compound_id,
                        "raw_value": raw_value,
                        "error_notes": str(validator.errors),
                        "requirement_level": level,
                    })
                    
            else: 
                error_lines.append({
                    "compound_id": compound_id,
                    "raw_value": raw_value,
                    "error_notes": f"Unknown value in 'STATUS' column: {status}.",
                    "requirement_level": level,
                })
                   
     # Special relationships validation - dependencies and conditionals
    special_relations = [
        {
            "condition_id": "violating_ungp_oecd",
            "condition_value": "yes",
            "dependent_ids": ["type_of_violations_ungc_oecd_guidelines"]
        },
        #NEW in 2025
        {
            "condition_id": "cyber_other",
            "condition_value": "yes",
            "dependent_ids": ["cyber_other_specify"]
        },
        #NEW in 2025
        {
            "condition_id": "number_of_data_breaches",
            "condition_value": "yes",
            "dependent_ids": ["data_breaches_qualitative"]
        },
        #NEW in 2025
        {
            "condition_id": "number_of_esg_incidents",
            "condition_value": "yes",
            "dependent_ids": ["qualitative_info_esg_incidents"]
        },
        #NEW in 2025
        {
            "condition_id": "number_of_workrelated_injuries",
            "condition_value": "yes",
            "dependent_ids": ["workrelated_injuries_qualitative"]
        },
        {
            "condition_id": "eu_taxonomy_assessment",
            "condition_value": "yes",
            "dependent_ids": [
                "percentage_turnover_eu_taxonomy",
                "percentage_capex_eu_taxonomy",
                "percentage_opex_eu_taxonomy"
            ]
        },
        {
            "condition_id": "tobacco_activities",
            "condition_value": "yes",
            "dependent_ids": ["percentage_turnover_tobacco_activities"]
        },
        {
            "condition_id": "hard_coal_and_lignite_activities",
            "condition_value": "yes",
            "dependent_ids": ["percentage_turnover_hard_coal_and_lignite_activities"]
        },
        {
            "condition_id": "oil_fuels_activities",
            "condition_value": "yes",
            "dependent_ids": ["percentage_turnover_oil_fuels_activities"]
        },
        {
            "condition_id": "gaseous_fuels_activities",
            "condition_value": "yes",
            "dependent_ids": ["percentage_turnover_gaseous_fuels_activities"]
        },
        {
            "condition_id": "high_ghg_intensity_electricity_generation",
            "condition_value": "yes",
            "dependent_ids": ["percentage_turnover_high_ghg_intensity_electricity_generation"]
        },
        # REMOVED in 2025 Update
        # {
        #     "condition_id": "ems_implemented",
        #     "condition_value": "yes_other_ems_certification",
        #     "dependent_ids": ["other_ems_certification"]
        # },
        {
            "condition_id": "listed",
            "condition_value": "yes",
            "dependent_ids": ["listed_ticker"]
        },
        
        # REMOVED in 2025 Update
        # {
        #     "condition_id": "occurrence_of_esg_incidents",
        #     "condition_value": "yes",
        #     "dependent_ids": ["number_of_esg_incidents"]
        # },
        
        # REMOVED in 2025 Update
        # {
        #     "condition_id": "dedicated_sustainability_staff",
        #     "condition_value": "yes",
        #     "dependent_ids": [
        #         "sustainability_staff_ceo",
        #         "sustainability_staff_cso",
        #         "sustainability_staff_cfo",
        #         "sustainability_staff_board",
        #         "sustainability_staff_management",
        #         "sustainability_staff_none_of_above"
        #     ]
        # },
        
        {
            "condition_ids": [
                "number_of_ftes_end_of_report_year_female",
                "number_of_ftes_end_of_report_year_non_binary",
                "number_of_ftes_end_of_report_year_non_disclosed",
                "number_of_ftes_end_of_report_year_male"
            ],
            "total_field": "total_ftes_end_of_report_year"
        },
        {
            "condition_ids": [
                "number_of_csuite_female",
                "number_of_csuite_non_binary",
                "number_of_csuite_non_disclosed",
                "number_of_csuite_male"
            ],
            "total_field": "total_csuite_employees"
        },
        {
            "condition_ids": [
                "number_of_founders_still_employed_female",
                "number_of_founders_still_employed_non_binary",
                "number_of_founders_still_employed_non_disclosed",
                "number_of_founders_still_employed_male"
            ],
            "total_field": "total_founders_still_employed"
        },
        {
            "condition_ids": [
                "number_of_board_members_female",
                "number_of_board_members_non_binary",
                "number_of_board_members_non_disclosed",
                "number_of_board_members_male",
                "number_of_board_members_underrepresented_groups",
                "number_of_independent_board_members"
            ],
            "total_field": "total_number_of_board_members"
        },
        {
            "condition_ids": [
                "energy_consumption_renewable"
            ],
            "total_field": "total_energy_consumption"
        },
        
        #New in 2025: Checking if csv states no responsibility but also states yes on one of the responsibility metrics
        {
            "conflict_trigger": "sustainability_responsibility_none",
            "conflict_trigger_value": "yes",
            "conflicting_fields": [
                "sustainability_responsibility_officer",
                "sustainability_responsibility_team",
                "sustainability_responsibility_referent",
                "sustainability_responsibility_cfo",
                "sustainability_responsibility_ceo",
                "sustainability_responsibility_cso",
                "sustainability_responsibility_management"
            ]
        },
        
        #New in 2025: Checking if csv states no responsibility but also states yes on one of the responsibility metrics
        {
            "conflict_trigger": "cyber_no_programme",
            "conflict_trigger_value": "yes",
            "conflicting_fields": [
                "cyber_scheduled_scans",
                "cyber_penetration_testing",
                "cyber_lifecycle_security_testing",
                "cyber_other",
            ]
        },

        # Sum validation checks - warn if total doesn't match sum of components
        {
            "sum_check": True,
            "total_field": "gross_revenue",
            "component_fields": ["gross_revenue_inside_eu", "gross_revenue_outside_eu"],
            "tolerance_percent": 1
        },
        {
            "sum_check": True,
            "total_field": "turnover",
            "component_fields": ["turnover_inside_eu", "turnover_outside_eu"],
            "tolerance_percent": 1
        },
        {
            "sum_check": True,
            "total_field": "total_ghg_emissions",
            "component_fields": ["total_scope_1_emissions", "total_scope_2_emissions", "total_scope_3_emissions"],
            "tolerance_percent": 5
        },
        {
            "sum_check": True,
            "total_field": "total_energy_consumption",
            "component_fields": ["energy_consumption_renewable", "non_renewable_energy_consumption"],
            "tolerance_percent": 5
        },
        {
            "sum_check": True,
            "total_field": "total_ftes_end_of_report_year",
            "component_fields": [
                "number_of_ftes_end_of_report_year_female",
                "number_of_ftes_end_of_report_year_male",
                "number_of_ftes_end_of_report_year_non_binary",
                "number_of_ftes_end_of_report_year_non_disclosed"
            ],
            "tolerance_percent": 5
        },
        {
            "sum_check": True,
            "total_field": "total_csuite_employees",
            "component_fields": [
                "number_of_csuite_female",
                "number_of_csuite_male",
                "number_of_csuite_non_binary",
                "number_of_csuite_non_disclosed"
            ],
            "tolerance_percent": 5
        },
        {
            "sum_check": True,
            "total_field": "total_founders_still_employed",
            "component_fields": [
                "number_of_founders_still_employed_female",
                "number_of_founders_still_employed_male",
                "number_of_founders_still_employed_non_binary",
                "number_of_founders_still_employed_non_disclosed"
            ],
            "tolerance_percent": 5
        },
        {
            "sum_check": True,
            "total_field": "total_number_of_board_members",
            "component_fields": [
                "number_of_board_members_female",
                "number_of_board_members_male",
                "number_of_board_members_non_binary",
                "number_of_board_members_non_disclosed"
            ],
            "tolerance_percent": 5
        }
        
    ]

    minimum = MINIMUM_METRICS[:]
    intermediate = INTERMEDIATE_METRICS[:]
    full = FULL_METRICS[:]
    
    for relation in special_relations:
        
        # Checks to make sure the total is always there for a metric that is a subset of that total (e.g., female FTE requires total FTE)
        if "condition_ids" in relation:
            # Check if any one of the fields has a value
            if any(company_metrics.get(condition_id) for condition_id in relation["condition_ids"]):
                total_field = relation["total_field"]
                # Ensure the total field is not marked as not_applicable or not_available
                total_status = company_statuses.get(total_field, "")
                
                if total_field not in company_metrics:
                    #Replace line in missing metrics with more detail
                    missing_metrics = [line for line in missing_metrics if line["compound_id"] != total_field]
                    missing_metrics.append({
                        "compound_id": total_field,
                        "requirement_level": f"Strongly recommended because at least one value is provided for {', '.join(relation['condition_ids'])}",
                        "reason": "Not in import file at all",
                    })
                    blank_lines = [line for line in blank_lines if line["compound_id"] != total_field]
                    
                elif company_metrics[total_field] == "" and total_status not in ["not_applicable", "not_available"]:
                    #Replace line in missing metrics with more detail
                    missing_metrics = [line for line in missing_metrics if line["compound_id"] != total_field]
                    missing_metrics.append({
                        "compound_id": total_field,
                        "requirement_level": f"Strongly recommended because at least one value is provided for {', '.join(relation['condition_ids'])}",
                        "reason": "Value is blank",
                    })
                    valid_lines = [line for line in valid_lines if line["compound_id"] != total_field]
                    blank_lines = [line for line in blank_lines if line["compound_id"] != total_field]

                elif total_status in ["not_applicable", "not_available"]:
                    #Replace line in recommended_but_missing_lines metrics with more detail
                    recommended_but_missing_lines = [line for line in recommended_but_missing_lines if line["compound_id"] != total_field]
                    recommended_but_missing_lines.append({
                        "compound_id": total_field,
                        "requirement_level": f"Strongly recommended because at least one value is provided for {', '.join(relation['condition_ids'])}",
                        "reason": "Marked as not_applicable or not_available"
                    })
                    blank_lines = [line for line in blank_lines if line["compound_id"] != total_field]
                    
                
                    
        # New in 2025: Checks for conflicting values, e.g., sustainability_responsibility_none = 'yes' conflicts with any other responsibility = 'yes'

        elif "conflict_trigger" in relation:

            trigger_field = relation["conflict_trigger"]
            trigger_value = relation["conflict_trigger_value"]
            conflicting_fields = relation["conflicting_fields"]

            if company_metrics.get(trigger_field) == trigger_value:

                for conflicting_field in conflicting_fields:

                    if company_metrics.get(conflicting_field) == "yes":

                        # Move from valid_lines to error_lines

                        valid_lines = [line for line in valid_lines if line["compound_id"] != conflicting_field]

                        blank_lines = [line for line in blank_lines if line["compound_id"] != conflicting_field]

                        error_lines.append({
                            "compound_id": conflicting_field,
                            "raw_value": "yes",
                            "error_notes": f"Conflict: '{conflicting_field}' is 'yes' but '{trigger_field}' is also '{trigger_value}'. If '{trigger_field}' is '{trigger_value}', then '{conflicting_field}' should be 'no'.",
                        })
        
        # Checks if total field matches sum of component fields (within tolerance)

        elif "sum_check" in relation:

            total_field = relation["total_field"]

            component_fields = relation["component_fields"]

            tolerance_percent = relation.get("tolerance_percent", 1)

            # Get total value if it exists and is numeric
            total_raw = company_metrics.get(total_field, "")

            if total_raw and total_raw != "":

                total_value = get_typed_value(schema=schema, value=total_raw, compound_id=total_field)

                if total_value is not None and isinstance(total_value, (int, float)):

                    # Sum up component values (only those that exist and are numeric)
                    component_sum = 0
                    components_found = []

                    for comp_field in component_fields:

                        comp_raw = company_metrics.get(comp_field, "")

                        if comp_raw and comp_raw != "":

                            comp_value = get_typed_value(schema=schema, value=comp_raw, compound_id=comp_field)

                            if comp_value is not None and isinstance(comp_value, (int, float)):

                                component_sum += comp_value
                                components_found.append(comp_field)

                    # Only check if at least one component was found

                    if components_found:

                        # Calculate tolerance
                        if total_value == 0:
                            # If total is 0, components should also sum to 0
                            is_mismatch = component_sum != 0

                        else:
                            tolerance = abs(total_value) * (tolerance_percent / 100)
                            is_mismatch = abs(total_value - component_sum) > tolerance

                        if is_mismatch:
                            warning_lines.append({
                                "compound_id": total_field,
                                "raw_value": total_raw,
                                "warning_notes": f"Sum mismatch: '{total_field}' is {total_value}, but sum of [{', '.join(components_found)}] is {component_sum}. Difference exceeds {tolerance_percent}% tolerance.",
                            })

 

        # Checks dependencies, e.g., percentage_turnover_tobacco_activities is required if tobacco_activities = 'yes'

        else:  
            condition_id = relation["condition_id"]
            condition_value = relation["condition_value"]
            dependent_ids = relation["dependent_ids"]

            if company_metrics.get(condition_id) == condition_value:
                for dependent_id in dependent_ids:
                    if dependent_id not in company_metrics:
                        #Replace line in missing metrics with more detail
                        missing_metrics = [line for line in missing_metrics if line["compound_id"] != dependent_id]
                        missing_metrics.append({
                            "compound_id": dependent_id,
                            "requirement_level": f"Strongly recommended because '{condition_id}' is '{condition_value}'",
                            "reason": "Not in import file at all",
                        })
                        blank_lines = [line for line in blank_lines if line["compound_id"] != dependent_id]
                        
                    elif company_metrics[dependent_id] == "" and company_statuses.get(dependent_id, "") not in ["not_applicable", "not_available"]:
                        #Replace line in missing metrics with more detail
                        missing_metrics = [line for line in missing_metrics if line["compound_id"] != dependent_id]
                        missing_metrics.append({
                            "compound_id": dependent_id,
                            "requirement_level": f"Strongly recommended because '{condition_id}' is '{condition_value}'",
                            "reason": "Value is blank",
                        })
                        valid_lines = [line for line in valid_lines if line["compound_id"] != dependent_id]
                        blank_lines = [line for line in blank_lines if line["compound_id"] != dependent_id]
                        
                    elif company_statuses.get(dependent_id, "") in ["not_applicable", "not_available"]:
                        #Replace line in recommended_but_missing_lines metrics with more detail
                        recommended_but_missing_lines = [line for line in recommended_but_missing_lines if line["compound_id"] != dependent_id]
                        recommended_but_missing_lines.append({
                            "compound_id": dependent_id,
                            "requirement_level": f"Strongly recommended because '{condition_id}' is '{condition_value}'",
                            "reason": "Marked as not_applicable or not_available",
                        })
                        blank_lines = [line for line in blank_lines if line["compound_id"] != dependent_id]
                        
                    else:
                        #Replace line in valid_lines metrics with correct requirement
                        
                        obj = next((x for x in valid_lines if x["compound_id"] == dependent_id), None)
                        if obj:
                            obj["requirement_level"] = f"Strongly recommended because '{condition_id}' is '{condition_value}'",
                    
                        
                    if condition_id in minimum:
                        minimum.append(dependent_id)
                    if condition_id in intermediate:
                        intermediate.append(dependent_id)
                    if condition_id in full:
                        full.append(dependent_id)


    # Handle unknown compound IDs
    for compound_id in company_metrics.keys():
        if compound_id not in schema:
            unknown_lines.append({
                "compound_id": compound_id,
                "raw_value": company_metrics[compound_id],
                "error_notes": "Unknown compound ID",
            })

    # Calculate valid metric percentages by level
    total_required = {level: len(required_metrics[level]) for level in required_metrics}

    # Combine missing metrics and error lines to count as missing
    all_missing_ids = {d["compound_id"] for d in missing_metrics} | {e["compound_id"] for e in error_lines}

    # Update met_required to exclude missing or erroneous metrics
    met_required = {
        level: sum(1 for m in required_metrics[level] if m not in all_missing_ids)
        for level in required_metrics
    }

    percentages = {
        level: round((met_required[level] / total_required[level]) * 100, 2) if total_required[level] > 0 else 0
        for level in required_metrics
    }

    # Count missing metrics by level, considering hierarchy and error lines
    missing_counts = {
        "minimum": sum(1 for m in missing_metrics if m["requirement_level"] == "minimum") + sum(1 for e in error_lines if e["compound_id"] in minimum),
        "intermediate": sum(1 for m in missing_metrics if m["requirement_level"] in ["minimum", "intermediate"]) + sum(1 for e in error_lines if e["compound_id"] in intermediate),
        "full": sum(1 for m in missing_metrics if m["requirement_level"] in ["minimum", "intermediate", "full"]) + sum(1 for e in error_lines if e["compound_id"] in full),
    }

    # Return the company summary
    #TO DO: Update these counts, and update the return for the new groups of lines
    return {
        "company_name": company_metrics.get("company_name", "Unknown Company"),
        "valid_lines": len(valid_lines),
        "invalid_lines": len(error_lines)+ len(missing_metrics),
        "percent_min": percentages["minimum"],
        "percent_rec": percentages["intermediate"],
        "percent_full": percentages["full"],
        "missing_minimum": missing_counts["minimum"],
        "missing_intermediate": missing_counts["intermediate"],
        "missing_full": missing_counts["full"],
        "correct_lines": valid_lines,
        "error_lines": error_lines,
        "unknown_lines": unknown_lines,
        "missing_metrics": missing_metrics,
        "blank_lines": blank_lines,
        "recommended_but_missing_lines": recommended_but_missing_lines,
        "warning_lines": warning_lines,
    }

def get_interpreted_value_portco(value: str, compound_id: str):
    """
    Interprets the value for a given compound_id using the SCHEMA_PORTCO and OPTIONS objects, turning it from the machine-readable into a human readable format. 
    
    :param compound_id: The compound ID (key) to look up in SCHEMA_PORTCO and OPTIONS.
    :param value: The value to interpret.
    :return: Interpreted value if found, else returns the value unchanged.
    """
    # Check if compound_id exists in SCHEMA_PORTCO
    if compound_id in SCHEMA_PORTCO:
        schema_entry = SCHEMA_PORTCO[compound_id]
        allowed_values = schema_entry.get("allowed")

        # If allowed values exist and are linked to a key in OPTIONS
        if allowed_values:
            # Find the key in OPTIONS by checking 'allowed' values
            for options_key, options_dict in OPTIONS.items():
                if set(allowed_values).issubset(options_dict.keys()):
                    # Use the value to get the interpreted value
                    interpreted_value = options_dict.get(value)
                    if interpreted_value:
                        return interpreted_value
    
    # Fallback: return the value unchanged if no interpretation is found
    return value

def get_interpreted_value_portco_with_units(value: str, compound_id: str, currency_unit: str):
    """
    Interprets the value for a given compound_id and appends the corresponding unit if applicable.

    :param compound_id: The compound ID (key) to look up.
    :param value: The typed value to interpret.
    :return: Interpreted value with unit appended if applicable.
    """
    interpreted_value = get_interpreted_value_portco(value, compound_id)

    # Add the unit if the compound ID is in the COMPOUND_ID_UNITS mapping
    if compound_id in COMPOUND_ID_UNITS:
        unit = COMPOUND_ID_UNITS[compound_id]
        # Special handling for currency
        if unit == "currency":
            return f"{interpreted_value} {currency_unit}"
        return f"{interpreted_value} {unit}"

    return interpreted_value

def validate_multiple_companies(all_companies_data: dict):
    """
    Validates the data for multiple companies.
    
    Args:
        all_companies_data (dict): Dictionary with company data for multiple companies.
    
    Returns:
        list: A summary of validation results for all companies.
    """
    validation_results = []
    for company_name, company_data in all_companies_data.items():
        # Perform validation for each company
        company_summary = validate_metrics_by_company(company_data, SCHEMA_PORTCO)
        #company_summary["company_name"] = company_name
        validation_results.append(company_summary)

    return validation_results

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({"error": "No files uploaded"}), 400
    files = request.files.getlist('files[]')
    if not files:
        return jsonify({"error": "No selected files"}), 400

    all_companies_data = {}
    errors = []

    for file in files:
        if not file.filename.lower().endswith('.csv'):
            errors.append(f"{file.filename}: Invalid file type. Only .csv files are accepted.")
            continue

        # Save the uploaded file temporarily for validation
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Give each company a UUID so they don't get mixed up or replaced
        company_id = uuid.uuid4() 

        try:
            # Validate and read the CSV file
            company_data = read_and_organize_csv(file_path, company_id)
            all_companies_data.update(company_data)
        except ValueError as e:
            errors.append(f"{file.filename}: {str(e)}")
        finally:
            os.remove(file_path)  # Clean up the file after processing

    if errors:
        return jsonify({"errors": errors}), 400

    # Validate the combined data
    validation_results = validate_multiple_companies(all_companies_data)

    # Render results as HTML table
    return render_template('validation_results.html', companies=validation_results)

@app.route('/convert_valid_data_to_excel', methods=['POST'])
def convert_valid_data_to_excel():
    try:
        # Extract JSON data from request
        data = request.get_json()
        companies_data = data.get("companies", {})

        if not companies_data:
            return jsonify({"error": "No valid company data found"}), 400

        # Define paths
        template_path = 'InvestEurope_Template.xlsx'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], "InvestEurope_Template_Completed.xlsx")

        if not os.path.exists(template_path):
            return jsonify({"error": f"The template file '{template_path}' was not found."}), 500

        wb = openpyxl.load_workbook(template_path)
        ws = wb["4. Aggregated PC level"]

        # Row mapping 
        row_mapping = {
            'company_name': [13],
            'business_identification_number': [14],
            'business_identification_number_system': [15],
            'country_of_domicile': [16],
            'primary_country_of_operations': [17],
            'other_EU_country_of_operation_1': [18],
            'other_EU_country_of_operation_2': [19],
            'main_industry_classification': [20],
            'total_ftes_end_of_report_year': [21],
            'total_ftes_end_of_previous_report_year': [22],
            'gross_revenue': [23],
            'gross_revenue_inside_eu': [24],
            'gross_revenue_outside_eu': [25],
            'annual_balance_sheet_assets_total': [26],
            'annual_balance_sheet_assets_total_inside_eu': [27],
            'annual_balance_sheet_assets_total_outside_eu': [28],
            'turnover': [29],
            'turnover_inside_eu': [30],
            'turnover_outside_eu': [31],
            'currency': [32],
            'listed': [33],
            'listed_ticker': [34],
            'code_of_conduct': [39],
            'overall_sustainability_policy': [40],
            'environmental_policy': [41],
            'anti_discrimination_and_equal_opportunities_policy': [42],
            'diversity_inclusion_policy': [43],
            'salary_remuneration_policy': [44],
            'health_and_safety_policy': [45],
            'human_rights_policy': [46],
            'anti_corruption_bribery_policy': [47],
            'data_privacy_security_policy': [48],
            'supply_chain_policy': [49],
            'cybersecurity_data_management_policy': [50],
            'dedicated_sustainability_staff': [51],
            'responsible_ai_policy': [51],
            'sustainability_responsibility_officer': [53],
            'sustainability_responsibility_team': [54],
            'sustainability_responsibility_referent': [55],
            'sustainability_responsibility_cfo': [56],
            'sustainability_responsibility_ceo': [57],
            'sustainability_responsibility_cso': [58],
            'sustainability_responsibility_management': [59],
            'sustainability_responsibility_none':[60],
            'number_of_esg_incidents': [64],
            'qualitative_info_esg_incidents': [65],
            'eu_taxonomy_assessment': [71],
            'percentage_turnover_eu_taxonomy': [72],
            'percentage_capex_eu_taxonomy': [73],
            'percentage_opex_eu_taxonomy': [74],
            'tobacco_activities': [78],
            'percentage_turnover_tobacco_activities': [79],
            'hard_coal_and_lignite_activities': [80],
            'percentage_turnover_hard_coal_and_lignite_activities': [81],
            'oil_fuels_activities': [82],
            'percentage_turnover_oil_fuels_activities': [83],
            'gaseous_fuels_activities': [84],
            'percentage_turnover_gaseous_fuels_activities': [85],
            'high_ghg_intensity_electricity_generation': [86],
            'percentage_turnover_high_ghg_intensity_electricity_generation': [87],
            'subject_to_csrd_reporting': [91],
            'ems_implemented': [97],
            'environmental_risk_tools': [98],
            'ghg_scope_measured_calculated': [102],
            'total_ghg_emissions': [103],
            'total_scope_1_emissions': [104, 224],
            'total_scope_1_emissions_methodology': [105],
            'total_scope_2_emissions': [106],
            'total_scope_2_emissions_methodology': [107],
            'total_scope_3_emissions': [108, 227],
            'total_scope_3_emissions_methodology': [109],
            'scope_3_primary_source': [110],
            'scope_3_primary_source_emissions': [111],
            'scope_3_secondary_source': [112],
            'scope_3_secondary_source_emissions': [113],
            'decarbonisation_strategy_set': [117],
            'ghg_reduction_target_set': [118],
            'long_term_net_zero_goal_set': [119],
            'year_on_year_emissions_profile': [120],
            'year_on_year_emissions_profile_qualitative': [121],
            'contribution_to_climate_solutions': [122],
            
            'total_energy_consumption': [126, 237],
            'energy_consumption_renewable': [127, 239],
            'total_emissions_to_water': [131, 281],
            'quantity_hazardous_radioactive_waste_generated': [132, 285],
            'circular_economy_principles': [133],
            'sites_affecting_biodiversity_areas': [137, 277],
            'number_of_ftes_end_of_report_year_female': [143],
            'number_of_ftes_end_of_report_year_non_binary': [144],
            'number_of_ftes_end_of_report_year_non_disclosed': [145],
            'number_of_ftes_end_of_report_year_male': [146],
            'total_csuite_employees': [147],
            'number_of_csuite_female': [148],
            'number_of_csuite_non_binary': [149],
            'number_of_csuite_non_disclosed': [150],
            'number_of_csuite_male': [151],
            'total_founders_still_employed': [152],
            'number_of_founders_still_employed_female': [153],
            'number_of_founders_still_employed_non_binary': [154],
            'number_of_founders_still_employed_non_disclosed': [155],
            'number_of_founders_still_employed_male': [156],
            'unadjusted_gender_pay_gap': [160, 298], 
            'number_of_new_hires_inside_eu_fte': [164],
            'number_of_new_hires_outside_eu_fte': [165],
            'number_of_leavers_inside_eu_fte': [166],
            'number_of_leavers_outside_eu_fte': [167],
            'number_of_new_hires_ma_fte': [168],
            'number_of_leavers_ma_fte': [169],
            'number_of_organic_net_new_hires_fte': [170],
            'number_of_total_net_new_hires_fte': [171],
            'turnover_fte': [172],
            'implements_employee_survey_questionnaires': [176],
            'percentage_employees_responding_employee_survey': [177],
            'implemented_whistleblower_procedure': [178],
            'number_of_workrelated_injuries': [182],
            'workrelated_injuries_qualitative': [183],
            'number_of_workrelated_fatalities': [184],
            'days_lost_due_to_injury': [185],
            'human_rights_due_diligence_process': [189],
            'total_number_of_board_members': [195, 304],
            'number_of_board_members_female': [196, 302],
            'number_of_board_members_non_binary': [197],
            'number_of_board_members_non_disclosed': [198],
            'number_of_board_members_male': [199, 303],
            'number_of_board_members_underrepresented_groups': [200],
            'number_of_independent_board_members': [201],
            'number_of_data_breaches': [205],
            'data_breaches_qualitative': [206],
            'cyber_scheduled_scans': [208],
            'cyber_penetration_testing': [209],
            'cyber_lifecycle_security_testing': [210],
            'cyber_other': [211],
            'cyber_other_specify': [212],
            'cyber_no_programme': [213],
            
            'total_scope_2_emissions_location_based': [225],
            'total_scope_2_emissions_market_based': [226],
            'total_ghg_emissions_location_based': [228],
            'total_ghg_emissions_market_based': [229],
            'active_in_fossil_sector': [233],
            'non_renewable_energy_consumption': [238],
            'total_energy_production': [240],
            'non_renewable_energy_production': [241],
            'renewable_energy_production': [242],
            'high_impact_climate_section_a_agriculture_forestry_fishing': [247],
            'high_impact_climate_section_a_agriculture_forestry_fishing_energy_consumption_gwh': [248],
            'high_impact_climate_section_a_agriculture_forestry_fishing_gross_revenue': [249],
            'high_impact_climate_section_b_mining_quarrying': [250],
            'high_impact_climate_section_b_mining_quarrying_energy_consumption_gwh': [251],
            'high_impact_climate_section_b_mining_quarrying_gross_revenue': [252],
            'high_impact_climate_section_c_manufacturing': [253],
            'high_impact_climate_section_c_manufacturing_energy_consumption_gwh': [254],
            'high_impact_climate_section_c_manufacturing_gross_revenue': [255],
            'high_impact_climate_section_d_electricity_gas_steam_air_conditioning_supply': [256],
            'high_impact_climate_section_d_electricity_gas_steam_air_conditioning_supply_energy_consumption_gwh': [257],
            'high_impact_climate_section_d_electricity_gas_steam_air_conditioning_supply_gross_revenue': [258],
            'high_impact_climate_section_e_water_supply_sewerage_waste_management_remediation_activities': [259],
            'high_impact_climate_section_e_water_supply_sewerage_waste_management_remediation_activities_energy_consumption_gwh': [260],
            'high_impact_climate_section_e_water_supply_sewerage_waste_management_remediation_activities_gross_revenue': [262],
            'high_impact_climate_section_f_construction': [262],
            'high_impact_climate_section_f_construction_energy_consumption_gwh': [263],
            'high_impact_climate_section_f_construction_gross_revenue': [264],
            'high_impact_climate_section_g_wholesale_retail_trade_repair_motor_vehicles_motorcycles': [265],
            'high_impact_climate_section_g_wholesale_retail_trade_repair_motor_vehicles_motorcycles_energy_consumption_gwh': [266],
            'high_impact_climate_section_g_wholesale_retail_trade_repair_motor_vehicles_motorcycles_gross_revenue': [267],
            'high_impact_climate_section_h_transportation_storage': [268],
            'high_impact_climate_section_h_transportation_storage_energy_consumption_gwh': [269],
            'high_impact_climate_section_h_transportation_storage_gross_revenue': [270],
            'violating_ungp_oecd': [289],
            'type_of_violations_ungc_oecd_guidelines':[290],
            'has_processes_monitor_ungp_oecd':[294],
            'involved_in_controversial_weapons':[308],
        }

        current_col = 5  # Starting column (E)
        

        # Iterate over the valid data (companies)
        for company_id, metrics in companies_data.items():
            print(f"Processing company '{company_id}' at column {current_col}")
            result = {item["compound_id"]: item["interpreted_value"] for item in metrics}
            for metric, value in result.items():
                if not value.strip():
                    print(f"Skipping empty value for metric '{metric}' in company '{company_id}'.")
                    continue
                rows = row_mapping.get(metric, [])
                if not rows:
                    print(f"Warning: No row mapping found for metric '{metric}'.")
                    continue
                for row in rows:
                    print(f"Writing '{value}' to row {row}, column {current_col}")
                    ws.cell(row=row, column=current_col).value = value
            current_col += 1

        # Save the file
        wb.save(output_path)
        
        @after_this_request
        def delete_file(response):
            if os.path.exists(output_path):
                os.remove(output_path)
            return response
        
       # Return the file as a response for download
        return send_file(output_path, as_attachment=True, download_name="InvestEurope_Template_Completed.xlsx")

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
    
### FUND VALIDATION LOGIC ###

def validate_metrics_by_fund(fund_data: dict, schema: dict):
    """
    Validates the data for a single fund based on the provided schema.
    
    Args:
        fund_data (dict): Data for a single fund, containing metrics and statuses.
        schema (dict): Validation schema for the metrics.
    
    Returns:
        dict: A summary of validation results for the company.
    """
    fund_metrics = fund_data["metrics"]
    fund_statuses = fund_data["status"]
    valid_lines = []
    error_lines = []
    unknown_lines = []
    blank_lines = []
    recommended_but_missing_lines = []
    missing_metrics = []
    
    for compound_id in ALL_FUND_METRICS:
        if compound_id not in fund_metrics:
            level = (
                "Strongly recommended" if compound_id in REQUIRED_FUND_METRICS
                else "Value not required"
            )
            missing_metrics.append({
                "compound_id": compound_id,
                "requirement_level": level,
                "reason": "Not in import file at all",
            })
            
        else:
            raw_value = fund_metrics[compound_id]
            status = fund_statuses.get(compound_id, "")

            # Handle not_applicable or not_available
            if status in ["not_applicable", "not_available"]:
                reason = (
                    "Marked as not applicable in import file"
                    if status == "not_applicable"
                    else "Marked as not available in import file"
                )
                level = (
                    "Strongly recommended" if compound_id in REQUIRED_FUND_METRICS
                    else "Value not required"
                )
                
                if level == "Strongly recommended":
                    recommended_but_missing_lines.append({
                        "compound_id": compound_id,
                        "requirement_level": level,
                        "reason": "Status is 'not_applicable' or 'not_available', but this is a strongly recommended metric.",
                    })
                else: 
                    blank_lines.append({
                        "compound_id": compound_id,
                        "requirement_level": level,
                        "reason": reason,
                    })
                continue  # Skip schema validation for these metrics

            # Handle blank values
            if raw_value == "" and status == "provided":
                error_lines.append({
                    "compound_id": compound_id,
                    "raw_value": raw_value,
                    "error_notes": "Value is blank but marked as 'provided'.",
                })
            elif status == "provided":
                # Validate value if not blank or excluded
                typed_value = get_typed_value(schema=SCHEMA_FUND, value=raw_value, compound_id=compound_id)
                interpreted_value = get_interpreted_value_fund_with_units(value=raw_value, compound_id=compound_id)

                validator = Validator({compound_id: schema.get(compound_id, {})})
                validation_data = {compound_id: typed_value}

                if validator.validate(validation_data):
                    valid_lines.append({
                        "compound_id": compound_id,
                        "raw_value": typed_value,
                        "interpreted_value": interpreted_value,
                    })
                else:
                    error_lines.append({
                        "compound_id": compound_id,
                        "raw_value": raw_value,
                        "error_notes": str(validator.errors),
                    })
                    
            else: 
                error_lines.append({
                    "compound_id": compound_id,
                    "raw_value": raw_value,
                    "error_notes": f"Unknown value in 'STATUS' column: {status}.",
                })
                
    # Special relationships validation
    special_relations = [
        # Removed in 2025/6
        # {
        #     "condition_id": "good_governance_post_investment",
        #     "condition_value": "yes",
        #     "dependent_ids": ["good_governance_post_investment_frequency"]
        # },
        {
            "condition_id": "adhere_to_ungc",
            "condition_value": "no",
            "dependent_ids": ["no_ungc_explanation"]
        },
        {
            "condition_id": "fund_marketing_under_sfdr",
            "condition_value": "article_8",
            "dependent_ids": [
                "article_8_sustainable_investment_commitment",
                "article_8_eu_taxonomy_alignment",
                "article_8_non_eu_taxonomy_environmental_objective",
                "article_8_social_objective_investment",
                "article_8_considers_significant_negative_impacts",
                "article_8_ghg_reduction_target",
                "article_8_uses_index_as_reference_benchmark",
            ]
        },
        {
            "condition_id": "article_8_sustainable_investment_commitment",
            "condition_value": "yes",
            "dependent_ids": ["article_8_sustainable_investment_commitment_minimum_share_percentage"]
        },
        {
            "condition_id": "article_8_eu_taxonomy_alignment",
            "condition_value": "yes",
            "dependent_ids": ["article_8_eu_taxonomy_alignment_minimum_share_percentage"]
        },
        {
            "condition_id": "article_8_non_eu_taxonomy_environmental_objective",
            "condition_value": "yes",
            "dependent_ids": ["article_8_non_eu_taxonomy_environmental_objective_minimum_share_percentage"]
        },
        {
            "condition_id": "article_8_social_objective_investment",
            "condition_value": "yes",
            "dependent_ids": ["article_8_social_objective_investment_minimum_share_percentage"]
        },
        {
            "condition_id": "article_8_ghg_reduction_target",
            "condition_value": "yes",
            "dependent_ids": [
                "article_8_ghg_reduction_target_main_strategy",
                "article_8_ghg_reduction_target_ambition",
                "article_8_ghg_reduction_target_financed_emissions_baseline",
                "article_8_ghg_reduction_target_base_year",
                "article_8_ghg_reduction_target_target_year",
                "article_8_ghg_reduction_target_financed_emissions_reporting",
            ]
        },
        {
            "condition_id": "fund_marketing_under_sfdr",
            "condition_value": "article_9",
            "dependent_ids": [
                "article_9_sustainable_investment_commitment",
                "article_9_eu_taxonomy_alignment",
                "article_9_non_eu_taxonomy_environmental_objective",
                "article_9_social_objective_investment",
                "article_9_considers_significant_negative_impacts",
                "article_9_ghg_reduction_target",
                "article_9_uses_index_as_reference_benchmark",
            ]
        },
        {
            "condition_id": "article_9_sustainable_investment_commitment",
            "condition_value": "yes",
            "dependent_ids": ["article_9_sustainable_investment_commitment_minimum_share_percentage"]
        },
        {
            "condition_id": "article_9_eu_taxonomy_alignment",
            "condition_value": "yes",
            "dependent_ids": ["article_9_eu_taxonomy_alignment_minimum_share_percentage"]
        },
        {
            "condition_id": "article_9_non_eu_taxonomy_environmental_objective",
            "condition_value": "yes",
            "dependent_ids": ["article_9_non_eu_taxonomy_environmental_objective_minimum_share_percentage"]
        },
        {
            "condition_id": "article_9_social_objective_investment",
            "condition_value": "yes",
            "dependent_ids": ["article_9_social_objective_investment_minimum_share_percentage"]
        },
        {
            "condition_id": "article_9_ghg_reduction_target",
            "condition_value": "yes",
            "dependent_ids": [
                "article_9_ghg_reduction_target_main_strategy",
                "article_9_ghg_reduction_target_ambition",
                "article_9_ghg_reduction_target_financed_emissions_baseline",
                "article_9_ghg_reduction_target_base_year",
                "article_9_ghg_reduction_target_target_year",
                "article_9_ghg_reduction_target_financed_emissions_reporting",
                "article_9_ghg_reduction_target_1_5_c_aligned",
            ]
        },
        {
            "condition_ids": [
                "number_of_partners_female",
                "number_of_partners_non_binary",
                "number_of_partners_non_disclosed",
                "number_of_partners_male"
            ],
            "total_field": "total_number_of_partners"
        },
        {
            "condition_id": "gender_diversity_pipeline_tracked",
            "condition_value": "yes",
            "dependent_ids": [
                "gender_diversity_pipeline_strategy_fit",
                "gender_diversity_pipeline_dd_undertaken",
                "gender_diversity_pipeline_term_sheet_issued",
            ]
        },
    ]
    
    
    required = REQUIRED_FUND_METRICS[:]

    for relation in special_relations:
        
        # Checks to make sure the total is always there for a metric that is a subset of that total (e.g., female FTE requires total FTE)
        if "condition_ids" in relation:
            # Check if any one of the fields has a value
            if any(fund_metrics.get(condition_id) for condition_id in relation["condition_ids"]):
                total_field = relation["total_field"]
                # Ensure the total field is not marked as not_applicable or not_available
                total_status = fund_statuses.get(total_field, "")
                
                if total_field not in fund_metrics:
                    #Replace line in missing metrics with more detail
                    missing_metrics = [line for line in missing_metrics if line["compound_id"] != total_field]
                    missing_metrics.append({
                        "compound_id": total_field,
                        "requirement_level": f"Strongly recommended because at least one value is provided for {', '.join(relation['condition_ids'])}",
                        "reason": "Not in import file at all",
                    })
                    blank_lines = [line for line in blank_lines if line["compound_id"] != total_field]
                    
                elif fund_metrics[total_field] == "":
                    #Replace line in missing metrics with more detail
                    missing_metrics = [line for line in missing_metrics if line["compound_id"] != total_field]
                    missing_metrics.append({
                        "compound_id": total_field,
                        "requirement_level": f"Strongly recommended because at least one value is provided for {', '.join(relation['condition_ids'])}",
                        "reason": "Value is blank",
                    })
                    valid_lines = [line for line in valid_lines if line["compound_id"] != total_field]
                    blank_lines = [line for line in blank_lines if line["compound_id"] != total_field]

                elif total_status in ["not_applicable", "not_available"]:
                    #Replace line in recommended_but_missing_lines metrics with more detail
                    recommended_but_missing_lines = [line for line in recommended_but_missing_lines if line["compound_id"] != total_field]
                    recommended_but_missing_lines.append({
                        "compound_id": total_field,
                        "requirement_level": f"Strongly recommended because at least one value is provided for {', '.join(relation['condition_ids'])}",
                        "reason": "Marked as not_applicable or not_available"
                    })
                    blank_lines = [line for line in blank_lines if line["compound_id"] != total_field]
                    
        else:   # Checks dependencies, e.g., percentage_turnover_tobacco_activities is required if tobacco_activities = 'yes'

            condition_id = relation["condition_id"]
            condition_value = relation["condition_value"]
            dependent_ids = relation["dependent_ids"]

            if fund_metrics.get(condition_id) == condition_value:
                for dependent_id in dependent_ids:
                    if dependent_id not in fund_metrics:
                        #Replace line in missing metrics with more detail
                        missing_metrics = [line for line in missing_metrics if line["compound_id"] != dependent_id]
                        missing_metrics.append({
                            "compound_id": dependent_id,
                            "requirement_level": f"Strongly recommended because '{condition_id}' is '{condition_value}'",
                            "reason": "Not in import file at all",
                        })
                        blank_lines = [line for line in blank_lines if line["compound_id"] != dependent_id]
                        
                    elif fund_metrics[dependent_id] == "" and fund_statuses.get(dependent_id, "") not in ["not_applicable", "not_available"]:
                        #Replace line in missing metrics with more detail
                        missing_metrics = [line for line in missing_metrics if line["compound_id"] != dependent_id]
                        missing_metrics.append({
                            "compound_id": dependent_id,
                            "requirement_level": f"Strongly recommended because '{condition_id}' is '{condition_value}'",
                            "reason": "Value is blank",
                        })
                        valid_lines = [line for line in valid_lines if line["compound_id"] != dependent_id]
                        blank_lines = [line for line in blank_lines if line["compound_id"] != dependent_id]
                        
                    elif fund_statuses.get(dependent_id, "") in ["not_applicable", "not_available"]:
                        #Replace line in recommended_but_missing_lines metrics with more detail
                        recommended_but_missing_lines = [line for line in recommended_but_missing_lines if line["compound_id"] != dependent_id]
                        recommended_but_missing_lines.append({
                            "compound_id": dependent_id,
                            "requirement_level": f"Strongly recommended because '{condition_id}' is '{condition_value}'",
                            "reason": "Marked as not_applicable or not_available",
                        })
                        blank_lines = [line for line in blank_lines if line["compound_id"] != dependent_id]

                        
                    required.append(dependent_id)
                        
    # Handle unknown compound IDs
    for compound_id in fund_metrics.keys():
        if compound_id not in schema:
            unknown_lines.append({
                "compound_id": compound_id,
                "raw_value": fund_metrics[compound_id],
                "error_notes": "Unknown compound ID",
            })
            
    provided_required_lines = [line for line in valid_lines if line["compound_id"] in required]
    
    percentage_completion = round((len(provided_required_lines) / len(required)) * 100, 2)

    # Return the fund summary
    return {
        "company_name": fund_metrics.get("fund_name", "Unknown Fund"),
        "valid_lines": len(valid_lines),
        "invalid_lines": len(error_lines) + len(missing_metrics),
        "percent_completion": percentage_completion,
        "correct_lines": valid_lines,
        "error_lines": error_lines,
        "unknown_lines": unknown_lines,
        "missing_metrics": missing_metrics,
        "blank_lines": blank_lines,
        "recommended_but_missing_lines": recommended_but_missing_lines,
    }                      

def get_interpreted_value_fund(value: str, compound_id: str):
    """
    Interprets the value for a given compound_id using the SCHEMA_FUND and OPTIONS objects.
    
    :param compound_id: The compound ID (key) to look up in SCHEMA_FUND and OPTIONS.
    :param value: The typed value to interpret.
    :return: Interpreted value if found, else returns the value unchanged.
    """
    # Check if compound_id exists in SCHEMA_FUND
    if compound_id in SCHEMA_FUND:
        schema_entry = SCHEMA_FUND[compound_id]
        allowed_values = schema_entry.get("allowed")

        # If allowed values exist and are linked to a key in OPTIONS_FUND
        if allowed_values:
            # Find the key in OPTIONS_FUND by checking 'allowed' values
            for options_key, options_dict in OPTIONS_FUND.items():
                if set(allowed_values).issubset(options_dict.keys()):
                    # Use the alue to get the interpreted value
                    interpreted_value = options_dict.get(value)
                    if interpreted_value:
                        return interpreted_value
    
    # Fallback: return the value unchanged if no interpretation is found
    return value

def get_interpreted_value_fund_with_units(value: str, compound_id: str):
    """
    Interprets the value for a given compound_id and appends the corresponding unit if applicable.

    :param compound_id: The compound ID (key) to look up.
    :param value: The typed value to interpret.
    :return: Interpreted value with unit appended if applicable.
    """
    interpreted_value = get_interpreted_value_fund(value, compound_id)

    # Add the unit if the compound ID is in the COMPOUND_ID_UNITS mapping
    if compound_id in FUND_COMPOUND_ID_UNITS:
        unit = FUND_COMPOUND_ID_UNITS[compound_id]
        
        return f"{interpreted_value} {unit}"

    return interpreted_value

def validate_fund_csv(csv_path: str) -> list[dict]:
    # Step 1: Read and organize the CSV data. Since it can only process 1 fund csv at a time, the UUID is just '1'.
    fund_data = read_and_organize_csv(csv_path, company_id="1")

    # Step 2: Validate metrics against the schema and organize data
    fund_summary = validate_metrics_by_fund(fund_data["1"], SCHEMA_FUND)

    return fund_summary


@app.route('/uploadfund', methods=['POST'])
def upload_file_fund():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    errors = []
    
    if not file.filename.lower().endswith('.csv'):
        errors.append(f"{file.filename}: Invalid file type. Only .csv files are accepted.")
        return jsonify({"errors": errors}), 400

    # Save the uploaded file temporarily for validation
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        # Validate and read the CSV file
         validation_results = validate_fund_csv(file_path)
    except ValueError as e:
        errors.append(f"{file.filename}: {str(e)}")
    finally:
        os.remove(file_path)  # Clean up the file after processing
        
    # Render results as HTML table
    return render_template('validation_results_fund_gp.html', fund=validation_results)

### GP VALIDATION LOGIC ###

def validate_metrics_by_gp(gp_data: dict, schema: dict):
    """
    Validates the data for a single GP based on the provided schema.
    
    Args:
        gp_data (dict): Data for a single GP, containing metrics and statuses.
        schema (dict): Validation schema for the metrics.
    
    Returns:
        dict: A summary of validation results for the GP.
    """
    gp_metrics = gp_data["metrics"]
    gp_statuses = gp_data["status"]
    valid_lines = []
    error_lines = []
    unknown_lines = []
    blank_lines = []
    recommended_but_missing_lines = []
    missing_metrics = []
    
    for compound_id in ALL_GP_METRICS:
        if compound_id not in gp_metrics:
            level = (
                "Strongly recommended" if compound_id in REQUIRED_GP_METRICS
                else "Value not required"
            )
            missing_metrics.append({
                "compound_id": compound_id,
                "requirement_level": level,
                "reason": "Not in import file at all",
            })
            
        else:
            raw_value = gp_metrics[compound_id]
            status = gp_statuses.get(compound_id, "")

            # Handle not_applicable or not_available
            if status in ["not_applicable", "not_available"]:
                reason = (
                    "Marked as not applicable in import file"
                    if status == "not_applicable"
                    else "Marked as not available in import file"
                )
                level = (
                    "Strongly recommended" if compound_id in REQUIRED_GP_METRICS
                    else "Value not required"
                )
                
                if level == "Strongly recommended":
                    recommended_but_missing_lines.append({
                        "compound_id": compound_id,
                        "requirement_level": level,
                        "reason": "Status is 'not_applicable' or 'not_available', but this is a strongly recommended metric.",
                    })
                else: 
                    blank_lines.append({
                        "compound_id": compound_id,
                        "requirement_level": level,
                        "reason": reason,
                    })
                continue  # Skip schema validation for these metrics

            # Handle blank values
            if raw_value == "" and status == "provided":
                error_lines.append({
                    "compound_id": compound_id,
                    "raw_value": raw_value,
                    "error_notes": "Value is blank but marked as 'provided'.",
                })
            elif status == "provided":
                # Validate value if not blank or excluded
                typed_value = get_typed_value(schema=SCHEMA_GP, value=raw_value, compound_id=compound_id)
                interpreted_value = get_interpreted_value_gp_with_units(value=raw_value, compound_id=compound_id)

                validator = Validator({compound_id: schema.get(compound_id, {})})
                validation_data = {compound_id: typed_value}

                if validator.validate(validation_data):
                    valid_lines.append({
                        "compound_id": compound_id,
                        "raw_value": typed_value,
                        "interpreted_value": interpreted_value,
                    })
                else:
                    error_lines.append({
                        "compound_id": compound_id,
                        "raw_value": raw_value,
                        "error_notes": str(validator.errors),
                    })
                    
            else: 
                error_lines.append({
                    "compound_id": compound_id,
                    "raw_value": raw_value,
                    "error_notes": f"Unknown value in 'STATUS' column: {status}.",
                })
                
    # Special relationships validation
    special_relations = [
        
        {
            "condition_id": "use_of_international_disclosing_standard",
            "condition_value": "yes",
            "dependent_ids": [
                "use_of_international_disclosing_standard_tcfd",
                "use_of_international_disclosing_standard_gri",
                "use_of_international_disclosing_standard_sasb",
                "use_of_international_disclosing_standard_tnfd",
                "use_of_international_disclosing_standard_sbti",
                "use_of_international_disclosing_standard_cdp",
                "use_of_international_disclosing_standard_issb",
                "use_of_international_disclosing_standard_esrs",
                "use_of_international_disclosing_standard_other"
            ]
        },
        {
            "condition_id": "participates_in_sustainability_climate_initiatives",
            "condition_value": "yes",
            "dependent_ids": [
                "participates_in_sustainability_climate_initiatives_pri",
                "participates_in_sustainability_climate_initiatives_nzami",
                "participates_in_sustainability_climate_initiatives_ici",
                "participates_in_sustainability_climate_initiatives_transition_pathway_initiative",
                "participates_in_sustainability_climate_initiatives_smi",
                "participates_in_sustainability_climate_initiatives_other"
            ]
        },
         # REMOVED in 2025 Update
        # {
        #     "condition_id": "ems_implemented",
        #     "condition_value": "yes_other_ems_certification",
        #     "dependent_ids": ["other_ems_certification"]
        # },
        #NEW in 2025
        {
            "condition_id": "number_of_esg_incidents",
            "condition_value": "yes",
            "dependent_ids": ["qualitative_info_esg_incidents"]
        },
        {
            "condition_ids": [
                "number_of_ftes_end_of_report_year_female",
                "number_of_ftes_end_of_report_year_non_binary",
                "number_of_ftes_end_of_report_year_non_disclosed",
                "number_of_ftes_end_of_report_year_male"
            ],
            "total_field": "total_ftes_end_of_report_year"
        },
        {
            "condition_ids": [
                "number_of_partners_female",
                "number_of_partners_non_binary",
                "number_of_partners_non_disclosed",
                "number_of_partners_male"
            ],
            "total_field": "total_number_of_partners"
        }
    ]
    
    required = REQUIRED_GP_METRICS[:]
    for relation in special_relations:
        # Checks to make sure the total is always there for a metric that is a subset of that total (e.g., female FTE requires total FTE)
        if "condition_ids" in relation:
            # Check if any one of the fields has a value
            if any(gp_metrics.get(condition_id) for condition_id in relation["condition_ids"]):
                total_field = relation["total_field"]
                # Ensure the total field is not marked as not_applicable or not_available
                total_status = gp_statuses.get(total_field, "")
                
                if total_field not in gp_metrics:
                    #Replace line in missing metrics with more detail
                    missing_metrics = [line for line in missing_metrics if line["compound_id"] != total_field]
                    missing_metrics.append({
                        "compound_id": total_field,
                        "requirement_level": f"Strongly recommended because at least one value is provided for {', '.join(relation['condition_ids'])}",
                        "reason": "Not in import file at all",
                    })
                    blank_lines = [line for line in blank_lines if line["compound_id"] != total_field]
                    
                elif gp_metrics[total_field] == "" and total_status not in ["not_applicable", "not_available"]:
                    #Replace line in missing metrics with more detail
                    missing_metrics = [line for line in missing_metrics if line["compound_id"] != total_field]
                    missing_metrics.append({
                        "compound_id": total_field,
                        "requirement_level": f"Strongly recommended because at least one value is provided for {', '.join(relation['condition_ids'])}",
                        "reason": "Value is blank",
                    })
                    valid_lines = [line for line in valid_lines if line["compound_id"] != total_field]
                    blank_lines = [line for line in blank_lines if line["compound_id"] != total_field]

                elif total_status in ["not_applicable", "not_available"]:
                    #Replace line in recommended_but_missing_lines metrics with more detail
                    recommended_but_missing_lines = [line for line in recommended_but_missing_lines if line["compound_id"] != total_field]
                    recommended_but_missing_lines.append({
                        "compound_id": total_field,
                        "requirement_level": f"Strongly recommended because at least one value is provided for {', '.join(relation['condition_ids'])}",
                        "reason": "Marked as not_applicable or not_available"
                    })
                    blank_lines = [line for line in blank_lines if line["compound_id"] != total_field]
                    
   
        else:  # Checks dependencies, e.g., percentage_turnover_tobacco_activities is required if tobacco_activities = 'yes'
            condition_id = relation["condition_id"]
            condition_value = relation["condition_value"]
            dependent_ids = relation["dependent_ids"]

            if gp_metrics.get(condition_id) == condition_value:
                for dependent_id in dependent_ids:
                    if dependent_id not in gp_metrics:
                        #Replace line in missing metrics with more detail
                        missing_metrics = [line for line in missing_metrics if line["compound_id"] != dependent_id]
                        missing_metrics.append({
                            "compound_id": dependent_id,
                            "requirement_level": f"Strongly recommended because '{condition_id}' is '{condition_value}'",
                            "reason": "Not in import file at all",
                        })
                        blank_lines = [line for line in blank_lines if line["compound_id"] != dependent_id]
                        
                    elif gp_metrics[dependent_id] == "" and gp_statuses.get(dependent_id, "") not in ["not_applicable", "not_available"]:
                        #Replace line in missing metrics with more detail
                        missing_metrics = [line for line in missing_metrics if line["compound_id"] != dependent_id]
                        missing_metrics.append({
                            "compound_id": dependent_id,
                            "requirement_level": f"Strongly recommended because '{condition_id}' is '{condition_value}'",
                            "reason": "Value is blank",
                        })
                        valid_lines = [line for line in valid_lines if line["compound_id"] != dependent_id]
                        blank_lines = [line for line in blank_lines if line["compound_id"] != dependent_id]
                        
                    elif gp_statuses.get(dependent_id, "") in ["not_applicable", "not_available"]:
                        #Replace line in recommended_but_missing_lines metrics with more detail
                        recommended_but_missing_lines = [line for line in recommended_but_missing_lines if line["compound_id"] != dependent_id]
                        recommended_but_missing_lines.append({
                            "compound_id": dependent_id,
                            "requirement_level": f"Strongly recommended because '{condition_id}' is '{condition_value}'",
                            "reason": "Marked as not_applicable or not_available",
                        })
                        blank_lines = [line for line in blank_lines if line["compound_id"] != dependent_id]

                    
                        
                    required.append(dependent_id)
                        
    # Handle unknown compound IDs
    for compound_id in gp_metrics.keys():
        if compound_id not in schema:
            unknown_lines.append({
                "compound_id": compound_id,
                "raw_value": gp_metrics[compound_id],
                "error_notes": "Unknown compound ID",
            })
            
    provided_required_lines = [line for line in valid_lines if line["compound_id"] in required]

            
    percentage_completion = round((len(provided_required_lines) / len(required)) * 100, 2)

    # Return the gp summary
    return {
        "company_name": gp_metrics.get("gp_name", "Unknown GP"),
        "valid_lines": len(valid_lines),
        "invalid_lines": len(error_lines),
        "percent_completion": percentage_completion,
        "correct_lines": valid_lines,
        "error_lines": error_lines,
        "unknown_lines": unknown_lines,
        "missing_metrics": missing_metrics,
        "blank_lines": blank_lines,
        "recommended_but_missing_lines": recommended_but_missing_lines,
    }

def get_interpreted_value_gp(value: str, compound_id: str):
    """
    Interprets the value for a given compound_id using the SCHEMA_GP and OPTIONS objects.
    
    :param compound_id: The compound ID (key) to look up in SCHEMA_GP and OPTIONS.
    :param value: The typed value to interpret.
    :return: Interpreted value if found, else returns the value unchanged.
    """
    # Check if compound_id exists in SCHEMA_GP
    if compound_id in SCHEMA_GP:
        schema_entry = SCHEMA_GP[compound_id]
        allowed_values = schema_entry.get("allowed")

        # If allowed values exist and are linked to a key in OPTIONS_GP
        if allowed_values:
            # Find the key in OPTIONS_GP by checking 'allowed' values
            for options_key, options_dict in OPTIONS_GP.items():
                if set(allowed_values).issubset(options_dict.keys()):
                    # Use the value to get the interpreted value
                    interpreted_value = options_dict.get(value)
                    if interpreted_value:
                        return interpreted_value
    
    # Fallback: return the value unchanged if no interpretation is found
    return value

def get_interpreted_value_gp_with_units(value: str, compound_id: str):
    """
    Interprets the value for a given compound_id and appends the corresponding unit if applicable.

    :param compound_id: The compound ID (key) to look up.
    :param value: The typed value to interpret.
    :return: Interpreted value with unit appended if applicable.
    """
    interpreted_value = get_interpreted_value_gp(value, compound_id)

    # Add the unit if the compound ID is in the COMPOUND_ID_UNITS mapping
    if compound_id in GP_COMPOUND_ID_UNITS:
        unit = GP_COMPOUND_ID_UNITS[compound_id]
        
        return f"{interpreted_value} {unit}"

    return interpreted_value

def validate_gp_csv(csv_path: str) -> list[dict]:
    # Step 1: Read and organize the CSV data
    gp_data = read_and_organize_csv(csv_path, company_id="1")

    # Step 2: Validate metrics against the schema and organize data
    gp_summary = validate_metrics_by_gp(gp_data["1"], SCHEMA_GP)

    return gp_summary

@app.route('/uploadgp', methods=['POST'])
def upload_file_gp():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    errors = []
    
    if not file.filename.lower().endswith('.csv'):
        errors.append(f"{file.filename}: Invalid file type. Only .csv files are accepted.")
        return jsonify({"errors": errors}), 400

    # Save the uploaded file temporarily for validation
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        # Validate and read the CSV file
         validation_results = validate_gp_csv(file_path)
    except ValueError as e:
        errors.append(f"{file.filename}: {str(e)}")
    finally:
        os.remove(file_path)  # Clean up the file after processing
        
    # Render results as HTML table
    return render_template('validation_results_fund_gp.html', fund=validation_results)


if __name__ == '__main__':
    app.run(debug=True)

from .executor import Executor

def handler(event, context):
    """
    serverless invoke local -f wmr-s3-parser
    --path pricers-etl/src/pricers_etl/
    importers/testEvents/wmrFile.json
    """
    main(event)


def main(event):
    pass

    # Get the file data
    file_config = {
        "file_name" : "pcs.csv",
        "file_ext" : "csv",
        "file_path" : "",
        "file_remote_store" : "blob",
        "file_remote_path" : "container-id",
        "file_remote_access_key" : "",
        "file_header" : ("id", "name", "code"),
        "file_validation_rule" : ("name", "required_data_point_exists"),
        "generate_catd" : True,
        "data_columns_to_generate_catd" : ("id"),
    }

    # Get the file Meta Data

    # create a pipeline
    execution_pipeline = [
        csl_sl.calc_is_pricing_day,
        csl_sl.calc_leap_value,
        csl_sl.calc_app_rate,
        csl_sl.calc_number_of_days_to_settle,
        csl_sl.calc_capital_adjustment,
        csl_sl.calc_is_market_disruption,
        csl_sl.calc_is_t_pricing_day,
        csl_sl.calc_is_indicative_pricing,
        csl_sl.calc_nav_type,
        csl_sl.calc_nav,
        csl_sl.calc_aum,
        csl_sl.calc_cash_component,
        csl_sl.calc_lead_line_totals,
        csl_sl.calc_next_line_totals,
        csl_sl.calc_line_total,
        csl_sl.calc_lead_hedged_positions,
        csl_sl.calc_next_hedged_positions,
        csl_sl.calc_hedged_positions,
        csl_sl.calc_creation_redemption_price,
    ]   

    # execute the pipeline 
    executor = Executor(execution_pipeline)
    stats = executor.execute(stats)
    
    # Save data into Database
   

    # Save the Responce into a file

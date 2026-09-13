import pandas as pd
from ingest.db import get_engine, write_dataframe
import logging
import yaml
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "models.yml"

with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f)

FEATURE_COLS = CONFIG["nearest_neighbors"]["feature_cols"]
REFERENCE_COLS = CONFIG["nearest_neighbors"]["reference_cols"]
NEIGHBORS_TABLE_NAME = "forecast_nearest_neighbors"
SCHEMA = 'gold'


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

QUERY = """
    with associated_session as (
        select
            ls.session_date
            , hl.time_block
            , hl.rating
            , hl.comment
        from gold.human_labels hl 
        left join gold.labeling_sessions ls
            on hl.session_id = ls.id
    ) 

    , time_group_logic as (
        select
            *
            , case when hour_of_day between 0 and 10 then 'morning'
                when hour_of_day between 11 and 15 then 'midday'
                when hour_of_day between 16 and 23 then 'evening'
                else null
            end as time_block
            , date(forecast_time - interval '4' hour) as forecast_date
        from gold.scored_forecasts
        
    )

    select
        tg.*
        , a.rating
        , a.comment
    from time_group_logic tg
    left join associated_session a
        on cast(forecast_date as date) = cast(a.session_date as date)
        and tg.time_block = a.time_block
    where break_id = 'belmar'
    order by forecast_time desc
"""


def get_data(engine, query = QUERY):
    with engine.connect() as conn:
        try:
            df = pd.read_sql(query, conn)
        except Exception as e:
            logging.error(f"Read failed: {e}")
            raise
    return df 


def preprocess_data(df, feature_cols: list):
    '''
    Prepare data for nearest neighbor fitting
        Includes:
            - Dropping columns
            - Handling nulls (the only nulls should be the tide columns)
            - Scaling features
    '''
    df = df.copy()

    # 1. Drop Columns
    df_features = df[feature_cols]

    # 2. Handle nulls
    df_nonnull_mask = df_features.notna().all(axis=1)
    df_features = df_features[df_nonnull_mask]

    # 3. Scaling Features
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_features)
    df_scaled = pd.DataFrame(df_scaled, columns=df_features.columns, index=df_features.index)

    return df_scaled


def fit_nearest_neighbors(df_ref, df_scaled, reference_cols: list):
    '''
    Find the nearest RATED neighbors to future UNRATED forecasts
        - Isolate the data points that have been rated that we want to associate to a forecast
        - Associate the rated data points to their nearest future forecasted date using nearest neighbors
    '''

    # Restrict to df_scaled's index (rows dropped for null features in preprocess_data
    # are excluded here too) so every mask below stays aligned with df_scaled by index.
    df_reference = df_ref.loc[df_scaled.index, reference_cols]
    rated_mask = df_reference['rating'].notna()
    df_rated = df_scaled[rated_mask].reset_index(drop=True) 
    df_rated_reference = df_reference[rated_mask].reset_index(drop=True)   # identity/labels for that same pool, same order
    future_mask = df_reference['forecast_time'] > pd.Timestamp.now(tz="UTC") # Isolate future dates, don't really care about finding look alike for past dates
    query_mask = ~rated_mask & future_mask
    df_query = df_scaled[query_mask]


    nbrs = NearestNeighbors(n_neighbors=1).fit(df_rated)
    distances, indices = nbrs.kneighbors(df_query)
    matched = df_rated_reference.iloc[indices[:, 0]].reset_index(drop=True)
    matched = matched[["forecast_time", "time_block", "rating", "comment"]].add_prefix("closest_match_")
    matched["closest_match_distance"] = distances[:, 0]
    matched.index = df_query.index
    df_result = df_ref.join(matched)

    return df_result


def main():
    '''
    Main orchestrator function
    '''
    try:
        ENGINE = get_engine()
        base_df = get_data(engine=ENGINE, query=QUERY)
        df_preprocessed = preprocess_data(base_df, feature_cols=FEATURE_COLS)
        df_knn = fit_nearest_neighbors(df_ref=base_df, df_scaled=df_preprocessed, reference_cols=REFERENCE_COLS)
        write_dataframe(df=df_knn, table_name=NEIGHBORS_TABLE_NAME, schema=SCHEMA, engine=ENGINE, if_exists='replace')

        return df_knn
    except Exception as e:
        logging.error(f"Nearest Neighbors run failed with following error: {e}")
        raise




if __name__ == "__main__":
    main()




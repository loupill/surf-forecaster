-- ============================================================
-- SCHEMAS
-- ============================================================

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS gold;

-- ============================================================
-- RAW MARINE
-- ============================================================

CREATE TABLE IF NOT EXISTS raw.marine_forecasts (
    id                      SERIAL PRIMARY KEY,
    break_id                TEXT            NOT NULL,
    retrieved_at            TIMESTAMPTZ     NOT NULL,
    forecast_time           TIMESTAMPTZ     NOT NULL,
    wave_height_m           NUMERIC(5, 2),
    swell_wave_height_m     NUMERIC(5, 2),
    swell_wave_period_s     NUMERIC(5, 2),
    swell_wave_direction_deg NUMERIC(5, 2),
    wind_wave_height_m      NUMERIC(5, 2),
    wave_period_s           NUMERIC(5, 2),
    wave_direction_deg      NUMERIC(5, 2),

    UNIQUE (break_id, forecast_time, retrieved_at)
);

-- ============================================================
-- RAW WEATHER
-- ============================================================

CREATE TABLE IF NOT EXISTS raw.weather_forecasts (
    id                      SERIAL PRIMARY KEY,
    break_id                TEXT            NOT NULL,
    retrieved_at            TIMESTAMPTZ     NOT NULL,
    forecast_time           TIMESTAMPTZ     NOT NULL,
    temperature_c           NUMERIC(5, 2),
    wind_speed_kmh          NUMERIC(5, 2),
    wind_direction_deg      NUMERIC(5, 2),
    wind_gusts_kmh          NUMERIC(5, 2),

    UNIQUE (break_id, forecast_time, retrieved_at)
);
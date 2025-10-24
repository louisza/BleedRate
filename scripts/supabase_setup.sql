-- BleedRate Supabase Database Setup
-- Run this SQL in your Supabase SQL Editor to create the submissions table

-- Drop existing table if you want to start fresh (WARNING: deletes all data!)
-- Uncomment the line below if you want to recreate the table from scratch
-- DROP TABLE IF EXISTS submissions CASCADE;

-- Create submissions table with all metadata columns
CREATE TABLE IF NOT EXISTS submissions (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    
    -- Key metrics (for quick queries)
    annual_salary INTEGER,
    total_to_govt NUMERIC(12,2),
    effective_rate NUMERIC(5,2),
    
    -- Full data as JSON
    form_data JSONB NOT NULL,
    results JSONB NOT NULL,
    
    -- Geographic data
    ip_hash VARCHAR(64),
    country_code VARCHAR(2),
    country_name VARCHAR(100),
    region VARCHAR(100),
    city VARCHAR(100),
    timezone VARCHAR(50),
    latitude NUMERIC(10,7),
    longitude NUMERIC(10,7),
    
    -- Browser & Device data
    user_agent TEXT,
    browser VARCHAR(50),
    browser_version VARCHAR(20),
    os VARCHAR(50),
    os_version VARCHAR(20),
    device_type VARCHAR(20), -- 'mobile', 'tablet', 'desktop'
    device_brand VARCHAR(50),
    device_model VARCHAR(100),
    
    -- Screen & Display
    screen_width INTEGER,
    screen_height INTEGER,
    screen_color_depth INTEGER,
    pixel_ratio NUMERIC(3,2),
    viewport_width INTEGER,
    viewport_height INTEGER,
    
    -- Traffic Source
    referrer TEXT,
    referrer_domain VARCHAR(255),
    utm_source VARCHAR(100),
    utm_medium VARCHAR(100),
    utm_campaign VARCHAR(100),
    utm_term VARCHAR(100),
    utm_content VARCHAR(100),
    
    -- Session & Behavior
    session_id UUID,
    language VARCHAR(20),
    languages TEXT, -- Full accept-language header
    time_to_complete_seconds INTEGER,
    page_load_time_ms INTEGER,
    
    -- Browser Capabilities
    cookies_enabled BOOLEAN,
    do_not_track BOOLEAN,
    online BOOLEAN,
    touch_support BOOLEAN,
    webgl_support BOOLEAN,
    local_storage_support BOOLEAN,
    
    -- Audit fields
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add new columns if table already exists (safe to run multiple times)
DO $$ 
BEGIN
    -- Geographic data
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='country_code') THEN
        ALTER TABLE submissions ADD COLUMN country_code VARCHAR(2);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='country_name') THEN
        ALTER TABLE submissions ADD COLUMN country_name VARCHAR(100);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='region') THEN
        ALTER TABLE submissions ADD COLUMN region VARCHAR(100);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='city') THEN
        ALTER TABLE submissions ADD COLUMN city VARCHAR(100);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='timezone') THEN
        ALTER TABLE submissions ADD COLUMN timezone VARCHAR(50);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='latitude') THEN
        ALTER TABLE submissions ADD COLUMN latitude NUMERIC(10,7);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='longitude') THEN
        ALTER TABLE submissions ADD COLUMN longitude NUMERIC(10,7);
    END IF;
    
    -- Browser & Device
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='browser') THEN
        ALTER TABLE submissions ADD COLUMN browser VARCHAR(50);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='browser_version') THEN
        ALTER TABLE submissions ADD COLUMN browser_version VARCHAR(20);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='os') THEN
        ALTER TABLE submissions ADD COLUMN os VARCHAR(50);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='os_version') THEN
        ALTER TABLE submissions ADD COLUMN os_version VARCHAR(20);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='device_type') THEN
        ALTER TABLE submissions ADD COLUMN device_type VARCHAR(20);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='device_brand') THEN
        ALTER TABLE submissions ADD COLUMN device_brand VARCHAR(50);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='device_model') THEN
        ALTER TABLE submissions ADD COLUMN device_model VARCHAR(100);
    END IF;
    
    -- Screen & Display
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='screen_width') THEN
        ALTER TABLE submissions ADD COLUMN screen_width INTEGER;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='screen_height') THEN
        ALTER TABLE submissions ADD COLUMN screen_height INTEGER;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='screen_color_depth') THEN
        ALTER TABLE submissions ADD COLUMN screen_color_depth INTEGER;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='pixel_ratio') THEN
        ALTER TABLE submissions ADD COLUMN pixel_ratio NUMERIC(3,2);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='viewport_width') THEN
        ALTER TABLE submissions ADD COLUMN viewport_width INTEGER;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='viewport_height') THEN
        ALTER TABLE submissions ADD COLUMN viewport_height INTEGER;
    END IF;
    
    -- Traffic Source
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='referrer') THEN
        ALTER TABLE submissions ADD COLUMN referrer TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='referrer_domain') THEN
        ALTER TABLE submissions ADD COLUMN referrer_domain VARCHAR(255);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='utm_source') THEN
        ALTER TABLE submissions ADD COLUMN utm_source VARCHAR(100);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='utm_medium') THEN
        ALTER TABLE submissions ADD COLUMN utm_medium VARCHAR(100);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='utm_campaign') THEN
        ALTER TABLE submissions ADD COLUMN utm_campaign VARCHAR(100);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='utm_term') THEN
        ALTER TABLE submissions ADD COLUMN utm_term VARCHAR(100);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='utm_content') THEN
        ALTER TABLE submissions ADD COLUMN utm_content VARCHAR(100);
    END IF;
    
    -- Session & Behavior
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='session_id') THEN
        ALTER TABLE submissions ADD COLUMN session_id UUID;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='language') THEN
        ALTER TABLE submissions ADD COLUMN language VARCHAR(20);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='languages') THEN
        ALTER TABLE submissions ADD COLUMN languages TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='time_to_complete_seconds') THEN
        ALTER TABLE submissions ADD COLUMN time_to_complete_seconds INTEGER;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='page_load_time_ms') THEN
        ALTER TABLE submissions ADD COLUMN page_load_time_ms INTEGER;
    END IF;
    
    -- Browser Capabilities
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='cookies_enabled') THEN
        ALTER TABLE submissions ADD COLUMN cookies_enabled BOOLEAN;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='do_not_track') THEN
        ALTER TABLE submissions ADD COLUMN do_not_track BOOLEAN;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='online') THEN
        ALTER TABLE submissions ADD COLUMN online BOOLEAN;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='touch_support') THEN
        ALTER TABLE submissions ADD COLUMN touch_support BOOLEAN;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='webgl_support') THEN
        ALTER TABLE submissions ADD COLUMN webgl_support BOOLEAN;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='submissions' AND column_name='local_storage_support') THEN
        ALTER TABLE submissions ADD COLUMN local_storage_support BOOLEAN;
    END IF;
END $$;

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_submissions_timestamp ON submissions(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_submissions_salary ON submissions(annual_salary);
CREATE INDEX IF NOT EXISTS idx_submissions_effective_rate ON submissions(effective_rate);
CREATE INDEX IF NOT EXISTS idx_submissions_total ON submissions(total_to_govt);
CREATE INDEX IF NOT EXISTS idx_submissions_created_at ON submissions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_submissions_country ON submissions(country_code);
CREATE INDEX IF NOT EXISTS idx_submissions_device_type ON submissions(device_type);
CREATE INDEX IF NOT EXISTS idx_submissions_referrer_domain ON submissions(referrer_domain);
CREATE INDEX IF NOT EXISTS idx_submissions_utm_source ON submissions(utm_source);

-- Create a function to get average effective rate (for statistics)
CREATE OR REPLACE FUNCTION get_avg_effective_rate()
RETURNS TABLE(avg_rate NUMERIC) AS $$
BEGIN
    RETURN QUERY
    SELECT ROUND(AVG(effective_rate), 2) as avg_rate
    FROM submissions
    WHERE effective_rate IS NOT NULL
      AND effective_rate > 0
      AND effective_rate < 100;
END;
$$ LANGUAGE plpgsql;

-- Create a view for basic statistics (optional, for dashboard)
CREATE OR REPLACE VIEW submission_stats AS
SELECT
    COUNT(*) as total_submissions,
    ROUND(AVG(effective_rate), 2) as avg_effective_rate,
    ROUND(AVG(total_to_govt), 2) as avg_total_to_govt,
    ROUND(AVG(annual_salary), 0) as avg_salary,
    MIN(timestamp) as first_submission,
    MAX(timestamp) as latest_submission
FROM submissions
WHERE effective_rate IS NOT NULL
  AND annual_salary IS NOT NULL;

-- Create salary band analysis view (optional, for insights)
CREATE OR REPLACE VIEW salary_band_stats AS
SELECT
    salary_band,
    COUNT(*) as submissions,
    ROUND(AVG(effective_rate), 2) as avg_effective_rate,
    ROUND(AVG(total_to_govt), 2) as avg_total_to_govt
FROM (
    SELECT
        CASE 
            WHEN annual_salary < 300000 THEN '< R300k'
            WHEN annual_salary < 600000 THEN 'R300k - R600k'
            WHEN annual_salary < 1000000 THEN 'R600k - R1M'
            WHEN annual_salary < 2000000 THEN 'R1M - R2M'
            ELSE '> R2M'
        END as salary_band,
        CASE 
            WHEN annual_salary < 300000 THEN 1
            WHEN annual_salary < 600000 THEN 2
            WHEN annual_salary < 1000000 THEN 3
            WHEN annual_salary < 2000000 THEN 4
            ELSE 5
        END as salary_band_order,
        effective_rate,
        total_to_govt
    FROM submissions
    WHERE annual_salary IS NOT NULL
) subquery
GROUP BY salary_band, salary_band_order
ORDER BY salary_band_order;

-- Comments for documentation
COMMENT ON TABLE submissions IS 'Stores all calculator form submissions with full input/output data';
COMMENT ON COLUMN submissions.annual_salary IS 'User annual salary in Rand (extracted for quick queries)';
COMMENT ON COLUMN submissions.total_to_govt IS 'Total annual amount flowing to government';
COMMENT ON COLUMN submissions.effective_rate IS 'Effective tax rate as percentage of gross income';
COMMENT ON COLUMN submissions.form_data IS 'Full form input data as JSON';
COMMENT ON COLUMN submissions.results IS 'Calculation results including breakdown';
COMMENT ON COLUMN submissions.ip_hash IS 'SHA-256 hash of IP address (for abuse prevention, not tracking)';

-- Disable Row Level Security for public submissions
-- Since this table only stores aggregated calculator data (no personal info),
-- we allow public inserts without authentication
ALTER TABLE submissions DISABLE ROW LEVEL SECURITY;

-- Grant permissions to anon role (used by anon/public key)
GRANT USAGE ON SCHEMA public TO anon;
GRANT INSERT ON submissions TO anon;
GRANT USAGE ON SEQUENCE submissions_id_seq TO anon;

-- Grant permissions to authenticated users (for future admin dashboard)
GRANT SELECT ON submissions TO authenticated;
GRANT SELECT ON submission_stats TO authenticated;
GRANT SELECT ON salary_band_stats TO authenticated;

-- Done! Your Supabase database is ready to log BleedRate submissions

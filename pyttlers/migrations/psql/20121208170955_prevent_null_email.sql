BEGIN;
    INSERT INTO migrations (version) SELECT '20121208170955';
    ALTER TABLE users ALTER COLUMN email_address SET NOT NULL;
COMMIT;

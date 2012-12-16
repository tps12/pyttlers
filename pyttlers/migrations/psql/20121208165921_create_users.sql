BEGIN;
    INSERT INTO migrations (version) SELECT '20121208165921';
    CREATE TABLE users (
        guid VARCHAR(36) PRIMARY KEY,
        email_address VARCHAR(64) UNIQUE,
        created_at TIMESTAMP,
        updated_at TIMESTAMP);
COMMIT;

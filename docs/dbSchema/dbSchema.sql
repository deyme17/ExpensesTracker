-- USERS
CREATE TABLE "users" (
    "user_id" VARCHAR(255) NOT NULL DEFAULT gen_random_uuid(),
    "name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "hashed_password" VARCHAR(255) NOT NULL,
    "encrypted_token" VARCHAR(255) NOT NULL,
    PRIMARY KEY ("user_id"),
    CONSTRAINT "users_email_unique" UNIQUE ("email")
);

-- CATEGORIES
CREATE TABLE "categories" (
    "mcc_code" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    PRIMARY KEY ("mcc_code")
);

-- CURRENCIES
CREATE TABLE "currencies" (
    "currency_code" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    PRIMARY KEY ("currency_code")
);

-- ACCOUNTS
CREATE TABLE "accounts" (
    "account_id" VARCHAR(255) NOT NULL,
    "user_id" VARCHAR(255) NOT NULL,
    "balance" DECIMAL(19, 4) NOT NULL,
    "currency_code" BIGINT NOT NULL,
    "type" VARCHAR(255) NOT NULL,
    "masked_pan" VARCHAR NOT NULL,
    PRIMARY KEY ("account_id"),
    FOREIGN KEY ("user_id") 
        REFERENCES "users"("user_id") ON DELETE CASCADE,
    FOREIGN KEY ("currency_code") 
        REFERENCES "currencies"("currency_code"),
);


CREATE TYPE payment_method_type AS ENUM ('card', 'cash');

-- TRANSACTIONS
CREATE TABLE "transactions" (
    "transaction_id" VARCHAR(255) NOT NULL,
    "user_id" VARCHAR(255) NOT NULL,
    "amount" DECIMAL(19, 4) NOT NULL,
    "date" DATE NOT NULL DEFAULT CURRENT_DATE,
    "account_id" VARCHAR(255) NOT NULL,
    "mcc_code" BIGINT NOT NULL,
    "currency_code" BIGINT NOT NULL DEFAULT 980,
    "payment_method" payment_method_type NOT NULL DEFAULT 'card',
    "type" VARCHAR(10) GENERATED ALWAYS AS (
        CASE
            WHEN amount > 0 THEN 'income'
            WHEN amount < 0 THEN 'expense'
            ELSE 'zero'
        END
    ) STORED,
    "description" VARCHAR(255) NOT NULL DEFAULT 'without_description',
    "cashback" DECIMAL(19, 4) NOT NULL,
    "commission" DECIMAL(19, 4) NOT NULL,
    PRIMARY KEY ("transaction_id"),
    FOREIGN KEY ("user_id") 
        REFERENCES "users"("user_id") ON DELETE CASCADE,
    FOREIGN KEY ("account_id") 
        REFERENCES "accounts"("account_id"),
    FOREIGN KEY ("mcc_code") 
        REFERENCES "categories"("mcc_code"),
    FOREIGN KEY ("currency_code") 
        REFERENCES "currencies"("currency_code"),
    CONSTRAINT "nonzero_amount" CHECK (amount != 0),
    CONSTRAINT "positive_cashback" CHECK (cashback >= 0),
    CONSTRAINT "positive_commission" CHECK (commission >= 0)
);

-- INDECIES
CREATE INDEX idx_transactions_user_id ON "transactions" ("user_id");
CREATE INDEX idx_transactions_date ON "transactions" ("date");
CREATE INDEX idx_transactions_mcc_code ON "transactions" ("mcc_code");
CREATE INDEX idx_accounts_user_id ON "accounts" ("user_id");

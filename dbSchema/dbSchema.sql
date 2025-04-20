CREATE TABLE "users" (
    "user_id" VARCHAR PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "balance" DECIMAL(19,4) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "token" VARCHAR(255)
);

CREATE TABLE "category" (
    "mcc_code" BIGINT PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL
);

CREATE TABLE "transactions" (
    "transaction_id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "user_id" VARCHAR NOT NULL,
    "amount" DECIMAL(19,4) NOT NULL,
    "date" DATE NOT NULL DEFAULT CURRENT_DATE,
    "currency_code" BIGINT NOT NULL DEFAULT 980,
    "mcc_code" BIGINT NOT NULL DEFAULT 0000,
    "type" VARCHAR(255) NOT NULL DEFAULT 'card',
    "description" VARCHAR(255) NOT NULL DEFAULT 'Without_description',
    "cashback" DECIMAL(19,4) NOT NULL DEFAULT 0,
    "commission" DECIMAL(19,4) NOT NULL DEFAULT 0,
    FOREIGN KEY("user_id") REFERENCES "users"("user_id"),
    FOREIGN KEY("mcc_code") REFERENCES "category"("mcc_code")
);

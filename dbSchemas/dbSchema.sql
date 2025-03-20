CREATE TABLE "users"(
    "user_id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "email" BIGINT NOT NULL,
    "password" BIGINT NOT NULL,
    "token" VARCHAR(255) NOT NULL,
    "webhookURL" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "users" ADD PRIMARY KEY("user_id");
CREATE TABLE "transaction"(
    "transaction_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "amount" FLOAT(53) NOT NULL,
    "date" DATE NOT NULL,
    "currency_id" BIGINT NOT NULL,
    "category_id" BIGINT NOT NULL,
    "type" VARCHAR(255) NOT NULL,
    "cashback" FLOAT(53) NOT NULL,
    "commission" FLOAT(53) NOT NULL
);
ALTER TABLE
    "transaction" ADD PRIMARY KEY("transaction_id");
CREATE TABLE "category"(
    "category_id" BIGINT NOT NULL,
    "cat_name" VARCHAR(255) NOT NULL,
    "priority" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL
);
ALTER TABLE
    "category" ADD PRIMARY KEY("category_id");
CREATE TABLE "budget"(
    "budget_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "balance" FLOAT(53) NOT NULL,
    "amount" BIGINT NOT NULL,
    "limit" FLOAT(53) NOT NULL
);
ALTER TABLE
    "budget" ADD PRIMARY KEY("budget_id");
CREATE TABLE "currency"(
    "currency_id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "in_hryvnia" FLOAT(53) NOT NULL,
    "in_dollars" FLOAT(53) NOT NULL
);
ALTER TABLE
    "currency" ADD PRIMARY KEY("currency_id");
CREATE TABLE "recurring_transactions"(
    "recurring_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "amount" FLOAT(53) NOT NULL,
    "category_id" BIGINT NOT NULL,
    "currency_id" BIGINT NOT NULL,
    "interval" VARCHAR(255) NOT NULL,
    "next_payment_date" DATE NOT NULL
);
ALTER TABLE
    "recurring_transactions" ADD PRIMARY KEY("recurring_id");
CREATE TABLE "settings"(
    "setting_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "notifications" BOOLEAN NOT NULL,
    "default_currency" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "settings" ADD PRIMARY KEY("setting_id");
ALTER TABLE
    "transaction" ADD CONSTRAINT "transaction_category_id_foreign" FOREIGN KEY("category_id") REFERENCES "category"("category_id");
ALTER TABLE
    "recurring_transactions" ADD CONSTRAINT "recurring_transactions_currency_id_foreign" FOREIGN KEY("currency_id") REFERENCES "currency"("currency_id");
ALTER TABLE
    "transaction" ADD CONSTRAINT "transaction_currency_id_foreign" FOREIGN KEY("currency_id") REFERENCES "currency"("currency_id");
ALTER TABLE
    "settings" ADD CONSTRAINT "settings_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("user_id");
ALTER TABLE
    "transaction" ADD CONSTRAINT "transaction_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("user_id");
ALTER TABLE
    "recurring_transactions" ADD CONSTRAINT "recurring_transactions_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("user_id");
ALTER TABLE
    "category" ADD CONSTRAINT "category_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("user_id");
ALTER TABLE
    "recurring_transactions" ADD CONSTRAINT "recurring_transactions_category_id_foreign" FOREIGN KEY("category_id") REFERENCES "transaction"("category_id");
ALTER TABLE
    "budget" ADD CONSTRAINT "budget_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("user_id");
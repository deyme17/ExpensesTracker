CREATE TABLE "users"(
    "user_id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "token" VARCHAR(255) NOT NULL,
    "webhookURL" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "users" ADD PRIMARY KEY("user_id");
ALTER TABLE
    "users" ADD CONSTRAINT "users_email_unique" UNIQUE("email");
CREATE TABLE "transaction"(
    "transaction_id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "amount" FLOAT(53) NOT NULL,
    "date" DATE NOT NULL,
    "currency_id" BIGINT NOT NULL,
    "category_id" BIGINT NOT NULL,
    "type" VARCHAR(255) NOT NULL,
    "description" VARCHAR(255) NOT NULL,
    "cashback" FLOAT(53) NOT NULL,
    "commission" FLOAT(53) NOT NULL
);
ALTER TABLE
    "transaction" ADD PRIMARY KEY("transaction_id");
CREATE TABLE "category"(
    "category_id" BIGINT NOT NULL,
    "cat_name" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "category" ADD PRIMARY KEY("category_id");
CREATE TABLE "currency"(
    "currency_id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "exchange_rate" FLOAT(53) NOT NULL
);
ALTER TABLE
    "currency" ADD PRIMARY KEY("currency_id");
ALTER TABLE
    "transaction" ADD CONSTRAINT "transaction_category_id_foreign" FOREIGN KEY("category_id") REFERENCES "category"("category_id");
ALTER TABLE
    "transaction" ADD CONSTRAINT "transaction_currency_id_foreign" FOREIGN KEY("currency_id") REFERENCES "currency"("currency_id");
ALTER TABLE
    "transaction" ADD CONSTRAINT "transaction_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("user_id");
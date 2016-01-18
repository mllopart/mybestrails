--python manage.py sqlmigrate track_management 0001
BEGIN;
--
-- Create model mdlTrack
--
CREATE TABLE "track" ("id" serial NOT NULL PRIMARY KEY, "name" varchar(4000) NOT NULL, "cmt" text NULL, "desc" text NULL, "src" varchar(100) NULL, "link" varchar(200) NULL, "number" integer NOT NULL, "type" varchar(100) NULL, "hash_code" varchar(32) NULL, "deleted" boolean NOT NULL, "created_timestamp" timestamp with time zone NOT NULL, "updated_timestamp" timestamp with time zone NOT NULL, "creation_user_id" integer NOT NULL);
ALTER TABLE "track" ADD CONSTRAINT "track_creation_user_id_c477a1fd_fk_auth_user_id" FOREIGN KEY ("creation_user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "track_e8ceeea3" ON "track" ("hash_code");
CREATE INDEX "track_93947d62" ON "track" ("creation_user_id");
CREATE INDEX "track_hash_code_7999674e_like" ON "track" ("hash_code" varchar_pattern_ops);

COMMIT;

--python manage.py sqlmigrate user_management 0001
BEGIN;
--
-- Create model CustomUser
--
CREATE TABLE "auth_user_extended" ("user_ptr_id" integer NOT NULL PRIMARY KEY, "timezone" varchar(50) NOT NULL, "gender" varchar(1) NULL, "birthdate" date NULL, "locale" varchar(10) NULL, "hash_code" varchar(32) NULL, "deleted" boolean NOT NULL, "activated" boolean NOT NULL);
ALTER TABLE "auth_user_extended" ADD CONSTRAINT "auth_user_extended_user_ptr_id_328523a9_fk_auth_user_id" FOREIGN KEY ("user_ptr_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "auth_user_extended_e8ceeea3" ON "auth_user_extended" ("hash_code");
CREATE INDEX "auth_user_extended_da602f0b" ON "auth_user_extended" ("deleted");
CREATE INDEX "auth_user_extended_c3905c37" ON "auth_user_extended" ("activated");
CREATE INDEX "auth_user_extended_hash_code_267105f9_like" ON "auth_user_extended" ("hash_code" varchar_pattern_ops);

COMMIT;

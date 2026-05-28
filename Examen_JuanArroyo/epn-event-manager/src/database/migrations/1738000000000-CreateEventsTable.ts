import { MigrationInterface, QueryRunner } from 'typeorm';

export class CreateEventsTable1738000000000 implements MigrationInterface {
  name = 'CreateEventsTable1738000000000';

  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`
      CREATE TABLE IF NOT EXISTS "events" (
        "id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
        "action" varchar NOT NULL,
        "source" varchar,
        "entity" varchar,
        "title" varchar,
        "description" varchar,
        "payload" text,
        "query_term" varchar,
        "created_at" datetime NOT NULL DEFAULT (datetime('now'))
      )
    `);

    await queryRunner.query(`DROP TABLE IF EXISTS "create_events"`);
    await queryRunner.query(`DROP TABLE IF EXISTS "update_events"`);
    await queryRunner.query(`DROP TABLE IF EXISTS "delete_events"`);
    await queryRunner.query(`DROP TABLE IF EXISTS "query_events"`);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`DROP TABLE IF EXISTS "events"`);
  }
}

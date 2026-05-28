import { DataSource } from 'typeorm';
import { config } from 'dotenv';
import { join } from 'path';
import { EventEntity } from './entities/event.entity';

config();

export default new DataSource({
  type: 'better-sqlite3',
  database: process.env.DB_DATABASE ?? 'db/events.sqlite',
  entities: [EventEntity],
  migrations: [join(__dirname, 'migrations', '*.{ts,js}')],
  synchronize: false,
});

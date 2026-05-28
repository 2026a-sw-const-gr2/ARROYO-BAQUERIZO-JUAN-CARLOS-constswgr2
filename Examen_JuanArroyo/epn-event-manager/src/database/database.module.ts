import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { join } from 'path';
import { EventEntity } from './entities/event.entity';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        type: 'better-sqlite3' as const,
        database: config.get<string>('DB_DATABASE', 'db/events.sqlite'),
        entities: [EventEntity],
        synchronize: config.get<string>('DB_SYNCHRONIZE', 'false') === 'true',
        migrations: [join(__dirname, 'migrations', '*.{ts,js}')],
        migrationsRun: config.get<string>('DB_RUN_MIGRATIONS', 'true') === 'true',
      }),
    }),
  ],
  exports: [TypeOrmModule],
})
export class DatabaseModule {}

import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { EventEntity } from '../../database/entities/event.entity';

export interface EventStats {
  create: number;
  update: number;
  delete: number;
  query: number;
  total: number;
}

@Injectable()
export class StatsService {
  constructor(
    @InjectRepository(EventEntity)
    private readonly eventRepo: Repository<EventEntity>,
  ) {}

  async getStats(): Promise<EventStats> {
    const create = await this.eventRepo.count({ where: { action: 'CREATE' } });
    const update = await this.eventRepo.count({ where: { action: 'UPDATE' } });
    const deleteCount = await this.eventRepo.count({
      where: { action: 'DELETE' },
    });
    const query = await this.eventRepo.count({ where: { action: 'QUERY' } });

    return {
      create,
      update,
      delete: deleteCount,
      query,
      total: create + update + deleteCount + query,
    };
  }
}

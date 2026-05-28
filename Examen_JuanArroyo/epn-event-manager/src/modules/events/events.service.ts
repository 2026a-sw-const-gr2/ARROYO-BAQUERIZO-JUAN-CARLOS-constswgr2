import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { EventEntity } from '../../database/entities/event.entity';
import { CreateEventDto } from './dto/create-event.dto';

@Injectable()
export class EventsService {
  constructor(
    @InjectRepository(EventEntity)
    private readonly eventRepo: Repository<EventEntity>,
  ) {}

  async registerEvent(dto: CreateEventDto): Promise<{ ok: boolean }> {
    const action = dto.action.toUpperCase();
    const event = this.eventRepo.create({
      source: dto.source,
      entity: dto.entity,
      action,
      title: dto.title,
      description: dto.description,
      payload: JSON.stringify(dto.payload ?? {}),
    });
    await this.eventRepo.save(event);
    return { ok: true };
  }

  async findAll(): Promise<EventEntity[]> {
    return this.eventRepo.find({
      order: { created_at: 'DESC' },
    });
  }

  async findOne(id: number): Promise<EventEntity> {
    const event = await this.eventRepo.findOne({ where: { id } });
    if (!event) {
      throw new NotFoundException(`Event with id ${id} not found`);
    }
    return event;
  }

  async findBySource(source: string): Promise<EventEntity[]> {
    return this.eventRepo.find({
      where: { source },
      order: { created_at: 'DESC' },
    });
  }

  async findByEntity(entity: string): Promise<EventEntity[]> {
    return this.eventRepo.find({
      where: { entity },
      order: { created_at: 'DESC' },
    });
  }
}

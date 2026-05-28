import {
  IsIn,
  IsNotEmpty,
  IsObject,
  IsOptional,
  IsString,
} from 'class-validator';

const EVENT_ACTIONS = ['CREATE', 'UPDATE', 'DELETE', 'QUERY'] as const;

export class CreateEventDto {
  @IsString()
  @IsNotEmpty()
  source: string;

  @IsString()
  @IsNotEmpty()
  entity: string;

  @IsString()
  @IsIn(EVENT_ACTIONS)
  action: string;

  @IsString()
  @IsNotEmpty()
  title: string;

  @IsOptional()
  @IsString()
  description?: string;

  @IsOptional()
  @IsObject()
  payload?: Record<string, unknown>;
}

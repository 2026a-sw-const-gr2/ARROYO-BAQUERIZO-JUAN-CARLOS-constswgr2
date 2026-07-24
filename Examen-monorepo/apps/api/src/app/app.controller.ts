import { Controller, Post, Body, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBody, ApiSecurity } from '@nestjs/swagger';
import { AppService } from './app.service';
import { ApiKeyGuard } from './api-key.guard';
import { ElectricityRequest } from '@org/shared';

@ApiTags('Electricity')
@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Post('v1/electricity')
  @ApiOperation({ summary: 'Cálculo de consumo eléctrico (API v1 - Crudo)' })
  @ApiBody({
    schema: {
      type: 'object',
      properties: {
        appliances: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              name: { type: 'string' },
              watts: { type: 'number' },
              hoursPerDay: { type: 'number' }
            }
          }
        },
        tiers: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              limitKwh: { type: 'number' },
              price: { type: 'number' }
            }
          }
        }
      }
    }
  })
  calculateV1(@Body() req: ElectricityRequest) {
    return this.appService.calculateRaw(req);
  }

  @Post('v2/electricity')
  @UseGuards(ApiKeyGuard)
  @ApiSecurity('x-api-key')
  @ApiOperation({ summary: 'Cálculo de consumo eléctrico (API v2 - Formateado)' })
  @ApiBody({
    schema: {
      type: 'object',
      properties: {
        appliances: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              name: { type: 'string' },
              watts: { type: 'number' },
              hoursPerDay: { type: 'number' }
            }
          }
        },
        tiers: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              limitKwh: { type: 'number' },
              price: { type: 'number' }
            }
          }
        }
      }
    }
  })
  calculateV2(@Body() req: ElectricityRequest) {
    return this.appService.calculateFormatted(req);
  }
}

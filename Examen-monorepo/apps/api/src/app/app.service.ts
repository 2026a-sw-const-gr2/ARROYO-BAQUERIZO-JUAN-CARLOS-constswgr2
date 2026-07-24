import { Injectable, BadRequestException } from '@nestjs/common';
import { 
  ElectricityRequest, 
  ElectricityResult, 
  validateElectricityRequest,
  formatElectricityResult 
} from '@org/shared';

@Injectable()
export class AppService {
  calculateRaw(data: ElectricityRequest): ElectricityResult {
    const errors = validateElectricityRequest(data);
    if (errors.length > 0) {
      throw new BadRequestException({ message: 'Error de validación', errors });
    }

    // calculate total kWh per month
    let totalKwh = 0;
    for (const app of data.appliances) {
      totalKwh += (app.watts / 1000) * app.hoursPerDay * 30;
    }

    const sortedTiers = [...data.tiers].sort((a, b) => a.limitKwh - b.limitKwh);
    
    let remainingKwh = totalKwh;
    let totalCost = 0;
    let previousLimit = 0;

    for (const tier of sortedTiers) {
      const tierSize = tier.limitKwh - previousLimit;
      if (remainingKwh <= 0) break;

      const kwhInThisTier = Math.min(remainingKwh, tierSize);
      totalCost += kwhInThisTier * tier.price;
      
      remainingKwh -= kwhInThisTier;
      previousLimit = tier.limitKwh;
    }
    
    if (remainingKwh > 0 && sortedTiers.length > 0) {
      const lastTier = sortedTiers[sortedTiers.length - 1];
      totalCost += remainingKwh * lastTier.price;
    }

    return { totalKwh, totalCost };
  }

  calculateFormatted(data: ElectricityRequest) {
    const raw = this.calculateRaw(data);
    return formatElectricityResult(raw);
  }
}

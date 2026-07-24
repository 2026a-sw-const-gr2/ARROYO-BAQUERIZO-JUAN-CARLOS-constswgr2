export interface Appliance {
  name: string;
  watts: number;
  hoursPerDay: number;
}

export interface Tier {
  limitKwh: number;
  price: number;
}

export interface ElectricityRequest {
  appliances: Appliance[];
  tiers: Tier[];
}

export interface ElectricityResult {
  totalKwh: number;
  totalCost: number;
}

export function validateElectricityRequest(req: Partial<ElectricityRequest>): string[] {
  const errors: string[] = [];
  if (!req.appliances || req.appliances.length === 0) {
    errors.push('Debe enviar al menos un electrodoméstico.');
  } else {
    req.appliances.forEach((app, i) => {
      if (!app.name) errors.push(`Electrodoméstico ${i+1}: El nombre es requerido.`);
      if (typeof app.watts !== 'number' || app.watts <= 0) errors.push(`Electrodoméstico ${i+1}: Los vatios deben ser mayores a cero.`);
      if (typeof app.hoursPerDay !== 'number' || app.hoursPerDay <= 0 || app.hoursPerDay > 24) errors.push(`Electrodoméstico ${i+1}: Las horas de uso diarias deben estar entre 0 y 24.`);
    });
  }

  if (!req.tiers || req.tiers.length === 0) {
    errors.push('Debe especificar al menos una tarifa escalonada.');
  } else {
    req.tiers.forEach((tier, i) => {
      if (typeof tier.limitKwh !== 'number' || tier.limitKwh <= 0) errors.push(`Escalón ${i+1}: El límite (kWh) debe ser mayor a cero.`);
      if (typeof tier.price !== 'number' || tier.price < 0) errors.push(`Escalón ${i+1}: El precio no puede ser negativo.`);
    });
  }
  return errors;
}

export function formatElectricityResult(result: ElectricityResult) {
  return {
    formattedKwh: `${result.totalKwh.toFixed(2)} kWh/mes`,
    formattedCost: `$${result.totalCost.toFixed(2)}`,
    ...result
  };
}

import { useState } from 'react';
import { Appliance, Tier, ElectricityRequest, validateElectricityRequest, formatElectricityResult } from '@org/shared';

export function App() {
  const [appliances, setAppliances] = useState<Appliance[]>([
    { name: 'Refrigerador', watts: 150, hoursPerDay: 24 }
  ]);
  const [tiers, setTiers] = useState<Tier[]>([
    { limitKwh: 100, price: 0.10 },
    { limitKwh: 999999, price: 0.15 }
  ]);
  const [apiKey, setApiKey] = useState('secret-key-123');
  const [result, setResult] = useState<{ kwh: string, cost: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAddAppliance = () => {
    setAppliances([...appliances, { name: '', watts: 0, hoursPerDay: 0 }]);
  };

  const handleApplianceChange = (index: number, field: keyof Appliance, value: string | number) => {
    const newAppliances = [...appliances];
    newAppliances[index] = { ...newAppliances[index], [field]: value } as Appliance;
    setAppliances(newAppliances);
  };

  const handleRemoveAppliance = (index: number) => {
    setAppliances(appliances.filter((_, i) => i !== index));
  };

  const callApi = async (version: 'v1' | 'v2') => {
    setError(null);
    setResult(null);

    const req: ElectricityRequest = { appliances, tiers };
    const validationErrors = validateElectricityRequest(req);
    
    if (validationErrors.length > 0) {
      setError(validationErrors.join('\n'));
      return;
    }

    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json'
      };
      
      if (version === 'v2') {
        headers['x-api-key'] = apiKey;
      }

      const response = await fetch(`http://localhost:3000/api/${version}/electricity`, {
        method: 'POST',
        headers,
        body: JSON.stringify(req)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      
      if (version === 'v1') {
        const formatted = formatElectricityResult(data);
        setResult({ kwh: formatted.formattedKwh, cost: formatted.formattedCost });
      } else {
        setResult({ kwh: data.formattedKwh, cost: data.formattedCost });
      }

    } catch (err: any) {
      setError(err.message || 'Error de conexión');
    }
  };

  return (
    <div className="container">
      <h1>Cálculo de Consumo Eléctrico</h1>
      <p className="subtitle">Estima el costo de tu factura de luz</p>

      <h2>Electrodomésticos</h2>
      {appliances.map((app, index) => (
        <div key={index} className="form-group">
          <input 
            type="text" 
            className="input-field" 
            placeholder="Nombre (ej. TV)" 
            value={app.name} 
            onChange={(e) => handleApplianceChange(index, 'name', e.target.value)} 
          />
          <input 
            type="number" 
            className="input-field" 
            placeholder="Vatios (W)" 
            value={app.watts || ''} 
            onChange={(e) => handleApplianceChange(index, 'watts', Number(e.target.value))} 
          />
          <input 
            type="number" 
            className="input-field" 
            placeholder="Horas al día" 
            value={app.hoursPerDay || ''} 
            onChange={(e) => handleApplianceChange(index, 'hoursPerDay', Number(e.target.value))} 
          />
          <button className="btn btn-danger" onClick={() => handleRemoveAppliance(index)}>X</button>
        </div>
      ))}
      <button className="btn btn-secondary" onClick={handleAddAppliance}>+ Agregar Electrodoméstico</button>

      <h2>Opciones de API v2</h2>
      <input 
        type="text" 
        className="input-field api-key-input" 
        placeholder="API Key (para v2)" 
        value={apiKey} 
        onChange={(e) => setApiKey(e.target.value)} 
      />

      <div className="actions">
        <button className="btn btn-primary" onClick={() => callApi('v1')}>Calcular (v1 Crudo)</button>
        <button className="btn btn-primary" style={{backgroundColor: '#10b981'}} onClick={() => callApi('v2')}>Calcular (v2 Formateado)</button>
      </div>

      {error && (
        <div className="result-card error">
          <strong>Error:</strong>
          <pre style={{whiteSpace: 'pre-wrap', textAlign: 'left', marginTop: '1rem', fontFamily: 'inherit'}}>{error}</pre>
        </div>
      )}

      {result && (
        <div className="result-card">
          <p>Consumo Total: <span className="result-value">{result.kwh}</span></p>
          <p>Costo Estimado: <span className="result-value">{result.cost}</span></p>
        </div>
      )}
    </div>
  );
}

export default App;

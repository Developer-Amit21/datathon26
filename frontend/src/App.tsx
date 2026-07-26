import { useEffect, useState } from 'react';
import axios from 'axios';
import './styles.css';

interface SummaryResponse {
  total_cases: number;
  high_risk_cases: number;
  repeat_offenders: number;
  districts: string[];
}

interface ChatResponse {
  answer: string;
  evidence: Array<{ source: string; evidence: string; score: number }>;
  confidence_score: number;
  data_source: str;
  reasoning: str;
  is_safe: boolean;
}

interface NetworkResponse {
  nodes: Array<{ id: string; label: string; type: string; risk?: number; gang?: string }>;
  edges: Array<{ source: string; target: string; relationship: string; confidence: number }>;
  community_detection: Array<{ community_id: number; name: string; size: number; modularity_score: number }>;
  centrality_analysis: Record<string, { label: string; betweenness: number; closeness: number; eigenvector: number }>;
}

interface ForecastResponse {
  target_district: string;
  forecasting_horizon: string;
  hotspots: Array<{ location: string; intensity_score: number; predicted_crime_type: string; peak_risk_window: string; probability_next_7_days: number }>;
  mo_clusters: Array<{ cluster_name: string; pattern: string }>;
}

interface FinancialResponse {
  total_transactions: number;
  total_volume_inr: number;
  suspicious_volume_inr: number;
  risk_ratio: number;
  suspicious_alerts: Array<{ tx_id: number; sender: string; receiver: string; amount: number; flag_reason: string }>;
}

interface RiskProfileResponse {
  offender_name: string;
  recidivism_risk_score: number;
  risk_category: string;
  shap_explanation: {
    base_value: number;
    feature_contributions: Record<string, number>;
    reasoning_summary: string;
  };
  recommended_action: string;
}

function App() {
  const [activeTab, setActiveTab] = useState<'summary' | 'chat' | 'network' | 'forecast' | 'financial' | 'risk'>('summary');
  
  // Data states
  const [summary, setSummary] = useState<SummaryResponse | null>(null);
  const [chatAnswer, setChatAnswer] = useState<ChatResponse | null>(null);
  const [chatQuery, setChatQuery] = useState('Show all theft FIRs in Bangalore');
  const [selectedLang, setSelectedLang] = useState('en');
  const [chatLoading, setChatLoading] = useState(false);

  const [network, setNetwork] = useState<NetworkResponse | null>(null);
  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [financial, setFinancial] = useState<FinancialResponse | null>(null);
  const [riskProfile, setRiskProfile] = useState<RiskProfileResponse | null>(null);

  const API_BASE = 'http://127.0.0.1:8000/api';

  useEffect(() => {
    axios.get(`${API_BASE}/analytics/summary`).then((res) => setSummary(res.data)).catch(() => {});
  }, []);

  const loadNetwork = () => {
    axios.get(`${API_BASE}/graph/network`).then((res) => setNetwork(res.data)).catch(() => {});
  };

  const loadForecast = () => {
    axios.get(`${API_BASE}/forecast/hotspots?district=Bangalore`).then((res) => setForecast(res.data)).catch(() => {});
  };

  const loadFinancial = () => {
    axios.get(`${API_BASE}/financial/analytics`).then((res) => setFinancial(res.data)).catch(() => {});
  };

  const loadRiskProfile = () => {
    axios.get(`${API_BASE}/forecast/risk/1`).then((res) => setRiskProfile(res.data)).catch(() => {});
  };

  const handleTabChange = (tab: 'summary' | 'chat' | 'network' | 'forecast' | 'financial' | 'risk') => {
    setActiveTab(tab);
    if (tab === 'network' && !network) loadNetwork();
    if (tab === 'forecast' && !forecast) loadForecast();
    if (tab === 'financial' && !financial) loadFinancial();
    if (tab === 'risk' && !riskProfile) loadRiskProfile();
  };

  const askChat = async () => {
    setChatLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/chat`, {
        message: chatQuery,
        user_name: 'investigator_lead',
        role: 'INVESTIGATOR',
        language: selectedLang
      });
      setChatAnswer(res.data);
    } catch {
      // error fallback
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div className="page">
      <header>
        <h1>Crime Intelligence & Conversational Analytics Platform</h1>
        <p>Enterprise AI Engine • PostGIS Spatio-Temporal • Neo4j Graph GDS • Hybrid RAG • Explainable SHAP</p>
      </header>

      {/* Tab Navigation */}
      <nav className="tab-nav">
        <button className={`tab-button ${activeTab === 'summary' ? 'active' : ''}`} onClick={() => handleTabChange('summary')}>📊 Operational Summary</button>
        <button className={`tab-button ${activeTab === 'chat' ? 'active' : ''}`} onClick={() => handleTabChange('chat')}>💬 Conversational RAG & Voice</button>
        <button className={`tab-button ${activeTab === 'network' ? 'active' : ''}`} onClick={() => handleTabChange('network')}>🕸️ Criminal Network & GDS</button>
        <button className={`tab-button ${activeTab === 'forecast' ? 'active' : ''}`} onClick={() => handleTabChange('forecast')}>🗺️ Hotspots & ST-GCN</button>
        <button className={`tab-button ${activeTab === 'financial' ? 'active' : ''}`} onClick={() => handleTabChange('financial')}>💳 Financial AML & Flow</button>
        <button className={`tab-button ${activeTab === 'risk' ? 'active' : ''}`} onClick={() => handleTabChange('risk')}>🎯 SHAP Risk Scorecard</button>
      </nav>

      {/* Tab 1: Operational Summary */}
      {activeTab === 'summary' && (
        <section className="card">
          <h2>Operational Overview & Metrics</h2>
          {summary ? (
            <div className="stats-grid">
              <div className="stat-box">
                <div className="number">{summary.total_cases}</div>
                <div className="label">Total Case FIRs</div>
              </div>
              <div className="stat-box">
                <div className="number">{summary.high_risk_cases}</div>
                <div className="label">High Severity Cases</div>
              </div>
              <div className="stat-box">
                <div className="number">{summary.repeat_offenders}</div>
                <div className="label">Repeat Suspects</div>
              </div>
              <div className="stat-box">
                <div className="number">{summary.districts.length}</div>
                <div className="label">Monitored Districts</div>
              </div>
            </div>
          ) : (
            <p>Loading analytics metrics...</p>
          )}
        </section>
      )}

      {/* Tab 2: Conversational RAG & Voice */}
      {activeTab === 'chat' && (
        <section className="card">
          <h2>Conversational Intelligence Assistant</h2>
          <div className="input-row">
            <input 
              value={chatQuery} 
              onChange={(e) => setChatQuery(e.target.value)} 
              placeholder="Ask an investigative query..."
            />
            <select value={selectedLang} onChange={(e) => setSelectedLang(e.target.value)} style={{ flex: '0 0 140px' }}>
              <option value="en">English (EN)</option>
              <option value="hi">Hindi (HI)</option>
              <option value="ka">Kannada (KA)</option>
              <option value="ta">Tamil (TA)</option>
            </select>
            <button className="btn-primary" onClick={askChat}>
              {chatLoading ? 'Thinking...' : 'Query Engine'}
            </button>
          </div>

          {chatAnswer && (
            <div className="response">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span className={`badge ${chatAnswer.is_safe ? 'badge-safe' : 'badge-critical'}`}>
                  {chatAnswer.is_safe ? 'PII & Injection Checked' : 'Security Alert Blocked'}
                </span>
                <span style={{ fontSize: '0.85rem', color: '#94a3b8' }}>Confidence: <strong>{(chatAnswer.confidence_score * 100).toFixed(0)}%</strong></span>
              </div>
              <p style={{ fontSize: '1.05rem', lineHeight: '1.5' }}>{chatAnswer.answer}</p>
              <p><strong>Data Grounding:</strong> {chatAnswer.data_source}</p>
              <p><strong>Explainable Reasoning:</strong> {chatAnswer.reasoning}</p>

              {chatAnswer.evidence.length > 0 && (
                <>
                  <h4 style={{ margin: '1rem 0 0.5rem 0' }}>Cited FIR Evidence:</h4>
                  <ul>
                    {chatAnswer.evidence.map((item, idx) => (
                      <li key={idx}><strong>{item.source}:</strong> {item.evidence} (Relevance: {item.score})</li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          )}
        </section>
      )}

      {/* Tab 3: Criminal Network */}
      {activeTab === 'network' && (
        <section className="card">
          <h2>Criminal Network Analysis & Neo4j GDS</h2>
          {network ? (
            <>
              <h3>Louvain Detected Communities</h3>
              <div className="network-list">
                {network.community_detection.map((comm) => (
                  <div key={comm.community_id} className="list-item">
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <strong>{comm.name}</strong>
                      <span className="badge badge-medium">Modularity: {comm.modularity_score}</span>
                    </div>
                    <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.85rem' }}>Members Count: {comm.size}</p>
                  </div>
                ))}
              </div>

              <h3 style={{ marginTop: '1.5rem' }}>Network Nodes ({network.nodes.length}) & Edges ({network.edges.length})</h3>
              <div className="network-list">
                {network.nodes.map((node) => (
                  <div key={node.id} className="list-item">
                    <strong>{node.label}</strong> ({node.type})
                    {node.gang && <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Gang: {node.gang}</div>}
                    {node.risk && <span className="badge badge-critical" style={{ marginTop: '0.4rem' }}>Risk Score: {node.risk}</span>}
                  </div>
                ))}
              </div>
            </>
          ) : (
            <p>Fetching graph network topology...</p>
          )}
        </section>
      )}

      {/* Tab 4: Forecasting & Hotspots */}
      {activeTab === 'forecast' && (
        <section className="card">
          <h2>Spatio-Temporal Crime Hotspots & ST-GCN Forecasting</h2>
          {forecast ? (
            <>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <span>District: <strong>{forecast.target_district}</strong></span>
                <span className="badge badge-medium">Horizon: {forecast.forecasting_horizon}</span>
              </div>
              <div className="hotspot-list">
                {forecast.hotspots.map((spot, idx) => (
                  <div key={idx} className="list-item">
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <strong>{spot.location}</strong>
                      <span className="badge badge-high">Prob: {(spot.probability_next_7_days * 100).toFixed(0)}%</span>
                    </div>
                    <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.85rem' }}>Category: {spot.predicted_crime_type}</p>
                    <p style={{ margin: '0.2rem 0 0 0', fontSize: '0.85rem' }}>Peak Risk: {spot.peak_risk_window}</p>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <p>Running spatial-temporal forecasting model...</p>
          )}
        </section>
      )}

      {/* Tab 5: Financial AML */}
      {activeTab === 'financial' && (
        <section className="card">
          <h2>Financial Crime & AML Money Flow Graph</h2>
          {financial ? (
            <>
              <div className="stats-grid" style={{ marginBottom: '1.5rem' }}>
                <div className="stat-box">
                  <div className="number">₹{(financial.total_volume_inr / 1000).toFixed(0)}k</div>
                  <div className="label">Total Monitored Volume</div>
                </div>
                <div className="stat-box">
                  <div className="number" style={{ color: '#ff4b2b' }}>₹{(financial.suspicious_volume_inr / 1000).toFixed(0)}k</div>
                  <div className="label">Flagged Suspicious Volume</div>
                </div>
                <div className="stat-box">
                  <div className="number">{financial.suspicious_alerts.length}</div>
                  <div className="label">AML Violations Flagged</div>
                </div>
              </div>

              <h3>Suspicious Transaction Alerts</h3>
              <div className="network-list">
                {financial.suspicious_alerts.map((alert) => (
                  <div key={alert.tx_id} className="list-item" style={{ borderLeft: '4px solid #ff4b2b' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <strong>{alert.sender} ➔ {alert.receiver}</strong>
                      <span className="badge badge-critical">₹{alert.amount.toLocaleString()}</span>
                    </div>
                    <p style={{ margin: '0.4rem 0 0 0', fontSize: '0.85rem', color: '#ff7675' }}>{alert.flag_reason}</p>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <p>Executing AML money flow transaction analysis...</p>
          )}
        </section>
      )}

      {/* Tab 6: SHAP Risk Scorecard */}
      {activeTab === 'risk' && (
        <section className="card">
          <h2>Explainable AI (SHAP) Offender Risk Scorecard</h2>
          {riskProfile ? (
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <div>
                  <h3 style={{ margin: 0 }}>{riskProfile.offender_name}</h3>
                  <span style={{ fontSize: '0.85rem', color: '#94a3b8' }}>Target Profile ID #1</span>
                </div>
                <span className="badge badge-critical" style={{ fontSize: '1rem', padding: '0.4rem 0.8rem' }}>
                  Risk Score: {(riskProfile.recidivism_risk_score * 100).toFixed(0)}% [{riskProfile.risk_category}]
                </span>
              </div>

              <p><strong>Reasoning Summary:</strong> {riskProfile.shap_explanation.reasoning_summary}</p>
              
              <h4 style={{ marginTop: '1.2rem' }}>SHAP Feature Contributions:</h4>
              <div className="stats-grid">
                {Object.entries(riskProfile.shap_explanation.feature_contributions).map(([key, val]) => (
                  <div key={key} className="stat-box" style={{ textAlign: 'left' }}>
                    <div className="label" style={{ textTransform: 'capitalize' }}>{key.replace(/_/g, ' ')}</div>
                    <div className="number" style={{ fontSize: '1.2rem', marginTop: '0.2rem' }}>+{val}</div>
                  </div>
                ))}
              </div>

              <p style={{ marginTop: '1.5rem' }}><strong>Recommended Intervention:</strong> {riskProfile.recommended_action}</p>
            </div>
          ) : (
            <p>Computing SHAP feature attributions...</p>
          )}
        </section>
      )}
    </div>
  );
}

export default App;

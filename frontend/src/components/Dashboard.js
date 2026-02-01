import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';
import { datasetService } from '../services/api';
import './Dashboard.css';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

function Dashboard({ username }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentData, setCurrentData] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const data = await datasetService.getHistory();
      setHistory(data);
    } catch (err) {
      console.error('Error fetching history:', err);
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError('');
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await datasetService.uploadCSV(file);
      setCurrentData(response);
      fetchHistory();
      setFile(null);
      document.getElementById('file-input').value = '';
    } catch (err) {
      setError(err.response?.data?.error || 'Error uploading file');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async (datasetId) => {
    try {
      await datasetService.downloadPDF(datasetId);
    } catch (err) {
      console.error('PDF Download Error:', err);
      alert('Error downloading PDF: ' + (err.response?.data?.error || err.message));
    }
  };

  const getTypeDistributionChart = (typeDistribution) => {
    const labels = Object.keys(typeDistribution);
    const data = Object.values(typeDistribution);
    
    return {
      labels,
      datasets: [{
        label: 'Equipment Count',
        data,
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 159, 64, 0.6)',
        ],
      }],
    };
  };

  const getParametersChart = (summary) => {
    return {
      labels: ['Flowrate', 'Pressure', 'Temperature'],
      datasets: [{
        label: 'Average Values',
        data: [summary.avg_flowrate, summary.avg_pressure, summary.avg_temperature],
        backgroundColor: [
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 99, 132, 0.6)',
          'rgba(75, 192, 192, 0.6)',
        ],
      }],
    };
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Chemical Equipment Visualizer</h1>
        <div className="user-info">
          <span>Welcome, {username}</span>
        </div>
      </header>

      <div className="upload-section">
        <h2>Upload CSV File</h2>
        <div className="upload-controls">
          <input
            id="file-input"
            type="file"
            accept=".csv"
            onChange={handleFileChange}
          />
          <button onClick={handleUpload} disabled={loading || !file}>
            {loading ? 'Uploading...' : 'Upload & Analyze'}
          </button>
        </div>
        {error && <div className="error-message">{error}</div>}
      </div>

      {currentData && (
        <div className="results-section">
          <h2>Analysis Results</h2>
          
          <div className="summary-cards">
            <div className="summary-card">
              <h3>Total Equipment</h3>
              <p className="big-number">{currentData.summary.total_count}</p>
            </div>
            <div className="summary-card">
              <h3>Avg Flowrate</h3>
              <p className="big-number">{currentData.summary.avg_flowrate}</p>
            </div>
            <div className="summary-card">
              <h3>Avg Pressure</h3>
              <p className="big-number">{currentData.summary.avg_pressure}</p>
            </div>
            <div className="summary-card">
              <h3>Avg Temperature</h3>
              <p className="big-number">{currentData.summary.avg_temperature}</p>
            </div>
          </div>

          <div className="charts-section">
            <div className="chart-container">
              <h3>Equipment Type Distribution</h3>
              <Pie data={getTypeDistributionChart(currentData.summary.type_distribution)} />
            </div>
            <div className="chart-container">
              <h3>Average Parameters</h3>
              <Bar data={getParametersChart(currentData.summary)} options={{
                scales: {
                  y: { beginAtZero: true }
                }
              }} />
            </div>
          </div>

          <div className="data-table-section">
            <h3>Equipment Data</h3>
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>Equipment Name</th>
                    <th>Type</th>
                    <th>Flowrate</th>
                    <th>Pressure</th>
                    <th>Temperature</th>
                  </tr>
                </thead>
                <tbody>
                  {currentData.data.map((row, idx) => (
                    <tr key={idx}>
                      <td>{row['Equipment Name']}</td>
                      <td>{row.Type}</td>
                      <td>{row.Flowrate}</td>
                      <td>{row.Pressure}</td>
                      <td>{row.Temperature}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <button 
            className="download-pdf-btn"
            onClick={() => handleDownloadPDF(currentData.dataset_id)}
          >
            Download PDF Report
          </button>
        </div>
      )}

      {history.length > 0 && (
        <div className="history-section">
          <h2>Upload History (Last 5)</h2>
          <div className="history-cards">
            {history.map((dataset) => (
              <div key={dataset.id} className="history-card">
                <h4>{dataset.filename}</h4>
                <p className="date">{new Date(dataset.uploaded_at).toLocaleString()}</p>
                <div className="history-stats">
                  <span>Count: {dataset.total_count}</span>
                  <span>Avg Flow: {dataset.avg_flowrate.toFixed(2)}</span>
                </div>
                <button onClick={() => handleDownloadPDF(dataset.id)}>
                  Download PDF
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;

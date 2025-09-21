// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

// API Endpoints
export const API_ENDPOINTS = {
  PREDICTORS: '/predictors',
  PREDICT: '/predict',
  PREDICTOR_FIELDS: (predictorId) => `/predictor/${predictorId}/fields`,
  DOWNLOAD_REPORT: '/download-report'
};

// Helper function to build full API URLs
export const buildApiUrl = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`;
};

// Export the base URL for direct use
export { API_BASE_URL };

// Default export
const apiConfig = {
  API_BASE_URL,
  API_ENDPOINTS,
  buildApiUrl
};

export default apiConfig;
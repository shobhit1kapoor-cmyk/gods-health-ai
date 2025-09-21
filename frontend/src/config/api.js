// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

export { API_BASE_URL };

// API endpoints
export const API_ENDPOINTS = {
  PREDICTORS: '/predictors',
  PREDICT: '/predict',
  ANALYZE: '/analyze',
  PREDICTOR_FIELDS: (predictorId: string) => `/predictor/${predictorId}/fields`,
  DOWNLOAD_REPORT: '/download-report',
};

// Helper function to build full URL
export const buildApiUrl = (endpoint: string): string => {
  return `${API_BASE_URL}${endpoint}`;
};
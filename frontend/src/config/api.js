// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';
const IS_STATIC_MODE = process.env.REACT_APP_STATIC_MODE === 'true';

// API Endpoints
export const API_ENDPOINTS = {
  PREDICTORS: '/predictors',
  PREDICT: '/predict',
  PREDICTOR_FIELDS: (predictorId) => `/predictor/${predictorId}/fields`,
  DOWNLOAD_REPORT: '/download-report'
};

// Helper function to build full API URLs
export const buildApiUrl = (endpoint) => {
  if (IS_STATIC_MODE) {
    // Return a dummy URL for static mode to prevent fetch errors
    return '#';
  }
  return `${API_BASE_URL}${endpoint}`;
};

// Check if we're in static mode
export const isStaticMode = () => IS_STATIC_MODE;

// Export the base URL for direct use
export { API_BASE_URL };

// Default export
const apiConfig = {
  API_BASE_URL,
  API_ENDPOINTS,
  buildApiUrl
};

export default apiConfig;
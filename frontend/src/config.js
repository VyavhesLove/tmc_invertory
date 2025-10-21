const config = {
  environment: import.meta.env.VITE_ENVIRONMENT || 'prod',
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  debug: import.meta.env.VITE_ENVIRONMENT === 'dev'
};

export default config;

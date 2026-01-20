// Configuration for API endpoints
const CONFIG = {
    // For local development, use current host
    // For production, set BACKEND_URL in your environment or uncomment and set below
    API_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? `${window.location.protocol}//${window.location.host}/api`
        : (window.BACKEND_URL || 'https://your-backend-url.com/api') // Replace with your deployed backend URL
};

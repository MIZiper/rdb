import axios from 'axios';

// Shared Axios instance
export const apiClient = axios.create({
  baseURL: "/api",
  headers: {
    'Content-Type': 'application/json',
  },
});
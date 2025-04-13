import axios from 'axios';

// Shared Axios instance
export const apiClient = axios.create({
  baseURL: "/api",
  headers: {
    'Content-Type': 'application/json',
  },
});

export const TAG_SPLITTER = ";;";
export const TAG_HIER = ":";
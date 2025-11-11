import axios from 'axios';
import router from '../router';
import { startLoadingTimer, stopLoadingTimer } from './loading';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

api.interceptors.request.use(config => {
  startLoadingTimer();
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  response => {
    stopLoadingTimer();
    return response;
  },
  error => {
    stopLoadingTimer();
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('authToken');
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

export default api;

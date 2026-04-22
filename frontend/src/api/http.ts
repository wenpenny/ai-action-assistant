import axios from 'axios';

const http = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 响应拦截器
http.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API 请求错误:', error);
    return Promise.reject(error);
  }
);

export default http;
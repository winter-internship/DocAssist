import axios from 'axios';

// 백엔드 URL
// Vite 프록시를 활용하기 위해 상대 경로를 사용합니다.
const baseURL = import.meta.env.VITE_API_URL || '/api/v1';

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 토큰 추가를 위한 요청 인터셉터
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 에러 처리를 위한 응답 인터셉터
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // 토큰 만료 또는 유효하지 않음
      localStorage.removeItem('token');
      // 보통 라우터나 스토어에서 로그인 페이지로 리다이렉트를 처리함
      // window.location.href = '/login'; 
    }
    return Promise.reject(error);
  }
);

export default api;


import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-lambda-api.amazonaws.com/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// リクエストインターセプター
apiClient.interceptors.request.use(
  (config) => {
    // 必要に応じて認証トークンを追加
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// レスポンスインターセプター
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // サーバーエラーの処理
      const message = error.response.data?.message || error.response.data?.error || 'サーバーエラーが発生しました';
      throw new Error(message);
    } else if (error.request) {
      // ネットワークエラーの処理
      throw new Error('ネットワークエラーが発生しました');
    } else {
      throw new Error('リクエストの設定でエラーが発生しました');
    }
  }
);

export default apiClient; 
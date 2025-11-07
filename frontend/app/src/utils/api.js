import router from '../router';

export const authenticatedFetch = async (url, options) => {
  const token = localStorage.getItem('authToken');
  const headers = {
    ...options?.headers,
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, { ...options, headers });

  if (response.status === 401) {
    localStorage.removeItem('authToken');
    router.push('/login');
    throw new Error('Unauthorized');
  }

  return response;
};
import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const askQuestion = (question) => {
  return axios.post(`${API_URL}/ask`, { question });
};

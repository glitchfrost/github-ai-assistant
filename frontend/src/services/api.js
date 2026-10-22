import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8080',
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function getAllRepositories() {
  const response = await api.get('/repositories');
  return response.data;
}

export async function analyzeRepository(githubUrl) {
  const response = await api.post('/repositories/analyze', { githubUrl });
  return response.data;
}

export async function askQuestion(repoName, question) {
  const response = await api.post('/repositories/chat', {
    repoName,
    question
  });

  return response.data;
}

export async function scanRepository(path) {
  const response = await api.get(`/scan?path=${encodeURIComponent(path)}`);
  return response.data;
}
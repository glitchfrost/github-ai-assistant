import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { MessageSquare, GitBranch, AlertCircle, Loader } from 'lucide-react';
import { getAllRepositories } from '../services/api';

export default function Dashboard() {
  const [repositories, setRepositories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchRepos() {
      try {
        const data = await getAllRepositories();
        setRepositories(data);
      } catch (err) {
        setError(err.message || 'Failed to fetch repositories.');
      } finally {
        setLoading(false);
      }
    }
    fetchRepos();
  }, []);

  return (
    <div className="dashboard-page">
      <h1 style={{ marginBottom: '2rem', fontSize: '2.5rem' }}>Indexed Repositories</h1>

      {loading ? (
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', color: 'var(--text-secondary)' }}>
          <Loader className="animate-spin" />
          <span>Loading repositories...</span>
        </div>
      ) : error ? (
        <div style={{ color: 'var(--danger)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <AlertCircle />
          <span>{error}</span>
        </div>
      ) : repositories.length === 0 ? (
        <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
          <GitBranch size={48} style={{ opacity: 0.5, marginBottom: '1rem' }} />
          <h2>No repositories indexed yet</h2>
          <p style={{ marginTop: '0.5rem', marginBottom: '2rem' }}>Add a new repository to start chatting with your codebase.</p>
          <Link to="/analyze" className="btn btn-primary">Add Your First Repository</Link>
        </div>
      ) : (
        <div className="repo-grid">
          {repositories.map(repo => (
            <div key={repo.id} className="glass-panel" style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
                <GitBranch color="var(--text-secondary)" />
                <h3 style={{ fontSize: '1.25rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {repo.repoName || repo.githubUrl.split('/').pop()}
                </h3>
              </div>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '1.5rem', wordBreak: 'break-all' }}>
                {repo.githubUrl}
              </p>
              <div style={{ marginTop: 'auto', display: 'flex', justifyContent: 'flex-end' }}>
                <Link to={`/chat/${repo.repoName || repo.githubUrl.split('/').pop()}`} className="btn btn-secondary" style={{ width: '100%' }}>
                  <MessageSquare size={16} />
                  Chat
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}

      <style>{`
        .animate-spin {
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

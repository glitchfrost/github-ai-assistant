import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, Loader, CheckCircle, GitBranch } from 'lucide-react';
import { analyzeRepository } from '../services/api';

export default function Analyze() {
  const [githubUrl, setGithubUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!githubUrl.trim()) return;

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      await analyzeRepository(githubUrl);
      setSuccess(true);
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (err) {
      setError(err.message || 'Failed to analyze repository. Check the URL and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '2rem 0' }}>
      <div style={{ marginBottom: '2rem' }}>
        <Link to="/" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', textDecoration: 'none' }}>
          <ArrowLeft size={16} />
          Back to Dashboard
        </Link>
      </div>

      <div className="glass-panel" style={{ padding: '3rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: '64px', height: '64px', borderRadius: '50%', background: 'var(--primary-light)', marginBottom: '1rem' }}>
            <GitBranch size={32} color="white" />
          </div>
          <h2>Analyze Repository</h2>
          <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>Enter a public GitHub URL to clone and index the codebase.</p>
        </div>

        {success ? (
          <div className="animate-fade-in" style={{ textAlign: 'center', padding: '2rem 0', color: '#4ade80' }}>
            <CheckCircle size={48} style={{ margin: '0 auto 1rem' }} />
            <h3>Analysis Complete!</h3>
            <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>Redirecting to dashboard...</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <div>
              <label htmlFor="url" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, color: 'var(--text-secondary)' }}>GitHub Repository URL</label>
              <input
                id="url"
                type="url"
                required
                placeholder="https://github.com/username/repository"
                className="input-field"
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                disabled={loading}
              />
            </div>

            {error && (
              <div style={{ padding: '1rem', background: 'rgba(255, 107, 107, 0.1)', borderLeft: '4px solid var(--danger)', color: 'var(--danger)', borderRadius: '4px' }}>
                {error}
              </div>
            )}

            <button type="submit" className="btn btn-primary" style={{ padding: '1rem', marginTop: '1rem' }} disabled={loading}>
              {loading ? (
                <>
                  <Loader className="animate-spin" size={20} />
                  Analyzing... (This may take a while)
                </>
              ) : (
                'Analyze Repository'
              )}
            </button>
          </form>
        )}
      </div>

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

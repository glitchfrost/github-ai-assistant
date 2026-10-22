import { useState, useRef, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Send, Loader, Bot, User } from 'lucide-react';
import { askQuestion } from '../services/api';

export default function Chat() {
  const { repoName } = useParams();
  const [messages, setMessages] = useState([
    { id: 1, role: 'ai', text: `Hi! I'm ready to answer questions about the repository **${repoName}**. What would you like to know?` }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { id: Date.now(), role: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Assuming askQuestion works for any currently selected repo
      // If backend requires repoName, the backend API should be updated, but based on RepositoryController, it just takes question string.
      const response = await askQuestion(
        repoName,
        userMessage.text
      );
      const aiResponseText = typeof response === 'string' ? response : response.answer || JSON.stringify(response);
      setMessages(prev => [...prev, { id: Date.now(), role: 'ai', text: aiResponseText }]);
    } catch (err) {
      console.error("AI Chat Error:", err);
      setMessages(prev => [...prev, { id: Date.now(), role: 'ai', text: 'Error: Failed to get response from the AI.', error: true }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 150px)', maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ marginBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Link to="/" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)', textDecoration: 'none' }}>
          <ArrowLeft size={16} />
          Back to Dashboard
        </Link>
        <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '0.5rem 1rem', borderRadius: '20px', fontSize: '0.875rem', border: '1px solid var(--border-glow)' }}>
          Chatting about: <strong style={{ color: 'var(--primary-light)' }}>{repoName}</strong>
        </div>
      </div>

      <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <div style={{ flex: 1, overflowY: 'auto', padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {messages.map(msg => (
            <div key={msg.id} style={{ display: 'flex', gap: '1rem', flexDirection: msg.role === 'user' ? 'row-reverse' : 'row' }}>
              <div style={{
                width: '40px', height: '40px', borderRadius: '50%', flexShrink: 0,
                background: msg.role === 'user' ? 'var(--primary)' : 'rgba(255, 255, 255, 0.1)',
                display: 'flex', alignItems: 'center', justifyContent: 'center'
              }}>
                {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
              </div>
              <div style={{
                background: msg.role === 'user' ? 'var(--primary)' : 'rgba(255, 255, 255, 0.05)',
                color: msg.error ? 'var(--danger)' : 'var(--text-primary)',
                padding: '1rem 1.5rem',
                borderRadius: '16px',
                borderBottomRightRadius: msg.role === 'user' ? '4px' : '16px',
                borderBottomLeftRadius: msg.role === 'ai' ? '4px' : '16px',
                maxWidth: '75%',
                border: msg.role === 'user' ? 'none' : '1px solid var(--border-glow)',
                lineHeight: 1.6
              }}>
                {msg.text}
              </div>
            </div>
          ))}
          {loading && (
            <div style={{ display: 'flex', gap: '1rem', flexDirection: 'row' }}>
               <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'rgba(255, 255, 255, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Bot size={20} />
              </div>
              <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '1rem 1.5rem', borderRadius: '16px', borderBottomLeftRadius: '4px', border: '1px solid var(--border-glow)' }}>
                <Loader className="animate-spin" size={20} color="var(--text-secondary)" />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div style={{ padding: '1.5rem', borderTop: '1px solid var(--border-glow)', background: 'rgba(0, 0, 0, 0.2)' }}>
          <form onSubmit={handleSend} style={{ display: 'flex', gap: '1rem' }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about the code..."
              className="input-field"
              style={{ flex: 1, borderRadius: '24px', padding: '1rem 1.5rem' }}
              disabled={loading}
            />
            <button
              type="submit"
              className="btn btn-primary"
              style={{ borderRadius: '24px', padding: '0 1.5rem' }}
              disabled={loading || !input.trim()}
            >
              <Send size={20} />
            </button>
          </form>
        </div>
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

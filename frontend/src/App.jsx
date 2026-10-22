import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { GitBranch, LayoutDashboard, PlusCircle } from 'lucide-react';
import Dashboard from './components/Dashboard';
import Analyze from './components/Analyze';
import Chat from './components/Chat';

function App() {
  return (
    <Router>
      <div className="app-container">
        <header className="header animate-fade-in">
          <Link to="/" className="header-logo">
            <GitBranch size={32} for="var(--text-primary)" />
            <span>GitHub AI</span>
          </Link>
          <nav style={{ display: 'flex', gap: '1rem' }}>
            <Link to="/" className="btn btn-secondary">
              <LayoutDashboard size={18} />
              Dashboard
            </Link>
            <Link to="/analyze" className="btn btn-primary">
              <PlusCircle size={18} />
              Add Repository
            </Link>
          </nav>
        </header>

        <main className="animate-fade-in" style={{ flex: 1 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analyze" element={<Analyze />} />
            <Route path="/chat/:repoName" element={<Chat />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
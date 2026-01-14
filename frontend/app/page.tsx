'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function Login() {
  const router = useRouter();

  const handleLogin = (e: { preventDefault: () => void; }) => {
    e.preventDefault();
    router.push('/dashboard');
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', alignItems: 'center', justifyContent: 'center' }}>
      
      <div className="login-container">
        <h2>System Auth</h2>

        <form onSubmit={handleLogin}>
          <div className="input-group">
            <input 
              type="text" 
              placeholder="IDENTITY STRING" 
              required 
              autoComplete="off" 
            />
          </div>
          
          <div className="input-group">
            <input 
              type="password" 
              placeholder="ACCESS KEY" 
              required 
            />
          </div>
          
          <button type="submit">Establish Link</button>
        </form>

        <div className="text-center mt-4" style={{ fontSize: '0.8em' }}>
          <span style={{ color: 'var(--terminal-green)' }}>NO CREDENTIALS?</span>{' '}
          <Link href="/register">INITIALIZE NEW USER</Link>
        </div>
      </div>
      
    </div>
  );
}
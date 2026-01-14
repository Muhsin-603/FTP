'use client';
import Link from 'next/link';

export default function Register() {
  return (
    <div style={{ display: 'flex', minHeight: '100vh', alignItems: 'center', justifyContent: 'center' }}>
      
      {/* Uses the global .login-container class for the box, border, and glow */}
      <div className="login-container">
        <h2>Initialize Agent</h2>

        {/* Unique "System Log" styling kept inline */}
        <div style={{ 
          fontSize: '0.75em', 
          color: 'var(--terminal-dim)', 
          marginBottom: '25px', 
          borderLeft: '2px solid var(--terminal-dim)', 
          paddingLeft: '10px', 
          lineHeight: '1.4',
          fontFamily: 'monospace'
        }}>
          &gt; ALLOCATING SECTOR... OK<br/>
          &gt; ENCRYPTING KEYS... OK<br/>
          &gt; AWAITING USER CREDENTIALS_
        </div>

        <form>
          <div className="input-group">
            <label style={{ fontSize: '0.7em', color: 'var(--terminal-dim)', textTransform: 'uppercase', display: 'block', marginBottom: '5px' }}>
              Define Identity String
            </label>
            <input type="text" placeholder="ENTER USERNAME" required autoComplete="off" />
          </div>
          
          <div className="input-group">
            <label style={{ fontSize: '0.7em', color: 'var(--terminal-dim)', textTransform: 'uppercase', display: 'block', marginBottom: '5px' }}>
              Set Security Clearance
            </label>
            <input type="password" placeholder="ENTER PASSWORD" required />
          </div>

          <button type="submit">Execute Registration</button>
        </form>

        <div className="text-center mt-4" style={{ fontSize: '0.85em', letterSpacing: '1px' }}>
          <span style={{ color: '#666' }}>ALREADY INITIALIZED?</span>{' '}
          <Link href="/">RETURN TO ACCESS PORT</Link>
        </div>
      </div>

    </div>
  );
}
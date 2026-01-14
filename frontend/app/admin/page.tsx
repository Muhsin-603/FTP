'use client';
import Link from 'next/link';
import { useState } from 'react';

export default function Admin() {
  const [users, setUsers] = useState([
    { id: 1, username: 'root_master', is_admin: true },
    { id: 2, username: 'neo_anderson', is_admin: false },
    { id: 3, username: 'trinity_hacker', is_admin: false },
  ]);

  const togglePower = (id) => {
    setUsers(users.map(u => u.id === id ? { ...u, is_admin: !u.is_admin } : u));
  };

  return (
    <div className="p-4 sm:p-10 min-h-screen relative z-10">
      <style jsx>{`
        h2 { border-bottom: 2px solid #00ff00; padding-bottom: 10px; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; min-width: 600px; } /* Min width prevents squishing */
        th, td { border: 1px solid #333; padding: 12px; text-align: left; }
        th { background: #333; }
        .btn { padding: 5px 10px; color: black; font-weight: bold; cursor: pointer; }
        .promote { background: #00ff00; }
        .demote { background: #ff4444; }
      `}</style>

      <div className="max-w-4xl mx-auto">
        <h2>// ROOT ACCESS // USER MANAGEMENT</h2>
        
        <div className="overflow-x-auto border border-[#333]">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {users.map(u => (
                <tr key={u.id}>
                  <td>{u.id}</td>
                  <td>{u.username}</td>
                  <td>
                    {u.is_admin ? <span className="text-[#ff00ff]">[ADMIN]</span> : <span>[USER]</span>}
                  </td>
                  <td>
                    {u.is_admin ? (
                      <button onClick={() => togglePower(u.id)} className="btn demote">REVOKE POWER</button>
                    ) : (
                      <button onClick={() => togglePower(u.id)} className="btn promote">GRANT POWER</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <Link href="/dashboard" className="block mt-8 text-gray-500 hover:text-[#00ff41]">
          &lt;&lt; Return to Vault Dashboard
        </Link>
      </div>
    </div>
  );
}
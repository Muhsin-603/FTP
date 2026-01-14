'use client';
import Link from 'next/link';
import { useState } from 'react';

export default function Dashboard() {
  const [folders, setFolders] = useState([
    { name: 'TOP_SECRET', uploader: 'admin' },
    { name: 'Blueprints', uploader: 'neo_anderson' },
    { name: 'Evidence', uploader: 'agent_007' }
  ]);
  
  const [files, setFiles] = useState([
    { name: 'passwords.txt', uploader: 'agent_007' },
    { name: 'mission_brief.log', uploader: 'root_master' }
  ]);

  // 2. Modal State
  const [modal, setModal] = useState({ open: false, title: '', progress: 0, status: '' });

  // 3. Simulation Function (Mimics XHR)
  const simulateAction = (title, startText) => {
    setModal({ open: true, title: title, progress: 0, status: startText });
    
    let p = 0;
    const interval = setInterval(() => {
      p += Math.floor(Math.random() * 15);
      if (p >= 100) {
        p = 100;
        clearInterval(interval);
        setModal(prev => ({ ...prev, progress: 100, status: 'COMPLETE' }));
        setTimeout(() => setModal({ open: false, title: '', progress: 0, status: '' }), 1000);
      } else {
        setModal(prev => ({ ...prev, progress: p, status: `PROCESSING PACKETS: ${p}%` }));
      }
    }, 300);
  };

  const handleUpload = () => simulateAction('TRANSMITTING TO CORE', 'INITIALIZING UPLOAD...');
  const handleRetrieve = (name) => simulateAction('RECEIVING DATA STREAM', `DOWNLOADING ${name}...`);
  const handleDelete = (name) => confirm(`Delete ${name}?`) && alert('Deleted (Simulation)');

  return (
    <div className="p-4 sm:p-10 min-h-screen relative z-10">
      
      <div className="dash-container">
        
        <div className="dash-header">
          <h3 className="text-lg">VAULT // AGENT_007</h3>
          <Link href="/" style={{ color: 'var(--error-red)' }} className="hover:underline">
            [ TERMINATE ]
          </Link>
        </div>

        <div className="sector-bar">
          <span>SECTOR: /root</span>
        </div>

        <div className="controls-wrapper">
          <div className="upload-panel">
            <div className="upload-col">
              <span className="upload-label">Standard Transmission</span>
              <input type="file" style={{ color: 'var(--terminal-green)', fontSize: '0.75rem', marginBottom: '8px' }} />
              <button className="btn-upload" onClick={handleUpload}>UPLOAD FILES</button>
            </div>
            
            <div className="hidden sm:block" style={{ width: '1px', background: 'var(--terminal-dim)' }}></div>
            
            <div className="upload-col">
              <span className="upload-label">Structure Injection</span>
              <input type="file" webkitdirectory="" style={{ color: 'var(--terminal-green)', fontSize: '0.75rem', marginBottom: '8px' }} />
              <button className="btn-upload" onClick={handleUpload}>UPLOAD FOLDER</button>
            </div>
          </div>

          <div className="purge-panel">
            <button 
              onClick={() => confirm('WARNING: INCINERATE SECTOR?')}
              className="btn-purge"
            >
              PURGE<br/>SECTOR
            </button>
          </div>
        </div>
        <div className="grid-files">
          {folders.map(folder => (
            <div key={folder.name} className="file-card">
              <div>
                <Link href="#" className="text-white font-bold block mb-2">
                  <span className="text-4xl block mb-1">📂</span>
                  {folder.name}
                </Link>
                <span className="uploader-tag">OWNER: {folder.uploader}</span>
              </div>
              
              <div className="btn-group">
                <button onClick={() => handleRetrieve(folder.name)} className="btn-retrieve">
                  [ RETRIEVE ]
                </button>
                <button onClick={() => handleDelete(folder.name)} className="btn-del-mini">
                  [ DELETE ]
                </button>
              </div>
            </div>
          ))}

          {files.map(file => (
            <div key={file.name} className="file-card">
              <div>
                <Link href="#" className="block mb-2 break-all" style={{ color: 'var(--terminal-green)' }}>
                  <span className="text-4xl block mb-1">📄</span>
                  {file.name}
                </Link>
                <span className="uploader-tag">OWNER: {file.uploader}</span>
              </div>

              <div className="btn-group">
                <button onClick={() => handleRetrieve(file.name)} className="btn-retrieve">
                  [ RETRIEVE ]
                </button>
                <button onClick={() => handleDelete(file.name)} className="btn-del-mini">
                  [ DELETE ]
                </button>
              </div>
            </div>
          ))}
        </div>
        
        {folders.length === 0 && files.length === 0 && (
            <div className="text-center text-[#666] p-10 italic">
                &gt; SECTOR EMPTY.<br/>
                &gt; AWAITING DATA INPUT...
            </div>
        )}
      </div>

      {modal.open && (
        <div className="modal-overlay">
          <div className="progress-box">
            <div className="progress-title">{modal.title}</div>
            <div className="progress-bar-container">
              <div className="progress-fill" style={{ width: `${modal.progress}%` }}></div>
            </div>
            <div className="progress-text">{modal.status}</div>
            <button className="btn-cancel" onClick={() => setModal({ ...modal, open: false })}>
              [ ABORT SEQUENCE ]
            </button>
          </div>
        </div>
      )}

    </div>
  );
}
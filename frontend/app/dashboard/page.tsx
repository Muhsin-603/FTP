'use client';
import Link from 'next/link';
import { useState } from 'react';

export default function Dashboard() {
  const [folders, setFolders] = useState(['TOP_SECRET', 'Blueprints', 'Evidence']);
  const [files, setFiles] = useState(['passwords.txt', 'mission_brief.log']);

  return (
    <div className="min-h-screen p-4 sm:p-10 relative z-10">
      <style jsx>{`
        .dash-container {
          max-width: 900px; margin: 0 auto; border: 2px solid var(--terminal-green);
          padding: 20px; background: var(--glass-black); box-shadow: 0 0 20px rgba(0, 255, 65, 0.1);
        }
        .header { border-bottom: 2px dashed var(--terminal-green); padding-bottom: 15px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
        .controls { display: flex; gap: 15px; margin-bottom: 20px; }
        .upload-box { flex-grow: 2; border: 1px solid var(--terminal-dim); padding: 15px; display: flex; gap: 15px; }
        .nuke-box { border: 1px solid var(--error-red); padding: 15px; display: flex; flex-direction: column; justify-content: center; }
        
        /* Buttons */
        .btn-upload { background: var(--terminal-green); color: black; border: none; padding: 8px; font-weight: bold; cursor: pointer; width: 100%; margin-top: auto;}
        .btn-nuke { background: transparent; color: var(--error-red); border: 1px solid var(--error-red); padding: 10px; font-weight: bold; cursor: pointer; height: 100%; }
        .btn-nuke:hover { background: var(--error-red); color: black; box-shadow: 0 0 10px var(--error-red); }

        /* Grid */
        .grid-layout { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 15px; }
        .item-card { border: 1px solid var(--dim-gray); padding: 10px; text-align: center; transition: 0.2s; display: flex; flex-direction: column; }
        .item-card:hover { border-color: var(--terminal-green); background: rgba(0, 255, 65, 0.05); }

        /* Responsive Adjustments */
        @media (max-width: 768px) {
          .controls { flex-direction: column; }
          .upload-box { flex-direction: column; }
          .nuke-box { width: 100%; }
          .btn-nuke { width: 100%; min-height: 50px; }
        }
      `}</style>

      <div className="dash-container">
        <div className="header">
          <h3 className="text-lg">VAULT // AGENT_007</h3>
          <Link href="/" className="text-[#ff3333] hover:underline">[ TERMINATE ]</Link>
        </div>

        <div className="bg-[#333] text-white p-2 text-sm mb-5 border-l-4 border-[#00ff41] flex justify-between items-center">
          <span>SECTOR: /root</span>
        </div>

        <div className="controls">
          <div className="upload-box">
            <div className="flex-1 flex flex-col">
              <span className="text-[#008f11] text-xs uppercase mb-1">Standard Transmission</span>
              <input type="file" className="text-[#00ff41] text-xs mb-2" />
              <button className="btn-upload">UPLOAD FILES</button>
            </div>
            <div className="w-[1px] bg-[#008f11] hidden sm:block"></div>
            <div className="flex-1 flex flex-col">
              <span className="text-[#008f11] text-xs uppercase mb-1">Structure Injection</span>
              <input type="file" webkitdirectory="" className="text-[#00ff41] text-xs mb-2" />
              <button className="btn-upload">UPLOAD FOLDER</button>
            </div>
          </div>

          <div className="nuke-box">
            <button className="btn-nuke" onClick={() => confirm('PURGE SECTOR?')}>PURGE<br/>SECTOR</button>
          </div>
        </div>
        <div className="grid-layout">
          {folders.map(folder => (
            <div key={folder} className="item-card">
              <Link href="#" className="text-white font-bold block mb-2">
                <span className="text-4xl block mb-1">📂</span>
                {folder}
              </Link>
              <button className="text-[#ff3333] border border-[#ff3333] text-xs hover:bg-[#ff3333] hover:text-white px-1 py-1 mt-auto">
                [ DELETE ]
              </button>
            </div>
          ))}

          {files.map(file => (
            <div key={file} className="item-card">
              <Link href="#" className="text-[#00ff41] block mb-2 break-all">
                <span className="text-4xl block mb-1">📄</span>
                {file}
              </Link>
              <button className="text-[#ff3333] border border-[#ff3333] text-xs hover:bg-[#ff3333] hover:text-white px-1 py-1 mt-auto">
                [ DELETE ]
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
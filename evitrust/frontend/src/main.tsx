import React, { useState } from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import Dashboard from './routes/Dashboard'
import CaseCreate from './routes/CaseCreate'
import CaseView from './routes/CaseView'
import EvidenceUpload from './routes/EvidenceUpload'
import EvidenceDetail from './routes/EvidenceDetail'
import Admin from './routes/Admin'
import { login } from './api/auth'
import { getUser, setToken, setUser } from './api/client'
import './styles.css'

function LoginCard({ onDone }: { onDone: () => void }) {
  const [email, setEmail] = useState('admin@evitrust.local')
  const [password, setPassword] = useState('password')
  const [error, setError] = useState('')
  return <div className='card'><h2>Login</h2><input value={email} onChange={e=>setEmail(e.target.value)} /><input type='password' value={password} onChange={e=>setPassword(e.target.value)} /><button onClick={async ()=>{try{const r=await login({email,password}); setToken(r.data.access_token); setUser(r.data.user); onDone()}catch{setError('Login failed')}}}>Sign in</button><p>{error}</p></div>
}

function App() {
  const [ready, setReady] = useState(!!localStorage.getItem('evitrust_token'))
  const user = getUser()
  return <BrowserRouter>
    <div className='container'>
      <h1>EviTrust</h1>
      {!ready ? <LoginCard onDone={()=>setReady(true)} /> : <>
        <div className='card'><b>{user?.name}</b> ({user?.role}) — {user?.department || 'N/A'}</div>
        <nav className='nav'>
          <Link to='/'>Dashboard</Link><Link to='/case/new'>Create Case</Link><Link to='/admin'>Admin</Link>
          <button className='secondary' onClick={()=>{localStorage.removeItem('evitrust_token'); localStorage.removeItem('evitrust_user'); window.location.reload()}}>Logout</button>
        </nav>
        <Routes>
          <Route path='/' element={<Dashboard />} />
          <Route path='/case/new' element={<CaseCreate />} />
          <Route path='/case/:id' element={<CaseView />} />
          <Route path='/case/:id/upload' element={<EvidenceUpload />} />
          <Route path='/evidence/:id' element={<EvidenceDetail />} />
          <Route path='/admin' element={<Admin />} />
        </Routes>
      </>}
    </div>
  </BrowserRouter>
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

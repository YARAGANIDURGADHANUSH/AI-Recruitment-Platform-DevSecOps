import React from 'react'
import ReactDOM from 'react-dom/client'
import {
  BrowserRouter,
  Routes,
  Route
} from 'react-router-dom'

import App from './App'
import Recruiter from './pages/Recruiter'

import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>

    <BrowserRouter>

      <Routes>

        <Route path="/" element={<App />} />

        <Route
          path="/recruiter"
          element={<Recruiter />}
        />

      </Routes>

    </BrowserRouter>

  </React.StrictMode>
)
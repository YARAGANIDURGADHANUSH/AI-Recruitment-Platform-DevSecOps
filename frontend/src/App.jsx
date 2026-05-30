import './App.css'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function App() {

  const [jobs, setJobs] = useState([])

  const navigate = useNavigate()

  useEffect(() => {

    axios.get('http://localhost:8000/jobs')
      .then(response => {
        setJobs(response.data)
      })
      .catch(error => {
        console.error(error)
      })

  }, [])

  return (
    <div className="container">

      <h1>AI Recruitment Platform</h1>

      <p className="subtitle">
        Cloud-Native Recruitment System with DevSecOps Pipeline
      </p>

      <div className="card-container">

        <div className="card">
          <h2>Candidate Portal</h2>

          <h3>Available Jobs</h3>

          {
            jobs.map(job => (
              <div key={job.id}>
                <p>
                  <strong>{job.title}</strong>
                </p>

                <p>{job.company}</p>

                <hr />
              </div>
            ))
          }

        </div>

        <div className="card">

          <h2>Recruiter Portal</h2>

          <p>
            Manage job postings and review candidates with AI scoring.
          </p>

          <button onClick={() => navigate('/recruiter')}>
            Recruiter Login
          </button>

        </div>

      </div>

    </div>
  )
}

export default App
import React, { useState, useEffect } from 'react'
import axios from 'axios'
import '../styles/recruiter.css'

function Recruiter() {

  // ======================================
  // STATES
  // ======================================

  const [file, setFile] = useState(null)

  const [result, setResult] = useState(null)

  const [candidates, setCandidates] = useState([])

  const [selectedCandidate, setSelectedCandidate] = useState(null)

  const [candidateInsights, setCandidateInsights] = useState(null)

  // SEARCH + FILTER
  const [search, setSearch] = useState("")

  const [minScore, setMinScore] = useState(0)

  // JOB DESCRIPTION
  const [jobTitle, setJobTitle] = useState("")

  const [jobDescription, setJobDescription] = useState("")

  const [activeJob, setActiveJob] = useState(null)

  // ANALYTICS
  const [analytics, setAnalytics] = useState(null)

  // ======================================
  // LOAD DATA
  // ======================================

  useEffect(() => {

    fetchCandidates()

    fetchAnalytics()

  }, [search, minScore])

  // ======================================
  // FETCH CANDIDATES
  // ======================================

  const fetchCandidates = async () => {

    try {

      const response = await axios.get(
        `http://127.0.0.1:8000/candidates/?search=${search}&min_score=${minScore}`
      )

      setCandidates(response.data)

    } catch (error) {

      console.error(
        "Error fetching candidates:",
        error
      )

    }

  }

  // ======================================
  // FETCH ANALYTICS
  // ======================================

  const fetchAnalytics = async () => {

    try {

      const response = await axios.get(
        'http://127.0.0.1:8000/candidates/analytics'
      )

      setAnalytics(response.data)

    } catch (error) {

      console.error(
        "Analytics Error:",
        error
      )

    }

  }

  // ======================================
  // FETCH AI INSIGHTS
  // ======================================

  const fetchCandidateInsights = async (candidate) => {

    try {

      const response = await axios.get(
        `http://127.0.0.1:8000/insights/${candidate.id}`
      )

      setCandidateInsights(response.data)

      setSelectedCandidate(candidate)

    } catch (error) {

      console.error(
        "Insights Error:",
        error
      )

    }

  }

  // ======================================
  // CREATE JOB
  // ======================================

  const createJob = async () => {

    if (!jobTitle || !jobDescription) {

      alert("Please enter job details")

      return

    }

    try {

      const response = await axios.post(
        'http://127.0.0.1:8000/jobs/create',
        {

          title: jobTitle,

          description: jobDescription
        }
      )

      setActiveJob(response.data)

      alert("Job Created Successfully")

    } catch (error) {

      console.error(
        "Job Creation Error:",
        error
      )

      alert("Failed to create job")

    }

  }

  // ======================================
  // UPLOAD RESUME
  // ======================================

  const handleUpload = async () => {

    if (!file) {

      alert("Please select a resume")

      return

    }

    const formData = new FormData()

    formData.append("file", file)

    try {

      // UPLOAD
      await axios.post(
        'http://127.0.0.1:8000/upload/',
        formData
      )

      // AI SCORE
      const response = await axios.post(
        'http://127.0.0.1:8000/ai/score',
        formData
      )

      setResult(response.data)

      fetchCandidates()

      fetchAnalytics()

    } catch (error) {

      console.error(
        "Error during upload:",
        error
      )

      alert(
        "Upload Failed. Please check console."
      )

    }

  }

  // ======================================
  // SHORTLIST
  // ======================================

  const shortlistCandidate = async (id) => {

    try {

      await axios.put(
        `http://127.0.0.1:8000/candidates/shortlist/${id}`
      )

      fetchCandidates()

      fetchAnalytics()

    } catch (error) {

      console.error(
        "Shortlist Error:",
        error
      )

    }

  }

  // ======================================
  // REJECT
  // ======================================

  const rejectCandidate = async (id) => {

    try {

      await axios.put(
        `http://127.0.0.1:8000/candidates/reject/${id}`
      )

      fetchCandidates()

      fetchAnalytics()

    } catch (error) {

      console.error(
        "Reject Error:",
        error
      )

    }

  }

  // ======================================
  // RESET
  // ======================================

  const resetCandidate = async (id) => {

    try {

      await axios.put(
        `http://127.0.0.1:8000/candidates/reset/${id}`
      )

      fetchCandidates()

      fetchAnalytics()

    } catch (error) {

      console.error(
        "Reset Error:",
        error
      )

    }

  }

  // ======================================
  // UI
  // ======================================

  return (

    <div className="container">

      <h1>Recruiter Dashboard</h1>

      <p>
        AI Powered Recruitment Platform
      </p>

      {/* ======================================
          ANALYTICS DASHBOARD
      ====================================== */}

      {
        analytics && (

          <div
            style={{
              display: 'grid',
              gridTemplateColumns:
                'repeat(auto-fit, minmax(220px, 1fr))',
              gap: '20px',
              marginTop: '30px',
              marginBottom: '30px'
            }}
          >

            <div className="card">
              <h3>Total Candidates</h3>
              <h1>{analytics.total_candidates}</h1>
            </div>

            <div className="card">
              <h3>Shortlisted</h3>
              <h1>{analytics.shortlisted}</h1>
            </div>

            <div className="card">
              <h3>Rejected</h3>
              <h1>{analytics.rejected}</h1>
            </div>

            <div className="card">
              <h3>Pending</h3>
              <h1>{analytics.pending}</h1>
            </div>

            <div className="card">
              <h3>Average Score</h3>
              <h1>{analytics.average_score}%</h1>
            </div>

            <div className="card">

              <h3>Top Candidate</h3>

              <h2>
                {
                  analytics.top_candidate
                    ?.name || "N/A"
                }
              </h2>

              <p>
                {
                  analytics.top_candidate
                    ?.score || 0
                }%
              </p>

            </div>

          </div>

        )
      }

      {/* ======================================
          JOB DESCRIPTION SECTION
      ====================================== */}

      <div
        className="card"
        style={{
          marginBottom: '30px',
          padding: '20px'
        }}
      >

        <h2>Create Job Description</h2>

        <input
          type="text"
          placeholder="Job Title"

          value={jobTitle}

          onChange={(e) =>
            setJobTitle(e.target.value)
          }

          style={{
            width: '100%',
            padding: '12px',
            marginBottom: '15px',
            borderRadius: '8px',
            border: 'none'
          }}
        />

        <textarea
          placeholder="Enter Job Description"

          value={jobDescription}

          onChange={(e) =>
            setJobDescription(e.target.value)
          }

          rows="6"

          style={{
            width: '100%',
            padding: '12px',
            borderRadius: '8px',
            border: 'none',
            marginBottom: '15px'
          }}
        />

        <button
          onClick={createJob}
        >
          Create Job
        </button>

      </div>

      {/* ======================================
          RESUME UPLOAD
      ====================================== */}

      <input
        type="file"
        accept=".pdf,.doc,.docx"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      <br /><br />

      <button onClick={handleUpload}>
        Upload Resume
      </button>

      {/* ======================================
          ACTIVE JOB
      ====================================== */}

      {
        activeJob && (

          <div
            className="card"
            style={{
              marginTop: '20px',
              padding: '20px'
            }}
          >

            <h2>
              Active Job Role
            </h2>

            <h3>
              {jobTitle}
            </h3>

            <p>
              <strong>Required Skills:</strong>
            </p>

            <div
              style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '10px',
                marginTop: '10px'
              }}
            >

              {
                activeJob.required_skills?.map(
                  (skill, index) => (

                    <span
                      key={index}

                      style={{
                        backgroundColor: '#2563eb',
                        padding: '8px 14px',
                        borderRadius: '20px',
                        fontWeight: 'bold'
                      }}
                    >
                      {skill}
                    </span>

                  )
                )
              }

            </div>

          </div>

        )
      }

      {/* ======================================
          SEARCH + FILTER
      ====================================== */}

      <div
        style={{
          display: 'flex',
          gap: '15px',
          marginBottom: '20px',
          marginTop: '20px'
        }}
      >

        <input
          type="text"
          placeholder="Search by name or skill"
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
        />

        <input
          type="number"
          placeholder="Minimum Score"
          value={minScore}
          onChange={(e) =>
            setMinScore(e.target.value)
          }
        />

      </div>

      {/* ======================================
          CANDIDATE DATABASE
      ====================================== */}

      <div
        className="card"
        style={{
          marginTop: '20px',
          padding: '20px'
        }}
      >

        <h2>Candidate Database</h2>

        <table
          width="100%"
          border="1"
          cellPadding="10"
          style={{
            borderCollapse: 'collapse'
          }}
        >

          <thead>

            <tr>

              <th>Resume</th>

              <th>Score</th>

              <th>Status</th>

              <th>Actions</th>

            </tr>

          </thead>

          <tbody>

            {
              candidates.map((candidate) => (

                <tr key={candidate.id}>

                  <td
                    onClick={async () => {

                      await fetchCandidateInsights(candidate)

                    }}

                    style={{
                      cursor: 'pointer'
                    }}
                  >
                    {candidate.filename}
                  </td>

                  <td>
                    {candidate.score}%
                  </td>

                  <td>
                    {candidate.status}
                  </td>

                  <td>

                    <button
                      onClick={() =>
                        shortlistCandidate(candidate.id)
                      }
                    >
                      Shortlist
                    </button>

                    <button
                      onClick={() =>
                        rejectCandidate(candidate.id)
                      }
                    >
                      Reject
                    </button>

                    <button
                      onClick={() =>
                        resetCandidate(candidate.id)
                      }
                    >
                      Reset
                    </button>

                  </td>

                </tr>

              ))
            }

          </tbody>

        </table>

      </div>

      {/* ======================================
          AI INSIGHTS MODAL
      ====================================== */}

      {
        selectedCandidate && candidateInsights && (

          <div
            style={{

              position: 'fixed',

              top: 0,

              left: 0,

              width: '100%',

              height: '100%',

              backgroundColor: 'rgba(0,0,0,0.7)',

              display: 'flex',

              justifyContent: 'center',

              alignItems: 'center',

              zIndex: 999
            }}
          >

            <div
              className="card"

              style={{

                width: '700px',

                maxHeight: '90vh',

                overflowY: 'auto',

                padding: '30px',

                position: 'relative'
              }}
            >

              <button

                onClick={() => {

                  setSelectedCandidate(null)

                  setCandidateInsights(null)

                }}
              >
                X
              </button>

              <h1>
                AI Candidate Intelligence
              </h1>

              <hr />

              <h2>
                {candidateInsights.candidate_name}
              </h2>

              <h3>
                Match Score:
                {' '}
                {candidateInsights.score}%
              </h3>

              <h3>
                Hiring Confidence:
                {' '}
                {candidateInsights.hiring_confidence}%
              </h3>

              <h3>
                Interview Readiness:
                {' '}
                {candidateInsights.interview_readiness}
              </h3>

              {/* MATCHED SKILLS */}

              <div style={{ marginTop: '20px' }}>

                <h2>Matched Skills</h2>

                <div
                  style={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: '10px'
                  }}
                >

                  {
                    candidateInsights.matched_skills?.map(
                      (skill, index) => (

                        <span
                          key={index}
                          style={{
                            backgroundColor: '#16a34a',
                            padding: '8px 14px',
                            borderRadius: '20px',
                            color: 'white'
                          }}
                        >
                          {skill}
                        </span>

                      )
                    )
                  }

                </div>

              </div>

              {/* WEAKNESSES */}

              <div style={{ marginTop: '20px' }}>

                <h2>Weaknesses</h2>

                <ul>

                  {
                    candidateInsights.weaknesses?.map(
                      (item, index) => (

                        <li key={index}>
                          {item}
                        </li>

                      )
                    )
                  }

                </ul>

              </div>

              {/* TRAINING */}

              <div style={{ marginTop: '20px' }}>

                <h2>
                  Training Recommendations
                </h2>

                <ul>

                  {
                    candidateInsights.training_recommendations?.map(
                      (item, index) => (

                        <li key={index}>
                          {item}
                        </li>

                      )
                    )
                  }

                </ul>

              </div>

              {/* RECOMMENDATION */}

              <div style={{ marginTop: '20px' }}>

                <h2>AI Recommendation</h2>

                <p>
                  {
                    candidateInsights.recommendation
                  }
                </p>

              </div>

            </div>

          </div>

        )
      }

    </div>

  )

}

export default Recruiter
import { useState } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)

  const handleFileChange = (e) => {
    if (e.target.files) {
      setFile(e.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://192.168.0.200:8000/upload', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const data = await response.json()
        setContent(data.content)
      } else {
        console.error('Upload failed')
        setContent('Upload failed')
      }
    } catch (error) {
      console.error('Error:', error)
      setContent(`Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>File Upload & Read</h1>
      <div className="upload-section">
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={!file || loading}>
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </div>

      <div style={{ marginTop: '1rem' }}>
        <a href="/link.html">
          <button>Go to Link Page</button>
        </a>
      </div>

      {content && (
        <div className="result-section">
          <h2>File Content:</h2>
          <pre>{content}</pre>
        </div>
      )}
    </div>
  )
}

export default App

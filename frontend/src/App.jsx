import { useState } from 'react'
import axios from 'axios'
import './App.css' 

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [status, setStatus] = useState("Waiting file...")
  const [isLoading, setIsLoading] = useState(false)

  const handleFileChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0])
      setStatus("File selected. Ready to convert.")
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please, select a file.")
      return
    }

    setIsLoading(true)
    setStatus("Sending and converting...")

    const formData = new FormData()
    formData.append("file", selectedFile) 

    try {
      const response = await axios.post("http://127.0.0.1:8000/convert", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'blob', 
      })

      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      
      const extensaoOriginal = selectedFile.name.split('.').pop().toLowerCase()
      const novoNome = extensaoOriginal === 'pdf' ? 'convertido.docx' : 'convertido.pdf'
      
      link.setAttribute('download', novoNome)
      document.body.appendChild(link)
      link.click() 
      
      link.parentNode.removeChild(link)
      setStatus("Download started.")

    } catch (error) {
      console.error("Error on upload:", error)
      setStatus("Error on converting file.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div style={{ padding: '50px', fontFamily: 'Arial' }}>
      <h2>File Converter</h2>
      
      <div style={{ border: '2px dashed #ccc', padding: '20px', margin: '20px 0' }}>
        <input 
          type="file" 
          onChange={handleFileChange} 
          accept=".pdf,.jpg,.jpeg,.png,.bmp"
        />
      </div>

      <button 
        onClick={handleUpload} 
        disabled={isLoading || !selectedFile}
        style={{ padding: '10px 20px', cursor: 'pointer', fontSize: '16px' }}
      >
        {isLoading ? "Loading..." : "Convert File"}
      </button>

      <p>Status: <strong>{status}</strong></p>
    </div>
  )
}

export default App
import { useState } from "react"

const API_BASE_URL = "http://127.0.0.1:8000"

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploadMessage, setUploadMessage] = useState("")
  const [question, setQuestion] = useState("")
  const [answerData, setAnswerData] = useState(null)
  const [loading, setLoading] = useState(false)

  function handleFileChange(event) {
    const file = event.target.files[0]
    setSelectedFile(file)
    setUploadMessage("")
  }

  async function handleUpload() {
    if (!selectedFile) {
      setUploadMessage("Please choose a file first.")
      return
    }

    setLoading(true)
    setUploadMessage("")

    const formData = new FormData()
    formData.append("file", selectedFile)

    try {
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: "POST",
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed")
      }

      setUploadMessage(
        `${data.file_name} uploaded successfully. Chunks created: ${data.chunks_created}`
      )
      setSelectedFile(null)
    } catch (error) {
      setUploadMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleAskQuestion() {
    if (!question.trim()) {
      return
    }

    setLoading(true)
    setAnswerData(null)

    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
          top_k: 3,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Question failed")
      }

      setAnswerData(data)
    } catch (error) {
      setAnswerData({
        answer: error.message,
        sources: [],
      })
    } finally {
      setLoading(false)
    }
  }

  async function handleReset() {
    setLoading(true)
    setAnswerData(null)
    setUploadMessage("")

    try {
      const response = await fetch(`${API_BASE_URL}/reset`, {
        method: "POST",
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Reset failed")
      }

      setUploadMessage(data.message)
    } catch (error) {
      setUploadMessage(error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-100 px-6 py-8">
      <div className="mx-auto max-w-4xl">
        <header className="mb-8 rounded-2xl bg-white p-6 shadow-sm">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">
              Multi-Document AI Assistant
            </h1>

            <p className="mt-2 text-slate-600">
              Upload PDF or TXT documents, then ask questions using your FAISS + LLM backend.
            </p>

            <p className="mt-3 text-sm text-slate-500">
              This system retrieves relevant chunks using FAISS and generates source-grounded answers using an LLM.
            </p>

            <div className="mt-5 flex justify-center">
              <button
                onClick={handleReset}
                disabled={loading}
                className="rounded-xl border border-red-200 px-6 py-2 font-medium text-red-600 hover:bg-red-50 disabled:opacity-50"
              >
                Reset Knowledge Base
              </button>
            </div>
          </div>
        </header>

        <div className="grid gap-6">
          <section className="rounded-2xl bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">
              1. Upload Document
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Upload one document at a time. You can upload multiple documents before asking questions.
            </p>

            <div className="mt-4 flex flex-col gap-3 sm:flex-row">
              <input
                type="file"
                accept=".pdf,.txt"
                onChange={handleFileChange}
                className="block w-full rounded-xl border border-slate-300 px-4 py-2 text-sm"
              />

              <button
                onClick={handleUpload}
                disabled={loading}
                className="rounded-xl bg-slate-900 px-5 py-2 font-medium text-white hover:bg-slate-700 disabled:opacity-50"
              >
                Upload
              </button>
            </div>

            {uploadMessage && (
              <p className="mt-3 rounded-xl bg-slate-50 p-3 text-sm text-slate-700">
                {uploadMessage}
              </p>
            )}
          </section>

          <section className="rounded-2xl bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">
              2. Ask a Question
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Ask a question based on the uploaded documents.
            </p>

            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Example: How quickly should phishing emails be reported?"
              rows="4"
              className="mt-4 w-full rounded-xl border border-slate-300 p-4 text-sm outline-none focus:border-slate-900"
            />

            <div className="mt-4">
              <button
                onClick={handleAskQuestion}
                disabled={loading}
                className="rounded-xl bg-blue-600 px-5 py-2 font-medium text-white hover:bg-blue-500 disabled:opacity-50"
              >
                Ask AI
              </button>
            </div>
          </section>

          {loading && (
            <div className="rounded-2xl bg-white p-6 text-slate-600 shadow-sm">
              Processing...
            </div>
          )}

          {answerData && (
            <section className="rounded-2xl bg-white p-6 shadow-sm">
              <h2 className="text-xl font-semibold text-slate-900">
                Answer
              </h2>

              <p className="mt-4 whitespace-pre-line rounded-xl bg-blue-50 p-4 text-slate-800">
                {answerData.answer}
              </p>

              {answerData.sources && answerData.sources.length > 0 && (
                <div className="mt-6">
                  <h3 className="font-semibold text-slate-900">
                    Sources
                  </h3>

                  <div className="mt-3 space-y-2">
                    {answerData.sources.map((source, index) => (
                      <div
                        key={index}
                        className="rounded-xl border border-slate-200 p-3 text-sm text-slate-700"
                      >
                        <div>
                          <span className="font-medium">File:</span>{" "}
                          {source.file_name}
                        </div>
                        <div>
                          <span className="font-medium">Chunk:</span>{" "}
                          {source.chunk_id}
                        </div>
                        <div>
                          <span className="font-medium">Score:</span>{" "}
                          {source.score.toFixed(3)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </section>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
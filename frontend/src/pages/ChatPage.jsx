import { useState, useRef, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { Send, Loader2, Bot, User, Sparkles, AlertCircle } from 'lucide-react'
import { sendChatMessage } from '../api/client'

export default function ChatPage() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [conversationId, setConversationId] = useState('')
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()

  // Auto-fill from URL query param (from landing page quick-start)
  useEffect(() => {
    const q = searchParams.get('q')
    if (q && messages.length === 0) {
      setInput(q)
    }
  }, [searchParams, messages.length])

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  const handleSend = async () => {
    const text = input.trim()
    if (!text || isLoading) return

    setError(null)
    const userMessage = { role: 'user', content: text }
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await sendChatMessage(text, conversationId || undefined)
      setConversationId(response.conversation_id)

      const assistantMessage = {
        role: 'assistant',
        content: response.message,
      }
      setMessages((prev) => [...prev, assistantMessage])

      // If response contains schemes, store them for results page
      if (response.schemes && response.schemes.length > 0) {
        sessionStorage.setItem('civicos_schemes', JSON.stringify(response.schemes))
        sessionStorage.setItem('civicos_eligibility', JSON.stringify(response.eligibility_results || []))
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Something went wrong'
      setError(errorMessage)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `I'm sorry, I couldn't process that request right now. ${errorMessage.includes('fetch') ? 'Please make sure the backend server is running.' : 'Please try again.'}`,
        },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const suggestions = [
    "I'm a 21-year-old student from UP, family income ₹2.5 lakh",
    "I'm a woman farmer in Maharashtra with 3 acres of land",
    "I'm a senior citizen in Kerala, retired teacher",
    "I'm looking for disability support schemes in Tamil Nadu",
  ]

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-4rem)] md:h-[calc(100vh-4rem)] flex flex-col">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center animate-[fade-in_0.3s_ease-out]">
            <div className="w-16 h-16 bg-primary-100 rounded-2xl flex items-center justify-center mb-6">
              <Sparkles className="w-8 h-8 text-primary-600" />
            </div>
            <h2 className="text-2xl font-bold text-surface-900 mb-2">
              Tell us about yourself
            </h2>
            <p className="text-surface-500 max-w-md mb-8">
              Describe your situation in plain language — age, where you live, what you do,
              your family's income. We'll search current government sources to find schemes you may qualify for.
            </p>
            <div className="grid sm:grid-cols-2 gap-3 w-full max-w-2xl">
              {suggestions.map((s) => (
                <button
                  key={s}
                  onClick={() => setInput(s)}
                  className="text-left bg-white border border-surface-200 hover:border-primary-300 hover:bg-primary-50 rounded-xl px-4 py-3 text-sm text-surface-600 hover:text-primary-700 transition-all duration-200 cursor-pointer"
                >
                  "{s}"
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex gap-3 animate-[slide-up_0.4s_ease-out] ${
                  msg.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                {msg.role === 'assistant' && (
                  <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-primary-100 flex items-center justify-center mt-1">
                    <Bot className="w-4 h-4 text-primary-700" />
                  </div>
                )}
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-primary-700 text-white rounded-br-md'
                      : 'bg-white border border-surface-200 text-surface-800 rounded-bl-md shadow-sm'
                  }`}
                >
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                </div>
                {msg.role === 'user' && (
                  <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-primary-700 flex items-center justify-center mt-1">
                    <User className="w-4 h-4 text-white" />
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className="flex gap-3 animate-[fade-in_0.3s_ease-out]">
                <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-primary-100 flex items-center justify-center mt-1">
                  <Bot className="w-4 h-4 text-primary-700" />
                </div>
                <div className="bg-white border border-surface-200 rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
                  <div className="flex items-center gap-2 text-surface-500 text-sm">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Searching government sources...</span>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Error */}
      {error && (
        <div className="mx-4 mb-2 bg-danger-50 border border-danger-200 text-danger-700 px-4 py-2.5 rounded-xl text-sm flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          {error}
        </div>
      )}

      {/* Input */}
      <div className="border-t border-surface-200 bg-white px-4 py-3">
        <div className="max-w-4xl mx-auto flex items-end gap-3">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Describe your situation... (e.g., I'm a 21-year-old student from UP)"
              rows={1}
              className="w-full resize-none bg-surface-50 border border-surface-200 rounded-xl px-4 py-3 text-sm text-surface-900 placeholder:text-surface-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              style={{ minHeight: '44px', maxHeight: '120px' }}
            />
          </div>
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="flex-shrink-0 w-11 h-11 bg-primary-700 hover:bg-primary-800 disabled:bg-surface-300 text-white rounded-xl flex items-center justify-center transition-all duration-200 cursor-pointer disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
        <p className="text-[11px] text-surface-400 mt-2 text-center">
          CivicOS searches official government sources. Results indicate you may meet published criteria — verify on the official portal.
        </p>
      </div>
    </div>
  )
}

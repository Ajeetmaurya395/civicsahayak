import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import ChatPage from './pages/ChatPage'
import ResultsPage from './pages/ResultsPage'
import SchemeDetailPage from './pages/SchemeDetailPage'
import ProfilePage from './pages/ProfilePage'
import SavedSchemesPage from './pages/SavedSchemesPage'
import LandingPage from './pages/LandingPage'

export default function App() {
  return (
    <Router>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/results" element={<ResultsPage />} />
          <Route path="/scheme/:id" element={<SchemeDetailPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/saved" element={<SavedSchemesPage />} />
        </Route>
      </Routes>
    </Router>
  )
}

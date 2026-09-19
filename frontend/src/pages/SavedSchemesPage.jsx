import { Link } from 'react-router-dom'
import { Bookmark, MessageSquare } from 'lucide-react'

export default function SavedSchemesPage() {
  // Placeholder — in production this loads from MongoDB
  return (
    <div className="max-w-4xl mx-auto px-4 py-20 text-center animate-[fade-in_0.3s_ease-out]">
      <div className="w-16 h-16 bg-surface-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
        <Bookmark className="w-8 h-8 text-surface-400" />
      </div>
      <h2 className="text-2xl font-bold text-surface-900 mb-2">No saved schemes yet</h2>
      <p className="text-surface-500 mb-6 max-w-md mx-auto">
        When you find schemes that interest you, save them here for easy access later.
      </p>
      <Link
        to="/chat"
        className="inline-flex items-center gap-2 bg-primary-700 hover:bg-primary-800 text-white px-6 py-3 rounded-xl font-semibold no-underline transition-all"
      >
        <MessageSquare className="w-5 h-5" />
        Find Schemes
      </Link>
    </div>
  )
}

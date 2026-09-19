import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, ExternalLink, ShieldCheck, ShieldAlert, FileText, MapPin, Building2 } from 'lucide-react'

export default function SchemeDetailPage() {
  const { id } = useParams()

  // In production this would fetch from API; for now load from sessionStorage
  const schemes = JSON.parse(sessionStorage.getItem('civicos_schemes') || '[]')
  const scheme = schemes.find((s) => (s.scheme_id || s.source_url) === decodeURIComponent(id || ''))

  if (!scheme) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center">
        <h2 className="text-2xl font-bold text-surface-900 mb-4">Scheme not found</h2>
        <Link to="/results" className="text-primary-600 hover:text-primary-700 font-medium no-underline">
          ← Back to results
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 animate-[fade-in_0.3s_ease-out]">
      <Link to="/results" className="inline-flex items-center gap-1 text-sm text-surface-500 hover:text-primary-600 no-underline mb-6 font-medium">
        <ArrowLeft className="w-4 h-4" />
        Back to results
      </Link>

      <div className="bg-white rounded-2xl border border-surface-200 overflow-hidden">
        <div className="p-6 sm:p-8">
          {/* Header */}
          <div className="flex items-start gap-3 mb-6">
            {scheme.source_verified ? (
              <span className="inline-flex items-center gap-1 text-xs font-medium bg-success-100 text-success-700 px-2.5 py-1 rounded-full">
                <ShieldCheck className="w-3.5 h-3.5" />
                Verified official source
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 text-xs font-medium bg-accent-100 text-accent-700 px-2.5 py-1 rounded-full">
                <ShieldAlert className="w-3.5 h-3.5" />
                Source not verified
              </span>
            )}
          </div>

          <h1 className="text-2xl sm:text-3xl font-bold text-surface-900 mb-4 leading-tight">
            {scheme.scheme_name}
          </h1>

          {/* Meta */}
          <div className="flex flex-wrap gap-4 mb-6 text-sm text-surface-500">
            {scheme.department && (
              <span className="flex items-center gap-1.5">
                <Building2 className="w-4 h-4" />
                {scheme.department}
              </span>
            )}
            {scheme.state && (
              <span className="flex items-center gap-1.5">
                <MapPin className="w-4 h-4" />
                {scheme.state}
              </span>
            )}
            {scheme.sector && (
              <span className="flex items-center gap-1.5 capitalize">
                <FileText className="w-4 h-4" />
                {scheme.sector}
              </span>
            )}
          </div>

          {/* Description */}
          {scheme.description && (
            <div className="mb-8">
              <h2 className="text-sm font-semibold text-surface-500 uppercase tracking-wide mb-2">About this scheme</h2>
              <p className="text-surface-700 leading-relaxed">{scheme.description}</p>
            </div>
          )}

          {/* Benefits */}
          {scheme.benefits && (
            <div className="mb-8">
              <h2 className="text-sm font-semibold text-surface-500 uppercase tracking-wide mb-2">Benefits</h2>
              <p className="text-surface-700 leading-relaxed">{scheme.benefits}</p>
            </div>
          )}

          {/* Required Documents */}
          {scheme.required_documents && scheme.required_documents.length > 0 && (
            <div className="mb-8">
              <h2 className="text-sm font-semibold text-surface-500 uppercase tracking-wide mb-3">Required documents</h2>
              <div className="grid sm:grid-cols-2 gap-2">
                {scheme.required_documents.map((doc) => (
                  <div key={doc} className="flex items-center gap-2 bg-surface-50 rounded-lg px-3 py-2.5">
                    <FileText className="w-4 h-4 text-surface-400 flex-shrink-0" />
                    <span className="text-sm text-surface-700">{doc}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* How to apply */}
          {scheme.how_to_apply && (
            <div className="mb-8">
              <h2 className="text-sm font-semibold text-surface-500 uppercase tracking-wide mb-2">How to apply</h2>
              <p className="text-surface-700 leading-relaxed">{scheme.how_to_apply}</p>
            </div>
          )}

          {/* Actions */}
          <div className="flex flex-wrap gap-3 pt-6 border-t border-surface-100">
            {scheme.official_application_url ? (
              <a
                href={scheme.official_application_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-primary-700 hover:bg-primary-800 text-white px-5 py-2.5 rounded-xl font-medium no-underline transition-all"
              >
                <ExternalLink className="w-4 h-4" />
                Apply on official portal
              </a>
            ) : (
              <span className="inline-flex items-center gap-2 bg-surface-100 text-surface-500 px-5 py-2.5 rounded-xl font-medium">
                Official application link unavailable — view official scheme information
              </span>
            )}

            {scheme.source_url && (
              <a
                href={scheme.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-white border border-surface-200 hover:bg-surface-50 text-surface-700 px-5 py-2.5 rounded-xl font-medium no-underline transition-all"
              >
                <ExternalLink className="w-4 h-4" />
                View source page
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

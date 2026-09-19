import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { CheckCircle2, XCircle, AlertTriangle, HelpCircle, ExternalLink, Bookmark, ChevronDown, ChevronUp, Shield, ShieldAlert, ShieldCheck } from 'lucide-react'

const statusConfig = {
  ELIGIBLE: {
    icon: CheckCircle2,
    label: 'You appear to meet the criteria',
    color: 'text-success-600',
    bg: 'bg-success-50',
    border: 'border-success-200',
    badge: 'bg-success-100 text-success-700',
    shieldIcon: ShieldCheck,
  },
  POTENTIALLY_ELIGIBLE: {
    icon: AlertTriangle,
    label: 'May qualify — more info needed',
    color: 'text-accent-600',
    bg: 'bg-accent-50',
    border: 'border-accent-200',
    badge: 'bg-accent-100 text-accent-700',
    shieldIcon: Shield,
  },
  NOT_ELIGIBLE: {
    icon: XCircle,
    label: 'Does not appear to match',
    color: 'text-danger-600',
    bg: 'bg-danger-50',
    border: 'border-danger-200',
    badge: 'bg-danger-100 text-danger-700',
    shieldIcon: ShieldAlert,
  },
  INSUFFICIENT_INFORMATION: {
    icon: HelpCircle,
    label: 'Need more information',
    color: 'text-surface-500',
    bg: 'bg-surface-50',
    border: 'border-surface-200',
    badge: 'bg-surface-100 text-surface-600',
    shieldIcon: Shield,
  },
}

function SchemeCard({ scheme, eligibility }) {
  const [expanded, setExpanded] = useState(false)
  const status = eligibility?.status || 'INSUFFICIENT_INFORMATION'
  const config = statusConfig[status]
  const StatusIcon = config.icon

  return (
    <div className={`bg-white rounded-2xl border ${config.border} overflow-hidden transition-all duration-300 hover:shadow-lg animate-[slide-up_0.4s_ease-out]`}>
      <div className="p-5">
        {/* Header */}
        <div className="flex items-start justify-between gap-3 mb-3">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1.5">
              {scheme.source_verified ? (
                <span className="inline-flex items-center gap-1 text-[11px] font-medium bg-success-100 text-success-700 px-2 py-0.5 rounded-full">
                  <ShieldCheck className="w-3 h-3" />
                  Verified source
                </span>
              ) : (
                <span className="inline-flex items-center gap-1 text-[11px] font-medium bg-accent-100 text-accent-700 px-2 py-0.5 rounded-full">
                  <ShieldAlert className="w-3 h-3" />
                  Unverified
                </span>
              )}
              {scheme.government_level && (
                <span className="text-[11px] font-medium bg-surface-100 text-surface-600 px-2 py-0.5 rounded-full capitalize">
                  {scheme.government_level}
                </span>
              )}
              {scheme.sector && (
                <span className="text-[11px] font-medium bg-primary-50 text-primary-700 px-2 py-0.5 rounded-full capitalize">
                  {scheme.sector}
                </span>
              )}
            </div>
            <h3 className="text-lg font-semibold text-surface-900 leading-snug">
              {scheme.scheme_name}
            </h3>
          </div>
        </div>

        {/* Status badge */}
        <div className={`flex items-center gap-2 ${config.bg} ${config.border} border rounded-xl px-3 py-2 mb-3`}>
          <StatusIcon className={`w-4 h-4 ${config.color}`} />
          <span className={`text-sm font-medium ${config.color}`}>{config.label}</span>
        </div>

        {/* Description */}
        {scheme.description && (
          <p className="text-sm text-surface-600 leading-relaxed mb-3 line-clamp-2">
            {scheme.description}
          </p>
        )}

        {/* Eligibility breakdown */}
        {eligibility && (eligibility.matched.length > 0 || eligibility.unmatched.length > 0 || eligibility.missing.length > 0) && (
          <div className="space-y-1.5 mb-3">
            {eligibility.explanation.map((exp, i) => (
              <div
                key={i}
                className={`flex items-start gap-2 text-sm ${
                  exp.startsWith('✓') ? 'text-success-700' :
                  exp.startsWith('✗') ? 'text-danger-600' :
                  'text-accent-600'
                }`}
              >
                <span className="font-mono text-xs mt-0.5">{exp.charAt(0)}</span>
                <span>{exp.substring(2)}</span>
              </div>
            ))}
          </div>
        )}

        {/* Gap description */}
        {eligibility?.gap_description && (
          <div className="bg-danger-50 border border-danger-200 rounded-xl px-3 py-2 mb-3">
            <p className="text-sm text-danger-700">{eligibility.gap_description}</p>
          </div>
        )}

        {/* Expand toggle */}
        <button
          onClick={() => setExpanded(!expanded)}
          className="flex items-center gap-1 text-sm text-primary-600 hover:text-primary-700 font-medium transition-colors cursor-pointer"
        >
          {expanded ? 'Show less' : 'Show more'}
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>

        {/* Expanded content */}
        {expanded && (
          <div className="mt-4 pt-4 border-t border-surface-100 space-y-4 animate-[fade-in_0.3s_ease-out]">
            {scheme.benefits && (
              <div>
                <h4 className="text-xs font-semibold text-surface-500 uppercase tracking-wide mb-1">Benefits</h4>
                <p className="text-sm text-surface-700">{scheme.benefits}</p>
              </div>
            )}

            {scheme.required_documents && scheme.required_documents.length > 0 && (
              <div>
                <h4 className="text-xs font-semibold text-surface-500 uppercase tracking-wide mb-2">Required documents</h4>
                <div className="flex flex-wrap gap-2">
                  {scheme.required_documents.map((doc) => (
                    <span key={doc} className="bg-surface-100 text-surface-700 px-2.5 py-1 rounded-lg text-xs font-medium">
                      {doc}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {scheme.how_to_apply && (
              <div>
                <h4 className="text-xs font-semibold text-surface-500 uppercase tracking-wide mb-1">How to apply</h4>
                <p className="text-sm text-surface-700">{scheme.how_to_apply}</p>
              </div>
            )}

            {scheme.department && (
              <div>
                <h4 className="text-xs font-semibold text-surface-500 uppercase tracking-wide mb-1">Department</h4>
                <p className="text-sm text-surface-700">{scheme.department}</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer actions */}
      <div className="border-t border-surface-100 px-5 py-3 flex items-center justify-between bg-surface-50/50">
        <div className="flex items-center gap-2">
          {scheme.source_url ? (
            <a
              href={scheme.source_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 text-sm text-primary-600 hover:text-primary-700 font-medium no-underline transition-colors"
            >
              <ExternalLink className="w-3.5 h-3.5" />
              View official source
            </a>
          ) : (
            <span className="text-sm text-surface-400">Source unavailable</span>
          )}
        </div>
        <button className="inline-flex items-center gap-1.5 text-sm text-surface-500 hover:text-primary-600 font-medium transition-colors cursor-pointer">
          <Bookmark className="w-3.5 h-3.5" />
          Save
        </button>
      </div>
    </div>
  )
}

export default function ResultsPage() {
  const [schemes, setSchemes] = useState([])
  const [eligibilityResults, setEligibilityResults] = useState([])
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    const storedSchemes = sessionStorage.getItem('civicos_schemes')
    const storedEligibility = sessionStorage.getItem('civicos_eligibility')
    if (storedSchemes) setSchemes(JSON.parse(storedSchemes))
    if (storedEligibility) setEligibilityResults(JSON.parse(storedEligibility))
  }, [])

  const getEligibility = (schemeId) => {
    return eligibilityResults.find((r) => r.scheme_id === schemeId)
  }

  const filteredSchemes = filter === 'all'
    ? schemes
    : schemes.filter((s) => {
        const e = getEligibility(s.scheme_id || s.source_url || '')
        return e?.status === filter
      })

  const statusCounts = {
    all: schemes.length,
    ELIGIBLE: eligibilityResults.filter((r) => r.status === 'ELIGIBLE').length,
    POTENTIALLY_ELIGIBLE: eligibilityResults.filter((r) => r.status === 'POTENTIALLY_ELIGIBLE').length,
    NOT_ELIGIBLE: eligibilityResults.filter((r) => r.status === 'NOT_ELIGIBLE').length,
  }

  if (schemes.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center animate-[fade-in_0.3s_ease-out]">
        <div className="w-16 h-16 bg-surface-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
          <HelpCircle className="w-8 h-8 text-surface-400" />
        </div>
        <h2 className="text-2xl font-bold text-surface-900 mb-2">No results yet</h2>
        <p className="text-surface-500 mb-6">
          Start a conversation to discover government schemes matching your profile.
        </p>
        <Link
          to="/chat"
          className="inline-flex items-center gap-2 bg-primary-700 hover:bg-primary-800 text-white px-6 py-3 rounded-xl font-semibold no-underline transition-all"
        >
          Find Schemes
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 animate-[fade-in_0.3s_ease-out]">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-surface-900">Scheme Results</h1>
        <p className="text-surface-500 mt-1">
          {schemes.length} scheme{schemes.length !== 1 ? 's' : ''} found from official government sources
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2 mb-6">
        {[
          { key: 'all', label: 'All' },
          { key: 'ELIGIBLE', label: 'May qualify' },
          { key: 'POTENTIALLY_ELIGIBLE', label: 'Need more info' },
          { key: 'NOT_ELIGIBLE', label: 'Not matching' },
        ].map(({ key, label }) => (
          <button
            key={key}
            onClick={() => setFilter(key)}
            className={`px-3.5 py-1.5 rounded-lg text-sm font-medium transition-all cursor-pointer ${
              filter === key
                ? 'bg-primary-700 text-white'
                : 'bg-white border border-surface-200 text-surface-600 hover:bg-surface-50'
            }`}
          >
            {label}
            {statusCounts[key] !== undefined && (
              <span className={`ml-1.5 ${filter === key ? 'text-primary-200' : 'text-surface-400'}`}>
                {statusCounts[key]}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Scheme cards */}
      <div className="space-y-4">
        {filteredSchemes.map((scheme, i) => (
          <SchemeCard
            key={scheme.scheme_id || scheme.source_url || i}
            scheme={scheme}
            eligibility={getEligibility(scheme.scheme_id || scheme.source_url || '')}
          />
        ))}
      </div>

      {filteredSchemes.length === 0 && (
        <div className="text-center py-12 text-surface-500">
          No schemes match the selected filter.
        </div>
      )}
    </div>
  )
}

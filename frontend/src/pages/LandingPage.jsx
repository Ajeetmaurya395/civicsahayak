import { Link } from 'react-router-dom'
import { MessageSquare, Search, Shield, FileText, CheckCircle2, ArrowRight, Sparkles, Globe, Lock } from 'lucide-react'

const features = [
  {
    icon: Search,
    title: 'Live Government Search',
    description: 'Searches official .gov.in sources in real-time — never a stale, pre-built list.',
  },
  {
    icon: Shield,
    title: 'Verified Sources Only',
    description: 'Every scheme comes from a trusted government domain, with the source URL for you to verify.',
  },
  {
    icon: CheckCircle2,
    title: 'Clear Eligibility Checks',
    description: 'See exactly why you match or don\'t — specific criteria, not a vague percentage.',
  },
  {
    icon: FileText,
    title: 'Document Checklist',
    description: 'Know exactly what documents you need and where to apply, before you start.',
  },
  {
    icon: Lock,
    title: 'Privacy First',
    description: 'No Aadhaar, PAN, or bank details stored. Only what\'s needed for matching.',
  },
  {
    icon: Globe,
    title: 'All of India',
    description: 'Central and state schemes, for students, farmers, women, seniors — anyone.',
  },
]

const profiles = [
  '21-year-old student from Uttar Pradesh',
  'Woman entrepreneur in Maharashtra',
  'Farmer in Punjab with 2 acres',
  'Senior citizen in Kerala',
  'Job seeker with disability in Tamil Nadu',
]

export default function LandingPage() {
  return (
    <div className="animate-[fade-in_0.3s_ease-out]">
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-900 via-primary-800 to-primary-950" />
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-20 w-72 h-72 bg-accent-400 rounded-full blur-3xl" />
          <div className="absolute bottom-20 right-20 w-96 h-96 bg-primary-400 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-28 lg:py-36">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm rounded-full px-4 py-1.5 mb-6 border border-white/20">
              <Sparkles className="w-4 h-4 text-accent-400" />
              <span className="text-sm font-medium text-primary-100">AI-powered scheme discovery</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white leading-tight tracking-tight">
              Find government schemes
              <span className="block text-primary-300 mt-1">you're entitled to</span>
            </h1>

            <p className="mt-6 text-lg sm:text-xl text-primary-200 max-w-2xl leading-relaxed">
              Tell us about yourself in plain language. CivicOS searches current government sources,
              checks your eligibility, and explains exactly why you match — or what's missing.
            </p>

            <div className="mt-10 flex flex-wrap gap-4">
              <Link
                to="/chat"
                className="inline-flex items-center gap-2 bg-accent-500 hover:bg-accent-600 text-white px-6 py-3.5 rounded-xl font-semibold text-base shadow-lg hover:shadow-xl transition-all duration-200 no-underline"
              >
                <MessageSquare className="w-5 h-5" />
                Start Finding Schemes
                <ArrowRight className="w-4 h-4" />
              </Link>
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 text-white px-6 py-3.5 rounded-xl font-semibold text-base backdrop-blur-sm border border-white/20 transition-all duration-200 no-underline"
              >
                View on GitHub
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-16 sm:py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-surface-900 tracking-tight">
              How CivicOS works
            </h2>
            <p className="mt-4 text-lg text-surface-500 max-w-2xl mx-auto">
              Three steps — describe yourself, we search, you see results.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 lg:gap-12">
            {[
              { step: '01', title: 'Describe your situation', desc: 'Tell us about yourself — age, state, occupation, income. In plain language, like talking to a friend.' },
              { step: '02', title: 'We search official sources', desc: 'CivicOS searches myscheme.gov.in, state portals, and official departments in real-time.' },
              { step: '03', title: 'See what matches', desc: 'Get clear results showing which schemes match your profile, why, and how to apply.' },
            ].map(({ step, title, desc }) => (
              <div key={step} className="text-center">
                <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-primary-50 text-primary-700 font-bold text-lg mb-5">
                  {step}
                </div>
                <h3 className="text-xl font-semibold text-surface-900 mb-3">{title}</h3>
                <p className="text-surface-500 leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 sm:py-24 bg-surface-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-surface-900 tracking-tight">
              Built different
            </h2>
            <p className="mt-4 text-lg text-surface-500 max-w-2xl mx-auto">
              Not another form. Not another database. A living search engine for government benefits.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8">
            {features.map(({ icon: Icon, title, description }) => (
              <div
                key={title}
                className="bg-white rounded-2xl p-6 border border-surface-200 hover:border-primary-200 hover:shadow-lg transition-all duration-300 group"
              >
                <div className="w-11 h-11 rounded-xl bg-primary-50 group-hover:bg-primary-100 flex items-center justify-center mb-4 transition-colors">
                  <Icon className="w-5 h-5 text-primary-700" />
                </div>
                <h3 className="text-lg font-semibold text-surface-900 mb-2">{title}</h3>
                <p className="text-surface-500 text-sm leading-relaxed">{description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Try it */}
      <section className="py-16 sm:py-24 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-surface-900 tracking-tight mb-4">
            Works for everyone
          </h2>
          <p className="text-lg text-surface-500 mb-10">
            The same system works for any profile — no hardcoded lists, no special cases.
          </p>
          <div className="flex flex-wrap justify-center gap-3">
            {profiles.map((p) => (
              <Link
                key={p}
                to={`/chat?q=${encodeURIComponent(`I am a ${p}`)}`}
                className="bg-surface-100 hover:bg-primary-50 text-surface-700 hover:text-primary-700 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 border border-surface-200 hover:border-primary-200 no-underline"
              >
                {p}
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 sm:py-20 bg-primary-900">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight mb-4">
            Ready to discover your benefits?
          </h2>
          <p className="text-primary-200 text-lg mb-8 max-w-2xl mx-auto">
            It takes less than a minute. Tell us about yourself, and we'll search current government sources to find schemes you may qualify for.
          </p>
          <Link
            to="/chat"
            className="inline-flex items-center gap-2 bg-accent-500 hover:bg-accent-600 text-white px-8 py-4 rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all duration-200 no-underline"
          >
            <MessageSquare className="w-5 h-5" />
            Start Now — It's Free
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-surface-900 text-surface-400 py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5 text-primary-500" />
              <span className="font-semibold text-surface-200">CivicOS</span>
            </div>
            <p className="text-sm text-center sm:text-right">
              Open source • Built with Strands Agents SDK, OpenSearch, Cedar, and AWS technologies
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

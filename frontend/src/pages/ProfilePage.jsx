import { useState } from 'react'
import { User, Save, AlertCircle } from 'lucide-react'

const STATES = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
  'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
  'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
  'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
  'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
  'Delhi', 'Jammu & Kashmir', 'Ladakh',
]

const CATEGORIES = ['General', 'OBC', 'SC', 'ST', 'EWS']

export default function ProfilePage() {
  const [profile, setProfile] = useState({
    age: '',
    gender: '',
    state: '',
    annual_family_income: '',
    occupation: '',
    education_level: '',
    category: '',
    disability: '',
    is_farmer: false,
    is_bpl: false,
  })
  const [saved, setSaved] = useState(false)

  const handleChange = (field, value) => {
    setProfile((prev) => ({ ...prev, [field]: value }))
    setSaved(false)
  }

  const handleSave = () => {
    sessionStorage.setItem('civicos_profile', JSON.stringify(profile))
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  const filledFields = Object.entries(profile).filter(([, v]) => v !== '' && v !== false).length
  const totalFields = Object.keys(profile).length
  const completeness = Math.round((filledFields / totalFields) * 100)

  return (
    <div className="max-w-2xl mx-auto px-4 py-8 animate-[fade-in_0.3s_ease-out]">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
          <User className="w-6 h-6 text-primary-700" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-surface-900">Your Profile</h1>
          <p className="text-surface-500 text-sm">
            The more you share, the better we can match you with schemes.
          </p>
        </div>
      </div>

      {/* Completeness indicator */}
      <div className="bg-white rounded-xl border border-surface-200 p-4 mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-surface-700">Profile completeness</span>
          <span className="text-sm font-semibold text-primary-700">{completeness}%</span>
        </div>
        <div className="w-full h-2 bg-surface-100 rounded-full overflow-hidden">
          <div
            className="h-full bg-primary-600 rounded-full transition-all duration-500"
            style={{ width: `${completeness}%` }}
          />
        </div>
      </div>

      {/* Form */}
      <div className="bg-white rounded-2xl border border-surface-200 p-6 space-y-5">
        {/* Age */}
        <div>
          <label className="block text-sm font-medium text-surface-700 mb-1.5">How old are you?</label>
          <input
            type="number"
            value={profile.age}
            onChange={(e) => handleChange('age', e.target.value)}
            placeholder="e.g., 21"
            className="w-full bg-surface-50 border border-surface-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {/* Gender */}
        <div>
          <label className="block text-sm font-medium text-surface-700 mb-1.5">Gender</label>
          <div className="flex gap-2">
            {['male', 'female', 'other'].map((g) => (
              <button
                key={g}
                onClick={() => handleChange('gender', g)}
                className={`flex-1 py-2.5 rounded-xl text-sm font-medium capitalize transition-all cursor-pointer ${
                  profile.gender === g
                    ? 'bg-primary-700 text-white'
                    : 'bg-surface-50 border border-surface-200 text-surface-600 hover:bg-surface-100'
                }`}
              >
                {g}
              </button>
            ))}
          </div>
        </div>

        {/* State */}
        <div>
          <label className="block text-sm font-medium text-surface-700 mb-1.5">Which state do you live in?</label>
          <select
            value={profile.state}
            onChange={(e) => handleChange('state', e.target.value)}
            className="w-full bg-surface-50 border border-surface-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">Select your state</option>
            {STATES.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        {/* Income */}
        <div>
          <label className="block text-sm font-medium text-surface-700 mb-1.5">
            Your family's yearly income (₹)
          </label>
          <input
            type="number"
            value={profile.annual_family_income}
            onChange={(e) => handleChange('annual_family_income', e.target.value)}
            placeholder="e.g., 250000"
            className="w-full bg-surface-50 border border-surface-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {/* Occupation */}
        <div>
          <label className="block text-sm font-medium text-surface-700 mb-1.5">What do you do?</label>
          <input
            type="text"
            value={profile.occupation}
            onChange={(e) => handleChange('occupation', e.target.value)}
            placeholder="e.g., student, farmer, business owner"
            className="w-full bg-surface-50 border border-surface-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {/* Education */}
        <div>
          <label className="block text-sm font-medium text-surface-700 mb-1.5">Highest education level</label>
          <input
            type="text"
            value={profile.education_level}
            onChange={(e) => handleChange('education_level', e.target.value)}
            placeholder="e.g., 10th pass, BTech, MA"
            className="w-full bg-surface-50 border border-surface-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {/* Category */}
        <div>
          <label className="block text-sm font-medium text-surface-700 mb-1.5">Social category</label>
          <div className="flex flex-wrap gap-2">
            {CATEGORIES.map((c) => (
              <button
                key={c}
                onClick={() => handleChange('category', c)}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition-all cursor-pointer ${
                  profile.category === c
                    ? 'bg-primary-700 text-white'
                    : 'bg-surface-50 border border-surface-200 text-surface-600 hover:bg-surface-100'
                }`}
              >
                {c}
              </button>
            ))}
          </div>
        </div>

        {/* Disability */}
        <div>
          <label className="block text-sm font-medium text-surface-700 mb-1.5">Disability (if any)</label>
          <input
            type="text"
            value={profile.disability}
            onChange={(e) => handleChange('disability', e.target.value)}
            placeholder="Leave blank if not applicable"
            className="w-full bg-surface-50 border border-surface-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {/* Toggles */}
        <div className="flex gap-6">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={profile.is_farmer}
              onChange={(e) => handleChange('is_farmer', e.target.checked)}
              className="w-4 h-4 text-primary-700 rounded"
            />
            <span className="text-sm text-surface-700">I am a farmer</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={profile.is_bpl}
              onChange={(e) => handleChange('is_bpl', e.target.checked)}
              className="w-4 h-4 text-primary-700 rounded"
            />
            <span className="text-sm text-surface-700">BPL card holder</span>
          </label>
        </div>

        {/* Privacy note */}
        <div className="flex items-start gap-2 bg-primary-50 rounded-xl px-4 py-3">
          <AlertCircle className="w-4 h-4 text-primary-600 flex-shrink-0 mt-0.5" />
          <p className="text-xs text-primary-700">
            We only use this information to match you with schemes. No Aadhaar, PAN, or bank details are stored.
            You'll be directed to the official portal for anything sensitive.
          </p>
        </div>

        {/* Save */}
        <button
          onClick={handleSave}
          className={`w-full flex items-center justify-center gap-2 py-3 rounded-xl font-semibold text-sm transition-all cursor-pointer ${
            saved
              ? 'bg-success-600 text-white'
              : 'bg-primary-700 hover:bg-primary-800 text-white'
          }`}
        >
          <Save className="w-4 h-4" />
          {saved ? 'Saved!' : 'Save Profile'}
        </button>
      </div>
    </div>
  )
}

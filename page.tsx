'use client'

import { useEffect, useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import {
  CheckCircle, Clock, Loader, Download, ArrowLeft,
  Copy, Check, Sparkles, Brain, ChevronDown, ChevronUp,
  AlertTriangle, Zap, History
} from 'lucide-react'
import { useI18n, LangSwitcher } from '@/lib/i18n'
import SwarmBrain from '@/components/SwarmBrain'

interface AgentState {
  id: number; name: string; emoji: string; role: string; color: string
  status: 'waiting' | 'active' | 'complete'; output: string
}

const AGENT_DEFS = [
  { id: 1,  emoji: '🎯', name: 'Brand Strategist',         role: 'Positioning & Identity',          color: '#a855f7' },
  { id: 2,  emoji: '🎨', name: 'Creative Director',        role: 'Visual & Creative Concept',        color: '#3b82f6' },
  { id: 3,  emoji: '📱', name: 'Social Media Manager',     role: 'Platform Strategy & Growth',       color: '#06b6d4' },
  { id: 4,  emoji: '🔍', name: 'SEO Specialist',           role: 'Search & Organic Traffic',         color: '#10b981' },
  { id: 5,  emoji: '✍️', name: 'Copywriter',               role: 'Copy, Headlines & CTAs',           color: '#f59e0b' },
  { id: 6,  emoji: '📅', name: 'Editorial Planner',        role: 'Content Calendar & Strategy',      color: '#ef4444' },
  { id: 7,  emoji: '🤖', name: 'Prompt Engineer',          role: 'AI Content Toolkit',               color: '#8b5cf6' },
  { id: 8,  emoji: '📊', name: 'Campaign Manager',         role: 'Paid Media & Channels',            color: '#0ea5e9' },
  { id: 9,  emoji: '📈', name: 'Analytics Specialist',     role: 'KPIs & Performance Tracking',      color: '#14b8a6' },
  { id: 10, emoji: '📝', name: 'Client Report Writer',     role: 'Final Deliverables',               color: '#f97316' },
  { id: 11, emoji: '👑', name: 'COO — Final Review',       role: 'Quality Control & Strategy',       color: '#fbbf24' },
  { id: 13, emoji: '📡', name: 'Trend Scout',              role: 'Trend Analysis & Viral Angles',    color: '#e879f9' },
  { id: 14, emoji: '🎬', name: 'Script & Storyboard',      role: 'Video Scripts & Shot Decks',       color: '#e879f9' },
  { id: 15, emoji: '🖼️', name: 'Visual Producer',          role: 'Art Direction & Image Prompts',    color: '#fb7185' },
  { id: 16, emoji: '♻️', name: 'Content Multiplier',       role: 'Cross-Platform Repurposing',       color: '#fb7185' },
]

const ORCHESTRATOR = { id: 12, emoji: '🧠', name: 'AI Orchestrator', role: 'Master Supervisor', color: '#c084fc' }

const THINKING: Record<number, string[]> = {
  1:  ['Analyzing brand brief...', 'Defining positioning...', 'Building personas...', 'Crafting brand voice...'],
  2:  ['Reviewing brand strategy...', 'Developing creative concept...', 'Designing visual direction...'],
  3:  ['Selecting platforms...', 'Planning content pillars...', 'Building posting schedule...'],
  4:  ['Researching keywords...', 'Mapping content clusters...', 'Planning link strategy...'],
  5:  ['Writing taglines...', 'Crafting ad headlines...', 'Polishing CTAs...'],
  6:  ['Planning content calendar...', 'Structuring blog topics...', 'Building email sequence...'],
  7:  ['Engineering image prompts...', 'Writing AI copy prompts...', 'Building content toolkit...'],
  8:  ['Allocating budget...', 'Structuring Google Ads...', 'Planning Meta campaigns...'],
  9:  ['Setting KPI targets...', 'Configuring tracking plan...', 'Building attribution model...'],
  10: ['Compiling deliverables...', 'Writing executive summary...', 'Formatting client report...'],
  11: ['Reviewing all outputs...', 'Checking strategic coherence...', 'Writing final verdict...'],
  12: ['Processing all 15 outputs...', 'Cross-referencing strategies...', 'Building master synthesis...', 'Calculating success score...', 'Finalizing orchestrator verdict...'],
  13: ['Scanning trending topics...', 'Analyzing viral formats...', 'Mapping cultural moments...', 'Finding competitor gaps...'],
  14: ['Writing hook variations...', 'Structuring shot deck...', 'Adapting for TikTok/Reels...', 'Finalizing video scripts...'],
  15: ['Defining art direction...', 'Building color palette...', 'Engineering DALL-E prompts...', 'Generating visual references...'],
  16: ['Repurposing for Instagram...', 'Writing TikTok pack...', 'Building LinkedIn content...', 'Planning 2-week calendar...'],
}

function renderMarkdown(text: string): string {
  return text
    .replace(/^### (.*$)/gm, '<h3 style="color:#cbd5e1;font-size:12px;font-weight:700;margin:16px 0 6px;text-transform:uppercase;letter-spacing:0.08em;opacity:0.7;">$1</h3>')
    .replace(/^## (.*$)/gm, '<h2 style="color:#f1f5f9;font-size:16px;font-weight:800;margin:20px 0 10px;padding-bottom:6px;border-bottom:1px solid rgba(255,255,255,0.06);">$1</h2>')
    .replace(/^# (.*$)/gm, '<h1 style="color:#f8fafc;font-size:20px;font-weight:900;margin:0 0 12px;">$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, '<strong style="color:#e2e8f0;font-weight:700;">$1</strong>')
    .replace(/\*(.*?)\*/g, '<em style="color:#c084fc;font-style:normal;font-weight:500;">$1</em>')
    .replace(/^- (.*$)/gm, '<div style="display:flex;gap:10px;margin:4px 0;align-items:flex-start;"><span style="color:#7c3aed;flex-shrink:0;margin-top:2px;font-size:10px;">●</span><span style="color:#94a3b8;">$1</span></div>')
    .replace(/^\d+\. (.*$)/gm, '<div style="display:flex;gap:10px;margin:4px 0;align-items:flex-start;padding-left:2px;"><span style="color:#94a3b8;">$1</span></div>')
    .replace(/`([^`]+)`/g, '<code style="background:rgba(139,92,246,0.15);color:#c084fc;padding:2px 7px;border-radius:5px;font-size:12px;font-family:monospace;">$1</code>')
    .replace(/\n\n/g, '<div style="height:12px"></div>')
    .replace(/\n/g, '<br/>')
}

// Extract image prompts from Visual Producer output
function extractImagePrompts(text: string): string[] {
  const prompts: string[] = []
  // Match numbered prompt blocks like "### 1. Hero Brand Image\n[prompt text]"
  const sections = text.split(/###\s*\d+[\.\-]?\s*/g).slice(1)
  for (const s of sections) {
    const lines = s.split('\n').filter(l => l.trim() && !l.startsWith('#'))
    const prompt = lines.slice(0, 3).join(' ').replace(/^\[|\]$/g, '').trim()
    if (prompt.length > 30) prompts.push(prompt.slice(0, 400))
  }
  // Also match lines starting with "Prompt:"
  const promptLines = text.match(/Prompt:\s*([^\n]+)/g)
  if (promptLines) {
    for (const l of promptLines) {
      const p = l.replace(/^Prompt:\s*/, '').trim()
      if (p.length > 30 && !prompts.includes(p)) prompts.push(p.slice(0, 400))
    }
  }
  return prompts.slice(0, 8)
}

interface GeneratedImage { prompt: string; url: string; loading: boolean; error?: string }

function ImageGallery({ agentOutput }: { agentOutput: string }) {
  const prompts = extractImagePrompts(agentOutput)
  const [images, setImages] = useState<GeneratedImage[]>(
    prompts.map(p => ({ prompt: p, url: '', loading: false }))
  )

  const generate = async (idx: number) => {
    setImages(prev => prev.map((img, i) => i === idx ? { ...img, loading: true, error: undefined } : img))
    try {
      const res = await fetch('/api/generate-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: images[idx].prompt, width: 1024, height: 1024 }),
      })
      const data = await res.json()
      setImages(prev => prev.map((img, i) => i === idx ? { ...img, url: data.url || data.base64 || '', loading: false } : img))
    } catch {
      setImages(prev => prev.map((img, i) => i === idx ? { ...img, loading: false, error: 'Errore generazione' } : img))
    }
  }

  const generateAll = () => images.forEach((_, i) => { if (!images[i].url && !images[i].loading) generate(i) })

  if (prompts.length === 0) return null

  return (
    <div style={{ marginTop: '24px', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '20px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '16px' }}>🖼️</span>
          <span style={{ color: 'white', fontWeight: 700, fontSize: '14px' }}>Genera immagini ({prompts.length} prompt)</span>
          <span style={{ fontSize: '10px', color: '#22c55e', background: 'rgba(34,197,94,0.1)', border: '1px solid rgba(34,197,94,0.2)', padding: '2px 8px', borderRadius: '999px', fontWeight: 600 }}>GRATIS</span>
        </div>
        <button onClick={generateAll}
          style={{ padding: '6px 14px', borderRadius: '8px', background: 'linear-gradient(135deg, #7c3aed, #2563eb)', color: 'white', border: 'none', cursor: 'pointer', fontSize: '12px', fontWeight: 600 }}>
          Genera tutte
        </button>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))', gap: '10px' }}>
        {images.map((img, idx) => (
          <div key={idx} style={{ borderRadius: '12px', overflow: 'hidden', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)', aspectRatio: '1', position: 'relative' }}>
            {img.url ? (
              <>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={img.url} alt={img.prompt} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                <a href={img.url} download={`image-${idx + 1}.jpg`} target="_blank" rel="noopener noreferrer"
                  style={{ position: 'absolute', bottom: '6px', right: '6px', background: 'rgba(0,0,0,0.7)', borderRadius: '6px', padding: '4px 8px', color: 'white', fontSize: '10px', textDecoration: 'none', fontWeight: 600 }}>
                  ↓
                </a>
              </>
            ) : (
              <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '8px', padding: '12px', cursor: 'pointer' }}
                onClick={() => !img.loading && generate(idx)}>
                {img.loading ? (
                  <>
                    <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1.2, ease: 'linear' }}
                      style={{ width: '24px', height: '24px', border: '2px solid rgba(124,58,237,0.3)', borderTopColor: '#7c3aed', borderRadius: '50%' }} />
                    <span style={{ color: '#475569', fontSize: '10px' }}>Generando...</span>
                  </>
                ) : (
                  <>
                    <span style={{ fontSize: '22px' }}>🎨</span>
                    <span style={{ color: '#475569', fontSize: '10px', textAlign: 'center', lineHeight: 1.3 }}>
                      {img.prompt.slice(0, 60)}...
                    </span>
                    <span style={{ color: '#7c3aed', fontSize: '10px', fontWeight: 600 }}>Clicca per generare</span>
                    {img.error && <span style={{ color: '#ef4444', fontSize: '9px' }}>{img.error}</span>}
                  </>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function ThinkingDots({ phrase, color = '#7c3aed' }: { phrase: string; color?: string }) {
  return (
    <motion.div key={phrase} initial={{ opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 8 }}
      style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#94a3b8', fontSize: '13px' }}>
      <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
        style={{ width: '14px', height: '14px', border: `2px solid ${color}33`, borderTopColor: color, borderRadius: '50%', flexShrink: 0 }} />
      {phrase}
    </motion.div>
  )
}

export default function RunPage() {
  const router = useRouter()
  const { t } = useI18n()

  // Agents state (1–11) + orchestrator (12)
  const allDefs = [...AGENT_DEFS, ORCHESTRATOR]
  const [agents, setAgents]             = useState<AgentState[]>(allDefs.map(a => ({ ...a, status: 'waiting', output: '' })))
  const [currentAgent, setCurrentAgent] = useState<number | null>(null)
  const [selectedAgent, setSelectedAgent] = useState<number>(1)
  const [done, setDone]                 = useState(false)
  const [clientName, setClientName]     = useState('')
  const [progress, setProgress]         = useState(0)
  const [error, setError]               = useState('')
  const [copiedId, setCopiedId]         = useState<number | null>(null)
  const [phraseIdx, setPhraseIdx]       = useState(0)
  const [expandedAgents, setExpandedAgents] = useState<Set<number>>(new Set([1]))
  const [liveAgents, setLiveAgents] = useState<{ agentId: number; name: string; status: string; collaboratingWith: number[] }[]>([])
  const [agentScores, setAgentScores] = useState<Record<number, number>>({})
  const [visualBrief, setVisualBrief] = useState<string>('')

  // Poll live agent status for swarm visualization
  useEffect(() => {
    const poll = () => {
      fetch('/api/agents/status')
        .then(r => r.ok ? r.json() : { agents: [] })
        .then(data => setLiveAgents(data.agents || []))
        .catch(() => {})
    }
    poll()
    const interval = setInterval(poll, 1500)
    return () => clearInterval(interval)
  }, [])

  const outputRef   = useRef<HTMLDivElement>(null)
  const startedRef  = useRef(false)
  const phraseTimer = useRef<ReturnType<typeof setInterval> | null>(null)

  const TOTAL = allDefs.length // 16 agents + orchestrator
  const completedCount = agents.filter(a => a.status === 'complete').length
  const orchestratorState = agents.find(a => a.id === 12)!
  const selectedState     = agents.find(a => a.id === selectedAgent)
  const selectedDef       = allDefs.find(a => a.id === selectedAgent)
  const currentPhrase     = currentAgent ? (THINKING[currentAgent]?.[phraseIdx % (THINKING[currentAgent]?.length || 1)] || '') : ''
  const isOrchestratorActive = currentAgent === 12

  // Rotate thinking phrases
  useEffect(() => {
    if (currentAgent) {
      setPhraseIdx(0)
      phraseTimer.current = setInterval(() => setPhraseIdx(p => p + 1), 2200)
    }
    return () => { if (phraseTimer.current) clearInterval(phraseTimer.current) }
  }, [currentAgent])

  // Auto-select active agent
  useEffect(() => {
    if (currentAgent) {
      setSelectedAgent(currentAgent)
      setExpandedAgents(prev => new Set([...prev, currentAgent]))
    }
  }, [currentAgent])

  // Auto-scroll
  useEffect(() => {
    if (outputRef.current && currentAgent === selectedAgent) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight
    }
  })

  // Stream runner
  useEffect(() => {
    if (startedRef.current) return
    startedRef.current = true

    const briefStr = localStorage.getItem('dcbr_brief')
    if (!briefStr) { router.push('/'); return }
    const brief = JSON.parse(briefStr)
    setClientName(brief.clientName || 'Client')

    const run = async () => {
      try {
        const res = await fetch('/api/run-agency', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(brief),
        })
        if (!res.ok) throw new Error('API error')
        const reader = res.body!.getReader()
        const decoder = new TextDecoder()
        let buffer = ''

        while (true) {
          const { done: streamDone, value } = await reader.read()
          if (streamDone) break
          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop() || ''

          for (const line of lines) {
            if (!line.startsWith('data: ')) continue
            const data = line.slice(6).trim()
            if (!data) continue
            try {
              const event = JSON.parse(data)
              if (event.type === 'agent_start') {
                setCurrentAgent(event.agentId)
                setAgents(prev => prev.map(a => a.id === event.agentId ? { ...a, status: 'active' } : a))
              } else if (event.type === 'chunk') {
                setAgents(prev => prev.map(a => a.id === event.agentId ? { ...a, output: a.output + event.text } : a))
              } else if (event.type === 'agent_complete') {
                setAgents(prev => prev.map(a => a.id === event.agentId ? { ...a, status: 'complete' } : a))
                setProgress(Math.round((event.agentId / TOTAL) * 100))
                if (event.score) setAgentScores(prev => ({ ...prev, [event.agentId]: event.score }))
              } else if (event.type === 'visual_brief') {
                setVisualBrief(event.brief || '')
              } else if (event.type === 'done') {
                setDone(true)
                setCurrentAgent(null)
                setProgress(100)
                setSelectedAgent(12)
              }
            } catch { /* ignore malformed */ }
          }
        }
      } catch {
        setError(t('run.error'))
      }
    }
    run()
  }, [router, TOTAL, t])

  const copyOutput = (id: number, text: string) => {
    navigator.clipboard.writeText(text)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const downloadAll = async () => {
    const completed = agents.filter(a => a.status === 'complete')
    const { generateCampaignPDF } = await import('@/lib/pdf')
    const doc = generateCampaignPDF(
      clientName,
      completed.map(a => ({ name: a.name, emoji: a.emoji, output: a.output }))
    )
    doc.save(`DCBR-${clientName.replace(/\s+/g, '-')}-Report.pdf`)
  }

  const toggleExpanded = (id: number) => {
    setExpandedAgents(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id); else next.add(id)
      return next
    })
    setSelectedAgent(id)
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', background: '#050a14', overflow: 'hidden' }}>

      {/* Swarm Brain Background */}
      <div style={{ position: 'fixed', inset: 0, pointerEvents: 'none', opacity: 0.4 }}>
        <SwarmBrain height="100%" showLabels={false} interactive={false} liveAgents={liveAgents} overlay="run" />
      </div>
      <div style={{ position: 'fixed', inset: 0, pointerEvents: 'none', background: 'radial-gradient(ellipse at center, rgba(5,10,20,0.3) 20%, #050a14 70%)' }} />

      {/* ── TOP BAR ── */}
      <div style={{ flexShrink: 0, borderBottom: '1px solid rgba(255,255,255,0.05)', background: 'rgba(5,10,20,0.95)', backdropFilter: 'blur(20px)', zIndex: 50, padding: '0 24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px', height: '60px' }}>
          <button onClick={() => router.push('/')}
            style={{ color: '#475569', background: 'none', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', flexShrink: 0, transition: 'color 0.2s' }}
            onMouseEnter={e => (e.currentTarget.style.color = 'white')}
            onMouseLeave={e => (e.currentTarget.style.color = '#475569')}>
            <ArrowLeft size={16} /> {t('nav.back_short')}
          </button>

          <a href="/projects"
            style={{ color: '#475569', display: 'flex', alignItems: 'center', gap: '5px', fontSize: '12px', fontWeight: 600, textDecoration: 'none', flexShrink: 0, padding: '4px 10px', borderRadius: '8px', border: '1px solid rgba(255,255,255,0.07)', transition: 'color 0.2s' }}
            onMouseEnter={e => { (e.currentTarget as HTMLAnchorElement).style.color = 'white'; (e.currentTarget as HTMLAnchorElement).style.borderColor = 'rgba(168,85,247,0.3)' }}
            onMouseLeave={e => { (e.currentTarget as HTMLAnchorElement).style.color = '#475569'; (e.currentTarget as HTMLAnchorElement).style.borderColor = 'rgba(255,255,255,0.07)' }}>
            <History size={13} /> Storico
          </a>

          <div style={{ width: '1px', height: '20px', background: 'rgba(255,255,255,0.07)' }} />

          <div style={{ flexShrink: 0 }}>
            <div style={{ color: 'white', fontWeight: 700, fontSize: '14px' }}>{t('run.agency')}</div>
            <div style={{ color: '#475569', fontSize: '11px' }}>{clientName}</div>
          </div>

          {/* Progress */}
          <div style={{ flex: 1, maxWidth: '500px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
              <AnimatePresence mode="wait">
                {currentAgent ? (
                  <ThinkingDots key={currentPhrase} phrase={currentPhrase} color={isOrchestratorActive ? '#c084fc' : '#7c3aed'} />
                ) : done ? (
                  <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ color: '#22c55e', fontSize: '13px', fontWeight: 600 }}>
                    ✓ {t('run.complete_all')} {TOTAL} {t('run.delivered')}
                  </motion.span>
                ) : (
                  <span style={{ color: '#475569', fontSize: '13px' }}>{t('run.init')}</span>
                )}
              </AnimatePresence>
              <span style={{ color: '#475569', fontSize: '12px', flexShrink: 0, marginLeft: '12px' }}>{completedCount}/{TOTAL}</span>
            </div>
            <div style={{ height: '4px', background: 'rgba(255,255,255,0.05)', borderRadius: '4px', overflow: 'hidden' }}>
              <motion.div animate={{ width: `${progress}%` }} transition={{ duration: 0.6 }}
                style={{ height: '100%', background: 'linear-gradient(90deg, #7c3aed, #2563eb, #c084fc)', borderRadius: '4px' }} />
            </div>
          </div>

          <div style={{ marginLeft: 'auto', flexShrink: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <LangSwitcher />
            {done ? (
              <motion.button initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
                onClick={downloadAll}
                style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 18px', borderRadius: '10px', background: 'linear-gradient(135deg, #7c3aed, #2563eb)', color: 'white', border: 'none', cursor: 'pointer', fontWeight: 600, fontSize: '13px' }}>
                <Download size={15} /> {t('run.download')}
              </motion.button>
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', gap: '7px' }}>
                <motion.div animate={{ scale: [1, 1.3, 1] }} transition={{ repeat: Infinity, duration: 1.5 }}
                  style={{ width: '7px', height: '7px', borderRadius: '50%', background: isOrchestratorActive ? '#c084fc' : '#a855f7' }} />
                <span style={{ color: isOrchestratorActive ? '#c084fc' : '#a855f7', fontSize: '12px', fontWeight: 600 }}>
                  {isOrchestratorActive ? t('run.orchestrator_active') : t('run.working')}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ── MAIN BODY ── */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden', position: 'relative', zIndex: 10 }}>

        {/* ═══ LEFT SIDEBAR ═══ */}
        <div style={{ width: '290px', flexShrink: 0, borderRight: '1px solid rgba(255,255,255,0.05)', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 0 }}>

          {/* ── Orchestrator pyramid card ── */}
          <motion.div
            onClick={() => { setSelectedAgent(12); setExpandedAgents(prev => new Set([...prev, 12])) }}
            whileHover={{ scale: 1.01 }}
            style={{
              margin: '12px 10px 0',
              padding: '16px',
              borderRadius: '16px',
              cursor: 'pointer',
              border: selectedAgent === 12
                ? '1px solid rgba(192,132,252,0.5)'
                : orchestratorState.status === 'active'
                ? '1px solid rgba(192,132,252,0.35)'
                : orchestratorState.status === 'complete'
                ? '1px solid rgba(192,132,252,0.25)'
                : '1px solid rgba(255,255,255,0.07)',
              background: selectedAgent === 12
                ? 'linear-gradient(135deg, rgba(192,132,252,0.12), rgba(124,58,237,0.08))'
                : 'rgba(255,255,255,0.02)',
              boxShadow: orchestratorState.status === 'active' ? '0 0 30px rgba(192,132,252,0.15)' : 'none',
              transition: 'all 0.3s',
              position: 'relative',
              overflow: 'hidden',
            }}>
            {/* Animated glow when active */}
            {orchestratorState.status === 'active' && (
              <motion.div animate={{ opacity: [0.3, 0.7, 0.3] }} transition={{ repeat: Infinity, duration: 2 }}
                style={{ position: 'absolute', inset: 0, background: 'radial-gradient(ellipse at center, rgba(192,132,252,0.08), transparent)', pointerEvents: 'none' }} />
            )}

            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
              <motion.div
                animate={orchestratorState.status === 'active' ? { scale: [1, 1.08, 1] } : {}}
                transition={{ repeat: Infinity, duration: 1.8 }}
                style={{ width: '38px', height: '38px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px', background: 'rgba(192,132,252,0.15)', border: '1px solid rgba(192,132,252,0.35)', flexShrink: 0 }}>
                🧠
              </motion.div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span style={{ color: 'white', fontWeight: 700, fontSize: '13px' }}>AI Orchestratore</span>
                  {orchestratorState.status === 'active' && (
                    <span style={{ fontSize: '9px', fontWeight: 700, color: '#c084fc', background: 'rgba(192,132,252,0.15)', padding: '2px 6px', borderRadius: '999px', border: '1px solid rgba(192,132,252,0.3)' }}>LIVE</span>
                  )}
                  {orchestratorState.status === 'complete' && (
                    <span style={{ fontSize: '9px', fontWeight: 700, color: '#22c55e', background: 'rgba(34,197,94,0.1)', padding: '2px 6px', borderRadius: '999px', border: '1px solid rgba(34,197,94,0.2)' }}>DONE</span>
                  )}
                </div>
                <div style={{ color: '#64748b', fontSize: '11px' }}>Master Supervisor</div>
              </div>
            </div>

            {/* Pyramid progress rings */}
            <div style={{ marginBottom: '8px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                <span style={{ color: '#64748b', fontSize: '11px' }}>{t('run.monitored')}</span>
                <span style={{ color: '#c084fc', fontSize: '11px', fontWeight: 600 }}>{Math.min(completedCount, 11)}/11</span>
              </div>
              <div style={{ height: '3px', background: 'rgba(255,255,255,0.05)', borderRadius: '3px', overflow: 'hidden' }}>
                <motion.div
                  animate={{ width: `${Math.min((Math.min(completedCount, 11) / 11) * 100, 100)}%` }}
                  transition={{ duration: 0.5 }}
                  style={{ height: '100%', background: 'linear-gradient(90deg, #7c3aed, #c084fc)', borderRadius: '3px' }} />
              </div>
            </div>

            {/* Pyramid visual: dots grid */}
            <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap' }}>
              {AGENT_DEFS.map(a => {
                const s = agents.find(ag => ag.id === a.id)?.status || 'waiting'
                return (
                  <motion.div key={a.id}
                    animate={s === 'active' ? { scale: [1, 1.4, 1], opacity: [0.7, 1, 0.7] } : {}}
                    transition={{ repeat: Infinity, duration: 1.5 }}
                    style={{ width: '18px', height: '18px', borderRadius: '5px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '10px',
                      background: s === 'complete' ? 'rgba(34,197,94,0.15)' : s === 'active' ? `${a.color}30` : 'rgba(255,255,255,0.03)',
                      border: `1px solid ${s === 'complete' ? 'rgba(34,197,94,0.3)' : s === 'active' ? `${a.color}60` : 'rgba(255,255,255,0.05)'}`,
                    }}>
                    {s === 'complete' ? '✓' : a.emoji}
                  </motion.div>
                )
              })}
            </div>

            {orchestratorState.status === 'complete' && orchestratorState.output && (
              <div style={{ marginTop: '10px', fontSize: '11px', color: '#c084fc', fontStyle: 'italic' }}>
                {t('run.click_synthesis')}
              </div>
            )}
          </motion.div>

          {/* ── Divider ── */}
          <div style={{ padding: '12px 16px 6px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ flex: 1, height: '1px', background: 'rgba(255,255,255,0.05)' }} />
              <span style={{ color: '#1e293b', fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.1em', flexShrink: 0 }}>{t('run.pipeline')}</span>
              <div style={{ flex: 1, height: '1px', background: 'rgba(255,255,255,0.05)' }} />
            </div>
          </div>

          {/* ── Brand Palette (live after Creative Director) ── */}
          {visualBrief && (() => {
            const colors: { role: string; hex: string; name: string }[] = []
            const lines = visualBrief.split('\n')
            for (const line of lines) {
              const m = line.match(/^(PRIMARY|SECONDARY|ACCENT|BACKGROUND|TEXT):\s*(#[0-9a-fA-F]{3,6})\s*\|\s*([^|]+)/)
              if (m) colors.push({ role: m[1], hex: m[2].trim(), name: m[3].trim() })
            }
            const tone = (visualBrief.match(/^TONE:\s*(.+)$/m) || [])[1] || ''
            const mood = (visualBrief.match(/^MOOD:\s*(.+)$/m) || [])[1] || ''
            if (colors.length === 0) return null
            return (
              <div style={{ margin: '0 10px 8px', padding: '12px', borderRadius: '12px', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
                <div style={{ color: '#475569', fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  🎨 Brand Palette
                  {tone && <span style={{ color: '#7c3aed', background: 'rgba(124,58,237,0.1)', padding: '1px 7px', borderRadius: '999px', textTransform: 'lowercase', letterSpacing: 0 }}>{tone}</span>}
                </div>
                <div style={{ display: 'flex', gap: '4px', marginBottom: '8px' }}>
                  {colors.map(c => (
                    <div key={c.role} title={`${c.role}: ${c.hex} — ${c.name}`}
                      style={{ flex: 1, height: '28px', borderRadius: '7px', background: c.hex, cursor: 'pointer', transition: 'transform 0.15s', border: '1px solid rgba(255,255,255,0.1)' }}
                      onClick={() => navigator.clipboard?.writeText(c.hex)}
                    />
                  ))}
                </div>
                <div style={{ display: 'flex', gap: '3px', flexWrap: 'wrap' }}>
                  {colors.map(c => (
                    <div key={c.role} style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <div style={{ width: '8px', height: '8px', borderRadius: '2px', background: c.hex, flexShrink: 0 }} />
                      <span style={{ color: '#334155', fontSize: '9px', fontFamily: 'monospace' }}>{c.hex}</span>
                    </div>
                  ))}
                </div>
                {mood && <div style={{ color: '#334155', fontSize: '10px', fontStyle: 'italic', marginTop: '6px', lineHeight: 1.4 }}>{mood}</div>}
              </div>
            )
          })()}

          {/* ── Performance Chart (live) ── */}
          {Object.keys(agentScores).length > 0 && (
            <div style={{ margin: '4px 10px 8px', padding: '12px', borderRadius: '12px', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
              <div style={{ color: '#475569', fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '10px' }}>Performance Score</div>
              <svg width="100%" height="60" viewBox={`0 0 260 60`} preserveAspectRatio="none">
                {allDefs.map((def, idx) => {
                  const score = agentScores[def.id] || 0
                  const barH = score > 0 ? Math.max(4, (score / 100) * 50) : 2
                  const x = (idx / allDefs.length) * 260
                  const barW = Math.max(4, 260 / allDefs.length - 3)
                  const color = score >= 90 ? '#22c55e' : score >= 70 ? '#a855f7' : score > 0 ? '#3b82f6' : '#1e293b'
                  return (
                    <g key={def.id}>
                      <rect x={x} y={60 - barH} width={barW} height={barH} fill={color} rx="2" opacity={score > 0 ? 0.9 : 0.3} />
                    </g>
                  )
                })}
              </svg>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '4px' }}>
                <span style={{ color: '#334155', fontSize: '9px' }}>Score</span>
                <span style={{ color: '#475569', fontSize: '9px', fontWeight: 600 }}>
                  {Object.keys(agentScores).length}/{TOTAL} completati
                </span>
              </div>
            </div>
          )}

          {/* ── Agent list ── */}
          <div style={{ padding: '0 10px 12px', display: 'flex', flexDirection: 'column', gap: '3px' }}>
            {AGENT_DEFS.map(def => {
              const agent   = agents.find(a => a.id === def.id)!
              const isActive   = agent.status === 'active'
              const isComplete = agent.status === 'complete'
              const isSelected = selectedAgent === def.id
              const isExpanded = expandedAgents.has(def.id)

              return (
                <div key={def.id}>
                  <motion.button
                    onClick={() => toggleExpanded(def.id)}
                    initial={{ opacity: 0, x: -12 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: def.id * 0.03 }}
                    style={{
                      display: 'flex', alignItems: 'center', gap: '10px',
                      padding: '9px 10px', borderRadius: '11px', border: 'none', cursor: 'pointer',
                      textAlign: 'left', width: '100%', transition: 'all 0.2s',
                      background: isSelected
                        ? `linear-gradient(135deg, ${def.color}18, rgba(13,21,38,0.8))`
                        : 'transparent',
                      outline: isSelected ? `1px solid ${def.color}30` : '1px solid transparent',
                      boxShadow: isActive ? `0 0 16px ${def.color}20` : 'none',
                    }}>

                    {/* Emoji icon */}
                    <div style={{ position: 'relative', flexShrink: 0 }}>
                      <div style={{ width: '32px', height: '32px', borderRadius: '9px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '15px',
                        background: isActive ? `${def.color}22` : isComplete ? `${def.color}12` : 'rgba(255,255,255,0.03)',
                        border: `1px solid ${isActive ? def.color + '55' : isComplete ? def.color + '25' : 'rgba(255,255,255,0.05)'}`,
                        transition: 'all 0.3s',
                      }}>
                        {def.emoji}
                      </div>
                      {isActive && (
                        <motion.div animate={{ scale: [1, 1.5, 1], opacity: [0.5, 0, 0.5] }} transition={{ repeat: Infinity, duration: 1.5 }}
                          style={{ position: 'absolute', inset: '-3px', borderRadius: '12px', border: `1px solid ${def.color}`, pointerEvents: 'none' }} />
                      )}
                    </div>

                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ color: isActive || isComplete ? 'white' : '#475569', fontWeight: 600, fontSize: '12px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {def.name}
                      </div>
                      <div style={{ fontSize: '10px', color: isActive ? '#94a3b8' : isComplete ? '#22c55e44' : '#1e293b', marginTop: '1px' }}>
                        {isComplete ? `✓ ${agent.output.split(' ').length} ${t('run.words')}` : isActive ? t('run.processing') : t('run.in_wait')}
                      </div>
                    </div>

                    <div style={{ flexShrink: 0, display: 'flex', alignItems: 'center', gap: '4px' }}>
                      {isComplete && <CheckCircle size={13} color="#22c55e" />}
                      {isActive && <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}><Loader size={13} color={def.color} /></motion.div>}
                      {agent.status === 'waiting' && <Clock size={12} color="#1e293b" />}
                      {isComplete && (isExpanded ? <ChevronUp size={11} color="#334155" /> : <ChevronDown size={11} color="#334155" />)}
                    </div>
                  </motion.button>

                  {/* Inline preview (collapsed output snippet) */}
                  <AnimatePresence>
                    {isExpanded && isComplete && agent.output && (
                      <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}
                        style={{ overflow: 'hidden', marginLeft: '10px', marginRight: '10px' }}>
                        <div onClick={() => setSelectedAgent(def.id)} style={{ padding: '8px 12px', margin: '2px 0 4px', borderRadius: '8px', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.04)', cursor: 'pointer' }}
                          onMouseEnter={e => (e.currentTarget.style.background = 'rgba(255,255,255,0.04)')}
                          onMouseLeave={e => (e.currentTarget.style.background = 'rgba(255,255,255,0.02)')}>
                          <div style={{ color: '#64748b', fontSize: '11px', lineHeight: 1.5, overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: '3', WebkitBoxOrient: 'vertical' as const }}>
                            {agent.output.replace(/[#*`]/g, '').slice(0, 160)}...
                          </div>
                          <div style={{ color: def.color, fontSize: '10px', marginTop: '4px', fontWeight: 600 }}>{t('run.read_all')}</div>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              )
            })}
          </div>
        </div>

        {/* ═══ RIGHT PANEL ═══ */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>

          {/* Panel header */}
          {selectedState && selectedDef && (
            <div style={{ flexShrink: 0, padding: '16px 24px', borderBottom: '1px solid rgba(255,255,255,0.05)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: 'rgba(5,10,20,0.6)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <motion.div
                  animate={selectedState.status === 'active' ? { boxShadow: [`0 0 0px ${selectedDef.color}00`, `0 0 24px ${selectedDef.color}50`, `0 0 0px ${selectedDef.color}00`] } : {}}
                  transition={{ repeat: Infinity, duration: 2 }}
                  style={{ width: '44px', height: '44px', borderRadius: '13px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '22px', flexShrink: 0, background: `${selectedDef.color}18`, border: `1px solid ${selectedDef.color}35` }}>
                  {selectedDef.emoji}
                </motion.div>
                <div>
                  <div style={{ color: 'white', fontWeight: 700, fontSize: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    {selectedDef.name}
                    {selectedState.status === 'active' && (
                      <motion.span animate={{ opacity: [1, 0.5, 1] }} transition={{ repeat: Infinity, duration: 1 }}
                        style={{ fontSize: '10px', fontWeight: 600, color: selectedDef.color, background: `${selectedDef.color}15`, padding: '2px 8px', borderRadius: '999px', border: `1px solid ${selectedDef.color}30` }}>
                        LIVE
                      </motion.span>
                    )}
                    {selectedState.status === 'complete' && (
                      <span style={{ fontSize: '10px', fontWeight: 600, color: '#22c55e', background: 'rgba(34,197,94,0.1)', padding: '2px 8px', borderRadius: '999px', border: '1px solid rgba(34,197,94,0.2)' }}>
                        COMPLETATO
                      </span>
                    )}
                  </div>
                  <div style={{ color: '#64748b', fontSize: '12px' }}>{selectedDef.role}</div>
                </div>
              </div>

              {selectedState.status === 'complete' && (
                <button onClick={() => copyOutput(selectedAgent, selectedState.output)}
                  style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '7px 14px', borderRadius: '9px', background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.08)', color: '#94a3b8', cursor: 'pointer', fontSize: '12px', fontWeight: 500, transition: 'all 0.2s' }}
                  onMouseEnter={e => (e.currentTarget.style.background = 'rgba(255,255,255,0.08)')}
                  onMouseLeave={e => (e.currentTarget.style.background = 'rgba(255,255,255,0.04)')}>
                  {copiedId === selectedAgent ? <><Check size={13} color="#22c55e" /><span style={{ color: '#22c55e' }}>{t('run.copied')}</span></> : <><Copy size={13} />{t('run.copy')}</>}
                </button>
              )}
            </div>
          )}

          {/* Output area */}
          <div ref={outputRef} style={{ flex: 1, overflowY: 'auto', padding: '28px 36px' }}>
            {error && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '16px 20px', borderRadius: '12px', background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.2)', color: '#f87171', marginBottom: '20px', fontSize: '14px' }}>
                <AlertTriangle size={18} />{error}
              </div>
            )}

            {/* Done banner */}
            <AnimatePresence>
              {done && (
                <motion.div initial={{ opacity: 0, y: -12 }} animate={{ opacity: 1, y: 0 }}
                  style={{ padding: '20px 24px', borderRadius: '16px', marginBottom: '24px', background: 'linear-gradient(135deg, rgba(192,132,252,0.1), rgba(124,58,237,0.1), rgba(37,99,235,0.08))', border: '1px solid rgba(192,132,252,0.25)', display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <div style={{ fontSize: '28px' }}>🎉</div>
                  <div>
                    <div style={{ color: 'white', fontWeight: 700, fontSize: '16px', marginBottom: '3px' }}>{t('run.complete')}</div>
                    <div style={{ color: '#94a3b8', fontSize: '13px' }}>12 {t('run.complete_desc')} <strong style={{ color: 'white' }}>{clientName}</strong>. {t('run.orchestrator_verdict')}</div>
                  </div>
                  <div style={{ marginLeft: 'auto', display: 'flex', gap: '8px', flexShrink: 0 }}>
                    <button onClick={() => setSelectedAgent(12)}
                      style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 14px', borderRadius: '10px', background: 'rgba(192,132,252,0.15)', border: '1px solid rgba(192,132,252,0.3)', color: '#c084fc', cursor: 'pointer', fontWeight: 600, fontSize: '12px' }}>
                      <Brain size={14} />{t('run.synthesis')}
                    </button>
                    <button onClick={downloadAll}
                      style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 14px', borderRadius: '10px', background: 'linear-gradient(135deg, #7c3aed, #2563eb)', color: 'white', border: 'none', cursor: 'pointer', fontWeight: 600, fontSize: '12px' }}>
                      <Download size={13} />{t('run.download_all')}
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Selected agent output */}
            {selectedState && (
              <>
                {selectedState.status === 'waiting' && (
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', paddingTop: '80px', gap: '16px', opacity: 0.4 }}>
                    <Clock size={36} color="#334155" />
                    <div style={{ color: '#334155', fontSize: '14px', textAlign: 'center' }}>{t('run.waiting')}</div>
                  </div>
                )}

                {selectedState.status === 'active' && selectedState.output === '' && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#64748b', fontSize: '14px' }}>
                    <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
                      style={{ width: '16px', height: '16px', border: `2px solid ${selectedDef?.color}33`, borderTopColor: selectedDef?.color, borderRadius: '50%' }} />
                    {t('run.starting')}
                  </div>
                )}

                {selectedState.output && (
                  <>
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                      style={{ fontFamily: "'Inter', sans-serif", fontSize: '14px', lineHeight: 1.8, color: '#94a3b8', maxWidth: '760px' }}
                      dangerouslySetInnerHTML={{
                        __html: renderMarkdown(selectedState.output) + (selectedState.status === 'active' ? '<span style="display:inline-block;width:2px;height:14px;background:#7c3aed;margin-left:2px;animation:blink 1s infinite;vertical-align:middle;border-radius:1px;"></span>' : '')
                      }}
                    />
                    {/* Image generator — available for Visual Producer and Prompt Engineer */}
                    {(selectedAgent === 15 || selectedAgent === 7) && selectedState.status === 'complete' && (
                      <ImageGallery agentOutput={selectedState.output} />
                    )}
                  </>
                )}
              </>
            )}
          </div>

          {/* Bottom emoji quick-nav */}
          <div style={{ flexShrink: 0, borderTop: '1px solid rgba(255,255,255,0.05)', padding: '8px 16px', display: 'flex', gap: '5px', overflowX: 'auto', background: 'rgba(5,10,20,0.6)', alignItems: 'center' }}>
            {/* Orchestrator at start */}
            <button onClick={() => setSelectedAgent(12)} title="AI Orchestratore"
              style={{ flexShrink: 0, width: '32px', height: '32px', borderRadius: '9px', border: 'none', cursor: 'pointer', fontSize: '15px', display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: selectedAgent === 12 ? 'rgba(192,132,252,0.22)' : orchestratorState.status === 'complete' ? 'rgba(34,197,94,0.06)' : 'rgba(255,255,255,0.02)',
                outline: selectedAgent === 12 ? '1.5px solid rgba(192,132,252,0.5)' : '1.5px solid transparent',
                opacity: orchestratorState.status === 'waiting' ? 0.3 : 1, transition: 'all 0.15s',
                boxShadow: orchestratorState.status === 'active' ? '0 0 14px rgba(192,132,252,0.4)' : 'none',
              }}>🧠</button>

            <div style={{ width: '1px', height: '20px', background: 'rgba(255,255,255,0.06)', flexShrink: 0 }} />

            {AGENT_DEFS.map(a => {
              const ag = agents.find(x => x.id === a.id)!
              return (
                <button key={a.id} onClick={() => setSelectedAgent(a.id)} title={a.name}
                  style={{ flexShrink: 0, width: '32px', height: '32px', borderRadius: '8px', border: 'none', cursor: 'pointer', fontSize: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center',
                    background: selectedAgent === a.id ? `${a.color}22` : ag.status === 'complete' ? 'rgba(34,197,94,0.05)' : 'rgba(255,255,255,0.02)',
                    outline: selectedAgent === a.id ? `1.5px solid ${a.color}50` : '1.5px solid transparent',
                    opacity: ag.status === 'waiting' ? 0.3 : 1, transition: 'all 0.15s',
                    boxShadow: ag.status === 'active' ? `0 0 10px ${a.color}40` : 'none',
                  }}>
                  {a.emoji}
                </button>
              )
            })}

            {/* Stats badge */}
            <div style={{ marginLeft: 'auto', flexShrink: 0, display: 'flex', alignItems: 'center', gap: '5px', padding: '4px 10px', borderRadius: '999px', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
              {done
                ? <><Sparkles size={11} color="#22c55e" /><span style={{ color: '#22c55e', fontSize: '11px', fontWeight: 600 }}>Completo</span></>
                : <><Zap size={11} color="#a855f7" /><span style={{ color: '#64748b', fontSize: '11px' }}>{completedCount}/{TOTAL}</span></>}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

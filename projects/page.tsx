'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import {
  ArrowLeft, Brain, Clock, Star, BarChart3, ChevronDown, ChevronUp,
  Play, FileText, Zap, X, BookOpen, TrendingUp, Users
} from 'lucide-react'
import { useI18n, LangSwitcher } from '@/lib/i18n'

interface AgentMemory {
  agent_id: number
  agent_name: string
  output_summary: string
  learnings: string
  performance_score: number
  word_count: number
  created_at: string
}

interface Project {
  project_name: string
  agents_done: number
  last_run: string
  avg_score: number
  total_words: number
  agent_names: string
  brief_summary: string
  all_learnings: string
  agents: AgentMemory[]
  content: { id: string; type: string; title: string; data: string; created_at: string } | null
}

const TOTAL_AGENTS = 16

const AGENT_COLORS: Record<number, string> = {
  1: '#f472b6', 2: '#f472b6', 3: '#f472b6',
  4: '#06b6d4', 5: '#06b6d4', 6: '#06b6d4',
  7: '#818cf8', 8: '#f59e0b', 9: '#f59e0b',
  10: '#10b981', 11: '#10b981', 12: '#a855f7',
  13: '#e879f9', 14: '#e879f9', 15: '#fb7185', 16: '#fb7185',
}

function ScoreBadge({ score }: { score: number }) {
  const color = score >= 80 ? '#22c55e' : score >= 60 ? '#f59e0b' : '#ef4444'
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '4px', padding: '3px 10px', borderRadius: '999px', background: `${color}12`, border: `1px solid ${color}30` }}>
      <Star size={11} color={color} />
      <span style={{ color, fontSize: '11px', fontWeight: 700 }}>{Math.round(score)}</span>
    </div>
  )
}

export default function ProjectsPage() {
  const router = useRouter()
  const { t } = useI18n()
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [expanded, setExpanded] = useState<string | null>(null)
  const [selectedAgent, setSelectedAgent] = useState<AgentMemory | null>(null)

  useEffect(() => {
    fetch('/api/projects')
      .then(r => r.ok ? r.json() : [])
      .then(data => {
        // Sort: incomplete first, then by date desc
        const sorted = [...data].sort((a: Project, b: Project) => {
          const aIncomplete = a.agents_done < TOTAL_AGENTS
          const bIncomplete = b.agents_done < TOTAL_AGENTS
          if (aIncomplete && !bIncomplete) return -1
          if (!aIncomplete && bIncomplete) return 1
          return new Date(b.last_run).getTime() - new Date(a.last_run).getTime()
        })
        setProjects(sorted)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const resumeProject = (project: Project) => {
    // Extract client name and brief from brief_summary
    // Format is: "clientName — industry — brief text"
    const parts = project.brief_summary?.split(' — ') || []
    const clientName = parts[0] || project.project_name
    const industry = parts[1] || ''
    const brief = parts.slice(2).join(' — ') || project.brief_summary || ''

    const savedBrief = {
      clientName,
      industry,
      brief,
      audience: '',
      website: '',
      budget: '',
      goals: '',
    }

    localStorage.setItem('dcbr_brief', JSON.stringify(savedBrief))
    router.push('/run')
  }

  const totalProjects = projects.length
  const totalWords = projects.reduce((s, p) => s + p.total_words, 0)
  const globalAvgScore = projects.length > 0
    ? Math.round(projects.reduce((s, p) => s + p.avg_score, 0) / projects.length)
    : 0

  return (
    <div style={{ minHeight: '100vh', background: '#050a14' }}>
      <div style={{ position: 'fixed', inset: 0, pointerEvents: 'none' }}>
        <div style={{ position: 'absolute', top: '-10%', left: '-5%', width: '500px', height: '500px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(168,85,247,0.06), transparent)', filter: 'blur(80px)' }} />
        <div style={{ position: 'absolute', bottom: '-10%', right: '-5%', width: '400px', height: '400px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(59,130,246,0.05), transparent)', filter: 'blur(80px)' }} />
      </div>

      {/* Nav */}
      <nav style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', background: 'rgba(5,10,20,0.95)', backdropFilter: 'blur(20px)', position: 'sticky', top: 0, zIndex: 50, padding: '0 24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', height: '60px', maxWidth: '1000px', margin: '0 auto' }}>
          <a href="/dashboard" style={{ color: '#475569', display: 'flex', alignItems: 'center', textDecoration: 'none' }}><ArrowLeft size={16} /></a>
          <div style={{ width: '1px', height: '20px', background: 'rgba(255,255,255,0.07)' }} />
          <BookOpen size={18} color="#a855f7" />
          <div>
            <span style={{ color: 'white', fontWeight: 800, fontSize: '15px' }}>Storico Progetti</span>
            <div style={{ color: '#475569', fontSize: '11px' }}>Memoria & Resume</div>
          </div>
          <div style={{ marginLeft: 'auto', display: 'flex', gap: '20px', alignItems: 'center' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ color: '#a855f7', fontWeight: 800, fontSize: '16px' }}>{totalProjects}</div>
              <div style={{ color: '#334155', fontSize: '9px', fontWeight: 600 }}>PROGETTI</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ color: '#22c55e', fontWeight: 800, fontSize: '16px' }}>{totalWords > 1000 ? `${(totalWords / 1000).toFixed(1)}k` : totalWords}</div>
              <div style={{ color: '#334155', fontSize: '9px', fontWeight: 600 }}>PAROLE</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ color: globalAvgScore >= 80 ? '#22c55e' : '#f59e0b', fontWeight: 800, fontSize: '16px' }}>{globalAvgScore || '—'}</div>
              <div style={{ color: '#334155', fontSize: '9px', fontWeight: 600 }}>SCORE</div>
            </div>
            <div style={{ width: '1px', height: '24px', background: 'rgba(255,255,255,0.06)' }} />
            <LangSwitcher />
          </div>
        </div>
      </nav>

      <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '32px 24px 80px', position: 'relative', zIndex: 10 }}>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '80px 0', color: '#334155' }}>
            <Brain size={32} style={{ margin: '0 auto 12px', opacity: 0.3 }} />
            <div style={{ fontSize: '14px' }}>Caricamento memoria...</div>
          </div>
        ) : projects.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '80px 0' }}>
            <Brain size={40} color="#1e293b" style={{ margin: '0 auto 16px' }} />
            <div style={{ color: '#334155', fontSize: '16px', fontWeight: 600, marginBottom: '8px' }}>Nessun progetto in memoria</div>
            <div style={{ color: '#1e293b', fontSize: '13px', marginBottom: '24px' }}>Lancia la prima campagna per iniziare ad accumulare memoria</div>
            <a href="/" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '12px 24px', borderRadius: '12px', background: 'linear-gradient(135deg, #7c3aed, #2563eb)', color: 'white', textDecoration: 'none', fontWeight: 700, fontSize: '14px' }}>
              <Zap size={16} /> Prima Campagna
            </a>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {projects.map((project, idx) => {
              const isExpanded = expanded === project.project_name
              const isIncomplete = project.agents_done < TOTAL_AGENTS
              const completionPct = Math.round((project.agents_done / TOTAL_AGENTS) * 100)

              return (
                <motion.div key={project.project_name} layout initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: idx * 0.05 }}
                  style={{ borderRadius: '18px', border: `1px solid ${isExpanded ? 'rgba(168,85,247,0.3)' : isIncomplete ? 'rgba(245,158,11,0.2)' : 'rgba(255,255,255,0.06)'}`, background: isExpanded ? 'rgba(168,85,247,0.04)' : isIncomplete ? 'rgba(245,158,11,0.02)' : 'rgba(255,255,255,0.02)', overflow: 'hidden', transition: 'border-color 0.2s' }}>

                  {/* Incomplete progress bar at top */}
                  {isIncomplete && (
                    <div style={{ height: '3px', background: 'rgba(255,255,255,0.04)' }}>
                      <div style={{ height: '100%', width: `${completionPct}%`, background: 'linear-gradient(90deg, #f59e0b, #f97316)', borderRadius: '0 2px 2px 0', transition: 'width 0.5s' }} />
                    </div>
                  )}

                  {/* Project header */}
                  <div
                    onClick={() => setExpanded(isExpanded ? null : project.project_name)}
                    style={{ padding: '20px 24px', display: 'flex', alignItems: 'center', gap: '16px', cursor: 'pointer' }}>

                    {/* Icon */}
                    <div style={{ width: 36, height: 36, borderRadius: '10px', background: isIncomplete ? 'rgba(245,158,11,0.12)' : 'rgba(168,85,247,0.12)', border: `1px solid ${isIncomplete ? 'rgba(245,158,11,0.25)' : 'rgba(168,85,247,0.2)'}`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, color: isIncomplete ? '#f59e0b' : '#a855f7', fontWeight: 900, fontSize: '15px' }}>
                      {isIncomplete ? '⏸' : idx + 1}
                    </div>

                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '4px', flexWrap: 'wrap' }}>
                        <span style={{ color: 'white', fontWeight: 800, fontSize: '16px' }}>{project.project_name}</span>
                        {isIncomplete ? (
                          <span style={{ fontSize: '10px', fontWeight: 700, color: '#f59e0b', background: 'rgba(245,158,11,0.12)', border: '1px solid rgba(245,158,11,0.25)', padding: '2px 8px', borderRadius: '999px' }}>
                            Incompleto — {project.agents_done}/{TOTAL_AGENTS} agenti
                          </span>
                        ) : (
                          <ScoreBadge score={project.avg_score} />
                        )}
                      </div>
                      <div style={{ color: '#475569', fontSize: '12px', display: 'flex', gap: '14px', flexWrap: 'wrap' }}>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <Users size={10} /> {project.agents_done} agenti completati
                        </span>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <BarChart3 size={10} /> {project.total_words > 1000 ? `${(project.total_words / 1000).toFixed(1)}k` : project.total_words} parole
                        </span>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <Clock size={10} /> {new Date(project.last_run).toLocaleDateString('it-IT', { day: '2-digit', month: 'short', year: 'numeric' })}
                        </span>
                      </div>
                    </div>

                    {/* Actions */}
                    <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }} onClick={e => e.stopPropagation()}>
                      <motion.button
                        whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
                        onClick={() => resumeProject(project)}
                        style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '8px 16px', borderRadius: '10px', background: isIncomplete ? 'linear-gradient(135deg, #f59e0b, #f97316)' : 'linear-gradient(135deg, #7c3aed, #2563eb)', border: 'none', color: 'white', fontSize: '12px', fontWeight: 700, cursor: 'pointer', boxShadow: isIncomplete ? '0 4px 16px rgba(245,158,11,0.3)' : '0 4px 16px rgba(124,58,237,0.3)' }}>
                        <Play size={13} fill="white" /> {isIncomplete ? 'Riprendi' : 'Riesegui'}
                      </motion.button>
                    </div>

                    <div style={{ color: '#334155', flexShrink: 0 }}>
                      {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                    </div>
                  </div>

                  {/* Expanded content */}
                  <AnimatePresence>
                    {isExpanded && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        style={{ overflow: 'hidden' }}>
                        <div style={{ borderTop: '1px solid rgba(255,255,255,0.05)', padding: '20px 24px', display: 'flex', gap: '20px', flexWrap: 'wrap' }}>

                          {/* Brief summary */}
                          {project.brief_summary && (
                            <div style={{ flex: '1 1 280px', padding: '14px 18px', borderRadius: '12px', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
                              <div style={{ color: '#64748b', fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '8px' }}>Brief</div>
                              <div style={{ color: '#94a3b8', fontSize: '12px', lineHeight: 1.7 }}>{project.brief_summary}</div>
                            </div>
                          )}

                          {/* Performance bar chart */}
                          <div style={{ flex: '1 1 300px', padding: '14px 18px', borderRadius: '12px', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
                            <div style={{ color: '#64748b', fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                              <TrendingUp size={12} color="#a855f7" /> Performance Agenti
                            </div>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                              {project.agents.map(agent => (
                                <div key={agent.agent_id}
                                  onClick={() => setSelectedAgent(selectedAgent?.agent_id === agent.agent_id ? null : agent)}
                                  style={{ cursor: 'pointer' }}>
                                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '3px' }}>
                                    <span style={{ color: '#64748b', fontSize: '10px' }}>{agent.agent_name}</span>
                                    <span style={{ color: AGENT_COLORS[agent.agent_id] || '#a855f7', fontSize: '10px', fontWeight: 700 }}>{agent.performance_score}</span>
                                  </div>
                                  <div style={{ height: '4px', borderRadius: '2px', background: 'rgba(255,255,255,0.05)', overflow: 'hidden' }}>
                                    <motion.div
                                      initial={{ width: 0 }}
                                      animate={{ width: `${agent.performance_score}%` }}
                                      transition={{ duration: 0.6, delay: 0.1 }}
                                      style={{ height: '100%', borderRadius: '2px', background: `linear-gradient(90deg, ${AGENT_COLORS[agent.agent_id] || '#a855f7'}40, ${AGENT_COLORS[agent.agent_id] || '#a855f7'})` }}
                                    />
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>

                        {/* Agent memory detail panel */}
                        <AnimatePresence>
                          {selectedAgent && project.agents.find(a => a.agent_id === selectedAgent.agent_id) && (
                            <motion.div
                              initial={{ opacity: 0, height: 0 }}
                              animate={{ opacity: 1, height: 'auto' }}
                              exit={{ opacity: 0, height: 0 }}
                              style={{ overflow: 'hidden', padding: '0 24px 20px' }}>
                              <div style={{ padding: '16px 20px', borderRadius: '14px', background: `${AGENT_COLORS[selectedAgent.agent_id] || '#a855f7'}08`, border: `1px solid ${AGENT_COLORS[selectedAgent.agent_id] || '#a855f7'}20` }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                                  <div style={{ color: AGENT_COLORS[selectedAgent.agent_id] || '#a855f7', fontWeight: 700, fontSize: '13px' }}>{selectedAgent.agent_name}</div>
                                  <button onClick={() => setSelectedAgent(null)} style={{ background: 'none', border: 'none', color: '#475569', cursor: 'pointer' }}><X size={14} /></button>
                                </div>
                                {selectedAgent.output_summary && (
                                  <div style={{ marginBottom: '10px' }}>
                                    <div style={{ color: '#475569', fontSize: '10px', fontWeight: 600, textTransform: 'uppercase', marginBottom: '4px' }}>Output</div>
                                    <div style={{ color: '#94a3b8', fontSize: '12px', lineHeight: 1.7 }}>{selectedAgent.output_summary}</div>
                                  </div>
                                )}
                                {selectedAgent.learnings && (
                                  <div>
                                    <div style={{ color: '#475569', fontSize: '10px', fontWeight: 600, textTransform: 'uppercase', marginBottom: '4px' }}>Learnings</div>
                                    <div style={{ color: '#64748b', fontSize: '11px', lineHeight: 1.7 }}>{selectedAgent.learnings}</div>
                                  </div>
                                )}
                                <div style={{ marginTop: '10px', display: 'flex', gap: '12px', color: '#334155', fontSize: '10px' }}>
                                  <span>{selectedAgent.word_count} parole</span>
                                  <span>{new Date(selectedAgent.created_at).toLocaleString('it-IT')}</span>
                                </div>
                              </div>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </motion.div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

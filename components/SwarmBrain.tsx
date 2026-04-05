'use client'

import { useEffect, useRef, useCallback, useState } from 'react'

interface SwarmNode {
  id: number
  x: number
  y: number
  vx: number
  vy: number
  radius: number
  color: string
  emoji: string
  name: string
  category: string
  active: boolean
  searchQuery: string | null
  dataPoints: { x: number; y: number; age: number; text: string }[]
}

interface LiveAgent {
  agentId: number
  name: string
  status: string
  collaboratingWith: number[]
}

interface Props {
  height?: string
  showLabels?: boolean
  interactive?: boolean
  liveAgents?: LiveAgent[]
  overlay?: 'hero' | 'run' | 'none'
}

const AGENT_DEFS = [
  { id: 0,  emoji: '🧠', name: 'JARVIS',              color: '#a855f7', category: 'core' },
  { id: 1,  emoji: '🎯', name: 'Brand Strategist',     color: '#f472b6', category: 'marketing' },
  { id: 2,  emoji: '🎨', name: 'Creative Director',    color: '#f472b6', category: 'marketing' },
  { id: 3,  emoji: '📱', name: 'Social Media',         color: '#f472b6', category: 'marketing' },
  { id: 4,  emoji: '🔍', name: 'SEO Specialist',       color: '#06b6d4', category: 'growth' },
  { id: 5,  emoji: '✍️', name: 'Copywriter',            color: '#06b6d4', category: 'growth' },
  { id: 6,  emoji: '📅', name: 'Editorial Planner',    color: '#06b6d4', category: 'growth' },
  { id: 7,  emoji: '⚙️', name: 'Prompt Engineer',       color: '#818cf8', category: 'tech' },
  { id: 8,  emoji: '📣', name: 'Campaign Manager',     color: '#f59e0b', category: 'strategy' },
  { id: 9,  emoji: '📊', name: 'Analytics',            color: '#f59e0b', category: 'strategy' },
  { id: 10, emoji: '📝', name: 'Report Writer',        color: '#10b981', category: 'delivery' },
  { id: 11, emoji: '👔', name: 'COO Review',           color: '#10b981', category: 'delivery' },
  { id: 12, emoji: '🤖', name: 'Orchestrator',         color: '#a855f7', category: 'core' },
  { id: 13, emoji: '📡', name: 'Trend Scout',          color: '#e879f9', category: 'koda' },
  { id: 14, emoji: '🎬', name: 'Script Writer',        color: '#e879f9', category: 'koda' },
  { id: 15, emoji: '🖼️', name: 'Visual Producer',      color: '#fb7185', category: 'koda' },
  { id: 16, emoji: '♻️', name: 'Content Multiplier',   color: '#fb7185', category: 'koda' },
]

// Neural connections
const CONNECTIONS: [number, number][] = [
  [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12],
  [0, 13], [0, 14], [0, 15], [0, 16],
  [1, 2], [1, 5], [1, 13], [2, 3], [2, 10], [2, 15], [3, 6], [3, 14], [3, 16],
  [4, 5], [4, 6], [5, 8], [6, 8], [7, 5], [7, 3], [7, 15],
  [8, 9], [9, 10], [10, 11], [11, 12], [12, 0],
  [13, 14], [14, 15], [15, 16], [16, 12],
]

export default function SwarmBrain({ height = '100%', showLabels = true, interactive = true, liveAgents = [], overlay = 'none' }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const nodesRef = useRef<SwarmNode[]>([])
  const particlesRef = useRef<{ x: number; y: number; vx: number; vy: number; life: number; color: string; fromId: number; toId: number }[]>([])
  const animRef = useRef<number>(0)
  const mouseRef = useRef<{ x: number; y: number; active: boolean }>({ x: 0, y: 0, active: false })
  const phaseRef = useRef(0)
  const [hovered, setHovered] = useState<number | null>(null)

  const initNodes = useCallback((w: number, h: number) => {
    const cx = w / 2
    const cy = h / 2
    const baseRadius = Math.min(w, h) * (overlay === 'hero' ? 0.3 : 0.35)

    const nodes: SwarmNode[] = AGENT_DEFS.map((def, i) => {
      let x: number, y: number
      if (i === 0) {
        x = cx; y = cy
      } else {
        const totalAgents = AGENT_DEFS.length - 1
        const angle = ((i - 1) / totalAgents) * Math.PI * 2 - Math.PI / 2
        const jitter = (Math.random() - 0.5) * 20
        x = cx + Math.cos(angle) * (baseRadius + jitter)
        y = cy + Math.sin(angle) * (baseRadius + jitter)
      }

      return {
        ...def,
        x, y,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        radius: i === 0 ? 32 : 20,
        active: false,
        searchQuery: null,
        dataPoints: [],
      }
    })

    nodesRef.current = nodes
  }, [overlay])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const dpr = window.devicePixelRatio || 1

    const resize = () => {
      const rect = canvas.parentElement!.getBoundingClientRect()
      canvas.width = rect.width * dpr
      canvas.height = rect.height * dpr
      canvas.style.width = rect.width + 'px'
      canvas.style.height = rect.height + 'px'
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)

      if (nodesRef.current.length === 0) {
        initNodes(rect.width, rect.height)
      }
    }
    resize()
    window.addEventListener('resize', resize)

    const draw = () => {
      phaseRef.current += 0.012
      const phase = phaseRef.current
      const w = canvas.width / dpr
      const h = canvas.height / dpr
      const nodes = nodesRef.current
      const cx = w / 2
      const cy = h / 2

      ctx.clearRect(0, 0, w, h)

      // Update live status
      liveAgents.forEach(la => {
        const node = nodes.find(n => n.id === la.agentId)
        if (node) {
          node.active = la.status === 'working'
        }
      })

      // Swarm physics — gentle floating
      nodes.forEach((node, i) => {
        if (i === 0) return // JARVIS stays centered-ish

        // Gravity toward original position
        const baseRadius = Math.min(w, h) * (overlay === 'hero' ? 0.3 : 0.35)
        const totalAgents = AGENT_DEFS.length - 1
        const angle = ((i - 1) / totalAgents) * Math.PI * 2 - Math.PI / 2
        const targetX = cx + Math.cos(angle) * baseRadius
        const targetY = cy + Math.sin(angle) * baseRadius

        node.vx += (targetX - node.x) * 0.002
        node.vy += (targetY - node.y) * 0.002

        // Organic swarm movement
        node.vx += Math.sin(phase * 1.5 + i * 0.8) * 0.04
        node.vy += Math.cos(phase * 1.2 + i * 0.6) * 0.04

        // Mouse repulsion
        if (mouseRef.current.active) {
          const dx = node.x - mouseRef.current.x
          const dy = node.y - mouseRef.current.y
          const dist = Math.sqrt(dx * dx + dy * dy)
          if (dist < 120) {
            const force = (120 - dist) / 120 * 0.5
            node.vx += (dx / dist) * force
            node.vy += (dy / dist) * force
          }
        }

        // Active agent — pulse outward
        if (node.active) {
          node.vx += Math.sin(phase * 4 + i) * 0.15
          node.vy += Math.cos(phase * 4 + i) * 0.15
        }

        // Damping
        node.vx *= 0.96
        node.vy *= 0.96

        node.x += node.vx
        node.y += node.vy

        // Keep on screen
        node.x = Math.max(40, Math.min(w - 40, node.x))
        node.y = Math.max(40, Math.min(h - 40, node.y))
      })

      // JARVIS stays near center with gentle movement
      nodes[0].x = cx + Math.sin(phase * 0.5) * 8
      nodes[0].y = cy + Math.cos(phase * 0.7) * 6

      // ── Draw connections ──
      CONNECTIONS.forEach(([fromId, toId]) => {
        const from = nodes.find(n => n.id === fromId)!
        const to = nodes.find(n => n.id === toId)!

        const isLiveCollab = liveAgents.some(la =>
          la.status === 'working' && (
            (la.agentId === fromId && la.collaboratingWith?.includes(toId)) ||
            (la.agentId === toId && la.collaboratingWith?.includes(fromId))
          )
        )

        const isActiveConnection = from.active || to.active || isLiveCollab
        const pulse = (Math.sin(phase * 2.5 + fromId * 0.4) + 1) / 2

        // Line
        ctx.beginPath()
        ctx.moveTo(from.x, from.y)
        ctx.lineTo(to.x, to.y)

        if (isLiveCollab) {
          ctx.strokeStyle = `rgba(34,197,94,${0.4 + pulse * 0.4})`
          ctx.lineWidth = 2.5
          ctx.setLineDash([8, 5])
        } else if (isActiveConnection) {
          ctx.strokeStyle = `${from.color}${Math.round(30 + pulse * 40).toString(16)}`
          ctx.lineWidth = 1.8
          ctx.setLineDash([])
        } else {
          ctx.strokeStyle = `rgba(80,80,120,${0.04 + pulse * 0.04})`
          ctx.lineWidth = 0.8
          ctx.setLineDash([])
        }
        ctx.stroke()
        ctx.setLineDash([])

        // Data flow particles on connections
        const numParticles = isLiveCollab ? 3 : (isActiveConnection ? 2 : 1)
        for (let p = 0; p < numParticles; p++) {
          const t = ((phase * (isLiveCollab ? 1.2 : 0.3) + fromId * 0.15 + p * 0.33) % 1)
          const px = from.x + (to.x - from.x) * t
          const py = from.y + (to.y - from.y) * t
          const pr = isLiveCollab ? 3.5 : (isActiveConnection ? 2.5 : 1.5)

          ctx.beginPath()
          ctx.arc(px, py, pr, 0, Math.PI * 2)
          ctx.fillStyle = isLiveCollab ? `rgba(34,197,94,${0.5 + pulse * 0.5})` : `${from.color}${Math.round(20 + pulse * 50).toString(16).padStart(2, '0')}`
          ctx.fill()
        }
      })

      // ── Draw ambient data particles ──
      const particles = particlesRef.current
      // Spawn new particles from active agents
      nodes.forEach(node => {
        if (node.active && Math.random() < 0.15) {
          const angle = Math.random() * Math.PI * 2
          const speed = 0.5 + Math.random() * 1.5
          particles.push({
            x: node.x,
            y: node.y,
            vx: Math.cos(angle) * speed,
            vy: Math.sin(angle) * speed,
            life: 1,
            color: node.color,
            fromId: node.id,
            toId: -1,
          })
        }
      })

      // Update and draw particles
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i]
        p.x += p.vx
        p.y += p.vy
        p.life -= 0.008
        if (p.life <= 0) { particles.splice(i, 1); continue }

        ctx.beginPath()
        ctx.arc(p.x, p.y, 1.5 * p.life, 0, Math.PI * 2)
        ctx.fillStyle = p.color + Math.round(p.life * 80).toString(16).padStart(2, '0')
        ctx.fill()
      }

      // Keep particle count reasonable
      if (particles.length > 200) particles.splice(0, particles.length - 200)

      // ── Draw nodes ──
      nodes.forEach((node, i) => {
        const isHovered = hovered === i
        const liveAgent = liveAgents.find(la => la.agentId === node.id)
        const isWorking = liveAgent?.status === 'working'
        const isDone = liveAgent?.status === 'done'
        const pulse = (Math.sin(phase * 3 + i * 0.7) + 1) / 2
        const r = node.radius + (isHovered ? 5 : 0) + (isWorking ? Math.sin(phase * 6) * 3 : 0)

        // Glow for active/working
        if (isWorking || isHovered || node.active) {
          const glowR = r + 15 + pulse * 12
          const glowColor = isWorking ? '#22c55e' : node.color
          const grad = ctx.createRadialGradient(node.x, node.y, r * 0.3, node.x, node.y, glowR)
          grad.addColorStop(0, glowColor + (isWorking ? '50' : '25'))
          grad.addColorStop(1, glowColor + '00')
          ctx.beginPath()
          ctx.arc(node.x, node.y, glowR, 0, Math.PI * 2)
          ctx.fillStyle = grad
          ctx.fill()
        }

        // Outer ring for working agents
        if (isWorking) {
          ctx.beginPath()
          ctx.arc(node.x, node.y, r + 6, -Math.PI / 2, -Math.PI / 2 + phase * 3 % (Math.PI * 2))
          ctx.strokeStyle = '#22c55e'
          ctx.lineWidth = 2.5
          ctx.stroke()
        }

        // Node body
        ctx.beginPath()
        ctx.arc(node.x, node.y, r, 0, Math.PI * 2)
        const bgGrad = ctx.createRadialGradient(node.x - r * 0.3, node.y - r * 0.3, 0, node.x, node.y, r)
        if (isWorking) {
          bgGrad.addColorStop(0, 'rgba(34,197,94,0.25)')
          bgGrad.addColorStop(1, 'rgba(10,15,25,0.9)')
        } else if (isDone) {
          bgGrad.addColorStop(0, node.color + '30')
          bgGrad.addColorStop(1, node.color + '10')
        } else {
          bgGrad.addColorStop(0, 'rgba(15,20,35,0.9)')
          bgGrad.addColorStop(1, 'rgba(10,15,25,0.95)')
        }
        ctx.fillStyle = bgGrad
        ctx.fill()

        ctx.strokeStyle = isWorking ? '#22c55e' : (isDone ? node.color + '80' : (isHovered ? node.color : 'rgba(80,80,120,0.15)'))
        ctx.lineWidth = isWorking ? 2.5 : (isHovered ? 2 : 1)
        ctx.stroke()

        // Emoji
        ctx.font = `${i === 0 ? 20 : 15}px sans-serif`
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(node.emoji, node.x, node.y)

        // Label
        if (showLabels) {
          ctx.font = `${isHovered ? 'bold ' : ''}${i === 0 ? 11 : 9}px Inter, sans-serif`
          ctx.fillStyle = isHovered || isWorking ? '#e2e8f0' : '#4a5568'
          ctx.fillText(node.name, node.x, node.y + r + 13)
        }

        // Working status text
        if (isWorking && liveAgent?.name) {
          ctx.font = 'bold 8px Inter, sans-serif'
          ctx.fillStyle = '#22c55e'
          ctx.fillText('PROCESSING', node.x, node.y + r + 24)
        }
        if (isDone) {
          ctx.font = 'bold 8px Inter, sans-serif'
          ctx.fillStyle = node.color + '99'
          ctx.fillText('DONE', node.x, node.y + r + 24)
        }
      })

      animRef.current = requestAnimationFrame(draw)
    }

    animRef.current = requestAnimationFrame(draw)

    return () => {
      cancelAnimationFrame(animRef.current)
      window.removeEventListener('resize', resize)
    }
  }, [initNodes, liveAgents, hovered, showLabels, overlay])

  const handleMouse = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = canvasRef.current?.getBoundingClientRect()
    if (!rect) return
    const mx = e.clientX - rect.left
    const my = e.clientY - rect.top
    mouseRef.current = { x: mx, y: my, active: true }

    if (!interactive) return

    let found = -1
    for (const [i, node] of nodesRef.current.entries()) {
      const dx = mx - node.x
      const dy = my - node.y
      if (Math.sqrt(dx * dx + dy * dy) < node.radius + 8) {
        found = i
        break
      }
    }
    setHovered(found >= 0 ? found : null)
    if (canvasRef.current) canvasRef.current.style.cursor = found >= 0 ? 'pointer' : 'default'
  }, [interactive])

  return (
    <canvas
      ref={canvasRef}
      onMouseMove={handleMouse}
      onMouseLeave={() => { mouseRef.current.active = false; setHovered(null) }}
      style={{ width: '100%', height, display: 'block' }}
    />
  )
}

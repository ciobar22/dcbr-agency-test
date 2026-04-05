import jsPDF from 'jspdf'
import 'jspdf-autotable'

// Extend jsPDF with autotable
declare module 'jspdf' {
  interface jsPDF {
    autoTable: (options: Record<string, unknown>) => jsPDF
    lastAutoTable: { finalY: number }
  }
}

// ── Colors ──────────────────────────────────────────────────────────
const COLORS = {
  primary: [124, 58, 237] as [number, number, number],       // #7c3aed
  secondary: [37, 99, 235] as [number, number, number],      // #2563eb
  dark: [5, 10, 20] as [number, number, number],              // #050a14
  text: [226, 232, 240] as [number, number, number],          // #e2e8f0
  muted: [100, 116, 139] as [number, number, number],         // #64748b
  white: [255, 255, 255] as [number, number, number],
  accent: [192, 132, 252] as [number, number, number],        // #c084fc
  success: [34, 197, 94] as [number, number, number],         // #22c55e
}

// ── Helpers ─────────────────────────────────────────────────────────
function stripMarkdown(text: string): string {
  return text
    .replace(/^#{1,3}\s+/gm, '')
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/\*(.*?)\*/g, '$1')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/^[-*]\s+/gm, '  • ')
    .replace(/^\d+\.\s+/gm, (match) => '  ' + match)
}

function addHeader(doc: jsPDF) {
  const w = doc.internal.pageSize.getWidth()
  const h = doc.internal.pageSize.getHeight()
  // Dark background — fix: text was near-white on white page
  doc.setFillColor(8, 12, 24)
  doc.rect(0, 0, w, h, 'F')
  // Gradient bar at top
  doc.setFillColor(...COLORS.primary)
  doc.rect(0, 0, w, 3, 'F')
  doc.setFillColor(...COLORS.secondary)
  doc.rect(w / 2, 0, w / 2, 3, 'F')
}

function addFooter(doc: jsPDF, pageNum: number) {
  const w = doc.internal.pageSize.getWidth()
  const h = doc.internal.pageSize.getHeight()
  doc.setFontSize(8)
  doc.setTextColor(...COLORS.muted)
  doc.text(`DCBR Marketing Agency — AI-Powered`, 20, h - 10)
  doc.text(`Pagina ${pageNum}`, w - 20, h - 10, { align: 'right' })
  // Bottom line
  doc.setDrawColor(...COLORS.primary)
  doc.setLineWidth(0.5)
  doc.line(20, h - 15, w - 20, h - 15)
}

function addCoverPage(doc: jsPDF, title: string, subtitle: string, date: string) {
  const w = doc.internal.pageSize.getWidth()
  const h = doc.internal.pageSize.getHeight()

  // Background
  doc.setFillColor(8, 12, 24)
  doc.rect(0, 0, w, h, 'F')

  // Accent gradient bar at top
  doc.setFillColor(...COLORS.primary)
  doc.rect(0, 0, w, 6, 'F')

  // DCBR Logo text
  doc.setFontSize(14)
  doc.setTextColor(...COLORS.accent)
  doc.text('DCBR', 20, 40)
  doc.setFontSize(10)
  doc.setTextColor(...COLORS.muted)
  doc.text('Marketing Agency', 47, 40)

  // Main title
  doc.setFontSize(36)
  doc.setTextColor(...COLORS.white)
  const titleLines = doc.splitTextToSize(title, w - 40)
  doc.text(titleLines, 20, h / 2 - 30)

  // Subtitle
  doc.setFontSize(14)
  doc.setTextColor(...COLORS.muted)
  const subLines = doc.splitTextToSize(subtitle, w - 40)
  doc.text(subLines, 20, h / 2 + 10)

  // Date
  doc.setFontSize(11)
  doc.setTextColor(...COLORS.accent)
  doc.text(date, 20, h / 2 + 40)

  // Bottom branding
  doc.setFontSize(9)
  doc.setTextColor(...COLORS.muted)
  doc.text('Generato da JARVIS AI — DCBR Marketing Intelligence', 20, h - 20)

  // Bottom accent bar
  doc.setFillColor(...COLORS.secondary)
  doc.rect(0, h - 6, w, 6, 'F')
}

function addSectionTitle(doc: jsPDF, y: number, title: string, emoji?: string): number {
  const w = doc.internal.pageSize.getWidth()

  if (y > doc.internal.pageSize.getHeight() - 60) {
    doc.addPage()
    addHeader(doc)
    y = 25
  }

  // Section background
  doc.setFillColor(15, 20, 35)
  doc.roundedRect(15, y - 4, w - 30, 14, 3, 3, 'F')

  doc.setFontSize(12)
  doc.setTextColor(...COLORS.white)
  const label = emoji ? `${emoji}  ${title}` : title
  doc.text(label, 20, y + 6)

  // Accent underline
  doc.setDrawColor(...COLORS.primary)
  doc.setLineWidth(0.8)
  doc.line(20, y + 11, 80, y + 11)

  return y + 20
}

function addTextBlock(doc: jsPDF, y: number, text: string, pageNum: { value: number }): number {
  const w = doc.internal.pageSize.getWidth()
  const maxWidth = w - 40
  const lineHeight = 5.5
  const pageHeight = doc.internal.pageSize.getHeight() - 25

  const clean = stripMarkdown(text)
  const lines = doc.splitTextToSize(clean, maxWidth)

  for (const line of lines) {
    if (y > pageHeight) {
      addFooter(doc, pageNum.value)
      pageNum.value++
      doc.addPage()
      addHeader(doc)
      y = 25
    }

    // Detect bullet points
    const trimmed = (line as string).trim()
    if (trimmed.startsWith('•')) {
      doc.setFontSize(9.5)
      doc.setTextColor(...COLORS.accent)
      doc.text('•', 22, y)
      doc.setTextColor(...COLORS.text)
      doc.text(trimmed.slice(1).trim(), 28, y)
    } else if (/^\d+\./.test(trimmed)) {
      doc.setFontSize(9.5)
      doc.setTextColor(...COLORS.accent)
      const numMatch = trimmed.match(/^(\d+\.)/)
      if (numMatch) {
        doc.text(numMatch[1], 22, y)
        doc.setTextColor(...COLORS.text)
        doc.text(trimmed.slice(numMatch[1].length).trim(), 30, y)
      }
    } else {
      doc.setFontSize(9.5)
      doc.setTextColor(...COLORS.text)
      doc.text(trimmed, 20, y)
    }

    y += lineHeight
  }

  return y + 4
}

// ── Public: Generate Campaign Report PDF ────────────────────────────

interface AgentOutput {
  name: string
  emoji: string
  output: string
}

export function generateCampaignPDF(
  clientName: string,
  agents: AgentOutput[]
): jsPDF {
  const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' })
  const date = new Date().toLocaleDateString('it-IT', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  })

  // Cover
  addCoverPage(
    doc,
    `Strategia Marketing\n${clientName}`,
    `Report completo generato da ${agents.length} agenti AI specializzati.\nOgni sezione e stata prodotta da un esperto dedicato.`,
    date
  )

  // Table of contents
  doc.addPage()
  addHeader(doc)
  let y = 25
  doc.setFontSize(18)
  doc.setTextColor(...COLORS.white)
  doc.text('Indice', 20, y)
  y += 15

  agents.forEach((agent, i) => {
    doc.setFontSize(10)
    doc.setTextColor(...COLORS.accent)
    doc.text(`${i + 1}.`, 22, y)
    doc.setTextColor(...COLORS.text)
    doc.text(`${agent.emoji}  ${agent.name}`, 30, y)
    y += 7
  })

  addFooter(doc, 1)
  const pageNum = { value: 2 }

  // Agent sections
  agents.forEach((agent) => {
    doc.addPage()
    addHeader(doc)
    let y = 20

    y = addSectionTitle(doc, y, agent.name, agent.emoji)
    y = addTextBlock(doc, y, agent.output, pageNum)

    addFooter(doc, pageNum.value)
    pageNum.value++
  })

  return doc
}

// ── Public: Generate single content PDF ─────────────────────────────

export function generateContentPDF(
  title: string,
  type: string,
  content: string,
  brandName?: string
): jsPDF {
  const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' })
  const date = new Date().toLocaleDateString('it-IT', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  })

  const subtitle = brandName
    ? `${type} per ${brandName}`
    : type

  addCoverPage(doc, title, subtitle, date)

  doc.addPage()
  addHeader(doc)

  const pageNum = { value: 1 }
  let y = 25

  y = addSectionTitle(doc, y, title)
  y = addTextBlock(doc, y, content, pageNum)

  addFooter(doc, pageNum.value)

  return doc
}

// ── Public: Generate JARVIS chat export PDF ─────────────────────────

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export function generateChatPDF(
  title: string,
  messages: ChatMessage[]
): jsPDF {
  const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' })
  const date = new Date().toLocaleDateString('it-IT', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  })

  addCoverPage(doc, title, 'Conversazione con JARVIS AI', date)

  doc.addPage()
  addHeader(doc)

  const pageNum = { value: 1 }
  let y = 25

  for (const msg of messages) {
    const label = msg.role === 'user' ? '👤 Tu' : '🧠 JARVIS'
    const color = msg.role === 'user' ? COLORS.secondary : COLORS.accent

    if (y > doc.internal.pageSize.getHeight() - 40) {
      addFooter(doc, pageNum.value)
      pageNum.value++
      doc.addPage()
      addHeader(doc)
      y = 25
    }

    // Speaker label
    doc.setFontSize(10)
    doc.setTextColor(...color)
    doc.text(label, 20, y)
    y += 7

    // Message content
    y = addTextBlock(doc, y, msg.content, pageNum)
    y += 3

    // Separator
    doc.setDrawColor(30, 40, 60)
    doc.setLineWidth(0.3)
    doc.line(20, y, doc.internal.pageSize.getWidth() - 20, y)
    y += 6
  }

  addFooter(doc, pageNum.value)
  return doc
}

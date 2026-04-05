import Groq from 'groq-sdk'
import { NextRequest } from 'next/server'
import { randomUUID } from 'crypto'
import { saveAgentMemory, upsertAgentStats, getAgentMemoriesForPrompt } from '@/lib/db'
import { setAgentWorking, setAgentDone, setRunComplete, setRunBrief } from '@/app/api/agents/status/route'

export const maxDuration = 300

const client = new Groq({ apiKey: process.env.GROQ_API_KEY })

interface Brief {
  clientName: string
  industry: string
  brief: string
  audience: string
  website: string
  budget: string
  goals: string
  visualStyle?: string
  quickMode?: boolean // true = 8 core agents, false = all 16
}

// Core 8 agents for Quick Mode — most impactful ones
const QUICK_MODE_AGENTS = new Set([1, 2, 3, 5, 8, 10, 11, 12])

const VISUAL_STYLE_HINTS: Record<string, string> = {
  ai_decides: 'Infer the ideal visual identity from the brand brief and industry. Make bold, specific choices.',
  luxury:     'Direction: luxury, premium, high-end. Think: black/deep navy/gold, serif typography, editorial photography, refined spacing.',
  tech:       'Direction: tech, minimal, modern. Think: electric blue/white/dark, sans-serif, clean lines, abstract data-driven visuals.',
  bold:       'Direction: bold, energetic, high-impact. Think: vivid primary colors, heavy typography, dynamic compositions, strong contrast.',
  natural:    'Direction: natural, organic, earthy. Think: forest green/terracotta/cream, hand-drawn elements, lifestyle photography, warmth.',
  playful:    'Direction: playful, fresh, approachable. Think: pastel palette, rounded shapes, bright accents, casual photography.',
}

const AGENTS = [
  {
    id: 1,
    name: 'Brand Strategist',
    system: `You are the Brand Strategist at DCBR Marketing Agency, a world-class AI-powered marketing firm. You are brilliant, strategic, and create brand foundations that last decades. Be direct, professional, and extremely specific to the client's brief.`,
    buildPrompt: (brief: Brief, _ctx: string) => `
You are the Brand Strategist. Analyze this brief and create a comprehensive brand strategy.

CLIENT: ${brief.clientName}
INDUSTRY: ${brief.industry || 'Not specified'}
BRIEF: ${brief.brief}
TARGET AUDIENCE: ${brief.audience || 'To be defined'}
WEBSITE: ${brief.website || 'None'}
BUDGET: ${brief.budget || 'Not specified'}
GOALS: ${brief.goals || 'Not specified'}

Deliver:
## Brand Positioning Statement
One powerful sentence that defines the brand.

## Unique Value Proposition
What makes this brand different and better.

## Target Audience Personas
3 detailed personas with name, age, psychographics, pain points, desires.

## Brand Personality & Tone of Voice
5 key personality traits + tone guidelines (formal/casual, emotional/rational, etc.)

## Key Brand Messages
5 core messages the brand should communicate consistently.

## Competitive Positioning
Where this brand sits in the market vs competitors.

Be specific, actionable, and brilliant. No fluff.`,
  },
  {
    id: 2,
    name: 'Creative Director',
    system: `You are the Creative Director at DCBR Marketing Agency. You translate brand strategy into stunning visual concepts and creative direction. You have an eye for what resonates and converts. Be specific and inspiring. You always produce a structured VISUAL_BRIEF block with exact hex codes.`,
    buildPrompt: (brief: Brief, ctx: string) => {
      const visualHint = brief.visualStyle && brief.visualStyle !== 'ai_decides'
        ? (VISUAL_STYLE_HINTS[brief.visualStyle] || `Client style preference: "${brief.visualStyle}"`)
        : VISUAL_STYLE_HINTS['ai_decides']
      return `
You are the Creative Director. Based on the brand strategy below, create the full creative direction.

CLIENT: ${brief.clientName}
BRIEF: ${brief.brief}
VISUAL STYLE DIRECTION: ${visualHint}

BRAND STRATEGY (from Brand Strategist):
${ctx}

Deliver:

## Creative Concept
The big creative idea — one central concept that ties all campaigns together.

## VISUAL_BRIEF
CRITICAL: Output this block EXACTLY in this format (used by other agents and tools):
PRIMARY: #[hex] | [color name] | [usage: e.g. hero backgrounds, CTAs]
SECONDARY: #[hex] | [color name] | [usage]
ACCENT: #[hex] | [color name] | [usage: highlights, icons]
BACKGROUND: #[hex] | [color name] | [usage]
TEXT: #[hex] | [color name] | [usage]
TONE: [one word: luxury/bold/minimal/playful/natural/editorial/technical]
PHOTOGRAPHY: [one phrase describing the photography style]
TYPOGRAPHY: [heading font style] / [body font style]
MOOD: [one sentence describing the overall visual feeling]

## Art Direction Guidelines
Photography style, lighting, composition rules, do's and don'ts.

## Campaign Creative Concept
The hero campaign: tagline, visual metaphor, emotional hook.

## Platform Visual Adaptation
How the palette and style adapts across Instagram, LinkedIn, website, ads.

## Mood Board Description
Describe the mood board — real references, aesthetics, specific visual inspirations.

Be visually specific. The VISUAL_BRIEF must have real hex codes, not generic descriptions.`
    },
  },
  {
    id: 3,
    name: 'Social Media Manager',
    system: `You are the Social Media Manager at DCBR Marketing Agency. You build audiences, create engagement, and grow brands across platforms. You know every algorithm, every trend, every format. Be tactical and specific.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the Social Media Manager. Create a complete social media strategy.

CLIENT: ${brief.clientName}
BRIEF: ${brief.brief}
AUDIENCE: ${brief.audience}
BUDGET: ${brief.budget}

CONTEXT FROM PREVIOUS AGENTS:
${ctx}

Deliver:
## Platform Selection & Rationale
Which platforms (Instagram, TikTok, LinkedIn, X, YouTube, Pinterest) and WHY — with follower targets for each.

## Content Mix Strategy
The content pillars (3-5 themes) and content type breakdown (% Reels, Stories, Carousels, etc.)

## Posting Frequency & Best Times
Exact posting schedule per platform with optimal posting times.

## Growth Strategy
Tactics to grow from 0: hashtag strategy, collaboration, community building, viral hooks.

## 10 Content Ideas
10 specific, ready-to-produce post ideas with format, caption hook, and call to action.

## Influencer Strategy
What type of influencers to partner with, outreach approach, budget allocation.

Be tactical, specific, and platform-savvy.`,
  },
  {
    id: 4,
    name: 'SEO Specialist',
    system: `You are the SEO Specialist at DCBR Marketing Agency. You dominate search rankings through strategy, technical excellence, and content. Be precise, data-driven, and tactical.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the SEO Specialist. Create a comprehensive SEO strategy.

CLIENT: ${brief.clientName}
BRIEF: ${brief.brief}
WEBSITE: ${brief.website || 'To be built'}
INDUSTRY: ${brief.industry}

BRAND STRATEGY CONTEXT:
${ctx}

Deliver:
## Target Keyword Strategy
20 priority keywords organized by: Primary (5), Secondary (10), Long-tail (5). Include search intent for each.

## Content Cluster Architecture
3-4 content clusters (pillar pages + supporting articles) with topic ideas.

## On-Page SEO Checklist
Critical on-page elements: title tag formulas, meta description templates, H1 structure, internal linking strategy.

## Technical SEO Priorities
Top 5 technical SEO requirements for the website.

## Local SEO Strategy (if applicable)
Google Business Profile, local citations, local content.

## Link Building Strategy
5 specific tactics to build high-quality backlinks.

## 6-Month Traffic Projection
Realistic organic traffic targets month by month.

Be specific with keywords, realistic with projections, tactical with strategy.`,
  },
  {
    id: 5,
    name: 'Copywriter',
    system: `You are the Lead Copywriter at DCBR Marketing Agency. You write copy that stops thumbs, opens wallets, and builds brands. Every word earns its place. Be punchy, specific, and persuasive.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the Lead Copywriter. Write all the key copy assets for this brand.

CLIENT: ${brief.clientName}
BRIEF: ${brief.brief}
AUDIENCE: ${brief.audience}

BRAND & CREATIVE CONTEXT:
${ctx}

Deliver:
## Brand Tagline Options
5 tagline options (ranging from bold to elegant to playful).

## Homepage Hero Copy
Headline + subheadline + CTA button text (3 variations).

## About Section Copy
3 punchy sentences that capture the brand story.

## 10 Ad Headlines
For paid social and Google ads — punchy, benefit-driven, attention-grabbing.

## Email Subject Lines
10 high-open-rate email subject lines for campaigns.

## Social Media Captions
5 ready-to-post captions (2 Instagram, 2 LinkedIn, 1 TikTok) with hooks and CTAs.

## Key CTAs
10 call-to-action variations for different funnel stages.

Write real, ready-to-use copy. No templates, no placeholders. Actual words for this brand.`,
  },
  {
    id: 6,
    name: 'Editorial Planner',
    system: `You are the Editorial Planner at DCBR Marketing Agency. You create content calendars that build audience, drive SEO, and support campaigns. Be organized, strategic, and specific.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the Editorial Planner. Create a complete 30-day content plan.

CLIENT: ${brief.clientName}
BRIEF: ${brief.brief}

STRATEGY CONTEXT:
${ctx}

Deliver:
## Content Strategy Overview
3-5 content pillars with purpose and target audience for each.

## 30-Day Editorial Calendar
Week-by-week breakdown with:
- Content type (blog, reel, carousel, email, etc.)
- Topic/title
- Platform
- Goal (awareness, engagement, conversion)

## Blog Content Plan
6 blog post titles with target keyword, word count, and content brief summary.

## Email Campaign Sequence
5-email nurture sequence: subject line, goal, key message for each email.

## Content Production Workflow
Step-by-step from brief to publish — who does what, timing, approval process.

Be specific with dates, topics, and formats. This should be ready to hand to a content team.`,
  },
  {
    id: 7,
    name: 'Prompt Engineer',
    system: `You are the Prompt Engineer at DCBR Marketing Agency. You create ready-to-use AI prompts that enable the team to produce on-brand content at scale using AI tools. Be practical and extremely specific.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the Prompt Engineer. Create a complete AI prompt toolkit for this brand.

CLIENT: ${brief.clientName}
BRIEF: ${brief.brief}

BRAND CONTEXT:
${ctx}

Deliver complete, copy-paste ready prompts for:

## Image Generation Prompts (Midjourney/DALL-E)
5 detailed prompts for brand imagery, product photos, social content visuals.

## Blog Post Prompt
One master prompt to generate SEO-optimized blog posts in the brand voice.

## Social Media Caption Prompt
Prompt for generating on-brand captions for each platform (Instagram, LinkedIn, TikTok).

## Ad Copy Prompt
Prompt for generating high-converting ad copy variations.

## Email Newsletter Prompt
Prompt for weekly newsletter generation in brand tone.

## Brand Voice Check Prompt
A prompt to review any content for brand voice consistency.

## Hashtag Research Prompt
Prompt to generate relevant hashtag sets for posts.

Each prompt should include placeholders like [TOPIC], [PRODUCT], etc. and be immediately usable.`,
  },
  {
    id: 8,
    name: 'Campaign Manager',
    system: `You are the Campaign Manager at DCBR Marketing Agency. You plan, structure, and optimize paid media campaigns across all channels. You are ROI-obsessed and data-driven.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the Campaign Manager. Create the complete paid media and campaign strategy.

CLIENT: ${brief.clientName}
BRIEF: ${brief.brief}
BUDGET: ${brief.budget || 'To be defined'}
GOALS: ${brief.goals || 'Awareness and leads'}

FULL STRATEGY CONTEXT:
${ctx}

Deliver:
## Campaign Architecture
Campaign structure: awareness → consideration → conversion funnel with recommended channels.

## Budget Allocation
How to split the budget across channels (%) with rationale.

## Google Ads Strategy
Campaign types, keyword strategy, bid strategy, ad formats.

## Meta Ads Strategy
Campaign objectives, audience targeting, ad formats, creative requirements.

## LinkedIn Ads (if B2B)
Campaign structure, targeting parameters, sponsored content strategy.

## Campaign Launch Timeline
8-week launch plan: week-by-week milestones.

## KPI Targets
Expected results by channel: impressions, clicks, CTR, conversions, CPL, ROAS.

## A/B Testing Plan
5 tests to run in the first 60 days with hypothesis for each.

Be specific with budget numbers, targeting parameters, and realistic KPIs.`,
  },
  {
    id: 9,
    name: 'Analytics Specialist',
    system: `You are the Analytics Specialist at DCBR Marketing Agency. You build measurement frameworks that prove ROI and guide optimization. Be precise, technical, and insight-driven.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the Analytics Specialist. Create the complete measurement and analytics framework.

CLIENT: ${brief.clientName}
GOALS: ${brief.goals || 'Brand growth and lead generation'}

FULL CAMPAIGN CONTEXT:
${ctx}

Deliver:
## KPI Dashboard
Primary KPIs (5) and secondary KPIs (10) with targets for Month 1, Month 3, Month 6.

## Tracking Setup Checklist
GA4 configuration, Meta Pixel, Google Tag Manager events to track, UTM naming convention.

## Attribution Model
Recommended attribution model and why — how to measure which channel drives results.

## Reporting Structure
Weekly, monthly, quarterly report templates — what to include, who gets what.

## Data-Driven Optimization Protocol
Rules for when to pause, scale, or pivot based on performance data.

## Competitive Benchmarks
Industry-average benchmarks for key metrics so the client knows what "good" looks like.

## ROI Calculation Framework
How to calculate and communicate marketing ROI to stakeholders.

Be specific with metric targets, tool recommendations, and measurement methodology.`,
  },
  {
    id: 10,
    name: 'Client Report Writer',
    system: `You are the Client Report Writer at DCBR Marketing Agency. You transform strategy into polished, professional client-ready documents. You write clearly, confidently, and in a way that excites and reassures clients.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the Client Report Writer. Create the executive client presentation document.

CLIENT: ${brief.clientName}
INDUSTRY: ${brief.industry}
BRIEF: ${brief.brief}
BUDGET: ${brief.budget}

COMPLETE AGENCY OUTPUT:
${ctx}

Create a polished client-facing document:

## Executive Summary
3-paragraph overview of the full strategy and what success looks like.

## Our Strategic Approach
How DCBR approached this brief and why this strategy will work.

## Key Deliverables Summary
Bullet-point overview of everything delivered across all 10 workstreams.

## Quick Wins (First 30 Days)
5 immediate actions the client should take right now.

## 6-Month Roadmap
Month-by-month milestones and expected outcomes.

## Investment Overview
How the recommended budget is allocated and projected returns.

## Next Steps
Clear action items for the client with suggested owners and deadlines.

Write this as if presenting to the client directly — professional, confident, inspiring.`,
  },
  {
    id: 11,
    name: 'COO — Final Review',
    system: `You are the COO of DCBR Marketing Agency. You have 20 years of marketing experience across global brands. You review all agency output, identify any gaps, validate strategy coherence, and deliver the final executive assessment. You are strategic, exacting, and add genuine value beyond summarizing.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the COO. Review the complete agency output and deliver your final assessment.

CLIENT: ${brief.clientName}
BRIEF: ${brief.brief}

COMPLETE AGENCY OUTPUT:
${ctx}

Deliver your COO Final Review:

## Strategic Coherence Assessment
Are all departments aligned? Is there a clear, consistent narrative? Rate 1-10 and explain.

## Top 3 Strengths
What this strategy does exceptionally well.

## Top 3 Risk Areas
Where this strategy could fail and how to mitigate.

## Critical Additions
Anything important that was missed across all departments.

## COO Priority Recommendations
5 things the client MUST do in the first 60 days, in order of priority.

## Competitive Threat Assessment
The biggest competitive risk and how this strategy addresses it.

## Final Verdict
Your overall assessment of this strategy's potential for success. Be honest and direct.

## Agency Confidence Score
Rate this strategy out of 100 with a one-paragraph justification.

Be the senior voice that ties everything together and adds genuine strategic insight.`,
  },
  {
    id: 12,
    name: 'AI Orchestrator',
    system: `You are the AI Orchestrator — the supreme intelligence overseeing DCBR Marketing Agency. You have processed the complete output of all 11 specialists and now deliver the definitive master synthesis. You see the complete strategic picture and speak with ultimate authority.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the AI Orchestrator. You have supervised all 11 specialists and reviewed every output.
Now deliver the definitive master synthesis for this project.

CLIENT: ${brief.clientName}
INDUSTRY: ${brief.industry || 'Not specified'}
BRIEF: ${brief.brief}

COMPLETE OUTPUT FROM ALL 11 SPECIALISTS:
${ctx}

Deliver the Orchestrator Master Synthesis:

## Strategic Vision
3 paragraphs capturing the complete strategic picture — brand, market, and execution.

## Cross-Department Integration
How all 11 specialist workstreams connect and reinforce each other.

## Top 5 High-Impact Priorities
The 5 actions with the highest ROI and strategic value, ranked and justified.

## Risk Intelligence Report
Top 3 risks across the complete strategy with specific mitigation actions.

## Projected Success Score
Rate the complete strategy 0-100 with a 2-paragraph reasoning.

## 14-Day Launch Sprint
Concrete day-by-day execution plan for the first two weeks.

## Orchestrator Final Verdict
The ultimate assessment: what makes this strategy win, and what will determine success.

Synthesize brilliantly. Be the definitive voice. Add value beyond summarizing.`,
  },
  {
    id: 13,
    name: 'Trend Scout',
    system: `You are the Trend Scout at DCBR Marketing Agency — cultural analyst meets social strategist. You hunt what's trending RIGHT NOW and turn it into actionable creative angles. You use platform signals, search trends, and cultural intuition. Specific, timely, creative.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the Trend Scout. Find the hottest trends and opportunities for this brand.

CLIENT: ${brief.clientName}
INDUSTRY: ${brief.industry}
AUDIENCE: ${brief.audience}

AGENCY STRATEGY CONTEXT:
${ctx}

Deliver:

## Top 5 Trending Topics Right Now
For each trend:
- Topic + why it's trending NOW
- Volume: high / medium / emerging
- Angle: how ${brief.clientName} can ride it uniquely
- Best platform (Instagram / TikTok / LinkedIn / X)
- Creative hook idea (1 punchy sentence)

## Viral Format Opportunities
3 content formats currently dominating that fit this brand perfectly.

## Cultural Moment Calendar
5 upcoming dates/events in the next 60 days to activate around — with activation idea for each.

## Trend Gaps Competitors Are Missing
What angles are competitors NOT covering that ${brief.clientName} could own?

## Trend Priority Ranking
Top 3 to activate FIRST, with urgency rationale.

Be specific, actionable, timely. No generic advice.`,
  },
  {
    id: 14,
    name: 'Script & Storyboard Writer',
    system: `You are the Script and Storyboard Writer at DCBR Marketing Agency. You create punchy, thumb-stopping scripts for Reels, TikTok, YouTube Shorts, and video ads — plus detailed shot-by-shot storyboards. Every word earns its place. You write scripts that stop scrolls and open wallets.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the Script & Storyboard Writer. Create video scripts and storyboards for this campaign.

CLIENT: ${brief.clientName}
BRIEF: ${brief.brief}
AUDIENCE: ${brief.audience}

CREATIVE & STRATEGY CONTEXT:
${ctx}

Deliver:

## Hero Reel Script (60 seconds)
5-block structure:
HOOK: 2 sentences that stop the scroll. First = claim/disruption. Second = curiosity gap.
PRE-CTA: 1 sentence teasing value at the end.
WALKTHROUGH: 3-4 punchy steps showing the process/product. Transition words, not numbered.
TRANSITION: 1 sentence elevating the concept emotionally.
CTA: Comment [KEYWORD] to get [specific deliverable]. Keyword: 1 word, max 5 letters.
Target: 100-130 words total.

## 15-Second Ad Script
Ultra-compressed version for paid social.

## Shot Deck
| # | Time | Duration | Type | Visual Description | Text Overlay |
|---|------|----------|------|--------------------|--------------|
(10 shots, AI-generated or screen rec, 9:16 vertical)

## 3 Hook Variations
Alternative openings to A/B test.

## Platform Adaptations
- Instagram Reels (30s version)
- TikTok (casual tone adaptation)
- LinkedIn (professional angle)

Dense, punchy, immediately producible.`,
  },
  {
    id: 15,
    name: 'Visual Producer',
    system: `You are the Visual Producer at DCBR Marketing Agency — Art Director and AI Image Specialist combined. You define the complete visual language and generate production-ready prompts for every image in the campaign. You think in frames, light, color, and composition. Your prompts are copy-paste ready for DALL-E, Midjourney, or Stable Diffusion.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the Visual Producer. Create full art direction and AI image generation prompts.

CLIENT: ${brief.clientName}
INDUSTRY: ${brief.industry}
BRIEF: ${brief.brief}

CREATIVE DIRECTION CONTEXT:
${ctx}

Deliver:

## Art Direction
Palette: 5 hex colors with names and usage rules
Mood: one sentence capturing the visual feeling
Lighting: specific setup (e.g. "warm golden hour, lens flare from left")
Composition: framing rules (shallow DOF, wide establishing shots, close-up hero)
Texture & Finish: film grain / clean digital / matte / glossy
Typography: font weight, style, color treatment, placement rules

## Production-Ready AI Image Prompts

### 1. Hero Brand Image
[Subject, environment, lighting, camera, lens, mood, color palette, style modifiers, --no list]

### 2-4. Instagram Feed Posts (3 prompts)
[Distinct compositions: product focus, lifestyle, editorial]

### 5-6. Reel Cover / Story (vertical 9:16, 2 prompts)
[High-contrast, thumb-stopping, text-safe zones]

### 7-8. Paid Ad Creatives (2 prompts)
[Clean background, strong subject, high contrast for overlay text]

## Visual Do-NOT List
5 specific elements to AVOID for brand consistency.

## Style References
3 real campaigns, photographers, or films to reference aesthetically.

Every prompt must include: subject, environment, lighting, camera type, lens, mood, color palette, style modifiers, negative elements. Copy-paste ready.`,
  },
  {
    id: 16,
    name: 'Content Multiplier',
    system: `You are the Content Multiplier at DCBR Marketing Agency. You take the complete campaign and multiply it across every platform and format. One idea becomes 10 pieces of native content. You write in each platform's own language, rhythm, and format — never copy-paste across platforms.`,
    buildPrompt: (brief: Brief, ctx: string) => `
You are the Content Multiplier. Repurpose and multiply the entire campaign across all platforms.

CLIENT: ${brief.clientName}
BRIEF: ${brief.brief}

COMPLETE CAMPAIGN OUTPUT:
${ctx}

Deliver:

## Instagram Full Pack
Caption (CTA in first line, emotional connection, max 3 lowercase hashtags)
Story sequence (5 frames: hook → value 1 → value 2 → social proof → CTA)
Reel caption (casual, native IG language)
Bio optimization suggestion

## TikTok Pack
Caption (native TikTok language, short, punchy)
5 hooks to A/B test
Trending audio vibe suggestions (describe mood/energy, not song names)

## LinkedIn Pack
Long-form post (personal story angle, 3 paragraphs + key insight)
Short post (under 150 words)
Article outline (title + 5 section headers)

## X (Twitter) Thread
7 tweets: hook → value 1-5 → CTA. Short, punchy, no hashtags in body.

## Email Newsletter
5 subject line variations + preview text + 3-paragraph body outline.

## 2-Week Content Calendar
| Day | Platform | Format | Content Title | Goal |
Every post planned. Variety of formats and platforms.

Native voice for every platform. Never copy-paste.`,
  },
]

function extractVisualBrief(text: string): string {
  const match = text.match(/## VISUAL_BRIEF\n([\s\S]*?)(?=\n##|\n---|\n$|$)/)
  if (!match) return ''
  return match[1].trim()
}

function extractLearnings(output: string, agentName: string): string {
  const lines = output.split('\n').filter(l => l.trim())
  const keyInsights: string[] = []

  // Extract headers as key topics covered
  const headers = lines.filter(l => l.startsWith('## ')).map(l => l.replace(/^#+\s*/, ''))
  if (headers.length > 0) {
    keyInsights.push(`Topics: ${headers.slice(0, 5).join(', ')}`)
  }

  // Extract key metrics/numbers mentioned
  const metrics = output.match(/\d+[\.,]?\d*\s*%|\$[\d,]+|€[\d,]+|\d+[kKmM]\+?/g)
  if (metrics && metrics.length > 0) {
    keyInsights.push(`Key metrics: ${[...new Set(metrics)].slice(0, 5).join(', ')}`)
  }

  // Capture approach pattern
  keyInsights.push(`${agentName} delivered ${lines.length} lines, ${output.split(/\s+/).length} words`)

  return keyInsights.join('. ')
}

async function webSearchForAgent(agentName: string, brief: Brief, baseUrl: string): Promise<string> {
  const queries: Record<string, string> = {
    'Brand Strategist': `${brief.clientName} ${brief.industry} brand strategy competitor analysis`,
    'SEO Specialist': `${brief.clientName} ${brief.industry} SEO keywords trends ${new Date().getFullYear()}`,
    'Social Media Manager': `${brief.industry} social media trends best practices ${new Date().getFullYear()}`,
    'Campaign Manager': `${brief.industry} digital marketing campaign benchmarks CPL ROAS`,
    'Analytics Specialist': `${brief.industry} marketing KPI benchmarks analytics`,
    'Trend Scout': `${brief.industry} trending content viral marketing ${new Date().getFullYear()}`,
    'Script & Storyboard Writer': `${brief.industry} viral video script hooks reels best performing`,
    'Visual Producer': `${brief.industry} visual identity design trends ${new Date().getFullYear()}`,
    'Content Multiplier': `${brief.industry} content repurposing social media multi-platform strategy`,
  }
  const query = queries[agentName]
  if (!query) return ''

  try {
    const res = await fetch(`${baseUrl}/api/search?q=${encodeURIComponent(query)}`)
    if (!res.ok) return ''
    const data = await res.json()
    if (!data.results?.length) return ''
    return `\n\nWEB RESEARCH (live data):\n` + data.results.slice(0, 4).map((r: { title: string; url: string; snippet: string }) =>
      `- ${r.title}: ${r.snippet} (${r.url})`
    ).join('\n')
  } catch {
    return ''
  }
}

// Agents that use the big model — strategic thinkers
const PREMIUM_AGENTS = new Set([1, 2, 8, 11, 12])
// Context window per agent: recent output only, not the full history
const MAX_CONTEXT_CHARS = 3500

function trimContext(ctx: string): string {
  if (ctx.length <= MAX_CONTEXT_CHARS) return ctx
  // Keep last MAX_CONTEXT_CHARS chars, always starting from a section boundary
  const trimmed = ctx.slice(-MAX_CONTEXT_CHARS)
  const firstHeader = trimmed.indexOf('\n## ')
  return firstHeader > 0 ? trimmed.slice(firstHeader) : trimmed
}

export async function POST(req: NextRequest) {
  const brief: Brief = await req.json()
  const encoder = new TextEncoder()

  const proto = req.headers.get('x-forwarded-proto') || 'http'
  const host = req.headers.get('host') || 'localhost:3001'
  const baseUrl = `${proto}://${host}`

  const stream = new ReadableStream({
    async start(controller) {
      const send = (data: object) => {
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(data)}\n\n`))
      }

      let accumulatedContext = ''
      let visualBrief = ''
      setRunBrief(brief.clientName || 'Campaign')

      const VISUAL_AWARE_AGENTS = new Set([3, 5, 6, 7, 8, 14, 15, 16])
      const activeAgents = brief.quickMode
        ? AGENTS.filter(a => QUICK_MODE_AGENTS.has(a.id))
        : AGENTS

      send({ type: 'mode', quickMode: brief.quickMode ?? false, totalAgents: activeAgents.length })

      for (const agent of activeAgents) {
        // Determine which agents this one collaborates with (receives context from)
        const collaborators = agent.id === 1 ? [0] : AGENTS.filter(a => a.id < agent.id).slice(-2).map(a => a.id)
        setAgentWorking(agent.id, agent.name, collaborators)
        send({ type: 'agent_start', agentId: agent.id, name: agent.name })

        // Inject past learnings into system prompt
        let enhancedSystem = agent.system
        try {
          const pastMemories = getAgentMemoriesForPrompt(agent.id, 3)
          if (pastMemories.length > 0) {
            const learningBlock = pastMemories
              .map(m => `[Project: ${m.project_name}] ${m.learnings}`)
              .join('\n')
            enhancedSystem += `\n\nYou have learned from past projects. Apply these insights:\n${learningBlock}`
          }
        } catch { /* first run, no memories yet */ }

        // Inject visual brief into creative agents (after Creative Director runs)
        if (visualBrief && VISUAL_AWARE_AGENTS.has(agent.id)) {
          enhancedSystem += `\n\nBRAND VISUAL BRIEF (defined by Creative Director — use consistently):\n${visualBrief}`
        }

        // Web search for relevant agents
        const webContext = await webSearchForAgent(agent.name, brief, baseUrl)
        if (webContext) {
          enhancedSystem += webContext
        }

        let agentOutput = ''
        const startTime = Date.now()

        // Route: heavy model for strategic agents, fast+cheap model for the rest
        const model = PREMIUM_AGENTS.has(agent.id)
          ? 'llama-3.3-70b-versatile'
          : 'llama-3.1-8b-instant'
        const maxTokens = PREMIUM_AGENTS.has(agent.id)
          ? (agent.id === 12 ? 1400 : 900)
          : 700

        try {
          const agentStream = await client.chat.completions.create({
            model,
            max_tokens: maxTokens,
            stream: true,
            messages: [
              { role: 'system', content: enhancedSystem },
              { role: 'user', content: agent.buildPrompt(brief, trimContext(accumulatedContext)) },
            ],
          })

          for await (const chunk of agentStream) {
            const text = chunk.choices?.[0]?.delta?.content
            if (text) {
              agentOutput += text
              send({ type: 'chunk', agentId: agent.id, text })
            }
          }
        } catch (e) {
          agentOutput = `Error running agent: ${e}`
          send({ type: 'chunk', agentId: agent.id, text: agentOutput })
        }

        // Save agent memory and update stats
        const wordCount = agentOutput.split(/\s+/).length
        const elapsed = (Date.now() - startTime) / 1000
        const score = Math.min(100, Math.max(30, Math.round(70 + (wordCount > 200 ? 15 : 0) + (elapsed < 30 ? 10 : 0) + (agentOutput.includes('Error') ? -30 : 5))))

        try {
          const briefSummary = `${brief.clientName} — ${brief.industry || 'N/A'} — ${(brief.brief || '').slice(0, 150)}`
          const outputSummary = agentOutput.slice(0, 300)
          const learnings = extractLearnings(agentOutput, agent.name)

          saveAgentMemory({
            id: randomUUID(),
            agent_id: agent.id,
            agent_name: agent.name,
            project_name: brief.clientName || 'Unnamed Project',
            brief_summary: briefSummary,
            output_summary: outputSummary,
            learnings,
            performance_score: score,
            word_count: wordCount,
          })
          upsertAgentStats(agent.id, agent.name, wordCount, score)
        } catch { /* non-blocking */ }

        // Extract and broadcast visual brief after Creative Director
        if (agent.id === 2 && agentOutput) {
          const extracted = extractVisualBrief(agentOutput)
          if (extracted) {
            visualBrief = extracted
            send({ type: 'visual_brief', brief: extracted })
          }
        }

        setAgentDone(agent.id)
        accumulatedContext += `\n\n---\n## ${agent.name}:\n${agentOutput}`
        send({ type: 'agent_complete', agentId: agent.id, score, wordCount })
      }

      setRunComplete()

      send({ type: 'done' })
      controller.close()
    },
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'X-Accel-Buffering': 'no',
    },
  })
}

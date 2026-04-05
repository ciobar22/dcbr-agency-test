import Database from "better-sqlite3";
import { mkdirSync } from "fs";
import { join } from "path";
import { randomUUID } from "crypto";

// ── Types ───────────────────────────────────────────────────────────

export interface AgentMemory {
  id: string;
  agent_id: number;
  agent_name: string;
  project_name: string;
  brief_summary: string;
  output_summary: string;
  learnings: string;
  performance_score: number;
  word_count: number;
  created_at: string;
}

export interface AgentStats {
  agent_id: number;
  agent_name: string;
  total_tasks: number;
  avg_score: number;
  total_words: number;
  specializations: string;
  strengths: string;
  last_active: string;
  updated_at: string;
}

export interface Integration {
  id: string;
  type: 'google_analytics' | 'meta_ads' | 'search_console' | 'client_db';
  name: string;
  status: 'disconnected' | 'connected' | 'error';
  config: string; // JSON
  brand_id: string | null;
  last_sync: string | null;
  created_at: string;
  updated_at: string;
}

export interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  conversation_id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export interface Brand {
  id: string;
  name: string;
  industry: string | null;
  description: string | null;
  audience: string | null;
  website: string | null;
  tone: string | null;
  colors: string | null;
  keywords: string | null;
  created_at: string;
  updated_at: string;
}

export interface Content {
  id: string;
  brand_id: string | null;
  type: string;
  title: string;
  data: string;
  created_at: string;
}

export interface Task {
  id: string;
  type: string;
  status: "pending" | "running" | "completed" | "failed";
  input: string;
  output: string | null;
  brand_id: string | null;
  created_at: string;
  completed_at: string | null;
}

// ── Database singleton ──────────────────────────────────────────────

let db: Database.Database | null = null;

const DB_PATH = join(process.cwd(), "data", "jarvis.db");

export function getDb(): Database.Database {
  if (db) return db;

  mkdirSync(join(process.cwd(), "data"), { recursive: true });

  db = new Database(DB_PATH);
  db.pragma("journal_mode = WAL");
  db.pragma("foreign_keys = ON");

  db.exec(`
    CREATE TABLE IF NOT EXISTS conversations (
      id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS messages (
      id TEXT PRIMARY KEY,
      conversation_id TEXT NOT NULL,
      role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
      content TEXT NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS brands (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      industry TEXT,
      description TEXT,
      audience TEXT,
      website TEXT,
      tone TEXT,
      colors TEXT,
      keywords TEXT,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS content (
      id TEXT PRIMARY KEY,
      brand_id TEXT,
      type TEXT NOT NULL,
      title TEXT NOT NULL,
      data TEXT NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS integrations (
      id TEXT PRIMARY KEY,
      type TEXT NOT NULL,
      name TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'disconnected',
      config TEXT NOT NULL DEFAULT '{}',
      brand_id TEXT,
      last_sync TEXT,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS agent_memories (
      id TEXT PRIMARY KEY,
      agent_id INTEGER NOT NULL,
      agent_name TEXT NOT NULL,
      project_name TEXT NOT NULL,
      brief_summary TEXT NOT NULL DEFAULT '',
      output_summary TEXT NOT NULL DEFAULT '',
      learnings TEXT NOT NULL DEFAULT '',
      performance_score INTEGER NOT NULL DEFAULT 70,
      word_count INTEGER NOT NULL DEFAULT 0,
      created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS agent_stats (
      agent_id INTEGER PRIMARY KEY,
      agent_name TEXT NOT NULL,
      total_tasks INTEGER NOT NULL DEFAULT 0,
      avg_score REAL NOT NULL DEFAULT 0,
      total_words INTEGER NOT NULL DEFAULT 0,
      specializations TEXT NOT NULL DEFAULT '[]',
      strengths TEXT NOT NULL DEFAULT '[]',
      last_active TEXT,
      updated_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS tasks (
      id TEXT PRIMARY KEY,
      type TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'running', 'completed', 'failed')),
      input TEXT NOT NULL,
      output TEXT,
      brand_id TEXT,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      completed_at TEXT,
      FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE SET NULL
    );
  `);

  return db;
}

// ── Conversations ───────────────────────────────────────────────────

export function createConversation(id: string, title: string): Conversation {
  const db = getDb();
  db.prepare(
    "INSERT INTO conversations (id, title) VALUES (?, ?)"
  ).run(id, title);
  return db.prepare("SELECT * FROM conversations WHERE id = ?").get(id) as Conversation;
}

export function getConversations(): Conversation[] {
  return getDb()
    .prepare("SELECT * FROM conversations ORDER BY updated_at DESC")
    .all() as Conversation[];
}

export function getMessages(conversationId: string): Message[] {
  return getDb()
    .prepare("SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC")
    .all(conversationId) as Message[];
}

export function addMessage(
  id: string,
  conversationId: string,
  role: "user" | "assistant",
  content: string
): Message {
  const db = getDb();
  db.prepare(
    "INSERT INTO messages (id, conversation_id, role, content) VALUES (?, ?, ?, ?)"
  ).run(id, conversationId, role, content);
  db.prepare(
    "UPDATE conversations SET updated_at = datetime('now') WHERE id = ?"
  ).run(conversationId);
  return db.prepare("SELECT * FROM messages WHERE id = ?").get(id) as Message;
}

export function deleteConversation(id: string): void {
  getDb().prepare("DELETE FROM conversations WHERE id = ?").run(id);
}

// ── Brands ──────────────────────────────────────────────────────────

export function createBrand(brand: Omit<Brand, "created_at" | "updated_at">): Brand {
  const db = getDb();
  db.prepare(`
    INSERT INTO brands (id, name, industry, description, audience, website, tone, colors, keywords)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    brand.id,
    brand.name,
    brand.industry ?? null,
    brand.description ?? null,
    brand.audience ?? null,
    brand.website ?? null,
    brand.tone ?? null,
    brand.colors ?? null,
    brand.keywords ?? null
  );
  return db.prepare("SELECT * FROM brands WHERE id = ?").get(brand.id) as Brand;
}

export function getBrands(): Brand[] {
  return getDb().prepare("SELECT * FROM brands ORDER BY name ASC").all() as Brand[];
}

export function getBrand(id: string): Brand | undefined {
  return getDb().prepare("SELECT * FROM brands WHERE id = ?").get(id) as Brand | undefined;
}

export function updateBrand(
  id: string,
  data: Partial<Omit<Brand, "id" | "created_at" | "updated_at">>
): Brand | undefined {
  const db = getDb();
  const fields: string[] = [];
  const values: unknown[] = [];

  for (const [key, value] of Object.entries(data)) {
    fields.push(`${key} = ?`);
    values.push(value);
  }

  if (fields.length === 0) return getBrand(id);

  fields.push("updated_at = datetime('now')");
  values.push(id);

  db.prepare(`UPDATE brands SET ${fields.join(", ")} WHERE id = ?`).run(...values);
  return getBrand(id);
}

export function deleteBrand(id: string): void {
  getDb().prepare("DELETE FROM brands WHERE id = ?").run(id);
}

// ── Content ─────────────────────────────────────────────────────────

export function saveContent(
  id: string,
  brandId: string | null,
  type: string,
  title: string,
  data: string
): Content {
  const db = getDb();
  db.prepare(
    "INSERT INTO content (id, brand_id, type, title, data) VALUES (?, ?, ?, ?, ?)"
  ).run(id, brandId, type, title, data);
  return db.prepare("SELECT * FROM content WHERE id = ?").get(id) as Content;
}

export function getContents(brandId?: string, type?: string): Content[] {
  const conditions: string[] = [];
  const params: unknown[] = [];

  if (brandId) {
    conditions.push("brand_id = ?");
    params.push(brandId);
  }
  if (type) {
    conditions.push("type = ?");
    params.push(type);
  }

  const where = conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";
  return getDb()
    .prepare(`SELECT * FROM content ${where} ORDER BY created_at DESC`)
    .all(...params) as Content[];
}

export function getContent(id: string): Content | undefined {
  return getDb().prepare("SELECT * FROM content WHERE id = ?").get(id) as Content | undefined;
}

export function deleteContent(id: string): void {
  getDb().prepare("DELETE FROM content WHERE id = ?").run(id);
}

// ── Tasks ───────────────────────────────────────────────────────────

export function createTask(
  id: string,
  type: string,
  input: string,
  brandId?: string
): Task {
  const db = getDb();
  db.prepare(
    "INSERT INTO tasks (id, type, input, brand_id) VALUES (?, ?, ?, ?)"
  ).run(id, type, input, brandId ?? null);
  return db.prepare("SELECT * FROM tasks WHERE id = ?").get(id) as Task;
}

export function updateTask(
  id: string,
  status: Task["status"],
  output?: string
): Task | undefined {
  const db = getDb();
  if (status === "completed" || status === "failed") {
    db.prepare(
      "UPDATE tasks SET status = ?, output = ?, completed_at = datetime('now') WHERE id = ?"
    ).run(status, output ?? null, id);
  } else {
    db.prepare("UPDATE tasks SET status = ?, output = ? WHERE id = ?").run(
      status,
      output ?? null,
      id
    );
  }
  return db.prepare("SELECT * FROM tasks WHERE id = ?").get(id) as Task | undefined;
}

export function getTasks(status?: Task["status"]): Task[] {
  if (status) {
    return getDb()
      .prepare("SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC")
      .all(status) as Task[];
  }
  return getDb()
    .prepare("SELECT * FROM tasks ORDER BY created_at DESC")
    .all() as Task[];
}

// ── Integrations ───────────────────────────────────────────────────

export function getIntegrations(brandId?: string): Integration[] {
  if (brandId) {
    return getDb()
      .prepare("SELECT * FROM integrations WHERE brand_id = ? ORDER BY type ASC")
      .all(brandId) as Integration[];
  }
  return getDb()
    .prepare("SELECT * FROM integrations ORDER BY type ASC")
    .all() as Integration[];
}

export function getIntegration(id: string): Integration | undefined {
  return getDb().prepare("SELECT * FROM integrations WHERE id = ?").get(id) as Integration | undefined;
}

export function getIntegrationByType(type: string, brandId?: string): Integration | undefined {
  if (brandId) {
    return getDb().prepare("SELECT * FROM integrations WHERE type = ? AND brand_id = ?").get(type, brandId) as Integration | undefined;
  }
  return getDb().prepare("SELECT * FROM integrations WHERE type = ? AND brand_id IS NULL").get(type) as Integration | undefined;
}

export function upsertIntegration(id: string, type: string, name: string, config: string, brandId?: string): Integration {
  const db = getDb();
  const existing = getIntegration(id);
  if (existing) {
    db.prepare("UPDATE integrations SET config = ?, status = 'connected', last_sync = datetime('now'), updated_at = datetime('now') WHERE id = ?")
      .run(config, id);
  } else {
    db.prepare("INSERT INTO integrations (id, type, name, status, config, brand_id) VALUES (?, ?, ?, 'connected', ?, ?)")
      .run(id, type, name, config, brandId ?? null);
  }
  return getIntegration(id)!;
}

export function disconnectIntegration(id: string): void {
  getDb().prepare("UPDATE integrations SET status = 'disconnected', config = '{}', updated_at = datetime('now') WHERE id = ?").run(id);
}

export function deleteIntegration(id: string): void {
  getDb().prepare("DELETE FROM integrations WHERE id = ?").run(id);
}

export function updateIntegrationSync(id: string, status: 'connected' | 'error'): void {
  getDb().prepare("UPDATE integrations SET status = ?, last_sync = datetime('now'), updated_at = datetime('now') WHERE id = ?").run(status, id);
}

// ── Agent Memories ─────────────────────────────────────────────────

export function saveAgentMemory(memory: Omit<AgentMemory, "created_at">): AgentMemory {
  const db = getDb();
  db.prepare(`
    INSERT INTO agent_memories (id, agent_id, agent_name, project_name, brief_summary, output_summary, learnings, performance_score, word_count)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    memory.id, memory.agent_id, memory.agent_name, memory.project_name,
    memory.brief_summary, memory.output_summary, memory.learnings,
    memory.performance_score, memory.word_count
  );
  return db.prepare("SELECT * FROM agent_memories WHERE id = ?").get(memory.id) as AgentMemory;
}

export function getAgentMemories(agentId?: number): AgentMemory[] {
  if (agentId !== undefined) {
    return getDb()
      .prepare("SELECT * FROM agent_memories WHERE agent_id = ? ORDER BY created_at DESC")
      .all(agentId) as AgentMemory[];
  }
  return getDb()
    .prepare("SELECT * FROM agent_memories ORDER BY created_at DESC")
    .all() as AgentMemory[];
}

export function getAgentMemoriesForPrompt(agentId: number, limit = 5): AgentMemory[] {
  return getDb()
    .prepare("SELECT * FROM agent_memories WHERE agent_id = ? ORDER BY performance_score DESC, created_at DESC LIMIT ?")
    .all(agentId, limit) as AgentMemory[];
}

// ── Agent Stats ────────────────────────────────────────────────────

export function getAgentStats(): AgentStats[] {
  return getDb()
    .prepare("SELECT * FROM agent_stats ORDER BY agent_id ASC")
    .all() as AgentStats[];
}

export function getAgentStat(agentId: number): AgentStats | undefined {
  return getDb()
    .prepare("SELECT * FROM agent_stats WHERE agent_id = ?")
    .get(agentId) as AgentStats | undefined;
}

export function upsertAgentStats(agentId: number, agentName: string, wordCount: number, score: number): AgentStats {
  const db = getDb();
  const existing = getAgentStat(agentId);

  if (existing) {
    const newTotal = existing.total_tasks + 1;
    const newAvg = ((existing.avg_score * existing.total_tasks) + score) / newTotal;
    const newWords = existing.total_words + wordCount;
    db.prepare(`
      UPDATE agent_stats SET total_tasks = ?, avg_score = ?, total_words = ?, last_active = datetime('now'), updated_at = datetime('now')
      WHERE agent_id = ?
    `).run(newTotal, Math.round(newAvg * 10) / 10, newWords, agentId);
  } else {
    db.prepare(`
      INSERT INTO agent_stats (agent_id, agent_name, total_tasks, avg_score, total_words, last_active, updated_at)
      VALUES (?, ?, 1, ?, ?, datetime('now'), datetime('now'))
    `).run(agentId, agentName, score, wordCount);
  }
  return getAgentStat(agentId)!;
}

export function updateAgentSpecializations(agentId: number, specializations: string[], strengths: string[]): void {
  getDb().prepare(`
    UPDATE agent_stats SET specializations = ?, strengths = ?, updated_at = datetime('now')
    WHERE agent_id = ?
  `).run(JSON.stringify(specializations), JSON.stringify(strengths), agentId);
}

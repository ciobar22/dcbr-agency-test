'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

export type Lang = 'it' | 'en' | 'ru'

const translations: Record<string, Record<Lang, string>> = {
  // ── Global / Nav ──
  'nav.dashboard': { it: 'Dashboard', en: 'Dashboard', ru: 'Панель' },
  'nav.brands': { it: 'Brand', en: 'Brands', ru: 'Бренды' },
  'nav.jarvis': { it: 'JARVIS AI', en: 'JARVIS AI', ru: 'JARVIS AI' },
  'nav.online': { it: 'Online', en: 'Online', ru: 'Онлайн' },
  'nav.back': { it: '← Torna alla home', en: '← Back to home', ru: '← На главную' },
  'nav.back_short': { it: 'Indietro', en: 'Back', ru: 'Назад' },

  // ── Home ──
  'home.badge': { it: '16 Specialisti AI · Orchestratore Supervisore · 8 Aree', en: '16 AI Specialists · Supervisor Orchestrator · 8 Areas', ru: '16 ИИ-специалистов · Оркестратор-супервизор · 8 областей' },
  'home.title1': { it: 'La tua Agenzia', en: 'Your Agency', ru: 'Ваше Агентство' },
  'home.title2': { it: 'AI. Istantanea.', en: 'AI. Instant.', ru: 'ИИ. Мгновенно.' },
  'home.subtitle': { it: "Inserisci un brief — testo, URL o documento. L'Orchestratore AI supervisiona 11 specialisti in tempo reale: marketing, strategia, prodotto, ingegneria, finanza e operations.", en: 'Enter a brief — text, URL or document. The AI Orchestrator supervises 11 specialists in real time: marketing, strategy, product, engineering, finance and operations.', ru: 'Введите бриф — текст, URL или документ. ИИ-оркестратор контролирует 11 специалистов в реальном времени: маркетинг, стратегия, продукт, инженерия, финансы и операции.' },
  'home.cta': { it: 'Avvia una Campagna', en: 'Launch a Campaign', ru: 'Запустить кампанию' },
  'home.cta2': { it: 'Lancia la Tua Prima Campagna', en: 'Launch Your First Campaign', ru: 'Запустите первую кампанию' },
  'home.stats.agents': { it: 'AI Agents', en: 'AI Agents', ru: 'ИИ-агенты' },
  'home.stats.specs': { it: 'Specializzazioni', en: 'Specializations', ru: 'Специализации' },
  'home.stats.deliver': { it: 'Deliverable', en: 'Deliverables', ru: 'Результаты' },
  'home.stats.auto': { it: 'Automatizzato', en: 'Automated', ru: 'Автоматизация' },
  'home.how': { it: 'Come funziona', en: 'How it works', ru: 'Как это работает' },
  'home.how.title': { it: 'Tre passi per una strategia completa', en: 'Three steps to a complete strategy', ru: 'Три шага к полной стратегии' },
  'home.step1.label': { it: 'Inserisci il brief', en: 'Enter the brief', ru: 'Введите бриф' },
  'home.step1.desc': { it: 'Testo, URL o documento — il sistema assorbe tutto.', en: 'Text, URL or document — the system absorbs everything.', ru: 'Текст, URL или документ — система впитает всё.' },
  'home.step2.label': { it: 'Gli agent si attivano', en: 'Agents activate', ru: 'Агенты активируются' },
  'home.step2.desc': { it: "L'Orchestratore supervisiona 11 specialisti in sequenza.", en: 'The Orchestrator supervises 11 specialists in sequence.', ru: 'Оркестратор контролирует 11 специалистов последовательно.' },
  'home.step3.label': { it: 'Strategia completa', en: 'Complete strategy', ru: 'Полная стратегия' },
  'home.step3.desc': { it: 'Scarica un pacchetto marketing professionale e completo.', en: 'Download a complete professional marketing package.', ru: 'Скачайте полный профессиональный маркетинговый пакет.' },
  'home.team': { it: 'Il team', en: 'The team', ru: 'Команда' },
  'home.team.title': { it: 'Incontra i tuoi 16 specialisti', en: 'Meet your 16 specialists', ru: 'Познакомьтесь с 16 специалистами' },
  'home.cat.all': { it: 'Tutti', en: 'All', ru: 'Все' },
  'home.cat.marketing': { it: 'Marketing', en: 'Marketing', ru: 'Маркетинг' },
  'home.cat.growth': { it: 'Growth', en: 'Growth', ru: 'Рост' },
  'home.cat.clevel': { it: 'C-Level', en: 'C-Level', ru: 'Топ-менеджмент' },
  'home.cat.product': { it: 'Product', en: 'Product', ru: 'Продукт' },
  'home.cat.engineering': { it: 'Engineering', en: 'Engineering', ru: 'Инженерия' },
  'home.cat.finance': { it: 'Finance', en: 'Finance', ru: 'Финансы' },
  'home.cat.operations': { it: 'Operations', en: 'Operations', ru: 'Операции' },

  // ── Brief Form ──
  'form.title': { it: 'Nuovo Brief di Progetto', en: 'New Project Brief', ru: 'Новый бриф проекта' },
  'form.subtitle': { it: 'Testo libero, URL o documento — scegli il tuo formato', en: 'Free text, URL or document — choose your format', ru: 'Текст, URL или документ — выберите формат' },
  'form.tab.text': { it: 'Testo', en: 'Text', ru: 'Текст' },
  'form.tab.url': { it: 'URL Web', en: 'Web URL', ru: 'URL сайта' },
  'form.tab.file': { it: 'Documento', en: 'Document', ru: 'Документ' },
  'form.brief.label': { it: 'Brief della Campagna', en: 'Campaign Brief', ru: 'Бриф кампании' },
  'form.brief.placeholder': { it: 'Descrivi il brand, prodotto, servizio o idea di campagna...', en: 'Describe the brand, product, service or campaign idea...', ru: 'Опишите бренд, продукт, услугу или идею кампании...' },
  'form.client.label': { it: 'Cliente / Brand', en: 'Client / Brand', ru: 'Клиент / Бренд' },
  'form.industry.label': { it: 'Settore', en: 'Industry', ru: 'Отрасль' },
  'form.industry.placeholder': { it: 'Seleziona settore', en: 'Select industry', ru: 'Выберите отрасль' },
  'form.audience.label': { it: 'Target Audience', en: 'Target Audience', ru: 'Целевая аудитория' },
  'form.budget.label': { it: 'Budget Mensile', en: 'Monthly Budget', ru: 'Месячный бюджет' },
  'form.budget.placeholder': { it: 'Seleziona budget', en: 'Select budget', ru: 'Выберите бюджет' },
  'form.website.label': { it: 'Website URL', en: 'Website URL', ru: 'URL сайта' },
  'form.goals.label': { it: 'Obiettivo Principale', en: 'Main Goal', ru: 'Главная цель' },
  'form.submit': { it: 'Attiva Orchestratore + 11 Agenti', en: 'Activate Orchestrator + 11 Agents', ru: 'Активировать оркестратор + 11 агентов' },
  'form.activating': { it: 'Attivazione in corso...', en: 'Activating...', ru: 'Активация...' },
  'form.url.label': { it: 'URL del sito o pagina', en: 'Website or page URL', ru: 'URL сайта или страницы' },
  'form.url.analyze': { it: 'Analizza', en: 'Analyze', ru: 'Анализ' },
  'form.url.analyzing': { it: 'Analisi...', en: 'Analyzing...', ru: 'Анализ...' },
  'form.file.drop': { it: 'Trascina o clicca per caricare', en: 'Drag or click to upload', ru: 'Перетащите или нажмите для загрузки' },
  'form.file.release': { it: 'Rilascia qui', en: 'Drop here', ru: 'Отпустите здесь' },
  'form.file.processing': { it: 'Elaborazione in corso...', en: 'Processing...', ru: 'Обработка...' },
  'form.extracted': { it: 'Estratto automaticamente — modifica se vuoi', en: 'Auto-extracted — edit if needed', ru: 'Извлечено автоматически — редактируйте при необходимости' },
  'form.chars': { it: 'caratteri', en: 'characters', ru: 'символов' },
  'form.chars_more': { it: 'ancora', en: 'more', ru: 'ещё' },
  'form.network_error': { it: 'Errore di rete. Riprova.', en: 'Network error. Try again.', ru: 'Ошибка сети. Попробуйте снова.' },
  'form.file_error': { it: "Errore durante l'elaborazione del file.", en: 'Error processing file.', ru: 'Ошибка обработки файла.' },

  // ── Run page ──
  'run.agency': { it: 'DCBR Marketing Agency', en: 'DCBR Marketing Agency', ru: 'DCBR Marketing Agency' },
  'run.complete': { it: 'Campagna Completata!', en: 'Campaign Complete!', ru: 'Кампания завершена!' },
  'run.complete_desc': { it: "agenti hanno lavorato per", en: 'agents worked for', ru: 'агентов работали для' },
  'run.orchestrator_verdict': { it: "L'Orchestratore AI ha prodotto la sintesi finale.", en: 'The AI Orchestrator produced the final synthesis.', ru: 'ИИ-оркестратор подготовил финальный синтез.' },
  'run.download': { it: 'Scarica Report', en: 'Download Report', ru: 'Скачать отчёт' },
  'run.download_all': { it: 'Scarica Tutto', en: 'Download All', ru: 'Скачать всё' },
  'run.synthesis': { it: 'Sintesi AI', en: 'AI Synthesis', ru: 'Синтез ИИ' },
  'run.working': { it: 'Agenzia al Lavoro', en: 'Agency Working', ru: 'Агентство работает' },
  'run.orchestrator_active': { it: 'Orchestratore Attivo', en: 'Orchestrator Active', ru: 'Оркестратор активен' },
  'run.init': { it: 'Inizializzazione...', en: 'Initializing...', ru: 'Инициализация...' },
  'run.pipeline': { it: 'Pipeline Specialisti', en: 'Specialist Pipeline', ru: 'Конвейер специалистов' },
  'run.monitored': { it: 'Pipeline monitorata', en: 'Monitored pipeline', ru: 'Контролируемый конвейер' },
  'run.waiting': { it: 'In attesa che gli agenti precedenti completino...', en: 'Waiting for previous agents to finish...', ru: 'Ожидание завершения предыдущих агентов...' },
  'run.starting': { it: 'Avvio in corso...', en: 'Starting...', ru: 'Запуск...' },
  'run.processing': { it: 'In elaborazione...', en: 'Processing...', ru: 'Обработка...' },
  'run.in_wait': { it: 'In attesa', en: 'Waiting', ru: 'Ожидание' },
  'run.words': { it: 'parole', en: 'words', ru: 'слов' },
  'run.copy': { it: 'Copia output', en: 'Copy output', ru: 'Копировать' },
  'run.copied': { it: 'Copiato!', en: 'Copied!', ru: 'Скопировано!' },
  'run.read_all': { it: 'Leggi tutto →', en: 'Read all →', ru: 'Читать всё →' },
  'run.click_synthesis': { it: 'Clicca per vedere la sintesi finale →', en: 'Click to see final synthesis →', ru: 'Нажмите для финального синтеза →' },
  'run.error': { it: 'Errore di connessione. Ricarica la pagina.', en: 'Connection error. Reload the page.', ru: 'Ошибка соединения. Перезагрузите страницу.' },
  'run.complete_all': { it: 'Campagna completa — tutti i', en: 'Campaign complete — all', ru: 'Кампания завершена — все' },
  'run.delivered': { it: 'agenti hanno consegnato', en: 'agents have delivered', ru: 'агентов доставили результат' },

  // ── JARVIS ──
  'jarvis.title': { it: 'JARVIS', en: 'JARVIS', ru: 'JARVIS' },
  'jarvis.subtitle': { it: 'DCBR Marketing Intelligence', en: 'DCBR Marketing Intelligence', ru: 'DCBR Маркетинг-интеллект' },
  'jarvis.online': { it: 'Online', en: 'Online', ru: 'Онлайн' },
  'jarvis.processing': { it: 'Elaborazione...', en: 'Processing...', ru: 'Обработка...' },
  'jarvis.booting': { it: 'Avvio...', en: 'Booting...', ru: 'Загрузка...' },
  'jarvis.welcome': { it: 'Ciao, sono', en: "Hi, I'm", ru: 'Привет, я' },
  'jarvis.desc': { it: 'La tua AI di marketing. Dimmi cosa ti serve — piano editoriale, campagna, copy, SEO, analytics — e lo creo subito.', en: 'Your marketing AI. Tell me what you need — editorial plan, campaign, copy, SEO, analytics — and I\'ll create it right away.', ru: 'Ваш маркетинговый ИИ. Скажите, что нужно — редакционный план, кампания, копирайт, SEO, аналитика — и я сделаю сразу.' },
  'jarvis.voice_hint': { it: 'Dì', en: 'Say', ru: 'Скажите' },
  'jarvis.voice_hint2': { it: '+ il tuo comando per attivare la voce', en: '+ your command to activate voice', ru: '+ вашу команду для голосового ввода' },
  'jarvis.input_placeholder': { it: 'Scrivi a JARVIS... o premi il microfono', en: 'Write to JARVIS... or press the mic', ru: 'Напишите JARVIS... или нажмите микрофон' },
  'jarvis.input_listening': { it: 'Parla... dì "Jarvis" + il comando', en: 'Speak... say "Jarvis" + command', ru: 'Говорите... скажите "Jarvis" + команду' },
  'jarvis.thinking': { it: 'JARVIS sta elaborando...', en: 'JARVIS is processing...', ru: 'JARVIS обрабатывает...' },
  'jarvis.shift_enter': { it: 'Shift+Enter per andare a capo', en: 'Shift+Enter for new line', ru: 'Shift+Enter — новая строка' },
  'jarvis.mic_active': { it: 'Microfono attivo — dì "Jarvis" per un comando rapido', en: 'Mic active — say "Jarvis" for a quick command', ru: 'Микрофон активен — скажите "Jarvis" для быстрой команды' },
  'jarvis.generate': { it: 'Genera completo', en: 'Generate complete', ru: 'Сгенерировать полностью' },
  'jarvis.tts_on': { it: 'Voce attiva', en: 'Voice on', ru: 'Голос вкл' },
  'jarvis.tts_off': { it: 'Voce disattivata', en: 'Voice off', ru: 'Голос выкл' },
  'jarvis.voice_lang': { it: 'Lingua voce', en: 'Voice language', ru: 'Язык голоса' },
  'jarvis.voice_select': { it: 'Scegli voce', en: 'Choose voice', ru: 'Выберите голос' },
  'jarvis.no_voices': { it: 'Nessuna voce disponibile', en: 'No voices available', ru: 'Нет доступных голосов' },
  'jarvis.new_chat': { it: 'Nuova conversazione', en: 'New conversation', ru: 'Новый чат' },
  'jarvis.download_pdf': { it: 'Scarica PDF', en: 'Download PDF', ru: 'Скачать PDF' },

  // ── Quick actions ──
  'qa.editorial': { it: 'Piano Editoriale', en: 'Editorial Plan', ru: 'Редакционный план' },
  'qa.campaign': { it: 'Campagna Marketing', en: 'Marketing Campaign', ru: 'Маркетинговая кампания' },
  'qa.email': { it: 'Sequenza Email', en: 'Email Sequence', ru: 'Email-рассылка' },
  'qa.copy': { it: 'Copy & Headline', en: 'Copy & Headlines', ru: 'Копирайт и заголовки' },
  'qa.seo': { it: 'Strategia SEO', en: 'SEO Strategy', ru: 'SEO-стратегия' },
  'qa.brand': { it: 'Brand Strategy', en: 'Brand Strategy', ru: 'Бренд-стратегия' },
  'qa.kpi': { it: 'KPI Dashboard', en: 'KPI Dashboard', ru: 'KPI-панель' },
  'qa.social': { it: 'Social Strategy', en: 'Social Strategy', ru: 'Соцсети-стратегия' },
  'qa.report': { it: 'Report Cliente', en: 'Client Report', ru: 'Отчёт клиенту' },
  'qa.editorial.prompt': { it: 'Crea un piano editoriale completo per 4 settimane per ', en: 'Create a complete 4-week editorial plan for ', ru: 'Создай полный редакционный план на 4 недели для ' },
  'qa.campaign.prompt': { it: 'Crea una campagna marketing completa per ', en: 'Create a complete marketing campaign for ', ru: 'Создай полную маркетинговую кампанию для ' },
  'qa.email.prompt': { it: 'Crea una sequenza di 5 email di nurturing per ', en: 'Create a 5-email nurturing sequence for ', ru: 'Создай серию из 5 nurturing-писем для ' },
  'qa.copy.prompt': { it: 'Scrivi 10 headline per ads + 5 tagline per ', en: 'Write 10 ad headlines + 5 taglines for ', ru: 'Напиши 10 заголовков для рекламы + 5 слоганов для ' },
  'qa.seo.prompt': { it: 'Crea una strategia SEO completa per ', en: 'Create a complete SEO strategy for ', ru: 'Создай полную SEO-стратегию для ' },
  'qa.brand.prompt': { it: 'Definisci il posizionamento e la brand strategy per ', en: 'Define positioning and brand strategy for ', ru: 'Определи позиционирование и бренд-стратегию для ' },
  'qa.kpi.prompt': { it: 'Progetta il KPI dashboard e il piano di tracking per ', en: 'Design the KPI dashboard and tracking plan for ', ru: 'Спроектируй KPI-панель и план отслеживания для ' },
  'qa.social.prompt': { it: 'Crea la strategia social media completa per ', en: 'Create a complete social media strategy for ', ru: 'Создай полную стратегию для соцсетей для ' },
  'qa.report.prompt': { it: 'Prepara un report professionale per il cliente ', en: 'Prepare a professional report for client ', ru: 'Подготовь профессиональный отчёт для клиента ' },

  // ── Dashboard ──
  'dash.welcome': { it: 'Benvenuto nel Centro di Comando', en: 'Welcome to Command Center', ru: 'Добро пожаловать в Центр управления' },
  'dash.desc': { it: 'Gestisci brand, conversazioni, contenuti generati e workflow da un unico punto.', en: 'Manage brands, conversations, generated content and workflows from a single point.', ru: 'Управляйте брендами, диалогами, контентом и процессами из одной точки.' },
  'dash.conversations': { it: 'Conversazioni', en: 'Conversations', ru: 'Диалоги' },
  'dash.brands': { it: 'Brand', en: 'Brands', ru: 'Бренды' },
  'dash.contents': { it: 'Contenuti', en: 'Contents', ru: 'Контент' },
  'dash.tasks_done': { it: 'Task completati', en: 'Tasks completed', ru: 'Выполнено задач' },
  'dash.quick': { it: 'Azioni rapide', en: 'Quick actions', ru: 'Быстрые действия' },
  'dash.talk_jarvis': { it: 'Parla con JARVIS', en: 'Talk to JARVIS', ru: 'Поговорить с JARVIS' },
  'dash.talk_desc': { it: 'Chat + voce', en: 'Chat + voice', ru: 'Чат + голос' },
  'dash.new_campaign': { it: 'Nuova Campagna', en: 'New Campaign', ru: 'Новая кампания' },
  'dash.new_campaign_desc': { it: '12 agenti AI', en: '12 AI agents', ru: '12 ИИ-агентов' },
  'dash.manage_brands': { it: 'Gestisci Brand', en: 'Manage Brands', ru: 'Управление брендами' },
  'dash.manage_brands_desc': { it: 'Multi-brand', en: 'Multi-brand', ru: 'Мульти-бренд' },
  'dash.saved_content': { it: 'Contenuti Salvati', en: 'Saved Content', ru: 'Сохранённый контент' },
  'dash.saved_content_desc': { it: 'Piani e report', en: 'Plans & reports', ru: 'Планы и отчёты' },
  'dash.recent_conv': { it: 'Conversazioni Recenti', en: 'Recent Conversations', ru: 'Недавние диалоги' },
  'dash.your_brands': { it: 'I tuoi Brand', en: 'Your Brands', ru: 'Ваши бренды' },
  'dash.no_conv': { it: 'Nessuna conversazione', en: 'No conversations', ru: 'Нет диалогов' },
  'dash.start_jarvis': { it: 'Inizia a parlare con JARVIS →', en: 'Start talking to JARVIS →', ru: 'Начните общение с JARVIS →' },
  'dash.no_brands': { it: 'Nessun brand configurato', en: 'No brands configured', ru: 'Нет настроенных брендов' },
  'dash.add_first': { it: 'Aggiungi il primo brand →', en: 'Add your first brand →', ru: 'Добавьте первый бренд →' },
  'dash.new': { it: '+ Nuova', en: '+ New', ru: '+ Новый' },
  'dash.add': { it: '+ Aggiungi', en: '+ Add', ru: '+ Добавить' },
  'dash.minds': { it: 'Mappa Mentale', en: 'Mind Map', ru: 'Карта разума' },
  'dash.minds_desc': { it: 'Rete neurale AI', en: 'AI Neural Network', ru: 'Нейросеть ИИ' },
  'dash.integrations': { it: 'Integrazioni', en: 'Integrations', ru: 'Интеграции' },
  'dash.integrations_desc': { it: 'GA4, Meta, GSC', en: 'GA4, Meta, GSC', ru: 'GA4, Meta, GSC' },
  'dash.projects': { it: 'Storico Progetti', en: 'Project History', ru: 'История проектов' },
  'dash.projects_desc': { it: 'Progetti passati e memorie', en: 'Past projects & memories', ru: 'Прошлые проекты' },
  'dash.generated': { it: 'Contenuti Generati', en: 'Generated Content', ru: 'Сгенерированный контент' },
  'dash.see_all': { it: 'Vedi tutti →', en: 'See all →', ru: 'Все →' },
  'dash.loading': { it: 'Caricamento...', en: 'Loading...', ru: 'Загрузка...' },
  'dash.sector_na': { it: 'Settore non specificato', en: 'Industry not specified', ru: 'Отрасль не указана' },
  'dash.command': { it: 'Centro di comando', en: 'Command center', ru: 'Центр управления' },

  // ── Brands page ──
  'brands.title': { it: 'Gestione Brand', en: 'Brand Management', ru: 'Управление брендами' },
  'brands.add': { it: 'Aggiungi Brand', en: 'Add Brand', ru: 'Добавить бренд' },
  'brands.edit': { it: 'Modifica Brand', en: 'Edit Brand', ru: 'Редактировать бренд' },
  'brands.name': { it: 'Nome Brand', en: 'Brand Name', ru: 'Название бренда' },
  'brands.industry': { it: 'Settore', en: 'Industry', ru: 'Отрасль' },
  'brands.desc': { it: 'Descrizione', en: 'Description', ru: 'Описание' },
  'brands.audience': { it: 'Target Audience', en: 'Target Audience', ru: 'Целевая аудитория' },
  'brands.website': { it: 'Sito Web', en: 'Website', ru: 'Сайт' },
  'brands.tone': { it: 'Tono di Voce', en: 'Tone of Voice', ru: 'Тон общения' },
  'brands.colors': { it: 'Colori Brand (hex)', en: 'Brand Colors (hex)', ru: 'Цвета бренда (hex)' },
  'brands.keywords': { it: 'Keywords', en: 'Keywords', ru: 'Ключевые слова' },
  'brands.save': { it: 'Salva', en: 'Save', ru: 'Сохранить' },
  'brands.saving': { it: 'Salvataggio...', en: 'Saving...', ru: 'Сохранение...' },
  'brands.cancel': { it: 'Annulla', en: 'Cancel', ru: 'Отмена' },
  'brands.delete_confirm': { it: 'Sei sicuro di voler eliminare questo brand?', en: 'Are you sure you want to delete this brand?', ru: 'Вы уверены, что хотите удалить этот бренд?' },
  'brands.use_jarvis': { it: 'Usa con JARVIS', en: 'Use with JARVIS', ru: 'Использовать с JARVIS' },
  'brands.no_brands': { it: 'Nessun brand ancora', en: 'No brands yet', ru: 'Пока нет брендов' },
  'brands.no_brands_desc': { it: 'Crea il tuo primo brand per personalizzare le strategie di JARVIS.', en: 'Create your first brand to customize JARVIS strategies.', ru: 'Создайте первый бренд для персонализации стратегий JARVIS.' },

  // ── Minds page ──
  'minds.title': { it: 'Mappa Mentale', en: 'Mind Map', ru: 'Карта разума' },
  'minds.subtitle': { it: 'Rete neurale degli agenti DCBR', en: 'DCBR Agent Neural Network', ru: 'Нейронная сеть агентов DCBR' },
  'minds.agents': { it: 'Menti', en: 'Minds', ru: 'Разумы' },
  'minds.tasks': { it: 'Task', en: 'Tasks', ru: 'Задачи' },
  'minds.words': { it: 'Parole', en: 'Words', ru: 'Слова' },
  'minds.avg_score': { it: 'Score Medio', en: 'Avg Score', ru: 'Ср. балл' },
  'minds.score': { it: 'Score', en: 'Score', ru: 'Балл' },
  'minds.memory': { it: 'Memoria & Apprendimento', en: 'Memory & Learning', ru: 'Память и обучение' },
  'minds.entries': { it: 'ricordi', en: 'memories', ru: 'воспоминаний' },
  'minds.no_memory': { it: 'Nessuna memoria', en: 'No memories yet', ru: 'Пока нет воспоминаний' },
  'minds.no_memory_desc': { it: 'Questo agente impara ad ogni progetto', en: 'This agent learns from each project', ru: 'Этот агент учится на каждом проекте' },
  'minds.specializations': { it: 'Specializzazioni', en: 'Specializations', ru: 'Специализации' },
  'minds.strengths': { it: 'Punti di Forza', en: 'Strengths', ru: 'Сильные стороны' },
  'minds.footprint': { it: 'Footprint Performance', en: 'Performance Footprint', ru: 'Отпечаток производительности' },
  'minds.no_data': { it: 'Nessun dato', en: 'No data', ru: 'Нет данных' },
  'minds.empty': { it: 'Le menti iniziano a imparare con il primo progetto', en: 'Minds start learning with the first project', ru: 'Разумы начнут обучаться с первым проектом' },
  'minds.launch_first': { it: 'Lancia la prima campagna', en: 'Launch first campaign', ru: 'Запустите первую кампанию' },
  'minds.working_now': { it: 'Agenti al lavoro', en: 'Agents working', ru: 'Агенты работают' },
  'minds.active': { it: 'attivi', en: 'active', ru: 'активных' },
  'minds.completed': { it: 'completati', en: 'completed', ru: 'завершено' },

  // ── Integrations page ──
  'int.title': { it: 'Integrazioni', en: 'Integrations', ru: 'Интеграции' },
  'int.subtitle': { it: 'Connetti i tuoi servizi', en: 'Connect your services', ru: 'Подключите сервисы' },
  'int.heading': { it: 'Connetti i tuoi dati reali', en: 'Connect your real data', ru: 'Подключите реальные данные' },
  'int.desc': { it: 'Collega Google Analytics, Meta Ads, Search Console e il database del cliente per dare ai tuoi agenti AI accesso a dati reali e generare strategie basate su numeri concreti.', en: 'Connect Google Analytics, Meta Ads, Search Console and client database to give your AI agents access to real data and generate strategies based on concrete numbers.', ru: 'Подключите Google Analytics, Meta Ads, Search Console и базу данных клиента, чтобы ИИ-агенты работали с реальными данными.' },
  'int.connected': { it: 'connessi', en: 'connected', ru: 'подключено' },
  'int.active': { it: 'Connesso', en: 'Connected', ru: 'Подключено' },
  'int.error': { it: 'Errore', en: 'Error', ru: 'Ошибка' },
  'int.last_sync': { it: 'Ultima sync', en: 'Last sync', ru: 'Посл. синхр.' },
  'int.disconnect': { it: 'Disconnetti', en: 'Disconnect', ru: 'Отключить' },
  'int.connect': { it: 'Connetti', en: 'Connect', ru: 'Подключить' },
  'int.connecting': { it: 'Connessione...', en: 'Connecting...', ru: 'Подключение...' },
  'int.security': { it: 'Le credenziali sono salvate localmente e criptate. Non vengono mai inviate a terzi.', en: 'Credentials are stored locally and encrypted. Never sent to third parties.', ru: 'Учётные данные хранятся локально и зашифрованы. Никогда не передаются третьим лицам.' },
  'int.how_title': { it: 'Come funziona', en: 'How it works', ru: 'Как это работает' },
  'int.how1_title': { it: 'Connetti', en: 'Connect', ru: 'Подключите' },
  'int.how1_desc': { it: 'Inserisci le credenziali API del servizio. Supportiamo OAuth e Service Account.', en: 'Enter the service API credentials. We support OAuth and Service Account.', ru: 'Введите учётные данные API. Поддерживаем OAuth и Service Account.' },
  'int.how2_title': { it: 'Sync automatica', en: 'Auto sync', ru: 'Авто-синхр.' },
  'int.how2_desc': { it: 'I dati vengono importati e aggiornati automaticamente ad ogni analisi.', en: 'Data is imported and updated automatically with each analysis.', ru: 'Данные импортируются и обновляются автоматически при каждом анализе.' },
  'int.how3_title': { it: 'AI potenziata', en: 'Enhanced AI', ru: 'Усиленный ИИ' },
  'int.how3_desc': { it: 'JARVIS e gli agenti usano i dati reali per strategie concrete e personalizzate.', en: 'JARVIS and agents use real data for concrete, personalized strategies.', ru: 'JARVIS и агенты используют реальные данные для конкретных стратегий.' },

  // ── Contents page ──
  'contents.title': { it: 'Contenuti Generati', en: 'Generated Content', ru: 'Сгенерированный контент' },
  'contents.saved': { it: 'elementi salvati', en: 'saved items', ru: 'сохранённых элементов' },
  'contents.all': { it: 'Tutti', en: 'All', ru: 'Все' },
  'contents.no_content': { it: 'Nessun contenuto', en: 'No content', ru: 'Нет контента' },
  'contents.hint': { it: 'I contenuti generati con JARVIS appariranno qui', en: 'Content generated with JARVIS will appear here', ru: 'Контент от JARVIS появится здесь' },
  'contents.select': { it: 'Seleziona un contenuto per visualizzarlo', en: 'Select content to view it', ru: 'Выберите контент для просмотра' },
  'contents.copy': { it: 'Copia', en: 'Copy', ru: 'Копировать' },
  'contents.copied': { it: 'Copiato', en: 'Copied', ru: 'Скопировано' },
  'contents.download': { it: 'Scarica', en: 'Download', ru: 'Скачать' },
  'contents.delete': { it: 'Elimina', en: 'Delete', ru: 'Удалить' },
}

// ── Context ──
interface I18nContextType {
  lang: Lang
  setLang: (lang: Lang) => void
  t: (key: string) => string
}

const I18nContext = createContext<I18nContextType>({
  lang: 'it',
  setLang: () => {},
  t: (key: string) => key,
})

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>('it')

  useEffect(() => {
    const saved = localStorage.getItem('dcbr_lang') as Lang | null
    if (saved && ['it', 'en', 'ru'].includes(saved)) {
      setLangState(saved)
    }
  }, [])

  const setLang = (l: Lang) => {
    setLangState(l)
    localStorage.setItem('dcbr_lang', l)
  }

  const t = (key: string): string => {
    return translations[key]?.[lang] || translations[key]?.['it'] || key
  }

  return (
    <I18nContext.Provider value={{ lang, setLang, t }}>
      {children}
    </I18nContext.Provider>
  )
}

export function useI18n() {
  return useContext(I18nContext)
}

// ── Language Switcher Component ──
const LANGS: { id: Lang; label: string; flag: string }[] = [
  { id: 'it', label: 'Italiano', flag: '🇮🇹' },
  { id: 'en', label: 'English', flag: '🇬🇧' },
  { id: 'ru', label: 'Русский', flag: '🇷🇺' },
]

export function LangSwitcher() {
  const { lang, setLang } = useI18n()
  const [open, setOpen] = useState(false)
  const current = LANGS.find(l => l.id === lang)!

  return (
    <div style={{ position: 'relative' }}>
      <button
        onClick={() => setOpen(!open)}
        style={{
          display: 'flex', alignItems: 'center', gap: '6px',
          padding: '5px 12px', borderRadius: '999px',
          background: 'rgba(255,255,255,0.04)',
          border: '1px solid rgba(255,255,255,0.1)',
          color: '#94a3b8', fontSize: '12px', fontWeight: 600,
          cursor: 'pointer', transition: 'all 0.2s',
        }}
      >
        <span style={{ fontSize: '14px' }}>{current.flag}</span>
        <span>{current.id.toUpperCase()}</span>
      </button>

      {open && (
        <>
          <div onClick={() => setOpen(false)} style={{ position: 'fixed', inset: 0, zIndex: 90 }} />
          <div style={{
            position: 'absolute', top: '100%', right: 0, marginTop: '6px',
            background: 'rgba(13,21,38,0.98)', backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px',
            padding: '4px', zIndex: 100, minWidth: '140px',
            boxShadow: '0 16px 40px rgba(0,0,0,0.5)',
          }}>
            {LANGS.map(l => (
              <button key={l.id}
                onClick={() => { setLang(l.id); setOpen(false) }}
                style={{
                  display: 'flex', alignItems: 'center', gap: '10px', width: '100%',
                  padding: '9px 14px', borderRadius: '8px', border: 'none',
                  cursor: 'pointer', fontSize: '13px', textAlign: 'left',
                  background: lang === l.id ? 'rgba(124,58,237,0.15)' : 'transparent',
                  color: lang === l.id ? '#c084fc' : '#94a3b8',
                  fontWeight: lang === l.id ? 700 : 500,
                  transition: 'all 0.15s',
                }}
              >
                <span style={{ fontSize: '16px' }}>{l.flag}</span>
                {l.label}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

## 🌐 Overall Vision
A local AI-driven Job Search Assistant that:
* Runs daily (scheduled task)
* Finds new job postings matching your preferences
* Summarizes each role + company
* Emails you a digest of opportunities with actionable checkboxes
* Generates custom materials (resume, cover letter, summary table) for your selected roles
* Lets you track application progress and recall details later
* Provides interview prep when callbacks happen

## 🧱 Architecture (High-Level Overview)
### 🧩 Core Components
| Layer | Purpose | Tools/Libraries | Status |
|----|----|----|----|
| Orchestration / Agent Framework | Manages autonomous agents & workflow | LangGraph | MVP in progress:<br>`src/main.py` |
| Data Retrieval | Scrape or query job boards | SerpAPI, RemoteOK + BeautifulSoup4 | MVP complete |
| Persistence | Store job summaries, choices, statuses | SQLite | done:<br>* JobSearchQuery<br>* JobPosting<br>* JobSummary<br><br>todo:<br>* app materials<br>* app tracking<br>* interview prep |
| Task Scheduling | Automate daily runs | cron | *not started* |
| Email Interface | Send/receive daily summary + selection | Gmail API | *not started* |
| LLM Integration | Summarization, resume/cover generation, interview prep | LangChain[openai, ollama] | MVP complete (ollama & Azure OpenAI) |
| Frontend / Local UI | View & update applications | Streamlit | done:<br>* view new jobs<br>* home page placeholder<br><br>todo:<br>* app tracking<br>* interview prep |  

### ⚙️ Application Workflow
| Service/Agent | Responsibilities | Key Inputs/Outputs | Status |
|----|----|----|----|
| 🕵️ Job Discovery Service | Crawl job boards daily, filter by requirements | → list of raw job postings | MVP complete |
| 🧾 Summarizer Agent | Generate concise job & company summaries | raw job → summarized description | MVP complete |
| 📧 Notifier Service | Compose HTML email with summaries + selection checkboxes | summaries → email digest |  |
| ✅ Selection Listener Service | Collect user selections from email/web form | selected jobs → trigger next stage |  |
| ✍️ Application Writer Agent | Tailor resume & cover letter for each selected role | job info + base resume → .pdf & .docx |  |
| 📊 Tracker Service | Maintain status table (Applied, Interviewing, Offer) | updates persisted in local DB |  |
| 🎯 Interview Coach Agent | Generate interview prep based on job + submitted materials | job data + materials → prep doc |  |
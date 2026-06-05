<details>
<summary><b>🇹🇷 Türkçe Proje Özeti (Tıklayın)</b></summary>


# Freelancer Proposal Agent

LangGraph ile geliştirilmiş, **yerel HuggingFace modeli** kullanan agentic bir proposal yazma sistemi.  
Kullanıcıdan iş ilanı alır, fine-tune edilmiş yerel model ile kazandırıcı bir freelance proposal üretir.

> Proje aktif geliştirme aşamasındadır. Kodex ile geliştirilmektedir.

---

## Nasıl Çalışır

```
Kullanıcı (iş ilanı girer)
        ↓
  Router Agent       ← intent tespiti
        ↓
Freelance Agent      ← proposal üretimi
        ↓
   [HuggingFace      ← yerel model inference
    local model]
        ↓
  Çıktı / Dosya
```

---

## Teknoloji Yığını

| Katman              | Araç                              |
|---------------------|-----------------------------------|
| Agent framework     | LangGraph                         |
| LLM (yerel)         | HuggingFace Transformers + PEFT   |
| Base model          | Mistral-7B (LoRA fine-tune)       |
| LangChain bağlantısı| `langchain-huggingface`           |
| Dil                 | Python 3.11+                      |
| Ortam yönetimi      | python-dotenv                     |
| Experiment tracking | MLflow *(sonraki aşama)*          |

---

## Kurulum

```bash
git clone https://github.com/yunusemreerken/Simple-Agent.git
cd Simple-Agent

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

`.env` dosyası oluştur:

```bash
cp .env.example .env
```

`.env` içeriği:

```
# HuggingFace model path veya HF Hub model adı
HF_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2

# HuggingFace Hub'dan indirmek için (opsiyonel, gated model değilse gerekmez)
HUGGINGFACE_TOKEN=hf_...

# LangSmith izleme (opsiyonel)
LANGCHAIN_API_KEY=...
LANGCHAIN_TRACING_V2=false
```

Çalıştır:

```bash
python main.py
```

---

## Proje Yapısı

```
Simple-Agent/
├── agents/
│   ├── router.py            # intent tespiti → freelance'a yönlendirir
│   └── freelance_agent.py   # proposal üretimi
├── tools/
│   └── file_writer.py       # üretilen proposal'ı dosyaya kaydeder
├── model/
│   └── loader.py            # HuggingFace model yükleme (local / Hub)
├── state.py                 # paylaşılan State tanımı
├── graph.py                 # LangGraph graph kurulumu
├── main.py                  # CLI giriş noktası
├── .env.example
├── requirements.txt
└── README.md
```

---

## State Yapısı

```python
class State(MessagesState):
    intent: Optional[str]        # router kararı
    user_info: Optional[dict]    # kullanıcı bağlamı
    proposal_draft: Optional[str] # freelance agent çıktısı
```

---

## Agent Ekleme

```python
# 1. agents/ altına yeni dosya
def seo_agent(state: State) -> dict:
    ...
    return {"messages": [...]}

# 2. graph.py içinde node ekle
builder.add_node("seo", seo_agent)

# 3. router.py içinde yeni route
routing_map["seo"] = "seo"
```

---

## Model Stratejisi

| Aşama       | Model                          | Açıklama                                      |
|-------------|--------------------------------|-----------------------------------------------|
| Geliştirme  | Mistral-7B-Instruct (Hub)      | HuggingFace Hub'dan direkt çekilir            |
| Fine-tune   | Mistral-7B + LoRA (PEFT)       | Proposal verisiyle fine-tune                  |
| Production  | Fine-tune edilmiş local model  | `model/` klasöründen yüklenir                 |

Fine-tune pipeline'ı ayrı bir repo olarak yönetilecek ve MLflow ile takip edilecektir.

---

## Güvenlik

- API key'ler `.env` dosyasında tutulur, koda yazılmaz.
- `.env` dosyası `.gitignore`'a eklidir.
- HuggingFace token gerekmiyorsa boş bırakılabilir.

---

## Yol Haritası

- [x] Mimari tasarım
- [x] LangGraph graph kurulumu
- [ ] HuggingFace model loader (`model/loader.py`)
- [ ] Router Agent (intent classification)
- [ ] Freelance Agent (ilk çalışan versiyon)
- [ ] `file_writer.py` tool entegrasyonu
- [ ] Fine-tune veri seti üretimi (sentetik)
- [ ] LoRA fine-tune pipeline
- [ ] MLflow experiment tracking
- [ ] LangGraph checkpointer (multi-turn memory)
- [ ] Support Agent *(sonraki milestone)*

---

## Lisans

MIT
</details>

<details>
<summary><b>🇬🇧 English Project Summary (Click to expand)</b></summary>

# Freelancer Proposal Agent

An agentic proposal writing system built with LangGraph, powered by a **local HuggingFace model**.  
Takes a job listing as input and generates a compelling freelance proposal using a fine-tuned local model.

> This project is under active development and is being built with Codex.

---

## How It Works

```
User (enters job listing)
        ↓
  Router Agent       ← detects intent
        ↓
Freelance Agent      ← generates proposal
        ↓
   [HuggingFace      ← local model inference
    local model]
        ↓
  Output / File
```

---

## Tech Stack

| Layer               | Tool                              |
|---------------------|-----------------------------------|
| Agent framework     | LangGraph                         |
| LLM (local)         | HuggingFace Transformers + PEFT   |
| Base model          | Mistral-7B (LoRA fine-tune)       |
| LangChain connector | `langchain-huggingface`           |
| Language            | Python 3.11+                      |
| Environment         | python-dotenv                     |
| Experiment tracking | MLflow *(next phase)*             |

---

## Setup

```bash
git clone https://github.com/yunusemreerken/Simple-Agent.git
cd Simple-Agent

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create your `.env` file:

```bash
cp .env.example .env
```

`.env` contents:

```
# HuggingFace model name (Hub) or local path
HF_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2

# HuggingFace Hub token (optional, not needed for public models)
HUGGINGFACE_TOKEN=hf_...

# LangSmith tracing (optional)
LANGCHAIN_API_KEY=...
LANGCHAIN_TRACING_V2=false
```

Run:

```bash
python main.py
```

---

## Project Structure

```
Simple-Agent/
├── agents/
│   ├── router.py            # detects intent → routes to freelance agent
│   └── freelance_agent.py   # proposal generation
├── tools/
│   └── file_writer.py       # saves the generated proposal to disk
├── model/
│   └── loader.py            # HuggingFace model loader (local / Hub)
├── state.py                 # shared State definition
├── graph.py                 # LangGraph graph setup
├── main.py                  # CLI entry point
├── .env.example
├── requirements.txt
└── README.md
```

---

## State Schema

```python
class State(MessagesState):
    intent: Optional[str]         # router decision
    user_info: Optional[dict]     # user context
    proposal_draft: Optional[str] # freelance agent output
```

---

## Adding a New Agent

```python
# 1. Create a new file under agents/
def seo_agent(state: State) -> dict:
    ...
    return {"messages": [...]}

# 2. Register the node in graph.py
builder.add_node("seo", seo_agent)

# 3. Add a new route in router.py
routing_map["seo"] = "seo"
```

---

## Model Strategy

| Phase       | Model                          | Description                                   |
|-------------|--------------------------------|-----------------------------------------------|
| Development | Mistral-7B-Instruct (Hub)      | Pulled directly from HuggingFace Hub          |
| Fine-tune   | Mistral-7B + LoRA (PEFT)       | Fine-tuned on proposal dataset                |
| Production  | Fine-tuned local model         | Loaded from the `model/` directory            |

The fine-tune pipeline will be managed as a separate repository and tracked with MLflow.

---

## Security

- API keys are stored in `.env` and never hardcoded.
- `.env` is listed in `.gitignore`.
- HuggingFace token can be left empty for public models.

---

## Roadmap

- [x] Architecture design
- [x] LangGraph graph setup
- [ ] HuggingFace model loader (`model/loader.py`)
- [ ] Router Agent (intent classification)
- [ ] Freelance Agent (first working version)
- [ ] `file_writer.py` tool integration
- [ ] Synthetic fine-tune dataset generation
- [ ] LoRA fine-tune pipeline
- [ ] MLflow experiment tracking
- [ ] LangGraph checkpointer (multi-turn memory)
- [ ] Support Agent *(next milestone)*

---

## License

MIT

</details>


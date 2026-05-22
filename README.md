# Agentic AI Projesi — Freelancer Bot & Müşteri Destek

Multi-agent mimari üzerine kurulu, LangGraph ile geliştirilmiş Python projesi.  
Freelance proposal yazımı ve müşteri destek süreçlerini otomatikleştirir.

---

## Mimari

```
Kullanıcı
    ↓
Router Agent          ← isteği analiz eder, yönlendirir
   /       \
Destek     Freelance
Agent      Agent
  |           |
[tools]    [tools]
```

Tüm agent'lar ortak bir `State` nesnesi üzerinden iletişim kurar.  
Yeni agent eklemek 3 adım: yaz → graph'a ekle → router'a route ekle.

---

## Teknoloji Yığını

| Katman | Araç |
|---|---|
| Agent framework | LangGraph |
| LLM | OpenAI / Anthropic Claude |
| Dil | Python 3.11+ |
| Ortam yönetimi | python-dotenv |
| İzleme (opsiyonel) | LangSmith |
| Vektör DB (opsiyonel) | Chroma / Pinecone |

---

## Kurulum

```bash
git clone https://github.com/kullanici/proje-adi.git
cd proje-adi

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

`.env` dosyası oluştur:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
LANGSMITH_API_KEY=...        # opsiyonel
```

---

## Proje Yapısı

```
proje/
├── agents/
│   ├── router.py          # isteği analiz eder, yönlendirir
│   ├── support_agent.py   # müşteri destek
│   └── freelance_agent.py # proposal yazımı
├── tools/
│   ├── web_search.py
│   ├── file_writer.py
│   └── ...
├── state.py               # paylaşılan State tanımı
├── graph.py               # LangGraph graph kurulumu
├── main.py                # giriş noktası
├── .env                   # API key'ler (git'e ekleme)
├── .env.example
├── requirements.txt
└── README.md
```

---

## State Yapısı

```python
from typing import TypedDict

class State(TypedDict):
    messages: list       # konuşma geçmişi
    intent: str          # router kararı
    user_info: dict      # tüm agent'lar okuyabilir
    proposal_draft: str  # freelance agent üretir
```

---

## Agent Ekleme

Yeni bir agent eklemek için:

```python
# 1. agents/ altına yeni dosya
def seo_agent(state: State) -> dict:
    ...
    return {"result": "..."}

# 2. graph.py içinde node ekle
graph.add_node("seo", seo_agent)

# 3. router.py içinde yeni koşul
if intent == "seo":
    return "seo"
```

Mevcut agent'lar etkilenmez.

---

## Güvenlik

- API key'ler `.env` dosyasında tutulur, koda yazılmaz.
- Her agent yalnızca kendi tool'larına erişebilir.
- `.env` dosyası `.gitignore`'a eklenmeli.

---

## Yol Haritası

- [x] Mimari tasarım
- [ ] Router Agent
- [ ] Freelance Agent (ilk çalışan versiyon)
- [ ] Destek Agent
- [ ] Tool entegrasyonları
- [ ] RAG sistemi
- [ ] LangSmith izleme
- [ ] Rate limiting & güvenlik katmanı

---

## Geliştirme Notları

Bu proje "çalışan en küçük parça" felsefesiyle geliştirilmektedir.  
Her agent bağımsız test edilebilir olmalıdır.

---

## Lisans

MIT

# Mimari Tartışma — Agentic AI Projesi

Tarih: Mayıs 2026  
Konu: Multi-agent mimari kararları, LangGraph, güvenlik, başlangıç stratejisi

---

## Proje Tanımı

**Uygulama türü:** Müşteri destek / chatbot + İş süreci otomasyonu + Freelancer bot (proposal yazımı)  
**Dil:** Python  
**Mimari karar:** Multi-agent (LangGraph)

---

## Tool Nedir?

Agent'ın LLM dışında çağırabileceği her fonksiyon bir "tool"dur.

Örnekler:
- `web_search()` → Google'da arama
- `write_docx()` → Word dosyası oluştur
- `send_email()` → mail gönder
- `query_db()` → veritabanı sorgula

Agent düşünür → hangi tool'u çağıracağına karar verir → tool çalışır → sonucu alır → devam eder.

---

## Neden Multi-Agent?

Tek bir "her şeyi yapan" agent yerine uzman agent'lar:

```
Kullanıcı mesajı
      ↓
Router Agent  ← "Bu ne tür istek?"
   /      \
Destek    Freelance
Agent     Agent
```

Her agent kendi tool'larıyla çalışır. Yeni agent veya tool eklemek → sadece yeni node.

---

## Neden LangGraph?

| Özellik | LangGraph |
|---|---|
| Tool ekleme | Çok kolay |
| Multi-agent | Native destek |
| State yönetimi | Güçlü |
| Hata yönetimi | Graph akışı ile |

---

## Agent Ekleme — Nasıl Çalışır?

LangGraph'ta yeni agent eklemek 3 adım:

```python
# 1. Yeni agent fonksiyonu
def seo_agent(state):
    return {"result": "..."}

# 2. Graph'a node ekle
graph.add_node("seo", seo_agent)

# 3. Router'a yeni route
if intent == "seo":
    return "seo"
```

Mevcut agent'lar bu değişiklikten etkilenmez.

---

## Agent'lar Arası İletişim

Tüm agent'lar ortak bir `State` nesnesi üzerinden konuşur:

```python
class State(TypedDict):
    messages: list        # konuşma geçmişi
    intent: str           # router kararı
    user_info: dict       # tüm agent'lar okuyabilir
    proposal_draft: str   # freelance agent yazar, başkası okur
```

Yeni agent → state'e yeni alan ekle → geriye dönük uyumluluk otomatik.

---

## Güvenlik — Öncelik Sırası

**Hemen (proje başında):**
- API key'leri `.env` dosyasına koy
- Her agent yalnızca kendi tool'larına erişsin

**İlk prototip çalışınca:**
- Rate limiting
- Input validation
- Prompt injection koruması

**Ürüne geçerken:**
- Tüm aksiyonları logla (LangSmith)
- Geri dönüşü zor işlemler için onay adımı
- LangSmith izleme entegrasyonu

---

## Başlangıç Stratejisi

Karar: Boş bir "hello world" agent yerine gerçek projeye başlamak.

**Gerekçe:** Gerçek bir problemi çözerken yapılan hatalar kalıcı öğretir.  
Soyut örnekler öğretmez.

**Sıralama:**
1. Router + Freelance Agent çalışsın (MVP)
2. Destek Agent ekle
3. Tool'ları genişlet
4. RAG sistemi
5. Güvenlik katmanı

---

## Öğrenme Yol Haritası

| Hafta | Konu |
|---|---|
| 1 | LLM API, Tool Calling, Agent döngüsü (ReAct) |
| 2 | LangGraph — Node, Edge, State, Conditional routing |
| 3 | Router + 2 Agent kurulumu (proje mimarisi) |
| 4 | RAG sistemi, Vektör DB, Agent memory |

---

## Sonraki Adım

İlk çalışan agent'ı kodlamak:  
Router Agent + Freelance Agent (minimal, çalışan versiyon).

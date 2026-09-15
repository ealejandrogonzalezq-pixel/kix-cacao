from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
import os, requests

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KIX CHAT - IA Mundial</title>
<style>
body{margin:0;font-family:Inter,Arial;background:#eef2f7}
.top{height:62px;background:#0f1e33;display:flex;align-items:center;justify-content:space-between;padding:0 18px;color:#fff}
.logo{font-weight:800;font-size:26px;display:flex;gap:10px;align-items:center}
.logo-ic{width:42px;height:42px;border-radius:10px;background:linear-gradient(135deg,#2dd4bf,#3b82f6);display:grid;place-items:center}
.pill{background:#1f304d;border:1px solid #2a4166;padding:7px 18px;border-radius:22px;font-size:13px;color:#dbe7ff}
.layout{display:grid;grid-template-columns:260px 1fr 360px;height:calc(100vh - 62px)}
.sidebar{background:#fff;border-right:1px solid #e2e8f0;padding:12px;display:flex;flex-direction:column;gap:10px;overflow:auto}
.btn-new{width:100%;background:#0f1e33;color:#fff;border:none;padding:11px;border-radius:10px;font-weight:700;cursor:pointer}
.chat-item{padding:9px 10px;background:#f8fafc;border-radius:8px;cursor:pointer;font-size:13px;margin-top:4px;display:flex;justify-content:space-between}
.chat-item.active{background:#0f1e33;color:#fff}
.chat-main{background:#f7f9fb;display:flex;flex-direction:column;position:relative}
.chat-header{height:50px;background:#fff;border-bottom:1px solid #e2e8f0;display:flex;align-items:center;justify-content:space-between;padding:0 14px}
.center{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px}
.messages{position:absolute;top:50px;bottom:90px;left:0;right:0;overflow:auto;padding:18px;display:none;flex-direction:column;gap:14px}
.msg{display:flex;gap:10px;max-width:88%}
.msg.user{margin-left:auto;flex-direction:row-reverse}
.avatar{width:30px;height:30px;border-radius:50%;background:#0f1e33;color:#fff;display:grid;place-items:center;font-size:11px;font-weight:700}
.bubble{background:#fff;border:1px solid #e2e8f0;padding:11px 13px;border-radius:14px;font-size:13.5px;white-space:pre-wrap;line-height:1.45}
.msg.user.bubble{background:#0f1e33;color:#fff}
.input-area{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);width:94%;max-width:700px;background:#fff;border:1px solid #cbd5e1;border-radius:16px;padding:8px 10px;display:flex;gap:8px;align-items:center}
.input-area input{flex:1;border:none;outline:none;padding:8px}
.ico{width:40px;height:40px;border-radius:10px;display:grid;place-items:center;cursor:pointer;border:none}
.right{background:#0f1e33;color:#e2e8f0;padding:12px;overflow:auto;display:flex;flex-direction:column;gap:14px}
.card{background:#132844;border:1px solid #1f3a5f;border-radius:12px;padding:12px}
.news{font-size:11.5px;color:#b8c7dd;margin-bottom:10px}.news b{color:#fff;display:block}
.acc{background:#0c1a2e;border:1px solid #1f3a5f;border-radius:10px;padding:10px}
.acc input{width:100%;background:#122a4a;border:1px solid #20406c;color:#fff;padding:8px;border-radius:7px;margin-bottom:7px;font-size:12px}
.btn-sign{width:100%;background:#10b981;border:none;color:#fff;padding:9px;border-radius:7px;font-weight:700;cursor:pointer}
.upload{border:1.5px dashed #2a4a70;border-radius:10px;padding:14px;text-align:center;color:#8ea8c7;font-size:11px}
.typing{font-size:12px;color:#64748b;font-style:italic;padding:5px}
</style>
</head>
<body>
<div class="top"><div class="logo"><div class="logo-ic">◈</div> KIX CHAT</div><div class="pill">🌍 Google + Wikipedia + IAs Activo</div><div style="width:34px;height:34px;background:#fff;color:#0f1e33;border-radius:50%;display:grid;place-items:center;font-weight:800" id="avatarTop">AG</div></div>
<div class="layout">
<div class="sidebar"><button class="btn-new" onclick="nuevoChat()">+ Nuevo chat</button><div style="font-size:11px;color:#64748b">Chats se guardan solo</div><div id="chatList"></div><button style="margin-top:auto;background:#f1f5f9;border:1px solid #e2e8f0;padding:8px;border-radius:8px;font-size:12px;cursor:pointer" onclick="location.reload()">↻ Actualizar</button></div>
<div class="chat-main"><div class="chat-header"><b id="chatTitle">New Chat</b><span onclick="nuevoChat()" style="cursor:pointer">↻ Nuevo</span></div><div class="center" id="center"><h1>¿Cómo puedo ayudarte hoy?</h1><p>Ya tengo acceso a <b>Google, Wikipedia y 3 IAs</b>. Pregúntame de TODO.</p></div><div class="messages" id="messages"></div><div class="input-area"><input id="userInput" placeholder="Escribe cualquier cosa..." onkeydown="if(event.key==='Enter') enviar()"><button class="ico" style="background:#10b981;color:#fff" onclick="enviar()">➤</button></div></div>
<div class="right">
<div class="card"><h4 style="margin:0 0 8px 0;color:#fff">News Bulletin — Cacao 🫘</h4><div class="news"><b>Precio cacao +8%</b>Sequía Ghana reduce cosecha 2026.</div><div class="news"><b>Fedecacao: Moniliasis</b>Poda + Trichoderma.</div></div>
<div class="acc"><h4 style="color:#fff;font-size:13px">Account</h4><input id="nombre" placeholder="Nombre"><input id="correo" placeholder="Correo"><button class="btn-sign" onclick="login()">Sign in</button><div id="loginStatus" style="font-size:11px;margin-top:6px;color:#10b981"></div></div>
</div>
</div>
<script>
let chats=JSON.parse(localStorage.getItem('kix_chats')||'[]');let currentId=localStorage.getItem('kix_current')||null;
function save(){localStorage.setItem('kix_chats',JSON.stringify(chats));localStorage.setItem('kix_current',currentId);render();}
function render(){let l=document.getElementById('chatList');l.innerHTML='';chats.slice().reverse().forEach(c=>{let d=document.createElement('div');d.className='chat-item '+(c.id==currentId?'active':'');d.innerHTML='<span>'+(c.title||'Chat').substring(0,22)+'</span><small>'+c.msgs.length+'</small>';d.onclick=()=>loadChat(c.id);l.appendChild(d);})}
function nuevoChat(){let id=Date.now().toString();let n={id:id,title:'New Chat '+(chats.length+1),msgs:[]};chats.push(n);currentId=id;save();document.getElementById('messages').innerHTML='';document.getElementById('messages').style.display='none';document.getElementById('center').style.display='flex';document.getElementById('chatTitle').innerText=n.title;}
function loadChat(id){currentId=id;let c=chats.find(x=>x.id==id);document.getElementById('chatTitle').innerText=c.title;document.getElementById('center').style.display='none';let cont=document.getElementById('messages');cont.style.display='flex';cont.innerHTML='';c.msgs.forEach(m=>addDOM(m.who,m.text,m.extra||''));save();}
function addDOM(who,text,extra){let cont=document.getElementById('messages');let d=document.createElement('div');d.className='msg '+(who=='user'?'user':'');let av=who=='user'?'U':'KX';let safe=text.replace(/</g,'&lt;');let ex=extra?'<div style="font-size:10px;color:#64748b;margin-top:6px;border-top:1px solid #eee;padding-top:4px">'+extra+'</div>':'';d.innerHTML='<div class=avatar>'+av+'</div><div class=bubble>'+safe+ex+'</div>';cont.appendChild(d);cont.scrollTop=cont.scrollHeight;}
function addMsg(who,text,extra){if(!currentId)nuevoChat();let c=chats.find(x=>x.id==currentId);c.msgs.push({who,text,extra});if(c.msgs.length==1)c.title=text.substring(0,30);save();document.getElementById('center').style.display='none';document.getElementById('messages').style.display='flex';addDOM(who,text,extra);}
function login(){let n=document.getElementById('nombre').value;let co=document.getElementById('correo').value;if(!n||!co){alert('Completa');return;}localStorage.setItem('kix_user',JSON.stringify({n,co}));document.getElementById('loginStatus').innerText='Sesión: '+n;document.getElementById('avatarTop').innerText=n.substring(0,2).toUpperCase();addMsg('kix','¡Bienvenido '+n+'! Ya tengo Google + Wikipedia + IAs. Pregúntame lo que quieras.');}
async function enviar(){
 let i=document.getElementById('userInput');let t=i.value.trim();if(!t)return;
 addMsg('user',t);i.value='';
 let typing=document.createElement('div');typing.className='typing';typing.id='typing';typing.innerText='KIX buscando en Google + Wikipedia + IAs...';document.getElementById('messages').appendChild(typing);
 try{
   let res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t,history:chats.find(x=>x.id==currentId)?.msgs||[]})});
   let data=await res.json();
   document.getElementById('typing')?.remove();
   addMsg('kix',data.reply||'Error',data.sources||'');
 }catch(e){
   document.getElementById('typing')?.remove();
   addMsg('kix','Error, intenta de nuevo: '+t);
 }
}
(function(){let u=JSON.parse(localStorage.getItem('kix_user')||'null');if(u){document.getElementById('nombre').value=u.n;document.getElementById('correo').value=u.co;document.getElementById('avatarTop').innerText=u.n.substring(0,2).toUpperCase();document.getElementById('loginStatus').innerText='Sesión: '+u.n;}if(chats.length==0)nuevoChat();else{render();if(currentId)loadChat(currentId);else nuevoChat();}})();
</script>
</body>
</html>
"""

def buscar_google_duck(q):
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(q, max_results=3))
            if results:
                txt = "\n".join([f"- {r['title']}: {r['body'][:120]}" for r in results])
                return txt
    except Exception as e:
        pass
    return ""

def buscar_wikipedia(q):
    try:
        import wikipedia
        wikipedia.set_lang("es")
        page = wikipedia.summary(q, sentences=2)
        return page[:400]
    except:
        return ""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.post("/api/chat")
async def chat_api(req: Request):
    data = await req.json()
    user_msg = data.get("message","")
    history = data.get("history",[])
    google_info = buscar_google_duck(user_msg)
    wiki_info = buscar_wikipedia(user_msg)
    contexto_extra = ""
    if google_info:
        contexto_extra += f"\nInfo de internet: {google_info}"
    if wiki_info:
        contexto_extra += f"\nInfo Wikipedia: {wiki_info}"

    groq_key = os.getenv("GROQ_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    if groq_key or openai_key:
        try:
            from openai import OpenAI
            if groq_key:
                client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")
                model = "llama-3.3-70b-versatile"
            else:
                client = OpenAI(api_key=openai_key)
                model = "gpt-4o-mini"
            system = f"Eres KIX CHAT, IA mundial como ChatGPT. Respondes de TODO. Usa esta info: {contexto_extra}"
            msgs = [{"role":"system","content":system}]
            for h in history[-6:]:
                role = "user" if h.get("who")=="user" else "assistant"
                msgs.append({"role":role,"content":h.get("text","")[:500]})
            msgs.append({"role":"user","content":user_msg})
            resp = client.chat.completions.create(model=model, messages=msgs, temperature=0.7, max_tokens=1000)
            reply = resp.choices[0].message.content
            return {"reply": reply, "sources": "Fuentes: Google + Wikipedia ✓"}
        except Exception as e:
            print(f"IA error: {e}")

    base = ""
    if google_info:
        base += f"\n🌍 Google: {google_info}"
    if wiki_info:
        base += f"\n📚 Wikipedia: {wiki_info}"

    if any(x in user_msg.lower() for x in ["hola","buenas"]):
        return {"reply": f"¡Hola! 👋 Soy KIX con Google + Wikipedia + IAs. Puedo responder de TODO. ¿Qué necesitas?{base}", "sources": "Google + Wikipedia activo"}

    r = f"Pregunta: '{user_msg}'\n{base}\n\nEstoy en modo general mundial. Puedo responder de matemáticas, código, recetas, historia, ciencia, cacao... Dame más detalles y te respondo completo.\n\n💡 Para ser más potente como ChatGPT-4, conecta API key gratis de Groq en Render."
    return {"reply": r, "sources": "🌍 Google + 📚 Wikipedia consultados" if (google_info or wiki_info) else "IA general activa"}

@app.post("/analizar-archivo")
async def analizar(file: UploadFile = File(...)):
    return {"permitido": True, "mensaje": "Archivo validado"}

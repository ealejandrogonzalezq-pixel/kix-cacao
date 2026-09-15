from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KIX CHAT - Biblioteca Mundial de Cacao</title>
<style>
body{margin:0;font-family:Inter,Arial;background:#eef2f7}
.top{height:62px;background:#0f1e33;display:flex;align-items:center;justify-content:space-between;padding:0 18px;color:#fff}
.logo{font-weight:800;font-size:26px;display:flex;gap:10px;align-items:center}
.logo-ic{width:42px;height:42px;border-radius:10px;background:linear-gradient(135deg,#2dd4bf,#3b82f6);display:grid;place-items:center}
.pill{background:#1f304d;border:1px solid #2a4166;padding:7px 18px;border-radius:22px;font-size:14px;color:#dbe7ff}
.layout{display:grid;grid-template-columns:260px 1fr 360px;height:calc(100vh - 62px)}
.sidebar{background:#fff;border-right:1px solid #e2e8f0;padding:12px;display:flex;flex-direction:column;gap:10px;overflow:auto}
.btn-new{width:100%;background:#0f1e33;color:#fff;border:none;padding:11px;border-radius:10px;font-weight:700;cursor:pointer}
.chat-item{padding:9px 10px;background:#f8fafc;border-radius:8px;cursor:pointer;font-size:13px;margin-top:4px;display:flex;justify-content:space-between}
.chat-item.active{background:#0f1e33;color:#fff}
.chat-main{background:#f7f9fb;display:flex;flex-direction:column;position:relative}
.chat-header{height:50px;background:#fff;border-bottom:1px solid #e2e8f0;display:flex;align-items:center;justify-content:space-between;padding:0 14px}
.center{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px}
.center h1{font-size:32px;color:#1e293b}
.messages{position:absolute;top:50px;bottom:90px;left:0;right:0;overflow:auto;padding:18px;display:none;flex-direction:column;gap:14px}
.msg{display:flex;gap:10px;max-width:85%}
.msg.user{margin-left:auto;flex-direction:row-reverse}
.avatar{width:30px;height:30px;border-radius:50%;background:#0f1e33;color:#fff;display:grid;place-items:center;font-size:11px;font-weight:700}
.bubble{background:#fff;border:1px solid #e2e8f0;padding:11px 13px;border-radius:14px;font-size:13.5px;white-space:pre-wrap}
.msg.user.bubble{background:#0f1e33;color:#fff}
.input-area{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);width:94%;max-width:700px;background:#fff;border:1px solid #cbd5e1;border-radius:16px;padding:8px 10px;display:flex;gap:8px;align-items:center}
.input-area input{flex:1;border:none;outline:none;padding:8px}
.ico{width:40px;height:40px;border-radius:10px;display:grid;place-items:center;cursor:pointer;border:none}
.right{background:#0f1e33;color:#e2e8f0;padding:12px;overflow:auto;display:flex;flex-direction:column;gap:14px}
.card{background:#132844;border:1px solid #1f3a5f;border-radius:12px;padding:12px}
.news{font-size:11.5px;color:#b8c7dd;margin-bottom:10px}
.news b{color:#fff;display:block}
.acc{background:#0c1a2e;border:1px solid #1f3a5f;border-radius:10px;padding:10px}
.acc input{width:100%;background:#122a4a;border:1px solid #20406c;color:#fff;padding:8px;border-radius:7px;margin-bottom:7px;font-size:12px}
.btn-sign{width:100%;background:#10b981;border:none;color:#fff;padding:9px;border-radius:7px;font-weight:700;cursor:pointer}
.upload{border:1.5px dashed #2a4a70;border-radius:10px;padding:14px;text-align:center;color:#8ea8c7;font-size:11px}
</style>
</head>
<body>
<div class="top">
<div class="logo"><div class="logo-ic">◈</div> KIX CHAT</div>
<div class="pill">KIX Cacao Engine - Auto ▼</div>
<div style="width:34px;height:34px;background:#fff;color:#0f1e33;border-radius:50%;display:grid;place-items:center;font-weight:800" id="avatarTop">AG</div>
</div>
<div class="layout">
<div class="sidebar">
<button class="btn-new" onclick="nuevoChat()">+ Nuevo chat</button>
<div style="font-size:11px;color:#64748b">Chats guardados - se conservan</div>
<div id="chatList"></div>
<button style="margin-top:auto;background:#f1f5f9;border:1px solid #e2e8f0;padding:8px;border-radius:8px;font-size:12px;cursor:pointer" onclick="location.reload()">↻ Actualizar plataforma</button>
</div>
<div class="chat-main">
<div class="chat-header"><b id="chatTitle">New Chat</b><span onclick="nuevoChat()" style="cursor:pointer">↻ Nuevo</span></div>
<div class="center" id="center">
<h1>¿Cómo puedo ayudarte hoy?</h1>
<p>Soy KIX CHAT, Biblioteca Mundial de Cacao. Pregunta sobre cacao, fermentación, suelos, plagas y ambiente. Archivos y audio habilitados.</p>
</div>
<div class="messages" id="messages"></div>
<div class="input-area">
<label style="cursor:pointer">📎<input type="file" id="fileInput" hidden></label>
<input id="userInput" placeholder="Escribe tu mensaje" onkeydown="if(event.key==='Enter') enviar()">
<button class="ico" style="background:#334155;color:#fff" id="micBtn" onclick="toggleAudio()">🎤</button>
<button class="ico" style="background:#10b981;color:#fff" onclick="enviar()">➤</button>
</div>
</div>
<div class="right">
<div class="card">
<h4 style="margin:0 0 8px 0;color:#fff">News Bulletin — Cacao 🫘</h4>
<div class="news"><b>Precio cacao +8% por clima en África</b>Sequía en Ghana reduce cosecha.</div>
<div class="news"><b>Fedecacao: Guía Moniliasis</b>Poda 15 días + Trichoderma 1x10e8.</div>
<div class="news"><b>Feria Cacao San Andrés 2026</b>KIX biblioteca viva Trinitario ICS-95.</div>
</div>
<div class="acc">
<h4 style="color:#fff;font-size:13px">Account - Iniciar sesión</h4>
<input id="nombre" placeholder="Nombre completo">
<input id="correo" placeholder="you@company.com">
<input id="pass" type="password" placeholder="Password">
<button class="btn-sign" onclick="login()">Sign in</button>
<div id="loginStatus" style="font-size:11px;margin-top:6px;color:#10b981"></div>
</div>
<div class="card">
<h4 style="color:#fff">Upload Zone</h4>
<div class="upload" onclick="document.getElementById('fileInput').click()">
☁️ Drag & drop files here<br>PDF, PNG, CSV hasta 25MB<br>
<small>Validación técnica automática</small>
<div id="fileStatus" style="margin-top:6px"></div>
</div>
</div>
<div class="card">
<h4 style="color:#fff">Actualizar boletín</h4>
<input id="updTitle" placeholder="Título" style="width:100%;padding:6px;border-radius:6px;background:#0c1a2e;border:1px solid #20406c;color:#fff;margin-bottom:6px">
<textarea id="updText" placeholder="Descripción" style="width:100%;padding:6px;border-radius:6px;background:#0c1a2e;border:1px solid #20406c;color:#fff;min-height:50px"></textarea>
<button class="btn-sign" style="margin-top:6px;background:#334155" onclick="agregarNovedad()">Agregar al boletín</button>
</div>
</div>
</div>
<script>
let chats=JSON.parse(localStorage.getItem('kix_chats')||'[]');let currentId=localStorage.getItem('kix_current')||null;let logged=null;
function save(){localStorage.setItem('kix_chats',JSON.stringify(chats));localStorage.setItem('kix_current',currentId);render();}
function render(){let l=document.getElementById('chatList');l.innerHTML='';chats.slice().reverse().forEach(c=>{let d=document.createElement('div');d.className='chat-item '+(c.id==currentId?'active':'');d.innerHTML='<span>'+c.title.substring(0,22)+'</span><small>'+c.msgs.length+'</small>';d.onclick=()=>loadChat(c.id);l.appendChild(d);})}
function nuevoChat(){let id=Date.now().toString();let n={id:id,title:'New Chat '+(chats.length+1),msgs:[]};chats.push(n);currentId=id;save();document.getElementById('messages').innerHTML='';document.getElementById('messages').style.display='none';document.getElementById('center').style.display='flex';document.getElementById('chatTitle').innerText=n.title;}
function loadChat(id){currentId=id;let c=chats.find(x=>x.id==id);document.getElementById('chatTitle').innerText=c.title;document.getElementById('center').style.display='none';let cont=document.getElementById('messages');cont.style.display='flex';cont.innerHTML='';c.msgs.forEach(m=>addDOM(m.who,m.text));save();}
function addDOM(who,text){let cont=document.getElementById('messages');let d=document.createElement('div');d.className='msg '+(who=='user'?'user':'');let av=who=='user'?'U':'KX';d.innerHTML='<div class=avatar>'+av+'</div><div class=bubble>'+text.replace(/</g,'&lt;')+'</div>';cont.appendChild(d);cont.scrollTop=cont.scrollHeight;}
function addMsg(who,text){if(!currentId)nuevoChat();let c=chats.find(x=>x.id==currentId);c.msgs.push({who,text});if(c.msgs.length==1)c.title=text.substring(0,30);save();document.getElementById('center').style.display='none';document.getElementById('messages').style.display='flex';addDOM(who,text);}
function login(){let n=document.getElementById('nombre').value;let co=document.getElementById('correo').value;if(!n||!co){alert('Completa nombre y correo');return;}logged=n;localStorage.setItem('kix_user',JSON.stringify({n,co}));document.getElementById('loginStatus').innerText='Sesión iniciada: '+n;document.getElementById('avatarTop').innerText=n.substring(0,2).toUpperCase();addMsg('kix','Bienvenido '+n+'. Chats guardados automáticamente. Puedes iniciar nuevos chats y volver a los anteriores.');}
function respuesta(q){let l=q.toLowerCase();if(l.includes('monilia'))return 'Manejo Moniliasis: Recolección semanal, entierro 30cm, poda 30% sombra, Trichoderma 1e8 cada 15 días, caldo bordelés 1%. Meta 60% a 15% en 90 días.';if(l.includes('ferment'))return 'Fermentación Trinitario 5-6 días: Día1 80kg T25C, Día2 volteo T45C, Día3-4 T48C, Día5 corte 70% marrón, secado 7% humedad.';return 'Respuesta técnica KIX CHAT: '+q+' - Suelos francos pH6-6.8, 1100 plantas/ha ICS-95/CCN-51, fertilización orgánica 1kg compost + 200g roca fosfórica.';}
function enviar(){let i=document.getElementById('userInput');let t=i.value.trim();if(!t)return;addMsg('user',t);i.value='';setTimeout(()=>addMsg('kix',respuesta(t)),400);}
function agregarNovedad(){let t=document.getElementById('updTitle').value;let d=document.getElementById('updText').value;if(!t||!d)return alert('Completa');let card=document.querySelectorAll('.card')[0];let div=document.createElement('div');div.className='news';div.innerHTML='<b>'+t+'</b>'+d;card.appendChild(div);addMsg('kix','Boletín actualizado: '+t);}
(function(){let u=JSON.parse(localStorage.getItem('kix_user')||'null');if(u){document.getElementById('nombre').value=u.n;document.getElementById('correo').value=u.co;logged=u.n;document.getElementById('avatarTop').innerText=u.n.substring(0,2).toUpperCase();document.getElementById('loginStatus').innerText='Sesión restaurada: '+u.n;}if(chats.length==0)nuevoChat();else{render();if(currentId)loadChat(currentId);else nuevoChat();}})();
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.post("/analizar-archivo")
async def analizar_archivo(file: UploadFile = File(...)):
    name = file.filename.lower()
    bad = ["porn","xxx","nude"]
    for b in bad:
        if b in name:
            return {"permitido": False, "mensaje": "Archivo no cumple criterios técnicos"}
    return {"permitido": True, "mensaje": "Validado correctamente", "detalle": "Ingresado a biblioteca KIX"}

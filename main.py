from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KIX - Biblioteca Mundial de Cacao</title>
<style>
body{font-family:'Segoe UI',sans-serif;background:#fdf6ec;margin:0;color:#3e2723}
.header{background:#3e2723;color:#fff;padding:30px 20px;text-align:center}
.container{max-width:900px;margin:0 auto;padding:20px}
.card{background:#fff;border-radius:16px;padding:20px;margin-bottom:20px;box-shadow:0 4px 12px rgba(0,0,0,0.08)}
.search{width:100%;padding:14px 18px;border-radius:12px;border:2px solid #d7ccc8;font-size:16px;box-sizing:border-box;margin-bottom:20px}
.tag{background:#8d6e63;color:white;padding:3px 10px;border-radius:20px;font-size:12px;margin-left:6px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px}
.variedad{border:1px solid #efebe9;border-radius:12px;padding:12px}
.variedad img{width:100%;height:130px;object-fit:cover;border-radius:8px}
.btn-wa{position:fixed;bottom:20px;right:20px;background:#25D366;color:white;padding:16px 22px;border-radius:50px;text-decoration:none;font-weight:bold;box-shadow:0 4px 15px rgba(0,0,0,0.3)}
h2{color:#5d4037}
.sol{padding:12px 0;border-bottom:1px solid #f5f5f5}
</style>
</head>
<body>
<div class="header">
<h1>KIX - Biblioteca Mundial de Cacao</h1>
<p>De San Andres, Cordoba para el mundo</p>
</div>
<div class="container">
<input id="buscador" class="search" type="text" placeholder="Buscar... ej: Criollo, Moniliasis" onkeyup="filtrar()">

<div class="card">
<h2>Variedades de Cacao</h2>
<div class="grid">
<div class="variedad" data-text="criollo centroamerica fino frutal"><img src="https://images.unsplash.com/photo-1511381939415-e44015466834?w=400"><b>Criollo</b><span class="tag">Centroamerica</span><br><small>Fino, frutal | Baja resistencia</small></div>
<div class="variedad" data-text="forastero amazonas fuerte amargo alta"><img src="https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=400"><b>Forastero</b><span class="tag">Amazonas</span><br><small>Fuerte, amargo | Alta resistencia</small></div>
<div class="variedad" data-text="trinitario trinidad equilibrado"><img src="https://images.unsplash.com/photo-1606312619070-d48b4fa37390?w=400"><b>Trinitario</b><span class="tag">Trinidad</span><br><small>Equilibrado | Media</small></div>
<div class="variedad" data-text="nacional ecuador floral"><img src="https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400"><b>Nacional</b><span class="tag">Ecuador</span><br><small>Floral | Aroma Arriba</small></div>
</div>
</div>

<div class="card">
<h2>Enfermedades y Soluciones</h2>
<div class="sol" data-text="moniliasis cafe polvoso"><b>Moniliasis:</b> Fruto cafe polvoso<br>Solucion: Poda sanitaria + caldo bordeles</div>
<div class="sol" data-text="escoba bruja hinchadas"><b>Escoba de bruja:</b> Ramas hinchadas<br>Solucion: Poda 30cm abajo + quemar</div>
<div class="sol" data-text="mazorca negra mancha"><b>Mazorca negra:</b> Mancha negra<br>Solucion: Drenaje + Trichoderma</div>
</div>
</div>

<a class="btn-wa" href="https://wa.me/573000000000?text=Hola%20KIX%20quiero%20info%20de%20cacao" target="_blank">WhatsApp</a>

<script>
function filtrar(){
 let t=document.getElementById('buscador').value.toLowerCase();
 document.querySelectorAll('.variedad, .sol').forEach(e=>{
   e.style.display=e.getAttribute('data-text').includes(t)?'':'none';
 });
}
</script>
</body>
</html>
    """

#!/usr/bin/env python3
"""
Fase 0 · Prueba 2: ¿cuánta de tu biblioteca de Spotify tiene BPM en ReccoBeats,
y alcanza para cubrir las recetas de 60′?

Solo usa la librería estándar de Python (3.9+).

Uso:
    export SPOTIFY_CLIENT_ID=<client id de tu app en developer.spotify.com>
    export GETSONGBPM_API_KEY=<opcional: clave de getsongbpm.com, 2.ª fuente para lo que no tenga ReccoBeats>
    python3 tools/bpm_coverage.py

Requisito en el dashboard de Spotify: añade la Redirect URI
    http://127.0.0.1:8888/callback
(Spotify ya no acepta "localhost"; hay que usar la IP de loopback.)

Salida:
    - Resumen por pantalla: temas importados, % con BPM, cobertura por bloque y por tipo.
    - tools/out/temas.csv con cada tema y su BPM.
    - tools/out/reccobeats_muestra.json con una respuesta cruda, para depurar.
"""
import base64
import csv
import hashlib
import http.server
import json
import os
import secrets
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "out"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPES = "user-library-read playlist-read-private playlist-read-collaborative"
RECCO = "https://api.reccobeats.com/v1"
RECCO_BATCH = 40  # Supuesto a validar: nº máximo de IDs por petición
TOLERANCIA = 0.03
MARGEN_COBERTURA = 1.5


# ---------------------------------------------------------------- HTTP helpers
USER_AGENT = "SpinCoach/0.1 (uso personal)"  # ReccoBeats (Cloudflare) bloquea el de Python-urllib


def http_json(url, headers=None, data=None, method=None):
    headers = {"User-Agent": USER_AGENT, **(headers or {})}
    for intento in range(6):
        req = urllib.request.Request(url, headers=headers, data=data, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode() or "null")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                espera = int(e.headers.get("Retry-After", "2")) + 1
                print(f"  429, espero {espera}s…")
                time.sleep(espera)
                continue
            cuerpo = e.read().decode(errors="replace")[:300]
            raise RuntimeError(f"HTTP {e.code} en {url}: {cuerpo}") from None
    raise RuntimeError(f"Demasiados 429 en {url}")


# ---------------------------------------------------------------- Spotify OAuth (PKCE)
def spotify_token(client_id):
    verifier = secrets.token_urlsafe(64)[:96]
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(16)
    params = {
        "client_id": client_id, "response_type": "code", "redirect_uri": REDIRECT_URI,
        "code_challenge_method": "S256", "code_challenge": challenge, "scope": SCOPES, "state": state,
    }
    recibido = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            recibido.update({k: v[0] for k, v in q.items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("Listo, puedes volver a la terminal.".encode())

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 8888), Handler)
    threading.Thread(target=srv.handle_request, daemon=True).start()
    url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
    print("Abriendo el navegador para autorizar en Spotify…\n" + url)
    webbrowser.open(url)
    for _ in range(300):
        if recibido:
            break
        time.sleep(1)
    srv.server_close()
    if recibido.get("state") != state or "code" not in recibido:
        sys.exit(f"Autorización fallida: {recibido}")
    body = urllib.parse.urlencode({
        "grant_type": "authorization_code", "code": recibido["code"], "redirect_uri": REDIRECT_URI,
        "client_id": client_id, "code_verifier": verifier,
    }).encode()
    tok = http_json("https://accounts.spotify.com/api/token", data=body,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
    return tok["access_token"]


def spotify_paginas(url, token):
    h = {"Authorization": f"Bearer {token}"}
    while url:
        pagina = http_json(url, headers=h)
        yield pagina
        url = pagina.get("next")


def pista_de(elemento):
    # Desde feb. 2026 el elemento de playlist puede venir como "item" en vez de "track".
    t = elemento.get("item") or elemento.get("track")
    if not t or t.get("type", "track") != "track" or not t.get("id"):
        return None
    return {
        "id": t["id"], "titulo": t.get("name", ""),
        "artistas": ", ".join(a.get("name", "") for a in t.get("artists", [])),
        "duracion_s": round(t.get("duration_ms", 0) / 1000),
    }


def importar_biblioteca(token):
    temas = {}
    me = http_json("https://api.spotify.com/v1/me", headers={"Authorization": f"Bearer {token}"})
    print("Leyendo canciones guardadas…")
    for p in spotify_paginas("https://api.spotify.com/v1/me/tracks?limit=50", token):
        for el in p.get("items", []):
            t = pista_de(el)
            if t:
                temas[t["id"]] = t
    print(f"  {len(temas)} temas")
    print("Leyendo tus playlists…")
    for p in spotify_paginas("https://api.spotify.com/v1/me/playlists?limit=50", token):
        for pl in p.get("items", []):
            propia = pl.get("owner", {}).get("id") == me.get("id") or pl.get("collaborative")
            if not propia:
                continue
            antes = len(temas)
            url = f"https://api.spotify.com/v1/playlists/{pl['id']}/items?limit=50"
            try:
                for pi in spotify_paginas(url, token):
                    for el in pi.get("items", []):
                        t = pista_de(el)
                        if t:
                            temas[t["id"]] = t
            except RuntimeError as e:
                print(f"  (omito «{pl.get('name')}»: {e})")
                continue
            print(f"  «{pl.get('name')}»: +{len(temas) - antes}")
    return list(temas.values())


# ---------------------------------------------------------------- ReccoBeats
def spotify_id_de(item):
    for campo in ("href", "uri", "spotifyId", "spotify_id"):
        v = item.get(campo)
        if isinstance(v, str) and v:
            return v.rstrip("/").split("/")[-1].split(":")[-1].split("?")[0]
    return None


def bpms_reccobeats(ids):
    """Supuesto a validar: GET /v1/audio-features?ids=<spotify ids> devuelve
    {"content": [{..., "href": "https://open.spotify.com/track/<id>", "tempo": 123.4}]}.
    Si la respuesta tiene otra forma, se guarda una muestra cruda para ajustarlo."""
    OUT.mkdir(parents=True, exist_ok=True)
    resultado, muestra_guardada = {}, False
    for i in range(0, len(ids), RECCO_BATCH):
        lote = ids[i:i + RECCO_BATCH]
        url = f"{RECCO}/audio-features?ids=" + ",".join(lote)
        try:
            data = http_json(url, headers={"Accept": "application/json"})
        except RuntimeError as e:
            print(f"  lote {i // RECCO_BATCH + 1}: {e}")
            continue
        if not muestra_guardada:
            (OUT / "reccobeats_muestra.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
            muestra_guardada = True
        items = data.get("content", []) if isinstance(data, dict) else (data or [])
        for it in items:
            sid = spotify_id_de(it)
            if sid and it.get("tempo"):
                resultado[sid] = float(it["tempo"])
        print(f"  {min(i + RECCO_BATCH, len(ids))}/{len(ids)} consultados, {len(resultado)} con BPM")
        time.sleep(0.3)
    return resultado


# ---------------------------------------------------------------- GetSongBPM (2.ª fuente)
import re
import unicodedata


def _norm(txt):
    txt = unicodedata.normalize("NFKD", txt or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]+", " ", txt).strip()


def _titulo_limpio(titulo):
    # Quita "- Remastered…", "(feat. …)", "- Canción original de…" que empeoran la búsqueda.
    titulo = re.split(r"\s+-\s+", titulo)[0]
    return re.sub(r"\s*[\(\[].*?[\)\]]", "", titulo).strip()


def bpms_getsongbpm(temas, api_key):
    """Busca por título + artista principal. Se acepta el resultado solo si el artista coincide."""
    resultado = {}
    for n, t in enumerate(temas, 1):
        titulo = _titulo_limpio(t["titulo"])
        artista = t["artistas"].split(",")[0].strip()
        lookup = f"song:{titulo} artist:{artista}"
        url = "https://api.getsongbpm.com/search/?" + urllib.parse.urlencode(
            {"api_key": api_key, "type": "both", "lookup": lookup})
        try:
            data = http_json(url)
        except RuntimeError as e:
            print(f"  {t['titulo']}: {e}")
            continue
        candidatos = data.get("search") if isinstance(data, dict) else None
        if isinstance(candidatos, list):
            for c in candidatos:
                nombre = (c.get("artist") or {}).get("name", "")
                if _norm(artista) and _norm(artista) in _norm(nombre) and c.get("tempo"):
                    try:
                        resultado[t["id"]] = float(c["tempo"])
                    except (TypeError, ValueError):
                        pass
                    break
        if n % 20 == 0:
            print(f"  {n}/{len(temas)} buscados, {len(resultado)} encontrados")
        time.sleep(0.4)
    return resultado


# ---------------------------------------------------------------- Cobertura
def encaja(bpm, bloque):
    lo, hi = bloque["bpm_min"] * (1 - TOLERANCIA), bloque["bpm_max"] * (1 + TOLERANCIA)
    return any(lo <= t <= hi for t in (bpm, bpm * 2, bpm / 2))


def informe(temas, bpm, fuente):
    bloques = {b["id"]: b for b in json.loads((ROOT / "data" / "bloques.json").read_text())["bloques"]}
    recetas = json.loads((ROOT / "data" / "recetas.json").read_text())["recetas"]
    con_bpm = [t for t in temas if t["id"] in bpm]
    print("\n================ RESULTADO ================")
    pct = 100 * len(con_bpm) / max(1, len(temas))
    print(f"Temas importados: {len(temas)} · con BPM: {len(con_bpm)} ({pct:.0f} %)"
          f" · objetivo fase 0: ≥ 80 %")
    por_fuente = {}
    for t in con_bpm:
        por_fuente[fuente[t["id"]]] = por_fuente.get(fuente[t["id"]], 0) + 1
    print("  por fuente: " + ", ".join(f"{k} {v}" for k, v in por_fuente.items()))

    minutos_bloque = {}
    print("\nMinutos de música que encajan por bloque:")
    for bid, b in bloques.items():
        m = sum(t["duracion_s"] for t in con_bpm if encaja(bpm[t["id"]], b)) / 60
        minutos_bloque[bid] = m
        print(f"  {bid:4} {b['nombre']:28} {b['bpm_min']:>3}–{b['bpm_max']:<3} BPM  {m:7.0f} min")

    print(f"\nCobertura de las recetas de 60′ con TODA tu biblioteca (necesario ≥ {MARGEN_COBERTURA}× por bloque):")
    for r in (r for r in recetas if r["duracion_min"] == 60):
        necesita = {}
        for f in r["fases"]:
            necesita[f["bloque"]] = necesita.get(f["bloque"], 0) + f["minutos"]
        faltan = [f"{bid} ({minutos_bloque[bid]:.0f}/{n * MARGEN_COBERTURA:.0f} min)"
                  for bid, n in necesita.items() if minutos_bloque[bid] < n * MARGEN_COBERTURA]
        print(f"  {r['tipo']:11} {'OK' if not faltan else 'FALTA: ' + ', '.join(faltan)}")
    print("\nOjo: esto es con toda la biblioteca junta; cada mezcla tendrá menos temas.")

    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "temas.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "titulo", "artistas", "duracion_s", "bpm", "fuente"])
        w.writeheader()
        for t in temas:
            w.writerow({**t, "bpm": bpm.get(t["id"], ""), "fuente": fuente.get(t["id"], "")})
    print(f"\nDetalle por tema en {OUT / 'temas.csv'}")


def main():
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    if not client_id:
        sys.exit("Falta SPOTIFY_CLIENT_ID (ver la cabecera de este script).")
    token = spotify_token(client_id)
    temas = importar_biblioteca(token)
    print(f"\nConsultando BPM en ReccoBeats para {len(temas)} temas…")
    bpm = bpms_reccobeats([t["id"] for t in temas])
    if not bpm:
        print(f"\nReccoBeats no devolvió ningún BPM reconocible. Revisa {OUT / 'reccobeats_muestra.json'}"
              " para ver la forma real de la respuesta y ajusta bpms_reccobeats().")
    fuente = {sid: "reccobeats" for sid in bpm}
    gs_key = os.environ.get("GETSONGBPM_API_KEY")
    faltan = [t for t in temas if t["id"] not in bpm]
    if gs_key and faltan:
        print(f"\nBuscando en GetSongBPM los {len(faltan)} temas sin BPM…")
        extra = bpms_getsongbpm(faltan, gs_key)
        bpm.update(extra)
        fuente.update({sid: "getsongbpm" for sid in extra})
    elif faltan:
        print(f"\n{len(faltan)} temas sin BPM. Define GETSONGBPM_API_KEY para probar una 2.ª fuente.")
    informe(temas, bpm, fuente)


if __name__ == "__main__":
    main()

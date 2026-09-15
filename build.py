#!/usr/bin/env python3
"""Gera o pacote de conhecimento da API flw.chat a partir da documentacao publica.

Fonte: https://flwchat.readme.io/llms.txt (indice oficial de todas as paginas).
Cada pagina de endpoint aceita o sufixo .md e embute um OpenAPI 3.0.1 auto-contido,
entao o build apenas baixa, separa guias de endpoints e mescla os fragmentos por servico.

Uso: python3 build.py [--no-cache]
"""
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://flwchat.readme.io"
ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ROOT, ".cache")
UA = "flwchat-api-kb-build/1.0"

# ponytail: paginas sem bloco OpenAPI sao guias; nao ha lista fixa, o conteudo decide.
OAS_RE = re.compile(r"#\s*OpenAPI definition\s*\n+```json\n(.*?)\n```", re.S)
BOILERPLATE = "Fetch the complete documentation index at:"


def fetch(url, use_cache=True):
    key = hashlib.sha1(url.encode()).hexdigest() + ".md"
    path = os.path.join(CACHE, key)
    if use_cache and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    parts = urllib.parse.urlsplit(url)  # paths tem acento (autenticacao.md)
    safe = urllib.parse.urlunsplit(parts._replace(path=urllib.parse.quote(parts.path)))
    req = urllib.request.Request(safe, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read().decode("utf-8")
    os.makedirs(CACHE, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    return body


def parse_index(txt):
    """- [Titulo](url.md): descricao  ->  [{title, url, desc}]"""
    out = []
    for line in txt.splitlines():
        m = re.match(r"-\s*\[(.+?)\]\((\S+?)\)(?::\s*(.*))?$", line.strip())
        if m:
            out.append({"title": m.group(1), "url": m.group(2), "desc": (m.group(3) or "").strip()})
    return out


def slug(url):
    return url.rsplit("/", 1)[-1][:-3] if url.endswith(".md") else url.rsplit("/", 1)[-1]


def strip_boilerplate(md):
    lines = md.splitlines()
    while lines and (not lines[0].strip() or lines[0].startswith(BOILERPLATE)):
        lines.pop(0)
    return "\n".join(lines).strip() + "\n"


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def apply_renames(obj, ren):
    if not ren:
        return obj
    s = json.dumps(obj, ensure_ascii=False)
    for old, new in ren.items():
        s = s.replace('"#/components/schemas/%s"' % old, '"#/components/schemas/%s"' % new)
    return json.loads(s)


def resolve_renames(frag_schemas, merged_schemas, conflicts, source):
    """Nomes iguais com conteudo diferente ganham sufixo por hash, em ponto fixo.

    O hash e deterministico, entao fragmentos com o mesmo conteudo convergem para o
    mesmo nome (dedupe) em vez de virar __2, __3, __4.
    """
    ren = {}
    for _ in range(len(frag_schemas) + 2):
        nxt = dict(ren)
        for name in sorted(frag_schemas):
            if name not in merged_schemas:
                continue
            # o proprio rename nao entra no corpo, para nao oscilar em schema recursivo
            local = {k: v for k, v in nxt.items() if k != name}
            body = apply_renames(frag_schemas[name], local)
            if canon(merged_schemas[name]) == canon(body):
                nxt.pop(name, None)
                continue
            h = hashlib.sha1(canon(body).encode()).hexdigest()[:8]
            nxt[name] = "%s__%s" % (name, h)
        if nxt == ren:
            for name in sorted(ren):
                conflicts.append("%s: %s -> %s" % (source, name, ren[name]))
            return ren
        ren = nxt
    sys.exit("ERRO: renomeacao de schemas nao convergiu em %s" % source)


def merge(fragments):
    """fragments: [(source, spec)] -> {service: spec}, conflitos, operacoes"""
    specs, conflicts, ops = {}, [], []
    for source, frag in fragments:
        svc = frag["info"]["title"].strip().lower()
        spec = specs.setdefault(svc, {
            "openapi": frag.get("openapi", "3.0.1"),
            "info": dict(frag["info"]),
            "servers": frag.get("servers", []),
            "paths": {},
            "components": {"schemas": {}, "securitySchemes": {}},
        })
        fs = frag.get("components", {}).get("schemas", {})
        ren = resolve_renames(fs, spec["components"]["schemas"], conflicts, source)
        for name, body in fs.items():
            final = ren.get(name, name)
            body = apply_renames(body, {k: v for k, v in ren.items() if k != name})
            if final in spec["components"]["schemas"]:
                if canon(spec["components"]["schemas"][final]) != canon(body):
                    sys.exit("ERRO: colisao nao resolvida no schema %s (%s)" % (final, source))
            else:
                spec["components"]["schemas"][final] = body
        spec["components"]["securitySchemes"].update(
            frag.get("components", {}).get("securitySchemes", {}))
        for path, item in apply_renames(frag["paths"], ren).items():
            dest = spec["paths"].setdefault(path, {})
            for method, op in item.items():
                if method in dest:
                    sys.exit("ERRO: %s %s duplicado (%s)" % (method.upper(), path, source))
                dest[method] = op
                ops.append({
                    "service": svc,
                    "method": method.upper(),
                    "path": path,
                    "full_path": "/%s%s" % (svc, path),
                    "summary": op.get("summary", ""),
                    "tags": op.get("tags", []),
                    "page": source,
                })
    return specs, conflicts, ops


# ---------------------------------------------------------------- referencia

def deaccent(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def tag_slug(tag):
    s = deaccent(tag).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "outros"


def ref_name(node):
    r = node.get("$ref") if isinstance(node, dict) else None
    return r.rsplit("/", 1)[-1] if r else None


def type_of(node):
    """Descricao curta do tipo de um schema node, incluindo $ref e enum."""
    if not isinstance(node, dict):
        return "?"
    n = ref_name(node)
    if n:
        return "[`%s`](#%s)" % (n, n.lower())
    if "enum" in node:
        vals = node["enum"]
        shown = ", ".join("`%s`" % v for v in vals[:12])
        return "enum: " + shown + (" … (+%d)" % (len(vals) - 12) if len(vals) > 12 else "")
    t = node.get("type", "object")
    if t == "array":
        return type_of(node.get("items", {})) + "[]"
    fmt = node.get("format")
    return "%s(%s)" % (t, fmt) if fmt else t


def collect_refs(node, out):
    if isinstance(node, dict):
        n = ref_name(node)
        if n:
            out.add(n)
        for v in node.values():
            collect_refs(v, out)
    elif isinstance(node, list):
        for v in node:
            collect_refs(v, out)


def clean(txt):
    return re.sub(r"\s+", " ", (txt or "").replace("<br />", " ")).strip()


def props_table(schema, schemas, lines):
    """Tabela de campos de um schema (resolve um $ref de topo)."""
    n = ref_name(schema)
    if n:
        schema = schemas.get(n, {})
    if not isinstance(schema, dict):
        return
    if schema.get("type") == "array":
        it = ref_name(schema.get("items", {}))
        lines.append("Array de %s." % (type_of(schema.get("items", {}))))
        if it:
            schema = schemas.get(it, {})
        else:
            lines.append("")
            return
    props = schema.get("properties")
    if not props:
        if schema.get("enum"):
            lines.append(type_of(schema))
        return
    req = set(schema.get("required", []))
    lines.append("| Campo | Tipo | Obrig. | Descrição |")
    lines.append("|---|---|---|---|")
    for k, v in props.items():
        lines.append("| `%s` | %s | %s | %s |" % (
            k, type_of(v), "sim" if k in req else "-", clean(v.get("description"))))
    lines.append("")


def render_reference(specs, ops):
    outdir = os.path.join(ROOT, "reference")
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        if f.endswith(".md"):
            os.remove(os.path.join(outdir, f))

    groups = {}
    for o in ops:
        groups.setdefault(((o["tags"] or ["Outros"])[0], o["service"]), []).append(o)

    written = []
    for (tag, svc), items in sorted(groups.items(), key=lambda kv: tag_slug(kv[0][0])):
        spec = specs[svc]
        schemas = spec["components"]["schemas"]
        L = ["# %s" % tag,
             "",
             "Serviço `%s` — base `https://api.wts.chat/%s`. Autenticação: `Authorization: Bearer <token>`." % (svc, svc),
             ""]
        used = set()
        for o in sorted(items, key=lambda o: (o["path"], o["method"])):
            op = spec["paths"][o["path"]][o["method"].lower()]
            L.append("## `%s` %s — %s" % (o["method"], o["full_path"], op.get("summary", "")))
            L.append("")
            if op.get("description"):
                L.append(clean(op["description"]))
                L.append("")
            params = op.get("parameters", [])
            if params:
                L.append("**Parâmetros**")
                L.append("")
                L.append("| Nome | Em | Obrig. | Tipo | Descrição |")
                L.append("|---|---|---|---|---|")
                for p in params:
                    collect_refs(p.get("schema", {}), used)
                    L.append("| `%s` | %s | %s | %s | %s |" % (
                        p["name"], p.get("in", ""), "sim" if p.get("required") else "-",
                        type_of(p.get("schema", {})), clean(p.get("description"))))
                L.append("")
            body = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
            if body:
                collect_refs(body, used)
                L.append("**Body** %s" % type_of(body))
                L.append("")
                props_table(body, schemas, L)
            ok = op.get("responses", {}).get("200") or op.get("responses", {}).get("201")
            sch = (ok or {}).get("content", {}).get("application/json", {}).get("schema") if ok else None
            if sch:
                collect_refs(sch, used)
                L.append("**Resposta 200** %s" % type_of(sch))
                L.append("")
                props_table(sch, schemas, L)
            elif ok:
                L.append("**Resposta 200** sem corpo.")
                L.append("")
            L.append("Erros: `400` `401` `429` `500` — ver envelope de erro no SKILL.md.  ")
            L.append("Doc: %s/reference/%s" % (BASE, o["page"]))
            L.append("")

        # fechamento transitivo dos schemas usados (sem os envelopes de erro)
        skip = {"InternalException", "ProblemDetails", "InternalExceptionId"}
        seen, queue = set(), [s for s in used if s not in skip]
        while queue:
            n = queue.pop()
            if n in seen or n in skip or n not in schemas:
                continue
            seen.add(n)
            nxt = set()
            collect_refs(schemas[n], nxt)
            queue.extend(nxt - seen)
        if seen:
            L.append("---")
            L.append("")
            L.append("## Schemas")
            L.append("")
            for n in sorted(seen):
                L.append("### %s" % n)
                L.append("")
                props_table(schemas[n], schemas, L)

        name = tag_slug(tag) + ".md"
        with open(os.path.join(outdir, name), "w", encoding="utf-8") as f:
            f.write("\n".join(L).rstrip() + "\n")
        written.append((name, tag, svc, len(items)))
    rendered = sum(open(os.path.join(outdir, w[0]), encoding="utf-8").read().count("\n## `")
                   for w in written)
    assert rendered == len(ops), "reference/ tem %d operacoes, esperado %d" % (rendered, len(ops))
    print("reference/: %d arquivos, %d operacoes" % (len(written), rendered))
    return written


def render_postman(specs):
    """Converte os specs em colecoes Postman via openapi-to-postmanv2 (npx) e normaliza a auth."""
    import shutil
    import subprocess
    outdir = os.path.join(ROOT, "postman")
    if not shutil.which("npx"):
        print("postman/: pulado (npx nao encontrado)")
        return
    os.makedirs(outdir, exist_ok=True)
    for svc in sorted(specs):
        dest = os.path.join(outdir, "%s.postman_collection.json" % svc)
        cmd = ["npx", "-y", "openapi-to-postmanv2@latest",
               "-s", os.path.join(ROOT, "openapi", svc + ".json"), "-o", dest, "-p",
               "-O", "folderStrategy=Tags,requestParametersResolution=Example"]
        if subprocess.run(cmd, capture_output=True).returncode != 0:
            print("postman/: falha ao converter %s" % svc)
            continue
        with open(dest, encoding="utf-8") as f:
            col = json.load(f)
        # ponytail: uma variavel {{token}} na colecao em vez de auth repetida em cada request
        col["auth"] = {"type": "bearer", "bearer": [{"key": "token", "value": "{{token}}", "type": "string"}]}
        col.setdefault("variable", [])
        if not any(v.get("key") == "token" for v in col["variable"]):
            col["variable"].append({"key": "token", "value": "pn_SEU_TOKEN_AQUI", "type": "string"})

        def strip_auth(items):
            n = 0
            for it in items:
                if "item" in it:
                    n += strip_auth(it["item"])
                elif it.get("request", {}).pop("auth", None) is not None:
                    n += 1
            return n

        n = strip_auth(col["item"])
        with open(dest, "w", encoding="utf-8") as f:
            json.dump(col, f, ensure_ascii=False, indent=2)
        print("  postman/%s.postman_collection.json (%d requests)" % (svc, n))


def render_llms_full(written, guides):
    parts = ["# flw.chat API — pacote completo",
             "",
             "Gerado de %s. Contém: referência rápida, guias oficiais e referência de todos os endpoints." % BASE,
             "", "---", ""]
    skill = os.path.join(ROOT, "SKILL.md")
    if os.path.exists(skill):
        md = open(skill, encoding="utf-8").read()
        md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)  # tira frontmatter
        parts += [md, "", "---", ""]
    parts += ["# Guias", ""]
    for entry, md in guides:
        parts += [md, "", "---", ""]
    parts += ["# Referência por domínio", ""]
    for name, tag, svc, _ in written:
        parts += [open(os.path.join(ROOT, "reference", name), encoding="utf-8").read(), "", "---", ""]
    with open(os.path.join(ROOT, "llms-full.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print("llms-full.md: %.0f KB" % (os.path.getsize(os.path.join(ROOT, "llms-full.md")) / 1024))


def inject_endpoints(ops):
    """Reescreve so o bloco marcado do SKILL.md, preservando o texto curado."""
    path = os.path.join(ROOT, "SKILL.md")
    if not os.path.exists(path):
        return
    order = {"core": 0, "chat": 1, "crm": 2}
    groups = {}
    for o in ops:
        groups.setdefault((o["service"], (o["tags"] or ["Outros"])[0]), []).append(o)
    lines = []
    last_svc = None
    for svc, tag in sorted(groups, key=lambda k: (order.get(k[0], 9), k[1])):
        if svc != last_svc:
            lines.append("\n### %s — `https://api.wts.chat/%s`\n" % (svc.upper(), svc))
            last_svc = svc
        lines.append("**%s**\n" % tag)
        lines.append("| Método | Path | O que faz | Doc |")
        lines.append("|---|---|---|---|")
        for o in sorted(groups[(svc, tag)], key=lambda o: (o["path"], o["method"])):
            lines.append("| `%s` | `%s` | %s | [↗](%s/reference/%s) |" % (
                o["method"], o["full_path"], o["summary"] or "-", BASE, o["page"]))
        lines.append("")
    block = "<!-- ENDPOINTS:START -->\n" + "\n".join(lines) + "\n<!-- ENDPOINTS:END -->"
    md = open(path, encoding="utf-8").read()
    md = re.sub(r"<!-- ENDPOINTS:START -->.*?<!-- ENDPOINTS:END -->", lambda _: block, md, flags=re.S)
    open(path, "w", encoding="utf-8").write(md)
    print("SKILL.md: indice com %d endpoints" % len(ops))


def main():
    use_cache = "--no-cache" not in sys.argv
    index = parse_index(fetch(BASE + "/llms.txt", use_cache))
    print("paginas no indice: %d" % len(index))

    with ThreadPoolExecutor(max_workers=8) as pool:
        pages = list(pool.map(lambda e: fetch(e["url"], use_cache), index))

    fragments, guides = [], []
    for entry, md in zip(index, pages):
        m = OAS_RE.search(md)
        if m:
            fragments.append((slug(entry["url"]), json.loads(m.group(1))))
        else:
            guides.append((entry, strip_boilerplate(md)))
    print("endpoints: %d | guias: %d" % (len(fragments), len(guides)))

    fragments.sort(key=lambda f: f[0])
    specs, conflicts, ops = merge(fragments)

    os.makedirs(os.path.join(ROOT, "openapi"), exist_ok=True)
    for svc, spec in specs.items():
        with open(os.path.join(ROOT, "openapi", svc + ".json"), "w", encoding="utf-8") as f:
            json.dump(spec, f, ensure_ascii=False, indent=2)
        print("  openapi/%s.json  paths=%d schemas=%d server=%s" % (
            svc, len(spec["paths"]), len(spec["components"]["schemas"]),
            spec["servers"][0]["url"] if spec["servers"] else "?"))

    gdir = os.path.join(ROOT, "guides")
    os.makedirs(gdir, exist_ok=True)
    for entry, md in guides:
        with open(os.path.join(gdir, slug(entry["url"]) + ".md"), "w", encoding="utf-8") as f:
            f.write(md)

    with open(os.path.join(ROOT, "index.json"), "w", encoding="utf-8") as f:
        json.dump({
            "source": BASE + "/llms.txt",
            "operations": sorted(ops, key=lambda o: (o["service"], o["path"], o["method"])),
            "guides": [{"title": e["title"], "slug": slug(e["url"]), "desc": e["desc"],
                        "url": e["url"][:-3]} for e, _ in guides],
        }, f, ensure_ascii=False, indent=2)

    inject_endpoints(ops)
    written = render_reference(specs, ops)
    render_llms_full(written, guides)
    render_postman(specs)

    # checagens
    print("\nconflitos de schema: %d" % len(conflicts))
    for c in conflicts:
        print("  " + c)
    total = sum(len(s["paths"]) for s in specs.values())
    assert len(ops) == len(set((o["service"], o["method"], o["path"]) for o in ops)), "operacao duplicada"
    assert len(ops) >= len(fragments), "operacoes (%d) < paginas de endpoint (%d)" % (len(ops), len(fragments))
    print("operacoes: %d em %d paths (paginas de endpoint: %d)" % (len(ops), total, len(fragments)))


if __name__ == "__main__":
    main()

from browser import document as doc, html, window as win
global c
c = doc["c"]
c.innerHTML += f"PYTHON {win.__BRYTHON__.__MAGIC__} ;]<br>READY<br>"
global stdin, thing
thing = ">>> "
stdin = ""
def arrow(thing):
    try:
        v = doc["v"]
        v.contentEditable = 'false'
        v.id = "n"
        v.unbind("keydown")
    except:
        pass
    v = html.DIV("", Class="out")
    v <= html.SPAN(serial(thing[:3]), Class="con") + html.SPAN(thing[3:].replace(" ", "\u200b \u200b"), Class="edt", Id="v")
    doc["c"] <= v
    v = doc["v"]
    v.bind("keydown", keys)
    v.contentEditable = 'true'
    v.focus()
    return v
def serial(st):
    st = st.replace("&", "&amp;")
    st = st.replace("<", "&lt;")
    st = st.replace(">", "&gt;")
    st = st.replace(" ", "\u200b \u200b")
    st = st.replace("\n", "<br>")
    return st
def print(*args, end = "\n", sep = " "):
    st = sep.join(args)+end
    doc["c"] <= html.DIV(serial(st), Class="out")
def null_print(*args, **kwargs):
    pass
def interpret():
  try:
    global stdin, thing
    c = doc["c"]
    v = doc["v"]
    nl = v.innerHTML.replace("\u200b", "").strip()
    if stdin:
        stdin += "\n"+nl
    else:
        stdin = nl
    if stdin.endswith(":") or ('.' in thing and nl):
        if thing == ">>> ":
            thing = "... "
        if stdin.endswith(":"):
            thing += "    "
        c <= arrow(thing)
        return
    
    if stdin.endswith("<br>") or ">" in thing or v.innerHTML.replace("\u200b", "").strip() == "":
        try:
            exec(stdin)
            try:
                out = eval(stdin, {"print": null_print})
            except:
                out = None
            typ = str(type(out)).split("'")[1]
            c <= html.DIV(serial(f"<{typ}> `{out}'"), Class="rtn")
        except Exception as ex:
            c <= html.DIV(serial(str(ex)), Class="err")
        thing = ">>> "
        c <= arrow(thing)
        stdin = ""
  except Exception as ex:
    print(ex)
def keys(k):
    if k.key == "Enter":
        interpret()
c <= arrow(thing)

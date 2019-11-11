from browser import document as doc, html, window as win, timer
global c
c = doc["c"]
ver = win.__BRYTHON__.__MAGIC__
c.innerHTML += f"<div style='text-align: center'>-------- PYTHON {ver} ;] --------</div>"
c.innerHTML += f"<div style='text-align: center'>----- INTERPRETER v2.7.3 ;] -----</div>"
c.innerHTML += "<div>STARTING...</div>"
import re
global stdin, thing
thing = ">>> "
stdin = ""
def arrow(thing):
    try:
        v = doc["v"]
        v.contentEditable = 'false'
        v.id = "n"
        v.unbind("keydown")
        v.blur()
    except:
        pass
    doc["c"] <= html.DIV()
    doc["c"] <= html.SPAN(serial(thing[:3]), Class="con")
    doc["c"] <= html.SPAN(thing[3:].replace(" ", "\u200b \u200b"), Class="edt", Id="v")
    v = doc["v"]
    v.bind("keydown", keys)
    v.contentEditable = 'true'
def serial(st):
    st = st.replace("&", "&amp;")
    st = st.replace("<", "&lt;")
    st = st.replace(">", "&gt;")
    st = st.replace(" ", "\u200b \u200b")
    st = st.replace("\n", "<br>")
    return st
def new_print(*args, end = "\n", sep = " "):
    st = sep.join(str(arg) for arg in args)+end
    doc["c"] <= html.DIV(serial(st), Class="out")
def null_print(*args, **kwargs):
    pass
def focuser():
    doc["v"].focus()
def interpret():
  try:
    global stdin, thing
    c = doc["c"]
    v = doc["v"]
    nl = v.innerHTML.replace("\u200b", "")
    nl = re.sub(r" *$", "", nl)
    nl = nl[1:] if nl.startswith(" ") else nl
    if stdin:
        stdin += "\n"+nl
    else:
        stdin = nl
    if nl.strip() and (stdin.endswith(":") or '.' in thing):
        if thing == ">>> ":
            thing = "... "
        thing = thing.strip()+" "
        for x in nl:
            if x != " ":
                break
            thing += " "
        if stdin.endswith(":"):
            thing += "    "
        arrow(thing)
        timer.set_timeout(focuser, 5)
        return
    
    if stdin.endswith("<br>") or ">" in thing or v.innerHTML.replace("\u200b", "").strip() == "":
        try:
            __builtins__.print = new_print
            exec(stdin.strip(), locals = globals(), globals = globals())
            try:
                __builtins__.print = null_print
                out = eval(stdin, locals = globals(), globals = globals())
            except:
                out = None
            typ = str(type(out)).split("'")[1]
            c <= html.DIV(serial(f"<{typ}> `{out}'"), Class="rtn")
        except Exception as ex:
            c <= html.DIV(serial(str(ex)), Class="err")
        thing = ">>> "
        arrow(thing)
        timer.set_timeout(focuser, 5)
        stdin = ""
  except Exception as ex:
    new_print(ex)
def keys(k):
    if k.key == "Enter":
        interpret()
c.innerHTML = c.innerHTML.replace("<div>STARTING...", "<div>READY</div>")
arrow(thing)
timer.set_timeout(focuser, 5)

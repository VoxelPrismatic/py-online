from browser import document as doc, html, window as win
global c
c = doc["c"]
c.innerHTML += f"Brython Console // Python v{win.__BRYTHON__.__MAGIC__}<br>"
global stdin, thing
thing = ">>> "
stdin = ""
def editable():
    doc["v"].contentEditable = 'true'
    doc["v"].bind("keydown", keys)
def arrow(thing):
    try:
        doc["v"].id = "n"
    except:
        pass
    v = html.DIV("", Class="out")
    v <= html.SPAN(serial(thing[:3]), Class="con")
    v <= html.SPAN(thing[3:].replace(" ", "\u200b \u200b"), Class="edt", Id="v")
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
    print("interpreter")
    global stdin, thing
    c = doc["c"]
    v = doc["v"]
    print("got stuff")
    if stdin:
        stdin += "\n"+v.innerHTML.replace("\u200b \u200b", " ")[1:]
    else:
        stdin = v.innerHTML.replace("\u200b \u200b", " ")[1:]
    print("stdin")
    if stdin.endswith(":"):
        if thing == ">>> ":
            thing = "... "
        thing += "    "
        c <= arrow(thing)
        editable()
        return
    print("thingy")
    if stdin.endswith("\n"):
        try:
            exec(stdin)
            try:
                out = eval(stdin, {"print": null_print})
            except:
                out = None
            typ = str(type(out)).split("'")[1]
            c <= html.DIV(serial(str(ex)), Class="rtn")
        except Exception as ex:
            c <= html.DIV(serial(str(ex)), Class="err")
        thing = ">>> "
        c <= arrow(thing)
        stdin = ""
        editable()
  except Exception as ex:
    print(ex)
def keys(k):
    if k.key == "Enter":
        interpret()
c <= arrow(thing)
editable()
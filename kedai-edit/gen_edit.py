#!/usr/bin/env python3
"""Generate kedai-edit/index.html: a tight 30 s vertical cut of the souvenir-shop walkthrough."""
import json, sys

OUT = sys.argv[1]

# (id, source in-point s, duration s, transition INTO this shot)
SHOTS = [
    ("hook",    62.8, 2.5, None),      # curly-hair doll close-up: frame-0 thumbnail
    ("pastel",   0.0, 2.4, "flash"),   # pastel plush keychains
    ("tower",    3.2, 2.8, "whipL"),   # keychain tower
    ("penyu",   13.6, 3.2, "punch"),   # turtle plush wall
    ("doll",    18.0, 2.4, "whipU"),   # orange hooded dolls
    ("magnet",  23.4, 2.8, "dip"),     # fridge magnets
    ("mini",    29.2, 3.2, "whipL"),   # mini turtle plush basket
    ("resin",   33.4, 2.8, "punch"),   # resin turtle keychains (blue baskets)
    ("set",     49.0, 2.8, "whipR"),   # red baskets, keychain sets
    ("helmet",  57.2, 2.0, "flash"),   # helmet turtle keychains
    ("end",     59.4, 3.2, "punch"),   # bunny + curly dolls, end card
]

starts, t = [], 0.0
for s in SHOTS:
    starts.append(round(t, 2)); t += s[2]
TOTAL = round(t, 2)

GRADE = {
    "preset": None, "intensity": 0.75,
    "adjust": {"exposure": 0.02, "contrast": 0.1, "highlights": -0.16, "shadows": 0.08,
               "whites": 0.0, "blacks": -0.06, "temperature": 0, "tint": 0,
               "vibrance": 0.06, "saturation": 0.04},
    "details": {"vignette": 0.04},
}

VARS = [
    {"id": "hookKicker", "type": "string", "label": "Hook kicker", "default": "Datang Terengganu?"},
    {"id": "hookBig", "type": "string", "label": "Hook headline", "default": "JANGAN BALIK"},
    {"id": "hookSub", "type": "string", "label": "Hook line 2", "default": "tanpa singgah kedai ni"},
    {"id": "endBig", "type": "string", "label": "End headline", "default": "Ole-ole Terengganu"},
    {"id": "endSub", "type": "string", "label": "End call to action", "default": "Save & tag geng travel kau"},
    {"id": "accent", "type": "color", "label": "Accent colour", "default": "#FFC93C"},
]

# Item chips: (id, comp start, duration, number, label, price or None)
def at(shot, off=0.15):
    return round(starts[[s[0] for s in SHOTS].index(shot)] + off, 2)

CHIPS = [
    ("c1", at("pastel"), 2.2, "01", "Keychain plush comel", None),
    ("c2", at("penyu"),  3.0, "02", "Penyu, ikon Terengganu", None),
    ("c3", at("magnet"), 2.6, "03", "Fridge magnet", "3 pcs RM10"),
    ("c4", at("mini"),   3.0, "04", "Penyu mini", None),
    ("c5", at("set"),    2.6, "05", "Keychain penyu", "1 set RM10"),
    ("c6", at("helmet"), 1.8, "06", "Penyu helmet", None),
]

SFX = []  # (id, file, start, dur, vol)
def sfx(i, f, s, d, v): SFX.append((i, f, round(max(s, 0), 2), d, v))

sfx("s-hit0", "impact-bass-1", 0.0, 1.6, 0.85)
sfx("s-spark0", "sparkle", 0.55, 1.6, 0.4)
for i, (sid, src, dur, tr) in enumerate(SHOTS):
    st = starts[i]
    if tr in ("whipL", "whipR", "whipU"):
        sfx(f"s-w{i}", "whoosh-short", st - 0.18, 0.58, 0.7)
    elif tr == "flash":
        sfx(f"s-w{i}", "whoosh", st - 0.25, 0.58, 0.6)
    elif tr == "punch":
        sfx(f"s-p{i}", "impact-bass-2", st, 1.2, 0.55)
    elif tr == "dip":
        sfx(f"s-d{i}", "click-soft", st, 0.37, 0.8)
for cid, cs, cd, *_ in CHIPS:
    sfx(f"s-pop-{cid}", "pop", cs + 0.05, 0.7, 0.5)
    if _[2]:
        sfx(f"s-ch-{cid}", "chime", cs + 0.45, 1.0, 0.35)
end_st = starts[-1]
sfx("s-riser", "riser", end_st - 1.6, 1.6, 0.45)
sfx("s-spark-end", "sparkle", end_st + 0.3, 1.6, 0.45)

h = []
h.append(f"""<!doctype html>
<html lang="ms" data-resolution="portrait"
  data-composition-variables='{json.dumps(VARS)}'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0b0b0e; }}
      body {{ font-family: "Inter", sans-serif; }}
      #root {{ --accent: #FFC93C; --ink: #101116; --paper: #FFF8EC; }}
      .cam {{ position: absolute; inset: 0; overflow: hidden; }}
      .cam video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .scrim-top {{ position: absolute; left: 0; top: 0; width: 1080px; height: 900px;
        background: linear-gradient(180deg, rgba(8,8,12,.62) 0%, rgba(8,8,12,.32) 55%, rgba(8,8,12,0) 100%); }}
      .scrim-end {{ position: absolute; inset: 0; background: radial-gradient(120% 70% at 50% 42%, rgba(8,8,12,.35) 0%, rgba(8,8,12,.78) 100%); }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 60; pointer-events: none; }}
      #dip {{ position: absolute; inset: 0; background: #000; opacity: 0; z-index: 59; pointer-events: none; }}
      /* hook */
      #hook-text {{ position: absolute; left: 70px; right: 70px; top: 300px; z-index: 40; text-align: left; }}
      #hook-kicker {{ font: 700 50px/1.1 "Inter", sans-serif; color: var(--paper); letter-spacing: .5px;
        text-shadow: 0 4px 18px rgba(0,0,0,.55); }}
      #hook-big {{ margin-top: 18px; font: 400 150px/0.95 "Archivo Black", sans-serif; color: var(--accent);
        letter-spacing: -2px; text-shadow: 0 8px 30px rgba(0,0,0,.5); }}
      #hook-sub {{ margin-top: 22px; font: 900 66px/1.05 "Inter", sans-serif; color: #fff;
        text-shadow: 0 6px 24px rgba(0,0,0,.6); }}
      #hook-sub .w {{ display: inline-block; margin-right: 16px; }}
      #hook-hl {{ display: inline-block; background: var(--accent); color: var(--ink); padding: 0 16px 4px; border-radius: 12px;
        text-shadow: none; }}
      /* chips */
      .chip {{ position: absolute; left: 60px; top: 1060px; z-index: 40; }}
      .chip-in {{ display: flex; align-items: center; gap: 22px; padding: 22px 34px 22px 22px; border-radius: 28px;
        background: rgba(12,13,18,.9); backdrop-filter: blur(22px); -webkit-backdrop-filter: blur(22px);
        box-shadow: 0 18px 50px rgba(0,0,0,.35); border: 1.5px solid rgba(255,255,255,.12); }}
      .num {{ font: 400 44px/1 "Archivo Black", sans-serif; color: var(--ink); background: var(--accent);
        border-radius: 18px; padding: 16px 16px 14px; min-width: 92px; text-align: center; }}
      .lbl {{ font: 900 52px/1.05 "Inter", sans-serif; color: #fff; white-space: nowrap; }}
      .price {{ position: absolute; left: 60px; top: 1210px; z-index: 41; }}
      .price-in {{ display: inline-block; font: 400 58px/1 "Archivo Black", sans-serif; color: var(--ink);
        background: var(--accent); padding: 20px 30px 18px; border-radius: 22px; transform-origin: 0% 50%;
        box-shadow: 0 14px 40px rgba(0,0,0,.35); }}
      /* end card */
      #end-text {{ position: absolute; left: 70px; right: 70px; top: 520px; z-index: 40; text-align: center; }}
      #end-kick {{ font: 700 46px/1.1 "Inter", sans-serif; color: var(--accent); letter-spacing: 4px; }}
      #end-big {{ margin-top: 20px; font: 400 128px/0.98 "Archivo Black", sans-serif; color: #fff;
        text-shadow: 0 8px 30px rgba(0,0,0,.5); }}
      #end-sub {{ display: inline-block; margin-top: 44px; font: 900 52px/1 "Inter", sans-serif; color: var(--ink);
        background: var(--accent); padding: 24px 40px; border-radius: 999px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}"
      data-width="1080" data-height="1920" data-motion-blur="on">""")

grade_attr = json.dumps(GRADE).replace('"', "&quot;")
for i, (sid, src, dur, tr) in enumerate(SHOTS):
    h.append(f"""
      <div id="cam-{sid}" class="cam" style="z-index:{i+1}">
        <video id="v-{sid}" class="clip" src="assets/kedai.mp4" playsinline data-has-audio="true" data-volume="0.35"
          data-start="{starts[i]}" data-duration="{dur}" data-media-start="{src}" data-track-index="0"
          data-color-grading="{grade_attr}"></video>
      </div>""")

hook_dur = SHOTS[0][2]
h.append(f"""
      <div id="hook-scrim" class="clip scrim-top" data-start="0" data-duration="{hook_dur}" data-track-index="1" style="z-index:30"></div>
      <div id="hook-text" class="clip" data-start="0" data-duration="{hook_dur - 0.02}" data-track-index="2">
        <div id="hook-kicker" data-var-text="hookKicker">Datang Terengganu?</div>
        <div id="hook-big" data-var-text="hookBig">JANGAN BALIK</div>
        <div id="hook-sub"><span class="w">tanpa</span><span class="w">singgah</span><span id="hook-hl" class="w">kedai ni</span></div>
      </div>""")

for cid, cs, cd, num, lbl, price in CHIPS:
    h.append(f"""
      <div id="{cid}" class="clip chip" data-start="{cs}" data-duration="{cd}" data-track-index="3">
        <div class="chip-in" id="{cid}-in"><div class="num">{num}</div><div class="lbl">{lbl}</div></div>
      </div>""")
    if price:
        h.append(f"""
      <div id="{cid}-p" class="clip price" data-start="{round(cs+0.35,2)}" data-duration="{round(cd-0.35,2)}" data-track-index="4">
        <div class="price-in" id="{cid}-pin">{price}</div>
      </div>""")

end_dur = SHOTS[-1][2]
h.append(f"""
      <div id="end-scrim" class="clip scrim-end" data-start="{round(end_st+0.25,2)}" data-duration="{round(end_dur-0.25,2)}" data-track-index="1" style="z-index:30"></div>
      <div id="end-text" class="clip" data-start="{round(end_st+0.35,2)}" data-duration="{round(end_dur-0.35,2)}" data-track-index="2">
        <div id="end-kick">SEBELUM BALIK</div>
        <div id="end-big" data-var-text="endBig">Ole-ole Terengganu</div>
        <div id="end-sub" data-var-text="endSub">Save &amp; tag geng travel kau</div>
      </div>
      <div id="flash"></div>
      <div id="dip"></div>""")

for i, f, s, d, v in SFX:
    h.append(f"""
      <audio id="{i}" class="clip" src="assets/sfx/{f}.mp3" data-start="{s}" data-duration="{d}" data-volume="{v}" data-track-index="{6 + (SFX.index((i,f,s,d,v)) % 2)}"></audio>""")

# ---------------- timeline ----------------
js = ["const tl = gsap.timeline({ paused: true });",
      "const vars = (window.__hyperframes && window.__hyperframes.getVariables) ? window.__hyperframes.getVariables() : {};",
      "if (vars.accent) document.getElementById('root').style.setProperty('--accent', vars.accent);"]
for i, (sid, src, dur, tr) in enumerate(SHOTS):
    st, en = starts[i], round(starts[i] + dur, 2)
    cam = f"#cam-{sid}"
    nxt = SHOTS[i + 1][3] if i + 1 < len(SHOTS) else None
    # entrance
    if tr == "punch":
        js.append(f'tl.fromTo("{cam}", {{scale:1.32}}, {{scale:1.08, duration:0.45, ease:"expo.out"}}, {st});')
        js.append(f'tl.to("{cam}", {{scale:1.0, duration:{round(dur-0.45,2)}, ease:"none"}}, {round(st+0.45,2)});')
    elif tr in ("whipL", "whipR", "whipU"):
        prop = "y" if tr == "whipU" else "x"
        sign = {"whipL": 1, "whipR": -1, "whipU": 1}[tr]
        js.append(f'tl.fromTo("{cam}", {{{prop}:{sign*170}, scale:1.28}}, {{{prop}:0, scale:1.1, duration:0.3, ease:"expo.out"}}, {st});')
        js.append(f'tl.to("{cam}", {{scale:1.02, duration:{round(dur-0.3,2)}, ease:"none"}}, {round(st+0.3,2)});')
    else:
        js.append(f'tl.fromTo("{cam}", {{scale:1.0}}, {{scale:1.08, duration:{dur}, ease:"none"}}, {st});')
    # exit, matching the next shot's entrance
    if nxt in ("whipL", "whipR", "whipU"):
        prop = "y" if nxt == "whipU" else "x"
        sign = {"whipL": -1, "whipR": 1, "whipU": -1}[nxt]
        js.append(f'tl.to("{cam}", {{{prop}:{sign*170}, scale:1.28, duration:0.16, ease:"power3.in", overwrite:"auto"}}, {round(en-0.16,2)});')
    # transitions that use overlays
    if tr == "flash":
        js.append(f'tl.fromTo("#flash", {{opacity:0.85}}, {{opacity:0, duration:0.35, ease:"power2.out", immediateRender:false}}, {st});')
        js.append(f'tl.fromTo("#flash", {{opacity:0}}, {{opacity:0.85, duration:0.08, ease:"power2.in", immediateRender:false}}, {round(st-0.08,2)});')
    if tr == "dip":
        js.append(f'tl.fromTo("#dip", {{opacity:0}}, {{opacity:0.45, duration:0.1, ease:"none", immediateRender:false}}, {round(st-0.1,2)});')
        js.append(f'tl.set("#dip", {{opacity:0}}, {st});')

# Hook text: kicker + headline on screen at frame 0 (thumbnail), settle in; sub per-word blur-in
js += [
    'tl.fromTo("#hook-big", {scale:1.12, transformOrigin:"0% 50%"}, {scale:1, duration:0.5, ease:"expo.out"}, 0);',
    
    'tl.fromTo("#hook-sub .w", {opacity:0, filter:"blur(8px)"}, {opacity:1, filter:"blur(0px)", duration:0.16, stagger:0.09, ease:"power2.out"}, 0.45);',
    'tl.fromTo("#hook-hl", {scale:0.6}, {scale:1, duration:0.45, ease:"back.out(1.6)"}, 0.68);',
    f'tl.to("#hook-text", {{opacity:0, filter:"blur(10px)", duration:0.2, ease:"power2.in"}}, {round(hook_dur-0.24,2)});',
]
for cid, cs, cd, num, lbl, price in CHIPS:
    js += [
        f'tl.fromTo("#{cid}-in", {{x:-80, opacity:0, filter:"blur(8px)"}}, {{x:0, opacity:1, filter:"blur(0px)", duration:0.45, ease:"expo.out"}}, {cs});',
        f'tl.fromTo("#{cid} .num", {{scale:0.4}}, {{scale:1, duration:0.5, ease:"back.out(1.7)"}}, {round(cs+0.08,2)});',
        f'tl.to("#{cid}-in", {{x:-60, opacity:0, filter:"blur(6px)", duration:0.22, ease:"power3.in"}}, {round(cs+cd-0.26,2)});',
    ]
    if price:
        ps, pd = round(cs + 0.35, 2), round(cd - 0.35, 2)
        js += [
            f'tl.fromTo("#{cid}-pin", {{scale:0, rotation:-8}}, {{scale:1, rotation:-3, duration:0.5, ease:"back.out(1.8)"}}, {ps});',
            f'tl.to("#{cid}-pin", {{scale:0.8, opacity:0, duration:0.2, ease:"power3.in"}}, {round(ps+pd-0.24,2)});',
        ]
es = round(end_st + 0.35, 2)
js += [
    f'tl.fromTo("#end-scrim", {{opacity:0}}, {{opacity:1, duration:0.4, ease:"power2.out"}}, {round(end_st+0.25,2)});',
    f'tl.fromTo("#end-kick", {{opacity:0, y:-20}}, {{opacity:1, y:0, duration:0.5, ease:"expo.out"}}, {es});',
    f'tl.fromTo("#end-big", {{opacity:0, filter:"blur(10px)", scale:1.08}}, {{opacity:1, filter:"blur(0px)", scale:1, duration:0.5, ease:"expo.out"}}, {round(es+0.15,2)});',
    f'tl.fromTo("#end-sub", {{opacity:0, y:40, scale:0.9}}, {{opacity:1, y:0, scale:1, duration:0.55, ease:"back.out(1.5)"}}, {round(es+0.55,2)});',
]
js.append('window.__timelines["main"] = tl;')

h.append("""
    </div>
    <script>
      """ + "\n      ".join(js) + """
    </script>
  </body>
</html>
""")
open(OUT, "w").write("".join(h))
print("total", TOTAL, "starts", starts)

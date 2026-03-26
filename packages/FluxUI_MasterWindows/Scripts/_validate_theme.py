import json
with open('FLUXIDE/extensions/flux-theme/themes/flux-theme.json', encoding='utf-8') as f:
    d = json.load(f)
tc = d.get('tokenColors', [])
print(f"Theme valid. {len(tc)} tokenColor rules, {len(d['colors'])} UI color rules.")
with open('FLUXIDE/extensions/flux-language/syntaxes/flux.tmLanguage.json', encoding='utf-8-sig') as f:
    g = json.load(f)
print(f"Grammar valid. {len(g['repository'])} rules, {len(g['patterns'])} top-level patterns.")

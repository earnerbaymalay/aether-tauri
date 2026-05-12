<div align="center">

# 🎨 Aether — Frontend Style Guide

*Design system reference for the Tauri UI.*

</div>

---

## Design Philosophy

The Aether UI is built around three principles:

1. **Terminal-native aesthetics** — The UI should feel like a premium terminal environment, not a generic web app.
2. **Purposeful restraint** — Every visual element serves a function. No decorative complexity without meaning.
3. **Seamless integration** — The xterm.js terminal and the surrounding chrome must feel like one unified surface.

---

## Color System

All colors are defined as CSS custom properties on `:root` in `src/styles/app.css`. **Never hardcode a hex value** in a component rule — always use the token.

### Palette Reference

| Token | Value | Role |
| :--- | :--- | :--- |
| `--bg` | `#0d1117` | Application canvas (deepest layer) |
| `--surface` | `#161b22` | Header bar, sidebars, panel backgrounds |
| `--card` | `#1c2333` | Cards, modals, elevated surfaces |
| `--border` | `#30363d` | All borders, dividers, and separators |
| `--teal` | `#58a6ff` | **Primary accent** — active states, links, xterm cursor, teal button borders |
| `--green` | `#3fb950` | Success / online / throughput indicators |
| `--orange` | `#ffa657` | Warnings and degraded states |
| `--purple` | `#bc8cff` | Nexus Shield accent |
| `--red` | `#ff7b72` | Errors and destructive states |
| `--text` | `#e6edf3` | Primary body text |
| `--text-dim` | `#8b949e` | Labels, secondary text, captions |
| `--text-muted` | `#484f58` | Placeholders and decorative text |

This palette mirrors GitHub's Dark High-Contrast theme — a deliberate choice for developer familiarity and WCAG contrast compliance.

### Usage Rules

```css
/* ✅ Correct */
.my-component {
  background: var(--card);
  border: 1px solid var(--border);
  color: var(--text);
}

/* ❌ Incorrect — never hardcode */
.my-component {
  background: #1c2333;
  border: 1px solid #30363d;
}
```

---

## Typography

### UI Chrome

The header, labels, and controls use the **system font stack** for native rendering performance:

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

### Terminal

The xterm.js terminal uses a **monospace coding font stack** with JetBrains Mono as the preferred choice:

```js
fontFamily: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace"
```

### Scale

| Usage | Size | Color |
| :--- | :--- | :--- |
| App title (`AETHER`) | `18px` | `--teal` |
| Subtitle / labels | `10px` | `--text-dim` (letter-spacing: 2–4px) |
| Pathway card title | `18px` | `--text` |
| Pathway model name | `11px` | `--text-dim` (monospace) |
| Pathway description | `12px` | `--text-dim` |
| Speed indicator | `11px` | `--green` |
| Button text | `13px` | `--text` |
| Small button | `11px` | `--text` |
| Info panel section | `12px` | `--text-dim` (letter-spacing: 2px) |

---

## Component Library

### Buttons

All buttons use the `.btn` base class:

```css
.btn {
  background: var(--card);
  color: var(--text);
  border: 1px solid var(--border);
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}
.btn:hover { background: var(--border); border-color: var(--teal); }
```

**Variants:**
- `.btn-small` — Reduced padding (`4px 10px`) and size (`11px`)
- `.btn-nexus` — Purple border (`--purple`) with purple hover background tint

**Example:**
```html
<button class="btn">Primary Action</button>
<button class="btn btn-small">← Back</button>
<button class="btn btn-small btn-nexus">🛡️ Nexus Shield</button>
```

---

### Pathway Cards

The pathway selector cards use a hover-lift + gradient-reveal pattern:

```
Resting state:   flat card, --border border
Hover state:     translateY(-4px), --teal border, gradient top strip fades in
```

The gradient strip is implemented with `::before` at `opacity: 0`, transitioning to `opacity: 1` on hover:

```css
.pathway-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--teal), var(--purple));
  opacity: 0;
  transition: opacity 0.3s;
}
.pathway-card:hover::before { opacity: 1; }
```

---

### Toggle Switches

Pure CSS toggles using the `.switch` + `.slider` pattern (no JavaScript):

```html
<label class="switch">
  <input type="checkbox" id="toggle-privacy" checked>
  <span class="slider"></span>
</label>
```

- **Off state:** `--border` background
- **On state:** `--teal` background, knob slides right by `20px`
- Size: `40px × 20px` pill

---

### Modal Overlays

The Nexus panel uses the standard overlay pattern:

```css
.nexus-panel {
  position: fixed;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  background: var(--surface);
  border: 1px solid var(--teal);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 0 50px rgba(0,0,0,0.8);
  z-index: 100;
}
```

New modals should follow this same pattern. Always pair with a `.hidden` toggle and a close button that re-adds `.hidden`.

---

### Status Indicators

| State | Class / Token | Example |
| :--- | :--- | :--- |
| OK / Online | `color: var(--green)` `.ok` | `✓ Found` |
| Warning / Degraded | `color: var(--orange)` `.warn` | `✗ Not found` |
| Error | `color: var(--red)` `.error` | `Failed to load` |

---

### Layout

The main content area is a flex row:

```
<main class="main-content">       ← flex row, height: calc(100vh - 56px)
  <div class="pathway-selector">  ← flex: 1, scrollable
  OR
  <div class="terminal-container"> ← flex: 1
  
  <aside class="info-panel">      ← fixed 260px sidebar, --surface bg
</main>
```

The header is fixed at `56px` height (`padding: 12px 20px` + content).

---

## Animation Conventions

| Interaction | Duration | Easing |
| :--- | :--- | :--- |
| Button hover | `0.2s` | `default (ease)` |
| Card hover + gradient reveal | `0.3s` | `ease` |
| Toggle switch | `0.4s` | `default` |
| Modal appear | Use `.hidden` class toggle (no animation currently) |

Keep animations **subtle and purposeful**. If an animation would exceed 500ms or involve complex keyframes, reconsider whether it adds value.

---

## Accessibility Notes

- All interactive elements have unique `id` attributes for automation and testing.
- Color is never the *only* indicator of state — text labels accompany all status colors.
- The toggle switch label wraps the input, making the full card area the click target.
- Avoid `outline: none` without providing a custom focus style for keyboard navigation.

---

## Adding New Components

Follow this checklist when adding a new UI component:

1. **Use existing tokens only** — refer to the palette above.
2. **Add styles to `app.css`** — do not use inline styles or `<style>` blocks in HTML.
3. **Name your CSS class semantically** — `.vault-panel`, not `.panel-2`.
4. **Include hover/focus transitions** — all interactive elements must respond to pointer interaction.
5. **Give all inputs and buttons unique `id` attributes** for testability.
6. **Document the component** in this file if it's reusable across the app.

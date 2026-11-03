---
title: "Media Block Template"
uuid: "system-media-template-001"
date_created: "2026-03-05"
status: "canonical"
tags:
  - system/template
  - system/media
---

# Media Block Template for Articles

## Usage
Place this callout block after the article's opening section (after the Structural Index, before the main body). The block shows only the items that have links — empty items are hidden gracefully.

## The Template (copy into each article)

```markdown
> [!info]- 🎧 Listen, Watch & Download
>
> **Podcasts**
> - 🎙️ Debate Format (Stress Test): `{{podcast_debate_link || "Coming soon"}}`
> - 🎙️ Deep Dive (Full Episode): `{{podcast_deepdive_link || "Coming soon"}}`
>
> **Audio**
> - 🔊 Article Narration: `{{audio_narration_link || "Coming soon"}}`
>
> **Slides & Downloads**
> - 📊 Presentation Slides: `{{slides_link || "Coming soon"}}`
> - 📁 Download All Files: `{{gdrive_link || "Coming soon"}}`
>
> *Items marked "Coming soon" are in production. Check back or subscribe for updates.*
```

## Live Example (with real links)

```markdown
> [!info]- 🎧 Listen, Watch & Download
>
> **Podcasts**
> - 🎙️ [Debate Format — The First Quantum State](https://notebooklm.google.com/notebook/xxxxx) *(stress test — two AI voices challenge the argument)*
> - 🎙️ [Deep Dive — The First Quantum State](https://notebooklm.google.com/notebook/yyyyy) *(full episode — the complete story)*
>
> **Audio**
> - 🔊 [Article Narration (12 min)](link-to-audio.m4a)
>
> **Slides & Downloads**
> - 📊 [Presentation Slides (PDF)](link-to-slides.pdf)
> - 📁 [Download All Files (Google Drive)](https://drive.google.com/drive/folders/xxxxx)
>
> *Subscribe to get notified when new episodes drop.*
```

## Live Example (partial — some items not ready)

```markdown
> [!info]- 🎧 Listen, Watch & Download
>
> **Podcasts**
> - 🎙️ [Debate Format — The First Quantum State](https://notebooklm.google.com/notebook/xxxxx) *(stress test — two AI voices challenge the argument)*
> - 🎙️ Deep Dive: *Coming soon*
>
> **Audio**
> - 🔊 [Article Narration (12 min)](link-to-audio.m4a)
>
> **Downloads**
> - 📁 [Download All Files (Google Drive)](https://drive.google.com/drive/folders/xxxxx)
>
> *Some items are still in production. Subscribe for updates.*
```

## CSS for Quartz/Web Version

For the web-published version, the media block gets custom styling:

```css
/* Media callout — distinct from content callouts */
.callout[data-callout="info"] {
  background: linear-gradient(135deg, rgba(212, 175, 55, 0.08), rgba(212, 175, 55, 0.03));
  border-left: 3px solid #d4af37;
  border-radius: 8px;
  padding: 16px 20px;
  margin: 24px 0;
}

.callout[data-callout="info"] .callout-title {
  color: #d4af37;
  font-weight: 600;
  font-size: 1.1em;
}

.callout[data-callout="info"] a {
  color: #f4d03f;
  text-decoration: none;
  border-bottom: 1px dotted rgba(244, 208, 63, 0.4);
}

.callout[data-callout="info"] a:hover {
  color: #fff;
  border-bottom-color: #fff;
}

/* "Coming soon" items — subtle, not attention-grabbing */
.callout[data-callout="info"] em {
  color: rgba(184, 184, 184, 0.6);
  font-style: italic;
}
```

## Automation Notes

### For the Python converter script:

The script should read YAML frontmatter for media links. Add these fields to the article YAML:

```yaml
media:
  podcast_debate: ""          # URL or empty
  podcast_deepdive: ""        # URL or empty  
  audio_narration: ""         # URL or empty
  audio_duration: ""          # e.g., "12 min"
  slides: ""                  # URL or empty
  gdrive_folder: ""           # URL or empty
```

The script generates the media callout block from these fields:
- If a field has a URL → render as clickable link
- If a field is empty → render as "Coming soon" in italics
- If ALL fields are empty → don't render the block at all (no empty media box)

```python
def generate_media_block(yaml_media):
    """Generate Obsidian media callout from YAML media fields."""
    if not yaml_media or all(v == "" for v in yaml_media.values()):
        return ""  # No media block if nothing exists
    
    lines = ['> [!info]- 🎧 Listen, Watch & Download', '>']
    
    # Podcasts
    lines.append('> **Podcasts**')
    if yaml_media.get('podcast_debate'):
        lines.append(f'> - 🎙️ [Debate Format]({yaml_media["podcast_debate"]}) *(stress test)*')
    else:
        lines.append('> - 🎙️ Debate Format: *Coming soon*')
    
    if yaml_media.get('podcast_deepdive'):
        lines.append(f'> - 🎙️ [Deep Dive]({yaml_media["podcast_deepdive"]}) *(full episode)*')
    else:
        lines.append('> - 🎙️ Deep Dive: *Coming soon*')
    
    lines.append('>')
    
    # Audio
    lines.append('> **Audio**')
    if yaml_media.get('audio_narration'):
        dur = yaml_media.get('audio_duration', '')
        dur_str = f' ({dur})' if dur else ''
        lines.append(f'> - 🔊 [Article Narration{dur_str}]({yaml_media["audio_narration"]})')
    else:
        lines.append('> - 🔊 Article Narration: *Coming soon*')
    
    lines.append('>')
    
    # Downloads
    lines.append('> **Downloads**')
    if yaml_media.get('slides'):
        lines.append(f'> - 📊 [Presentation Slides]({yaml_media["slides"]})')
    if yaml_media.get('gdrive_folder'):
        lines.append(f'> - 📁 [Download All Files]({yaml_media["gdrive_folder"]})')
    if not yaml_media.get('slides') and not yaml_media.get('gdrive_folder'):
        lines.append('> - 📁 Downloads: *Coming soon*')
    
    lines.append('>')
    lines.append('> *Items marked "Coming soon" are in production.*')
    
    return '\n'.join(lines)
```

### For the preflight checklist:

Add to Section D (Images & Media):
- [ ] **Media YAML fields populated** (at least podcast_debate OR audio_narration has a URL)
- [ ] **Media callout block present** in article (if any media exists)
- [ ] **All media URLs resolve** (HTTP 200)
- [ ] **Audio files are > 30 seconds** (not empty/corrupt)

---

## Placement in Article

```
---
YAML frontmatter
---

> [!abstract]- 📋 Structural Index — [Title]     ← FIRST (collapsed)
> ...

---

> [!info]- 🎧 Listen, Watch & Download           ← SECOND (collapsed)
> ...

---

# Article Title                                    ← THIRD (the actual content)
...
```

The structural index comes first (for researchers). The media block comes second (for listeners/downloaders). The article starts third. Both callouts are collapsed by default so readers who just want to read aren't interrupted.

---

*This template lives at: `00_AI/AI_VAULT/MEDIA_BLOCK_TEMPLATE.md`*
*Used by: All published articles in Convergence, GTQ, and Logos Papers*

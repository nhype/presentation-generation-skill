# Presentation Generation Skill for Claude Code

A Claude Code skill that generates professional HTML and PDF presentations from markdown content, URLs, or topic descriptions. It creates visually stunning slides with AI-generated illustrations, keyboard navigation, and automatic PDF export.

## Features

- **Multiple input sources** — markdown files, URLs, plain text, or topic descriptions
- **Design matching** — analyzes reference images in `references/` folder and replicates the visual style
- **AI-generated illustrations** — creates custom images for each slide using OpenAI GPT Image models
- **Interactive HTML** — full-viewport slides with keyboard navigation, progress bar, and slide counter
- **PDF export** — automatic conversion of slides to a single PDF document
- **Editable content** — exports `content.md` for easy re-generation with updated text

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- [Node.js](https://nodejs.org/) 18+ (for the MCP server)
- [Python 3](https://www.python.org/) + [Pillow](https://pillow.readthedocs.io/) (for PDF export)
- [OpenAI API key](https://platform.openai.com/api-keys) (for image generation)
- Playwright MCP server (optional, for slide screenshot validation)

## Installation

### Option 1: Clone and copy (recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/presentation-generation-skill.git

# Copy the skill to your project
cp -r presentation-generation-skill/skills/generate-presentation YOUR_PROJECT/.claude/skills/
```

### Option 2: Personal skill (available in all projects)

```bash
cp -r presentation-generation-skill/skills/generate-presentation ~/.claude/skills/
```

### Set up the MCP server

The skill requires the OpenAI GPT Image MCP server for generating slide illustrations.

```bash
# Build the MCP server
cd presentation-generation-skill/mcp-servers/openai-gpt-image
npm install
npm run build
```

Add to your project's `.mcp.json` (create if it doesn't exist):

```json
{
  "mcpServers": {
    "openai-gpt-image-mcp": {
      "command": "node",
      "args": [
        "/absolute/path/to/mcp-servers/openai-gpt-image/dist/index.js",
        "--env-file",
        "/absolute/path/to/.env"
      ]
    }
  }
}
```

Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=sk-your-key-here
```

### Install Python dependency

```bash
pip install Pillow
```

## Usage

In Claude Code, run:

```
/generate-presentation My startup pitch deck about AI-powered analytics
```

Or with a markdown file:

```
/generate-presentation presentation/content.md
```

Or with a URL:

```
/generate-presentation https://example.com/blog-post-to-present
```

### Design References

Place reference images in a `references/` folder in your project root. The skill will analyze these images and match the visual style (colors, typography, layout) in the generated slides.

```
your-project/
├── references/
│   ├── design-reference-1.png
│   └── design-reference-2.jpg
├── presentation/           # Generated output goes here
│   ├── slides.html
│   ├── presentation.pdf
│   ├── content.md
│   ├── slide_1.png
│   └── images/
└── .claude/
    └── skills/
        └── generate-presentation/
```

If no reference images are provided, the skill uses a clean modern default style.

### Re-generating

After the presentation is created, edit `presentation/content.md` and run:

```
/generate-presentation presentation/content.md
```

This regenerates all slides with your updated content while keeping the same visual style.

## Output

| File | Description |
|------|-------------|
| `presentation/slides.html` | Interactive HTML presentation (open in browser) |
| `presentation/presentation.pdf` | PDF export (one slide per page, 1920x1080) |
| `presentation/slide_N.png` | Individual slide screenshots |
| `presentation/images/` | AI-generated illustrations |
| `presentation/content.md` | Editable markdown source |

## How It Works

1. **Content gathering** — Reads your input (markdown, URL, or topic) and structures it into slides
2. **Design analysis** — Studies reference images to extract color palette, typography, and layout patterns
3. **HTML generation** — Creates a self-contained HTML file with all slides
4. **Image generation** — Uses OpenAI GPT Image to create custom illustrations for slides
5. **Validation** — Screenshots each slide and compares against reference design, iterating until it matches
6. **PDF export** — Converts slide screenshots into a single PDF document
7. **Content export** — Generates editable `content.md` for future regeneration

## Project Structure

```
presentation-generation-skill/
├── skills/
│   └── generate-presentation/
│       ├── SKILL.md                 # Main skill definition
│       ├── scripts/
│       │   └── slides_to_pdf.py     # PDF conversion utility
│       └── templates/
│           └── slide-template.html  # HTML slide template
├── mcp-servers/
│   └── openai-gpt-image/           # Bundled MCP server for image generation
│       ├── src/index.ts
│       ├── package.json
│       └── tsconfig.json
├── examples/
│   └── example-content.md          # Example input markdown
├── README.md
└── LICENSE                          # Apache 2.0
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.

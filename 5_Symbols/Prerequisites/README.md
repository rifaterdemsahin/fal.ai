# Prerequisites Symbols

This folder contains assets and generators for the Prerequisites section of the presentation/content.

## Contents

- `PrerequisitesGenerator.py`: Python script to generate the sprite sheet assets using Fal.ai.
- `generated_prerequisites/`: Directory containing the generated assets.

## Workflow

The prerequisites are visualized as "animated bullet points" effectively created as a sprite sheet. The steps are:

1. **Goto n8n.com**: Browser view.
2. **Open an account**: Sign up interface.
3. **Try out online**: Workflow editor.
4. **Setup environment**: Local coding environment.

## Usage

Run the generator:

```bash
python PrerequisitesGenerator.py
```

Ensure `FAL_KEY` is set in the parent `.env` file or environment variables.

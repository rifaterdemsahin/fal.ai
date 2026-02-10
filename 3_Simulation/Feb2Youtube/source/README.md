# Source Files Directory

## Overview
This directory contains all source materials for video production pre-production planning. As a video production assistant, these files help organize and plan content generation before the actual production begins.

## File Structure

### Core Source Files
All source files follow the `source_*` naming convention for consistency:

1. **source_transcript.md** - Complete video script with dialogue and scene descriptions
2. **source_subtitle.srt** - Subtitle/caption file in SubRip format with timestamps
3. **source_edl.md** - Edit Decision List with cutting points and transitions
4. **source_chapter_markers.txt** - Chapter markers and scene timestamps for video navigation

### Pre-Production Planning Files

5. **source_storyboard.md** - Visual planning with frame-by-frame descriptions, camera angles, and mood notes
6. **source_shotlist.md** - Detailed shot-by-shot breakdown with equipment needs and technical specifications
7. **source_broll.md** - B-roll footage planning organized by scene and category
8. **source_music.md** - Music tracks, sound effects, and audio cues with timing and licensing information
9. **source_graphics.md** - Graphics, overlays, motion graphics, and visual elements planning

## Purpose

These files serve as the foundation for:
- **Pre-production planning** - Organize all elements before shooting
- **Production guidance** - Reference during filming and recording
- **Post-production workflow** - Guide editing, effects, and finishing
- **Team collaboration** - Share consistent vision across departments
- **Asset management** - Track all required materials and resources

## Usage Guidelines

### For Producers
- Review all files to understand scope and requirements
- Use files to create production schedules and budgets
- Identify resource needs and potential challenges

### For Directors
- Use storyboard and shotlist for visual planning
- Reference transcript for performance direction
- Coordinate with all departments using these docs

### For Editors
- Start with EDL for cutting structure
- Use chapter markers for organization
- Reference all files during assembly and refinement

### For Audio Team
- Follow music.md for audio design
- Use transcript for dialogue timing
- Sync sound effects per planning docs

### For Graphics Team
- Implement designs from graphics.md
- Match timing specified in files
- Maintain consistency across all elements

## File Format Standards

- **Markdown (.md)** - Documentation, planning, and structured content
- **Text (.txt)** - Simple lists and data
- **SubRip (.srt)** - Standard subtitle format with timestamps

## Timestamp Convention

**Important:** There is a timestamp offset across source files:
- **Core source files** (subtitle.srt, edl.md, chapter_markers.txt, transcript.md): Use **01:00:00** as the base timestamp
- **Planning files** (storyboard, shotlist, broll, music, graphics): Use **00:00:00** as the base for easier planning

**Note for Production:** When implementing the planning documents during actual production/post-production, add 1 hour (01:00:00) to all timestamps in the planning files to align with the final video timeline in the core source files. This offset exists because planning documents start from a zero base for simplicity during the pre-production phase.

## Workflow Integration

1. **Start with transcript** - Core narrative and structure
2. **Create storyboard** - Visual interpretation
3. **Develop shotlist** - Technical breakdown
4. **Plan B-roll** - Supplementary footage
5. **Design audio** - Music and sound
6. **Plan graphics** - Visual elements
7. **Generate EDL** - Edit structure
8. **Add chapter markers** - Navigation
9. **Prepare subtitles** - Accessibility

## Version Control

All files are version controlled with Git:
- Changes are tracked
- History is preserved
- Collaboration is enabled
- Rollback is possible

## Contributing

When adding or modifying source files:
1. Follow the `source_*` naming convention
2. Use markdown for documentation
3. Include timestamps where relevant
4. Keep content organized and clear
5. Update this README if adding new file types

## File Dependencies

```
source_transcript.md (core narrative)
    ├── source_storyboard.md (visual interpretation)
    │   ├── source_shotlist.md (technical specs)
    │   └── source_broll.md (supplementary footage)
    ├── source_edl.md (editing structure)
    ├── source_chapter_markers.txt (navigation)
    ├── source_subtitle.srt (captions)
    ├── source_music.md (audio design)
    └── source_graphics.md (visual elements)
```

## Contact

For questions about source files or pre-production workflow:
- Check this README first
- Review individual file documentation
- Consult with production team

---

**Last Updated:** 2026-02-10  
**Production:** Feb2Youtube  
**Status:** Pre-production planning phase

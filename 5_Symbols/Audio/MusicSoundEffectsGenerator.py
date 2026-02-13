#!/usr/bin/env python3
"""
Music & Sound Effects Generator - Cost-Effective Edition
Generates audio files using free synthesis libraries (pydub, numpy)
Perfect for background music and sound effects
"""

import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List

try:
    from pydub import AudioSegment
    from pydub.generators import Sine, Square, Sawtooth, Triangle, WhiteNoise
except ImportError:
    print("❌ pydub not installed. Run: pip install pydub")
    sys.exit(1)


class MusicSoundEffectsGenerator:
    """Generates music tracks and sound effects using audio synthesis"""

    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir) / "audio"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Audio specifications
        self.sample_rate = 48000  # 48kHz for video production
        self.bit_depth = 16  # 16-bit for compatibility

    def create_whoosh_transition(self, duration_ms: int = 500) -> AudioSegment:
        """Create a whoosh transition sound effect"""
        # Start with white noise
        noise = WhiteNoise().to_audio_segment(duration=duration_ms)

        # Apply fade in and fade out for whoosh effect
        whoosh = noise.fade_in(100).fade_out(100)

        # Reduce volume
        whoosh = whoosh - 20

        return whoosh

    def create_tech_beep(self, frequency: int = 880, duration_ms: int = 200) -> AudioSegment:
        """Create a tech/UI beep sound"""
        beep = Sine(frequency).to_audio_segment(duration=duration_ms)
        beep = beep.fade_in(10).fade_out(50)
        beep = beep - 15
        return beep

    def create_success_chime(self) -> AudioSegment:
        """Create a success notification chime (3-tone)"""
        # Three ascending tones: C5, E5, G5
        note1 = Sine(523).to_audio_segment(duration=150) - 12
        note2 = Sine(659).to_audio_segment(duration=150) - 12
        note3 = Sine(784).to_audio_segment(duration=200) - 12

        # Add slight gap and combine
        silence = AudioSegment.silent(duration=50)
        chime = note1 + silence + note2 + silence + note3

        return chime.fade_out(100)

    def create_error_beep(self) -> AudioSegment:
        """Create an error notification sound (descending)"""
        # Two descending tones
        note1 = Sine(440).to_audio_segment(duration=200) - 10
        note2 = Sine(220).to_audio_segment(duration=250) - 10

        silence = AudioSegment.silent(duration=30)
        error = note1 + silence + note2

        return error.fade_out(100)

    def create_click_sound(self) -> AudioSegment:
        """Create a subtle UI click sound"""
        click = Sine(2000).to_audio_segment(duration=30)
        click = click.fade_in(2).fade_out(20)
        click = click - 18
        return click

    def create_ambient_drone(self, duration_ms: int = 10000, base_freq: int = 110) -> AudioSegment:
        """Create an ambient background drone"""
        # Layer multiple sine waves for richness
        drone1 = Sine(base_freq).to_audio_segment(duration=duration_ms)
        drone2 = Sine(base_freq * 1.5).to_audio_segment(duration=duration_ms) - 6
        drone3 = Sine(base_freq * 2).to_audio_segment(duration=duration_ms) - 10

        # Mix the drones
        drone = drone1.overlay(drone2).overlay(drone3)

        # Reduce volume and add fades
        drone = drone - 25
        drone = drone.fade_in(2000).fade_out(2000)

        return drone

    def create_riser_effect(self, duration_ms: int = 2000) -> AudioSegment:
        """Create a riser/build-up effect"""
        # Create white noise
        noise = WhiteNoise().to_audio_segment(duration=duration_ms)

        # Apply automation-like fade in
        riser = noise.fade_in(duration_ms - 100)

        # Reduce volume
        riser = riser - 18

        return riser

    def create_impact_hit(self) -> AudioSegment:
        """Create an impact/hit sound"""
        # Low frequency sine with quick decay
        impact = Sine(60).to_audio_segment(duration=300)
        impact = impact.fade_out(250)
        impact = impact - 8

        # Add some noise for texture
        noise = WhiteNoise().to_audio_segment(duration=100) - 20

        combined = impact.overlay(noise)
        return combined

    def create_typing_sound(self, num_keystrokes: int = 10) -> AudioSegment:
        """Create keyboard typing sounds"""
        typing = AudioSegment.silent(duration=0)

        for i in range(num_keystrokes):
            # Random frequency variation for each keystroke
            freq = 1500 + (i % 3) * 100
            keystroke = Sine(freq).to_audio_segment(duration=50)
            keystroke = keystroke.fade_in(5).fade_out(30)
            keystroke = keystroke - 20

            # Add keystroke with gap
            typing += keystroke + AudioSegment.silent(duration=80 + (i % 2) * 40)

        return typing

    def create_simple_background_music(self, duration_ms: int = 30000, bpm: int = 120) -> AudioSegment:
        """Create simple background music with chord progression"""
        # Beat duration in milliseconds
        beat_duration = int(60000 / bpm)

        # Chord progression (frequencies for C major, F major, G major, C major)
        chords = [
            [262, 330, 392],  # C major (C, E, G)
            [349, 440, 523],  # F major (F, A, C)
            [392, 494, 587],  # G major (G, B, D)
            [262, 330, 392],  # C major (C, E, G)
        ]

        music = AudioSegment.silent(duration=0)

        # Create progression
        num_bars = duration_ms // (beat_duration * 4)

        for bar in range(num_bars):
            chord_notes = chords[bar % len(chords)]

            # Create chord
            chord = AudioSegment.silent(duration=0)
            for freq in chord_notes:
                note = Sine(freq).to_audio_segment(duration=beat_duration * 4)
                note = note - 18
                if len(chord) == 0:
                    chord = note
                else:
                    chord = chord.overlay(note)

            # Add fade for smoothness
            chord = chord.fade_in(100).fade_out(100)
            music += chord

        # Limit to requested duration
        music = music[:duration_ms]

        # Overall volume adjustment
        music = music - 15

        return music

    def generate_sound_effects_library(self) -> Dict:
        """Generate a library of common sound effects"""
        print("\n" + "=" * 60)
        print("🔊 GENERATING SOUND EFFECTS LIBRARY")
        print("=" * 60)

        sfx_dir = self.output_dir / "sfx"
        sfx_dir.mkdir(parents=True, exist_ok=True)

        effects = {
            "whoosh_transition": self.create_whoosh_transition(),
            "tech_beep": self.create_tech_beep(),
            "success_chime": self.create_success_chime(),
            "error_beep": self.create_error_beep(),
            "ui_click": self.create_click_sound(),
            "riser_buildup": self.create_riser_effect(),
            "impact_hit": self.create_impact_hit(),
            "typing_sequence": self.create_typing_sound(),
        }

        generated_files = []

        for name, audio in effects.items():
            filename = f"sfx_{name}.wav"
            filepath = sfx_dir / filename

            # Export as WAV
            audio.export(
                str(filepath),
                format="wav",
                parameters=["-ar", "48000", "-ac", "2"]
            )

            print(f"   ✅ {filename} ({len(audio)}ms)")
            generated_files.append(str(filepath))

        return {
            "success": True,
            "count": len(effects),
            "files": generated_files,
            "directory": str(sfx_dir)
        }

    def generate_background_music_tracks(self) -> Dict:
        """Generate background music tracks based on source_music.md"""
        print("\n" + "=" * 60)
        print("🎵 GENERATING BACKGROUND MUSIC TRACKS")
        print("=" * 60)

        music_dir = self.output_dir / "music"
        music_dir.mkdir(parents=True, exist_ok=True)

        # Define tracks based on the music specification
        tracks = [
            {
                "name": "track_01_opening_theme",
                "duration": 35000,
                "bpm": 85,
                "description": "The Weight of Legacy - Opening theme"
            },
            {
                "name": "track_02_transformation",
                "duration": 60000,
                "bpm": 124,
                "description": "Breaking Free - Transformation theme"
            },
            {
                "name": "track_03_innovation",
                "duration": 45000,
                "bpm": 105,
                "description": "The Builder's Journey - Innovation theme"
            },
            {
                "name": "track_04_tech_ecosystem",
                "duration": 40000,
                "bpm": 120,
                "description": "The Digital Landscape - Tech theme"
            },
            {
                "name": "track_05_the_feast",
                "duration": 45000,
                "bpm": 128,
                "description": "Options & Possibilities - The Feast"
            },
        ]

        generated_files = []

        for track in tracks:
            print(f"\n   🎼 Creating: {track['description']}")

            # Create ambient drone as base
            drone = self.create_ambient_drone(
                duration_ms=track['duration'],
                base_freq=110 if track['bpm'] < 110 else 130
            )

            # Create simple melodic background
            melody = self.create_simple_background_music(
                duration_ms=track['duration'],
                bpm=track['bpm']
            )

            # Mix drone and melody
            music = drone.overlay(melody)

            # Export
            filename = f"{track['name']}.wav"
            filepath = music_dir / filename

            music.export(
                str(filepath),
                format="wav",
                parameters=["-ar", "48000", "-ac", "2"]
            )

            print(f"   ✅ {filename} ({track['duration']/1000:.1f}s, {track['bpm']} BPM)")
            generated_files.append(str(filepath))

        return {
            "success": True,
            "count": len(tracks),
            "files": generated_files,
            "directory": str(music_dir)
        }

    def generate_ambient_tracks(self) -> Dict:
        """Generate ambient atmosphere tracks"""
        print("\n" + "=" * 60)
        print("🌊 GENERATING AMBIENT ATMOSPHERE TRACKS")
        print("=" * 60)

        ambient_dir = self.output_dir / "ambient"
        ambient_dir.mkdir(parents=True, exist_ok=True)

        ambients = [
            ("ambient_tech_office", 60000, 150),
            ("ambient_futuristic_city", 60000, 100),
            ("ambient_digital_space", 60000, 130),
        ]

        generated_files = []

        for name, duration, freq in ambients:
            ambient = self.create_ambient_drone(duration_ms=duration, base_freq=freq)

            filename = f"{name}.wav"
            filepath = ambient_dir / filename

            ambient.export(
                str(filepath),
                format="wav",
                parameters=["-ar", "48000", "-ac", "2"]
            )

            print(f"   ✅ {filename} ({duration/1000:.1f}s)")
            generated_files.append(str(filepath))

        return {
            "success": True,
            "count": len(ambients),
            "files": generated_files,
            "directory": str(ambient_dir)
        }

    def generate_all(self) -> Dict:
        """Generate all audio assets"""
        print("\n" + "=" * 60)
        print("🎵 AUDIO GENERATOR - Cost-Effective Edition")
        print("=" * 60)
        print("💰 Cost: $0.00 (FREE! Using pydub synthesis)")
        print(f"📥 Input:  {self.input_dir}")
        print(f"📤 Output: {self.output_dir}")
        print("=" * 60)

        results = {
            "timestamp": datetime.now().isoformat(),
            "sfx": self.generate_sound_effects_library(),
            "music": self.generate_background_music_tracks(),
            "ambient": self.generate_ambient_tracks(),
        }

        # Save summary
        summary_path = self.output_dir / f"audio_generation_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_path, 'w') as f:
            json.dump(results, f, indent=2)

        print("\n" + "=" * 60)
        print("✅ AUDIO GENERATION COMPLETE!")
        print("=" * 60)
        print(f"🔊 Sound Effects:  {results['sfx']['count']} files")
        print(f"🎵 Music Tracks:   {results['music']['count']} files")
        print(f"🌊 Ambient Tracks: {results['ambient']['count']} files")
        print(f"📊 Summary: {summary_path}")
        print("=" * 60)

        print("\n✨ BENEFITS FOR DAVINCI RESOLVE:")
        print("=" * 60)
        print("✅ WAV format (uncompressed audio)")
        print("✅ 48kHz sample rate (video production standard)")
        print("✅ Stereo output")
        print("✅ Ready for timeline import")
        print("✅ Royalty-free (synthesized)")
        print("=" * 60)

        return results


def main():
    """Main execution"""
    input_dir = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/input")
    output_dir = Path("/Users/rifaterdemsahin/projects/fal.ai/3_Simulation/2026-02-15/output")

    generator = MusicSoundEffectsGenerator(input_dir=input_dir, output_dir=output_dir)
    generator.generate_all()


if __name__ == "__main__":
    main()

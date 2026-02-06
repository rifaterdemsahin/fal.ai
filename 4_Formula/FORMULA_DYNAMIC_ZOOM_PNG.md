You *can* do that, and in some cases, it’s actually faster—but it comes with a major trade-off.

If you export your SVG as a PNG, you are converting it from a **vector** (mathematically defined lines) to a **raster** (fixed pixels).

### The "PNG vs. SVG" Trade-off

| Feature | PNG (Raster) | SVG (Fusion Import) |
| --- | --- | --- |
| **Ease of Use** | **High.** Just drag, drop, and move. | **Medium.** Requires the Fusion page. |
| **Scaling** | Becomes blurry if you zoom in. | Stays perfectly sharp at any size. |
| **Control** | You can only move the *whole* image. | You can animate individual parts/lines. |
| **Performance** | Very light on your computer. | Can get heavy if the SVG is complex. |

---

### How to animate PNGs "The Easy Way"

If you decide to go the PNG route because you just need the image to slide or fade without complex "drawing" effects, stay on the **Edit Page**:

1. **Drag the PNG** onto your timeline.
2. **Open the Inspector** (top right corner).
3. **Use the "Transform" section:** * Click the **Diamond icon** next to "Position" to set a keyframe.
* Move your playhead, change the position values, and a second keyframe is created automatically.


4. **Add "Dynamic Zoom":** If you want a smooth, automatic zoom-in or out without manual keyframing, just toggle the **Dynamic Zoom** switch in the Inspector.

### When you should stick to SVG

Don't switch to PNG if:

* You want to **change the color** of specific parts of the logo inside Resolve.
* You want that **"writing" effect** where lines grow across the screen.
* You need to **zoom in tight** on a detail (a PNG will look "crunchy" and pixelated).

---

**Would you like me to generate a quick checklist of the best export settings to use in Illustrator or Inkscape so your files play nice with Resolve?**

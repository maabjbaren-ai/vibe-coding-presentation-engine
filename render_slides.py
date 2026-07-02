import json
from pathlib import Path

def generate_presentation():
    # Load the slides content
    try:
        with open("slides_content.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: slides_content.json not found. Please ensure it exists.")
        return

    # Force the correct group code provided by the user
    group_code = "mm-biu26"
    
    # HTML Shell with Reveal.js and absolute architectural RTL support
    html_template = """<!完整 html>
<html lang="he" dir="rtl">
<head>
    <meta charset="utf-8">
    <title>Mulltimedia Architecture via Vibe Coding</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reset.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/theme/black.min.css">
    
    <style>
        /* RTL & Bidi Architectural Fixes to prevent broken rendering */
        .reveal .slides { text-align: right; direction: rtl; }
        .slide-container { width: 100%; direction: rtl; text-align: right; }
        .en-slide { direction: ltr !important; text-align: left !important; }
        .en-slide .slide-container { direction: ltr !important; text-align: left !important; }
        
        /* Custom Flexbox/Table bullet list layout to avoid browser RTL bugs */
        .custom-bullet-list { display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }
        .custom-bullet-item { display: flex; align-items: flex-start; gap: 15px; font-size: 28px; }
        .en-slide .custom-bullet-item { flex-direction: row; }
        .he-slide .custom-bullet-item { flex-direction: row; }
        
        .bullet-dot {
            min-width: 12px; height: 12px; background-color: #3b82f6; 
            border-radius: 50%; margin-top: 12px; flex-shrink: 0;
        }
        
        .bidi-text { unicode-bidi: embed; }
        .ltr-wrap { direction: ltr; display: inline-block; }
        
        /* Table Layout Fixes */
        .reveal table { margin: 20px auto; width: 90%; font-size: 24px; border-collapse: collapse; }
        .reveal th { background-color: #1e3a8a; color: white; padding: 10px; text-align: center; }
        .reveal td { border: 1px solid #333; padding: 8px; text-align: center; }
        
        /* Code Block Styling */
        .code-box { background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 22px; text-align: left; direction: ltr; white-space: pre-wrap; border-left: 5px solid #3b82f6; }
        
        /* Footer branding requirement */
        .slide-footer { position: absolute; bottom: -40px; width: 100%; display: flex; justify-content: space-between; font-size: 16px; color: #666; border-top: 1px solid #333; padding-top: 5px; }
    </style>
</head>
<body>
    <!-- Background Audio Controller -->
    <audio id="bg-audio" loop autoplay>
        <source src="https://actions.google.com/sounds/v1/ambiences/tech_amenity_space.ogg" type="audio/ogg">
    </audio>

    <div class="reveal">
        <div class="slides">
            {{SLIDES_PLACEHOLDER}}
        </div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.js"></script>
    <script>
        Reveal.initialize({
            controls: true,
            progress: true,
            center: false, /* Required to prevent overlap with RTL custom layouts */
            hash: true,
            transition: 'slide'
        });
        
        // Ensure audio plays upon user interaction
        document.addEventListener('click', function() {
            var audio = document.getElementById('bg-audio');
            if (audio) { audio.play(); }
        });
    </script>
</body>
</html>"""

    slides_html = []
    
    # Process each chunk inside the JSON schema
    for slide in data["slides"]:
        lang_class = "he-slide" if slide["language"] == "he" else "en-slide"
        slide_direction = "rtl" if slide["language"] == "he" else "ltr"
        
        slide_str = f'<section data-transition="slide" class="{lang_class}">\n'
        slide_str += f'  <div class="slide-container" style="direction: {slide_direction};">\n'
        
        if slide["type"] == "title":
            slide_str += f'    <h2 style="color: #3b82f6;">{slide["title"]}</h2>\n'
            slide_str += f'    <h3 style="color: #888;">{slide["subtitle"]}</h3>\n'
            
        elif slide["type"] == "bullets":
            slide_str += f'    <h3 style="color: #3b82f6; text-align: start;">{slide["title"]}</h3>\n'
            slide_str += f'    <h4 style="color: #aaa; text-align: start; font-size: 24px; margin-bottom:10px;">{slide["subtitle"]}</h4>\n'
            slide_str += '    <div class="custom-bullet-list">\n'
            for bullet in slide["bullets"]:
                slide_str += '      <div class="custom-bullet-item">\n'
                slide_str += '        <div class="bullet-dot"></div>\n'
                slide_str += f'        <div class="bidi-text">{bullet}</div>\n'
                slide_str += '      </div>\n'
            slide_str += '    </div>\n'
            
        elif slide["type"] == "table":
            slide_str += f'    <h3 style="color: #3b82f6;">{slide["title"]}</h3>\n'
            slide_str += '    <table>\n'
            slide_str += '      <thead><tr>\n'
            for header in slide["headers"]:
                slide_str += f'        <th>{header}</th>\n'
            slide_str += '      </tr></thead>\n'
            slide_str += '      <tbody>\n'
            for row in slide["rows"]:
                slide_str += '        <tr>\n'
                for cell in row:
                    slide_str += f'          <td>{cell}</td>\n'
                slide_str += '        </tr>\n'
            slide_str += '      </tbody>\n'
            slide_str += '    </table>\n'
            
        elif slide["type"] == "code":
            slide_str += f'    <h3 style="color: #3b82f6; text-align: start;">{slide["title"]}</h3>\n'
            slide_str += f'    <h4 style="color: #aaa; text-align: start; font-size: 24px;">{slide["subtitle"]}</h4>\n'
            slide_str += f'    <div class="code-box">{slide["code"]}</div>\n'
            
        # Standard corporate footer injected dynamically across all nodes
        slide_str += '    <div class="slide-footer">\n'
        slide_str += f'      <span>קבוצה: {group_code}</span>\n'
        slide_str += f'      <span style="font-style: italic;">מקור: {slide["source"]}</span>\n'
        slide_str += '    </div>\n'
        
        slide_str += '  </div>\n'
        slide_str += '</section>\n'
        slides_html.append(slide_str)

    # Inherent structural injection step
    final_output = html_template.replace("{{SLIDES_PLACEHOLDER}}", "\n".join(slides_html))
    
    # Save the output file matching Cinderella specifications
    output_filename = f"{group_code}-ex06.html"
    Path(output_filename).write_text(final_output, encoding="utf-8")
    print(f"Success! Generated {output_filename} containing exactly 20 architectural slides.")

if __name__ == "__main__":
    generate_presentation()

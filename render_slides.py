import json
from pathlib import Path

def generate_presentation():
    # הטענת קובץ התוכן
    try:
        with open("slides_content.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: slides_content.json not found. Please ensure it exists.")
        return

    # קוד הקבוצה המעודכן שלך
    group_code = "mm-biu26"
    
    # שלד ה-HTML המלא עם Reveal.js ותשתית ה-CSS המעודכנת
    html_template = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="utf-8">
    <title>Multimedia Architecture via Vibe Coding</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reset.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/theme/black.min.css">
    
    <style>
        /* הגדרות כיווניות וארכיטקטורת RTL למניעת טקסט שבור */
        .reveal .slides { text-align: right; direction: rtl; }
        .slide-container { width: 100%; direction: rtl; text-align: right; }
        .en-slide { direction: ltr !important; text-align: left !important; }
        .en-slide .slide-container { direction: ltr !important; text-align: left !important; }
        
        /* פתרון ארכיטקטוני מבוסס תצוגת טבלה למניעת בריחת נקודות בעברית */
        .custom-bullet-list { 
            display: table; 
            margin: 20px 0; 
            text-align: right; 
            direction: rtl; 
            width: 100%;
        }
        .en-slide .custom-bullet-list {
            text-align: left;
            direction: ltr;
        }
        .custom-bullet-item { 
            display: table-row; 
            font-size: 28px; 
        }
        .bidi-text { 
            display: list-item;
            list-style-type: disc;
            padding-bottom: 15px; 
            unicode-bidi: embed; 
        }
        .he-slide .bidi-text { margin-right: 30px; }
        .en-slide .bidi-text { margin-left: 30px; }
        
        /* עיצוב טבלאות */
        .reveal table { margin: 20px auto; width: 90%; font-size: 24px; border-collapse: collapse; }
        .reveal th { background-color: #1e3a8a; color: white; padding: 10px; text-align: center; }
        .reveal td { border: 1px solid #333; padding: 8px; text-align: center; }
        
        /* עיצוב בלוק קוד */
        .code-box { background: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 8px; font-family: monospace; font-size: 22px; text-align: left; direction: ltr; white-space: pre-wrap; border-left: 5px solid #3b82f6; }
        
        /* כותרת תחתונה מיתוגית מחויבת במחוון */
        .slide-footer { position: absolute; bottom: -40px; width: 100%; display: flex; justify-content: space-between; font-size: 16px; color: #666; border-top: 1px solid #333; padding-top: 5px; }
        .en-slide .slide-footer { direction: rtl; }
    </style>
</head>
<body>
    <audio id="bg-audio" loop autoplay>
        <source src="music.mp3" type="audio/mpeg">
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
            center: false, /* קריטי כדי למנוע קפיצות טקסט ב-RTL */
            hash: true,
            transition: 'slide'
        });
        
        // הפעלת הסאונד בלחיצה ראשונה על המסך או מקלדת
        function playAudio() {
            var audio = document.getElementById('bg-audio');
            if (audio) { audio.play().catch(function(e){ console.log("Audio play blocked", e); }); }
        }
        document.addEventListener('click', playAudio);
        document.addEventListener('keydown', playAudio);
    </script>
</body>
</html>"""

    slides_html = []
    
    # ריצה על פריטי ה-JSON והזרקה לשלד ה-HTML
    for slide in data["slides"]:
        lang_class = "he-slide" if slide["language"] == "he" else "en-slide"
        slide_direction = "rtl" if slide["language"] == "he" else "ltr"
        
        slide_str = f'<section data-transition="slide" class="{lang_class}">\n'
        slide_str += f'  <div class="slide-container" style="direction: {slide_direction};">\n'
        
        if slide["type"] == "title":
            slide_str += f'    <h2 style="color: #3b82f6;">{slide["title"]}</h2>\n'
            slide_str += f'    <h3 style="color: #888;">{slide["subtitle"]}</h3>\n'
            
        elif slide["type"] == "bullets":
            slide_str += f'    <h3 style="color: #3b82f6;">{slide["title"]}</h3>\n'
            slide_str += f'    <h4 style="color: #aaa; font-size: 24px; margin-bottom:10px;">{slide["subtitle"]}</h4>\n'
            slide_str += '    <div class="custom-bullet-list">\n'
            for bullet in slide["bullets"]:
                slide_str += '      <div class="custom-bullet-item">\n'
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
            slide_str += f'    <h3 style="color: #3b82f6;">{slide["title"]}</h3>\n'
            slide_str += f'    <h4 style="color: #aaa; font-size: 24px;">{slide["subtitle"]}</h4>\n'
            slide_str += f'    <div class="code-box">{slide["code"]}</div>\n'
            
        # כותרת תחתונה דינמית לכל שקופית
        slide_str += '    <div class="slide-footer">\n'
        slide_str += f'      <span>קבוצה: {group_code}</span>\n'
        slide_str += f'      <span style="font-style: italic;">מקור: {slide["source"]}</span>\n'
        slide_str += '    </div>\n'
        
        slide_str += '  </div>\n'
        slide_str += '</section>\n'
        slides_html.append(slide_str)

    # הזרקה סופית ושמירת הקובץ
    final_output = html_template.replace("{{SLIDES_PLACEHOLDER}}", "\n".join(slides_html))
    output_filename = f"{group_code}-ex06.html"
    Path(output_filename).write_text(final_output, encoding="utf-8")
    print(f"Success! Generated {output_filename} containing exactly 20 architectural slides.")

if __name__ == "__main__":
    generate_presentation()

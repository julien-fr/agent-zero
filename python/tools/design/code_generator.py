import os
import json
from typing import Dict, Any

from python.helpers.tool import Tool, Response
from python.helpers import files

class CodeGenerator(Tool):
    """
    Generate React/Tailwind code from a design system.
    """
    
    async def execute(self, design_system: Dict[str, Any] = None, output_dir: str = "", **kwargs):
        """
        Generate code based on design system.
        
        Args:
            design_system: Design system dictionary (from DesignAnalyzer)
            output_dir: Directory to output generated files (default: tmp/code_gen)
            
        Returns:
            Response with paths to generated files.
        """
        self.agent.context.log.set_progress("CodeGenerator: Generating code from design system")
        
        if not design_system:
            return Response(message="No design system provided", break_loop=False)
        
        # Set output directory
        if not output_dir:
            output_dir = files.get_abs_path("tmp/code_gen")
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract palette
        palette = design_system.get("palette", {})
        typography = design_system.get("typography", {})
        layout = design_system.get("layout", {})
        
        # 1. Generate tailwind.config.js
        tailwind_config = self._generate_tailwind_config(palette, typography)
        tailwind_path = os.path.join(output_dir, "tailwind.config.js")
        with open(tailwind_path, "w") as f:
            f.write(tailwind_config)
        
        # 2. Generate React component
        component = self._generate_react_component(design_system)
        component_path = os.path.join(output_dir, "HeroSection.jsx")
        with open(component_path, "w") as f:
            f.write(component)
        
        # 3. Generate sample HTML page
        html = self._generate_html_page(design_system)
        html_path = os.path.join(output_dir, "index.html")
        with open(html_path, "w") as f:
            f.write(html)
        
        # 4. Generate README
        readme = self._generate_readme(design_system)
        readme_path = os.path.join(output_dir, "README.md")
        with open(readme_path, "w") as f:
            f.write(readme)
        
        result = {
            "output_dir": output_dir,
            "files": [
                tailwind_path,
                component_path,
                html_path,
                readme_path
            ],
            "design_system": design_system
        }
        
        return Response(
            message=f"Code generated successfully in {output_dir}",
            additional=result,
            break_loop=False
        )
    
    def _generate_tailwind_config(self, palette: Dict, typography: Dict) -> str:
        """Generate Tailwind config with custom colors and fonts."""
        colors = {}
        for key, value in palette.items():
            if isinstance(value, str) and value.startswith("#"):
                colors[key] = value
        
        font_family_heading = typography.get("font_family_heading", "Inter")
        font_family_body = typography.get("font_family_body", "Inter")
        
        config = f"""module.exports = {{
  content: ["./index.html", "./src/**/*.{{js,ts,jsx,tsx}}"],
  theme: {{
    extend: {{
      colors: {json.dumps(colors, indent=6)},
      fontFamily: {{
        heading: ['{font_family_heading}', 'sans-serif'],
        body: ['{font_family_body}', 'sans-serif'],
      }},
      borderRadius: {{
        'base': '{typography.get("border_radius_base", "8px")}',
      }},
      spacing: {{
        'base': '{layout.get("spacing_base", "4px")}',
      }},
    }},
  }},
  plugins: [],
}}
"""
        return config
    
    def _generate_react_component(self, design_system: Dict) -> str:
        """Generate a sample React component using Tailwind."""
        palette = design_system.get("palette", {})
        primary = palette.get("primary", "#3B82F6")
        theme_name = design_system.get("theme_name", "Modern Theme")
        
        return f"""import React from 'react';

export default function HeroSection() {{
  return (
    <div className="min-h-screen bg-background text-text_primary p-8">
      <header className="container mx-auto max-w-6xl">
        <nav className="flex justify-between items-center py-4">
          <div className="text-2xl font-heading font-bold">{theme_name}</div>
          <div className="space-x-6">
            <a href="#" className="hover:text-primary transition-colors">Home</a>
            <a href="#" className="hover:text-primary transition-colors">About</a>
            <a href="#" className="hover:text-primary transition-colors">Contact</a>
          </div>
        </nav>
      </header>
      
      <main className="container mx-auto max-w-6xl mt-16">
        <section className="bg-surface rounded-base p-8 shadow-xl">
          <h1 className="text-5xl font-heading font-bold mb-4">Welcome to {theme_name}</h1>
          <p className="text-xl text-text_secondary mb-8">
            This component was generated automatically from a design system extracted by AI.
          </p>
          <div className="flex space-x-4">
            <button 
              className="bg-primary text-white px-6 py-3 rounded-base hover:opacity-90 transition-opacity"
              style={{{{ backgroundColor: '{primary}' }}}}
            >
              Primary Action
            </button>
            <button 
              className="bg-secondary text-text_primary px-6 py-3 rounded-base border border-gray-300 hover:bg-gray-100 transition-colors"
            >
              Secondary Action
            </button>
          </div>
        </section>
        
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8">
          {{[1, 2, 3].map(i => (
            <div key={{i}} className="bg-surface rounded-base p-6 shadow-lg">
              <h3 className="text-2xl font-heading font-bold mb-2">Feature {{i}}</h3>
              <p className="text-text_secondary">
                This card demonstrates the spacing and card styles defined in the design system.
              </p>
            </div>
          ))}}
        </div>
      </main>
      
      <footer className="container mx-auto max-w-6xl mt-16 py-8 border-t border-gray-200">
        <p className="text-center text-text_secondary">
          Generated by AgentZero Design Autonomously • {theme_name}
        </p>
      </footer>
    </div>
  );
}}
"""
    
    def _generate_html_page(self, design_system: Dict) -> str:
        """Generate a standalone HTML page with inline Tailwind."""
        theme_name = design_system.get("theme_name", "AI Generated Design")
        primary = design_system.get("palette", {}).get("primary", "#3B82F6")
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{theme_name}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            primary: '{primary}',
            background: '{design_system.get("palette", {}).get("background", "#0F172A")}',
            surface: '{design_system.get("palette", {}).get("surface", "#1E293B")}',
            text_primary: '{design_system.get("palette", {}).get("text_primary", "#F1F5F9")}',
          }}
        }}
      }}
    }}
  </script>
  <style>
    body {{
      font-family: 'Inter', sans-serif;
    }}
  </style>
</head>
<body class="bg-background text-text_primary min-h-screen p-8">
  <div class="container mx-auto max-w-6xl">
    <h1 class="text-4xl font-bold mb-6">{theme_name}</h1>
    <p class="text-xl mb-8">This HTML page was generated from an AI‑extracted design system.</p>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="bg-surface p-6 rounded-lg shadow-xl">
        <h2 class="text-2xl font-bold mb-4">Color Palette</h2>
        <div class="space-y-4">
          {self._generate_color_swatches(design_system.get("palette", {}))}
        </div>
      </div>
      
      <div class="bg-surface p-6 rounded-lg shadow-xl">
        <h2 class="text-2xl font-bold mb-4">Generated Components</h2>
        <button class="bg-primary text-white px-6 py-3 rounded-lg hover:opacity-90 transition-opacity">
          Primary Button
        </button>
        <button class="ml-4 border border-gray-300 text-text_primary px-6 py-3 rounded-lg hover:bg-gray-800 transition-colors">
          Secondary Button
        </button>
      </div>
    </div>
    
    <div class="mt-12">
      <h2 class="text-2xl font-bold mb-4">Design System JSON</h2>
      <pre class="bg-gray-900 text-gray-200 p-4 rounded-lg overflow-auto">
{json.dumps(design_system, indent=2)}
      </pre>
    </div>
  </div>
</body>
</html>
"""
    
    def _generate_color_swatches(self, palette: Dict) -> str:
        """Generate HTML divs for color swatches."""
        swatches = []
        for name, color in palette.items():
            if isinstance(color, str) and color.startswith("#"):
                swatches.append(f'''
          <div class="flex items-center">
            <div class="w-12 h-12 rounded-lg mr-4 border border-gray-700" style="background-color: {color}"></div>
            <div>
              <div class="font-medium">{name}</div>
              <div class="text-gray-400">{color}</div>
            </div>
          </div>''')
        return '\n'.join(swatches)
    
    def _generate_readme(self, design_system: Dict) -> str:
        """Generate README file."""
        theme_name = design_system.get("theme_name", "AI Generated Design")
        return f"""# {theme_name}

This project was generated automatically by AgentZero's autonomous UI design agent.

## Files
- `tailwind.config.js` – Tailwind configuration with custom design tokens
- `HeroSection.jsx` – Sample React component using the design system
- `index.html` – Standalone HTML demo page
- `README.md` – This file

## Design System

### Palette
{self._format_palette(design_system.get('palette', {}))}

### Typography
- Heading font: {design_system.get('typography', {}).get('font_family_heading', 'Inter')}
- Body font: {design_system.get('typography', {}).get('font_family_body', 'Inter')}

### Layout
- Base spacing: {design_system.get('layout', {}).get('spacing_base', '4px')}
- Border radius: {design_system.get('layout', {}).get('border_radius_base', '8px')}

## Usage
1. Install dependencies: `npm install tailwindcss`
2. Import the component in your React app.
3. Enjoy your AI‑generated design!

---
*Generated on {datetime.now().strftime('%Y‑%m‑d %H:%M')} by AgentZero.*
"""
    
    def _format_palette(self, palette: Dict) -> str:
        """Format palette for README."""
        lines = []
        for name, color in palette.items():
            if isinstance(color, str) and color.startswith("#"):
                lines.append(f"- `{name}`: `{color}`")
        return '\n'.join(lines)


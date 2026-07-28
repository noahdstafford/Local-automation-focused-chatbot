import re
from chat import ask_ollama

def run_website_generator():
    description = input("Describe the website you want built: ")

    # Prompt which has been structured so that ollama is able to give a strong website page instead of a basic document
    prompt = f"""Create a complete, single HTML file for a professional, modern, visually polished website based on the description below.

Design requirements:
- Use a modern, cohesive color palette (not just default blue/white) — consider gradients or a distinct accent color
- Use modern typography — import a Google Font via a <link> tag
- Include thoughtful spacing, padding, and visual hierarchy
- Add hover effects, subtle shadows, and smooth transitions on interactive elements and section cards
- Make it responsive for both desktop and mobile widths
- Include a proper multi-section layout (header/nav, hero section, content sections, footer)
- Use flexbox or grid for layout
- The footer must sit naturally at the bottom of the page in normal document flow — never floating, absolutely positioned, or detached from the page
- Do not use list-style bullets, arrows, or default marker icons in navigation menus — use plain text links with proper spacing
- Do not reference local image files or made-up image paths, since they will not exist and will break the page
- If images are needed, use https://picsum.photos/[width]/[height] as placeholder image URLs (e.g. https://picsum.photos/400/300), which always return a real image
- Give every image a fixed width and height in CSS so the layout doesn't shift or break if an image fails to load

Include all CSS and JavaScript inline within the HTML file — do not reference external files (except Google Fonts links).
Respond ONLY with the raw HTML code, no explanations, no markdown code fences.

DESCRIPTION:
{description}"""

    print("\n Building your website please wait")

    # Sends the user prompt to ollama modle 
    answer = ask_ollama(prompt)
    # Removes unecessary HTML markdown and backticks to ensure response is clear
    answer = answer.replace("'''html", "").replace("'''", "").strip()

    # Generates HTML website with the ocde so the site can be ran in the browser
    filename = "generated_site.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(answer)

    print(f"\nSaved to {filename} — open it in your browser to view it.")

    # Starts a loop that acts as corrective loop for the website 
    while True:
        change_request = input("\nWant any changes made? Describe them, or press Enter to finish: ")
        if change_request.strip() == "":
            break

        fix_prompt = f"""Here is an existing HTML website. Make the following changes, and return ONLY the full updated HTML file.

Do not include any explanation, commentary, or description of what you changed. Do not say things like "Sure, here's the updated HTML" — respond with nothing except the raw HTML code itself, starting directly with <!DOCTYPE html>.

CHANGES REQUESTED:
{change_request}

EXISTING HTML:
{answer}"""

        print("\nUpdating your website, please wait...\n")

        answer = ask_ollama(fix_prompt)
        answer = answer.replace("```html", "").replace("```", "").strip()
        # Extra safety to cut off extra text before the HTML update
        if "<!DOCTYPE" in answer:
            answer = answer[answer.index("<!DOCTYPE"):]

        with open(filename, "w", encoding="utf-8") as f:
            f.write(answer)

        print(f"\nUpdated {filename} — refresh your browser to see the changes.")

if __name__ == "__main__":
    run_website_generator()
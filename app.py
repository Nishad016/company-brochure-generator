import os
import gradio as gr
from openai import OpenAI
from scraper import fetch_website_links, fetch_website_contents

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_brochure(company_name, website_url):
    links = fetch_website_links(website_url)

    # Select useful company-related pages
    keywords = ["about", "company", "product", "service", "career", "contact"]
    relevant_links = [
        link for link in links
        if any(keyword in link.lower() for keyword in keywords)
    ][:8]

    # Always include the main website
    pages = [website_url] + relevant_links

    contents = []
    for url in pages:
        try:
            contents.append(fetch_website_contents(url))
        except Exception:
            pass

    website_content = "\n\n--- PAGE ---\n\n".join(contents)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
Create a professional company brochure in Markdown.

Include:
- Company overview
- Products/services
- Customers
- Company culture
- Careers
- Key takeaways

Use only the information provided.
"""
            },
            {
                "role": "user",
                "content": f"""
Company: {company_name}

Website content:
{website_content}
"""
            }
        ]
    )

    return response.choices[0].message.content


with gr.Blocks() as demo:
    gr.Markdown("# AI Company Brochure Generator")
    gr.Markdown("Enter a company and its website to generate a brochure.")

    company = gr.Textbox(label="Company Name")
    website = gr.Textbox(label="Website URL")

    button = gr.Button("Generate Brochure")
    output = gr.Markdown()

    button.click(
        create_brochure,
        inputs=[company, website],
        outputs=output
    )

demo.launch()

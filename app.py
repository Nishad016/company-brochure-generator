import os
import gradio as gr
from openai import OpenAI
from scraper import fetch_website_links, fetch_website_contents


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_brochure(company_name, website_url):
    links = fetch_website_links(website_url)

    prompt = f"""
You are an assistant that creates professional company brochures.

Company: {company_name}
Website: {website_url}

Here are the relevant website pages:
{links}

Create a concise but informative company brochure in Markdown.
Include:
- Company overview
- Products/services
- Customers
- Company culture
- Careers
- Key takeaways

Only use information found from the provided website content.
"""

    contents = fetch_website_contents(links)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": contents},
        ],
    )

    return response.choices[0].message.content


with gr.Blocks(title="AI Company Brochure Generator") as demo:
    gr.Markdown("# AI Company Brochure Generator")
    gr.Markdown("Enter a company and its website to generate an AI-powered brochure.")

    company = gr.Textbox(label="Company Name", placeholder="e.g. OpenAI")
    website = gr.Textbox(label="Website URL", placeholder="https://openai.com")

    generate = gr.Button("Generate Brochure", variant="primary")
    output = gr.Markdown()

    generate.click(
        fn=create_brochure,
        inputs=[company, website],
        outputs=output
    )


demo.launch()

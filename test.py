import markdown
import pdfkit


# 将 Markdown 转换为 PDF
def md_to_pdf(md_file, pdf_file):
    # 读取 Markdown 内容
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Markdown 转 HTML
    html_content = markdown.markdown(md_content, output_format='html5')

    # 如果需要，可以加上简单的 HTML 头部样式
    html_template = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                padding: 20px;
            }}
            pre {{
                background-color: #f5f5f5;
                padding: 10px;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # 生成 PDF（需要安装 wkhtmltopdf）
    pdfkit.from_string(html_template, pdf_file)


if __name__ == "__main__":
    md_to_pdf("example.md", "output.pdf")
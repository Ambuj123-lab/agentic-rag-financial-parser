import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import List
from datetime import datetime

def send_daily_insight_email(to_emails: List[str], subject: str, insight_title: str, insight_explanation: str, real_life_scenario: str, sources: List[str]):
    """
    Sends the generated AI Insight email to a list of recipients.
    Premium HTML template — designed by Ambuj Kumar Tripathi.
    """
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_APP_PASSWORD")

    if not sender_email or not sender_password:
        print("Email credentials missing in .env")
        return False

    # Dynamic date
    today_date = datetime.now().strftime("%B %d, %Y")
    
    # Extract category from title (e.g., "Did you know? - Consumer Rights" → "Consumer Rights")
    category = "Legal & Financial"
    if " - " in insight_title:
        category = insight_title.split(" - ", 1)[1][:40]

    # Source links HTML
    source_links_html = ""
    for i, src in enumerate(sources, 1):
        # Truncate long URLs for display
        display_url = src if len(src) < 60 else src[:57] + "..."
        source_links_html += f'''
            <tr>
              <td style="padding: 8px 0; border-bottom: 1px solid #f3f4f6;">
                <table cellpadding="0" cellspacing="0" border="0" width="100%"><tr>
                  <td width="28" valign="top" style="padding-right: 10px;">
                    <div style="width: 24px; height: 24px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 6px; text-align: center; line-height: 24px; color: #fff; font-size: 12px; font-weight: bold;">{i}</div>
                  </td>
                  <td>
                    <a href="{src}" style="color: #6366f1; text-decoration: none; font-size: 13px; word-break: break-all;">{display_url}</a>
                  </td>
                </tr></table>
              </td>
            </tr>'''

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; background-color: #0f172a; font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
      
      <!-- Outer Container -->
      <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #0f172a; padding: 30px 0;">
        <tr>
          <td align="center">
            <table cellpadding="0" cellspacing="0" border="0" width="600" style="max-width: 600px; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 25px 50px rgba(0,0,0,0.3);">
              
              <!-- ═══════ HEADER ═══════ -->
              <tr>
                <td style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #312e81 100%); padding: 35px 30px; text-align: center;">
                  <!-- AI Badge -->
                  <div style="display: inline-block; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 20px; padding: 4px 14px; margin-bottom: 15px;">
                    <span style="color: #a5b4fc; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 600;">⚡ AI-Powered Newsletter</span>
                  </div>
                  <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700; letter-spacing: -0.5px;">Daily Legal &amp; Financial Insights</h1>
                  <p style="color: #94a3b8; margin: 8px 0 0 0; font-size: 14px;">Curated autonomously by Ambuj's Agentic RAG AI</p>
                  <div style="margin-top: 15px; height: 3px; background: linear-gradient(90deg, transparent, #6366f1, #a855f7, #6366f1, transparent); border-radius: 2px;"></div>
                  <p style="color: #64748b; margin: 12px 0 0 0; font-size: 12px;">📅 {today_date}</p>
                </td>
              </tr>

              <!-- ═══════ CATEGORY BADGE ═══════ -->
              <tr>
                <td style="padding: 25px 30px 0 30px;">
                  <div style="display: inline-block; background: linear-gradient(135deg, #eef2ff, #e0e7ff); border: 1px solid #c7d2fe; border-radius: 8px; padding: 6px 16px;">
                    <span style="color: #4338ca; font-size: 12px; font-weight: 700; letter-spacing: 0.5px;">📂 {category}</span>
                  </div>
                </td>
              </tr>

              <!-- ═══════ TITLE ═══════ -->
              <tr>
                <td style="padding: 15px 30px 5px 30px;">
                  <h2 style="color: #0f172a; margin: 0; font-size: 22px; font-weight: 700; line-height: 1.3;">💡 {insight_title}</h2>
                </td>
              </tr>

              <!-- ═══════ DIVIDER ═══════ -->
              <tr>
                <td style="padding: 10px 30px;">
                  <div style="height: 2px; background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899); border-radius: 1px;"></div>
                </td>
              </tr>

              <!-- ═══════ THE LAW / FACT ═══════ -->
              <tr>
                <td style="padding: 15px 30px;">
                  <table cellpadding="0" cellspacing="0" border="0" width="100%">
                    <tr>
                      <td style="background: linear-gradient(135deg, #f8fafc, #f1f5f9); border-left: 4px solid #6366f1; border-radius: 0 12px 12px 0; padding: 20px 22px;">
                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                          <tr>
                            <td>
                              <div style="display: inline-block; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 8px; padding: 4px 12px; margin-bottom: 12px;">
                                <span style="color: #ffffff; font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">📜 The Law / Fact</span>
                              </div>
                              <p style="color: #334155; margin: 0; font-size: 15px; line-height: 1.7;">{insight_explanation}</p>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- ═══════ REAL-LIFE SCENARIO ═══════ -->
              <tr>
                <td style="padding: 10px 30px;">
                  <table cellpadding="0" cellspacing="0" border="0" width="100%">
                    <tr>
                      <td style="background-color: #fffbeb; border: 1px solid #fde68a; border-radius: 12px; padding: 20px 22px;">
                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                          <tr>
                            <td>
                              <div style="display: inline-block; background: linear-gradient(135deg, #f59e0b, #d97706); border-radius: 8px; padding: 4px 12px; margin-bottom: 12px;">
                                <span style="color: #ffffff; font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">🛡️ Real-Life Scenario</span>
                              </div>
                              <p style="color: #78350f; margin: 0; font-size: 14px; line-height: 1.7;">{real_life_scenario}</p>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- ═══════ SOURCES ═══════ -->
              <tr>
                <td style="padding: 20px 30px 10px 30px;">
                  <table cellpadding="0" cellspacing="0" border="0" width="100%">
                    <tr>
                      <td style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px 20px;">
                        <p style="color: #64748b; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin: 0 0 10px 0;">🔍 Sources Verified via Tavily AI</p>
                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                          {source_links_html}
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- ═══════ CTA BUTTON ═══════ -->
              <tr>
                <td style="padding: 20px 30px; text-align: center;">
                  <a href="https://agentic-rag-financial-parser.onrender.com" style="display: inline-block; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #ffffff; text-decoration: none; padding: 12px 32px; border-radius: 10px; font-size: 14px; font-weight: 700; letter-spacing: 0.5px; box-shadow: 0 4px 15px rgba(99,102,241,0.4);">🤖 Try the AI Chatbot →</a>
                </td>
              </tr>

              <!-- ═══════ DISCLAIMER ═══════ -->
              <tr>
                <td style="padding: 0 30px 20px 30px;">
                  <div style="background-color: #fef2f2; border: 1px solid #fecaca; border-radius: 10px; padding: 14px 16px;">
                    <p style="color: #991b1b; font-size: 10px; margin: 0; line-height: 1.6; font-style: italic;">
                      <strong>⚠️ Disclaimer:</strong> This email is automatically generated by an autonomous AI agent for educational and informational purposes only. It does not constitute formal legal, financial, or professional advice. While the AI verifies facts via web search, please consult a certified professional or refer to official government sources before making any decisions.
                    </p>
                  </div>
                </td>
              </tr>

              <!-- ═══════ FOOTER ═══════ -->
              <tr>
                <td style="background: linear-gradient(135deg, #0f172a, #1e293b); padding: 25px 30px; text-align: center;">
                  <!-- Tech Stack Badge -->
                  <div style="display: inline-block; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 4px 14px; margin-bottom: 12px;">
                    <span style="color: #64748b; font-size: 10px; letter-spacing: 1px;">LANGGRAPH • TAVILY • GEMINI AI • PINECONE</span>
                  </div>
                  <p style="color: #94a3b8; font-size: 12px; margin: 0; line-height: 1.6;">
                    🤖 Generated autonomously by <strong style="color: #a5b4fc;">Agentic ReAct RAG Platform</strong>
                  </p>
                  <p style="color: #64748b; font-size: 11px; margin: 6px 0 0 0;">
                    Developed by <a href="https://ambuj-ai-portfolio.vercel.app" style="color: #818cf8; text-decoration: none; font-weight: 600;">Ambuj Kumar Tripathi</a> — AI Engineer &amp; RAG Systems Architect
                  </p>
                  <p style="color: #475569; font-size: 10px; margin: 8px 0 0 0;">📍 Gorakhpur, India</p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    try:
        # Create SMTP session with 30s timeout (prevents infinite hang on Render)
        print("  📧 SMTP: Connecting to smtp.gmail.com:587...")
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
        
        print("  📧 SMTP: Starting TLS...")
        server.starttls()
        
        print(f"  📧 SMTP: Logging in as {sender_email}...")
        server.login(sender_email, sender_password)
        print("  📧 SMTP: Login successful!")

        # Loop and send
        for recipient in to_emails:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"💡 {subject}"
            msg['From'] = f"Ambuj's AI Insights <{sender_email}>"
            msg['To'] = recipient

            # Attach HTML content
            part = MIMEText(html_content, 'html')
            msg.attach(part)

            server.send_message(msg)
            print(f"  ✅ SMTP: Sent to {recipient}")

        server.quit()
        print(f"Successfully sent AI Insight to {len(to_emails)} recipients.")
        return True
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP AUTH FAILED: {e}. Check SENDER_EMAIL and SENDER_APP_PASSWORD.")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"❌ SMTP CONNECTION FAILED: {e}. Gmail port 587 might be blocked by Render.")
        return False
    except TimeoutError as e:
        print(f"❌ SMTP TIMEOUT: {e}. Connection to Gmail hung for 30+ seconds.")
        return False
    except Exception as e:
        print(f"❌ SMTP UNKNOWN ERROR: {type(e).__name__}: {e}")
        return False

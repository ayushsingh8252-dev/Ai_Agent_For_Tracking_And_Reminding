from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp import types
import smtplib, imaplib, email
from auth.credentials import CREDENTIALS


server = Server("email-sever")

def get_gmail_connection():
    """Returns an authenticated Gmail SMTP connection."""
    creds = CREDENTIALS["email"]
    # For real OAuth, use google-auth library to get access token
    # Here we show the simple App Password approach for clarity
    # Simple Mail Transfer Protocol
    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login(creds["client_id"], creds["client_secret"])
    return smtp

#retriveing toold trom server
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """Tell the agent what tools this server provides."""
    return[
        types.Tool(
            name="send_email",
            description="Send an email to someone",
            inputSchema={
                "types" : "object",
                "properties" : {
                    "to": {"type": "string", "description": "Recipient email"},
                    "subject" : {"type": "string", "description": "Email subject"},
                    "body":  {"type": "string", "description": "Email body"},
                },
                "required" : ["to", "subject", "body"],
            },
        ),
        types.Tool(
            name = "list_inbox",
            description ="List recent emails from inbox",
            inputSchema = {
                "types" : "object",
                "properties" : {
                    "limit": {"type": "integer", "description": "How many emails", "default": 5}
                },
            },
        ),
    ]
@server.call_tool()
#arguments = {to, subject, body}
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls from the agent."""
    if name == "send_email":
        smtp = get_gmail_connection()
        msg = f"Subject: {arguments['subject']}\n\n{arguments['body']}"
        smtp.sendmail("ayushrajput8252@gmail.com", arguments['body'])
        smtp.quit()
        return [types.TextContent(type="text", text=f"Email sent to {arguments['to']}")]
    elif name == "list_inbox":
        # Simplified — returns mock data for clarity
        return [types.TextContent(type="text", text="Inbox: 3 new emails from Alice, Bob, Carol")]
    raise ValueError(f"Unknown tool: {name}")
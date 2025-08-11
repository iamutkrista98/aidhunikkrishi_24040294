import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import streamlit as st
import datetime

# Determine the root directory of the project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def send_feedback_session_invitation(session_date, session_time, email_addresses):
    # Set up email details
    sender_email = "aidhunikkheti@gmail.com"
    password = "lllx eghw hfpt lbap"
    for email_address in email_addresses:
        receiver_email = email_address
        subject = f"Invitation: AiDhunik Krishi Project Feedback Session on {session_date.strftime('%B %d, %Y')} at {session_time.strftime('%I:%M %p')}"
        
        # Define the logo path
        logo_path = os.path.join(root_dir, "assets", "projectlogo1.png")
        
        body = f"""
        <html>
        <body>
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td align="center" bgcolor="#f7f7f7">
                        <table width="600" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td align="center" style="padding: 20px 0;">
                                    <img src="cid:logo" alt="Penta Synergetics" width="100">
                                </td>
                            </tr>
                            <tr>
                                <td align="left" bgcolor="#ffffff" style="padding: 20px; font-family: Arial, sans-serif; color: #333333;">
                                    <p>Dear Stakeholder,</p>
                                    <p>You are cordially invited to the <strong> AiDHUNIK KRISHI Project:  An Advanced CNN Based Plant Leaf Disease Classification Platform Feedback Session</strong>, which will be held on <strong>{session_date.strftime('%B %d, %Y')}</strong> at <strong>{session_time}</strong>.</p>
                                    <p>This session is an opportunity for us to gather your valuable input, discuss the system's performance, and identify areas for improvement. Your participation is crucial to the continuous enhancement of our Plant Leaf Disease Detection System.</p>
                                    <p>Please let us know if you can attend the session by responding to this email.</p>
                                    <p>Best regards,<br>
                                    AiDhunik Krishi Project</p>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 20px 0; font-family: Arial, sans-serif; color: #777777; font-size: 12px;">
                                    <p>AiDhunik Krishi<br>
                                    The Trade Tower, Thapathali, Kathmandu, Nepal<br>
                                    <a href="mailto:aidhunikkheti@gmail.com">aidhunikkheti@gmail.com</a></p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

        # Specify the file path of the attachment
        attachment_path = os.path.join(root_dir, "Component_datasets", "Feedback.csv")

        # Create a multipart message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Attach the body to the email
        message.attach(MIMEText(body, "html"))

        # Attach the logo
        with open(logo_path, "rb") as logo:
            logo_part = MIMEBase("application", "octet-stream")
            logo_part.set_payload(logo.read())
            encoders.encode_base64(logo_part)
            logo_part.add_header("Content-ID", "<logo>")
            logo_part.add_header("Content-Disposition", "inline", filename=os.path.basename(logo_path))
            message.attach(logo_part)

        # Attach the file
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(attachment_path)}")
            message.attach(part)

        # Send the email
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.send_message(message)
                logging.info("E-mail invitation sent successfully")
                st.success(f"Feedback session invitation email ✉️ has been sent to {email_address}.")
                st.warning("📬 Haven't received the email invitation? Check your spam folder for any missed messages!")

        except Exception as e:
            logging.error(f"Error sending email: {e}")
            st.error("An error occurred while sending the email invitation. Please try again later.")

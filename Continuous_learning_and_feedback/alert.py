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

def send_alert(avg_rating, rating_threshold, negative_feedback_count, negative_feedback_threshold):
    # Set up email details
    sender_email = "aidhunikkheti@gmail.com"
    receiver_email = "autkrista24@britishinternationalcollege.edu.np"
    password = "lllx eghw hfpt lbap"
    subject = "User Feedback Alert - System Approaching Thresholds"

    # Define the logo path
    logo_path = os.path.join(root_dir, "assets", "teamlogo.png")

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
                                <p>Dear Team,</p>
                                <p>Our user feedback monitoring system has detected that one or more of the configured thresholds has been approached or exceeded. This automated alert is to notify you of the issue, so that you can investigate and address the underlying problems.</p>
                                <p>The specific details are as follows:</p>
                                <ul>
                                    <li><strong>Average User Rating Threshold:</strong><br>
                                    &emsp;-> Current Average Rating: {avg_rating}<br>
                                    &emsp;-> Threshold: {rating_threshold}<br>
                                    &emsp;-> The average user rating is nearing or has fallen below the desired threshold of {rating_threshold} stars. This suggests potential quality or usability concerns that need to be addressed.</li>
                                    <li><strong>Negative Feedback Threshold:</strong><br>
                                    &emsp;-> Current Negative Feedback Count: {negative_feedback_count}<br>
                                    &emsp;-> Threshold: {negative_feedback_threshold}<br>
                                    &emsp;-> The number of negative user feedback responses has approached or exceeded the threshold of {negative_feedback_threshold}. This indicates that users are experiencing significant problems with the system.</li>
                                </ul>
                                <p>These thresholds are in place to help us proactively identify and resolve issues before they escalate and impact a larger portion of our user base. We'd appreciate if the engineering team could prioritize the following actions:</p>
                                <ol>
                                    <li>Analyze the specific negative feedback to uncover common themes, root causes, and potential solutions.</li>
                                    <li>Reach out to a sample of users who provided negative feedback to gather more contextual information about their experiences.</li>
                                    <li>Collaborate with the product and design teams to develop and implement fixes or improvements that address the user pain points.</li>
                                    <li>Provide progress updates to the wider organization and affected users to maintain transparency and build trust.</li>
                                    <li>Please review the user feedback data and submit an action plan within the next 24 hours. Let me know if you need any additional information or have any questions.</li>
                                </ol>
                                <p>Thank you for your prompt attention to this matter. Together, we can ensure a positive user experience and maintain the overall health of the system.</p>
                                <p>Best regards,<br>
                                The User Feedback Monitoring System</p>
                            </td>
                        </tr>
                        <tr>
                            <td align="center" style="padding: 20px 0; font-family: Arial, sans-serif; color: #777777; font-size: 12px;">
                                <p>AiDhunik Krishi<br>
                                Trade Tower, Thapathali, Kathmandu, Nepal<br>
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
            logging.info("E-mail alert sent successfully")
            st.success(f"Alert report email ✉️ has been sent to {receiver_email}.")
            st.warning("📬 Haven't received the email? Check your spam folder for any missed messages!")

    except Exception as e:
        logging.error(f"Error sending email: {e}")
        st.error("An error occurred while sending the email alert. Please try again later.")

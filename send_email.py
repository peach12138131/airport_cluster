
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import formataddr
import os
import json

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os




email_password="wastgafpfzeiczme"





def send_email(subject, body, to_email, file_path=None):
    """
    使用Gmail发送邮件（支持附件）
    
    参数:
        subject: 邮件主题
        body: 邮件正文
        to_email: 收件人邮箱（字符串或列表）
        file_path: 附件路径
    
    返回:
        True/False: 发送成功/失败
    """
    # ========== Gmail SMTP配置 ==========
    sender_email = "ai-insight@avi-go.com"
    sender_name = "AI Insight"
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # SSL端口
    username = "ai-insight@avi-go.com"
    password = email_password
    # ===================================
    
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = formataddr((sender_name, sender_email))  # ✅ 修正：添加发件人名称
    msg['To'] = to_email if isinstance(to_email, str) else ', '.join(to_email)
    msg['Subject'] = Header(subject, 'utf-8')
    
    # 添加正文
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    
    # 添加附件
    if file_path:
        files_to_send = []
        if os.path.isdir(file_path):
            print(f"扫描目录: {file_path}")
            for item in os.listdir(file_path):
                full_path = os.path.join(file_path, item)
                if os.path.isfile(full_path):
                    files_to_send.append(full_path)
        elif os.path.isfile(file_path):  # ✅ 添加单文件处理
            files_to_send.append(file_path)
        for file_path in files_to_send:
            filename = os.path.basename(file_path)
            with open(file_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 
                          f'attachment; filename={filename}')
            msg.attach(part)
            print(f"✓ 已添加附件: {filename}")
    
    # 发送邮件
    try:
        print("正在连接Gmail服务器...")
        # ✅ 修正：465端口使用SMTP_SSL
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30) as server:
            print("正在登录...")
            server.login(username, password)
            print("正在发送邮件...")
            server.send_message(msg)
        print("✓ 邮件发送成功！")
        return True
    
    except smtplib.SMTPAuthenticationError:
        print("✗ 认证失败！")
        print("请检查：")
        print("  1. 是否使用了'应用专用密码'（不是普通登录密码）")
        print("  2. 是否已开启两步验证")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"✗ 连接失败: {e}")
        print("可能的原因：")
        print("  1. 网络问题或防火墙阻止")
        print("  2. SMTP服务器不可达")
        print("  3. 端口被封锁")
        return False
    except Exception as e:
        print(f"✗ 发送失败: {e}")
        return False



if __name__ == "__main__":
    contacts=["vivien.ong@jet-bay.com","taoxu@avi-go.com","Hermans@avi-go.com","karhaolee@jet-bay.com",]
    # contacts=["taoxu@avi-go.com",]
    html_body =html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: #ffffff;
                border-radius: 10px;
                padding: 40px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                border-bottom: 3px solid #2196F3;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                color: #2196F3;
                margin: 0;
                font-size: 28px;
            }}
            .header p {{
                color: #666;
                margin: 5px 0 0 0;
                font-size: 14px;
            }}
            .content {{
                margin: 30px 0;
            }}
            .content p {{
                margin: 15px 0;
                font-size: 16px;
            }}
            .highlight-box {{
                background-color: #E3F2FD;
                border-left: 4px solid #2196F3;
                padding: 20px;
                margin: 25px 0;
                border-radius: 5px;
            }}
            .highlight-box h3 {{
                color: #1976D2;
                margin-top: 0;
                font-size: 18px;
            }}
            .attachment-notice {{
                background-color: #FFF3E0;
                border: 2px dashed #FF9800;
                padding: 15px;
                border-radius: 5px;
                margin: 25px 0;
                text-align: center;
            }}
            .attachment-notice p {{
                margin: 5px 0;
                color: #E65100;
                font-weight: bold;
            }}
            .attachment-icon {{
                font-size: 24px;
                margin-bottom: 10px;
            }}
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #e0e0e0;
                font-size: 14px;
                color: #666;
            }}
            .footer p {{
                margin: 5px 0;
            }}
            .button {{
                display: inline-block;
                padding: 12px 30px;
                background-color: #2196F3;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
                font-weight: bold;
            }}
            .stats {{
                display: table;
                width: 100%;
                margin: 20px 0;
            }}
            .stat-item {{
                display: table-cell;
                text-align: center;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 5px;
            }}
            .stat-item:not(:last-child) {{
                border-right: 2px solid #fff;
            }}
            .stat-number {{
                font-size: 24px;
                font-weight: bold;
                color: #2196F3;
                display: block;
            }}
            .stat-label {{
                font-size: 12px;
                color: #666;
                text-transform: uppercase;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- 邮件头部 -->
            <div class="header">
                <h1>✈️ Airport Industry Analysis Report</h1>
               
            </div>
            
            <!-- 邮件正文 -->
            <div class="content">
                <p>Dear Team,</p>
                
                <p>I hope this email finds you well. Please find attached the latest <strong>Airport Industry Analysis Report</strong> containing comprehensive insights and data.</p>
                
                <!-- 重点信息框 -->
                <div class="highlight-box">
                    <h3>📊 Report Highlights</h3>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li>Latest airport industry trends and analysis</li>
                        <li>Key performance metrics and benchmarks</li>
                        <li>Market insights and competitive landscape</li>
                        <li>Strategic recommendations</li>
                    </ul>
                </div>
                
                
                <!-- 附件提醒 -->
                <div class="attachment-notice">
                    <div class="attachment-icon">📎</div>
                    <p>ATTACHMENT INCLUDED</p>
                    <p style="font-weight: normal; color: #666; font-size: 14px;">airportcluster.zip</p>
                </div>
                
                <p>Please review the attached file at your earliest convenience. The report includes detailed analysis and actionable insights that may be valuable for our upcoming strategic discussions.</p>
                
                <p>If you have any questions or need further clarification on any aspect of the report, please don't hesitate to reach out.</p>
            </div>
            
            <!-- 邮件footer -->
            <div class="footer">
                <p><strong>Best Regards,</strong></p>
                <p><strong>AI Insight Team</strong></p>
                <p style="color: #999; font-size: 12px; margin-top: 15px;">
                    This is an automated report generated by AI Insight Analytics Platform<br>
                    © 2025 AVI-GO. All rights reserved.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    send_email(
            subject="Full Airport articles",
            body=html_body,
            to_email=contacts, 
            file_path=r"D:\TAOXU\code\after_20250214\decrease_AI_rate\output\airportcluster2.zip"
        )
    
#!/usr/bin/env python3
"""
Standalone Adult Demo Site
For testing BlockVerify integration end-to-end
"""

import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Adult Demo Site", version="1.0.0")

@app.get("/")
async def home():
    """Adult demo site homepage"""
    return {"message": "Adult Demo Site", "status": "running"}

@app.get("/site", response_class=HTMLResponse)
async def adult_site(verified: str = Query(None)):
    """The actual adult demo site"""
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🔞 PremiumAdultSite.com - BlockVerify Protected</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 0;
                background: #1a1a1a;
                color: white;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
                padding: 40px;
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                border-radius: 12px;
            }}
            .content-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 40px 0;
            }}
            .content-card {{
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 12px;
                text-align: center;
                transition: transform 0.3s;
            }}
            .content-card:hover {{
                transform: translateY(-5px);
            }}
            .btn {{
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 500;
                transition: all 0.3s;
            }}
            .btn:hover {{
                background: linear-gradient(135deg, #ff5252 0%, #e55100 100%);
                transform: translateY(-2px);
            }}
            .privacy-info {{
                background: rgba(76,175,80,0.1);
                border: 2px solid #4CAF50;
                padding: 30px;
                border-radius: 12px;
                margin: 40px 0;
            }}
            .age-gate {{
                background: rgba(255,107,107,0.1);
                border: 2px solid #ff6b6b;
                padding: 60px;
                border-radius: 12px;
                text-align: center;
                margin: 40px 0;
            }}
            .loading {{
                display: none;
                text-align: center;
                padding: 40px;
                background: rgba(33,150,243,0.1);
                border-radius: 12px;
                margin: 20px 0;
            }}
            .spinner {{
                border: 4px solid #f3f3f3;
                border-top: 4px solid #2196F3;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            }}
            @keyframes spin {{
                0% {{ transform: rotate(0deg); }}
                100% {{ transform: rotate(360deg); }}
            }}
            .verification-status {{
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                z-index: 1000;
            }}
            .status-verified {{
                background: #4CAF50;
            }}
            .status-pending {{
                background: #ff9800;
            }}
            .dev-info {{
                background: rgba(33,150,243,0.1);
                border: 1px solid #2196F3;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                font-family: monospace;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔞 PremiumAdultSite.com</h1>
                <p>The finest adult entertainment platform</p>
                <p><small>🔐 Protected by BlockVerify Age Verification</small></p>
            </div>

            <!-- Loading Screen -->
            <div id="loadingScreen" class="loading">
                <div class="spinner"></div>
                <h3>🔐 Checking Age Verification...</h3>
                <p>Please wait while we verify your access credentials...</p>
            </div>

            <!-- Age Gate -->
            <div id="ageGate" style="display: none;">
                <h2>⚠️ Age Verification Required</h2>
                <p style="font-size: 18px; margin: 20px 0;">
                    You must be 18+ years old to access this premium adult content
                </p>
                <p style="color: #ccc;">
                    This site uses BlockVerify for secure, privacy-preserving age verification
                </p>
                <button class="btn" onclick="startVerification()" style="font-size: 18px; padding: 20px 40px;">
                    🔐 Verify My Age (18+)
                </button>
                
                <div class="dev-info" style="margin-top: 40px;">
                    <h4>🔧 For Developers:</h4>
                    <p><strong>Integration Method:</strong> BlockVerify JavaScript SDK</p>
                    <p><strong>API Endpoint:</strong> https://blockverify-api-production.up.railway.app</p>
                    <p><strong>Verification Flow:</strong> User redirects → BlockVerify → Returns with token</p>
                </div>
            </div>

            <!-- Premium Content (shown after verification) -->
            <div id="premiumContent" style="display: none;">
                <div class="privacy-info">
                    <h3>✅ Age Verified Successfully!</h3>
                    <p>🎉 Welcome! You have been verified as 18+ by BlockVerify.</p>
                    <p><strong>Privacy Note:</strong> No personal information was shared with this site during verification.</p>
                </div>

                <div class="content-grid">
                    <div class="content-card">
                        <h3>🎬 Premium Videos</h3>
                        <p>Access our exclusive collection of adult content with crystal-clear 4K quality.</p>
                        <button class="btn">Watch Now</button>
                    </div>
                    
                    <div class="content-card">
                        <h3>📸 Photo Galleries</h3>
                        <p>Browse thousands of high-resolution photos from professional photographers.</p>
                        <button class="btn">View Gallery</button>
                    </div>
                    
                    <div class="content-card">
                        <h3>💬 Live Chat</h3>
                        <p>Connect with performers in real-time through our interactive platform.</p>
                        <button class="btn">Start Chat</button>
                    </div>
                    
                    <div class="content-card">
                        <h3>⭐ VIP Content</h3>
                        <p>Unlock exclusive VIP content available only to verified premium members.</p>
                        <button class="btn">Go VIP</button>
                    </div>
                    
                    <div class="content-card">
                        <h3>🔞 Live Shows</h3>
                        <p>Experience live adult entertainment with interactive features.</p>
                        <button class="btn">Watch Live</button>
                    </div>
                    
                    <div class="content-card">
                        <h3>📱 Mobile App</h3>
                        <p>Download our mobile app for premium content on the go.</p>
                        <button class="btn">Download</button>
                    </div>
                </div>

                <div class="dev-info">
                    <h4>✅ Integration Success!</h4>
                    <p><strong>User Token:</strong> <span id="userToken">Loading...</span></p>
                    <p><strong>Verification Status:</strong> <span style="color: #4CAF50;">VALID ADULT (18+)</span></p>
                    <p><strong>Last Verified:</strong> <span id="verificationTime"></span></p>
                    <button onclick="clearVerification()" style="background: #f44336; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; margin-top: 10px;">
                        🗑️ Clear Verification (Test Again)
                    </button>
                </div>
            </div>
        </div>

        <!-- BlockVerify SDK Integration -->
        <script>
            // Configuration - Replace with your real API key
            const BLOCKVERIFY_CONFIG = {{
                apiUrl: 'https://blockverify-api-production.up.railway.app',
                verifyUrl: 'https://blockverify-api-production.up.railway.app/verify',
                returnUrl: window.location.href.split('?')[0] + '/site',
                debug: true
            }}};

            // Simple BlockVerify SDK implementation
            class BlockVerifySDK {{
                constructor(config) {{
                    this.config = config;
                    this.log('🔐 BlockVerify SDK initialized');
                }}

                log(message, data = '') {{
                    if (this.config.debug) {{
                        console.log(`[BlockVerify] ${{message}}`, data);
                    }}
                }}

                // Check if user has a valid age verification token
                checkAgeVerification() {{
                    this.log('🔍 Checking age verification...');
                    
                    // Check URL for verification callback
                    const urlParams = new URLSearchParams(window.location.search);
                    if (urlParams.get('verified') === 'true') {{
                        this.log('🔄 User returned from verification');
                        // Small delay to allow token to be set
                        setTimeout(() => this.validateToken(), 500);
                        return;
                    }}

                    // Check for existing token
                    const token = this.getStoredToken();
                    if (token) {{
                        this.log('🎫 Found stored token', token.substring(0, 20) + '...');
                        this.validateToken();
                    }} else {{
                        this.log('❌ No token found, showing age gate');
                        this.showAgeGate();
                    }}
                }}

                getStoredToken() {{
                    // Try multiple storage locations
                    return localStorage.getItem('AgeToken') ||
                           this.getCookie('AgeToken') ||
                           sessionStorage.getItem('AgeToken');
                }}

                getCookie(name) {{
                    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
                    return match ? match[2] : null;
                }}

                validateToken() {{
                    const token = this.getStoredToken();
                    if (!token) {{
                        this.showAgeGate();
                        return;
                    }}

                    // For demo purposes, validate locally
                    // In production, you'd send this to your backend with your API key
                    if (token.includes('adult_verified') || token.includes('verified')) {{
                        this.log('✅ Token validation successful');
                        this.showPremiumContent(token);
                    }} else {{
                        this.log('❌ Token validation failed');
                        this.showAgeGate();
                    }}
                }}

                showLoadingScreen() {{
                    document.getElementById('loadingScreen').style.display = 'block';
                    document.getElementById('ageGate').style.display = 'none';
                    document.getElementById('premiumContent').style.display = 'none';
                }}

                showAgeGate() {{
                    document.getElementById('loadingScreen').style.display = 'none';
                    document.getElementById('ageGate').style.display = 'block';
                    document.getElementById('premiumContent').style.display = 'none';
                    
                    this.showStatus('Age verification required', 'pending');
                }}

                showPremiumContent(token) {{
                    document.getElementById('loadingScreen').style.display = 'none';
                    document.getElementById('ageGate').style.display = 'none';
                    document.getElementById('premiumContent').style.display = 'block';
                    
                    // Update token display
                    document.getElementById('userToken').textContent = token.substring(0, 30) + '...';
                    document.getElementById('verificationTime').textContent = new Date().toLocaleString();
                    
                    this.showStatus('Age verified (18+)', 'verified');
                    this.log('🎉 Premium content unlocked');
                }}

                showStatus(message, type) {{
                    // Remove existing status
                    const existing = document.querySelector('.verification-status');
                    if (existing) existing.remove();

                    // Add new status
                    const status = document.createElement('div');
                    status.className = `verification-status status-${{type}}`;
                    status.textContent = message;
                    document.body.appendChild(status);

                    // Auto-remove after 5 seconds
                    setTimeout(() => {{
                        if (status.parentNode) status.remove();
                    }}, 5000);
                }}

                startVerification() {{
                    this.log('🚀 Starting verification process...');
                    const verifyUrl = `${{this.config.verifyUrl}}?return_url=${{encodeURIComponent(this.config.returnUrl)}}`;
                    this.log('🔄 Redirecting to:', verifyUrl);
                    window.location.href = verifyUrl;
                }}

                clearVerification() {{
                    this.log('🗑️ Clearing verification data...');
                    localStorage.removeItem('AgeToken');
                    sessionStorage.removeItem('AgeToken');
                    document.cookie = 'AgeToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                    
                    // Refresh page
                    window.location.href = window.location.href.split('?')[0] + '/site';
                }}
            }}

            // Initialize SDK when page loads
            document.addEventListener('DOMContentLoaded', function() {{
                window.blockVerify = new BlockVerifySDK(BLOCKVERIFY_CONFIG);
                
                // Show loading screen initially
                window.blockVerify.showLoadingScreen();
                
                // Start verification check after a brief delay
                setTimeout(() => {{
                    window.blockVerify.checkAgeVerification();
                }}, 1000);
            }});

            // Global functions for UI
            function startVerification() {{
                window.blockVerify.startVerification();
            }}

            function clearVerification() {{
                if (confirm('This will clear your verification and require you to verify again. Continue?')) {{
                    window.blockVerify.clearVerification();
                }}
            }}

            // URL parameter check for verification callback
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('verified') === 'true') {{
                console.log('🔄 [BlockVerify] Verification callback detected');
            }}
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port) 
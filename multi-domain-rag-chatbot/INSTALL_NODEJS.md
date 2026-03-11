# Installing Node.js and npm

## The Problem
You're seeing `npm is not recognized` because Node.js (which includes npm) is not installed on your system.

## Solution: Install Node.js

### Option 1: Download from Official Website (Recommended)

1. **Go to:** https://nodejs.org/
2. **Download the LTS version** (Long Term Support - recommended)
   - It will be a `.msi` installer file (e.g., `node-v20.x.x-x64.msi`)
3. **Run the installer:**
   - Double-click the downloaded file
   - Follow the installation wizard
   - **Important:** Make sure to check "Add to PATH" option during installation
   - Click "Next" through all steps
   - Click "Install"
4. **Restart your terminal** (close and reopen Command Prompt/PowerShell)
5. **Verify installation:**
   ```cmd
   node --version
   npm --version
   ```

### Option 2: Using Chocolatey (If you have it)

If you have Chocolatey package manager installed:
```cmd
choco install nodejs
```

### Option 3: Using Winget (Windows Package Manager)

```cmd
winget install OpenJS.NodeJS.LTS
```

---

## After Installation

1. **Close and reopen your terminal** (important!)
2. **Verify it works:**
   ```cmd
   node --version
   npm --version
   ```
3. **Navigate to frontend folder:**
   ```cmd
   cd multi-domain-rag-chatbot\frontend
   ```
4. **Install dependencies:**
   ```cmd
   npm install
   ```
5. **Start the dev server:**
   ```cmd
   npm run dev
   ```

---

## Troubleshooting

**Still not working after installation?**
- Close and reopen your terminal completely
- Restart your computer (sometimes needed for PATH updates)
- Check if Node.js is installed: Look for `C:\Program Files\nodejs\` folder
- Manually add to PATH:
  1. Search "Environment Variables" in Windows
  2. Edit "Path" variable
  3. Add: `C:\Program Files\nodejs\`
  4. Restart terminal

**Which version to install?**
- **LTS (Long Term Support)** - Recommended for most users
- **Current** - Latest features, but may be less stable

---

## Quick Check Commands

After installation, run these to verify:
```cmd
node --version    # Should show something like v20.x.x
npm --version     # Should show something like 10.x.x
```

Once these work, you can proceed with:
```cmd
cd multi-domain-rag-chatbot\frontend
npm install
npm run dev
```


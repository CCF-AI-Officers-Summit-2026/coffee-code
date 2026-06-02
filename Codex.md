# Getting Started With Codex CLI In GitHub Codespaces

Use these steps to create a GitHub Codespace from the workshop repository and
start using the Codex CLI inside that Codespace.

## 1. Create A New Codespace

1. Open the workshop repository in GitHub.
2. Select **Code**.
3. Select the **Codespaces** tab.
4. Select **Create codespace**.
5. Wait for the Codespace to finish loading.

## 2. Install The Codex CLI

In the Codespace terminal, install the Codex CLI using one of the following
methods.

### macOS/Linux

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

### npm

```bash
npm install -g @openai/codex
```

### Homebrew

```bash
brew install --cask codex
```

## 3. Sign In With Device Authentication

In the Codespace terminal, start the Codex login flow with device
authentication:

```bash
codex login --device-auth
```

Codex will show a link and a one-time device code in the terminal.

1. Open the link in your browser.
2. Sign in to the **Coffee & Code 6/4 ChatGPT Workspace** using the email and
   password associated with your account.
3. Enter the device code shown in the Codespace terminal.
4. Return to the Codespace terminal when the login completes.

## 4. Start Using Codex

From the workshop repository directory in the Codespace terminal, run:

```bash
codex
```

You are now ready to use Codex CLI in the workshop repository.

## Documentation

For more details, see the Codex CLI documentation:

https://developers.openai.com/codex/cli

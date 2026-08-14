## 🎯 Summary

<!-- Please provide a clear and concise description of the changes proposed in this PR. -->

### Type of Change
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 📝 Documentation update (changes to docs or templates)
- [ ] 🧹 Code cleanup / Refactoring (no functional changes)

---

## ⚙️ Workflow & Portability Impact

<!-- Describe how this change affects existing workflows, local configurations, or platform portability. -->
- **Workflow Impact**: <!-- e.g., how agents execute, change in behavior -->
- **Portability Impact**: <!-- e.g., compatibility with macOS, Windows, Linux, different python versions -->

---

## 🛠️ Verification & Testing

Please verify that the following checks pass before submitting:

### Static Validation & Analysis
- [ ] `python tools/import_and_analyze.py` runs with no errors
- [ ] `python tools/validate_repo.py` runs with `PASS` status
- [ ] All Python files pass syntax check (`py_compile`)

### Hygiene & Security Guardrails
- [ ] No private Windows/Unix absolute paths (e.g. `C:\Users\...`, `/Users/...`)
- [ ] No personal identifiers or client-specific terms (`HF_`, `KHPT`, etc.)
- [ ] No hardcoded passwords, tokens, or API credentials
- [ ] Source originals are unchanged or safely versioned

---

## 📂 Evidence

<!-- Provide evidence of successful execution (e.g., terminal output, json schema logs, or verification commands). -->
```json
// Paste the output of python tools/validate_repo.py here
```

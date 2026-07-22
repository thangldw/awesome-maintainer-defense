```yaml
name: 📚 Documentation Correction Request
description: Use this form when you have found documentation that is unclear, outdated, inaccurate, or confusing.
labels: [] # Labels are assigned by repository maintainers after issue creation

body: |
  ---
  ### 📂 1. Location Details (Mandatory)

  *   **Page/File:** *Specify the exact file path and name where the documentation lives.*
  *   **Section Title:** *What is the title or subheading containing the problematic text?*
  *   **Version Context (If Applicable):** *Is this issue specific to a version, e.g., "v1.2" vs "latest"?*

  ---
  ### 📝 2. Problem Area Identification (Mandatory)

  Please provide the exact passage or snippet of code/text that is incorrect, misleading, or unclear. This helps maintainers pinpoint the issue quickly.

  **Current Wording/Code Snippet:**
  *(Provide the text here. Use a code block for code snippets.)*
  ```markdown
  [Paste the problematic text or snippet here]
  ```

  ---
  ### ✨ 3. Proposed Correction (Mandatory)

  Please provide the fully corrected, desired documentation passage. This should be ready to copy-paste directly into the file. When proposing a correction for code examples, please include the updated runnable example if necessary.

  **Proposed Replacement:**
  *(Write your proposed solution here.)*
  ```markdown
  [Draft your ideal text or replacement snippet here]
  ```

  ---
  ### 💡 4. Supporting Evidence and Rationale (Highly Recommended)

  If the correction is based on a factual claim, API behavior, or external source, please provide supporting evidence. This validates the claim and drastically speeds up review time.

  **Evidence/Links:**
  *   [Link to official API documentation, RFCs, etc.]
  *   [Description of how you tested this (e.g., "Observed in Console Log X when running command Y").]

  ---
  ### ✍️ Summary and Tone Check

  **Briefly summarize:** Why is the current wording confusing/incorrect, and what does the corrected version achieve? (E.g., *The original snippet missed handling asynchronous state changes.*)

```
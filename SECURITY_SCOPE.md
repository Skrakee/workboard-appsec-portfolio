# About this lab

Workboard is a local learning project with sample organizations, accounts and known security weaknesses. The goal is to find, test and fix those weaknesses.

Run it at `http://127.0.0.1:8085` with sample data. Do not publish the running lab on the Internet.

The sample passwords and signing secrets are public on purpose. They are for this lab only. Real passwords and live sign-in tokens must be hidden in reports.

The original before-and-after commit sequence was rebuilt from a saved copy of the vulnerable code. It shows the test and fix, but it is not the original development history. The manual requests and retest in [finding 1](findings/1-document-update.md) were performed with Burp Suite.

The [threat model](docs/threat-model.md) separates completed checks from tests that still need to be done.

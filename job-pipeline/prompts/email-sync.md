# Email sync agent prompt

Fill every `{{PLACEHOLDER}}` from `config.yaml`. Give this task only the mail
connector's read and search tools and the sheet connector.

---

Weekly email sync of {{OWNER_NAME}}'s job search into the Google Sheet
"{{SHEET_NAME}}" (spreadsheet id {{SHEET_ID}}). The sheet is the only source of
truth. Read and write it with the Google Sheets connector. Do not create files,
JSON snapshots or spreadsheet copies (temporary scratch files are fine).

This task only syncs email into the sheet. A separate task refreshes the data
sources; do not do that work here.

Tabs used here: Pipeline (sheetId {{TAB_PIPELINE}}), Recruiters
({{TAB_RECRUITERS}}), Shortlist ({{TAB_SHORTLIST}}). Row 1 of each tab is a
description, row 2 the header. Pipeline columns: A Company, B Role, C Channel,
D Stage, E Last contact, F Follow up by, G Next step, H Contact, I Notes.
Active rows at the top, then a row reading "Closed", then closed rows.

Steps
1. Read the Pipeline, Recruiters and Shortlist tabs in full.
2. Search email for the last {{LOOKBACK_DAYS}} days: application confirmations,
   interview invites and confirmations, rejections, offers, and recruiter mail.
   Also search Sent mail, because {{OWNER_NAME}} emails some companies and
   recruiters directly. Open full threads before concluding anyone did not
   reply; search results may show only part of a thread.
3. Update Pipeline first. Match rows by company name, not cell position. Update
   Stage, Last contact (YYYY-MM-DD), Next step, Contact and Notes. Add new
   processes and applications. Move rejected, withdrawn or closed processes to
   the Closed section with the date.
4. Set Follow up by (column F) for every active row: 2 business days after an
   interview with no news; 1 week after a direct email application; 2 weeks
   after a job-board application; after any reply, recompute from that reply's
   date. If someone gave a decision date, use the next business day after it.
   Leave closed rows blank.
5. Update Recruiters (last contact, status, next step). Add new recruiters. Add
   suspicious senders to the Ignore section: generic scraped pitches, domains
   that do not match the company they claim, free-mail addresses posing as
   companies, chat-app-first contact. Never engage with them.
6. On Shortlist, only mark applied or rejected for companies already listed. Do
   not change any other notes.
7. Update the "last updated" date in Pipeline row 1.

Rules
- Use only mail tools that search and read. Do not use any tool that sends,
  drafts, replies, forwards, labels, trashes or changes mail.
- Do not guess. If an email is ambiguous about which company or role it refers
  to, say so in the row instead of assuming.
- A cell value starting with "=" is read as a formula; prefix it with "'".
- On a Sheets quota error, wait about a minute and retry.
- {{EXTRA_RULES}}

Report: send one short message listing (a) changes made to the sheet, (b) rows
whose Follow up by date is today or past, with the contact for each, and (c)
anything that needs a decision, including anything ambiguous or any step that
failed. If nothing changed, say so in one sentence and still list due
follow-ups.

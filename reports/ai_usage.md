# AI Usage Acknowledgement

## Project
IPL Cricket Analytics

## AI Tools Used
- ChatGPT
- Google Gemini

## Purpose of AI Usage
AI tools were used to:
- Generate and explain SQL queries.
- Suggest approaches for cricket data analysis.
- Explain statistical concepts.
- Compare alternative SQL solutions.
- Support report writing and documentation.

## Independent Verification
AI-generated answers were checked using:
- SQLite database queries.
- Database schema inspection.
- Cricket scoring rules.
- Independent calculations and comparisons.

## Examples of Corrections

### Bowling Wickets
Gemini omitted `caught and bowled` from a wicket-count query.
The query returned 224 wickets for YS Chahal.
After correcting the query and checking the database,
the verified result was 228 wickets.

### First-Innings Score Bands
An AI-generated query referenced `first_innings_runs`,
which was not a column in the database view.
The actual column was `first_innings_total`.
The query was corrected and verified.

## Responsibility Statement
AI tools assisted with analysis and documentation,
but their outputs were not treated as authoritative.
All final findings were checked against the project database.
Responsibility for the submitted work and its accuracy
remains with the project author.

# Four-Point Fabric Inspection Calculator

**Student:** Syed Kafeel Ahmed Shah  
**Roll No.:** 25TE051  
**Department:** Textile Engineering, Mehran University of Engineering and Technology (MUET), Jamshoro  
**Course:** AI234 – Artificial Intelligence | 3rd Semester  
**Instructor:** Dr. Pardeep Kumar Gianchandani

## Project overview
This Streamlit web application calculates the four-point fabric inspection score from defect lengths and quantities. The user enters fabric width and inspected roll length. The application assigns penalty points to each defect, calculates points per 100 square yards, and classifies the inspected roll as Pass or Reject against an editable acceptance limit.

## Features
- Fabric width in inches and inspected roll length in yards.
- Editable defect table with defect length and quantity.
- Four-point defect schedule: 0–3 inches = 1 point; over 3–6 = 2; over 6–9 = 3; over 9 = 4.
- Total defect count and total penalty points.
- Inspected area in square yards.
- Points per 100 square yards.
- Pass/Reject classification using an editable threshold.
- Penalty breakdown table and chart.
- Limitations and Responsible Use statement.

## Calculation method
Penalty points are assigned to each defect based on its length:
- 0 to 3 inches: 1 point
- Over 3 to 6 inches: 2 points
- Over 6 to 9 inches: 3 points
- Over 9 inches: 4 points maximum per defect

`Inspected area (sq. yd) = (Fabric width in inches ÷ 36) × inspected length in yards`

`Points per 100 sq. yd = (Total penalty points ÷ inspected area in sq. yd) × 100`

The roll is classified as **Pass** when the score is less than or equal to the selected acceptance limit; otherwise it is **Reject**.

## Run locally
1. Install Python 3.10 or later.
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`

## GitHub and Streamlit Community Cloud deployment
1. Create a public GitHub repository.
2. Upload `app.py`, `requirements.txt` and `README.md`.
3. Sign in at https://share.streamlit.io/ using GitHub.
4. Select the repository, branch and `app.py`, then deploy.
5. Test the live app URL and add the GitHub repository and live Streamlit URLs to Slide 5 of the presentation.

## Responsible use and limitations
This is a rule-based educational calculator, not an AI vision inspection system. It relies on user-entered defect measurements and counts. The example acceptance limit of 40 points per 100 square yards is not universal; confirm the buyer or mill specification and the applicable inspection procedure before commercial acceptance. The app does not collect or store personal data.

## Submission
Suggested presentation filename: `25TE051_AI234_TextileAI.pptx`  
Assignment deadline shown in the supplied brief: **06 December 2026**.

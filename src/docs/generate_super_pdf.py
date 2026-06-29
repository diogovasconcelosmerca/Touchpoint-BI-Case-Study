import os
from fpdf import FPDF

class SuperPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.set_text_color(20, 164, 155)
        self.cell(0, 10, 'Touchpoint Analytics: Technical Business Case & Architecture Review', 0, 1, 'C')
        self.set_font('helvetica', 'I', 10)
        self.set_text_color(148, 163, 184)
        self.cell(0, 5, 'Comprehensive End-to-End Implementation Guide', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, num, title):
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(255, 140, 0)
        self.set_fill_color(20, 25, 30)
        self.cell(0, 10, f'Chapter {num}: {title}', 0, 1, 'L', fill=True)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, text)
        self.ln(5)

def create_super_pdf():
    pdf = SuperPDF()
    pdf.add_page()
    
    # Chapter 1: The Corporate Profile & Case Study Alignment
    pdf.chapter_title(1, 'The Corporate Profile & Case Study Alignment')
    t1 = (
        "THE BEVERAMA CORPORATE ESSENCE:\n"
        "To build a truly impactful Business Intelligence solution, we must align the data architecture with the company's DNA as outlined in the Case Study:\n\n"
        "1. Global Market Leader: Beverama is the world's largest beverage producer with a 33% global market share and 57 locations worldwide. The UK operations are based in Scarborough.\n"
        "2. Brand Ethos ('It\\'s all tasty'): The company focuses on the quality of its beverages and strong relationships with suppliers, communities, and customers.\n"
        "3. Sustainable Growth: Beverama invests heavily in alternative energy (e.g., wind turbines) and supports local charities and social impact projects.\n"
        "4. Product Portfolio & Innovation: The portfolio covers all consumer trends: Beverama (natural juices), Bevty (anti-oxidant blends), Juiced (affordable range), and Wipe Bevs (fortified blends). The focus is on healthier drinks and adapting to evolving lifestyles.\n"
        "5. Local Market Strategy: This dataset represents a recent entry into the local market, focusing specifically on the two largest retail chains (medium and large-format supermarkets).\n\n"
        "By grounding our BI solution in this corporate profile, we ensure that every metric and insight serves the ultimate goal: strengthening Beverama's position in this new local market while respecting its global ethos."
    )
    pdf.chapter_body(t1)

    # Chapter 2
    pdf.chapter_title(2, 'The Business Story & Time Window (The Pitch)')
    t2 = (
        "THE PITCH (Memorize this for the interview):\n"
        "\"I analyzed a comprehensive dataset spanning a Time Window of exactly 25 months (from January 1, 2018, to January 27, 2020). "
        "The goal was to dissect EUR 2.7M in total revenue to understand exactly 'what happened' and 'how it happened'.\n\n"
        "WHAT HAPPENED:\n"
        "Over these two years, the business exhibited extreme seasonality. We observe massive revenue spikes at the end of each year, followed by sharp contractions in the first quarter. "
        "Despite these peaks, the overarching trend required deeper investigation into product pricing and geographic concentration.\n\n"
        "HOW IT HAPPENED (The Sub-Brand Portfolio Strategy):\n"
        "1. The Parent Company vs Sub-Brand Dynamic: As per the case study, 'Beverama' is the parent company, but its namesake natural juice line ('Beverama') is the #1 anchor of the sub-brand portfolio, driving the highest volume and revenue (EUR 720k).\n"
        "2. The Core Pillars (Juiced & Wipe Bevs): These are not niche sub-brands; they are massive financial pillars, generating over EUR 600k each and moving tremendous volume, rivaling the leader.\n"
        "3. The Premium Niche (Bevty): Operates at a higher price point (Premium), driving EUR 380k in revenue despite having only a fraction of the volume of the others.\n"
        "4. Geographic Concentration: Cities like Detroit and Minneapolis act as heavy financial anchors, dominating the client footprint.\n"
        "5. The 'Unknown SKU' Strategy: Over 110k units sold were unmapped to any Master Data product. A junior analyst would drop these rows, losing critical financial data. Instead, I strategically aggregated them under the parent 'Beverama' brand. This preserves 100% of global Revenue for the C-level, while keeping the 'Unknown SKU' flag at the product level for the MDM team to urgently fix.\n\n"
        "With this historical context established, I built an AI predictive model to forecast the next 6 months and engineered a dynamic dashboard so managers can slice this story by any sub-brand, city, or date.\""
    )
    pdf.chapter_body(t2)
    
    # Chapter 3
    pdf.chapter_title(3, 'Executive Strategy & Architecture Selection')
    t3 = (
        "This project was designed from the ground up to demonstrate a 'Senior Data Engineer' approach rather than "
        "a junior script. Instead of relying on standard Pandas (which is notorious for Out-Of-Memory errors on "
        "production-scale data), the pipeline leverages DuckDB.\n\n"
        "Architecture Choice: Native ELT (Extract, Load, Transform) via Medallion Architecture.\n"
        "- Bronze Layer: Raw CSV files are read natively into memory without strict typing.\n"
        "- Silver Layer: Pure SQL is used for cleansing, type casting, and anomaly removal.\n"
        "- Gold Layer: Data is normalized into a strict Kimball Star Schema.\n"
        "This approach proves that the candidate understands how to scale analytics to gigabytes of data using "
        "columnar, in-process engines, minimizing computational overhead on the final Streamlit dashboard."
    )
    pdf.chapter_body(t3)

    # Chapter 4
    pdf.chapter_title(4, 'Data Extraction & Cleansing (Silver Layer)')
    t4 = (
        "The raw data contained several format inconsistencies and mathematical anomalies that required handling:\n\n"
        "1. String Cleansing: The 'PVP' (Price) column contained 'EUR' currency symbols and European comma separators. "
        "These were surgically removed via SQL REPLACE functions and CAST to DOUBLE.\n"
        "2. Upstream Pre-calculation: Revenue was calculated directly in the ELT layer (Price * Volume) rather than "
        "forcing the Streamlit dashboard to calculate it on the fly. This saves critical CPU cycles during UI rendering.\n"
        "3. Anomaly Expurgation: An extreme logic audit revealed 16 transactions with zero or negative Volume/Revenue "
        "(likely customer returns). A strict WHERE clause was added to the Silver layer to drop these records, "
        "ensuring that downstream metrics like 'Average Price' (Revenue / Volume) are mathematically safe from division-by-zero errors."
    )
    pdf.chapter_body(t4)

    # Chapter 5
    pdf.chapter_title(5, 'Kimball Star Schema & Data Quality (Gold Layer)')
    t5 = (
        "The core of the Business Intelligence engine is a robust Relational Model adhering to Ralph Kimball's rules.\n\n"
        "- Dim_Store (1:1 Granularity): The 'Store' and 'Client' raw files were joined. A critical duplication was solved "
        "by recognizing that 'Cliente' and 'BannerID' together form a composite key, ensuring perfect uniqueness.\n"
        "- Dim_Date: A programmatic continuous calendar was generated from Jan 2018 to Dec 2020. This allows for flawless Time-Intelligence.\n"
        "- Dim_Item & The 'Unknown SKU' Strategy: The raw Fact table contained 11 ITEMCODEs that did not exist in the Master Items list. "
        "A junior analyst would drop these rows (losing financial data) or fail the pipeline. Instead, the ETL dynamically maps missing codes "
        "to an 'Unknown SKU' dimension. This brilliant strategy preserves 100% of global Revenue while mathematically flagging Master Data inconsistencies for the business to fix."
    )
    pdf.chapter_body(t5)

    # Chapter 6
    pdf.chapter_title(6, 'Dashboard Logic & Mathematical Edge Cases')
    t6 = (
        "The Streamlit application was built to be highly interactive, but filters can break simple math. Several advanced protections were coded:\n\n"
        "1. Year-to-Date (YTD) YoY Alignment: The dataset ends abruptly on January 27, 2020. A naive YoY calculation would compare "
        "27 days of 2020 against 365 days of 2019, resulting in a false -95% drop. The code enforces a strict YTD limit on the previous year "
        "matching the exact day-of-year of the current year.\n"
        "2. The Target Gauge: Instead of arbitrary fixed numbers, the KPI Target Gauge calculates the 'All-Time Best Historic Year' for the selected filters. "
        "This dynamic benchmark constantly challenges executives to beat their best historical performance."
    )
    pdf.chapter_body(t6)
    
    # Chapter 7
    pdf.chapter_title(7, 'KPI Strategy & Metric Definitions (Business Justifications)')
    t7 = (
        "Every metric on the dashboard was carefully selected to answer specific executive questions:\n\n"
        "1. Total Revenue: The ultimate anchor of business health. Tells C-Levels exactly how much money the business generated under the selected filters.\n"
        "2. Total Volume (Units): Revenue can grow artificially through price inflation while market share shrinks. Tracking Volume ensures we monitor actual product demand.\n"
        "3. Average Price / Unit (Revenue / Volume): A crucial profitability metric. By tracking this, managers can instantly see if discounting strategies are hurting margins or if premium products are driving growth.\n"
        "4. YoY Growth (Year-over-Year): Calculated dynamically with strict Year-to-Date alignment. Justification: Absolute numbers lack context. A manager needs to know the 'momentum' of the business (growing or shrinking compared to the same period last year).\n"
        "5. Best Year Benchmark (Target Gauge): Instead of arbitrary static targets, the Gauge calculates the 'All-Time Historic High' for the exact filter context. This visually challenges managers to constantly beat their own historical records.\n"
        "6. Machine Learning Forecast (6-Months): Descriptive KPIs only tell what happened. The AI Forecast provides a mathematical projection of where the Revenue is heading, allowing Supply Chain and Finance to prepare in advance."
    )
    pdf.chapter_body(t7)

    # Chapter 8
    pdf.chapter_title(8, 'Data Visualization & Best Practices')
    t8 = (
        "The UI follows 2026 Executive Dashboard aesthetics:\n\n"
        "- Sparkline Indicators: Standard KPIs were upgraded to Plotly Sparklines. Numbers are overlayed on historical trend areas, providing instant context.\n"
        "- Waterfall Chart: Bridges the exact category-level drivers behind Revenue growth or contraction between years.\n"
        "- Pareto Chart (80/20 Rule): A cumulative percentage line graph instantly reveals which core Brands drive the vast majority of the company's financial weight.\n"
        "- Scatter Plots: By plotting Price vs Volume, Product Managers can instantly visualize market positioning and identify 'Cash Cows'."
    )
    pdf.chapter_body(t8)

    # Chapter 9
    pdf.chapter_title(9, 'Predictive Analytics (XGBoost) & ML Poisoning')
    t9 = (
        "To move beyond Descriptive Analytics into Predictive Intelligence, an XGBoost Regression model was implemented.\n\n"
        "- Feature Engineering: The model learns from Time Indexes, Lag_1 (previous month), Lag_2, and a 3-month Rolling Mean.\n"
        "- Preventing ML Poisoning: Since Jan 2020 only has 27 days, its total volume is artificially low. Training the model on this incomplete month "
        "would 'poison' the AI, causing it to predict a massive future contraction. The pipeline detects incomplete final months and gracefully excludes them from the training set, ensuring the forecast remains highly accurate and stable."
    )
    pdf.chapter_body(t9)
    
    pdf.add_page()
    
    # Chapter 10
    pdf.chapter_title(10, 'Enterprise Scalability Roadmap (Phase 2)')
    t10 = (
        "While perfectly tailored for this case study, scaling this architecture to 100 Million+ rows requires the following Enterprise upgrades:\n\n"
        "1. Schema Contracts: Replace 'read_csv_auto' with explicit schema definitions to prevent pipeline crashes if upstream source data types drift.\n"
        "2. Currency Agnosticism: Replace hardcoded 'EUR' replacement with Regex (Regular Expressions) to extract numerics, supporting future global expansion.\n"
        "3. Incremental Upserting: Move away from 'Full Load' (CREATE OR REPLACE) to 'Incremental Load', checking the MAX(Date) and importing only net-new daily data.\n"
        "4. ML Caching & Tuning: Implement '@st.cache_resource' to prevent the model from retraining on every UI click, and add GridSearch for dynamic Hyperparameter Tuning."
    )
    pdf.chapter_body(t10)

    # Save to the specific folder
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_dir = BASE_DIR
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "Super_Guia_Tecnico_Touchpoint.pdf")
    pdf.output(out_path)
    print(f"Super PDF successfully generated at: {out_path}")

if __name__ == '__main__':
    create_super_pdf()

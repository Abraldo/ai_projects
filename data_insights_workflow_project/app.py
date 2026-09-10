import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-openai-key")

class AutomatedDataPipeline:
    def __init__(self, csv_path: str = "retail_leads.csv"):
        self.csv_path = csv_path
        self.engine = create_engine("sqlite:///:memory:")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
        self._bootstrap_database()

    def _bootstrap_database(self):
        """Creates dummy data combining Pandas and SQLite to model enterprise lead datasets."""
        # Generate raw business data using pandas/numpy
        np.random.seed(42)
        records = 50
        data = {
            "lead_id": range(1001, 1001 + records),
            "candidate_name": [f"Candidate_{i}" for i in range(records)],
            "technical_score": np.random.randint(60, 100, size=records),
            "experience_years": np.random.randint(1, 15, size=records),
            "lead_status": np.random.choice(["New", "Screened", "Qualified", "Scheduled"], size=records),
            "conversion_probability": np.round(np.random.uniform(0.1, 0.95, size=records), 2)
        }
        df = pd.DataFrame(data)
        df.to_csv(self.csv_path, index=False)
        
        # Load CSV into clean in-memory relational SQL table
        df_sql = pd.read_csv(self.csv_path)
        df_sql.to_sql("leads", self.engine, index=False, if_exists="replace")

    def get_schema(self) -> str:
        return "Table: leads\nColumns: lead_id (INT), candidate_name (TEXT), technical_score (INT), experience_years (INT), lead_status (TEXT), conversion_probability (FLOAT)"

    def text_to_sql_execution(self, natural_query: str) -> dict:
        """Translates natural language to valid SQL, executes it, and reflects analytical results."""
        schema = self.get_schema()
        
        prompt = ChatPromptTemplate.from_template(
            "You are an expert data analyst. Given the following SQL schema, translate the user's natural language request into a single valid SQLite query. "
            "Return ONLY the plain executable SQL string. Do not wrap it in markdown block tags.\n\n"
            "Schema:\n{schema}\n\n"
            "Request: {query}\nSQL Query:"
        )
        
        chain = prompt | self.llm | StrOutputParser()
        generated_sql = chain.invoke({"schema": schema, "query": natural_query}).strip()
        
        # Clean potential markdown wrapping safely
        if generated_sql.startswith("```sql"):
            generated_sql = generated_sql[6:-3].strip()
        elif generated_sql.startswith("```"):
            generated_sql = generated_sql[3:-3].strip()

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(generated_sql))
                columns = result.keys()
                rows = [dict(zip(columns, row)) for row in result.fetchall()]
                
            return {
                "status": "SUCCESS",
                "generated_sql": generated_sql,
                "data": rows,
                "error": None
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "generated_sql": generated_sql,
                "data": [],
                "error": str(e)
            }

    def trigger_webhook_workflow(self, workflow_type: str, payload: dict) -> dict:
        """Simulates enterprise business automation endpoints (n8n/Zapier/Make/Calendly)."""
        # Emulating successful standard API response envelopes matching Bubble or Postman AI outputs
        return {
            "automation_platform": workflow_type,
            "status": "DISPATCHED",
            "payload_transmitted": payload,
            "webhook_response_code": 200,
            "integrated_systems": ["Notion DB Sync", "Calendly Scheduler v2 API"]
        }

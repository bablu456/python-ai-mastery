import google.generativeai as genai
import os



os.environ["GEMENI_API_KEY"] = ""
genai.configure(api_key=os.environ["GEMENI_API_KEY"])

def analyze_backend_error(error_log):
    print(" Ai is analyzing the backend error log...\n ")

    model = genai.GenerativeModel('gemeni-1.5-flash')

    promt = f"""
    you are an expert backend developer. Explain the following error in one simple sentence and provide the exact fix.

    Error Log:
    {error_log}
    """
    response = model.generate_content(promt)

    return response.text

postgres_error = """
org.postgresql.util.PSQLException: FATAL: password authentication failed for user 'postgres'
    at org.postgresql.core.v3.ConnectionFactoryImpl.doAuthentication(ConnectionFactoryImpl.java:514)
"""

ai_solution = analyze_backend_error(postgres_error)

print(" AI's analysis and solution:\n")
print(ai_solution)

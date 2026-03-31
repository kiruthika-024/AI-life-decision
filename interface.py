import gradio as gr
def analyze_user(decision, income, savings, dependents):
    income = float(income)
    savings = float(savings)
    dependents = int(dependents)

    if decision.lower() in ["business", "invest"]:
        if savings > 100000 and income > 30000:
            recommendation = "✅ Decision is correct"
        else:
            recommendation = "❌ Decision might be risky"
    else:
        recommendation = "Decision is fine"

    reasoning = f"Income: {income}, Savings: {savings}, Dependents: {dependents}"
    return recommendation, reasoning

iface = gr.Interface(
    fn=analyze_user,
    inputs=[
        gr.Textbox(label="Decision"),
        gr.Textbox(label="Monthly Income (₹)"),
        gr.Textbox(label="Total Savings (₹)"),
        gr.Textbox(label="Dependents")
    ],
    outputs=[
        gr.Textbox(label="Final Decision"),
        gr.Textbox(label="Reasoning")
    ],
    title="AI Life Decision Helper",
    description="Enter your details and decision to get a recommendation."
)
iface.launch()

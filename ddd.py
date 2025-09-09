from graphviz import Digraph

# Create a directed graph for the proposed system dataflow
dot = Digraph(comment="Dataflow of the Proposed System (High Level)", format="png")

# Define nodes (actors and processes)
dot.node("CUST", "Customer (Web/Mobile)", shape="oval", style="filled", fillcolor="lightblue")
dot.node("BR", "Bank Branch / Portal", shape="rectangle", style="rounded,filled", fillcolor="lightgrey")
dot.node("CPU", "Card Personalization Unit", shape="rectangle", style="rounded,filled", fillcolor="lightgrey")
dot.node("TRACK", "Tracking System", shape="rectangle", style="rounded,filled", fillcolor="lightgreen")
dot.node("COURIER", "Courier Service", shape="rectangle", style="rounded,filled", fillcolor="lightgrey")
dot.node("NTF", "Automated Notification (SMS/Email/App)", shape="parallelogram", style="filled", fillcolor="lightyellow")

# Define edges (dataflow)
dot.edge("CUST", "BR", "Submit Card Request Online")
dot.edge("BR", "CPU", "Forward Request")
dot.edge("CPU", "BR", "Return Personalized Card")
dot.edge("CPU", "COURIER", "Send Card for Delivery")
dot.edge("COURIER", "TRACK", "Update Delivery Status")
dot.edge("TRACK", "CUST", "Real-Time Tracking Info")
dot.edge("BR", "NTF", "System Sends Notification")
dot.edge("NTF", "CUST", "SMS/Email/App Updates")
dot.edge("COURIER", "CUST", "Deliver Card (With Tracking)")

# Render the diagram to a file
file_path = "/mnt/data/proposed_system_dataflow"
dot.render(file_path)

file_path + ".png"

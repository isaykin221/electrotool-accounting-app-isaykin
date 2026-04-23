from flask import Flask, jsonify, redirect, render_template, request, url_for

from database import (
    add_tool,
    get_maintenance,
    get_stats,
    get_tools,
    init_db,
    issue_tool,
    return_tool,
    seed_demo_data,
    send_to_repair,
)


app = Flask(__name__)

init_db()
seed_demo_data()


@app.get("/")
def index():
    status = request.args.get("status", "").strip()
    search = request.args.get("search", "").strip()
    tools = get_tools(status=status or None, search=search or None)
    return render_template(
        "index.html",
        tools=tools,
        maintenance=get_maintenance(),
        stats=get_stats(),
        selected_status=status,
        search=search,
    )


@app.post("/tools")
def create_tool():
    add_tool(
        inventory_number=request.form["inventory_number"].strip(),
        name=request.form["name"].strip(),
        category=request.form["category"].strip(),
        location=request.form["location"].strip(),
        condition=request.form.get("condition", "исправен").strip() or "исправен",
    )
    return redirect(url_for("index"))


@app.post("/tools/<int:tool_id>/issue")
def issue(tool_id):
    issue_tool(
        tool_id=tool_id,
        employee=request.form["employee"].strip(),
        planned_return_at=request.form.get("planned_return_at", "").strip(),
    )
    return redirect(url_for("index"))


@app.post("/tools/<int:tool_id>/return")
def return_item(tool_id):
    return_tool(tool_id)
    return redirect(url_for("index"))


@app.post("/tools/<int:tool_id>/repair")
def repair(tool_id):
    send_to_repair(
        tool_id=tool_id,
        description=request.form["description"].strip(),
        cost=float(request.form.get("cost") or 0),
    )
    return redirect(url_for("index"))


@app.get("/api/tools")
def api_tools():
    status = request.args.get("status", "").strip()
    search = request.args.get("search", "").strip()
    tools = get_tools(status=status or None, search=search or None)
    return jsonify({"count": len(tools), "items": tools})


if __name__ == "__main__":
    app.run(debug=True)

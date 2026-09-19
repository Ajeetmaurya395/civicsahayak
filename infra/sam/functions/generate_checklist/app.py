"""Lambda function: Generate application checklist from eligibility results."""
import json


def handler(event, context):
    """Process SQS messages and generate application checklists.

    Turns a finished eligibility result into a downloadable application checklist.
    """
    for record in event.get("Records", []):
        body = json.loads(record.get("body", "{}"))

        scheme_name = body.get("scheme_name", "Unknown Scheme")
        eligibility_status = body.get("status", "UNKNOWN")
        required_documents = body.get("required_documents", [])
        user_documents = body.get("user_documents", [])
        official_url = body.get("official_application_url")

        # Generate checklist
        checklist = {
            "scheme_name": scheme_name,
            "eligibility_status": eligibility_status,
            "documents_checklist": [],
            "next_steps": [],
        }

        for doc in required_documents:
            is_uploaded = doc.lower() in [d.lower() for d in user_documents]
            checklist["documents_checklist"].append({
                "document": doc,
                "status": "uploaded" if is_uploaded else "missing",
                "required": True,
            })

        if official_url:
            checklist["next_steps"].append(f"Apply online at: {official_url}")
        else:
            checklist["next_steps"].append(
                "Official application link unavailable — view official scheme information"
            )

        missing_docs = [
            d["document"] for d in checklist["documents_checklist"]
            if d["status"] == "missing"
        ]
        if missing_docs:
            checklist["next_steps"].insert(
                0, f"Obtain missing documents: {', '.join(missing_docs)}"
            )

        print(f"Generated checklist for {scheme_name}: {json.dumps(checklist)}")

    return {"statusCode": 200, "body": "Checklists generated"}

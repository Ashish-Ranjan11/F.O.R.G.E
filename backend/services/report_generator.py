from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter


# ==========================================
# PDF REPORT GENERATOR
# ==========================================

def generate_pdf_report(
    result,
    output_path
):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    # ======================================
    # TITLE
    # ======================================

    elements.append(
        Paragraph(
            "DeepFakeConnect Forensic Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    # ======================================
    # MAIN RESULT
    # ======================================

    elements.append(
        Paragraph(
            f"<b>Prediction:</b> {result.get('prediction', 'N/A')}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Confidence:</b> {result.get('confidence', 0)}%",
            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    # ======================================
    # PARAMETER REASONING
    # ======================================

    if "parameter_contribution" in result:

        elements.append(
            Paragraph(
                "Parameter Reasoning",
                styles["Heading2"]
            )
        )

        for key, value in result[
            "parameter_contribution"
        ].items():

            text = f"""
            <b>{key.upper()}</b><br/>
            Score: {value.get('score',0)}<br/>
            Risk: {value.get('risk','N/A')}<br/>
            Reason: {value.get('reason','N/A')}<br/><br/>
            """

            elements.append(
                Paragraph(
                    text,
                    styles["BodyText"]
                )
            )

        elements.append(
            Spacer(1, 20)
        )

    # ======================================
    # FUSION ENGINE BREAKDOWN
    # ======================================

    if "fusion_breakdown" in result:

        elements.append(
            Paragraph(
                "Fusion Engine Breakdown",
                styles["Heading2"]
            )
        )

        for key, value in result[
            "fusion_breakdown"
        ].items():

            elements.append(
                Paragraph(
                    f"<b>{key.upper()}</b>: {value}",
                    styles["BodyText"]
                )
            )

        elements.append(
            Spacer(1, 20)
        )

    # ======================================
    # TEXT FORENSICS REPORT
    # ======================================

    if "full_document" in result:

        elements.append(
            Paragraph(
                "Sentence Level Analysis",
                styles["Heading2"]
            )
        )

        for item in result[
            "full_document"
        ]:

            sentence = item.get(
                "sentence",
                ""
            )

            score = item.get(
                "score",
                0
            )

            reason = item.get(
                "reason",
                ""
            )

            txt = f"""
            <b>Sentence:</b> {sentence}<br/>
            <b>AI Score:</b> {score}%<br/>
            <b>Reason:</b> {reason}<br/><br/>
            """

            elements.append(
                Paragraph(
                    txt,
                    styles["BodyText"]
                )
            )

    # ======================================
    # IMAGE FORENSICS REPORT
    # ======================================

    elif "heatmap" in result:

        elements.append(
            Paragraph(
                "Image Forensic Analysis",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Heatmap:</b> {result.get('heatmap')}",
                styles["BodyText"]
            )
        )

        elements.append(
            Spacer(1, 20)
        )

    # ======================================
    # BUILD PDF
    # ======================================

    doc.build(elements)
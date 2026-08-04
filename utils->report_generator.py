# =====================================================
# GEO COMPILER AI
# Professional AI Report Generator V5
# utils/report_generator.py
# =====================================================


import os
import json

from datetime import datetime
from pathlib import Path


from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


from reportlab.lib.styles import (
    getSampleStyleSheet
)


from reportlab.lib import colors







REPORT_TITLE = (
    "GEO COMPILER AI\n"
    "Satellite Intelligence Report"
)


REPORT_VERSION = (
    "Enterprise V5"
)








# =====================================================
# REPORT FOLDER
# =====================================================


def create_report_folder(

        folder="reports"

):


    try:


        Path(folder).mkdir(

            exist_ok=True

        )


        return folder



    except Exception:


        return folder







# =====================================================
# JSON EXPORT
# =====================================================


def save_json_report(

        report,

        filename

):


    try:


        with open(

            filename,

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                report,

                f,

                indent=4,

                default=str,

                ensure_ascii=False

            )



        return filename



    except Exception as e:


        return str(e)









# =====================================================
# AI REPORT BUILDER
# =====================================================


def generate_ai_report(

        data

):


    return {


        "title":

        REPORT_TITLE,



        "version":

        REPORT_VERSION,



        "generated":

        str(datetime.now()),



        "system":

        "Geo Compiler AI",



        "data":

        data


    }









# =====================================================
# TEXT REPORT GENERATOR
# =====================================================


def generate_text_report(

        report

):


    try:


        lines=[]



        lines.append(

            "===================================="

        )


        lines.append(

            " GEO COMPILER AI REPORT "

        )


        lines.append(

            "===================================="

        )



        lines.append("")



        def recursive_print(

                obj,

                prefix=""

        ):



            if isinstance(

                obj,

                dict

            ):


                for k,v in obj.items():


                    lines.append(

                        f"{prefix}{k}:"

                    )


                    recursive_print(

                        v,

                        prefix+"   "

                    )



            elif isinstance(

                obj,

                list

            ):


                for item in obj:


                    recursive_print(

                        item,

                        prefix+"   "

                    )



            else:


                lines.append(

                    f"{prefix}{obj}"

                )





        recursive_print(

            report

        )



        return "\n".join(

            lines

        )



    except Exception as e:


        return str(e)









# =====================================================
# PDF REPORT ENGINE
# =====================================================


def generate_pdf_report(

        report,

        filename=None

):


    try:



        if filename is None:


            create_report_folder()



            filename=os.path.join(

                "reports",

                "GeoCompiler_AI_Report.pdf"

            )






        doc=SimpleDocTemplate(

            str(filename),

            title=

            "Geo Compiler AI Report"

        )





        styles=getSampleStyleSheet()



        story=[]





        story.append(

            Paragraph(

                "GEO COMPILER AI<br/>"
                "Satellite Intelligence Report",

                styles["Title"]

            )

        )



        story.append(

            Spacer(

                1,

                20

            )

        )







        generated = [

            [

                "System",

                report.get(

                    "System",

                    "Geo Compiler AI"

                )

            ],


            [

                "Generated",

                report.get(

                    "Generated",

                    datetime.now()

                )

            ],


            [

                "Version",

                "Enterprise V5"

            ]

        ]





        table=Table(

            generated

        )



        table.setStyle(

            TableStyle([


                (

                "GRID",

                (0,0),

                (-1,-1),

                0.5,

                colors.grey

                )


            ])

        )



        story.append(

            table

        )




        story.append(

            Spacer(

                1,

                20

            )

        )







        story.append(

            Paragraph(

                "AI Analysis Summary",

                styles["Heading2"]

            )

        )






        text = generate_text_report(

            report

        )



        story.append(

            Paragraph(

                text.replace(

                    "\n",

                    "<br/>"

                ),

                styles["BodyText"]

            )

        )





        doc.build(

            story

        )



        return filename






    except Exception as e:


        return None










# =====================================================
# COMPLETE REPORT PIPELINE
# =====================================================


def generate_full_report(

        data,

        output_folder="reports"

):


    create_report_folder(

        output_folder

    )



    report=generate_ai_report(

        data

    )



    json_file=os.path.join(

        output_folder,

        "GeoCompiler_Report.json"

    )


    pdf_file=os.path.join(

        output_folder,

        "GeoCompiler_Report.pdf"

    )



    save_json_report(

        report,

        json_file

    )



    generate_pdf_report(

        report,

        pdf_file

    )



    return {


        "status":

        "SUCCESS",



        "json":

        json_file,



        "pdf":

        pdf_file


    }

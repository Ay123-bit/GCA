# =====================================================
# GEO COMPILER AI
# Environmental Recommendation Engine V5
# utils/recommendation.py
# =====================================================


import logging


logger = logging.getLogger(

    "GeoCompilerAI"

)






# =====================================================
# NDVI CONDITION ANALYZER
# =====================================================


def analyze_ndvi_condition(ndvi):


    try:


        if ndvi >= 0.7:


            return (

                "Excellent vegetation health"

            )


        elif ndvi >= 0.4:


            return (

                "Healthy vegetation condition"

            )


        elif ndvi >= 0.2:


            return (

                "Moderate vegetation condition"

            )


        elif ndvi >= 0:


            return (

                "Sparse vegetation detected"

            )


        else:


            return (

                "Water or non-vegetated surface"

            )



    except Exception:


        return (

            "Unknown NDVI condition"

        )









# =====================================================
# LAND COVER ADVICE
# =====================================================


def landcover_advice(

        landcover

):


    try:


        landcover=str(

            landcover

        ).lower()



        if "forest" in landcover:


            return (

                "Forest monitoring and biodiversity protection recommended."

            )



        elif "agriculture" in landcover:


            return (

                "Crop health monitoring and irrigation optimization recommended."

            )



        elif "water" in landcover:


            return (

                "Water resource monitoring recommended."

            )



        elif "urban" in landcover:


            return (

                "Urban expansion and heat monitoring recommended."

            )



        elif "barren" in landcover:


            return (

                "Land restoration and soil improvement recommended."

            )



        return (

            "General environmental monitoring recommended."

        )



    except Exception:


        return (

            "No land cover recommendation available."

        )









# =====================================================
# ENVIRONMENT RISK SCORE
# =====================================================


def calculate_environment_risk(

        ndvi,

        water,

        vegetation

):


    try:


        risk=0





        if ndvi < 0.2:


            risk += 30



        if vegetation < 0.3:


            risk += 30



        if water > 0.7:


            risk += 20



        if risk >=70:


            return "High"



        elif risk >=40:


            return "Medium"



        else:


            return "Low"




    except Exception:


        return "Unknown"









# =====================================================
# MAIN AI RECOMMENDATION ENGINE
# =====================================================


def generate_recommendation(

        landcover="Unknown",

        ndvi=0,

        water=0,

        vegetation=0

):


    try:



        ndvi=float(

            ndvi

        )



        water=float(

            water

        )



        vegetation=float(

            vegetation

        )





        ndvi_status = analyze_ndvi_condition(

            ndvi

        )





        land_message = landcover_advice(

            landcover

        )





        risk = calculate_environment_risk(

            ndvi,

            water,

            vegetation

        )







        recommendations=[]




        # Vegetation


        if ndvi >=0.5:


            recommendations.append(

                "Maintain current vegetation management practices."

            )


        elif ndvi <0.2:


            recommendations.append(

                "Consider ecological restoration and vegetation improvement."

            )






        # Water


        if water >0.5:


            recommendations.append(

                "Monitor water bodies and aquatic ecosystem changes."

            )







        # Urban


        if "urban" in str(

            landcover

        ).lower():


            recommendations.append(

                "Monitor urban growth and surface temperature."

            )







        # Agriculture


        if "agriculture" in str(

            landcover

        ).lower():


            recommendations.append(

                "Optimize irrigation and crop monitoring."

            )







        final_report = f"""

🌍 GEO COMPILER AI ENVIRONMENT REPORT


Land Cover:

{landcover}



NDVI Status:

{ndvi_status}



Environmental Risk:

{risk}



Primary Analysis:

{land_message}



AI Recommendations:


"""


        for r in recommendations:


            final_report += (

                "\n• "

                +

                r

            )




        if not recommendations:


            final_report += (

                "\n• Continue periodic satellite monitoring."

            )




        return final_report.strip()




    except Exception as e:


        logger.error(

            str(e)

        )


        return (

            "Recommendation engine unavailable."

        )









# =====================================================
# QUICK TEST FUNCTION
# =====================================================


def recommendation_status():


    return {


        "engine":

        "Environmental AI Recommendation Engine",



        "status":

        "Active"


    }

import pandas as pd


df = pd.read_csv("outfits.csv")


def recommend_outfits(
    style,
    event,
    season,
    preferred_color,
    detected_colors
):

    recommendations = df.copy()

    recommendations["match_score"] = 0


    # ---------------------------
    # STYLE MATCH
    # ---------------------------

    recommendations.loc[
        recommendations["style"].str.lower()
        == style.lower(),
        "match_score"
    ] += 35


    # ---------------------------
    # EVENT MATCH
    # ---------------------------

    recommendations.loc[
        recommendations["event"].str.lower()
        == event.lower(),
        "match_score"
    ] += 30


    # ---------------------------
    # SEASON MATCH
    # ---------------------------

    recommendations.loc[
        (
            recommendations["season"].str.lower()
            == season.lower()
        )
        |
        (
            recommendations["season"].str.lower()
            == "all"
        ),
        "match_score"
    ] += 15


    # ---------------------------
    # USER COLOR PREFERENCE
    # ---------------------------

    recommendations.loc[
        recommendations["color"].str.lower()
        == preferred_color.lower(),
        "match_score"
    ] += 10


    # ---------------------------
    # PHOTO COLOR MATCH
    # ---------------------------

    recommendations["photo_color_match"] = (
        recommendations["color"]
        .str.lower()
        .isin(
            [color.lower() for color in detected_colors]
        )
    )

    recommendations.loc[
        recommendations["photo_color_match"],
        "match_score"
    ] += 10


    # Sort outfits
    recommendations = recommendations.sort_values(
        by="match_score",
        ascending=False
    )

    return recommendations.head(3)
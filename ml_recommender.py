import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity

from database import get_feedback_score


class FashionRecommender:

    def __init__(self, file_path="outfits.csv"):

        self.df = pd.read_csv(file_path)

        self.features = [
            "style",
            "event",
            "season",
            "color",
            "fit"
        ]

        self.encoder = OneHotEncoder(
            handle_unknown="ignore"
        )

        self.encoder.fit(
            self.df[self.features]
        )


    def recommend(
        self,
        user_name,
        style,
        event,
        season,
        preferred_color,
        fit,
        budget,
        detected_colors
    ):

        recommendations = self.df.copy()


        # ==========================================
        # BUDGET FILTERING
        # ==========================================

        if budget == "Under ₹1000":

            recommendations = recommendations[
                recommendations["price"] < 1000
            ]


        elif budget == "₹1000 - ₹3000":

            recommendations = recommendations[
                (recommendations["price"] >= 1000)
                &
                (recommendations["price"] <= 3000)
            ]


        elif budget == "₹3000 - ₹5000":

            recommendations = recommendations[
                (recommendations["price"] >= 3000)
                &
                (recommendations["price"] <= 5000)
            ]


        elif budget == "Above ₹5000":

            recommendations = recommendations[
                recommendations["price"] > 5000
            ]


        # If no results are found
        if recommendations.empty:

            recommendations = self.df.copy()


        # ==========================================
        # CREATE USER PROFILE
        # ==========================================

        user_profile = pd.DataFrame(
            [[
                style,
                event,
                season,
                preferred_color,
                fit
            ]],
            columns=self.features
        )


        # ==========================================
        # CONVERT USER TO VECTOR
        # ==========================================

        user_vector = self.encoder.transform(
            user_profile
        )


        # ==========================================
        # CONVERT OUTFITS TO VECTORS
        # ==========================================

        outfit_vectors = self.encoder.transform(
            recommendations[self.features]
        )


        # ==========================================
        # COSINE SIMILARITY
        # ==========================================

        similarity_scores = cosine_similarity(
            user_vector,
            outfit_vectors
        ).flatten()


        recommendations = recommendations.copy()

        recommendations["match_score"] = (
            similarity_scores * 100
        )


        # ==========================================
        # PHOTO COLOR BONUS
        # ==========================================

        detected_colors_lower = [
            str(color).lower()
            for color in detected_colors
        ]


        recommendations["color_lower"] = (
            recommendations["color"]
            .astype(str)
            .str.lower()
        )


        for index, outfit in recommendations.iterrows():

            if outfit["color_lower"] in detected_colors_lower:

                recommendations.loc[
                    index,
                    "match_score"
                ] += 10


        # ==========================================
        # FEEDBACK LEARNING
        # ==========================================

        for index, outfit in recommendations.iterrows():

            feedback_score = get_feedback_score(
                user_name,
                outfit["outfit_id"]
            )

            recommendations.loc[
                index,
                "match_score"
            ] += feedback_score


        # ==========================================
        # LIMIT SCORE
        # ==========================================

        recommendations["match_score"] = (
            recommendations["match_score"]
            .clip(lower=0, upper=100)
        )


        # Remove temporary column
        recommendations = recommendations.drop(
            columns=["color_lower"]
        )


        # ==========================================
        # SORT RESULTS
        # ==========================================

        recommendations = recommendations.sort_values(
            by="match_score",
            ascending=False
        )


        return recommendations.head(3)
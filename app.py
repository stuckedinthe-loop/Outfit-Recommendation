import streamlit as st

from image_analysis import (
    analyze_image,
    get_dominant_colors,
    rgb_to_color_name
)

from ml_recommender import FashionRecommender

from database import (
    create_tables,
    save_outfit,
    save_feedback,
    get_saved_outfits
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Personal Fashion Stylist",
    page_icon="👗",
    layout="centered"
)


# ==========================================
# CREATE DATABASE
# ==========================================

create_tables()


# ==========================================
# LOAD RECOMMENDER
# ==========================================

@st.cache_resource
def load_recommender():
    return FashionRecommender("outfits.csv")


recommender = load_recommender()


# ==========================================
# TITLE
# ==========================================

st.title("👗 AI Personal Fashion Stylist")

st.write(
    "Upload your photo and get personalized "
    "AI-powered outfit recommendations!"
)


# ==========================================
# USER PROFILE
# ==========================================

st.header("👤 Your Profile")

user_name = st.text_input(
    "Enter your name"
)


# ==========================================
# PHOTO UPLOAD
# ==========================================

st.header("📸 Upload Your Photo")

uploaded_file = st.file_uploader(
    "Choose your photo",
    type=["jpg", "jpeg", "png"]
)


# ==========================================
# STYLE AND FIT
# ==========================================

col1, col2 = st.columns(2)

with col1:

    style = st.selectbox(
        "✨ Preferred Style",
        [
            "Casual",
            "Formal",
            "Traditional",
            "Elegant",
            "Trendy",
            "Streetwear"
        ]
    )


with col2:

    fit = st.selectbox(
        "👕 Preferred Fit",
        [
            "Slim",
            "Regular",
            "Oversized"
        ]
    )


# ==========================================
# EVENT AND SEASON
# ==========================================

col1, col2 = st.columns(2)

with col1:

    event = st.selectbox(
        "🎉 Event",
        [
            "College",
            "Party",
            "Wedding",
            "Interview",
            "Office",
            "Date"
        ]
    )


with col2:

    season = st.selectbox(
        "🌤️ Season",
        [
            "Summer",
            "Winter",
            "All"
        ]
    )


# ==========================================
# COLOR AND BUDGET
# ==========================================

col1, col2 = st.columns(2)

with col1:

    preferred_color = st.selectbox(
        "🎨 Preferred Color",
        [
            "Black",
            "White",
            "Blue",
            "Red",
            "Beige",
            "Grey",
            "Pastel",
            "Floral"
        ]
    )


with col2:

    budget = st.selectbox(
        "💰 Budget",
        [
            "Under ₹1000",
            "₹1000 - ₹3000",
            "₹3000 - ₹5000",
            "Above ₹5000"
        ]
    )


# ==========================================
# FIND OUTFIT BUTTON
# ==========================================

if st.button("✨ Find My Perfect Outfit", use_container_width=True):

    if user_name.strip() == "":

        st.warning("⚠️ Please enter your name.")

    elif uploaded_file is None:

        st.warning("⚠️ Please upload your photo.")

    else:

        try:

            # ==========================================
            # ANALYZE IMAGE
            # ==========================================

            image, image_array = analyze_image(
                uploaded_file
            )

            # ==========================================
            # DETECT COLORS
            # ==========================================

            dominant_colors = get_dominant_colors(
                image_array,
                num_colors=3
            )

            detected_colors = []

            for color in dominant_colors:

                color_name = rgb_to_color_name(color)

                if color_name not in detected_colors:
                    detected_colors.append(color_name)


            # ==========================================
            # GET RECOMMENDATIONS
            # IMPORTANT: ALL 8 ARGUMENTS ARE REQUIRED
            # ==========================================

            results = recommender.recommend(
                user_name,
                style,
                event,
                season,
                preferred_color,
                fit,
                budget,
                detected_colors
            )


            # ==========================================
            # SAVE DATA IN SESSION
            # ==========================================

            st.session_state["results"] = results
            st.session_state["user_name"] = user_name
            st.session_state["image"] = image
            st.session_state["detected_colors"] = detected_colors


        except Exception as e:

            st.error(f"❌ Error: {str(e)}")


# ==========================================
# DISPLAY PHOTO AND COLORS
# ==========================================

if "image" in st.session_state:

    st.markdown("---")

    st.header("📸 Your Uploaded Photo")

    st.image(
        st.session_state["image"],
        width=350
    )

    st.subheader("🎨 Colors Detected From Your Photo")

    detected_colors = st.session_state["detected_colors"]

    if detected_colors:
        st.write(" • ".join(detected_colors))
    else:
        st.write("No dominant colors detected.")


# ==========================================
# DISPLAY RECOMMENDATIONS
# ==========================================

if "results" in st.session_state:

    results = st.session_state["results"]

    st.markdown("---")

    st.header("👗 Your Top Outfit Recommendations")


    for rank, (_, outfit) in enumerate(
        results.iterrows(),
        start=1
    ):

        st.markdown("---")

        st.subheader(
            f"🏆 Recommendation #{rank}"
        )


        # ==========================================
        # OUTFIT DETAILS
        # ==========================================

        st.write(
            f"👕 **Top:** {outfit['top']}"
        )

        st.write(
            f"👖 **Bottom:** {outfit['bottom']}"
        )

        st.write(
            f"👟 **Shoes:** {outfit['shoes']}"
        )

        st.write(
            f"💍 **Accessories:** {outfit['accessories']}"
        )

        st.write(
            f"✨ **Style:** {outfit['style']}"
        )

        st.write(
            f"🎉 **Best For:** {outfit['event']}"
        )

        st.write(
            f"🌤️ **Season:** {outfit['season']}"
        )

        st.write(
            f"🎨 **Color:** {outfit['color']}"
        )

        st.write(
            f"👕 **Fit:** {outfit['fit']}"
        )

        st.write(
            f"💰 **Estimated Price: ₹{outfit['price']}**"
        )


        # ==========================================
        # COMPATIBILITY SCORE
        # ==========================================

        score = int(outfit["match_score"])

        st.write(
            f"⭐ **Compatibility Score: {score}%**"
        )

        st.progress(score)


        # ==========================================
        # SAVE AND FEEDBACK BUTTONS
        # ==========================================

        col1, col2, col3 = st.columns(3)

        current_user = st.session_state["user_name"]


        # SAVE
        with col1:

            if st.button(
                "❤️ Save",
                key=f"save_{rank}_{outfit['outfit_id']}"
            ):

                save_outfit(
                    current_user,
                    outfit
                )

                st.success("❤️ Outfit saved!")


        # LIKE
        with col2:

            if st.button(
                "👍 Like",
                key=f"like_{rank}_{outfit['outfit_id']}"
            ):

                save_feedback(
                    current_user,
                    outfit["outfit_id"],
                    "Like"
                )

                st.success("👍 Thanks for your feedback!")


        # DISLIKE
        with col3:

            if st.button(
                "👎 Dislike",
                key=f"dislike_{rank}_{outfit['outfit_id']}"
            ):

                save_feedback(
                    current_user,
                    outfit["outfit_id"],
                    "Dislike"
                )

                st.info("👎 Feedback saved!")


# ==========================================
# SAVED OUTFITS
# ==========================================

st.markdown("---")

st.header("❤️ My Saved Outfits")

if st.button("Show My Saved Outfits"):

    if user_name.strip() == "":

        st.warning(
            "⚠️ Please enter your name first."
        )

    else:

        saved_outfits = get_saved_outfits(
            user_name
        )

        if saved_outfits:

            for outfit in saved_outfits:

                st.write(
                    f"👕 **Top:** {outfit[3]}"
                )

                st.write(
                    f"👖 **Bottom:** {outfit[4]}"
                )

                st.write(
                    f"🎉 **Event:** {outfit[7]}"
                )

                st.write(
                    f"⭐ **Score:** {int(outfit[9])}%"
                )

                st.markdown("---")

        else:

            st.info(
                "You haven't saved any outfits yet."
            )
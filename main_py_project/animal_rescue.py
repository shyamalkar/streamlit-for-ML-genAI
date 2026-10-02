import streamlit as st
import streamlit as st
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
import uuid
import pandas as pd


# ============================================================
# APPLICATION CONFIGURATION . 
# ============================================================

st.set_page_config(
    page_title="Animal Rescue",
    page_icon="🐾",
    layout="wide"
)


# ============================================================
# DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    exist_ok=True
)


DATABASE = BASE_DIR / "animal_rescue.db"


# ============================================================
# CONSTANTS
# ============================================================

ANIMAL_TYPES = [
    "🐕 Dog",
    "🐈 Cat",
    "🐄 Cow",
    "🐐 Goat",
    "🐦 Bird",
    "🐒 Monkey",
    "🐎 Horse",
    "🦌 Wild Animal",
    "🐾 Other"
]


EMERGENCY_LEVELS = [
    "🔴 Critical",
    "🟠 Serious",
    "🟡 Moderate",
    "🟢 Low"
]


PROBLEM_TYPES = [
    "Accident / Injury",
    "Bleeding",
    "Sick / Weak",
    "Trapped",
    "Abandoned",
    "Animal Abuse",
    "Stray Animal in Danger",
    "Unable to Walk",
    "Other"
]


RESCUE_STATUSES = [
    "Report Submitted",
    "Rescue Team Notified",
    "Team Assigned",
    "Rescue Team On The Way",
    "Animal Rescued",
    "Treatment / Shelter",
    "Case Closed"
]


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()


    # --------------------------------------------------------
    # USERS TABLE
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT NOT NULL,

            phone TEXT,

            created_at TEXT NOT NULL

        )
        """
    )


    # --------------------------------------------------------
    # REPORTS TABLE
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            report_id TEXT UNIQUE NOT NULL,

            username TEXT NOT NULL,

            phone TEXT,

            animal_type TEXT NOT NULL,

            emergency_level TEXT NOT NULL,

            problem_type TEXT NOT NULL,

            description TEXT NOT NULL,

            image_path TEXT,

            latitude REAL,

            longitude REAL,

            location_name TEXT,

            status TEXT NOT NULL,

            created_at TEXT NOT NULL,

            updated_at TEXT NOT NULL

        )
        """
    )


    connection.commit()

    connection.close()


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# CREATE DEFAULT ADMIN
# ============================================================

def create_default_admin():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        ("admin",)
    )


    existing_admin = cursor.fetchone()


    if existing_admin is None:

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password,
                role,
                phone,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "admin",
                hash_password("admin123"),
                "admin",
                "",
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )


    connection.commit()

    connection.close()


# ============================================================
# REGISTER USER
# ============================================================

def register_user(
    username,
    password,
    phone
):

    connection = get_connection()

    cursor = connection.cursor()


    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password,
                role,
                phone,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                username,
                hash_password(password),
                "user",
                phone,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )


        connection.commit()

        return True, "Account created successfully."


    except sqlite3.IntegrityError:

        return False, "Username already exists."


    finally:

        connection.close()


# ============================================================
# LOGIN USER
# ============================================================

def login_user(
    username,
    password
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (
            username,
            hash_password(password)
        )
    )


    user = cursor.fetchone()

    connection.close()


    if user:

        return dict(user)


    return None


# ============================================================
# CREATE REPORT
# ============================================================

def create_report(
    username,
    phone,
    animal_type,
    emergency_level,
    problem_type,
    description,
    image_path,
    latitude,
    longitude,
    location_name
):

    connection = get_connection()

    cursor = connection.cursor()


    # Generate unique report ID

    report_id = (
        "AR-"
        + datetime.now().strftime("%Y%m%d")
        + "-"
        + uuid.uuid4().hex[:6].upper()
    )


    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute(
        """
        INSERT INTO reports
        (
            report_id,
            username,
            phone,
            animal_type,
            emergency_level,
            problem_type,
            description,
            image_path,
            latitude,
            longitude,
            location_name,
            status,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            report_id,
            username,
            phone,
            animal_type,
            emergency_level,
            problem_type,
            description,
            image_path,
            latitude,
            longitude,
            location_name,
            "Report Submitted",
            current_time,
            current_time
        )
    )


    connection.commit()

    connection.close()


    return report_id


# ============================================================
# GET USER REPORTS
# ============================================================

def get_user_reports(username):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM reports
        WHERE username = ?
        ORDER BY id DESC
        """,
        (username,)
    )


    reports = cursor.fetchall()

    connection.close()


    return [dict(report) for report in reports]


# ============================================================
# GET ALL REPORTS
# ============================================================

def get_all_reports():

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM reports
        ORDER BY id DESC
        """
    )


    reports = cursor.fetchall()

    connection.close()


    return [dict(report) for report in reports]


# ============================================================
# UPDATE REPORT STATUS
# ============================================================

def update_report_status(
    report_id,
    status
):

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        UPDATE reports

        SET status = ?,
            updated_at = ?

        WHERE report_id = ?
        """,
        (
            status,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            report_id
        )
    )


    connection.commit()

    connection.close()


# ============================================================
# INITIALIZE APPLICATION
# ============================================================

initialize_database()

create_default_admin()


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "username" not in st.session_state:

    st.session_state.username = None


if "role" not in st.session_state:

    st.session_state.role = None


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.title("🐾 Animal Rescue")

    st.caption(
        "Help an animal in need."
    )


    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Register"
        ]
    )


    # ========================================================
    # LOGIN
    # ========================================================

    with login_tab:

        st.subheader("🔐 Login")


        username = st.text_input(
            "Username",
            key="login_username"
        )


        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )


        if st.button(
            "Login",
            use_container_width=True
        ):

            if not username or not password:

                st.warning(
                    "Please enter username and password."
                )

            else:

                user = login_user(
                    username,
                    password
                )


                if user:

                    st.session_state.logged_in = True

                    st.session_state.username = (
                        user["username"]
                    )

                    st.session_state.role = (
                        user["role"]
                    )

                    st.success(
                        "Login successful."
                    )

                    st.rerun()


                else:

                    st.error(
                        "Invalid username or password."
                    )


        st.info(
            "Demo Rescue Team account: "
            "**admin / admin123**"
        )


    # ========================================================
    # REGISTER
    # ========================================================

    with register_tab:

        st.subheader("📝 Create Account")


        new_username = st.text_input(
            "Choose Username",
            key="register_username"
        )


        new_phone = st.text_input(
            "Phone Number",
            key="register_phone"
        )


        new_password = st.text_input(
            "Create Password",
            type="password",
            key="register_password"
        )


        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )


        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not new_username:

                st.warning(
                    "Username is required."
                )

            elif not new_phone:

                st.warning(
                    "Phone number is required."
                )

            elif not new_password:

                st.warning(
                    "Password is required."
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(new_password) < 6:

                st.warning(
                    "Password should contain "
                    "at least 6 characters."
                )

            else:

                success, message = register_user(
                    new_username,
                    new_password,
                    new_phone
                )


                if success:

                    st.success(
                        message
                    )

                else:

                    st.error(
                        message
                    )


    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🐾 Animal Rescue")


st.sidebar.write(
    f"👤 **{st.session_state.username}**"
)


if st.session_state.role == "admin":

    st.sidebar.success(
        "🚑 Rescue Team"
    )

else:

    st.sidebar.info(
        "👤 Reporter"
    )


if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False

    st.session_state.username = None

    st.session_state.role = None

    st.rerun()


# ============================================================
# ADMIN DASHBOARD
# ============================================================

if st.session_state.role == "admin":

    st.title(
        "🚑 Rescue Team Dashboard"
    )


    st.caption(
        "Monitor and manage incoming animal rescue reports."
    )


    reports = get_all_reports()


    # --------------------------------------------------------
    # DASHBOARD METRICS
    # --------------------------------------------------------

    total_reports = len(reports)


    critical_reports = sum(
        1
        for report in reports
        if report["emergency_level"]
        == "🔴 Critical"
    )


    rescued_reports = sum(
        1
        for report in reports
        if report["status"]
        == "Animal Rescued"
    )


    closed_reports = sum(
        1
        for report in reports
        if report["status"]
        == "Case Closed"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "📋 Total Reports",
            total_reports
        )


    with col2:

        st.metric(
            "🔴 Critical",
            critical_reports
        )


    with col3:

        st.metric(
            "🐾 Rescued",
            rescued_reports
        )


    with col4:

        st.metric(
            "✅ Closed",
            closed_reports
        )


    st.divider()


    # --------------------------------------------------------
    # REPORT LIST
    # --------------------------------------------------------

    st.subheader(
        "📋 Incoming Rescue Reports"
    )


    if not reports:

        st.info(
            "No rescue reports yet."
        )


    for report in reports:

        title = (
            f"{report['report_id']} | "
            f"{report['animal_type']} | "
            f"{report['emergency_level']}"
        )


        with st.expander(title):

            col1, col2 = st.columns(
                [1, 2]
            )


            # ----------------------------------------------
            # IMAGE
            # ----------------------------------------------

            with col1:

                if report["image_path"]:

                    image_path = Path(
                        report["image_path"]
                    )


                    if image_path.exists():

                        st.image(
                            str(image_path),
                            use_container_width=True
                        )

                else:

                    st.info(
                        "No image uploaded."
                    )


            # ----------------------------------------------
            # REPORT INFORMATION
            # ----------------------------------------------

            with col2:

                st.write(
                    f"**Report ID:** "
                    f"{report['report_id']}"
                )


                st.write(
                    f"**Animal:** "
                    f"{report['animal_type']}"
                )


                st.write(
                    f"**Emergency:** "
                    f"{report['emergency_level']}"
                )


                st.write(
                    f"**Problem:** "
                    f"{report['problem_type']}"
                )


                st.write(
                    f"**Reporter:** "
                    f"{report['username']}"
                )


                st.write(
                    f"**Phone:** "
                    f"{report['phone']}"
                )


                st.write(
                    f"**Description:** "
                    f"{report['description']}"
                )


                st.write(
                    f"**Location:** "
                    f"{report['location_name']}"
                )


                if (
                    report["latitude"]
                    is not None
                    and
                    report["longitude"]
                    is not None
                ):

                    st.write(
                        f"📍 Latitude: "
                        f"{report['latitude']}"
                    )

                    st.write(
                        f"📍 Longitude: "
                        f"{report['longitude']}"
                    )


                    map_data = pd.DataFrame(
                        {
                            "lat": [
                                report["latitude"]
                            ],
                            "lon": [
                                report["longitude"]
                            ]
                        }
                    )


                    st.map(
                        map_data,
                        zoom=14
                    )


                    google_maps_url = (
                        "https://www.google.com/maps/search/"
                        "?api=1&query="
                        f"{report['latitude']},"
                        f"{report['longitude']}"
                    )


                    st.markdown(
                        f"[🗺️ Open Location in Google Maps]"
                        f"({google_maps_url})"
                    )


                st.write(
                    f"**Created:** "
                    f"{report['created_at']}"
                )


                st.write(
                    f"**Current Status:** "
                    f"{report['status']}"
                )


            # ----------------------------------------------
            # STATUS UPDATE
            # ----------------------------------------------

            st.divider()


            st.write(
                "### 🔄 Update Rescue Status"
            )


            current_index = 0


            if report["status"] in RESCUE_STATUSES:

                current_index = (
                    RESCUE_STATUSES.index(
                        report["status"]
                    )
                )


            new_status = st.selectbox(
                "Status",
                RESCUE_STATUSES,
                index=current_index,
                key=f"status_{report['report_id']}"
            )


            if st.button(
                "💾 Update Status",
                key=f"update_{report['report_id']}"
            ):

                update_report_status(
                    report["report_id"],
                    new_status
                )


                st.success(
                    "Status updated successfully."
                )


                st.rerun()


# ============================================================
# NORMAL USER APPLICATION
# ============================================================

else:

    st.title(
        "🐾 Animal Rescue"
    )


    st.subheader(
        "🚨 Report an Animal in Distress"
    )


    st.write(
        """
        If you see an injured, sick, trapped or abused animal,
        submit a report so the rescue team can investigate.
        """
    )


    # ========================================================
    # REPORT FORM
    # ========================================================

    with st.form(
        "rescue_report_form",
        clear_on_submit=False
    ):

        # ----------------------------------------------------
        # ANIMAL
        # ----------------------------------------------------

        st.subheader(
            "🐾 Animal Information"
        )


        animal_type = st.selectbox(
            "Animal Type",
            ANIMAL_TYPES
        )


        emergency_level = st.selectbox(
            "Emergency Level",
            EMERGENCY_LEVELS
        )


        problem_type = st.selectbox(
            "Problem Type",
            PROBLEM_TYPES
        )


        description = st.text_area(
            "📝 Describe the situation",
            placeholder=(
                "Describe what happened, "
                "where the animal is, "
                "and its current condition..."
            ),
            height=150
        )


        # ----------------------------------------------------
        # CONTACT
        # ----------------------------------------------------

        st.subheader(
            "📞 Your Contact Information"
        )


        connection = get_connection()

        cursor = connection.cursor()


        cursor.execute(
            """
            SELECT phone
            FROM users
            WHERE username = ?
            """,
            (st.session_state.username,)
        )


        user_data = cursor.fetchone()

        connection.close()


        default_phone = (
            user_data["phone"]
            if user_data
            else ""
        )


        phone = st.text_input(
            "Phone Number",
            value=default_phone
        )


        # ----------------------------------------------------
        # IMAGE
        # ----------------------------------------------------

        st.subheader(
            "📷 Evidence / Animal Photo"
        )


        uploaded_image = st.file_uploader(
            "Upload an image",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ]
        )


        if uploaded_image:

            st.image(
                uploaded_image,
                caption="Uploaded Animal Image",
                use_container_width=True
            )


        # ----------------------------------------------------
        # LOCATION
        # ----------------------------------------------------

        st.subheader(
            "📍 Location"
        )


        st.info(
            """
            For this first version, enter the animal's
            approximate GPS coordinates. Later we can add
            automatic browser GPS detection.
            """
        )


        col1, col2 = st.columns(2)


        with col1:

            latitude = st.number_input(
                "Latitude",
                min_value=-90.0,
                max_value=90.0,
                value=0.0,
                format="%.6f"
            )


        with col2:

            longitude = st.number_input(
                "Longitude",
                min_value=-180.0,
                max_value=180.0,
                value=0.0,
                format="%.6f"
            )


        location_name = st.text_input(
            "📍 Location / Area Name",
            placeholder=(
                "Example: Contai, Purba Medinipur"
            )
        )


        # ----------------------------------------------------
        # SUBMIT
        # ----------------------------------------------------

        submitted = st.form_submit_button(
            "🚨 SUBMIT RESCUE REQUEST",
            use_container_width=True
        )


    # ========================================================
    # PROCESS REPORT
    # ========================================================

    if submitted:

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not description.strip():

            st.error(
                "❌ Please describe the situation."
            )

        elif not phone.strip():

            st.error(
                "❌ Please provide your phone number."
            )

        elif not location_name.strip():

            st.error(
                "❌ Please provide the location."
            )

        elif latitude == 0.0 and longitude == 0.0:

            st.error(
                "❌ Please enter valid coordinates."
            )

        else:

            # ------------------------------------------------
            # SAVE IMAGE
            # ------------------------------------------------

            image_path = None


            if uploaded_image:

                file_extension = Path(
                    uploaded_image.name
                ).suffix.lower()


                unique_filename = (
                    uuid.uuid4().hex
                    + file_extension
                )


                saved_path = (
                    UPLOAD_DIR
                    / unique_filename
                )


                with open(
                    saved_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_image.getbuffer()
                    )


                image_path = str(
                    saved_path
                )


            # ------------------------------------------------
            # CREATE DATABASE REPORT
            # ------------------------------------------------

            report_id = create_report(

                username=st.session_state.username,

                phone=phone,

                animal_type=animal_type,

                emergency_level=emergency_level,

                problem_type=problem_type,

                description=description,

                image_path=image_path,

                latitude=latitude,

                longitude=longitude,

                location_name=location_name
            )


            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            st.success(
                "🎉 Rescue report submitted successfully!"
            )


            st.balloons()


            st.subheader(
                "🚨 Report Details"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Report ID",
                    report_id
                )


            with col2:

                st.metric(
                    "Status",
                    "Report Submitted"
                )


            st.info(
                """
                Your report has been saved.
                The rescue team can now review the
                information and update the rescue status.
                """
            )


            google_maps_url = (
                "https://www.google.com/maps/search/"
                "?api=1&query="
                f"{latitude},{longitude}"
            )


            st.markdown(
                f"[🗺️ View Report Location on Google Maps]"
                f"({google_maps_url})"
            )


    # ========================================================
    # USER REPORT HISTORY
    # ========================================================

    st.divider()


    st.subheader(
        "📋 My Rescue Reports"
    )


    user_reports = get_user_reports(
        st.session_state.username
    )


    if not user_reports:

        st.info(
            "You haven't submitted any rescue reports yet."
        )


    else:

        for report in user_reports:

            with st.expander(
                f"{report['report_id']} — "
                f"{report['animal_type']} — "
                f"{report['status']}"
            ):

                col1, col2 = st.columns(2)


                with col1:

                    if report["image_path"]:

                        image_path = Path(
                            report["image_path"]
                        )


                        if image_path.exists():

                            st.image(
                                str(image_path),
                                use_container_width=True
                            )


                with col2:

                    st.write(
                        f"**Animal:** "
                        f"{report['animal_type']}"
                    )


                    st.write(
                        f"**Emergency:** "
                        f"{report['emergency_level']}"
                    )


                    st.write(
                        f"**Problem:** "
                        f"{report['problem_type']}"
                    )


                    st.write(
                        f"**Status:** "
                        f"{report['status']}"
                    )


                    st.write(
                        f"**Location:** "
                        f"{report['location_name']}"
                    )


                    st.write(
                        f"**Submitted:** "
                        f"{report['created_at']}"
                    )


                    if (
                        report["latitude"]
                        is not None
                        and
                        report["longitude"]
                        is not None
                    ):

                        google_maps_url = (
                            "https://www.google.com/maps/search/"
                            "?api=1&query="
                            f"{report['latitude']},"
                            f"{report['longitude']}"
                        )


                        st.markdown(
                            f"[🗺️ Open Location]"
                            f"({google_maps_url})"
                        )
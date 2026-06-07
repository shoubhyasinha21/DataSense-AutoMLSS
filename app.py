import io
import warnings
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import joblib
import time
import sqlite3
import os


from joblib import Parallel, delayed
from utils.reports import create_excel_report, create_pdf_report
from components.styles import load_css
from components.ui import hero_section
from utils.database import init_db, create_user
from utils.auth import render_auth_suite, check_session_timeout, logout_user

# machine learning imports
from sklearn.ensemble import (
    ExtraTreesClassifier, ExtraTreesRegressor, 
    AdaBoostClassifier, AdaBoostRegressor,
    RandomForestClassifier, RandomForestRegressor,
    GradientBoostingClassifier, GradientBoostingRegressor
)
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import LinearSVC, LinearSVR  # Swapped for high-speed linear variants
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, f1_score, 
    mean_absolute_error, mean_squared_error, precision_score, r2_score, recall_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

# PDF Generation Imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)

# Initialize App Configurations
warnings.filterwarnings("ignore")
st.set_page_config(page_title="DataSense AutoMLSS", layout="wide")
load_css()
init_db()

import os

ADMIN_EMAIL = os.getenv("ss21@gmail.com")
ADMIN_PASSWORD = os.getenv("kd21admin")

try:
    create_user(
        "Admin",
        ADMIN_EMAIL,
        ADMIN_PASSWORD,
        is_admin=1
    )
except:
    pass

# User Authentication Management
# --- REPLACED SECURE AUTHENTICATION MANAGEMENT ---
from utils.auth import render_auth_suite, check_session_timeout, logout_user

# Enforce background session timeout checks
check_session_timeout()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Render the new advanced multi-tab security interface if not logged in
if not st.session_state["logged_in"]:
    render_auth_suite()
    st.stop()

# If authorized, pull the user object safely
user = st.session_state["user"]

st.sidebar.success(f"Logged in as {user['name']}")
st.sidebar.info(f"Plan: {user['plan'].title()}")

if st.sidebar.button("Logout", key="main_logout_button"):
    logout_user()
    st.rerun()

hero_section()

# --- HERO VIEW UI GRID ---
st.markdown("""
<style>
.main-hero {
    padding: 70px 45px;
    border-radius: 32px;
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.35), transparent 35%),
        radial-gradient(circle at top right, rgba(168,85,247,0.35), transparent 35%),
        linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 25px 80px rgba(0,0,0,0.45);
    margin-top: 20px;
    margin-bottom: 35px;
}
.hero-badge {
    display: inline-block;
    padding: 10px 18px;
    border-radius: 999px;
    background: rgba(37,99,235,0.18);
    color: #93c5fd;
    border: 1px solid rgba(147,197,253,0.35);
    font-weight: 700;
    margin-bottom: 22px;
}
.hero-title {
    font-size: 58px;
    line-height: 1.1;
    font-weight: 900;
    margin-bottom: 20px;
    background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    font-size: 22px;
    color: #e5e7eb;
    line-height: 1.8;
    max-width: 1100px;
}
.question-card {
    margin-top: 30px;
    padding: 28px;
    border-radius: 24px;
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(255,255,255,0.1);
}
.question-card p {
    font-size: 18px;
    color: #cbd5e1;
    line-height: 1.9;
}
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 18px;
    margin-top: 28px;
}
.feature-box {
    padding: 20px;
    border-radius: 18px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    color: #e5e7eb;
    font-weight: 700;
    text-align: center;
}
.cta-box {
    margin-top: 34px;
    padding: 24px;
    border-radius: 22px;
    background: linear-gradient(135deg, #2563eb, #7c3aed, #db2777);
    color: white;
    text-align: center;
    font-size: 22px;
    font-weight: 800;
}
</style>

<div class="main-hero">
<div class="hero-badge">🚀 AI-Powered AutoML Platform</div>
<div class="hero-title">DataSense AutoMLSS Dataset Analyzer and Trainer</div>
<div class="hero-subtitle">Welcome to DataSense AutoMLSS</div>
<div class="question-card">
<p>Hey Guys! Ever been in a situation where your faculty, mentor, or project reviewer suddenly asks:</p>
<p>
✅ How many features are there in your dataset?<br>
✅ Which feature is the most important?<br>
✅ How many missing values exist?<br>
✅ What insights did you discover from the data?<br>
✅ Which ML model performed the best and why?
</p>
<p>And you're left searching through hundreds or thousands of rows? 😅</p>
<p>Don't worry — <b>DataSense AutoMLSS</b> is here to help!</p>
<p>Simply upload your CSV or Excel dataset and this platform will automatically analyze your dataset, show feature details, create visualizations, train ML models, compare results, and let you download reports and the best trained model.</p>
</div>
<div class="feature-grid">
<div class="feature-box">📊 Dataset Analysis</div>
<div class="feature-box">🔍 Feature Insights</div>
<div class="feature-box">📈 Visualizations</div>
<div class="feature-box">🤖 ML Training</div>
<div class="feature-box">🏆 Model Comparison</div>
<div class="feature-box">📥 Report Download</div>
</div>
<div class="cta-box">🎯 Perfect for students, researchers, data analysts, and ML enthusiasts.</div>
</div>
""", unsafe_allow_html=True)


# --- UTILITY PIPELINE FUNCTIONS ---

def read_file(uploaded_file):
    file_name = uploaded_file.name.lower()
    if file_name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        return pd.read_excel(uploaded_file)
    raise ValueError("Only CSV, XLSX, and XLS files are supported.")


def iqr_outlier_count(series):
    clean_series = series.dropna()
    if len(clean_series) < 4:
        return 0
    q1 = clean_series.quantile(0.25)
    q3 = clean_series.quantile(0.75)
    iqr = q3 - q1
    lower_limit = q1 - 1.5 * iqr
    upper_limit = q3 + 1.5 * iqr
    return int(((clean_series < lower_limit) | (clean_series > upper_limit)).sum())


def dataset_summary(df):
    numeric_columns = df.select_dtypes(include=np.number).columns
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns
    boolean_columns = df.select_dtypes(include="bool").columns
    total_missing = int(df.isna().sum().sum())

    return pd.DataFrame(
        {
            "Metric": [
                "Rows", "Columns / Features", "Total Cells", "Missing Values",
                "Missing Percentage", "Duplicate Rows", "Numeric Features",
                "Categorical Features", "Boolean Features", "Memory Usage MB",
            ],
            "Value": [
                df.shape[0], df.shape[1], df.size, total_missing,
                round((total_missing / max(df.size, 1)) * 100, 3),
                int(df.duplicated().sum()), len(numeric_columns),
                len(categorical_columns), len(boolean_columns),
                round(df.memory_usage(deep=True).sum() / (1024 ** 2), 3),
            ],
        }
    )


def feature_report(df):
    feature_rows = []
    for column in df.columns:
        series = df[column]
        row = {
            "Feature Name": column,
            "Data Type": str(series.dtype),
            "Non Null Count": int(series.notna().sum()),
            "Missing Count": int(series.isna().sum()),
            "Missing Percentage": round(series.isna().mean() * 100, 3),
            "Unique Values": int(series.nunique(dropna=True)),
            "Sample Values": ", ".join(map(str, series.dropna().unique()[:5])),
        }

        if pd.api.types.is_numeric_dtype(series):
            row.update(
                {
                    "Minimum": series.min(), "Maximum": series.max(),
                    "Mean": series.mean(), "Median": series.median(),
                    "Standard Deviation": series.std(), "Skewness": series.skew(),
                    "Kurtosis": series.kurtosis(), "Outlier Count IQR": iqr_outlier_count(series),
                }
            )
        else:
            value_counts = series.value_counts(dropna=True)
            row.update(
                {
                    "Most Common Value": value_counts.index[0] if len(value_counts) > 0 else None,
                    "Most Common Count": int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                }
            )
        feature_rows.append(row)
    return pd.DataFrame(feature_rows)


def infer_task_type(target_series):
    if pd.api.types.is_numeric_dtype(target_series):
        unique_count = target_series.nunique(dropna=True)
        if unique_count <= 20:
            return "Classification"
        return "Regression"
    return "Classification"


def create_preprocessor(X, num_strategy="median"):
    numeric_columns = X.select_dtypes(include=np.number).columns.tolist()
    categorical_columns = [col for col in X.columns if col not in numeric_columns]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy=num_strategy)),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_columns),
            ("categorical", categorical_pipeline, categorical_columns),
        ]
    )
    return preprocessor, numeric_columns, categorical_columns


def get_models(task_type):
    """Optimized Hyperparameters for Accelerated Execution Times"""
    if task_type == "Classification":
        return {
            "Logistic Regression": LogisticRegression(max_iter=500, solver="lbfgs"),
            "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=8),
            "Random Forest": RandomForestClassifier(random_state=42, n_estimators=60, max_depth=10, n_jobs=-1),
            "Extra Trees": ExtraTreesClassifier(random_state=42, n_estimators=60, max_depth=10, n_jobs=-1),
            "Gradient Boosting": GradientBoostingClassifier(random_state=42, n_estimators=50, max_depth=4),
            "AdaBoost": AdaBoostClassifier(random_state=42, n_estimators=40),
            "KNN": KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
            "SVM": LinearSVC(random_state=42, max_iter=1000, dual="auto"), # Fast Linear Approximator
        }
    return {
        "Linear Regression": LinearRegression(n_jobs=-1),
        "Decision Tree": DecisionTreeRegressor(random_state=42, max_depth=8),
        "Random Forest": RandomForestRegressor(random_state=42, n_estimators=60, max_depth=10, n_jobs=-1),
        "Extra Trees": ExtraTreesRegressor(random_state=42, n_estimators=60, max_depth=10, n_jobs=-1),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42, n_estimators=50, max_depth=4),
        "AdaBoost": AdaBoostRegressor(random_state=42, n_estimators=40),
        "KNN": KNeighborsRegressor(n_neighbors=5, n_jobs=-1),
        "SVR": LinearSVR(random_state=42, max_iter=1000, dual="auto"), # Fast Linear Approximator
    }


def train_single_model(model_name, model, preprocessor, X_train, X_test, y_train, y_test, task_type, label_encoder):
    try:
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", model),
        ])

        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)

        if task_type == "Classification":
            result = {
                "Model": model_name,
                "Accuracy": accuracy_score(y_test, predictions),
                "Precision Weighted": precision_score(y_test, predictions, average="weighted", zero_division=0),
                "Recall Weighted": recall_score(y_test, predictions, average="weighted", zero_division=0),
                "F1 Weighted": f1_score(y_test, predictions, average="weighted", zero_division=0),
            }
        else:
            result = {
                "Model": model_name,
                "MAE": mean_absolute_error(y_test, predictions),
                "RMSE": np.sqrt(mean_squared_error(y_test, predictions)),
                "R2 Score": r2_score(y_test, predictions),
            }

        trained_model = {
            "pipeline": pipeline, "X_test": X_test, "y_test": y_test,
            "predictions": predictions, "label_encoder": label_encoder,
        }
        return result, model_name, trained_model
    except Exception as error:
        return {"Model": model_name, "Error": str(error)}, model_name, None


def train_models(df, target_column, task_type, test_size, num_strategy="median"):
    X = df.drop(columns=[target_column])
    y = df[target_column]

    valid_rows = y.notna()
    X = X.loc[valid_rows]
    y = y.loc[valid_rows]
    label_encoder = None

    if task_type == "Classification":
        label_encoder = LabelEncoder()
        y = label_encoder.fit_transform(y.astype(str))
    else:
        y = pd.to_numeric(y, errors="coerce")
        valid_rows = ~pd.isna(y)
        X = X.loc[valid_rows]
        y = y.loc[valid_rows]

    if len(X) < 5:
        raise ValueError("Dataset is too small after cleaning target column.")

    preprocessor, numeric_columns, categorical_columns = create_preprocessor(X, num_strategy=num_strategy)
    models = get_models(task_type)
    stratify_value = None

    if task_type == "Classification":
        unique_classes, class_counts = np.unique(y, return_counts=True)
        if len(unique_classes) > 1 and class_counts.min() >= 2:
            stratify_value = y

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=stratify_value,
    )

    # Fast Concurrent Map execution utilizing max CPU cores (-1)
    outputs = Parallel(n_jobs=-1, backend="loky")(
        delayed(train_single_model)(
            model_name, model, preprocessor, X_train, X_test, y_train, y_test, task_type, label_encoder,
        )
        for model_name, model in models.items()
    )

    results = []
    trained_models = {}
    for result, model_name, trained_model in outputs:
        results.append(result)
        if trained_model is not None:
            trained_models[model_name] = trained_model

    return pd.DataFrame(results), trained_models, numeric_columns, categorical_columns


def shorten_text(value, max_length=60):
    value = str(value)
    if len(value) > max_length:
        return value[:max_length] + "..."
    return value


def make_pdf_table(df, max_rows=25, max_cols=6, max_text_length=60):
    safe_df = df.copy()
    if len(safe_df) > max_rows:
        safe_df = safe_df.head(max_rows)
    if len(safe_df.columns) > max_cols:
        safe_df = safe_df.iloc[:, :max_cols]

    safe_df = safe_df.map(lambda x: shorten_text(x, max_text_length))
    data = [safe_df.columns.astype(str).tolist()] + safe_df.values.tolist()

    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def calculate_dataset_health(df):
    total_cells = df.size
    total_rows = len(df)

    missing_percentage = (df.isna().sum().sum() / max(total_cells, 1)) * 100
    duplicate_percentage = (df.duplicated().sum() / max(total_rows, 1)) * 100

    numeric_columns = df.select_dtypes(include=np.number).columns
    total_outliers = 0
    total_numeric_values = 0

    for column in numeric_columns:
        series = df[column].dropna()
        if len(series) > 4:
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            lower_limit = q1 - 1.5 * iqr
            upper_limit = q3 + 1.5 * iqr
            outliers = ((series < lower_limit) | (series > upper_limit)).sum()
            total_outliers += outliers
            total_numeric_values += len(series)

    outlier_percentage = (total_outliers / max(total_numeric_values, 1)) * 100
    missing_score = max(0, 100 - missing_percentage * 2)
    duplicate_score = max(0, 100 - duplicate_percentage * 2)
    outlier_score = max(0, 100 - outlier_percentage)

    health_score = round((missing_score * 0.45) + (duplicate_score * 0.30) + (outlier_score * 0.25), 2)

    if health_score >= 85:
        health_status = "Excellent"
        health_message = "Your dataset looks very clean and ready for ML."
    elif health_score >= 70:
        health_status = "Good"
        health_message = "Your dataset is usable but may need minor cleaning."
    elif health_score >= 50:
        health_status = "Average"
        health_message = "Your dataset needs cleaning before serious model training."
    else:
        health_status = "Poor"
        health_message = "Your dataset has major quality issues and needs preprocessing."

    health_df = pd.DataFrame(
        {
            "Health Factor": ["Missing Values", "Duplicate Rows", "Numeric Outliers", "Overall Health Score"],
            "Percentage / Score": [
                round(missing_percentage, 2), round(duplicate_percentage, 2),
                round(outlier_percentage, 2), health_score,
            ],
        }
    )
    return health_score, health_status, health_message, health_df


# --- ADVANCED FEATURE DEFINITIONS ---

def plot_feature_importance(best_pipeline, numeric_cols, categorical_cols):
    model = best_pipeline.named_steps["model"]
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        feat_names = numeric_cols + [f"Category_Feature_{i}" for i in range(len(importances) - len(numeric_cols))]
        
        importance_df = pd.DataFrame({
            "Feature": feat_names[:len(importances)],
            "Importance Value": importances
        }).sort_values(by="Importance Value", ascending=False).head(10)
        
        fig = px.bar(importance_df, x="Importance Value", y="Feature", orientation="h",
                     title="🔥 Top 10 Features Driving Predictions", color="Importance Value",
                     color_continuous_scale="Blugrn", template="plotly_dark")
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
        return fig
    return None


def log_training_run(user_email, target, task, best_model, metric_score):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS training_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT, target_column TEXT, task_type TEXT,
                best_model TEXT, score REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute(
            "INSERT INTO training_history (email, target_column, task_type, best_model, score) VALUES (?, ?, ?, ?, ?)",
            (user_email, target, task, best_model, metric_score)
        )
        conn.commit()
        conn.close()
    except:
        pass


# --- MAIN INTERACTIVE WORKFLOW ---

uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx", "xls"])

if uploaded_file is None:
    st.info("Upload a CSV or Excel file to start.")
    st.stop()

df = read_file(uploaded_file)

st.header("1. Dataset Preview")
st.dataframe(df.head(100), width="stretch")

st.header("2. Dataset Summary")
summary_df = dataset_summary(df)
st.dataframe(summary_df, width="stretch")

st.header("3. Feature Details")
feature_df = feature_report(df)
st.success(f"This dataset has {df.shape[1]} features / columns.")

st.dataframe(
    feature_df,
    use_container_width=True,
    hide_index=True
)

fig_feature = px.imshow(
    feature_df.isnull(),
    title="Feature Details Missing Data Map",
    color_continuous_scale="Purples",
    aspect="auto"
)

fig_feature.update_layout(
    height=600,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
)

st.plotly_chart(
    fig_feature,
    use_container_width=True,
    config={
        "displayModeBar": True,
        "displaylogo": False,
        "toImageButtonOptions": {
            "format": "png",
            "filename": "feature_details",
            "height": 900,
            "width": 1400,
            "scale": 2,
        },
    },
)

st.header("4. Dataset Health")
health_score, health_status, health_message, health_df = calculate_dataset_health(df)
st.metric("Health Score", f"{health_score}/100")
st.info(health_message)
st.dataframe(health_df, width="stretch")

st.header("5. Missing Values and Duplicate Rows")
left_col, right_col = st.columns(2)

with left_col:
    missing_values = df.isna().sum().sort_values(ascending=False)
    missing_values = missing_values[missing_values > 0]
    st.subheader("Missing Values Per Feature")
    if len(missing_values) > 0:
        st.bar_chart(missing_values)
    else:
        st.write("No missing values found.")

with right_col:
    st.subheader("Duplicate Rows")
    st.metric("Duplicate Rows", int(df.duplicated().sum()))

st.header("6. Automatic Visualizations")

numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
categorical_columns = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

def show_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=30, r=30, t=70, b=30),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "scrollZoom": True,
            "toImageButtonOptions": {
                "format": "png",
                "filename": "datasense_chart",
                "height": 900,
                "width": 1400,
                "scale": 2,
            },
        },
    )


if len(numeric_columns) > 0:
    st.subheader("Numeric Feature Distribution")

    selected_numeric = st.selectbox(
        "Select numeric feature",
        numeric_columns,
        key="numeric_distribution_select"
    )

    chart_type = st.selectbox(
        "Select numeric chart type",
        [
            "Histogram",
            "Box Plot",
            "Violin Plot",
            "Density Histogram",
            "ECDF Plot",
            "Strip Plot",
        ],
        key="numeric_chart_type"
    )

    if chart_type == "Histogram":
        fig = px.histogram(
            df,
            x=selected_numeric,
            marginal="box",
            title=f"Distribution of {selected_numeric}",
        )

    elif chart_type == "Box Plot":
        fig = px.box(
            df,
            y=selected_numeric,
            points="outliers",
            title=f"Box Plot of {selected_numeric}",
        )

    elif chart_type == "Violin Plot":
        fig = px.violin(
            df,
            y=selected_numeric,
            box=True,
            points="all",
            title=f"Violin Plot of {selected_numeric}",
        )

    elif chart_type == "Density Histogram":
        fig = px.histogram(
            df,
            x=selected_numeric,
            histnorm="probability density",
            nbins=40,
            title=f"Density Histogram of {selected_numeric}",
        )

    elif chart_type == "ECDF Plot":
        fig = px.ecdf(
            df,
            x=selected_numeric,
            title=f"ECDF Plot of {selected_numeric}",
        )

    else:
        fig = px.strip(
            df,
            y=selected_numeric,
            title=f"Strip Plot of {selected_numeric}",
        )

    show_chart(fig)


if len(numeric_columns) >= 2:
    st.subheader("Relationship Between Numeric Features")

    col_x, col_y = st.columns(2)

    with col_x:
        x_feature = st.selectbox(
            "Select X feature",
            numeric_columns,
            key="scatter_x_feature"
        )

    with col_y:
        y_feature = st.selectbox(
            "Select Y feature",
            numeric_columns,
            index=1 if len(numeric_columns) > 1 else 0,
            key="scatter_y_feature"
        )

    relation_chart = st.selectbox(
        "Select relationship chart",
        [
            "Scatter Plot",
            "Bubble Plot",
            "Trendline Scatter",
            "2D Density Heatmap",
        ],
        key="relationship_chart_type"
    )

    if relation_chart == "Scatter Plot":
        fig = px.scatter(
            df,
            x=x_feature,
            y=y_feature,
            title=f"{x_feature} vs {y_feature}",
        )

    elif relation_chart == "Bubble Plot":
        size_feature = st.selectbox(
            "Select bubble size feature",
            numeric_columns,
            key="bubble_size_feature"
        )

        fig = px.scatter(
            df,
            x=x_feature,
            y=y_feature,
            size=size_feature,
            title=f"{x_feature} vs {y_feature} Bubble Plot",
        )

    elif relation_chart == "Trendline Scatter":
        fig = px.scatter(
            df,
            x=x_feature,
            y=y_feature,
            trendline="ols",
            title=f"{x_feature} vs {y_feature} With Trendline",
        )

    else:
        fig = px.density_heatmap(
            df,
            x=x_feature,
            y=y_feature,
            title=f"2D Density Heatmap: {x_feature} vs {y_feature}",
        )

    show_chart(fig)


if len(numeric_columns) >= 2:
    st.subheader("Correlation Heatmap")

    correlation = df[numeric_columns].corr(numeric_only=True)

    fig_corr = px.imshow(
        correlation,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap",
        color_continuous_scale="RdBu_r",
    )

    show_chart(fig_corr)


if len(categorical_columns) > 0:
    st.subheader("Categorical Feature Visualizations")

    selected_category = st.selectbox(
        "Select categorical feature",
        categorical_columns,
        key="categorical_feature_select"
    )

    category_chart_type = st.selectbox(
        "Select categorical chart type",
        [
            "Bar Chart",
            "Pie Chart",
            "Donut Chart",
            "Treemap",
        ],
        key="categorical_chart_type"
    )

    value_count_df = df[selected_category].value_counts().head(20).reset_index()
    value_count_df.columns = [selected_category, "Count"]

    if category_chart_type == "Bar Chart":
        fig = px.bar(
            value_count_df,
            x=selected_category,
            y="Count",
            title=f"Top Categories in {selected_category}",
        )

    elif category_chart_type == "Pie Chart":
        fig = px.pie(
            value_count_df,
            names=selected_category,
            values="Count",
            title=f"Category Share of {selected_category}",
        )

    elif category_chart_type == "Donut Chart":
        fig = px.pie(
            value_count_df,
            names=selected_category,
            values="Count",
            hole=0.45,
            title=f"Donut Chart of {selected_category}",
        )

    else:
        fig = px.treemap(
            value_count_df,
            path=[selected_category],
            values="Count",
            title=f"Treemap of {selected_category}",
        )

    show_chart(fig)


if len(categorical_columns) > 0 and len(numeric_columns) > 0:
    st.subheader("Category vs Numeric Analysis")

    col_cat, col_num = st.columns(2)

    with col_cat:
        selected_category_2 = st.selectbox(
            "Select category",
            categorical_columns,
            key="category_numeric_category"
        )

    with col_num:
        selected_numeric_2 = st.selectbox(
            "Select numeric value",
            numeric_columns,
            key="category_numeric_value"
        )

    cat_num_chart = st.selectbox(
        "Select category vs numeric chart",
        [
            "Box Plot",
            "Violin Plot",
            "Average Bar Chart",
            "Strip Plot",
        ],
        key="category_numeric_chart"
    )

    temp_df = df[[selected_category_2, selected_numeric_2]].dropna().copy()

    top_categories = temp_df[selected_category_2].value_counts().head(10).index
    temp_df = temp_df[temp_df[selected_category_2].isin(top_categories)]

    if cat_num_chart == "Box Plot":
        fig = px.box(
            temp_df,
            x=selected_category_2,
            y=selected_numeric_2,
            title=f"{selected_numeric_2} by {selected_category_2}",
        )

    elif cat_num_chart == "Violin Plot":
        fig = px.violin(
            temp_df,
            x=selected_category_2,
            y=selected_numeric_2,
            box=True,
            title=f"{selected_numeric_2} Distribution by {selected_category_2}",
        )

    elif cat_num_chart == "Average Bar Chart":
        avg_df = (
            temp_df
            .groupby(selected_category_2)[selected_numeric_2]
            .mean()
            .reset_index()
            .sort_values(selected_numeric_2, ascending=False)
        )

        fig = px.bar(
            avg_df,
            x=selected_category_2,
            y=selected_numeric_2,
            title=f"Average {selected_numeric_2} by {selected_category_2}",
        )

    else:
        fig = px.strip(
            temp_df,
            x=selected_category_2,
            y=selected_numeric_2,
            title=f"{selected_numeric_2} Strip Plot by {selected_category_2}",
        )

    show_chart(fig)

if len(numeric_columns) > 0:
    st.subheader("Numeric Feature Distribution")
    selected_numeric = st.selectbox("Select numeric feature", numeric_columns)
    histogram = px.histogram(df, x=selected_numeric, marginal="box", title=f"Distribution of {selected_numeric}")
    st.plotly_chart(histogram, width="stretch")

    if len(numeric_columns) >= 2:
        st.subheader("Correlation Heatmap")
        correlation = df[numeric_columns].corr(numeric_only=True)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(correlation, annot=False, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

if len(categorical_columns) > 0:
    st.subheader("Categorical Feature Counts")
    selected_category = st.selectbox("Select categorical feature", categorical_columns)
    value_count_df = df[selected_category].value_counts().head(20).reset_index()
    value_count_df.columns = [selected_category, "Count"]
    category_chart = px.bar(value_count_df, x=selected_category, y="Count", title=f"Top categories in {selected_category}")
    st.plotly_chart(category_chart, width="stretch")

st.header("7. Model Training Setup")
col1, col2 = st.columns(2)
with col1:
    target_column = st.selectbox("Select target column", df.columns)
    suggested_task = infer_task_type(df[target_column])
    task_type = st.radio(
        "Problem type", ["Classification", "Regression"], index=0 if suggested_task == "Classification" else 1
    )
with col2:
    num_strategy = st.selectbox("Missing Value Numerical Imputation Strategy", ["median", "mean", "most_frequent"])
    test_size = st.slider("Validation Holdout Size (Test size)", min_value=0.1, max_value=0.4, value=0.2, step=0.05)

if st.button("Train Models"):
    with st.spinner("⚡ Hyper-threaded parallel engines processing models..."):
        start_time = time.time()
        result_df, trained_models, used_numeric, used_categorical = train_models(
            df, target_column, task_type, test_size, num_strategy=num_strategy
        )
        training_time = time.time() - start_time
        st.success(f"⚡ Training completed in {training_time:.2f} seconds")
        
    st.session_state["result_df"] = result_df
    st.session_state["trained_models"] = trained_models
    st.session_state["task_type"] = task_type
    st.session_state["target_column"] = target_column
    st.session_state["used_numeric"] = used_numeric
    st.session_state["used_categorical"] = used_categorical

# --- DASHBOARD VISUALIZATION AND METRICS COUPLING ---
if "result_df" in st.session_state:
    result_df = st.session_state["result_df"]
    trained_models = st.session_state["trained_models"]
    task_type = st.session_state["task_type"]
    target_column = st.session_state["target_column"]
    used_numeric = st.session_state["used_numeric"]
    used_categorical = st.session_state["used_categorical"]

    st.subheader("Model Results")
    st.dataframe(result_df, width="stretch")

    if len(trained_models) == 0:
        st.error("No model trained successfully. Please choose another target column.")
        st.stop()

    if task_type == "Classification":
        clean_result_df = result_df.dropna(subset=["F1 Weighted"])
        best_model_name = clean_result_df.sort_values("F1 Weighted", ascending=False).iloc[0]["Model"]
        top_metric = clean_result_df.sort_values("F1 Weighted", ascending=False).iloc[0]["F1 Weighted"]
    else:
        clean_result_df = result_df.dropna(subset=["R2 Score"])
        best_model_name = clean_result_df.sort_values("R2 Score", ascending=False).iloc[0]["Model"]
        top_metric = clean_result_df.sort_values("R2 Score", ascending=False).iloc[0]["R2 Score"]

    log_training_run(user["email"], target_column, task_type, best_model_name, float(top_metric))

    best_data = trained_models[best_model_name]
    best_pipeline = best_data["pipeline"]
    X_test = best_data["X_test"]
    y_test = best_data["y_test"]
    predictions = best_data["predictions"]
    label_encoder = best_data.get("label_encoder")

    st.success(f"🥇 Dominant Selected Paradigm Model: {best_model_name}")

    st.subheader("🔮 Predictive Attribute Significance (Feature Importance)")
    importance_chart = plot_feature_importance(best_pipeline, used_numeric, used_categorical)
    if importance_chart:
        st.plotly_chart(importance_chart, width="stretch")
    else:
        st.info("Feature importance extraction is specialized for Tree-based models (Random Forest, Extra Trees, etc.).")

    st.subheader("Prediction Sample")
    prediction_df = X_test.copy()

    if task_type == "Classification" and label_encoder is not None:
        prediction_df["Actual"] = label_encoder.inverse_transform(y_test)
        prediction_df["Predicted"] = label_encoder.inverse_transform(predictions)
    else:
        prediction_df["Actual"] = y_test.values
        prediction_df["Predicted"] = predictions

    st.dataframe(prediction_df.head(50), width="stretch")

    st.header("8. Result Visualizations")
    st.subheader("Model Performance Comparison")

    if task_type == "Classification":
        metric_options = [col for col in ["Accuracy", "Precision Weighted", "Recall Weighted", "F1 Weighted"] if col in result_df.columns]
    else:
        metric_options = [col for col in ["MAE", "RMSE", "R2 Score"] if col in result_df.columns]

    selected_metric = st.selectbox("Select Metric", metric_options, key="metric_selector")
    comparison_chart = st.selectbox("Select Comparison Chart Type", ["Bar Chart", "Line Chart", "Area Chart"], key="comparison_chart_selector")

    if comparison_chart == "Bar Chart":
        fig = px.bar(result_df, x="Model", y=selected_metric, title=f"{selected_metric} Comparison", text_auto=True)
    elif comparison_chart == "Line Chart":
        fig = px.line(result_df, x="Model", y=selected_metric, markers=True, title=f"{selected_metric} Comparison")
    else:
        fig = px.area(result_df, x="Model", y=selected_metric, title=f"{selected_metric} Comparison")
    st.plotly_chart(fig, width="stretch")

    st.subheader("Actual vs Predicted Visualization")

    if task_type == "Classification":
        chart_type = st.radio(
            "Select Visualization", ["Actual vs Predicted Class Distribution", "Prediction Count Pie Chart"],
            horizontal=True, key="classification_chart_type",
        )
        st.success(f"You selected: {chart_type}")

        if chart_type == "Actual vs Predicted Class Distribution":
            actual_counts = prediction_df["Actual"].value_counts().reset_index()
            actual_counts.columns = ["Class", "Actual Count"]
            predicted_counts = prediction_df["Predicted"].value_counts().reset_index()
            predicted_counts.columns = ["Class", "Predicted Count"]
            distribution_df = pd.merge(actual_counts, predicted_counts, on="Class", how="outer").fillna(0)
            fig_result = px.bar(distribution_df, x="Class", y=["Actual Count", "Predicted Count"], barmode="group", title="Actual vs Predicted Class Distribution")
        else:
            pie_df = prediction_df["Predicted"].value_counts().reset_index()
            pie_df.columns = ["Predicted Class", "Count"]
            fig_result = px.pie(pie_df, names="Predicted Class", values="Count", title="Predicted Class Share")
        st.plotly_chart(fig_result, width="stretch")
    else:
        chart_type = st.radio(
            "Select Visualization",
            ["Line Chart", "Scatter Plot", "Histogram", "Box Plot", "Area Chart", "Violin Plot", "Density Histogram", "Residual Scatter Plot", "Residual Histogram", "Sorted Actual vs Predicted", "Cumulative Comparison"],
            horizontal=True, key="regression_chart_type",
        )
        st.success(f"You selected: {chart_type}")

        if chart_type == "Line Chart":
            chart_df = prediction_df[["Actual", "Predicted"]].head(100).reset_index()
            fig_result = px.line(chart_df, x="index", y=["Actual", "Predicted"], title="Actual vs Predicted Line Chart")
        elif chart_type == "Scatter Plot":
            fig_result = px.scatter(prediction_df, x="Actual", y="Predicted", title="Actual vs Predicted Scatter Plot")
        elif chart_type == "Histogram":
            fig_result = px.histogram(prediction_df, x=["Actual", "Predicted"], nbins=30, barmode="overlay", title="Actual vs Predicted Histogram")
        elif chart_type == "Box Plot":
            fig_result = px.box(prediction_df, y=["Actual", "Predicted"], title="Actual vs Predicted Box Plot")
        elif chart_type == "Area Chart":
            chart_df = prediction_df[["Actual", "Predicted"]].head(100).reset_index()
            fig_result = px.area(chart_df, x="index", y=["Actual", "Predicted"], title="Actual vs Predicted Area Chart")
        elif chart_type == "Violin Plot":
            fig_result = px.violin(prediction_df, y=["Actual", "Predicted"], box=True, title="Actual vs Predicted Violin Plot")
        elif chart_type == "Density Histogram":
            fig_result = px.histogram(prediction_df, x=["Actual", "Predicted"], nbins=30, histnorm="probability density", barmode="overlay", title="Actual vs Predicted Density Histogram")
        elif chart_type == "Residual Scatter Plot":
            residual_df = prediction_df.copy()
            residual_df["Residual"] = residual_df["Actual"] - residual_df["Predicted"]
            fig_result = px.scatter(residual_df, x="Predicted", y="Residual", title="Residual Scatter Plot")
        elif chart_type == "Residual Histogram":
            residual_df = prediction_df.copy()
            residual_df["Residual"] = residual_df["Actual"] - residual_df["Predicted"]
            fig_result = px.histogram(residual_df, x="Residual", nbins=30, title="Residual Histogram")
        elif chart_type == "Sorted Actual vs Predicted":
            sorted_df = prediction_df[["Actual", "Predicted"]].sort_values("Actual").head(200).reset_index()
            fig_result = px.line(sorted_df, x="index", y=["Actual", "Predicted"], title="Sorted Actual vs Predicted")
        else:
            cumulative_df = prediction_df[["Actual", "Predicted"]].head(200).copy()
            cumulative_df["Actual"] = cumulative_df["Actual"].cumsum()
            cumulative_df["Predicted"] = cumulative_df["Predicted"].cumsum()
            cumulative_df = cumulative_df.reset_index()
            fig_result = px.line(cumulative_df, x="index", y=["Actual", "Predicted"], title="Cumulative Actual vs Predicted")
        st.plotly_chart(fig_result, width="stretch")

    classification_report_df = None

    if task_type == "Classification":
        st.subheader("Classification Report")
        unique_test_labels = np.unique(np.concatenate([y_test, predictions]))
        target_names = label_encoder.inverse_transform(unique_test_labels) if label_encoder is not None else None

        report = classification_report(
            y_test, predictions, labels=unique_test_labels, target_names=target_names, output_dict=True, zero_division=0
        )
        classification_report_df = pd.DataFrame(report).transpose()
        st.dataframe(classification_report_df, width="stretch")

        st.subheader("Confusion Matrix")
        cm = confusion_matrix(y_test, predictions, labels=unique_test_labels)
        fig_cm, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(cm, annot=True, fmt="d", ax=ax)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        st.pyplot(fig_cm)

    st.header("9. Download Outputs")
    model_bytes = io.BytesIO()
    joblib.dump(best_pipeline, model_bytes)

    st.download_button(
        label="Download Best Model (.joblib)",
        data=model_bytes.getvalue(),
        file_name="best_model.joblib",
        mime="application/octet-stream",
    )

    report_bytes = create_excel_report(
        summary_df=summary_df, feature_df=feature_df, result_df=result_df,
        prediction_df=prediction_df, classification_report_df=classification_report_df,
    )
    st.download_button(
        label="Download Full Excel Report",
        data=report_bytes,
        file_name="full_ml_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    pdf_bytes = create_pdf_report(
        summary_df=summary_df, feature_df=feature_df, result_df=result_df,
        target_column=target_column, task_type=task_type, best_model_name=best_model_name,
        prediction_df=prediction_df, classification_report_df=classification_report_df,
    )
    st.download_button(
        label="Download PDF Report",
        data=pdf_bytes,
        file_name="datasense_automlss_report.pdf",
        mime="application/pdf",
    )

    # --- SOCIALS AND CONNECT ENGINE ---
    st.markdown("""
<div style="
margin-top:30px;
margin-bottom:20px;
padding:35px;
border-radius:24px;
background:rgba(255,255,255,0.05);
backdrop-filter:blur(20px);
-webkit-backdrop-filter:blur(20px);
border:1px solid rgba(255,255,255,0.1);
box-shadow:0 8px 32px rgba(0,0,0,0.3);
text-align:center;
">
<h1 style="margin-bottom:10px;font-size:36px;background:linear-gradient(90deg,#60a5fa,#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:800;">
🚀 Connect With The Creator
</h1>
<p style="font-size:18px;color:#cbd5e1;margin-bottom:25px;">
Built by <b>Shoubhya Sinha</b><br>
ML Engineer • Data Scientist • AI Developer
</p>
<a href="https://www.linkedin.com/in/shoubhya-sinha-135199380/" target="_blank" style="display:inline-block;padding:14px 30px;background:linear-gradient(135deg,#0ea5e9,#2563eb);color:white;font-size:18px;font-weight:700;border-radius:14px;text-decoration:none;box-shadow:0 8px 25px rgba(37,99,235,0.4);">
💼 Connect on LinkedIn
</a>
<p style="margin-top:20px;color:#94a3b8;font-size:14px;">Let's collaborate on AI, Machine Learning, Data Science, and Research Projects.</p>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div style="margin-top:40px;padding:38px;border-radius:28px;background:linear-gradient(135deg,rgba(37,99,235,0.18),rgba(168,85,247,0.18));border:1px solid rgba(255,255,255,0.12);box-shadow:0 20px 60px rgba(0,0,0,0.35);">
<h1 style="font-size:46px;font-weight:900;text-align:center;background:linear-gradient(90deg,#60a5fa,#a78bfa,#f472b6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">
🎯 Complete Dataset Analysis & ML Workflow
</h1>
<p style="text-align:center;font-size:18px;color:#cbd5e1;margin-bottom:35px;">A premium A-Z explanation of how DataSense AutoMLSS analyzes, trains, compares, and exports your ML project.</p>
<div style="padding:25px;border-radius:22px;background:rgba(15,23,42,0.75);border:1px solid rgba(255,255,255,0.1);margin-bottom:25px;">
<h2 style="color:#38bdf8;">🚀 Why This Project?</h2>
<p style="font-size:17px;color:#e5e7eb;line-height:1.8;">Hey Guys! Ever been in a situation where your faculty, mentor, or project reviewer suddenly asks:</p>
<ul style="font-size:17px;color:#e5e7eb;line-height:2;">
<li> How many features are there in your dataset?</li>
<li> Which feature is the most important?</li>
<li> How many missing values exist?</li>
<li> What insights did you discover from the data?</li>
<li> Which model performed the best and why?</li>
<li> What preprocessing techniques did you apply?</li>
<li> How did you handle missing values and categorical data?</li>
</ul>
<p style="font-size:17px;color:#e5e7eb;line-height:1.8;">Don’t worry — <b style="color:#60a5fa;">DataSense AutoMLSS</b> is here to help!</p>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px;margin-top:25px;">
<div style="padding:24px;border-radius:20px;background:linear-gradient(135deg,#0f172a,#1e293b);border:1px solid rgba(96,165,250,0.25);">
<h3 style="color:#60a5fa;">📂 Dataset Understanding</h3>
<p style="color:#cbd5e1;line-height:1.8;">
1. Dataset uploaded by user.<br>2. Dataset loaded using Pandas.<br>3. Rows and columns identified.<br>4. Dataset preview generated.<br>5. Missing values checked.<br>6. Duplicate records detected.<br>7. Memory usage analyzed.<br>8. Dataset structure explored.
</p>
</div>
<div style="padding:24px;border-radius:20px;background:linear-gradient(135deg,#111827,#312e81);border:1px solid rgba(167,139,250,0.25);">
<h3 style="color:#a78bfa;">🔍 Feature Analysis</h3>
<p style="color:#cbd5e1;line-height:1.8;">
9. Every feature analyzed.<br>10. Feature names extracted.<br>11. Data types identified.<br>12. Unique values calculated.<br>13. Missing percentage calculated.<br>14. Sample values displayed.<br>15. Numeric statistics generated.<br>16. Outliers detected using IQR.
</p>
</div>
<div style="padding:24px;border-radius:20px;background:linear-gradient(135deg,#0f172a,#064e3b);border:1px solid rgba(52,211,153,0.25);">
<h3 style="color:#34d399;">📊 Data Visualization</h3>
<p style="color:#cbd5e1;line-height:1.8;">
17. Missing value charts created.<br>18. Feature distributions generated.<br>19. Box plots displayed.<br>20. Correlation heatmap created.<br>21. Category charts generated.<br>22. Interactive visualizations displayed.
</p>
</div>
<div style="padding:24px;border-radius:20px;background:linear-gradient(135deg,#111827,#7c2d12);border:1px solid rgba(251,146,60,0.25);">
<h3 style="color:#fb923c;">⚙️ Data Preprocessing</h3>
<p style="color:#cbd5e1;line-height:1.8;">
23. Target column selected: <b>{target_column}</b>.<br>24. Problem type selected: <b>{task_type}</b>.<br>25. Train-test split performed.<br>26. Numeric missing values filled.<br>27. Categorical missing values filled.<br>28. One-Hot Encoding applied.<br>29. StandardScaler applied.
</p>
</div>
<div style="padding:24px;border-radius:20px;background:linear-gradient(135deg,#0f172a,#581c87);border:1px solid rgba(216,180,254,0.25);">
<h3 style="color:#d8b4fe;">🤖 Machine Learning</h3>
<p style="color:#cbd5e1;line-height:1.8;">
30. Multiple ML models initialized.<br>31. Models trained automatically.<br>32. Predictions generated.<br>33. Performance evaluated.<br>34. Accuracy, Precision, Recall, F1 calculated.<br>35. Regression metrics calculated if needed.<br>36. Best model selected automatically after training.
</p>
</div>
<div style="padding:24px;border-radius:20px;background:linear-gradient(135deg,#111827,#831843);border:1px solid rgba(244,114,182,0.25);">
<h3 style="color:#f472b6;">📥 Export & Reports</h3>
<p style="color:#cbd5e1;line-height:1.8;">
37. Excel report generated.<br>38. PDF report generated.<br>39. Dataset summary exported.<br>40. Feature analysis exported.<br>41. Model results exported.<br>42. Best trained model downloadable.<br>43. Ready for viva and presentation.
</p>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="margin-top:35px;padding:32px;border-radius:24px;background:linear-gradient(135deg,#2563eb,#7c3aed,#db2777);text-align:center;box-shadow:0 18px 50px rgba(124,58,237,0.35);">
<h2 style="color:white;font-size:34px;">🏆 Final Outcome</h2>
<p style="color:white;font-size:18px;line-height:2;">
✅ Understand your dataset completely<br>✅ Answer faculty questions confidently<br>✅ Identify important features and insights<br>✅ Compare multiple ML models automatically<br>✅ Download professional reports<br>✅ Save the best trained model<br>✅ Complete an end-to-end ML workflow with a single upload
</p>
<h2 style="color:white;margin-top:20px;">🚀 Upload → Analyze → Visualize → Train → Compare → Download → Present</h2>
</div>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div style="text-align:center;padding:30px;color:#64748b;font-size:15px;">
🚀 <b>DataSense AutoMLSS</b><br><br>
AI-Powered Dataset Analyzer • AutoML • Report Generator<br><br>
Built with ❤️ by <a href="https://www.linkedin.com/in/shoubhya-sinha-135199380/" target="_blank">Shoubhya Sinha</a><br><br>
© 2026 DataSense AutoMLSS
</div>
""", unsafe_allow_html=True)

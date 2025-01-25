import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import helper 
from itertools import combinations
from collections import Counter

# Load the dataset
@st.cache_data
def load_data():
    file_path = "jobs_data_preprocessed.csv"  
    df= pd.read_csv(file_path)
    df['job_id'] = df['job_id'].astype(str)
    return df

def preprocess(df):
    df['rating'] = df['rating'].replace('missing', np.nan)
    df['rating'] = df['rating'].astype(float)
    df['min_experience'] = df['experience'].str.extract(r'(\d+)-').astype(float)
    df['max_experience'] = df['experience'].str.extract(r'-(\d+)').astype(float)
    df['min_salary'] = df['salary'].str.extract(r'(\d+\.?\d*)-')[0].astype(float)
    df['max_salary'] = df['salary'].str.extract(r'-(\d+\.?\d*)')[0].astype(float)
    return df


df = load_data()
Job_Role_list=helper.job_role_list(df)
skill_list=helper.skill_list(df)

# Title and Description
st.sidebar.title("Job Analyzer")
st.sidebar.write("Explore job market trends, including roles, companies, locations, salaries, and skills.")

# Sidebar for navigation
menu = st.sidebar.radio(
    "Select Analysis Section",
    ["Dataset Overview", "Job Role Analysis", "Company Analysis", "Location Analysis", "Skill Analysis", "Salary Analysis", "Experience Analysis"]
)

# Dataset Overview
if menu == "Dataset Overview":
    
    st.header("Dataset Overview")
    st.dataframe(df)
    st.write("Shape of the dataset:", df.shape)
    st.write("Summary Statistics:")
    st.write(df.describe(include="all"))

# Job Role Analysis
elif menu == "Job Role Analysis":
    # Top job roles
    st.header("Job Role Analysis")
    st.subheader("Top 50 Job Roles")
    jobRole_df = df["job_role"].value_counts().sort_values(ascending = False).reset_index()
    st.dataframe(jobRole_df[0:51])
    
    # Figure
    st.write("                 ")
    job_role_counts = jobRole_df.head(30)
    fig=plt.figure(figsize=(10,6))
    sns.barplot(x=job_role_counts["job_role"], y=job_role_counts["count"], palette="viridis")
    plt.title("Top 30 Most Common Job Roles")
    plt.xlabel("Job roles")
    plt.ylabel("Number of Job Listings")
    plt.xticks(rotation=90)
    st.pyplot(fig)

    Job_Role_list=helper.job_role_list(df)
    
    # selected_jobrole = st.sidebar.selectbox("Select Job_Role",Job_Role_list,placeholder='choose the Job Role')
    
 
    st.header("Search for a specific Job Role")
    selected_role=st.selectbox("Select Job_Role",Job_Role_list,placeholder='choose the Job Role')
    if(selected_role=='Overall'):
        role_df=jobRole_df
        st.dataframe(role_df)
    else:
        role_df=jobRole_df[jobRole_df['job_role']==selected_role]
        st.table(role_df)

    # company by job role
    job_role_by_company = df.groupby([ 'job_role','company']).size().reset_index(name='count').sort_values(['job_role','count'], ascending= [True,False])
    st.subheader("Companies by Job Role")
    if(selected_role=='Overall'):
        role_company_df=job_role_by_company
        st.dataframe(role_company_df)
    else:
        role_company_df=job_role_by_company[job_role_by_company['job_role']==selected_role]
        st.dataframe(role_company_df)

    # Location for Job Role
    role_location = df.groupby(['job_role', 'location']).size().reset_index(name='count')
    st.subheader("Location for Job Role")
    if(selected_role=='Overall'):
        role_location_df=role_location
        st.dataframe(role_location_df)
    else:
        role_location_df=role_location[role_location['job_role'] == selected_role].sort_values('count', ascending=False)
        st.dataframe(role_location_df)



# Company Analysis
elif menu == "Company Analysis":
    df = preprocess(df)
    Company_list=helper.company_list(df)
    selected_company = st.sidebar.selectbox("Select Company",Company_list,placeholder='choose the Company')
    st.header("Company Analysis")
    top_companies = df['company'].value_counts().sort_values(ascending = False).reset_index()[1:51]

    st.write("Top 30 Companies with Most Job Listings:")
    company_counts = top_companies.head(30)
    fig=plt.figure(figsize=(10,6))
    sns.barplot(x=company_counts["company"], y=company_counts["count"], palette="coolwarm")
    plt.title("Top 30 Companies by Number of Job Listings")
    plt.xlabel("Number of Job Listings")
    plt.ylabel("Companies")
    plt.xticks(rotation=90)
    plt.show()
    st.pyplot(fig)
    
    st.subheader("Top 50 Companies with most job listings:")
    st.dataframe(top_companies)
    
    # Average Rating of a Company
    company_ratings = df.groupby('company')['rating'].mean().sort_values(ascending=False)
    job_role_by_company = df.groupby(['company', 'job_role']).size().reset_index(name='count')
    locations_by_company = df.groupby(['company', 'location']).size().reset_index(name='count')
    
    if(selected_company==' '):
        pass
    elif(selected_company=='Overall'):
       st.subheader(f"Rating of Companies:")
       st.dataframe(company_ratings)
       st.subheader(f"Job_Roles offer by Companies:")
       st.dataframe(job_role_by_company)
       st.subheader(f"Locations for Companies")
       st.dataframe(locations_by_company)
    else:
        rating=company_ratings[selected_company]
        st.subheader(f"Rating of '{selected_company}' is:")
        st.markdown(f"**{rating:.2f}**")


        # Job role offered by Company
        st.subheader(f"Job_Roles offer by '{selected_company}':")
        Job_role_for_company = job_role_by_company[job_role_by_company['company'] == selected_company].sort_values(by='count', ascending=False)
        st.dataframe(Job_role_for_company)


        # locations for a specific company
        st.subheader(f"Locations for '{selected_company}':")
        locations_for_company = locations_by_company[locations_by_company['company'] == selected_company].sort_values(by='count', ascending=False)
        st.dataframe(locations_for_company)


     
# Location Analysis
elif menu == "Location Analysis":
    st.header("Location Analysis")
    location_distribution = df['location'].str.lower().str.split(',').explode().value_counts().sort_values(ascending = False).head(20).reset_index()

    # Plot the top 10 locations with the most jobs
    st.write("Top 20 Locations with Most Jobs:")
    fig=plt.figure(figsize=(10, 6))
    sns.barplot(x=location_distribution["location"], y=location_distribution["count"], palette="coolwarm")
    plt.title('Top 20 Locations with Most Job Listings')
    plt.xlabel('Location')
    plt.ylabel('Number of Jobs')
    plt.xticks(rotation=75)
    plt.show()
    st.pyplot(fig)

    # Remote Work Opportunities
    st.subheader("Remote Work Opportunities")
    remote_jobs = df[df['location'].str.contains('Remote|Work From Home|WFH|wfo|remote', na=False, case=False)]
    percentage_remote = (len(remote_jobs) / len(df)) * 100
    st.write(f"Percentage of remote jobs: **{percentage_remote:.2f}%**")
    st.dataframe(remote_jobs['job_role'].value_counts())
        

# Skill Analysis
elif menu == "Skill Analysis":
    df1=preprocess(df)
    st.header("Skill Analysis")  
    skills_df = df['skills'].str.lower().str.split(',').explode().value_counts().sort_values(ascending = False).reset_index()
    st.dataframe(skills_df)
    skills_count=skills_df.head(50).reset_index()
   
    st.subheader("Top Skills")
    fig=plt.figure(figsize=(14,6))
    plt.bar(skills_count['skills'], skills_count['count'])
    plt.title('Top 20 skills')
    plt.xlabel('Skills')
    plt.ylabel('Frequency')
    plt.xticks(rotation=90)
    plt.show()
    st.pyplot(fig)

    # Skills for Job_role
    st.subheader("Skills by job Role")
    selected_role=st.selectbox("Select Job_Role",Job_Role_list,placeholder='select the Job Role')
    skills_for_role = df[df['job_role'].str.contains(selected_role, na=False)]['skills']
    skills=skills_for_role .str.lower().str.split(',').explode().value_counts().sort_values(ascending = False).head(31).reset_index()
    if(selected_role==' '):
        pass
    else:
        st.write(f"Top Skills require for {selected_role}:")
        st.table(skills)

    # skills with Average salary

    
    # Top skills for Freshers
    st.subheader("Top Skills for freshers")
    fresher_jobs = df1[df1['min_experience'] <= 1]
    skills_for_freshers_df = fresher_jobs['skills'].str.lower().str.split(',').explode().value_counts().sort_values(ascending = False)

    st.dataframe(skills_for_freshers_df.head(100))

   # Top Skill Combinations
    st.subheader("Top Skill Combinations")
    all_skill_sets = df['skills'].dropna().str.split(',')
    skill_combinations = []
    for skills in all_skill_sets:
        skills = [skill.strip() for skill in skills]
        skill_combinations.extend(combinations(skills, 3))

    combination_counts = Counter(skill_combinations)
    combination_counts_df = pd.DataFrame(combination_counts.items(), columns=['Skill Combination', 'Frequency']).sort_values(by='Frequency', ascending=False)
    st.dataframe(combination_counts_df.head(10))


# Salary Analysis
elif menu == "Salary Analysis":
    df1=preprocess(df)
    st.header("Salary Analysis")
    # Distribution of Salary
    st.subheader("Distribution of Salary")
    fig=plt.figure(figsize=(10, 6))
    sns.histplot(df1['min_salary'], bins=20, kde=True, color='blue')
    plt.title("Distribution of Minimum Salary")
    plt.xlabel("Salary (in Lacs)")
    plt.ylabel("Frequency")
    plt.show()
    st.pyplot(fig)

    # Plot the distribution of maximum salary
    fig=plt.figure(figsize=(10, 6))
    sns.histplot(df1['max_salary'], bins=20, kde=True, color='green')
    plt.title("Distribution of Maximum Salary")
    plt.xlabel("Salary (in Lacs)")
    plt.ylabel("Frequency")
    plt.show()
    st.pyplot(fig)

    # Average salary by job_role
    st.subheader("Average min and max salary for a job role")
    salary_by_role = df.groupby('job_role')[['min_salary', 'max_salary']].mean().sort_values('min_salary', ascending=False).reset_index()
    selected_role=st.selectbox("Select Job_Role",Job_Role_list,placeholder='choose the Job Role')
    if(selected_role==' ' or selected_role=='Overall'):
        st.dataframe(salary_by_role)
    else:
        salary_for_role= salary_by_role[salary_by_role['job_role'] == selected_role]
        st.dataframe(salary_for_role)

    #salary offer by Company
    st.subheader("Salary offers by Companies")
    salary_by_company = df.groupby('company')[['min_salary', 'max_salary']].mean().sort_values('min_salary', ascending=False)
    st.dataframe(salary_by_company)
    
    # Jobs Offering a Salary Above a Threshold
    st.subheader(" Jobs Offering a Salary Above a Threshold(in Lacs)")
    range=st.slider("Select a Threshold", min_value=0, max_value=90)
    st.write(f"Jobs above {range} Lac min salary")
    high_salary_jobs = df[df['min_salary'] > range]
    salary_df=high_salary_jobs[['job_role', 'company', 'min_salary', 'max_salary']].sort_values('min_salary', ascending=True)
    st.dataframe(salary_df)


# Experience Analysis
elif menu == "Experience Analysis":
    df1=preprocess(df)
    st.header("Experience Analysis")
    
    st.write("Experience Requirements Distribution:")
    fig=plt.figure(figsize=(10, 6))
    sns.histplot(df1['min_experience'], bins=10, kde=True, color='blue')
    plt.title("Distribution of Minimum Experience Requirements")
    plt.xlabel("Years of Experience")
    plt.ylabel("Frequency")
    plt.show()
    st.pyplot(fig)

    #Average Experience Requirement by Job Role
    st.subheader("Average Experience Requirement for Job Roles(in year)")
    experience_by_role = df1.groupby('job_role')[['min_experience', 'max_experience']].mean().round(0).sort_values('min_experience', ascending=False).reset_index()
    selected_role=st.selectbox("Select Job_Role",Job_Role_list,placeholder='choose the Job Role')
    if(selected_role==' ' or selected_role=='Overall'):
        st.dataframe(experience_by_role)
    else:
        experience_for_role= experience_by_role[experience_by_role['job_role'] == selected_role]
        st.dataframe(experience_for_role)

    # Top Job roles for Fresher (0–1 Year of Experience)
    st.subheader("Top Job roles for Fresher (0–1 Year of Experience)")
    fresher_jobs = df1[df1['min_experience'] <= 1]
    fresher_job_roles = fresher_jobs['job_role'].value_counts()
    st.dataframe(fresher_job_roles.head(50))

    #Freshers vs Experienced Job Opportunities
    st.subheader("Freshers vs Experienced Job Opportunities")
    freshers_jobs = df1[df1['min_experience'] <= 1]
    experienced_jobs = df1[df1['min_experience'] > 1]

    st.markdown(f"Jobs for Freshers: **{len(freshers_jobs)}**")
    st.markdown(f"Jobs for Experienced Candidates: **{len(experienced_jobs)}**")


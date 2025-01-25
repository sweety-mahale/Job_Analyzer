def job_role_list(df):
    Job_Role_list = df['job_role'].unique().tolist()
    Job_Role_list.sort()
    Job_Role_list.insert(0, 'Overall')
    Job_Role_list.insert(0, ' ')
    return Job_Role_list

def company_list(df):
    Company_list= df['company'].unique().tolist()
    Company_list.sort()
    Company_list.insert(0, 'Overall')
    Company_list.insert(0, ' ')
    return Company_list

def skill_list(df):
    skills_df = df['skills'].str.lower().str.split(',').explode()
    skill_list= skills_df.unique().tolist()
    skill_list.sort()
    skill_list.insert(0, 'Overall')
    skill_list.insert(0, ' ')
    return skill_list

#def generate_word_cloud():

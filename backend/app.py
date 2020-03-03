import streamlit as st
import pandas as pd
import itertools

@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv('mock_job_samples.csv',sep=',')
    df['skills_as_list'] = df['skills'].apply(lambda x: x.split(','))
    return df

def filter_skills(row, artists):
    if len(set(artists).intersection(row)) > 0:
        return True
    return False

def main():
    # Will only run once if already cached
    df = load_data()

    st.header('Job Ads dashboard')
    dedication = st.sidebar.selectbox("Choose your age: ", df['job_type'].unique())

    # convert
    unique_skills = list(set(list(itertools.chain(*df['skills_as_list'].tolist()))))
    artists = st.sidebar.multiselect("Select your skills", unique_skills)

    filtered_df = df[(df['skills_as_list'].apply(lambda x: filter_skills(x, artists))) & (df['job_type'] == dedication)]
    for job_index, job_ad in enumerate(filtered_df.itertuples()):
        # st.write(job_ad)
        st.markdown('### {}. Job dedication: {}'.format(job_index + 1, job_ad.job_type))
        st.markdown('*{}*'.format(job_ad.job_description))
        st.markdown('**Skills:** {}'.format(job_ad.skills))

if __name__ == "__main__":
    main()

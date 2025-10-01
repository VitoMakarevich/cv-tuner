# About
This repository contains a GenAI application designed to optimize and tailor CVs.  

## Motivation
**All statements are supported by [links](#links) and are not merely personal opinions.**  

As of 2025, the highest rejection rate (98%) occurs not during recruiter, behavioral, or technical interviews, but at the CV screening stage.  
On average, a candidate needs to submit 51 resumes to secure a job. Key reasons include:  

1. **[ATS (Applicant Tracking Systems)](https://en.wikipedia.org/wiki/Applicant_tracking_system)** – Each company has unique configurations, expectations, and requirements. Some demand a 99% match, expecting candidates to have worked on nearly identical projects, while others value passion and minimal coding experience. In reality, 98% of large companies use ATS tools, and 75% of resumes are rejected before reaching a human reviewer.  
2. **Recruiters** – Human reviewers are often even less consistent than ATSs. Frequently, after about 10 seconds, a recruiter may decide “other candidates’ experience aligns more closely.”  

## Solution
Companies like [Amazon](https://www.aboutamazon.com/news/workplace/amazon-job-application-resume-writing-tips) and [Google](https://www.youtube.com/watch?v=BYUy1yvjHxE) recommend tailoring your resume to each specific job description.  

I agree with this approach, although it can feel unfair that sophisticated systems can reject candidates in seconds while job seekers must spend significant time customizing their resumes. To address this, I developed a tool that automates resume tailoring.  

## Price
Good news - it’s almost free to use.  

As of September 2025, I’ve primarily been using GPT-5-mini or GPT-5, which works exceptionally well for this task.  
Processing ~240,000 tokens for 100 requests costs around $0.81, making the cost per resume **less than $0.01**.


## Usage Instructions
The tool allows full customization - you can make your CV polite and professional, follow Big Tech guidelines, or even adopt a more creative “pirate” style that makes it look like you’ve been in a role for years. The choice is yours, though we recommend staying mostly honest.

The tool is distributed as a Python package, offering two usage options:  

### UI-Based
The simplest way to use the tool is via Docker:  
```bash
docker run --platform linux/amd64 -p 8501:8501 ghcr.io/vitomakarevich/cv-tuner:latest
```
Then open the local [web page](http://localhost:8501) to use the app.  

The application runs fully locally and does **not** store any of your data.  
However, note that the **AI provider may process and store your input**.  

- [UI instruction manual](./tool_description.md)  
- You can download generated data directly from the UI or access the full debug version at [streamlit_output](./streamlit_output/).  

### Programmatic Usage
You can also run the tool programmatically using a [test script](./tests/test_real.py).  
Provide your real experience, job description, and configure rules in the [template folder](./template/).  
The tool will process this data and generate the output in [output](./output).  

## Links
1. [Resume statistics: Study, recruiter survey, and analysis of 25,000 resumes | Jan 2023](https://standout-cv.com/usa/stats-usa/resume-statistics#percentage-of-resumes)

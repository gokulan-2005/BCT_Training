from crewai import Task

def jd_task(agent, jd):
    return Task(
        description=f"Extract key skills and requirements from this job description:\n{jd}",
        agent=agent,
        expected_output="List of required skills and responsibilities"
    )

def candidate_task(agent, profile):
    return Task(
        description=f"Extract skills and experience from this candidate profile:\n{profile}",
        agent=agent,
        expected_output="Candidate skill set and experience"
    )

def match_task(agent, jd_output, candidate_output):
    return Task(
        description=f"Compare job requirements:\n{jd_output}\n\nwith candidate skills:\n{candidate_output}\n\nIdentify matches and gaps.",
        agent=agent,
        expected_output="Skill match analysis with gaps"
    )

def decision_task(agent, match_output):
    return Task(
        description=f"Based on this evaluation:\n{match_output}\n\nProvide hiring recommendation.",
        agent=agent,
        expected_output="Hire / Reject with reasoning"
    )
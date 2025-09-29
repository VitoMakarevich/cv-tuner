from pydantic import BaseModel


class Education(BaseModel):
    """Higher education block."""

    institution: str
    location: str
    degree: str
    duration: str


class Experience(BaseModel):
    """Work experience block."""

    title: str
    duration: str
    company: str
    location: str
    descriptions: list[str]


class Skills(BaseModel):
    """Hard skills block."""

    languages: list[str]
    frameworks: list[str]
    databases: list[str]
    cloud_devops: list[str]
    data_engineering: list[str]
    tools_technologies: list[str]


class Language(BaseModel):
    """Natural language knowledge block."""

    name: str
    proficiency: str


class CVData(BaseModel):
    """Root class holding all parameters."""

    name: str
    title: str
    phone: str
    description: str
    email: str
    linkedin: str
    linkedin_url: str
    github: str
    github_url: str
    educations: list[Education]
    experiences: list[Experience]
    skills: Skills
    languages: list[Language]

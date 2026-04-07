from enum import Enum
from pydantic import BaseModel,Field
from typing import Optional

class IssuePriority(str,Enum):
    low="low"
    medium="medium"
    high="high"

class IssueStatus(str,Enum):
    open="open"
    in_progress="in_progress"
    closed="closed"

class createIssue(BaseModel):
    title:str=Field(min_length=5,max_length=100)
    description:str=Field(min_length=5,max_length=1000)
    priority:IssuePriority=IssuePriority.medium
    status:IssueStatus=IssueStatus.open

class updateIssue(BaseModel):
    title:Optional[str]=Field(default=None,max_length=100)
    description:Optional[str]=Field(default=None,max_length=1000)
    priority:Optional[IssuePriority]=None
    status:Optional[IssueStatus]=None

class getIssues(BaseModel):
    id:str
    title:str
    description:str
    priority:IssuePriority
    status:IssueStatus


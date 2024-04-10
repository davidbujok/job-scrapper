import { Job as JobType } from "../Interfaces"

interface JobComponentProps {
  job: JobType;
}

export default function JobComponent({ job }: JobComponentProps) {

  return (
    <>
      <div className="flex-col">
        <h1>{job.title}</h1>
        <h2>{job.position}</h2>
        <h3>{job.location}</h3>
        <a href={job.url}>Website Link</a>
        <div className="">
        <p>{job.about}</p>
        </div>
      </div>
    </>
  )
}

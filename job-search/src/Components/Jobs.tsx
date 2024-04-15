import { Dispatch, useEffect } from "react"
import { Job as JobType } from "../Interfaces";


interface JobsProps {
  setJob: Dispatch<React.SetStateAction<JobType | null>>;
  setJobs: Dispatch<React.SetStateAction<JobType[]>>;
  jobs: JobType[];
}

const Jobs = ({ setJob, jobs, setJobs }: JobsProps) => {


  async function fetchJobs() {
    const response = await fetch("http://127.0.0.1:5000/jobs");
    const jobs = await response.json()
    setJobs(jobs)
  }

  async function fetchJuniorJobs() {
    const response = await fetch("http://127.0.0.1:5000/junior_jobs");
    const junior_jobs = await response.json()
    setJobs(junior_jobs)
  }

  const toggleToggle = (index: number) => {
    const jobsCopy = [...jobs]
    const job = jobsCopy[index]
    console.log(job.apply_status)
    job.apply_status = job.apply_status ? false : true
    console.log(job.apply_status)
    jobsCopy[index] = job
    setJobs(jobsCopy)
  }

  useEffect(() => {
    fetchJobs()
  }, [])


  return (
    <>
      {jobs?.map((job, index) => (
        <div onClick={() => setJob(job)} key={job.id} className="mb-2">
          <div className="flex justify-between">
            <p className="overflow-hidden">{job.title} | {job.company} | {job.post_date}
              {/*<input className="ml-3" onClick={() => toggleToggle(index)} type="checkbox"></input>*/}
            </p>
          </div>
        </div>
      ))
      }
    </>
  )
}

export default Jobs
